# Core Abstractions

## Design Pattern Philosophy

Vajra's architecture is built upon a set of core abstractions that provide consistency, extensibility, and performance across the distributed system. These abstractions embody key design patterns from distributed systems and high-performance computing.

### Interface-Driven Design

All major components implement well-defined interfaces that separate specification from implementation:

```cpp
// Base interface for schedulers
class BaseScheduler {
public:
    virtual std::pair<SchedulerOutputPtr, MutableSequences> Schedule() = 0;
    virtual void OnStepCompleted(const MutableSequences& seqs, TimeS execution_time) = 0;
    virtual ~BaseScheduler() = default;
};
```

This pattern enables:
- **Pluggable implementations**: Easy swapping of scheduling algorithms
- **Testing isolation**: Mock implementations for unit testing
- **Runtime polymorphism**: Dynamic algorithm selection based on workload

### Template-Based Composition

Generic programming patterns provide type safety and performance:

```cpp
// Generic priority queue for different sequence types
template <typename SequenceType, typename ComparatorType>
class ConcurrentPriorityQueue {
    boost::concurrent::sync_priority_queue<
        SequenceType, 
        std::vector<SequenceType>, 
        ComparatorType> queue_;
};
```

Benefits include:
- **Zero-cost abstractions**: Template instantiation eliminates runtime overhead
- **Type safety**: Compile-time verification of interface compatibility
- **Code reuse**: Generic implementations across different sequence types

## Fundamental Abstractions

### Controller Pattern

All system controllers implement the AbstractController pattern:

```cpp
template <typename ConfigType>
class AbstractController : public NonCopyableNonMovable {
protected:
    // Configuration established at construction
    std::shared_ptr<const ConfigType> config_;
    
    // Thread-safe queues for asynchronous communication
    Queue<InputMessageType> input_queue_;
    Queue<OutputMessageType> output_queue_;
};
```

**Pattern Benefits:**

1. **Consistent Lifecycle**: Uniform start/stop semantics across controllers
2. **Thread Safety**: Queue-based communication eliminates shared state races
3. **Resource Management**: RAII principles for thread and resource cleanup

## Scheduling Abstractions

### Scheduler Hierarchy

The scheduling system implements a three-level hierarchy with consistent interfaces:

```cpp
// Level 1: Request prioritization
class BaseRequestPrioritizer {
    virtual MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
        MutableSequencePtr seq) = 0;
};

// Level 2: Inter-replica scheduling
class BaseReplicasetScheduler {
    virtual void Schedule(MutableBaseSequenceWithPriorityPtr seq) = 0;
    virtual SequencePriorityQueuePtr GetReplicaQueue(ReplicaId replica_id) const = 0;
};

// Level 3: Intra-replica scheduling  
class BaseReplicaScheduler {
    virtual std::pair<SchedulerOutputPtr, MutableSequences> Schedule() = 0;
    virtual void OnStepCompleted(/* args */) = 0;
};
```

Each level encapsulates specific concerns:
- **Prioritizer**: Sequence ordering and preemption decisions
- **Replicaset**: Load distribution across replicas
- **Replica**: Batch formation and memory allocation

## Communication Abstractions

### Process Group Wrapper

Distributed communication is abstracted through a process group interface:

```cpp
class ProcessGroupWrapper {
public:
    // Collective operations
    void AllReduce(torch::Tensor& tensor);
    void AllGather(const torch::Tensor& input, torch::Tensor& output);
    void ReduceScatter(const torch::Tensor& input, torch::Tensor& output);
    
    // Point-to-point operations  
    void Send(const torch::Tensor& tensor, int dest_rank);
    torch::Tensor Recv(const std::vector<int64_t>& shape, int src_rank);
    
    // Process group properties
    int GetRank() const { return rank_; }
    int GetSize() const { return size_; }
    
private:
    c10::intrusive_ptr<c10d::ProcessGroup> process_group_;
    int rank_;
    int size_;
};
```

**Abstraction Benefits:**

1. **Backend Independence**: Same interface for NCCL, MPI, or custom backends
2. **Error Handling**: Unified error handling across communication operations
3. **Performance Optimization**: Backend-specific optimizations hidden from users

### ZMQ Integration

Asynchronous messaging uses a ZMQ wrapper:

```cpp
template <typename MessageType>
class ZmqHelper {
public:
    static void Send(zmq::socket_t& socket, const MessageType& message) {
        zmq::multipart_t multipart;
        SerializeToMultipart(multipart, message);
        multipart.send(socket, zmq::send_flags::none);
    }
    
    static MessageType Recv(zmq::socket_t& socket) {
        zmq::multipart_t multipart;
        auto result = multipart.recv(socket);
        
        MessageType message;
        DeserializeFromMultipart(multipart, message);
        return message;
    }
};
```

This provides:
- **Type Safety**: Template-based serialization prevents type errors
- **Error Handling**: Unified error handling for network operations
- **Performance**: Zero-copy serialization where possible
