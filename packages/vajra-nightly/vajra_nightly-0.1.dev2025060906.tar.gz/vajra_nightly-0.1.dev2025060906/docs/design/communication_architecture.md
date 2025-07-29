# Communication Architecture

## Introduction

Vajra implements a dual-layer communication architecture that separates control plane and data plane operations. The control plane uses ZeroMQ (ZMQ) for coordination with data plane, while the data plane leverages PyTorch's distributed communication backend (primarily NCCL) for high-performance tensor operations.

## Design Approach

We Separate control messaging from tensor data movement to optimize each independently.

1. **Control Plane - Data Plane Communication (ZMQ)**: Lightweight coordination messages, scheduling decisions, result collection
2. **Data Plane (NCCL/PyTorch)**: High-performance tensor operations, GPU-to-GPU communication
3. **Asynchronous Operation**: Both layers operate independently without blocking each other
4. **Fault Isolation**: Failures in either layer can be handled independently

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                 CONTROL PLANE (ZMQ)                 │
│                                                     │
│  Controller ─[PUB/SUB]─> Workers                    │
│      ▲                      │                       │
│      └─[PUSH/PULL]──────────┘                       │
│                                                     │
├─────────────────────────────────────────────────────┤
│                 DATA PLANE (NCCL)                   │
│                                                     │
│  Worker1 ◄─[AllReduce]─► Worker2                    │
│     │                      │                        │
│     └─[Send/Recv]─► Worker3 (Pipeline Stage)        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Data Plane: PyTorch Distributed Communication

### Process Group Architecture

**Design Challenge**: Support three parallelization dimensions (Pipeline, Tensor, KV-Parallel) simultaneously.

**Solution**: Multiple PyTorch process groups for different communication patterns:

```cpp
// Process group types
TensorParallelGroup     // AllReduce for weight sharding
PipelineParallelGroup   // Send/Recv between stages  
KVParallelGroup         // AllGather for KV cache distribution
```

### Communication Patterns by Parallelism Type

**Tensor Parallelism**: AllReduce and AllGather operations
- **AllReduce**: Synchronize gradients across tensor parallel ranks
- **AllGather**: Collect sharded tensors for output

**Pipeline Parallelism**: Point-to-point Send/Recv operations
- **Chunked Optimization**: Send only tensor parallel slice, gather at receiver
- **Stream Overlap**: Use CUDA streams to overlap communication with computation

## Control Plane -  Data Plane : ZeroMQ

### Communication Patterns

**PUB/SUB Pattern** (Controller → Workers):
- **Use Case**: Broadcasting scheduling decisions to all workers
- **Characteristics**: One-to-many, fire-and-forget, automatic fan-out
- **Message Type**: StepInputs containing scheduler output and sequence metadata

**PUSH/PULL Pattern** (Workers → Controller):
- **Use Case**: Collecting execution results from workers
- **Characteristics**: Many-to-one, load balancing, back-pressure support
- **Message Type**: StepOutputs with sampler results and completion status

**Pipeline Parallelism Specific Pattern**:
- **Use Case**: Stage completion signaling in pipeline parallelism
- **Pattern**: Additional PUSH/PULL for microbatch tracking

### Message Flow Architecture

```
1. Controller broadcasts schedule
   ┌─────────────┐    [StepInputs]    ┌─────────────┐
   │ Controller  │ ──────[PUB]──────> │   Workers   │
   └─────────────┘                    └─────────────┘

2. Workers execute model with NCCL
   ┌─────────────┐                    ┌─────────────┐
   │   Worker1   │ ◄─[AllReduce/Send]─┤   Worker2   │
   └─────────────┘                    └─────────────┘

3. Workers return results
   ┌─────────────┐   [StepOutputs]    ┌─────────────┐
   │   Workers   │ ──────[PUSH]─────> │ Controller  │
   └─────────────┘                    └─────────────┘
```

### Protocol Buffer Integration

**Design Decision**: Use Protocol Buffers for serialization to ensure:
- **Version Compatibility**: Schema evolution support
- **Efficient Encoding**: Compact binary representation
- **Language Independence**: The data plane can operate in both Python & C++

**Key Message Types**:
- `StepInputs`: Scheduler decisions and sequence parameters
- `StepOutputs`: Sampler results and completion status
- `StepMicrobatchOutputs`: Pipeline stage completion signals
