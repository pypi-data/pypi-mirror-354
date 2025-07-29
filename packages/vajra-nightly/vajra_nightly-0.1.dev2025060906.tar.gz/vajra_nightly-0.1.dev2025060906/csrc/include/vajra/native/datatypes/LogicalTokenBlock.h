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
#include "commons/Constants.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/StringUtils.h"
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief LogicalTokenBlock is a class that represents a logical token block.
 */
struct LogicalTokenBlock {
  LogicalTokenBlock(BlockNumber block_number_param /*[in]*/,
                    std::size_t block_size_param /*[in]*/,
                    TokenIds token_ids_param /*[in]*/,
                    std::size_t num_tokens_param /*[in]*/)
      : block_number(block_number_param),
        block_size(block_size_param),
        token_ids_(token_ids_param),
        num_tokens_(num_tokens_param) {
    token_ids_.resize(block_size_param);
  }

  LogicalTokenBlock(BlockNumber block_number_param /*[in]*/,
                    std::size_t block_size_param /*[in]*/)
      : LogicalTokenBlock(block_number_param, block_size_param, {}, 0) {}

  /**
   * @brief Checks if the block is empty
   *
   * @return Whether the block is empty
   */
  inline bool IsEmpty() const { return num_tokens_ == 0; }

  /**
   * @brief Gets the number of empty slots in the block
   *
   * @return The number of empty slots in the block
   */
  inline std::size_t NumEmptySlots() const { return block_size - num_tokens_; }

  /**
   * @brief Checks if the block is full
   *
   * @return Whether the block is full
   */
  inline bool IsFull() const { return num_tokens_ == block_size; }

  /**
   * @brief Appends tokens to the block
   *
   * @param token_ids The token IDs to append
   */
  void AppendTokens(const TokenIds& token_ids /*[in]*/);

  /**
   * @brief Gets the last token ID in the block
   *
   * @return The last token ID in the block
   */
  inline std::size_t GetLastTokenId() const {
    ASSERT_VALID_RUNTIME(num_tokens_ > 0,
                         "Block is empty, no tokens available");
    return token_ids_[num_tokens_ - 1];
  }

  /**
   * @brief Gets the token IDs in the block
   *
   * @return The token IDs in the block
   */
  inline const TokenIds& GetTokenIds() const { return token_ids_; }

  /**
   * @brief Gets a copy of the token IDs in the block
   *
   * @return A copy of the token IDs in the block
   */
  inline const TokenIds GetTokenIdsCopy() const { return token_ids_; }

  /**
   * @brief Gets the number of tokens in the block
   *
   * @return The number of tokens in the block
   */
  inline std::size_t GetNumTokens() const { return num_tokens_; }

  /**
   * @brief Convert to string representation
   *
   * @return String representation of the LogicalTokenBlock
   */
  [[nodiscard]] std::string ToString() const {
    // Show first few token IDs if available
    std::string token_preview = "[]";
    if (num_tokens_ > 0) {
      std::size_t preview_count = std::min(num_tokens_, kMaxTokenPreviewCount);
      TokenIds preview_tokens(token_ids_.begin(),
                              token_ids_.begin() + preview_count);
      token_preview = std::format("[{}{}]", JoinStrings(preview_tokens, ", "),
                                  num_tokens_ > kMaxTokenPreviewCount
                                      ? std::format(", {}", kEllipsis)
                                      : "");
    }
    return std::format(
        "LogicalTokenBlock(block_number={}, block_size={}, num_tokens={}, "
        "tokens={})",
        block_number, block_size, num_tokens_, token_preview);
  }

  const BlockNumber block_number;
  const std::size_t block_size;

 private:
  TokenIds token_ids_;
  std::size_t num_tokens_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
