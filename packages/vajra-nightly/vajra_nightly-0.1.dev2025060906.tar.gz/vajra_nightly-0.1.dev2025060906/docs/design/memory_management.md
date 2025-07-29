# Memory Management

## Introduction

Memory management is a critical challenge in LLM inference due to massive KV cache requirements that scale with sequence length and batch size. Vajra implements a sophisticated paged memory management system with paged attention, providing efficient memory utilization while preventing out-of-memory conditions.

## Core Design Principles

### Paged Memory Architecture

Vajra uses a **block-based memory allocation** system that divides KV cache memory into fixed-size blocks, similar to virtual memory paging in operating systems:

- **Fixed Block Size**: Typically 16 tokens per block for balance between fragmentation and overhead
- **Logical-to-Physical Mapping**: Sequences use logical token blocks that map to physical memory blocks
- **Dynamic Allocation**: Blocks allocated on-demand as sequences grow during generation

### Watermark-Based Protection

The system maintains a **memory watermark** to prevent out-of-memory conditions:

- **Reserve Capacity**: Maintains a configurable percentage of free blocks (e.g., 1% = 10 blocks out of 1000)
- **Allocation Guard**: Prevents allocations that would breach the watermark threshold
- **Preemption Trigger**: When memory is tight, lower-priority sequences are preempted to free space

## Memory Components

### BlockSpaceManager

The core memory allocator that manages the logical-to-physical block mapping:

```cpp
class BlockSpaceManager {
private:
    int block_size_;              // Tokens per block (typically 16)
    int num_total_gpu_blocks_;    // Total available blocks  
    float watermark_;             // Free block ratio to maintain
    
    // Sequence ID → Physical block IDs mapping
    std::unordered_map<std::string, BlockTablePtr> block_tables_;
    std::vector<int> free_blocks_;
};
```

**Key Operations**:
- **Allocate**: Reserve blocks for new sequences
- **AppendSlot**: Add blocks as sequences grow
- **Free**: Return blocks when sequences complete
- **CanAllocate**: Check if allocation would breach watermark

### LogicalTokenBlock

Organizes tokens within sequences into block-sized chunks:

```cpp
struct LogicalTokenBlock {
    const std::size_t block_number;   // Logical block index
    const std::size_t block_size;     // Capacity (e.g., 16 tokens)
    
private:
    std::vector<std::size_t> token_ids_;  // Actual tokens
    std::size_t num_tokens_;              // Current occupancy
};
```

**Benefits**:
- **Eliminates External Fragmentation**: All allocations are block-sized
- **Enables Efficient Preemption**: Can free memory in block-sized chunks
- **Supports Incremental Growth**: Add blocks as sequences generate new tokens

## Distributed Memory (KVP System)

### KVP State Tracker

For sequences that exceed single-GPU memory capacity, the **KVP (KV-Parallel) system** distributes memory across multiple workers:

**Group-Based Allocation**: Sequences are assigned to KVP groups based on token ranges
**Cross-Worker Coordination**: Ensures atomic allocation/deallocation across all workers
**Block Counting**: Tracks block usage per group to prevent overallocation

### Memory Coordination

```cpp
class KvpStateTracker {
    // Per-KVP-group block managers
    std::vector<std::unique_ptr<BlockSpaceManager>> block_managers_;
    
    // Atomic allocation across groups
    std::pair<bool, int> Allocate(const SequencePtr& seq);
};
```

**Atomic Operations**: Allocation either succeeds across all groups or fails completely, preventing deadlocks.

## Allocation Strategies

### Bulk Allocation

The scheduler uses **bulk allocation** to avoid memory deadlocks:

- **Upfront Allocation**: Allocate all estimated blocks when sequence arrives
- **Prevents Partial Allocation**: Avoids scenarios where sequences block each other
- **Watermark Checking**: Ensure each allocation maintains memory safety
- **Trade-off**: Higher memory usage but eliminates allocation deadlocks and frequent preemptions

### Incremental Growth

During generation, sequences need additional blocks:

- **Single Block Allocation**: Typically add one block at a time as tokens generate
- **Preemption Fallback**: If allocation fails, preempt lower-priority sequences

## Memory Safety Mechanisms

### Preemption System

When memory pressure occurs:

1. **Priority-Based Selection**: Choose lowest-priority sequences for preemption
2. **Immediate Deallocation**: Free all blocks associated with preempted sequences  
3. **State Preservation**: Preempted sequences return to waiting queue with preserved state
4. **Memory Availability**: Freed memory immediately available for higher-priority sequences

## Design Trade-offs

### Block Size Selection

**Smaller Blocks (8 tokens)**:
- ✅ Reduced internal fragmentation
- ✅ Finer-grained prefix cache sharing
- ❌ Higher attention and metadata management overhead

**Larger Blocks (32 tokens)**:
- ✅ Lower metadata and attention overhead  
- ❌ Higher internal fragmentation

**Standard Choice (16 tokens)**: Balances trade-offs for typical workloads.

### Memory vs. Latency Trade-offs

**Bulk Allocation**:
- ✅ Prevents allocation deadlocks
- ✅ Predictable memory requirements
- ❌ Higher memory usage
- ❌ May prevent admission of more sequences

**Incremental Allocation**:
- ✅ Lower memory usage
- ✅ Better memory utilization
- ❌ Risk of allocation deadlocks
- ❌ Frequent preemptions due to OOMs

## Integration with Scheduling

The memory management system tightly integrates with the scheduler:

**Memory-Aware Admission**: Scheduler checks memory availability before admitting sequences

**Priority-Based Preemption**: Memory pressure triggers preemption of lowest-priority sequences

**Batch Formation**: Memory constraints influence batch composition and size

**Resource Coordination**: KVP system coordinates memory across distributed worker

This integrated approach ensures that scheduling decisions consider memory availability, while memory management respects scheduling priorities, creating a cohesive system that efficiently utilizes available resources.
