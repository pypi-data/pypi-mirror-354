# Model Execution

## Design Approrach

### Hybrid Python/C++ Architecture

Vajra implements a hybrid architecture where Python and C++ code coexist within the same model definition. Critical path computations can seamlessly delegate to C++ implementations while maintaining Python's flexibility for boilerplate operations.

```python
class LlamaAttention(nn.Module):
    def __init__(self, ...):
        # Python handles configuration, weight setup, HF compatibility
        self.qkv_proj = ColumnParallelLinear(...)
        self.rotary_emb = get_rope(...)
        
        # C++ native handle for performance-critical execution
        if use_native_execution_backend:
            self.native_handle = LlamaAttentionC(
                self.q_size, self.kv_size, self.scaling, layer_id,
                self.qkv_proj.native_handle,
                self.o_proj.native_handle,
                self.rotary_emb.native_handle
            )
    
    @use_native_backend  # Seamless delegation to C++
    def forward(self, positions, hidden_states, kv_cache):
        # This can run in either Python or C++ transparently
        qkv = self.qkv_proj(hidden_states)
        q, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        q, k = self.rotary_emb(positions, q, k)
        attn_output = AttentionWrapper.forward(q, k, v, kv_cache, self.layer_id)
        return self.o_proj(attn_output)
```

**Hybrid Benefits**:
- **Python Side**: Handles model definition, weight loading, HuggingFace compatibility, configuration
- **C++ Side**: Executes performance-critical forward passes using PyTorch C++ API
- **Seamless Integration**: Same PyTorch tensors used by both, zero conversion overhead
- **Identical Structure**: C++ mirrors Python exactly, enabling easy debugging and validation

### Dual-Path Strategy

Vajra implements two execution paths to balance performance and compatibility:

**Native C++ Path (Preferred)**:
- Minimizes CPU dispatch overhead

**Python Fallback Path**:
- Broad model compatibility using PyTorch ecosystem
- Automatic fallback for unsupported architectures

### Execution Architecture

```
┌─────────────────────────────────────────────────────┐
│                 LLMModelRunner                      │
│         (Orchestration & Pipeline)                  │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   C++ Path  │  │Python Path  │  │   Sampler   │
│ (Preferred) │  │ (Fallback)  │  │(C++/Python) │
└─────────────┘  └─────────────┘  └─────────────┘
```

## Model Runner Architecture

### Core Abstraction

The `BaseModelRunner` provides a unified interface regardless of execution path:

```cpp
class BaseModelRunner {
public:
    virtual PreparedInputs PrepareInputs(
        const Sequences& seqs,
        const SequenceMetadataVector& seq_metadata_list) const = 0;
        
    virtual SamplerOutputs Run(
        const Sequences& seqs,
        const SequenceMetadataVector& seq_metadata_list,
        std::vector<torch::Tensor>& gpu_caches) = 0;
};
```

### Pipeline Parallelism Integration

The model runner handles pipeline parallelism coordination:
- **First Stage**: Processes token inputs and sends hidden states
- **Middle Stages**: Receive and forward hidden states  
- **Last Stage**: Receives hidden states and performs sampling

Stream-based communication enables overlap between computation and communication for optimal pipeline utilization.

## Attention Mechanism Architecture

### Why Attention is Different

Unlike other layers that use simple matrix multiplications or activation kernels, attention requires complex kernel initialization and sequence-specific optimization:

- **Kernel Initialization**: FlashInfer requires per-batch initialization with `plan` methods
- **Sequence Heterogeneity**: Mixed batches of prefill/decode sequences with varying lengths  
- **Memory Layout**: Different optimal memory arrangements for different sequence types
- **Performance Sensitivity**: Attention computation is critical for performance, especially with long context scenarios

### Singleton Pattern for AttentionWrapper

**Design Challenge**: FlashInfer kernels need expensive initialization for each batch, but we want to reuse initialized kernels across calls.

**Solution**: Thread-local singleton pattern provides kernel reuse while maintaining thread safety:

```cpp
class AttentionWrapper {
    static thread_local AttentionWrapperPtr instance_;
    
public:
    static AttentionWrapperPtr GetOrCreateThreadLocalInstance() {
        if (!instance_) {
            instance_ = std::make_shared<AttentionWrapper>();
        }
        return instance_;
    }
    
    void BeginForward(const SequenceMetadataVector& seq_metadata_list);
    torch::Tensor Forward(query, key, value, kv_cache, layer_id);
    void EndForward();
};
```

### Hierarchical Sequence Arrangement

**Core Problem**: Different sequence types require different FlashInfer kernel schedules (`plan` invocations) for optimal performance. Mixing incompatible sequences hurts performance.

**Solution**: Hierarchical arrangement system that groups sequences by multiple characteristics:

```
SequenceArrangement
├── Prefill (num_q_tokens > 1)
│   ├── LengthBasedArrangement  
│   │   ├── Long Sequences (> threshold)
│   │   │   ├── SaveKvCache=true
│   │   │   │   ├── KVP Requests
│   │   │   │   └── Non-KVP Requests
│   │   │   └── SaveKvCache=false
│   │   │       ├── KVP Requests  
│   │   │       └── Non-KVP Requests
│   │   └── Short Sequences (<= threshold)
│   │       └── [Similar nested structure]
│   └── [Similar nested structure]
└── Decode (num_q_tokens = 1)
    └── [Similar nested structure]
```
**Arrangement Hierarchy**:
1. **SequenceArrangement**: Separates prefill (multi-token) vs decode (single-token)
2. **LengthBasedSequenceArrangement**: Separates long vs short sequences
3. **SaveKvCacheBasedSequenceArrangement**: Separates by KV cache persistence
4. **SequenceGroupArrangement**: Separates KVP vs non-KVP requests

Based on the sequence arrangement request in a batch are ordered, so that inputs for each flashinfer wrapper are contiguous in memory.