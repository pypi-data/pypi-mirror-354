# Vajra C++ Style Guide

## Introduction

This style guide outlines the coding conventions and best practices for writing C++ code within the Vajra project. It follows the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) with Vajra-specific modifications and leverages modern C++20/23 features extensively. All code should adhere to these guidelines to ensure consistency, readability, maintainability, and effective collaboration.

## Key Goals

- **Readability**: Code should be easy to understand and follow by any developer
- **Consistency**: Uniformity in style across the project reduces cognitive load and improves predictability
- **Maintainability**: Well-structured and clearly written code is easier to modify, debug, and extend over time
- **Collaboration**: Shared style guidelines facilitate seamless teamwork and code integration
- **Modern C++**: Embrace C++20/23 features for type safety, performance, and expressiveness

## File Organization

### Header File Structure

All header files must follow this exact structure:

```cpp
//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#pragma once
//==============================================================================
#include "vajra/commons/StdCommon.h"      // Standard C++ headers
#include "vajra/commons/TorchCommon.h"    // PyTorch integration (if needed)
#include "vajra/commons/BoostCommon.h"    // Boost utilities (if needed)
//==============================================================================
#include "vajra/commons/ClassTraits.h"
#include "vajra/commons/Logging.h"
#include "vajra/project_headers.h"
//==============================================================================
namespace vajra {
//==============================================================================

// Class declarations and implementations

//==============================================================================
}  // namespace vajra
//==============================================================================
```

### Common Header Files

Vajra uses centralized header files to ensure consistent imports and reduce compilation time:

**StdCommon.h** - All standard C++ headers:
- Containers: `<memory>`, `<vector>`, `<unordered_map>`, `<array>`
- Algorithms: `<algorithm>`, `<numeric>`, `<functional>`
- Concurrency: `<thread>`, `<mutex>`, `<atomic>`, `<future>`
- Utilities: `<optional>`, `<variant>`, `<string_view>`, `<format>`

**TorchCommon.h** - PyTorch integration:
- Core PyTorch: `<torch/all.h>`, `<torch/extension.h>`
- CUDA integration: `<torch/cuda.h>`, `<c10/cuda/CUDAGuard.h>`
- Distributed: `<torch/csrc/distributed/c10d/ProcessGroup.hpp>`

**BoostCommon.h** - Boost utilities:
- Concurrent queues: `boost::concurrent::sync_queue`, `boost::concurrent::sync_priority_queue`
- Type aliases: `Queue<T>`, `PriorityQueue<T>`

### Implementation File Structure

```cpp
//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#include "corresponding_header.h"
//==============================================================================
#include "vajra/commons/StdCommon.h"
#include "vajra/commons/TorchCommon.h"  // If needed
//==============================================================================
#include "other_project_headers.h"
//==============================================================================
namespace vajra {
//==============================================================================

// Implementation code

//==============================================================================
}  // namespace vajra
//==============================================================================
```

### Benefits of Common Headers

This approach provides:
- **Consistency**: Uniform header inclusion across all files
- **Compile Time**: Precompiled headers reduce build times significantly
- **Dependency Management**: Clear separation of external library dependencies
- **Maintenance**: Centralized management of library versions and compatibility

## Naming Conventions

### Classes, Structs, Types, and Enums
- **PascalCase**: `LogicalTokenBlock`, `SamplingParams`, `SequenceStatus`
- **Enum Classes**: Always use `enum class` with PascalCase values

```cpp
enum class SequenceStatus {
  Waiting,
  Running, 
  Finished,
  FinishedEOS,
  FinishedMaxTokens
};
```

### Functions and Methods
- **PascalCase**: `ToString()`, `GetStatus()`, `SetStatus()`, `Forward()`
- **Getters/Setters**: Prefix with "Get"/"Set"

```cpp
[[nodiscard]] std::string ToString() const;
[[nodiscard]] SequenceStatus GetStatus() const;
void SetStatus(SequenceStatus status /*[in]*/);
```

### Variables
- **snake_case**: `prompt_token_ids`, `arrival_time`, `hidden_states`
- **Member variables**: snake_case with trailing underscore: `state_`, `tokens_`
- **Boolean variables**: Use descriptive predicates: `is_finished_`, `has_value_`

```cpp
class Sequence {
private:
    SequenceStatus state_;
    TokenIdsPtr prompt_token_ids_;
    bool prompt_processing_finished_;
};
```

### Constants
- **PascalCase with k prefix**: `kSamplingEps`

```cpp
constexpr double kSamplingEps = 1e-5;
```

### Type Aliases
- **PascalCase** with descriptive suffixes:

```cpp
using SequencePtr = std::shared_ptr<const Sequence>;
using MutableSequencePtr = std::shared_ptr<Sequence>;
using Sequences = std::vector<SequencePtr>;
using MutableSequences = std::vector<MutableSequencePtr>;
using TokenIdsPtr = std::shared_ptr<TokenIds>;
```

## Class Design and Inheritance

### Base Class Traits

Use the standard Vajra class traits from `vajra/commons/ClassTraits.h`:

```cpp
//==============================================================================
#include "vajra/commons/StdCommon.h"
#include "vajra/commons/ClassTraits.h"
//==============================================================================

// For classes that should not be copied
class SequenceManager : public NonCopyable {
    // Implementation
};

// For classes that should not be moved or copied
class BaseModelRunner : public NonCopyableNonMovable {
    // Implementation  
};

// For utility classes with only static methods
class ModelUtils : public StaticClass {
public:
    static bool ValidateConfig(const ModelConfig& config);
};
```

### Constructor Patterns

- Use member initializer lists
- Validate all pointer parameters immediately
- Place each initialization on its own line for readability

```cpp
//==============================================================================
#include "vajra/commons/StdCommon.h"
#include "vajra/commons/Logging.h"
//==============================================================================

Sequence::Sequence(
    const std::string seq_id_param,
    const std::string prompt_param, 
    const TokenIdsPtr prompt_token_ids_param,
    const std::size_t block_size_param,
    const TokenId eos_token_id_param,
    const TimeS arrival_time_param,
    const SamplingParams sampling_params_param)
    : seq_id(seq_id_param),
      prompt(prompt_param),
      prompt_token_ids(prompt_token_ids_param),
      block_size(block_size_param),
      eos_token_id(eos_token_id_param),
      arrival_time(arrival_time_param),
      sampling_params(sampling_params_param),
      state_(SequenceStatus::Waiting),
      prompt_processing_finished_(false) {
  
  ASSERT_VALID_POINTER_ARGUMENT(prompt_token_ids);
  ASSERT_VALID_ARGUMENTS(block_size > 0, "Block size must be positive");
  ASSERT_VALID_ARGUMENTS(!prompt.empty(), "Prompt cannot be empty");
}
```

## Validation and Error Handling

### Assertion Macros

Always use Vajra validation macros from `vajra/commons/Logging.h`:

```cpp
// For null pointer validation
ASSERT_VALID_POINTER_ARGUMENT(ptr);

// For runtime conditions with formatted messages
ASSERT_VALID_RUNTIME(condition, "Failed because: {}", reason);

// For argument validation with formatted messages  
ASSERT_VALID_ARGUMENTS(value > 0, "Value {} must be positive", value);
```

### Error Throwing Macros

```cpp
// For runtime errors
THROW_RUNTIME_ERROR("Operation failed: {}", error_message);

// For invalid arguments
RAISE_INVALID_ARGUMENTS_ERROR("Invalid parameter: {}", param_name);
```

### Example Usage

```cpp
//==============================================================================
#include "vajra/commons/StdCommon.h"
#include "vajra/commons/Logging.h"
//==============================================================================

void ProcessSequence(const MutableSequencePtr& seq /*[in]*/) {
    ASSERT_VALID_POINTER_ARGUMENT(seq);
    ASSERT_VALID_RUNTIME(seq->IsRunning(), 
        "Sequence {} is not in running state", seq->seq_id);
    
    if (seq->GetOutputLength() > MAX_SEQUENCE_LENGTH) {
        RAISE_INVALID_ARGUMENTS_ERROR(
            "Sequence {} exceeds maximum length {}", 
            seq->seq_id, MAX_SEQUENCE_LENGTH);
    }
    
    // Process sequence...
}
```

## Logging

Use the structured logging macros from `vajra/commons/Logging.h`:

```cpp
LOG_DEBUG("Debug info: value = {}", value);
LOG_INFO("Processing {} sequences", num_sequences);
LOG_WARNING("Memory usage is high: {}MB", memory_mb);
LOG_ERROR("Failed to allocate memory for sequence {}", seq_id);
LOG_CRITICAL("System is in unrecoverable state");
```
Never use **std::cout**, always use the logging macros instead of direct output:

```cpp
// ❌ Don't do this
std::cout << "Processing sequence" << std::endl;

// ✅ Do this instead
LOG_INFO("Processing sequence {}", seq_id);
```

## Modern C++ Features

### Concepts

Use concepts for template constraints:

```cpp
template <typename T>
concept Printable = requires(const T& t) {
    { t.ToString() } -> std::convertible_to<std::string>;
};

template <Printable T>
void LogObject(const T& obj) {
    LOG_INFO("Object: {}", obj.ToString());
}
```

### std::format

Always use `std::format` for string formatting:

```cpp
std::string ToString() const {
    return std::format(
        "SamplingParams(temperature={}, top_p={}, top_k={}, "
        "ignore_eos={}, max_tokens={})",
        temperature, top_p, top_k, ignore_eos, max_tokens);
}
```

### [[nodiscard]] and const

Mark functions appropriately:

```cpp
class Sequence {
public:
    [[nodiscard]] std::string ToString() const;
    [[nodiscard]] std::size_t GetPromptLength() const;
    [[nodiscard]] bool IsFinished() const;
    
    // Non-const modifiers
    void SetStatus(SequenceStatus status /*[in]*/);
    void AppendTokenId(TokenId token_id /*[in]*/);
};
```

### Parameter Direction Annotations

Document all parameters with direction annotations:

```cpp
void UpdateSequenceState(
    const std::string& seq_id /*[in]*/,
    SequenceStatus new_status /*[in]*/,
    std::vector<TokenId>& output_tokens /*[out]*/,
    SequenceMetadata& metadata /*[inout]*/) {
    
    // Implementation
}
```

### Range-based for loops

Prefer range-based loops with auto:

```cpp
// ✅ Good
for (const auto& seq : sequences) {
    LOG_INFO("Processing sequence {}", seq->seq_id);
}

// ✅ Also good for modification
for (auto& seq : mutable_sequences) {
    seq->SetStatus(SequenceStatus::Running);
}
```

### Smart Pointers

Use smart pointers with descriptive type aliases:

```cpp
using ModelPtr = std::shared_ptr<BaseModel>;
using LayerPtr = std::shared_ptr<BaseLayer>;
using SequenceManagerPtr = std::unique_ptr<BaseSequenceManager>;

class ModelRunner {
private:
    ModelPtr model_;
    std::vector<LayerPtr> layers_;
    SequenceManagerPtr sequence_manager_;
    
public:
    ModelRunner(ModelPtr model /*[in]*/, 
               std::vector<LayerPtr> layers /*[in]*/)
        : model_(std::move(model)),
          layers_(std::move(layers)) {
        
        ASSERT_VALID_POINTER_ARGUMENT(model_);
        ASSERT_VALID_ARGUMENTS(!layers_.empty(), "No layers provided");
    }
};
```

## Memory Management

### RAII and Smart Pointers

- Use `std::shared_ptr` for shared ownership
- Use `std::unique_ptr` for exclusive ownership  
- Always validate pointer arguments in constructors
- Prefer move semantics for performance

```cpp
class CacheEngine {
private:
    std::unique_ptr<BlockSpaceManager> block_manager_;
    std::shared_ptr<TokenizerWrapper> tokenizer_;
    
public:
    CacheEngine(std::unique_ptr<BlockSpaceManager> block_manager,
               std::shared_ptr<TokenizerWrapper> tokenizer)
        : block_manager_(std::move(block_manager)),
          tokenizer_(std::move(tokenizer)) {
        
        ASSERT_VALID_POINTER_ARGUMENT(block_manager_);
        ASSERT_VALID_POINTER_ARGUMENT(tokenizer_);
    }
};
```

### Resource Management

Use RAII for all resources:

```cpp
class GPUMemoryPool {
private:
    void* gpu_memory_;
    std::size_t size_;
    
public:
    GPUMemoryPool(std::size_t size) : size_(size) {
        gpu_memory_ = allocateGPUMemory(size_);
        ASSERT_VALID_RUNTIME(gpu_memory_ != nullptr, 
            "Failed to allocate {}MB of GPU memory", size_ / 1024 / 1024);
    }
    
    ~GPUMemoryPool() {
        if (gpu_memory_) {
            freeGPUMemory(gpu_memory_);
        }
    }
    
    // Delete copy, allow move
    GPUMemoryPool(const GPUMemoryPool&) = delete;
    GPUMemoryPool& operator=(const GPUMemoryPool&) = delete;
    GPUMemoryPool(GPUMemoryPool&& other) noexcept 
        : gpu_memory_(other.gpu_memory_), size_(other.size_) {
        other.gpu_memory_ = nullptr;
        other.size_ = 0;
    }
};
```

## Threading and Concurrency

### Thread Safety

Document thread safety requirements:

```cpp
class SequenceManager {
private:
    mutable std::recursive_mutex mutex_;  // Allows recursive locking
    std::unordered_map<std::string, MutableSequencePtr> seq_map_;
    
public:
    // Thread-safe: Uses internal locking
    void AddSequence(MutableSequencePtr seq /*[in]*/) {
        std::lock_guard<std::recursive_mutex> lock(mutex_);
        ASSERT_VALID_POINTER_ARGUMENT(seq);
        seq_map_[seq->seq_id] = std::move(seq);
    }
    
    // Thread-safe: Read-only access with lock
    [[nodiscard]] SequencePtr GetSequence(const std::string& seq_id /*[in]*/) const {
        std::lock_guard<std::recursive_mutex> lock(mutex_);
        auto it = seq_map_.find(seq_id);
        return (it != seq_map_.end()) ? it->second : nullptr;
    }
};
```

### Atomic Operations

Use atomics for simple shared state:

```cpp
class MetricsCollector {
private:
    std::atomic<std::uint64_t> request_count_{0};
    std::atomic<std::uint64_t> tokens_processed_{0};
    
public:
    void IncrementRequests() noexcept {
        request_count_.fetch_add(1, std::memory_order_relaxed);
    }
    
    [[nodiscard]] std::uint64_t GetRequestCount() const noexcept {
        return request_count_.load(std::memory_order_relaxed);
    }
};
```

## Performance Guidelines

### Avoid Unnecessary Copies

```cpp
// ✅ Pass large objects by const reference
void ProcessLargeObject(const LargeObject& obj /*[in]*/) {
    // Implementation
}

// ✅ Return by value for move-constructible types
[[nodiscard]] std::vector<TokenId> GenerateTokens() {
    std::vector<TokenId> tokens;
    // Fill tokens...
    return tokens;  // RVO/move
}

// ✅ Use string_view for read-only string parameters
void LogMessage(std::string_view message /*[in]*/) {
    LOG_INFO("{}", message);
}
```

### Prefer Stack Allocation

```cpp
// ✅ Stack allocation when size is known
std::array<float, 1024> buffer;

// ✅ Heap allocation only when necessary
auto large_buffer = std::make_unique<std::array<float, 1024*1024>>();
```

### Move Semantics

```cpp
class ResourceHolder {
private:
    std::vector<ExpensiveResource> resources_;
    
public:
    // Accept by value and move
    void SetResources(std::vector<ExpensiveResource> resources /*[in]*/) {
        resources_ = std::move(resources);
    }
    
    // Return by value for move
    [[nodiscard]] std::vector<ExpensiveResource> ReleaseResources() {
        return std::move(resources_);
    }
};
```

## Testing and Documentation

### Unit Test Naming

```cpp
class SequenceTest : public ::testing::Test {
protected:
    void SetUp() override;
    void TearDown() override;
};

TEST_F(SequenceTest, Constructor_ValidParameters_CreatesSequence) {
    // Test implementation
}

TEST_F(SequenceTest, AppendToken_ValidToken_UpdatesLength) {
    // Test implementation  
}

TEST_F(SequenceTest, SetStatus_InvalidTransition_ThrowsException) {
    // Test implementation
}
```

### Documentation Comments

Use clear, concise documentation:

```cpp
/// @brief Manages the lifecycle and state of inference sequences
/// 
/// The SequenceManager is responsible for tracking sequence state transitions,
/// managing memory allocation for sequences, and coordinating between the
/// scheduler and execution engines. It is thread-safe and supports concurrent
/// access from multiple threads.
///
/// @note All public methods are thread-safe unless otherwise noted
class SequenceManager : public NonCopyable {
public:
    /// @brief Adds a new sequence to be managed
    /// @param seq The sequence to add (must not be null)
    /// @throws std::invalid_argument if seq is null
    /// @throws std::runtime_error if sequence ID already exists
    void AddSequence(MutableSequencePtr seq /*[in]*/);
    
    /// @brief Retrieves a sequence by ID
    /// @param seq_id The unique sequence identifier
    /// @return Pointer to sequence, or nullptr if not found
    /// @note Thread-safe for concurrent access
    [[nodiscard]] SequencePtr GetSequence(const std::string& seq_id /*[in]*/) const;
};
```

## Common Patterns

### Factory Functions

```cpp
class ModelFactory {
public:
    [[nodiscard]] static std::unique_ptr<BaseModel> CreateModel(
        const ModelConfig& config /*[in]*/) {
        
        ASSERT_VALID_ARGUMENTS(!config.model_name.empty(), 
            "Model name cannot be empty");
        
        if (config.model_type == ModelType::LLAMA) {
            return std::make_unique<LlamaModel>(config);
        } else if (config.model_type == ModelType::MISTRAL) {
            return std::make_unique<MistralModel>(config);
        }
        
        THROW_RUNTIME_ERROR("Unsupported model type: {}", 
            static_cast<int>(config.model_type));
    }
};
```
