# Configuration Reference

Vajra uses a sophisticated polymorphic configuration system that provides type safety and flexibility across different deployment scenarios. This page covers all configuration options and their usage, to get a deeper understanding of how Vajra manages its configuration, please refer to the [design doc](../design/configuration_system.md).

> **For practical usage examples**: See the [Python Usage Guide](python_usage.md) or [OpenAI Server Guide](openai_server.md) which show common usage pattern.

## Getting Started

### Configuration Architecture

Vajra's configuration system is built around polymorphic configs that allow runtime switching between different implementations:

```python
from vajra.config import (
    ModelConfig,
    ParallelConfig, 
    SchedulerConfig,
    FixedChunkReplicaSchedulerConfig,
    DynamicChunkReplicaSchedulerConfig
)

# Polymorphic scheduler configuration
scheduler_config = FixedChunkReplicaSchedulerConfig(
    max_batch_size=128,
    chunk_size=2048
)

# Can be swapped at runtime
scheduler_config = DynamicChunkReplicaSchedulerConfig(
    max_batch_size=128,
    max_chunk_size_param=8192,
    min_chunk_size_param=32,
    target_batch_time_param=0.05
)
```

## Core Configuration Classes

### ModelConfig

Controls model loading and behavior:

```python
ModelConfig(
    model="meta-llama/Llama-2-7b-chat-hf",     # HuggingFace model identifier
    trust_remote_code=True,                     # Allow remote code execution
    download_dir=None,                          # Cache directory
    load_format="auto",                         # Weight format: auto, pt, safetensors
    dtype="float16",                           # Model precision
    seed=0,                                    # Random seed
    revision=None,                             # Git revision/branch
    max_model_len=4096,                        # Context length limit
    override_num_layers=None                   # Override layer count
)
```

**Data Types:**
- `float16` - Half precision (recommended for most GPUs)
- `bfloat16` - Brain floating point (good for training)
- `float32` - Full precision (highest quality, memory intensive)
- `auto` - Automatic selection based on model

### ParallelConfig

Defines parallelism strategies:

```python
ParallelConfig(
    pipeline_parallel_size=1,                  # Pipeline stages
    tensor_parallel_size=1,                    # Tensor parallel groups
    enable_expert_parallel=False,              # MoE expert parallelism
    enable_sequence_pipeline_parallel=False,   # Sequence-level pipelining
    enable_chunked_pipeline_comm_opt=False,    # Communication optimization
    kv_parallel_size=1,                        # KV cache parallelism
    max_num_tokens_per_kvp_group=0             # KV group token limit
)
```

**Parallelism Types:**
- **Tensor Parallel**: Split model weights across GPUs
- **Pipeline Parallel**: Split model layers across GPUs  
- **KV Parallel**: Distribute KV cache across GPUs
- **Expert Parallel**: Distribute MoE experts across GPUs

### WorkerConfig

Controls worker behavior:

```python
WorkerConfig(
    gpu_memory_utilization=0.8,               # GPU memory fraction
    use_native_execution_backend=True         # Use C++ backend for model execution
)
```

### CacheConfig

KV cache management:

```python
CacheConfig(
    block_size=16                             # Cache block size in tokens
)
```

**Block Size Guidelines:**
- Smaller blocks (8-16): Better memory utilization, slightly higher overhead
- Larger blocks (32-64): Lower overhead, potential memory waste

## Replica Scheduling Configurations

### Fixed Chunk Scheduler

This is the default scheduler in Vajra and mimics the chunk prefill behaviour described in Sarathi-Serve.

```python
FixedChunkReplicaSchedulerConfig(
    max_batch_size=128,                       # Maximum sequences per batch
    chunk_size=2048                          # Fixed processing chunk size
)
```

### Dynamic Chunk Scheduler  

Dynamic chunking scheduler is an extension of the baseline Sarathi-Serve policy which tries to create chunks of fixed latency cost instead of fixed number of tokens. This is useful for scenarios with variable sequence lengths. To use this scheduler, the model must be supported by Vidur.

```python
DynamicChunkReplicaSchedulerConfig(
    max_batch_size=128,                       # Maximum sequences per batch
    max_chunk_size_param=8192,               # Maximum chunk size
    min_chunk_size_param=32,                 # Minimum chunk size
    target_batch_time_param=0.05             # Target batch processing time
)
```

### Space Sharing Scheduler

Vajra also supports prefill-prefill batching scenarios for efficient long-context serving as described in Medha. Prefill-prefill batching balances the load between MLP and Attention layers by combining two prefill chunks one --- one short chunk from a long request (e.g. 32 token chunk with 256K context) with a long chunk from a short request (e.g. 512 tokens with 1K context).

```python
SpaceSharingReplicaSchedulerConfig(
    max_batch_size=128,                       # Maximum sequences per batch
    max_chunk_size_param=8192,               # Maximum chunk size
    min_chunk_size_param=32,                 # Minimum chunk size
    target_batch_time_param=0.05,            # Target batch processing time
    long_seq_kv_cache_len_threshold=262144   # Long sequence threshold
)
```

## Request Prioritization

### FCFS (First-Come-First-Served)

Simple queue-based prioritization:

```python
FcfsRequestPrioritizerConfig()
```

### EDF (Earliest Deadline First)

Deadline-based prioritization:

```python
EdfRequestPrioritizerConfig(
    deadline_multiplier=1.5,                 # Deadline calculation factor
    min_deadline=0.5                         # Minimum deadline in seconds
)
```

### LRS (Least Remaining Slack)

The least remaining slack prioritizer approximates the prioritization approach described in Medha. This prioratizer is useful in long context scenarios where EDF strategy fails due to request length variation.

```python
LrsRequestPrioritizerConfig(
    deadline_multiplier=1.5,                 # Deadline calculation factor
    min_deadline=0.5                         # Minimum deadline in seconds
)
```

## Replica Set Configuration

### Controller Configuration

```python
LLMReplicaSetControllerConfig(
    num_replicas=1,                          # Number of replicas
    num_tokenizer_workers=10                 # Tokenizer worker processes
)
```

### Replica Controller Types

**Base LLM Controller:**
```python
LLMBaseReplicaControllerConfig(
    model_config=model_config,
    parallel_config=parallel_config,
    worker_config=worker_config,
    cache_config=cache_config,
    scheduler_config=scheduler_config
)
```

**Pipeline Parallel Controller:**
```python
LLMPipelineParallelReplicaControllerConfig(
    model_config=model_config,
    parallel_config=parallel_config,
    worker_config=worker_config,
    cache_config=cache_config,
    scheduler_config=scheduler_config
)
```

## Metrics Configuration

Comprehensive monitoring and observability:

```python
MetricsConfig(
    write_metrics=False,                      # Enable metrics collection
    wandb_project=None,                       # W&B project name
    wandb_group=None,                         # W&B group
    wandb_run_name=None,                      # W&B run name
    wandb_sweep_id=None,                      # W&B sweep ID
    wandb_run_id=None,                        # W&B run ID
    enable_gpu_op_level_metrics=False,        # GPU operation metrics
    enable_cpu_op_level_metrics=False,        # CPU operation metrics
    enable_chrome_trace=False,                # Chrome tracing
    keep_individual_batch_metrics=False,      # Detailed batch metrics
    store_png=False,                          # Store plot images
    output_dir="."                           # Output directory
)
```

**Metrics Types:**
- **System Metrics**: GPU/CPU utilization, memory usage
- **Performance Metrics**: Throughput, latency, queue times
- **Operation Metrics**: Detailed kernel-level profiling
- **Batch Metrics**: Per-batch performance characteristics
