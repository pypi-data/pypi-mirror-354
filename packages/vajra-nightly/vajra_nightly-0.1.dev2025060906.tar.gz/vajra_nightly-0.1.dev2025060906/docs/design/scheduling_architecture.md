# Scheduling Architecture

## Introduction

The scheduling subsystem in Vajra represents one of the most sophisticated components of the system, implementing a multi-level hierarchy that balances efficiency, fairness, and latency requirements. This chapter provides an in-depth analysis of the scheduling architecture, from high-level request distribution to fine-grained token-level scheduling.

## Scheduling Hierarchy

Vajra implements a three-level scheduling hierarchy:

```
┌─────────────────────────────────────────────────────────┐
│             RequestPrioritizer                          │
│        (Request-level prioritization)                   │
│  - Assigns priorities to sequences                      │
│  - Determines preemption order                          │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               ReplicasetScheduler                       │
│         (Inter-replica scheduling)                      │
│  - Distributes requests across replicas                 │
│  - Load balancing strategies                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                ReplicaScheduler                         │
│          (Intra-replica scheduling)                     │
│  - Forms execution batches                              │
│  - Manages memory allocation                            │
│  - Handles preemption                                   │
└─────────────────────────────────────────────────────────┘
```

## Request Prioritization Framework

### Role of RequestPrioritizer

The RequestPrioritizer is a critical component that sits at the boundary between the InferenceEngine and the scheduling subsystem. It transforms incoming sequences into priority-wrapped objects that determine scheduling order throughout the system.

**Key Responsibilities**:
1. **Priority Assignment**: Assigns numerical priorities to sequences based on configured policy
2. **Preemption Ordering**: Determines which sequences to preempt under memory pressure
3. **Fairness Enforcement**: Ensures starvation-free scheduling through priority mechanisms
4. **Dynamic Adjustment**: Supports policies that recalculate priorities during execution

**Integration Flow**:
```cpp
// 1. User request arrives at InferenceEngine
UserSequenceParams user_params{seq_id, prompt, sampling_params};

// 2. LlmReplicasetController receives and tokenizes
MutableSequencePtr seq = std::make_shared<Sequence>(seq_params);

// 3. RequestPrioritizer wraps with priority
auto seq_with_priority = request_prioritizer_->GetSeqWithPriority(seq);

// 4. ReplicasetScheduler distributes to replica
replica_scheduler_->Schedule(seq_with_priority);

// 5. ReplicaScheduler uses priority for ordering
waiting_->push(seq_with_priority);  // Priority queue insertion
```

### BaseRequestPrioritizer Interface

All prioritizers implement a simple but powerful interface:

```cpp
class BaseRequestPrioritizer {
public:
    // Core interface - wraps sequence with priority
    virtual MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
        MutableSequencePtr seq) = 0;
        
    virtual ~BaseRequestPrioritizer() = default;
};
```

The returned `BaseSequenceWithPriority` object:
```cpp
class BaseSequenceWithPriority {
protected:
    MutableSequencePtr sequence_;
    
public:
    BaseSequenceWithPriority(MutableSequencePtr seq) : sequence_(seq) {}
    
    // Pure virtual - subclasses define priority calculation
    virtual float GetPriority() const = 0;
    
    MutableSequencePtr GetSequence() const { return sequence_; }
};
```

### Priority Semantics

Vajra implements a sophisticated priority system with **lower numerical values indicating higher priority**:

```cpp
struct BaseSequenceWithPriorityComparator {
    bool operator()(const MutableBaseSequenceWithPriorityPtr& a,
                    const MutableBaseSequenceWithPriorityPtr& b) const {
        // Lower numerical priority = higher actual priority
        if (a->GetPriority() != b->GetPriority()) {
            return a->GetPriority() < b->GetPriority();
        }
        // Deterministic tie-breaking
        return a->GetSequence()->seq_id < b->GetSequence()->seq_id;
    }
};
```

### FCFS (First-Come-First-Served) Prioritizer

The simplest prioritizer uses arrival time as priority:

```cpp
class SequenceWithFcfsPriority : public BaseSequenceWithPriority {
public:
    [[nodiscard]] float GetPriority() const override {
        return static_cast<float>(GetSequence()->arrival_time);
    }
};
```

**Characteristics**:
- Fair ordering based on arrival
- No starvation
- Suitable for homogeneous workloads

### EDF (Earliest-Deadline-First) Prioritizer

EDF assigns priorities based on computed deadlines:

```cpp
class EdfRequestPrioritizer : public BaseRequestPrioritizer {
private:
    std::shared_ptr<PrefillTimeCalculator> prefill_time_calculator_;
    
public:
    MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
        MutableSequencePtr seq) override {
        
        // Estimate prefill time using execution predictor
        auto prefill_time = 
            prefill_time_calculator_->GetPrefillTime(seq->GetPromptLength());
            
        // Compute deadline with multiplier
        double deadline_time = std::max(
            prefill_time * config_.deadline_multiplier,
            config_.min_deadline);
            
        // Absolute deadline = arrival_time + deadline_time
        double deadline = deadline_time + seq->arrival_time;
        
        return std::make_shared<SequenceWithEdfPriority>(
            seq, static_cast<float>(deadline));
    }
};
```

**Key Features**:
- Uses Vidur execution time predictor
- Configurable deadline multiplier
- Minimum deadline guarantee

### LRS (Least-Remaining-Slack) Prioritizer

The most sophisticated prioritizer that dynamically adjusts priorities:

```cpp
class SequenceWithLrsPriority : public BaseSequenceWithPriority {
public:
    [[nodiscard]] float GetPriority() const override {
        auto seq = GetSequence();
        
        // Remaining work estimation
        auto remaining_prefill_time = prefill_time_calculator_->GetPrefillTime(
            seq->GetPromptLength(),
            seq->GetNumPromptTokensStageProcessed());
            
        // Slack = deadline - current_time - remaining_work
        auto slack = seq->arrival_time + deadline_time_ - 
                    time_utils::now_s() - remaining_prefill_time;
                    
        // Normalized slack (higher slack = lower priority)
        return slack / deadline_time_;
    }
};
```

**Advanced Properties**:
- **Dynamic Priority**: Recalculated on each access
- **Progress-Aware**: Accounts for partially processed tokens
- **Urgency-Based**: Lower slack means higher urgency

### Priority Queue Integration

The RequestPrioritizer works seamlessly with the scheduler's priority queues:

```cpp
// Priority queue definition in BaseReplicaScheduler
using SequencePriorityQueue = boost::concurrent::sync_priority_queue<
    MutableBaseSequenceWithPriorityPtr,
    std::vector<MutableBaseSequenceWithPriorityPtr>,
    BaseSequenceWithPriorityComparator>;

SequencePriorityQueuePtr waiting_;  // Sequences waiting to be scheduled

// Multiset for partial prefills (also priority ordered)
std::multiset<MutableBaseSequenceWithPriorityPtr,
              BaseSequenceWithPriorityComparator> partial_prefills_;
```

**Key Points**:
- Sequences maintain their priority wrapper throughout their lifecycle
- Priority queues automatically order sequences by priority
- Dynamic priority policies (like LRS) are recalculated on each access
- Preemption decisions use the same priority ordering


### RequestPrioritizer in Multi-Replica Settings

In a multi-replica setting, the RequestPrioritizer is shared among replicas within each replicaset:

```cpp
// From LlmReplicasetController constructor signature
LlmReplicasetController(
    std::shared_ptr<LlmReplicasetControllerConfig> config,
    const std::string& tokenizer_path,
    TokenId eos_token_id,
    UserSequenceParamQueuePtr waiting_queue,
    RequestOutputQueuePtr output_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,  // Shared among replicas
    std::shared_ptr<BaseReplicasetScheduler> replicaset_scheduler);
```

**Architecture Structure**:
```
InferenceEngine
├── Replicaset 1
│   ├── RequestPrioritizer (shared)
│   ├── Replica 1.1 ── uses ──┐
│   ├── Replica 1.2 ── uses ──┼── RequestPrioritizer
│   └── Replica 1.3 ── uses ──┘
└── Replicaset 2
    ├── RequestPrioritizer (shared)
    ├── Replica 2.1 ── uses ──┐
    └── Replica 2.2 ── uses ──┼── RequestPrioritizer
                              ┘
```

**Sharing Benefits**:
- **Consistent Priority Assignment**: All replicas within a replicaset apply identical prioritization logic
- **Unified Policy Management**: Single point of configuration per replicaset

**Cross-Replicaset Considerations**:
- Each replicaset maintains its own RequestPrioritizer instance
- Different replicasets can apply different prioritization policies if needed
- Global fairness maintained through consistent priority assignment within each replicaset

This design ensures that within a replicaset, all replicas make consistent scheduling decisions based on the same prioritization logic, while allowing different replicasets to potentially use different prioritization strategies.

## ReplicasetScheduler Design

### Core Abstraction

The `BaseReplicasetScheduler` defines the interface for distributing requests across replicas:

```cpp
// From csrc/include/vajra/native/core/scheduler/replicaset_schedulers/BaseReplicasetScheduler.h
class BaseReplicasetScheduler : public NonCopyableNonMovable {
public:
    BaseReplicasetScheduler(std::shared_ptr<BaseReplicasetSchedulerConfig> config,
                          std::size_t num_replicas)
        : config_(config), num_replicas_(num_replicas) {}

    virtual ~BaseReplicasetScheduler() = default;

    [[nodiscard]] virtual SequencePriorityQueuePtr GetReplicaQueue(
        ReplicaId replica_id) const = 0;

    virtual void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) = 0;

protected:
    std::shared_ptr<BaseReplicasetSchedulerConfig> config_;
    std::size_t num_replicas_;
};
```

### Round-Robin Implementation

The `RoundRobinReplicasetScheduler` provides simple load distribution:

```cpp
class RoundRobinReplicasetScheduler : public BaseReplicasetScheduler {
private:
    std::size_t current_replica_index_ = 0;
    std::vector<SequencePriorityQueuePtr> replica_queues_;
    
public:
    SequencePriorityQueuePtr GetReplicaQueue(ReplicaId replica_id) const override {
        return replica_queues_[replica_id];
    }
    
    void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) override {
        // Round-robin assignment to replica queues
        auto target_queue = replica_queues_[current_replica_index_];
        target_queue->push(seq);
        current_replica_index_ = (current_replica_index_ + 1) % num_replicas_;
    }
};
```

### Pull-Based Scheduling

The `PullReplicasetScheduler` implements a dynamic approach where the replica schedulers can pull requests rather the replicaset scheduler making an early-binding decision.

```cpp
class PullReplicasetScheduler : public BaseReplicasetScheduler {
private:
    // Single shared queue that all replicas pull from
    SequencePriorityQueuePtr shared_queue_;
    
public:
    SequencePriorityQueuePtr GetReplicaQueue(ReplicaId replica_id) const override {
        // All replicas share the same queue
        return shared_queue_;
    }
    
    void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) override {
        // Add to shared queue - replicas pull when ready
        shared_queue_->push(seq);
    }
};
```

## ReplicaScheduler Design

### Core Design Philosophy

The ReplicaScheduler represents the heart of Vajra's scheduling system, implementing sophisticated resource allocation and batch formation within a single replica. The design prioritizes three key objectives:

**Memory-Aware Scheduling**: All scheduling decisions consider available KV cache memory, ensuring sequences can execute without memory allocation failures.

**Priority-Based Resource Management**: Higher priority sequences receive preferential treatment in both allocation and preemption decisions.

**Batch Formation Optimization**: Intelligent batching maximizes hardware utilization while respecting resource constraints.

### State Management Architecture

The scheduler maintains several critical data structures that enable efficient coordination:

```cpp
class BaseReplicaScheduler : public NonCopyableNonMovable {
protected:
    // Priority-ordered sequences awaiting resource allocation
    SequencePriorityQueuePtr waiting_;
    
    // Currently executing sequences (decode phase)
    MutableSequences running_;
    
    // Sequences with partially processed prompts
    std::multiset<MutableBaseSequenceWithPriorityPtr,
                  BaseSequenceWithPriorityComparator> partial_prefills_;
    
    // Distributed memory coordination
    std::shared_ptr<KvpStateTracker> kvp_state_tracker_;
    
    // Request prioritization policy
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer_;
};
```

**Waiting Queue**: Priority-ordered sequences awaiting resource allocation and scheduling. Uses a thread-safe priority queue with configurable prioritization strategies.

**Running Sequences**: Currently executing sequences in their decode phase, guaranteed to have allocated memory and predictable resource requirements.

**Partial Prefills**: Sequences that have begun prefill processing but require additional scheduling rounds to complete prompt processing.

**Memory Tracking**: Distributed state tracker coordinating with the KVP (KV-Parallel) system for memory allocation across multiple workers.

### Three-Phase Scheduling Algorithm

The scheduler executes a carefully orchestrated four-phase algorithm each scheduling round:

```cpp
std::pair<SchedulerOutputPtr, MutableSequences> 
BaseReplicaScheduler::ScheduleInternal() {
    auto batch_formation_tracker = GetBatchFormationTracker();
    MutableSequences scheduled_seqs;
    
    // Phase 1: Schedule running sequences (decode)
    for (auto& seq : running_) {
        if (batch_formation_tracker->CanAddSeq(seq, 1) && 
            EnsureCanAppendSlot(seq, *batch_formation_tracker)) {
            batch_formation_tracker->AddSeq(seq, 1);
            scheduled_seqs.push_back(seq);
        }
    }
    
    // Phase 2: Continue partial prefills
    // Phase 3: Admit new sequences from waiting queue  
    
    return {BuildSchedulerOutput(scheduled_seqs), scheduled_seqs};
}
```

#### Phase 1: Decode Scheduling
Running sequences receive highest priority for continued execution. Each decode step requires exactly one additional KV cache slot, making resource requirements predictable. The scheduler ensures memory availability before committing to decode operations.

#### Phase 2: Partial Prefill Continuation  
Sequences with partially processed prompts continue their prefill operations. The scheduler dynamically determines optimal chunk sizes based on available resources and execution time predictions.

#### Phase 3: New Sequence Admission
Waiting sequences undergo admission control involving:
- **Memory allocation** through the distributed KVP state tracker
- **Priority evaluation** against currently running workloads  
- **Preemption analysis** to create space if necessary
- **Batch formation constraints** to maintain execution efficiency


### Priority-Based Preemption

The preemption system implements a sophisticated priority-aware mechanism:

**Graceful Preemption**: Sequences are preempted at natural boundaries (between tokens) rather than mid-computation.

**Memory Reclamation**: Preempted sequences release their KV cache allocations immediately, making memory available for higher-priority work.

**State Preservation**: Preempted sequences maintain their processing state and can be resumed when resources become available.

### Specialized Scheduler Implementations

The system provides three specialized scheduler implementations, each optimized for different workload characteristics:

```cpp
class BaseReplicaScheduler {
protected:
    // Key abstraction: determine chunk size for sequence
    virtual std::size_t GetSeqNextNumQTokens(
        const MutableSequencePtr& seq,
        const BatchFormationTracker& batch_formation_tracker) const = 0;
};

// Fixed-size chunks for predictable latency
class FixedChunkReplicaScheduler : public BaseReplicaScheduler {
protected:
    std::size_t GetSeqNextNumQTokens(...) const override {
        return std::min(seq->GetNumProcessableTokens(), 
                       config_->scheduling_chunk_size);
    }
};

// Adaptive chunks based on execution time prediction
class DynamicChunkReplicaScheduler : public BaseReplicaScheduler {
protected:
    std::size_t GetSeqNextNumQTokens(...) const override {
        // Use ML predictor to find optimal chunk size for target batch time
        return ComputeOptimalChunkSize(seq, batch_formation_tracker);
    }
};
```

#### Fixed Chunk Scheduler
- **Design Principle**: Predictable, uniform resource usage across all sequences
- **Use Case**: Workloads with consistent prompt lengths and latency requirements
- **Benefit**: Simplified capacity planning and predictable execution times

#### Dynamic Chunk Scheduler  
- **Design Principle**: Adaptive batching based on real-time execution predictions
- **Use Case**: Mixed workloads with varying prompt lengths and latency targets
- **Benefit**: Optimizes throughput by adapting batch sizes to current system state

#### Space Sharing Scheduler
- **Design Principle**: Resource isolation between different request classes  
- **Use Case**: Multi-tenant environments requiring performance guarantees
- **Benefit**: Prevents resource contention between different service tiers

### Dynamic Batch Formation 

The batch formation system incorporates multiple sophisticated tracking mechanisms:

**Resource Budget Tracking**: Monitors prefill tokens, decode tokens, and total computation budget to prevent resource overcommitment.

**Execution Time Prediction**: Uses machine learning models to predict batch execution times, enabling dynamic optimization using Vidur.

**Hardware Constraint Awareness**: Considers GPU memory limitations, tensor/pipeline parallel communication overhead, etc.

## Scheduling Lifecycle

### Step Execution Flow

1. **Schedule()** - Main scheduling entry point
   ```cpp
   auto [scheduler_output, scheduled_seqs] = scheduler->Schedule();
   ```

2. **OnStepCompleted()** - Post-execution callback
   ```cpp
   scheduler->OnStepCompleted(scheduled_seqs, execution_time);
   ```

3. **OnStageCompleted()** - Pipeline stage completion (PP > 1)
   ```cpp
   scheduler->OnStageCompleted(stage_seqs);
   ```

### State Transitions

```
WAITING ──Schedule()──> RUNNING ──OnStepCompleted()──> RUNNING/FINISHED
   ↑                        │
   └────Preempt()───────────┘
```

