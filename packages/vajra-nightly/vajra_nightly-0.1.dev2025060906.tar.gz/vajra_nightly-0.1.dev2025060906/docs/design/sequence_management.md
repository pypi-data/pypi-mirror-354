# Sequence Management

## Introduction

Sequence management is the central orchestration component in Vajra that maintains distributed state consistency, handles lifecycle transitions, and coordinates execution across workers. All sequence state mutations must flow through the sequence manager to ensure correctness in distributed, pipelined execution.

## Sequence Lifecycle and State Semantics

### Core State Machine

```
                    ┌─────────────┐
                    │   WAITING   │ (Initial arrival)
                    └──────┬──────┘
                           │ Schedule()
                    ┌──────▼──────┐
          ┌─────────┤   RUNNING   ├─────────┐
          │         └──────┬──────┘         │
          │                │                │
     Preempt()      ┌──────▼──────┐   CheckStop()
          │         │   PAUSED    │         │
          │         └──────┬──────┘         │
          │                │                │
          │          Resume()               │
          │                │                │
    ┌─────▼─────────┐      │        ┌───────▼────┐
    │WAITING_PREEMPT│◄─────┘        │  FINISHED  │
    └───────────────┘               └────────────┘
```

### State Semantics

**WAITING**: Sequence has arrived but not yet scheduled for execution
- Memory not allocated
- Queued based on priority policy (FCFS, EDF, LRS)
- Can transition to RUNNING or IGNORED

**RUNNING**: Sequence is actively being processed
- Memory allocated
- Undergoing actual execution on the worker
- Can transition to PAUSED, FINISHED, or WAITING_PREEMPT

**PAUSED**: Sequence temporarily suspended
- Memory remains allocated
- Waiting to be scheduled again
- Automatically transitions back to RUNNING

**WAITING_PREEMPT**: Sequence was preempted due to resource pressure
- Memory freed and returned to pool
- Retains processing state for resumption
- Returns to priority queue for rescheduling

**FINISHED**: Sequence has completed generation
- Triggered by stop conditions
- Memory freed, final output generated
- Terminal state

## State Replication and Sequence Manager Architecture

### Distributed Coordination Challenge

Vajra's distributed architecture creates a fundamental challenge: **multiple components need consistent views of sequence state**. Consider the coordination required:

- **Controllers** need to make scheduling decisions based on current sequence progress
- **Workers** need to track execution state and coordinate memory allocation

Without consistent state management abstraction, these components could have inconsistent views leading to memory leaks and race conditions.

### State Replication Protocol

**Mutation Invariant**: All sequence state changes must flow through sequence managers to maintain consistency.

```cpp
class BaseSequenceManager {
protected:
    std::recursive_mutex mutex_;                    // Thread safety
    std::unordered_map<std::string, MutableSequencePtr> seq_map_;  // Sequence registry
    
public:
    // All mutations go through these controlled methods
    virtual void OnSchedule(SchedulerOutputPtr scheduler_output) = 0;
    virtual void OnStepCompleted(/* parameters */) = 0;
    virtual void OnStageCompleted(/* parameters */) = 0;
    virtual void PreemptSeq(const std::string& seq_id) = 0;
    virtual void FreeSeq(const std::string& seq_id) = 0;
};
```

Both the control plane and data plane have their own copies of the sequence manage:

```
Controller (EngineSequenceManager)
├── Authoritative state management
├── Token detokenization  
├── Stop condition evaluation
└── Output generation

Workers (WorkerSequenceManager)  
├── Execution state tracking
├── KV cache management
├── Block table coordination
└── Pipeline stage progress
```

### Synchronization Events

**OnSchedule**: Controller notifies workers of scheduling decisions
- Transitions sequences: WAITING → RUNNING  
- Handles preemptions: RUNNING → WAITING_PREEMPT
- Manages ignored sequences: WAITING → IGNORED

**OnStepCompleted**: Workers report full processing completion
- Evaluates stop conditions  
- Updates step_processed counters
- Generates new tokens for decode

**OnStageCompleted**: Workers report stage processing completion (PP only)
- Updates stage_processed counters
- Enables sequence pipeline parallelism
- Coordinates pipeline handoffs


## Step Processed vs Stage Processed Semantics

### Pipeline Parallelism Motivation

In pipeline parallelism, model layers are distributed across multiple stages, and sequences flow through these stages sequentially. This creates a challenge: **when has a sequence actually completed processing?**

Consider a 2-stage pipeline processing a long sequence:
- **Stage 0** processes the first half of the sequence
- **Stage 1** processes the second half, but also receives output from Stage 0

Without proper tracking, we might incorrectly evaluate stop conditions or generate outputs based on partially processed sequences. Vajra solves this with two distinct progress counters.

### Processing Granularity

### Step Processed
**Definition**: Tokens that have completed **all pipeline stages** and are fully processed

**Scope**: Complete end-to-end processing

**Usage**: 
- Determines final output text
- Used for stop condition evaluation
- Represents actual inference completion

```cpp
class Sequence {
    std::size_t num_tokens_step_processed_ = 0;  // Fully processed tokens
    
    bool IsStepProcessingComplete() const {
        return num_tokens_step_processed_ >= GetPromptLength();
    }
};
```

### Stage Processed  

**Definition**: Tokens that have completed processing at the **current pipeline stage** or **first stage** for control plane.

**Scope**: Single pipeline stage completion

**Usage**:
- Enables sequence pipeline parallelism
- Coordinates pipeline stage handoffs
- Tracks partial processing progress

```cpp
class Sequence {
    std::size_t num_prompt_tokens_stage_processed_ = 0;  // Current stage only
    
    bool GetPromptStageProcessingFinished() const {
        return num_prompt_tokens_stage_processed_ >= GetPromptLength();
    }
};
```

### Example: Pipeline Processing

```
Sequence with 1000 tokens, 2 pipeline stages (PP=2):

Time 0: Stage 0 starts processing tokens 0-500
        step_processed = 0    (nothing fully complete)
        stage_0_processed = 0  (stage 0 in progress)
        stage_1_processed = 0  (stage 1 idle)

Time 1: Stage 0 completes tokens 0-500, Stage 1 starts processing them
        step_processed = 0    (tokens in Stage 1, not fully complete)
        stage_0_processed = 500  (stage 0 completed first batch)
        stage_1_processed = 0    (stage 1 in progress)

Time 2: Stage 0 processes tokens 500-1000, Stage 1 completes tokens 0-500
        step_processed = 500  (tokens 0-500 completed both stages)
        stage_0_processed = 1000 (stage 0 completed all tokens)
        stage_1_processed = 500  (stage 1 completed first batch)

Time 3: Stage 1 completes tokens 500-1000
        step_processed = 1000 (all tokens completed both stages)
        stage_0_processed = 1000
        stage_1_processed = 1000
```

This distinction enables Vajra to:
- **Pipeline Coordination**: Track progress across distributed pipeline stages
- **Sequence Pipelining**: Allow partial sequences to flow through pipeline
- **Stop Condition Accuracy**: Only evaluate stops on fully processed tokens
