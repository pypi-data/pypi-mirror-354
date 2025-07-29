# Event-Driven Architecture

## Introduction

Every major component interaction in Vajra from request scheduling to memory allocation, is orchestrated through events. This chapter demonstrates how the event system works in Vajra.

## Event System in Context

### Why Event Driven Design?

The distributed nature of Vajra, with its multi-level scheduling hierarchy and pipeline parallel execution, requires careful coordination across components that may be:

- **Physically Distributed**: Controllers and workers on different nodes
- **Temporally Decoupled**: Pipeline stages processing different microbatches
- **Logically Independent**: Schedulers, memory managers, and execution engines

Events provide the coordination mechanism that ties these components together while maintaining:
- **Loose Coupling**: Components don't need direct references to each other
- **Observable State**: All transitions are trackable for debugging and metrics
- **Asynchronous Execution**: Non-blocking operations maximize throughput

### Event Flow in the System Architecture

Recall from [system overview](./system_overview.md) the hierarchical architecture:

```
InferenceEngine → ReplicasetController → ReplicaController → Workers
```

Events flow through this hierarchy, triggering actions at each level:

```
AddRequest() → OnRequestArrival() → Schedule() → OnSchedule() → Execute() → OnStepCompleted()
     ↓               ↓                   ↓            ↓            ↓             ↓
[Engine Event]  [Metrics Event]    [Scheduler]  [Seq Manager] [Worker]    [Completion]
```

## Core Event Handlers

### Scheduling Events

The scheduling system is entirely event-driven. Each scheduling decision triggers cascading events:

```cpp
// In ReplicaController - triggering scheduling event
void ReplicaController::SchedulerStep() {
    // Schedule sequences
    auto [scheduler_output, scheduled_seqs] = scheduler_->Schedule();
    
    // Trigger sequence manager event
    auto [ignored_seqs, active_seqs] = 
        engine_sequence_manager_->OnSchedule(scheduler_output);
    
    // Trigger metrics event
    engine_metrics_store_->OnSchedule(scheduler_output);
    
    // Send to workers for execution
    SendToWorkers(scheduler_output, active_seqs);
}
```

### Execution Completion Events

When workers complete execution, they trigger a chain of events that update state across the system:

```cpp
// In Worker - after model execution
void Worker::ExecutionComplete(SamplerOutputs outputs) {
    // Send results back to controller
    SendOutputs(outputs);
}

// In ReplicaController - receiving completion
void ReplicaController::OnStepCompleted(
    SchedulerOutputPtr scheduler_output,
    const SamplerOutputs& sampler_outputs) {
    
    // Update sequence states
    engine_sequence_manager_->OnStepCompleted(
        scheduler_output->seq_schedule_metadata_list,
        sampler_outputs);
    
    // Update scheduler state
    scheduler_->OnStepCompleted(scheduled_seqs, execution_time);
    
    // Record metrics
    engine_metrics_store_->OnBatchEnd(sampler_outputs, execution_time);
    
    // Generate outputs for completed requests
    auto request_outputs = engine_sequence_manager_->GenerateRequestOutputs(
        ignored_seqs, scheduled_seqs);
        
    // Deliver to clients
    DeliverOutputs(request_outputs);
}
```

## Event-Driven State Management

### Sequence Lifecycle Events

The sequence lifecycle is entirely managed through events:

```
Request → OnRequestArrival() → WAITING
                                  ↓
                            OnSchedule() → RUNNING
                                  ↓
                         OnStepCompleted() → PAUSED/FINISHED
                                  ↓
                           OnRequestEnd() → Cleanup
```

Each transition triggers state updates across distributed components:

```cpp
// Sequence state transitions via events
void BaseSequenceManager::OnSchedule(SchedulerOutputPtr output) {
    // Handle preempted sequences
    for (auto seq_id : output->preempted_seq_ids) {
        PreemptSeq(seq_id);  // RUNNING → WAITING_PREEMPTED
    }
    
    // Handle scheduled sequences  
    for (auto metadata : output->seq_schedule_metadata_list) {
        OnSeqScheduled(metadata);  // WAITING → RUNNING
    }
}
```
