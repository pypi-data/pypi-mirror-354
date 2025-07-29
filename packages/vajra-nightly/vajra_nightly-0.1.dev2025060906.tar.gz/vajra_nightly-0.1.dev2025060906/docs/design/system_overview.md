# System Overview

Vajra employs a multi-level hierarchy for resource allocation and scheduling:

```
╔═══════════════════════════════════════════════════════════╗
║                    InferenceEngine                        ║
║                  (Global Coordination)                    ║
╚═══════════════════════════╤═══════════════════════════════╝
                            │
            ╔═══════════════▼═══════════════╗
            ║     ReplicasetController      ║
            ║    (Inter-replica sched.)     ║
            ╚═══════════════╤═══════════════╝
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ╔════▼════╗         ╔════▼════╗         ╔════▼════╗
   ║  RC-1   ║         ║  RC-2   ║         ║  RC-3   ║
   ║ (Intra- ║         ║ (Intra- ║         ║ (Intra- ║
   ║ replica ║         ║ replica ║         ║ replica ║
   ║ coord.) ║         ║ coord.) ║         ║ coord.) ║
   ╚════╤════╝         ╚════╤════╝         ╚════╤════╝
        │                   │                   │
   ┌────┼────┐         ┌────┼────┐         ┌────┼────┐
   │    │    │         │    │    │         │    │    │
 ┌─▼─┐┌─▼─┐┌─▼─┐     ┌─▼─┐┌─▼─┐┌─▼─┐     ┌─▼─┐┌─▼─┐┌─▼─┐
 │W1 ││W2 ││W3 │     │W4 ││W5 ││W6 │     │W7 ││W8 ││W9 │
 │GPU││GPU││GPU│     │GPU││GPU││GPU│     │GPU││GPU││GPU│
 └───┘└───┘└───┘     └───┘└───┘└───┘     └───┘└───┘└───┘
```

This hierarchy enables efficient scaling by distributing coordination responsibilities and avoiding centralized bottlenecks.


## Component Architecture

### Control Plane Components

**InferenceEngine**
- Global request coordination and load balancing
- Cross-replicaset resource allocation
- System-wide metrics aggregation and health monitoring

**ReplicasetController**  
- Manages a group of replicas serving identical model configurations
- Implements inter-replica load balancing strategies (round-robin, pull-based)
- Coordinates resource allocation across replica boundaries

**ReplicaController**
- Controls execution within a single replica (group of workers)
- Implements sophisticated scheduling policies (FCFS, EDF, LRS)
- Manages distributed state consistency across pipeline stages

### Data Plane Components

**Workers**
- Execute model computations on GPU devices
- Manage local KV cache storage and block allocation
- Handle tensor parallel communication within stages

**CacheEngine**
- Manages GPU memory allocation for KV cache storage
- Implements paged memory with block-based allocation
- Coordinates with distributed memory management for KVP

### Replicated Components

**SequenceManager**
- Maintains distributed sequence state across workers and control plane
- Coordinates sequence lifecycle events (schedule, execute, complete)

**Metrics Store**
- Collects metrics from all components including request level metrics, gpu/cpu operation runtimes
- Enables metrics aggeration from different sources

## Execution Model

### Request Processing Pipeline

```
1. Request Arrival
   ├─> InferenceEngine.AddRequest()
   └─> EngineMetricsStore.OnRequestArrival()

2. Replicaset Assignment  
   ├─> ReplicasetScheduler.Schedule()
   └─> Load balancing across replicas

3. Replica Scheduling
   ├─> ReplicaScheduler.Schedule()
   ├─> Memory allocation and batch formation
   └─> Priority-based preemption if needed

4. Worker Execution
   ├─> Model forward pass
   ├─> Attention computation with KV cache
   └─> Token sampling and generation

5. Result Processing
   ├─> Sequence state updates
   ├─> Output token aggregation
   └─> Request completion detection
```

### Parallelism Integration

Vajra implements three-dimensional parallelism to maximize hardware utilization:

**Pipeline Parallel (PP)**
- Distributes transformer layers across pipeline stages
- Enables processing of different microbatches simultaneously
- Supports both traditional and sequence-level pipeline parallelism

**Tensor Parallel (TP)**
- Shards individual layers across multiple GPUs within a stage
- Uses efficient all-reduce communication for gradient synchronization
- Minimizes communication overhead through operator fusion

**KV-Parallel (KVP)**  
- Distributes KV cache across memory groups for long sequences
- Enables sequences exceeding single-GPU memory capacity
- Coordinates memory allocation across distributed KV storage

**Note**: KV parallelism is not currently functional in main.

## Design Rationale

### Hierarchical vs. Flat Architecture

Traditional inference systems often employ flat architectures where a single scheduler manages all resources. Vajra's hierarchical approach provides several advantages:

**Scalability**: Each level handles a manageable number of entities, preventing coordination bottlenecks

**Flexibility**: Different scheduling policies can be applied at different levels

**Fault Isolation**: Failures at one level don't cascade to the entire system

**Load Distribution**: Coordination overhead is distributed across multiple controllers

### Event-Driven vs. Synchronous Design

The event-driven architecture provides us the following advantages:

- **Loose Coupling**: Components can evolve independently
- **Observable Behavior**: All state transitions are visible for debugging and metrics
- **Easy Asynchronous Processing**: Allows integration of asynchronous execution


## External Interfaces

The system provides multiple interfaces for different use cases:

- **OpenAI-compatible API**: Standard REST interface for application integration
- **Benchmark runner**: Performance evaluation and comparative analysis
- **Offline inference**: Batch processing for research and data pipeline integration

### Monitoring and Observability

Comprehensive metrics collection enables operational visibility:

- **Request-level metrics**: Latency, throughput, and completion statistics
- **System-level metrics**: Memory utilization, GPU usage, and queue depths
- **Component-level metrics**: Scheduling decisions, preemption events, and error rates
- **Performance profiling**: Detailed timing analysis for optimization

The hierarchical architecture and event-driven coordination combine to create a system capable of efficiently serving diverse LLM inference workloads while maintaining operational simplicity and observability.
