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
#include "commons/StdCommon.h"
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Forward declaration
class Tokenizer;
//==============================================================================
/**
 * @class DecodeStream
 * @brief Manages incremental decoding state for a token sequence
 *
 * This class encapsulates the state needed for incremental decoding,
 * tracking which tokens have been processed and providing clean APIs
 * for getting newly decoded text.
 */
class DecodeStream {
 public:
  /**
   * @brief Construct a DecodeStream for incremental decoding
   */
  DecodeStream() = default;

  /**
   * @brief Decode new tokens that have been added to the sequence
   *
   * @param tokenizer The tokenizer to use for decoding
   * @param token_ids The complete token sequence (shared pointer)
   */
  void DecodeIncremental(std::shared_ptr<Tokenizer> tokenizer,
                         const TokenIdsPtr& token_ids);

  /**
   * @brief Get the current accumulated output text
   *
   * @return The complete decoded text so far
   */
  [[nodiscard]] const std::string& GetOutputText() const {
    return output_text_;
  }

  /**
   * @brief Reset the decode stream state
   */
  void Reset();

 private:
  std::string output_text_;
  std::size_t prefix_offset_ = 0;
  std::size_t read_offset_ = 0;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
