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
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Metadata for sequence execution in the inference engine.
 *
 * SequenceMetadata contains all the information needed to execute a sequence
 * during model inference, including token counts, memory block mappings, and
 * KV cache management parameters. This struct is used to pass sequence
 * information between the scheduler and the model execution layers.
 *
 * The metadata tracks both query (Q) and key-value (KV) token counts separately
 * to support advanced attention mechanisms and KV cache sharing across
 * sequences.
 *
 * @note This struct is immutable after construction to ensure thread safety.
 */
struct SequenceMetadata final {
  /**
   * @brief Constructs sequence metadata for execution.
   *
   * @param schedule_id_param Unique ID assigned by the scheduler
   * @param seq_id_param Original sequence identifier
   * @param num_q_tokens_param Number of query tokens to process
   * @param num_kv_tokens_param Number of key-value tokens available
   * @param block_table_param Physical block IDs for KV cache storage
   * @param kvp_group_ids_param KV parallel group IDs for distributed execution
   * @param save_kv_cache_param Whether to save computed KV values to cache
   */
  SequenceMetadata(ScheduleId schedule_id_param /*[in]*/,
                   const SeqId seq_id_param /*[in]*/,
                   std::size_t num_q_tokens_param /*[in]*/,
                   std::size_t num_kv_tokens_param /*[in]*/,
                   const BlockTable& block_table_param /*[in]*/,
                   const KvpGroupIds& kvp_group_ids_param /*[in]*/,
                   bool save_kv_cache_param /*[in]*/)
      : schedule_id(schedule_id_param),
        seq_id(seq_id_param),
        num_q_tokens(num_q_tokens_param),
        num_kv_tokens(num_kv_tokens_param),
        block_table(block_table_param),
        kvp_group_ids(kvp_group_ids_param),
        save_kv_cache(save_kv_cache_param),
        is_kvp_request(kvp_group_ids_param.size() > 1) {}

  std::string ToString() const {
    return std::format(
        "SequenceMetadata("
        "ScheduleId: {}, "
        "SeqId: {}, "
        "NumQTokens: {}, "
        "NumKvTokens: {}, "
        "KvpGroupIds: [{}], "
        "SaveKvCache: {}, "
        "IsKvpRequest: {})",
        schedule_id, seq_id, num_q_tokens, num_kv_tokens,
        JoinStrings(kvp_group_ids, ", "), save_kv_cache, is_kvp_request);
  }

  const ScheduleId schedule_id;     ///< Unique scheduling ID for this execution
  const SeqId seq_id;               ///< Original sequence identifier
  const std::size_t num_q_tokens;   ///< Number of query tokens to process
  const std::size_t num_kv_tokens;  ///< Number of key-value tokens in cache
  const BlockTable block_table;     ///< Physical block IDs for KV cache
  const KvpGroupIds kvp_group_ids;  ///< KV parallel group assignments
  const bool save_kv_cache;         ///< Whether to save KV values to cache
  const bool is_kvp_request;  ///< Whether using KV parallelism (auto-computed)
};
//==============================================================================
using SequenceMetadataPtr = std::shared_ptr<const SequenceMetadata>;
using SequenceMetadataVector = std::vector<SequenceMetadataPtr>;
//==============================================================================
}  // namespace vajra
//==============================================================================
