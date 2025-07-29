# Configuration System Architecture

## Introduction

Vajra implements a sophisticated configuration system that provides type safety, polymorphism, automatic CLI generation, and seamless C++/Python integration. The system is built around several key innovations: polymorphic configs, flat dataclass transformation, 1:1 config-to-class mapping, and native handle bridging. This chapter provides a comprehensive analysis of this unique configuration architecture.

## Core Properties

**1. Type Safety Across Languages**
- Configs are defined in both Python and C++ with identical structure
- Automatic validation prevents configuration errors at startup
- Compile-time and runtime type checking

**2. Polymorphic Configuration**
- Base config classes support multiple implementations
- Runtime type selection through enum-based dispatch
- Extensible without modifying existing code

**3. 1:1 Config-Class Mapping**
- Every major component has exactly one corresponding config class
- Clear ownership and responsibility boundaries
- Simplified dependency injection

**4. Flat Transformation for CLI**
- Nested config hierarchies automatically flattened for command-line parsing
- Complex configurations become simple CLI arguments
- Automatic help generation with type checking

**5. Cross-Language Consistency**
- Python configs automatically generate C++ native handles
- Bidirectional conversion maintains data integrity
- Unified configuration source of truth

**6. Immutability**
- All config classes are immutable by design
- Config values remain consistent across the program lifecycle


## Configuration Hierarchy Overview

### Top-Level Configuration Structure

```python
@frozen_dataclass
class InferenceEngineConfig:
    model_config: ModelConfig
    parallel_config: ParallelConfig  
    cache_config: CacheConfig
    worker_config: WorkerConfig
    metrics_config: MetricsConfig
    
    # Polymorphic configurations
    replica_controller_config: BaseReplicaControllerConfig
    replicaset_controller_config: BaseReplicasetControllerConfig
    request_prioritizer_config: BaseRequestPrioritizerConfig
    
    # System configuration
    driver_ip: str = "localhost"
    enable_chrome_trace: bool = False
```

### Component-to-Config Mapping

```
System Component           ↔  Configuration Class
─────────────────────────     ─────────────────────────
InferenceEngine           ↔  InferenceEngineConfig
ReplicaController         ↔  BaseReplicaControllerConfig
  ├─ BaseLLMReplicaController ↔ BaseLLMReplicaControllerConfig  
  └─ PipelineParallelController ↔ PipelineParallelConfig
ReplicasetController      ↔  BaseReplicasetControllerConfig
ReplicaScheduler          ↔  BaseReplicaSchedulerConfig
  ├─ FixedChunkScheduler  ↔  FixedChunkReplicaSchedulerConfig
  ├─ DynamicChunkScheduler ↔ DynamicChunkReplicaSchedulerConfig
  └─ SpaceSharingScheduler ↔ SpaceSharingReplicaSchedulerConfig
RequestPrioritizer        ↔  BaseRequestPrioritizerConfig
  ├─ FcfsPrioritizer      ↔  FcfsRequestPrioritizerConfig
  ├─ EdfPrioritizer       ↔  EdfRequestPrioritizerConfig
  └─ LrsPrioritizer       ↔  LrsRequestPrioritizerConfig
Worker                    ↔  WorkerConfig
Model                     ↔  ModelConfig
Cache                     ↔  CacheConfig
Metrics                   ↔  MetricsConfig
```

## Polymorphic Configuration Framework

### BasePolyConfig Foundation

```python
from abc import ABC
from enum import Enum

@frozen_dataclass  
class BasePolyConfig(ABC):
    
    @classmethod
    def create_from_type(cls, type_: Enum) -> Any:
        """Factory method for polymorphic instantiation"""
        for subclass in get_all_subclasses(cls):
            if subclass.get_type() == type_:
                return subclass()
        raise ValueError(f"Invalid type: {type_}")
    
    @staticmethod
    def get_type() -> Enum:
        """Each subclass defines its type identifier"""
        raise NotImplementedError
```

### Concrete Polymorphic Example: ReplicaSchedulerConfig

```python
# Base configuration class
@frozen_dataclass
class BaseReplicaSchedulerConfig(BasePolyConfig):
    max_batch_size: int = 128
    
    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        raise NotImplementedError

# Concrete implementations
@frozen_dataclass
class FixedChunkReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    chunk_size: int = 2048
    
    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.FIXED_CHUNK

@frozen_dataclass  
class DynamicChunkReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    max_chunk_size: int = 8192
    min_chunk_size: int = 32
    target_batch_time: float = 0.05
    
    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.DYNAMIC_CHUNK

@frozen_dataclass
class SpaceSharingReplicaSchedulerConfig(DynamicChunkReplicaSchedulerConfig):
    long_seq_threshold: int = 256 * 1024
    
    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.SPACE_SHARING
```

### Enum-Driven Type Selection

```python
from enum import Enum

class ReplicaSchedulerType(Enum):
    FIXED_CHUNK = "fixed_chunk"
    DYNAMIC_CHUNK = "dynamic_chunk"  
    SPACE_SHARING = "space_sharing"

class RequestPrioritizerType(Enum):
    FCFS = "fcfs"
    EDF = "edf"
    LRS = "lrs"

# Usage in configuration
@frozen_dataclass
class ReplicaControllerConfig:
    replica_scheduler_config: BaseReplicaSchedulerConfig = field(
        default_factory=lambda: FixedChunkReplicaSchedulerConfig())
    
    # Automatic type field generation for CLI
    replica_scheduler_type: ReplicaSchedulerType = ReplicaSchedulerType.FIXED_CHUNK
```

## Flat Dataclass Transformation

### Problem: CLI Parsing of Nested Configs

Traditional nested dataclasses don't work well with command-line interfaces:

```python
# Problematic for CLI
@frozen_dataclass
class ComplexConfig:
    model_config: ModelConfig
    scheduler_config: BaseReplicaSchedulerConfig
    cache_config: CacheConfig
    
# How to specify: --model_config.model="llama-7b" ??
# How to handle polymorphic scheduler_config??
```

### Solution: Automatic Flattening

```python
def create_flat_dataclass(input_dataclass: Any) -> Any:
    """
    Creates a new FlatClass type by recursively flattening the input dataclass.
    Enables easy CLI parsing while preserving hierarchical structure.
    """
    meta_fields = []
    processed_classes = set()
    dataclass_dependencies = defaultdict(set)
    
    def process_dataclass(_input_dataclass: Any, prefix=""):
        for field in fields(_input_dataclass):
            prefixed_name = f"{prefix}{field.name}"
            
            # Handle polymorphic configs
            if is_subclass(field_type, BasePolyConfig):
                # Add type selection field
                type_field_name = f"{field.name}_type"
                meta_fields.append((type_field_name, EnumType, 
                                  dataclass_field(default=default_type)))
                
                # Process all possible subclasses
                for subclass in get_all_subclasses(field_type):
                    process_dataclass(subclass, f"{to_snake_case(subclass.__name__)}_")
            
            # Handle nested dataclasses  
            elif hasattr(field_type, "__dataclass_fields__"):
                process_dataclass(field_type, f"{to_snake_case(field_type.__name__)}_")
            
            # Handle primitive fields
            else:
                meta_fields.append((prefixed_name, field_type, field))
    
    # Create flattened class with reconstruction capability
    FlatClass = make_dataclass("FlatClass", meta_fields)
    setattr(FlatClass, "reconstruct_original_dataclass", reconstruction_method)
    return FlatClass
```

### Flattened CLI Example

```bash
# Original nested structure flattened to CLI arguments
python -m vajra.entrypoints.openai.api_server \
    --model "meta-llama/Meta-Llama-3-8B-Instruct" \
    --max_model_len 4096 \
    --tensor_parallel_size 4 \
    --pipeline_parallel_size 2 \
    --replica_scheduler_type "dynamic_chunk" \
    --dynamic_chunk_replica_scheduler_config_max_chunk_size 8192 \
    --dynamic_chunk_replica_scheduler_config_target_batch_time 0.05 \
    --request_prioritizer_type "edf" \
    --edf_request_prioritizer_config_deadline_multiplier 1.5 \
    --cache_config_block_size 16 \
    --worker_config_device "cuda"
```

## C++/Python Config Integration

### Dual Language Definition

**Python Side (vajra/config/model_config.py):**
```python
@frozen_dataclass
class ModelConfig:
    model: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    trust_remote_code: bool = True
    dtype: str = "float16"
    max_model_len: int = -1
    
    def __post_init__(self):
        # Validation and preprocessing in Python
        self._verify_load_format()
        self.hf_config = get_config(self.model, self.trust_remote_code, self.revision)
        self.torch_dtype = get_and_verify_dtype(self.hf_config, self.dtype)
        self.max_model_len = get_and_verify_max_len(self.hf_config, self.max_model_len)
        
        # Create C++ native handle after validation
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
            self.get_hidden_size()
        )
```

**C++ Side (csrc/include/vajra/native/configs/ModelConfig.h):**
```cpp
struct ModelConfig final {
    ModelConfig(std::string model_param, bool trust_remote_code_param,
                std::optional<std::string> download_dir_param,
                std::string load_format_param, std::string dtype_param,
                std::size_t seed_param, std::optional<std::string> revision_param,
                std::size_t max_model_len_param, std::size_t total_num_layers_param,
                std::size_t total_num_q_heads_param,
                std::size_t total_num_kv_heads_param, std::size_t hidden_size_param);

    // Const member variables for immutability
    const std::string model;
    const bool trust_remote_code;
    const std::optional<std::string> download_dir;
    const std::string load_format;
    const std::string dtype;
    const std::size_t seed;
    const std::optional<std::string> revision;
    const std::size_t max_model_len;
    const std::size_t total_num_layers;
    const std::size_t total_num_q_heads;
    const std::size_t total_num_kv_heads;
    const std::size_t hidden_size;
    
    // Helper methods
    std::size_t GetHeadSize() const;
    std::size_t GetNumLayers(const ParallelConfig& parallel_config) const;
    std::string ToString() const;
};
```

### Native Handle Pattern

```python
class ConfigWithNativeHandle:
    """Pattern for configs that bridge to C++"""
    
    def __post_init__(self):
        # Validation and preprocessing in Python
        self._validate_config()
        self._compute_derived_values()
        
        # Create immutable C++ representation
        self.native_handle = self._create_native_handle()
    
    def _create_native_handle(self):
        """Subclasses implement specific C++ construction"""
        raise NotImplementedError
    
    def update_native_handle(self):
        """Recreate native handle after modifications"""
        self.native_handle = self._create_native_handle()
```

### Polymorphic Config C++ Integration

```cpp
// C++ polymorphic config hierarchy mirrors Python
struct BaseReplicaSchedulerConfig {
    virtual ~BaseReplicaSchedulerConfig() = default;
    virtual ReplicaSchedulerType GetType() const = 0;
    virtual std::string ToString() const = 0;
    
    // Virtual interface matches Python polymorphic methods
    virtual std::size_t GetMaxChunkSize() const = 0;
    virtual std::size_t GetMinChunkSize() const = 0;
    virtual float GetTargetBatchTime() const = 0;
};

struct FixedChunkReplicaSchedulerConfig final : public BaseReplicaSchedulerConfig {
    explicit FixedChunkReplicaSchedulerConfig(std::size_t chunk_size_param = 2048)
        : chunk_size(chunk_size_param) {}
    
    ReplicaSchedulerType GetType() const override {
        return ReplicaSchedulerType::FIXED_CHUNK;
    }
    
    std::size_t GetMaxChunkSize() const override { return chunk_size; }
    std::size_t GetMinChunkSize() const override { return chunk_size; }
    float GetTargetBatchTime() const override { return 0; }
    
    std::string ToString() const override {
        return std::format("FixedChunkReplicaSchedulerConfig(chunk_size={})", chunk_size);
    }
    
private:
    const std::size_t chunk_size;
};
```

## Config-to-Class Instantiation

### Factory Pattern Implementation

```python
def create_replica_scheduler(config: BaseReplicaSchedulerConfig) -> BaseReplicaScheduler:
    """Factory function using config type for instantiation"""
    
    scheduler_type = config.get_type()
    
    if scheduler_type == ReplicaSchedulerType.FIXED_CHUNK:
        return FixedChunkReplicaScheduler(
            model_config=model_config,
            scheduler_config=config,  # Config passed to constructor
            cache_config=cache_config,
            parallel_config=parallel_config,
            # ... other dependencies
        )
    elif scheduler_type == ReplicaSchedulerType.DYNAMIC_CHUNK:
        return DynamicChunkReplicaScheduler(
            model_config=model_config,
            scheduler_config=config,
            execution_time_predictor=execution_time_predictor,  # Additional dependency
            # ... 
        )
    elif scheduler_type == ReplicaSchedulerType.SPACE_SHARING:
        return SpaceSharingReplicaScheduler(
            model_config=model_config,
            scheduler_config=config,
            # ...
        )
    else:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")
```

### C++ Factory Integration

```cpp
// C++ factory mirrors Python structure
std::unique_ptr<BaseReplicaScheduler> CreateReplicaScheduler(
    const ModelConfig& model_config,
    std::shared_ptr<const BaseReplicaSchedulerConfig> scheduler_config,
    const CacheConfig& cache_config,
    const ParallelConfig& parallel_config,
    std::size_t num_gpu_blocks,
    SequencePriorityQueuePtr waiting_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer) {
    
    switch (scheduler_config->GetType()) {
        case ReplicaSchedulerType::FIXED_CHUNK:
            return std::make_unique<FixedChunkReplicaScheduler>(
                model_config, scheduler_config, cache_config, parallel_config,
                num_gpu_blocks, waiting_queue, request_prioritizer);
                
        case ReplicaSchedulerType::DYNAMIC_CHUNK:
            return std::make_unique<DynamicChunkReplicaScheduler>(
                model_config, scheduler_config, cache_config, parallel_config,
                num_gpu_blocks, waiting_queue, request_prioritizer);
                
        case ReplicaSchedulerType::SPACE_SHARING:
            return std::make_unique<SpaceSharingReplicaScheduler>(
                model_config, scheduler_config, cache_config, parallel_config,
                num_gpu_blocks, waiting_queue, request_prioritizer);
                
        default:
            throw std::invalid_argument("Unknown scheduler type");
    }
}
```
