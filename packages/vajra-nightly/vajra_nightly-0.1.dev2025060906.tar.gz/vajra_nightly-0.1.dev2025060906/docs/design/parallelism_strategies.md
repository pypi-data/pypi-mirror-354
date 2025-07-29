# Parallelism Strategies

## Introduction

Vajra implements a comprehensive three-dimensional parallelism framework that enables efficient scaling across diverse hardware configurations. The system combines pipeline parallelism (PP), tensor parallelism (TP), and KV-parallelism (KVP) to maximize throughput while supporting sequences that exceed single-GPU memory capacity.

## Parallelism Dimensions

### Configuration Overview

```cpp
struct ParallelConfig {
    std::size_t pipeline_parallel_size;       // PP degree
    std::size_t tensor_parallel_size;         // TP degree  
    std::size_t kv_parallel_size;             // KVP degree
    std::size_t max_num_tokens_per_kvp_group; // KVP granularity
    std::size_t world_size;                   // PP × TP × KVP
};
```

### Three-Dimensional Layout

The system organizes GPUs in a **3D grid** (PP × KVP × TP):

```
32 GPUs = 4 (PP) × 4 (KVP) × 2 (TP)

Pipeline Stage 0: [KVP0: TP0,TP1] [KVP1: TP0,TP1] [KVP2: TP0,TP1] [KVP3: TP0,TP1]
Pipeline Stage 1: [KVP0: TP0,TP1] [KVP1: TP0,TP1] [KVP2: TP0,TP1] [KVP3: TP0,TP1]
Pipeline Stage 2: [KVP0: TP0,TP1] [KVP1: TP0,TP1] [KVP2: TP0,TP1] [KVP3: TP0,TP1]
Pipeline Stage 3: [KVP0: TP0,TP1] [KVP1: TP0,TP1] [KVP2: TP0,TP1] [KVP3: TP0,TP1]
```

Each dimension serves a distinct purpose:
- **PP**: Model layers across stages
- **TP**: Model weights within layers  
- **KVP**: Sequence tokens across memory groups

## Pipeline Parallelism (PP)

### Key Approach

Vajra's pipeline parallelism implements **asynchronous execution** with:

**Multi-threaded Controller**: Separate threads for scheduling, monitoring, and output collection

**Dynamic Microbatching**: Adaptive batch formation based on sequence characteristics

**Sequence-Level Pipelining**: Intra-sequence parallelism for long context prefills (inspired by Medha)

### Three-Thread Architecture

```cpp
class PipelineParallelLlmReplicaController {
    std::thread scheduler_thread_;           // Main scheduling loop
    std::thread microbatch_watcher_thread_;  // Monitors stage completions  
    std::thread output_thread_;              // Collects final outputs
};
```

Each thread has distinct responsibilities:
- **Scheduler**: Forms batches and sends to workers
- **Microbatch Watcher**: Tracks first stage completions
- **Output Collector**: Aggregates results from final stage

### Sequence Pipeline Parallelism (SPP)

Traditional pipeline parallelism processes entire sequences at single stages. Vajra enables **intra-sequence pipelining**:

```
Traditional PP:
Stage 0: [Seq A: tokens 0-512] → [Seq B: tokens 0-512]
Stage 1: idle → [Seq A: tokens 0-512] → [Seq B: tokens 0-512]

Sequence-Level PP:
Stage 0: [Seq A: tokens 0-512] → [Seq A: tokens 512-1024]
Stage 1: idle → [Seq A: tokens 0-512] → [Seq A: tokens 512-1024]
```

**Benefits**:
- Faster processing of long sequences
- Reduced pipeline bubbles
- Better GPU utilization  

## Tensor Parallelism (TP)

### Design Approach

Tensor parallelism splits model weights across GPUs within each layer:

**Column Parallelism**: Linear layers split along output dimension

**Row Parallelism**: Subsequent layers split along input dimension

**All-Reduce Communication**: Synchronizes gradients across TP group

We use Megatron-LM style weight sharding to minimize communication overhead.

### Integration with Pipeline Stages

Each pipeline stage contains a complete TP group:

```
Pipeline Stage 0:
├── TP Rank 0: [Layer 0-7 weights, columns 0-2047]
└── TP Rank 1: [Layer 0-7 weights, columns 2048-4095]

Pipeline Stage 1:  
├── TP Rank 0: [Layer 8-15 weights, columns 0-2047]
└── TP Rank 1: [Layer 8-15 weights, columns 2048-4095]
```

## KV-Parallelism (KVP)

### Design Rationale

KV-parallelism addresses decode latency issue in extreme long context processing by sharding the KV cache across the sequence dimension, please refer to Medha for more details.

### Token Distribution Strategy

Sequences are distributed across KVP groups by **token ranges**:

```
Sequence with 1M tokens, 4 KVP groups:
KVP0: tokens [0 : 250K]      - Stores first quarter of KV cache
KVP1: tokens [250K : 500K]   - Stores second quarter  
KVP2: tokens [500K : 750K]   - Stores third quarter
KVP3: tokens [750K : 1M]     - Stores final quarter
```

### Memory Coordination

**Group Assignment**: Sequences assigned to KVP groups based on token ranges

**Atomic Allocation**: Memory allocation succeeds across all groups or fails completely

**Independent Scheduling**: Each KVP group maintains separate memory management

## Design Trade-offs

### Pipeline Parallelism

**Advantages**:
- Good scalability with minimal communication overhead across nodes or on commodity hardware

**Challenges**:
- Pipeline bubbles can hurt efficiency

### Tensor Parallelism

**Advantages**:
- Reduces latency 
- Simple programming model
- Good for wide range models

**Challenges**:
- High communication overhead
- Limited scalability (typically 2-8 GPUs)
- Requires fast interconnect

### KV-Parallelism

**Advantages**:
- Enables low-latency decodes for ultra-long sequences

**Challenges**:
- Complex memory coordination
- Potential load imbalancing
