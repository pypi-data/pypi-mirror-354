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
#include "native/core/Types.h"
#include "native/core/block_space_manager/BlockSpaceManager.h"
#include "native/core/sequence_manager/BaseSequenceManager.h"
#include "native/datatypes/SequenceMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
//==============================================================================
/**
 * @brief KV cache information for a sequence
 */
struct KVCacheInfo {
  std::size_t kv_cache_length;
  bool should_save_kv_cache;

  KVCacheInfo(std::size_t length, bool save)
      : kv_cache_length(length), should_save_kv_cache(save) {}
};
//==============================================================================
class WorkerSequenceManager : public BaseSequenceManager {
 public:
  explicit WorkerSequenceManager(std::size_t block_size,
                                 std::size_t num_gpu_blocks,
                                 std::size_t max_model_len,
                                 std::size_t max_num_tokens_per_kvp_group,
                                 Rank rank, KvpGroupId kvp_group_id,
                                 std::size_t kvp_parallel_world_size,
                                 bool enable_sequence_pipeline_parallel);

  void OnStageCompleted(SchedulerOutputPtr scheduler_output) override;

  void OnStepCompleted(const std::vector<SequenceScheduleMetadataPtr>&
                           seq_schedule_metadata_list,
                       const ValidSamplerOutputs& sampler_outputs) override;

  [[nodiscard]] OnScheduleResult OnSchedule(
      SchedulerOutputPtr scheduler_output) override;

 protected:
  void FreeSeq(const SeqId& seq_id) override;

  void PreemptSeq(const SeqId& seq_id) override;

  void OnSeqScheduled(SequenceScheduleMetadataPtr seq_sched_metadata) override;

  [[nodiscard]] BlockTable GetBlockTable(SequencePtr seq) const override;

 private:
  KVCacheInfo ComputeKVCacheInfo(SequencePtr seq,
                                 const KvpGroupIds& kvp_group_ids);

  Rank rank_;
  KvpGroupId kvp_group_id_;
  std::size_t max_num_tokens_per_kvp_group_;
  BlockSpaceManager block_manager_;
};
//==============================================================================
using WorkerSequenceManagerPtr = std::shared_ptr<WorkerSequenceManager>;
//==============================================================================
}  // namespace vajra
//==============================================================================
