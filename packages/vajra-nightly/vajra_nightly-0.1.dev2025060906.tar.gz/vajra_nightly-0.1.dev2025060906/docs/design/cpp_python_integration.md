# C++/Python Integration

## Introduction

The C++/Python integration in Vajra is a strategic architectural decision that enables the system to leverage the performance of C++ for critical paths while maintaining the flexibility and ecosystem of Python for orchestration and configuration. This section demonstrates how the native handle system, combined with careful interface design, creates a seamless bridge between the two languages that powers the entire inference engine.

## Why Two Languages?

Vajra's dual-language architecture addresses fundamental tradeoffs in system design:

**C++ for Performance-Critical Components:**
- **Scheduling**: Microsecond-level scheduling decisions
- **State & Memory Management**: High-frequency state updates
- **Concurrency**: Concurreny without GIL contention

**Python for Orchestration and Flexibility:**
- **Model Loading**: Leveraging PyTorch ecosystem
- **API Servers**: FastAPI integration
- **Configuration**: Dynamic configuration management
- **Metrics**: Integration with monitoring systems

## Native Handle Architecture

The heart of Vajra's C++/Python integration is the **native handle pattern** - a bridge mechanism that enables zero-copy data transfer and shared ownership between Python and C++ components. This pattern ensures that performance-critical operations execute entirely in C++ while maintaining Python-friendly interfaces.

### Core Design Principles

**1. Shared Ownership via Smart Pointers**
Every native handle represents a `std::shared_ptr` to a C++ object, enabling safe cross-language object lifetime management:

```cpp
// C++ side: Smart pointer-based ownership
class InferenceEngine : public NonCopyableNonMovable {
private:
    EngineMetricsStorePtr metrics_store_;           // shared_ptr<EngineMetricsStore>
    UserSequenceParamQueuePtr waiting_seq_queue_;   // shared_ptr<UserSequenceParamQueue>
    RequestOutputQueuePtr output_queue_;            // shared_ptr<RequestOutputQueue>
public:
    explicit InferenceEngine(const EngineMetricsStorePtr& metrics_store);
};
```

**2. Python Wrapper with Native Handle**
Python objects maintain references to C++ objects through `.native_handle` properties:

```python
class InferenceEngine:
    def __init__(self, config: InferenceEngineConfig) -> None:
        # Create C++ InferenceEngine via pybind11
        self.native_handle = InferenceEngine_C(metrics_store.native_handle)
        
        # Get shared queue references from C++
        self.controller = ReplicasetControllerRegistry.get(
            config.controller_config.get_type(),
            config.controller_config,
            resource_mapping,
            self.native_handle.get_waiting_seq_queue(),  # C++ -> Python queue handle
            self.native_handle.get_output_queue(),       # C++ -> Python queue handle
        )
```

**3. Zero-Copy Queue Sharing**
Critical for performance, queues are shared directly between languages without serialization:

```cpp
// C++ InferenceEngine exposes shared queue references
UserSequenceParamQueuePtr GetWaitingSeqQueue() const { return waiting_seq_queue_; }
RequestOutputQueuePtr GetOutputQueue() const { return output_queue_; }
```

### Pybind11 Integration Layer

The `EnginePybind.cpp` file demonstrates the clean pybind11 integration:

```cpp
void InitInferenceEnginePybindClass(py::module_& pm) {
  py::class_<InferenceEngine, std::shared_ptr<InferenceEngine>>(pm, "InferenceEngine")
      .def(py::init<const EngineMetricsStorePtr&>())
      .def("add_request",
           [](InferenceEngine& self, const std::optional<std::string>& seq_id,
              const std::string& prompt, const TokenIds& prompt_token_ids,
              const SamplingParams& sampling_params) {
             // Convert Python list to shared_ptr for zero-copy
             auto prompt_token_ids_shared = std::make_shared<TokenIds>(prompt_token_ids);
             self.AddRequest(seq_id, prompt, prompt_token_ids_shared, sampling_params);
           })
      .def("get_waiting_seq_queue", &InferenceEngine::GetWaitingSeqQueue)
      .def("get_output_queue", &InferenceEngine::GetOutputQueue)
      .def("get_outputs", [](InferenceEngine& self, const bool block) {
        // Critical: Release GIL during potentially blocking C++ operations
        py::gil_scoped_release release;
        return self.GetOutputs(block);
      });
}
```

**Key Integration Features:**
- **GIL Management**: Automatic GIL release for blocking operations
- **Shared Pointer Binding**: Direct `std::shared_ptr` exposure to Python
- **Type Conversion**: Automatic conversion between Python/C++ types
- **Memory Safety**: RAII ensures proper cleanup across language boundaries

## Configuration System Integration

Vajra's configuration system exemplifies the native handle pattern, enabling polymorphic configuration with C++ performance:

### Python Configuration with Native Handles

```python
@frozen_dataclass
class ModelConfig:
    model: str = "meta-llama/Llama-2-7b-hf"
    trust_remote_code: bool = True
    dtype: str = "float16"
    # ... other fields
    
    def __post_init__(self):
        # Python-side validation and preprocessing
        self._verify_load_format()
        self.hf_config = get_config(self.model, self.trust_remote_code, self.revision)
        self.torch_dtype = get_and_verify_dtype(self.hf_config, self.dtype)
        
        # Create immutable C++ representation
        self.native_handle = ModelConfig_C(
            self.model,
            self.trust_remote_code,
            self.download_dir,
            self.load_format,
            self.dtype,
            self.seed,
            self.revision,
            self.max_model_len,
            self.get_total_num_layers(),
            self.get_total_num_q_heads(),
            self.get_total_num_kv_heads(),
            self.get_hidden_size(),
        )
```

### Polymorphic Configuration Pattern

The native handle pattern extends to polymorphic configurations, enabling runtime type selection with C++ performance:

```python
@frozen_dataclass
class BaseReplicaSchedulerConfig(BasePolyConfig):
    max_batch_size: int = 128
    
    @property
    def native_handle(self):
        return self._native_handle

@frozen_dataclass  
class FixedChunkReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    max_chunk_size: int = 1024
    min_chunk_size: int = 512
    
    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.FIXED_CHUNK
        
    def __post_init__(self):
        # Create type-specific C++ config
        self._native_handle = FixedChunkReplicaSchedulerConfig_C(
            self.max_batch_size,
            self.max_chunk_size,
            self.min_chunk_size,
        )
```

### Hierarchical Configuration Assembly

Complex configurations compose their native handles from constituent parts:

```python
@frozen_dataclass
class LlmReplicaControllerConfig(BaseReplicaControllerConfig):
    def __post_init__(self):
        # Ensure cross-config validation
        self.model_config.verify_with_parallel_config(self.parallel_config)
        
        # Compose C++ config from native handles of constituents
        self._native_handle = LlmReplicaControllerConfig_C(
            self.model_config.native_handle,      # ModelConfig_C
            self.worker_config.native_handle,     # WorkerConfig_C  
            self.cache_config.native_handle,      # CacheConfig_C
            self.parallel_config.native_handle,   # ParallelConfig_C
            self.scheduler_config.native_handle,  # BaseReplicaSchedulerConfig_C
        )
```

## Component Integration Patterns

### Engine-Controller Integration

The InferenceEngine demonstrates sophisticated component integration:

```python
class InferenceEngine:
    def __init__(self, config: InferenceEngineConfig) -> None:
        # 1. Create C++ engine with metrics store handle
        self.native_handle = InferenceEngine_C(metrics_store.native_handle)
        
        # 2. Share C++ queues with Python controllers
        self.controller = ReplicasetControllerRegistry.get(
            config.controller_config.get_type(),
            config.controller_config,
            resource_mapping,
            self.native_handle.get_waiting_seq_queue(),  # Shared queue
            self.native_handle.get_output_queue(),       # Shared queue
        )
    
    def add_request(self, prompt: str, sampling_params: SamplingParams, 
                   prompt_token_ids: List[int] = [], seq_id: Optional[str] = None) -> None:
        # Direct delegation to C++ for performance
        self.native_handle.add_request(seq_id, prompt, prompt_token_ids, sampling_params)
    
    def get_outputs(self, block: bool = False) -> List[RequestOutput]:
        # C++ handles blocking and queue management
        return self.native_handle.get_outputs(block)
```

### Model Layer Integration

Neural network layers seamlessly integrate PyTorch tensors with C++ computation:

```python
class LlamaAttention(nn.Module):
    def __init__(self, replica_controller_config: LlmReplicaControllerConfig):
        super().__init__()
        
        # PyTorch layer initialization
        self.qkv_proj = QKVParallelLinear(...)
        self.o_proj = RowParallelLinear(...)
        self.rotary_emb = RotaryEmbedding(...)
        
        # Create C++ computation kernel with handles to PyTorch layers
        self.native_handle = LlamaAttentionC(
            replica_controller_config.model_config.native_handle,
            replica_controller_config.cache_config.native_handle,
            replica_controller_config.parallel_config.native_handle,
            self.qkv_proj.native_handle,    # C++ reference to PyTorch layer
            self.o_proj.native_handle,      # C++ reference to PyTorch layer  
            self.rotary_emb.native_handle,  # C++ reference to PyTorch layer
        )
```


The metrics system demonstrates cross-language data collection:

```python
class WorkerMetricsStore(BaseMetricsStore):
    def __init__(self, config: MetricsConfig, model_num_layers: int, rank: int):
        self.model_num_layers = model_num_layers
        self.rank = rank
        super().__init__(config)

    def _get_native_handle_impl(self) -> Type[WorkerMetricsStoreC]:
        return WorkerMetricsStoreC

    @property
    def native_handle(self) -> WorkerMetricsStoreC:
        return self._native_handle

    def _create_native_handle(self) -> WorkerMetricsStoreC:
        return WorkerMetricsStoreC(
            self.config.native_handle,
            {metric: datastore.native_handle for metric, datastore in self.cdf_datastores.items()},
            {metric: datastore.native_handle for metric, datastore in self.time_series_datastores.items()},
            self.chrome_tracer,
            self.rank,  # Additional worker-specific parameter
        )
```

## Performance Optimizations

### GIL Management

Strategic GIL release ensures C++ operations don't block Python threads:

```cpp
.def("get_outputs", [](InferenceEngine& self, const bool block) {
    // Release GIL before potentially blocking C++ operation
    py::gil_scoped_release release;
    return self.GetOutputs(block);
});
```

### Zero-Copy Data Transfer

Native handles enable zero-copy sharing of large data structures:

```python
# Python side - no data copying
waiting_queue = self.native_handle.get_waiting_seq_queue()
output_queue = self.native_handle.get_output_queue()

# C++ side - direct shared_ptr access
UserSequenceParamQueuePtr GetWaitingSeqQueue() const { return waiting_seq_queue_; }
RequestOutputQueuePtr GetOutputQueue() const { return output_queue_; }
```
