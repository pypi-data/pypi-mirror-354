# Vajra System Design Documentation

Vajra is a high-performance distributed LLM inference system designed to efficiently serve multi-million token sequences. This documentation provides a comprehensive technical analysis of the system architecture, from foundational concepts through detailed implementation specifics.

```{toctree}
:maxdepth: 1
:caption: System Foundations

system_overview
core_abstractions
configuration_system
```

```{toctree}
:maxdepth: 1
:caption: Resource Management

scheduling_architecture
memory_management
parallelism_strategies
```

```{toctree}
:maxdepth: 1
:caption: Distributed Execution

sequence_management
model_execution
communication_architecture
```

```{toctree}
:maxdepth: 1
:caption: System Integration

event_driven_architecture
cpp_python_integration
```

## Documentation Structure

This documentation follows a logical progression from foundational concepts to implementation details:

### System Foundations
- **[System Overview](system_overview.md)** - Architecture principles and component relationships
- **[Core Abstractions](core_abstractions.md)** - Fundamental interfaces and design patterns
- **[Configuration System](configuration_system.md)** - Polymorphic configs and cross-language integration

### Resource Management and Scheduling  
- **[Scheduling Architecture](scheduling_architecture.md)** - Hierarchical scheduling and resource allocation
- **[Memory Management](memory_management.md)** - Paged KV cache and distributed memory coordination
- **[Parallelism Strategies](parallelism_strategies.md)** - Three-dimensional parallelism (PP/TP/KVP)

### Distributed Execution
- **[Sequence Management](sequence_management.md)** - Distributed state consistency and lifecycle
- **[Model Execution](model_execution.md)** - Computation pipeline and kernel optimization  
- **[Communication Architecture](communication_architecture.md)** - Dual-layer communication (ZMQ control plane + NCCL data plane)

### System Design and Integration
- **[Event-Driven Architecture](event_driven_architecture.md)** - Asynchronous coordination patterns
- **[C++/Python Integration](cpp_python_integration.md)** - Cross-language design and native handles

## Reading Guide

### For System Architects
Start with **System Foundations** for architectural foundations including configuration patterns, then **Resource Management** for resource management strategies. **Distributed Execution** covers distributed execution patterns.

### For Performance Engineers  
Focus on **Scheduling Architecture**, **Memory Management**, **Model Execution**, and **System Integration** for system integration patterns.

### For Developers
Begin with **System Foundations** for foundational concepts, especially **Configuration System** for configuration management, then **System Integration** for implementation patterns, especially **C++/Python Integration** for cross-language integration.

### For Researchers
**Configuration System**, **Memory Management**, **Parallelism Strategies**, and **Sequence Management** contain novel contributions to distributed LLM inference systems.

## Implementation Architecture

Vajra implements a dual-language architecture optimizing for both performance and productivity:

### C++ Performance Core
- **Location**: `csrc/vajra/native/`
- **Purpose**: Performance-critical scheduling, memory management, and model execution
- **Key Components**: Schedulers, sequence managers, block space managers, model runners

### Python Orchestration Layer  
- **Location**: `vajra/`
- **Purpose**: System coordination, configuration management, and external interfaces
- **Key Components**: Inference engine, cache engine, API servers

### Cross-Language Integration
- **Native Handles**: Shared pointer-based bridges enabling zero-copy data transfer
- **Event Interfaces**: Consistent event patterns across language boundaries
- **Configuration Management**: Unified configuration system with validation
