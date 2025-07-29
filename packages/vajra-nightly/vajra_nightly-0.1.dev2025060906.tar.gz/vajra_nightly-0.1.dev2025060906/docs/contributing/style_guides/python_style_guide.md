# Vajra Python Style Guide

## Introduction

This style guide outlines the coding conventions and best practices for writing Python code within the Vajra project. It builds upon [PEP 8](https://peps.python.org/pep-0008/) and incorporates Vajra-specific patterns. We use **Black** for code formatting, which automatically handles most style decisions.

## Key Goals

- **Readability**: Code should be easy to understand and follow by any developer
- **Consistency**: Uniformity in style across the project reduces cognitive load
- **Type Safety**: Comprehensive type hints improve code reliability and IDE support
- **Maintainability**: Well-structured code is easier to modify and extend
- **Integration**: Seamless interop with C++ components through native handles

## Code Formatting

### Running Black

```bash
# Format all Python files
make format

# Check formatting without making changes
black --check .
```

## Import Organization

### Import Order

Follow this exact order with blank lines between sections:

```python
# 1. Standard library imports
import logging
import time
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import field

# 2. Third-party imports  
import torch
import numpy as np
from transformers import AutoTokenizer

# 3. Vajra native imports (C++ bindings)
from vajra._native.configs import ModelConfig as ModelConfig_C
from vajra._native.datatypes import Request, SamplingParams

# 4. Vajra Python imports
from vajra.config.base_poly_config import BasePolyConfig
from vajra.config.parallel_config import ParallelConfig
from vajra.logger import init_logger
from vajra.utils.dataclasses import frozen_dataclass
```

### Import Guidelines

- Use absolute imports for all Vajra modules
- Group native (C++) imports separately from Python imports
- Import specific items rather than using `import *`

## Naming Conventions

### Variables and Functions
- **snake_case**: `model_config`, `process_request`, `token_ids`
- **Boolean variables**: Use descriptive predicates: `is_finished`, `has_cache`, `can_schedule`

```python
model_name: str = "llama-7b"
is_ready: bool = False
can_process: bool = True

def process_sequences(sequences: List[Sequence]) -> List[SamplerOutput]:
    """Process a batch of sequences."""
    pass
```

### Classes and Types
- **PascalCase**: `ModelConfig`, `InferenceEngine`, `SamplingParams`
- **Type aliases**: Descriptive PascalCase names

```python
from typing import Dict, List

# Type aliases
SequenceId = str
TokenId = int
RequestMapping = Dict[SequenceId, Request]
BatchTokens = List[List[TokenId]]
```

### Constants
- **UPPER_SNAKE_CASE**: `MAX_SEQUENCE_LENGTH`, `DEFAULT_TEMPERATURE`

```python
MAX_SEQUENCE_LENGTH: int = 4096
DEFAULT_TEMPERATURE: float = 1.0
SUPPORTED_MODELS: List[str] = ["llama", "mistral", "mixtral"]
```

### Files and Modules
- **snake_case**: `model_config.py`, `sequence_manager.py`, `inference_engine.py`

## Type Hints

### Comprehensive Type Annotations

All functions, methods, and class attributes must have type hints:

```python
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_name: str
    max_model_len: int
    vocab_size: Optional[int] = None
    dtype: str = "float16"
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.max_model_len <= 0:
            raise ValueError(f"max_model_len must be positive, got {self.max_model_len}")

def process_batch(
    sequences: List[Sequence],
    sampling_params: SamplingParams,
    kv_caches: List[torch.Tensor],
) -> Tuple[List[SamplerOutput], Dict[str, Any]]:
    """Process a batch of sequences with given sampling parameters."""
    # Implementation
    return outputs, metrics
```

### Generic Types

Use generic types for flexible, reusable code:

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Cacheable(Protocol):
    def cache_key(self) -> str: ...

class Cache(Generic[T]):
    def __init__(self) -> None:
        self._cache: Dict[str, T] = {}
    
    def get(self, item: Cacheable) -> Optional[T]:
        return self._cache.get(item.cache_key())
    
    def put(self, item: Cacheable, value: T) -> None:
        self._cache[item.cache_key()] = value
```

### Custom Type Annotations

Define domain-specific types for clarity:

```python
from typing import NewType

# Strong type aliases for domain concepts
SequenceId = NewType('SequenceId', str)
TokenId = NewType('TokenId', int)
BlockId = NewType('BlockId', int)
GPUDeviceId = NewType('GPUDeviceId', int)

def schedule_sequence(seq_id: SequenceId, device: GPUDeviceId) -> None:
    """Schedule sequence on specific GPU device."""
    pass
```

## Dataclasses and Configuration

### Frozen Dataclasses

Use the Vajra `@frozen_dataclass` decorator for configuration classes:

```python
from vajra.utils.dataclasses import frozen_dataclass
from dataclasses import field
from typing import List, Optional

@frozen_dataclass
class ModelConfig:
    model_name: str = field(
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        metadata={"help": "Name or path of the HuggingFace model to use."}
    )
    max_model_len: int = field(
        default=4096,
        metadata={"help": "Maximum sequence length supported by the model."}
    )
    trust_remote_code: bool = field(
        default=False,
        metadata={"help": "Trust remote code when loading model."}
    )
    
    def __post_init__(self) -> None:
        """Validate and initialize derived fields."""
        self._validate_parameters()
        self.hf_config = get_config(self.model_name, self.trust_remote_code)
        # Create native handle for C++ interop
        object.__setattr__(self, 'native_handle', ModelConfig_C(
            model_name=self.model_name,
            max_model_len=self.max_model_len,
            # ... other parameters
        ))
    
    def _validate_parameters(self) -> None:
        """Validate configuration parameters."""
        if self.max_model_len <= 0:
            raise ValueError(f"max_model_len must be positive, got {self.max_model_len}")
        
        if not self.model_name.strip():
            raise ValueError("model_name cannot be empty")
```

### Field Metadata

Use field metadata for documentation and CLI generation:

```python
@frozen_dataclass
class ParallelConfig:
    tensor_parallel_size: int = field(
        default=1,
        metadata={
            "help": "Number of tensor parallel replicas.",
            "constraints": "Must be a power of 2 and <= number of GPUs"
        }
    )
    pipeline_parallel_size: int = field(
        default=1, 
        metadata={
            "help": "Number of pipeline parallel stages.",
            "constraints": "Must be >= 1"
        }
    )
```

## Logging

### Logger Initialization

Use the Vajra logging system:

```python
from vajra.logger import init_logger

logger = init_logger(__name__)

class InferenceEngine:
    def __init__(self, config: InferenceEngineConfig):
        logger.info("Initializing InferenceEngine with config: %s", config.model_name)
        self.config = config
        # ... initialization
```

### Logging Patterns

Use structured logging with appropriate levels:

```python
def process_request(self, request: Request) -> None:
    """Process an inference request."""
    logger.debug("Processing request %s with %d tokens", 
                request.request_id, len(request.prompt_token_ids))
    
    try:
        # Process request
        result = self._execute_inference(request)
        logger.info("Successfully processed request %s in %.2fs", 
                   request.request_id, result.processing_time)
    
    except Exception as e:
        logger.error("Failed to process request %s: %s", 
                    request.request_id, str(e))
        raise
    
    logger.debug("Request %s generated %d tokens", 
                request.request_id, len(result.output_tokens))
```

## Class Design Patterns

### Polymorphic Base Classes

Use the BasePolyConfig pattern for extensible configurations:

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, ClassVar, Dict

class SchedulerType(Enum):
    FCFS = "fcfs"
    PRIORITY = "priority"
    FAIR_SHARE = "fair_share"

@frozen_dataclass
class BaseSchedulerConfig(BasePolyConfig):
    """Base class for scheduler configurations."""
    
    @classmethod
    @abstractmethod
    def get_type(cls) -> SchedulerType:
        """Return the scheduler type for this config."""
        pass

@frozen_dataclass  
class FCFSSchedulerConfig(BaseSchedulerConfig):
    """First-Come-First-Served scheduler configuration."""
    queue_timeout_s: float = 30.0
    
    @classmethod
    def get_type(cls) -> SchedulerType:
        return SchedulerType.FCFS

@frozen_dataclass
class PrioritySchedulerConfig(BaseSchedulerConfig):
    """Priority-based scheduler configuration."""
    default_priority: int = 5
    max_priority: int = 10
    
    @classmethod 
    def get_type(cls) -> SchedulerType:
        return SchedulerType.PRIORITY
```

### Registry Pattern

Use registries for extensible component systems:

```python
from typing import Type, Dict, Any
from abc import ABC, abstractmethod

class BaseRegistry(ABC):
    """Base class for component registries."""
    _registry: ClassVar[Dict[Enum, Type[Any]]] = {}
    
    @classmethod
    def register(cls, key: Enum, implementation_class: Type[Any]) -> None:
        """Register an implementation for the given key."""
        if key in cls._registry:
            logger.warning("Overriding existing registration for %s", key)
        cls._registry[key] = implementation_class
    
    @classmethod
    def get(cls, key: Enum, *args: Any, **kwargs: Any) -> Any:
        """Create an instance of the registered implementation."""
        if key not in cls._registry:
            raise ValueError(f"{key} is not registered in {cls.__name__}")
        return cls._registry[key](*args, **kwargs)
    
    @classmethod
    def list_registered(cls) -> List[Enum]:
        """List all registered keys."""
        return list(cls._registry.keys())

class SchedulerRegistry(BaseRegistry):
    """Registry for scheduler implementations."""
    _registry: ClassVar[Dict[SchedulerType, Type[BaseScheduler]]] = {}

# Register implementations
SchedulerRegistry.register(SchedulerType.FCFS, FCFSScheduler)
SchedulerRegistry.register(SchedulerType.PRIORITY, PriorityScheduler)

# Use registry
scheduler = SchedulerRegistry.get(SchedulerType.FCFS, config)
```

### Native Handle Integration

Integrate with C++ components through native handles:

```python
import vajra._native as vajra_native
from typing import Optional

class InferenceEngine:
    """Python wrapper for C++ InferenceEngine."""
    
    def __init__(self, config: InferenceEngineConfig):
        self.config = config
        self._tokenizer = AutoTokenizer.from_pretrained(config.model_config.model_name)
        self._request_tracker: Dict[str, RequestInfo] = {}
        
        # Create C++ engine through native handle
        self._native_handle = vajra_native.create_inference_engine(
            config.to_native_config()
        )
    
    def add_request(
        self,
        prompt: str,
        sampling_params: SamplingParams,
        seq_id: Optional[str] = None,
    ) -> str:
        """Add a new inference request."""
        # Tokenize in Python (ecosystem integration)
        prompt_token_ids = self._tokenizer.encode(prompt)
        
        # Generate ID if needed
        if seq_id is None:
            seq_id = f"req_{uuid.uuid4().hex[:8]}"
        
        # Create native request
        native_request = vajra_native.Request(
            request_id=seq_id,
            prompt=prompt,
            prompt_token_ids=prompt_token_ids,
            sampling_params=sampling_params.to_native()
        )
        
        # Pass to C++ engine
        self._native_handle.add_request(native_request)
        
        # Track in Python for API responses
        self._request_tracker[seq_id] = RequestInfo(
            prompt=prompt,
            arrival_time=time.time(),
            status="pending"
        )
        
        return seq_id
    
    def __del__(self) -> None:
        """Ensure cleanup of native resources."""
        if hasattr(self, '_native_handle'):
            self._native_handle.stop()
```

## Testing Patterns

### Test Class Organization

```python
import pytest
import torch
from unittest.mock import Mock, patch
from vajra.config.model_config import ModelConfig
from vajra.engine.inference_engine import InferenceEngine

class TestModelConfig:
    """Test ModelConfig functionality."""
    
    def test_valid_config_creation(self):
        """Test creating a valid ModelConfig."""
        config = ModelConfig(
            model_name="meta-llama/Meta-Llama-3-8B-Instruct",
            max_model_len=4096
        )
        assert config.model_name == "meta-llama/Meta-Llama-3-8B-Instruct"
        assert config.max_model_len == 4096
    
    def test_invalid_max_model_len_raises_error(self):
        """Test that invalid max_model_len raises ValueError."""
        with pytest.raises(ValueError, match="max_model_len must be positive"):
            ModelConfig(
                model_name="test-model",
                max_model_len=-1
            )
    
    def test_empty_model_name_raises_error(self):
        """Test that empty model_name raises ValueError."""
        with pytest.raises(ValueError, match="model_name cannot be empty"):
            ModelConfig(
                model_name="",
                max_model_len=4096
            )

class TestInferenceEngine:
    """Test InferenceEngine functionality."""
    
    @pytest.fixture
    def mock_config(self) -> ModelConfig:
        """Create a mock configuration for testing."""
        return ModelConfig(
            model_name="test-model",
            max_model_len=2048
        )
    
    @pytest.fixture  
    def engine(self, mock_config: ModelConfig) -> InferenceEngine:
        """Create an InferenceEngine for testing."""
        with patch('vajra._native.create_inference_engine'):
            return InferenceEngine(mock_config)
    
    def test_add_request_returns_request_id(self, engine: InferenceEngine):
        """Test that add_request returns a valid request ID."""
        request_id = engine.add_request(
            prompt="Test prompt",
            sampling_params=SamplingParams(temperature=0.7)
        )
        assert isinstance(request_id, str)
        assert len(request_id) > 0
    
    def test_add_request_with_empty_prompt_raises_error(self, engine: InferenceEngine):
        """Test that empty prompt raises ValueError."""
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            engine.add_request(
                prompt="",
                sampling_params=SamplingParams()
            )
```

### Pytest Configuration

Use pytest with appropriate fixtures and markers:

```python
# conftest.py
import pytest
import torch

@pytest.fixture(scope="session")
def cuda_available():
    """Check if CUDA is available for testing."""
    return torch.cuda.is_available()

@pytest.fixture
def sample_model_config():
    """Provide a standard model config for testing."""
    return ModelConfig(
        model_name="test-model",
        max_model_len=1024,
        dtype="float16"
    )

# Mark GPU tests
pytestmark = pytest.mark.gpu

class TestGPUOperations:
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_gpu_memory_allocation(self):
        """Test GPU memory allocation."""
        pass
```

## Documentation

### Docstring Style

Use Google-style docstrings with type information:

```python
def schedule_sequences(
    self,
    sequences: List[Sequence],
    available_blocks: int,
    current_time: float,
) -> Tuple[List[Sequence], List[Sequence]]:
    """Schedule sequences based on available memory and priorities.
    
    This method implements the core scheduling logic, deciding which sequences
    can be executed based on memory constraints and scheduling policies.
    
    Args:
        sequences: List of sequences to schedule.
        available_blocks: Number of memory blocks available for allocation.
        current_time: Current timestamp for scheduling decisions.
        
    Returns:
        A tuple containing:
            - List of sequences that can be scheduled immediately
            - List of sequences that must wait for resources
            
    Raises:
        ValueError: If available_blocks is negative.
        RuntimeError: If scheduling algorithm fails to converge.
        
    Example:
        >>> scheduler = PriorityScheduler()
        >>> ready, waiting = scheduler.schedule_sequences(seqs, 100, time.time())
        >>> print(f"Scheduled {len(ready)} sequences")
    """
    if available_blocks < 0:
        raise ValueError(f"available_blocks must be non-negative, got {available_blocks}")
    
    # Implementation...
```

### Module-Level Documentation

```python
"""Vajra model configuration management.

This module provides configuration classes for model loading, validation,
and parameter management. It integrates with the HuggingFace transformers
library for model discovery and with Vajra's native C++ implementation
for performance-critical operations.

Example:
    Basic usage of ModelConfig:
    
    >>> config = ModelConfig(
    ...     model_name="meta-llama/Meta-Llama-3-8B-Instruct",
    ...     max_model_len=4096
    ... )
    >>> config.validate()
    >>> engine = InferenceEngine(config)

Classes:
    ModelConfig: Configuration for model loading and execution.
    ModelRegistry: Registry for supported model types.
    
Functions:
    validate_model_config: Validate model configuration parameters.
    load_model_config: Load configuration from file or dictionary.
"""

from typing import Dict, List, Optional
# ... rest of module
```
