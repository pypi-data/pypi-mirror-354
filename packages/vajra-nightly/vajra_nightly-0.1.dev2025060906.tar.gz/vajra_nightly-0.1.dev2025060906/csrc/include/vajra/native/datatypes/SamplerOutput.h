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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/StringUtils.h"
#include "native/core/Types.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Output from the token sampling stage of generation.
 *
 * SamplerOutput represents the tokens sampled for a single sequence during
 * one generation step. It contains the sampled token IDs along with sequence
 * identification information needed for routing the output back to the
 * appropriate sequence.
 *
 * This class is used internally by the engine to pass sampling results between
 * the model execution and sequence management layers.
 */
class SamplerOutput {
 public:
  /**
   * @brief Constructs a sampler output.
   *
   * @param schedule_id Scheduling ID assigned to this sequence
   * @param seq_id Original sequence identifier
   * @param output_tokens Sampled token IDs for this step
   */
  SamplerOutput(ScheduleId schedule_id /*[in]*/, SeqId seq_id /*[in]*/,
                std::vector<TokenId> output_tokens /*[in]*/)
      : schedule_id_(schedule_id),
        seq_id_(seq_id),
        output_tokens_(output_tokens) {}

  inline ScheduleId GetScheduleId() const { return schedule_id_; }
  inline const SeqId& GetSeqId() const { return seq_id_; }
  inline std::string GetSeqIdCopy() const { return seq_id_; }
  inline const std::vector<TokenId>& GetOutputTokens() const {
    return output_tokens_;
  }
  inline std::vector<TokenId> GetOutputTokensCopy() const {
    return output_tokens_;
  }

  std::string ToString() const {
    return std::format(
        "SamplerOutput("
        "ScheduleId: {},"
        "SeqId: {},"
        "OutputTokens: {})",
        schedule_id_, seq_id_, JoinStrings(output_tokens_, ", "));
  }

 private:
  ScheduleId schedule_id_;              ///< Scheduling ID for sequence tracking
  SeqId seq_id_;                        ///< Original sequence identifier
  std::vector<TokenId> output_tokens_;  ///< Sampled tokens for this step
};
//==============================================================================
using SamplerOutputPtr = std::shared_ptr<SamplerOutput>;
using SamplerOutputs = std::vector<std::optional<SamplerOutputPtr>>;
using ValidSamplerOutputs = std::vector<SamplerOutputPtr>;
//==============================================================================
}  // namespace vajra
//==============================================================================
