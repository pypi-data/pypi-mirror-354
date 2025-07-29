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
#include "commons/BoostCommon.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/core/Types.h"
#include "native/datatypes/DecodeStream.h"
#include "native/datatypes/LogicalTokenBlock.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/SequenceState.h"
#include "native/datatypes/TokenRangeTracker.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief UserSequenceParams is a struct that contains the parameters for a user
 * sequence.
 */
struct UserSequenceParams final {
  UserSequenceParams(const SeqId seq_id_param, const std::string prompt_param,
                     const TokenIdsPtr prompt_token_ids_param,
                     const TimeS arrival_time_param,
                     const SamplingParams sampling_params_param)
      : seq_id(seq_id_param),
        prompt(prompt_param),
        prompt_token_ids(prompt_token_ids_param),
        arrival_time(arrival_time_param),
        sampling_params(sampling_params_param) {
    ASSERT_VALID_POINTER_ARGUMENT(prompt_token_ids);
  }

  /// @brief Convert to string representation
  /// @return String representation of the UserSequenceParams
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "UserSequenceParams(seq_id={}, prompt_len={}, arrival_time={}, "
        "sampling_params={})",
        seq_id, prompt_token_ids ? prompt_token_ids->size() : 0, arrival_time,
        sampling_params.ToString());
  }

  const SeqId seq_id;
  const std::string prompt;
  const TokenIdsPtr prompt_token_ids;
  const TimeS arrival_time;
  const SamplingParams sampling_params;
};
//==============================================================================
/**
 * @brief SequenceParams is a struct that contains the parameters for a
 * sequence.
 */
struct SequenceParams final {
  SequenceParams(const SeqId seq_id_param, const std::string prompt_param,
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
        sampling_params(sampling_params_param) {
    ASSERT_VALID_POINTER_ARGUMENT(prompt_token_ids);
  }

  /// @brief Convert to string representation
  /// @return String representation of the SequenceParams
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "SequenceParams(seq_id={}, prompt_len={}, block_size={}, "
        "eos_token_id={}, arrival_time={}, sampling_params={})",
        seq_id, prompt_token_ids ? prompt_token_ids->size() : 0, block_size,
        eos_token_id, arrival_time, sampling_params.ToString());
  }

  const SeqId seq_id;
  const std::string prompt;
  const TokenIdsPtr prompt_token_ids;
  const std::size_t block_size;
  const TokenId eos_token_id;
  const TimeS arrival_time;
  const SamplingParams sampling_params;
};
//==============================================================================
/**
 * @brief Sequence is a class that represents a sequence of tokens.
 */
class Sequence {
 public:
  Sequence(const SeqId seq_id_param, const std::string prompt_param,
           const TokenIdsPtr prompt_token_ids_param,
           const std::size_t block_size_param, const TokenId eos_token_id_param,
           const TimeS arrival_time_param,
           const SamplingParams sampling_params_param);

  explicit Sequence(const SequenceParams& params)
      : Sequence(params.seq_id, params.prompt, params.prompt_token_ids,
                 params.block_size, params.eos_token_id, params.arrival_time,
                 params.sampling_params) {}

  /**
   * @brief Gets the status of the sequence
   *
   * @return The status of the sequence
   */
  inline SequenceStatus GetStatus() const { return state_.GetStatus(); }

  /**
   * @brief Gets the prompt token IDs
   *
   * @return The prompt token IDs
   */
  inline TokenIdsPtr GetPromptTokenIds() const { return prompt_token_ids_; }

  /**
   * @brief Gets the output token IDs
   *
   * @return The output token IDs
   */
  inline TokenIdsPtr GetOutputTokenIds() const { return output_token_ids_; }

  /**
   * @brief Gets the logical token blocks
   *
   * @return The logical token blocks
   */
  inline const std::vector<std::shared_ptr<vajra::LogicalTokenBlock>>&
  GetLogicalTokenBlocks() const {
    return logical_token_blocks_;
  }

  /**
   * @brief Gets whether the prompt processing is finished
   *
   * @return Whether the prompt processing is finished
   */
  inline bool GetPromptProcessingFinished() const {
    return prompt_processing_finished_;
  }

  /**
   * @brief Gets whether the prompt stage processing is finished
   *
   * @return Whether the prompt stage processing is finished
   */
  inline bool GetPromptStageProcessingFinished() const {
    return prompt_stage_processing_finished_;
  }

  /**
   * @brief Gets the state of the sequence
   *
   * @return The state of the sequence
   */
  inline const SequenceState& GetState() const { return state_; }

  std::size_t GetNumProcessableTokens() const {
    auto next_unprocessed_range =
        token_range_tracker_.GetNextUnprocessedRange();
    return next_unprocessed_range.end - next_unprocessed_range.start;
  }

  /**
   * @brief Gets the length of the sequence
   *
   * @return The length of the sequence
   */
  inline std::size_t Length() const {
    return output_token_ids_->size() + prompt_token_ids_->size();
  }

  /**
   * @brief Gets the length of the prompt
   *
   * @return The length of the prompt
   */
  inline std::size_t GetPromptLength() const {
    return prompt_token_ids_->size();
  }

  /**
   * @brief Gets the length of the output
   *
   * @return The length of the output
   */
  inline std::size_t GetOutputLength() const {
    return output_token_ids_->size();
  }

  /**
   * @brief Gets the number of prompt tokens processed
   *
   * @return The number of prompt tokens processed
   */
  inline std::size_t GetNumPromptTokensProcessed() const {
    return std::min(GetPromptLength(), GetNumTokensProcessed());
  }

  /**
   * @brief Gets the number of prompt tokens stage processed
   *
   * @return The number of prompt tokens stage processed
   */
  inline std::size_t GetNumPromptTokensStageProcessed() const {
    return std::min(GetPromptLength(), GetNumTokensStageProcessed());
  }

  /**
   * @brief Gets the number of tokens processed
   *
   * @return The number of tokens processed
   */
  inline std::size_t GetNumTokensProcessed() const {
    return token_range_tracker_.GetProcessedPrefixLength();
  }

  /**
   * @brief Gets the number of tokens stage processed
   *
   * @return The number of tokens stage processed
   */
  inline std::size_t GetNumTokensStageProcessed() const {
    return token_range_tracker_.GetStageProcessedPrefixLength();
  }

  /**
   * @brief Gets the last token ID
   *
   * @return The last token ID
   */
  inline std::size_t GetLastTokenId() const {
    return output_token_ids_->size() > 0 ? output_token_ids_->back()
                                         : prompt_token_ids_->back();
  }

  /**
   * @brief Gets the last N token IDs
   *
   * @param n The number of token IDs to get
   * @param truncate Whether to truncate the token IDs
   * @return The last N token IDs
   */
  std::vector<TokenId> GetLastNTokenIds(std::size_t n /*[in]*/,
                                        bool truncate = false) const;

  /**
   * @brief Checks if the sequence is finished
   *
   * @return Whether the sequence is finished
   */
  inline bool IsFinished() const {
    return sequence_status::IsFinished(state_.GetStatus());
  }

  /**
   * @brief Checks if the sequence is executing
   *
   * @return Whether the sequence is executing
   */
  inline bool IsExecuting() const {
    return sequence_status::IsExecuting(state_.GetStatus());
  }

  /**
   * @brief Checks if the sequence is waiting
   *
   * @return Whether the sequence is waiting
   */
  inline bool IsWaiting() const {
    return sequence_status::IsWaiting(state_.GetStatus());
  }

  /**
   * @brief Checks if the sequence is paused
   *
   * @return Whether the sequence is paused
   */
  inline bool IsPaused() const {
    return sequence_status::IsPaused(state_.GetStatus());
  }

  /**
   * @brief Checks if the sequence is running
   *
   * @return Whether the sequence is running
   */
  inline bool IsRunning() const {
    return sequence_status::IsRunning(state_.GetStatus());
  }

  /**
   * @brief Checks if the sequence is waiting preempted
   *
   * @return Whether the sequence is waiting preempted
   */
  inline bool IsWaitingPreempted() const {
    return sequence_status::IsWaitingPreempted(state_.GetStatus());
  }

  /**
   * @brief Gets the output text
   *
   * @return The output text
   */
  inline const std::string& GetOutputText() const {
    return decode_stream_->GetOutputText();
  }

  /**
   * @brief Get the decode stream for this sequence
   *
   * @return Shared pointer to the decode stream
   */
  std::shared_ptr<DecodeStream> GetDecodeStream() const {
    return decode_stream_;
  }

  /**
   * @brief Converts the sequence to a string
   *
   * @return The string representation of the sequence
   */
  std::string ToString() {
    return std::format(
        "Sequence(seq_id={}, "
        "status={}, "
        "num_blocks={}, "
        "num_prompt_tokens={}, "
        "num_output_tokens={}, "
        "prompt_processing_finished={}, "
        "num_prompt_tokens_processed={}, "
        "num_prompt_tokens_stage_processed={}, "
        "prompt_stage_processing_finished={})",
        seq_id, GetStatus(), logical_token_blocks_.size(), GetPromptLength(),
        GetOutputLength(), prompt_processing_finished_,
        GetNumPromptTokensProcessed(), GetNumPromptTokensStageProcessed(),
        prompt_stage_processing_finished_);
  }

  /**
   * @brief Gets the parameters of the sequence
   *
   * @return The parameters of the sequence
   */
  [[nodiscard]] SequenceParams GetParams() const {
    return SequenceParams(seq_id, prompt, prompt_token_ids_, block_size,
                          eos_token_id, arrival_time, sampling_params);
  }

  const SeqId seq_id;
  const std::string prompt;
  const std::size_t block_size;
  const TokenId eos_token_id;
  const TimeS arrival_time;
  const SamplingParams sampling_params;

 private:
  // Friend classes that are allowed to mutate sequences
  friend class BaseSequenceManager;
  friend class EngineSequenceManager;
  friend class WorkerSequenceManager;
  // Test helper class needs access for unit testing
  friend class TestSequenceManager;

  // Mutating methods - only accessible to sequence managers
  /**
   * @brief Sets the status of the sequence
   *
   * @param status The status to set
   */
  inline void SetStatus(SequenceStatus status /*[in]*/) {
    state_.SetStatus(status);
  }

  /**
   * @brief Updates the number of tokens processed
   *
   * @param num_tokens The number of tokens to update
   */
  void UpdateTokensProcessed(std::size_t num_tokens /*[in]*/);

  /**
   * @brief Updates the number of prompt tokens processed
   *
   * @param num_tokens The number of tokens to update
   */
  void UpdatePromptTokensProcessed(std::size_t num_tokens /*[in]*/);

  /**
   * @brief Updates the number of prompt tokens stage processed
   *
   * @param num_tokens The number of tokens to update
   */
  void UpdatePromptTokensStageProcessed(std::size_t num_tokens /*[in]*/);

  /**
   * @brief Appends a token ID to the sequence
   *
   * @param token_id The token ID to append
   */
  void AppendTokenId(TokenId token_id /*[in]*/);

  /**
   * @brief Resets the sequence
   */
  void Reset();

  /**
   * @brief Checks if the sequence should stop
   *
   * @param num_new_tokens The number of new tokens
   */
  void CheckStop(std::size_t num_new_tokens /*[in]*/);

  /**
   * @brief Appends a logical block to the sequence
   */
  void AppendLogicalBlock();

  /**
   * @brief Appends tokens to the blocks
   *
   * @param token_ids The token IDs to append
   */
  void AppendTokensToBlocks(const TokenIds& token_ids /*[in]*/);

  // Decode stream for incremental decoding
  std::shared_ptr<DecodeStream> decode_stream_ =
      std::make_shared<DecodeStream>();

  TokenIdsPtr prompt_token_ids_ =
      std::make_shared<TokenIds>(std::vector<TokenId>());
  TokenIdsPtr output_token_ids_ =
      std::make_shared<TokenIds>(std::vector<TokenId>());
  bool prompt_processing_finished_ = false;
  bool prompt_stage_processing_finished_ = false;

  std::vector<std::shared_ptr<vajra::LogicalTokenBlock>> logical_token_blocks_;
  SequenceState state_;

  TokenRangeTracker token_range_tracker_;
};
//==============================================================================
using SequencePtr = std::shared_ptr<const Sequence>;
using Sequences = std::vector<SequencePtr>;

using MutableSequencePtr = std::shared_ptr<Sequence>;
using MutableSequences = std::vector<MutableSequencePtr>;

using UserSequenceParamsPtr = std::shared_ptr<const UserSequenceParams>;
using MutableUserSequenceParamsPtr = std::shared_ptr<UserSequenceParams>;
//==============================================================================
inline const vajra::Sequences& AsConstSequences(
    const vajra::MutableSequences& seqs) {
  // reinterpret_cast is typically forbidden in this codebase
  // but we use it for fast conversion of MutableSequences to Sequences (as
  // const)
  return *reinterpret_cast<const vajra::Sequences*>(&seqs);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
