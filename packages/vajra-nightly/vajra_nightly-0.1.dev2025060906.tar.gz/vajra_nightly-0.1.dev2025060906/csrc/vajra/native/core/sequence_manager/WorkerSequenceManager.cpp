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
#include "native/core/sequence_manager/WorkerSequenceManager.h"
//==============================================================================
#include "native/core/Types.h"
#include "native/model_executor/layers/attention/SequenceArrangement.h"
//==============================================================================
namespace vajra {
//==============================================================================
WorkerSequenceManager::WorkerSequenceManager(
    std::size_t block_size, std::size_t num_gpu_blocks,
    std::size_t max_model_len, std::size_t max_num_tokens_per_kvp_group,
    Rank rank, KvpGroupId kvp_group_id, std::size_t kvp_parallel_world_size,
    bool enable_sequence_pipeline_parallel)
    : BaseSequenceManager(enable_sequence_pipeline_parallel),
      rank_(rank),
      kvp_group_id_(kvp_group_id),
      block_manager_(
          BlockSpaceManager(block_size, num_gpu_blocks, max_model_len)) {
  if (kvp_parallel_world_size == 1) {
    max_num_tokens_per_kvp_group_ = max_model_len;
  } else {
    max_num_tokens_per_kvp_group_ = max_num_tokens_per_kvp_group;
  }
}
//==============================================================================
void WorkerSequenceManager::OnStageCompleted(
    SchedulerOutputPtr scheduler_output) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  std::lock_guard<std::recursive_mutex> lk(mutex_);

  if (!enable_sequence_pipeline_parallel_) return;

  for (auto metadata : scheduler_output->seq_schedule_metadata_list) {
    auto seq = seq_map_[metadata->seq_id];
    ASSERT_VALID_RUNTIME(!seq->IsFinished(), "seq {} has finished!",
                         seq->seq_id);

    if (seq->IsWaitingPreempted()) continue;

    if (seq->GetPromptStageProcessingFinished()) continue;

    seq->UpdatePromptTokensStageProcessed(metadata->num_q_tokens);

    bool kvp_group_id_found =
        std::find(metadata->kvp_group_ids.begin(),
                  metadata->kvp_group_ids.end(),
                  kvp_group_id_) != metadata->kvp_group_ids.end();
    if (kvp_group_id_found && !seq->GetPromptStageProcessingFinished())
      PauseSeq(metadata->seq_id);
  }
}
//==============================================================================
void WorkerSequenceManager::OnStepCompleted(
    const std::vector<SequenceScheduleMetadataPtr>& seq_schedule_metadata_list,
    const ValidSamplerOutputs& sampler_outputs) {
  std::lock_guard<std::recursive_mutex> lk(mutex_);

  std::vector<SequenceScheduleMetadataPtr> filtered_seq_metadata;
  ValidSamplerOutputs sorted_sampler_outputs;

  std::unordered_map<SeqId, SamplerOutputPtr> sampler_outputs_map;
  for (auto s : sampler_outputs) {
    sampler_outputs_map[s->GetSeqId()] = s;
  }

  for (auto metadata : seq_schedule_metadata_list) {
    ASSERT_VALID_POINTER_ARGUMENT(metadata);

    auto seq = seq_map_[metadata->seq_id];
    ASSERT_VALID_RUNTIME(!seq->IsFinished(), "seq {} has finished!",
                         seq->seq_id);

    bool kvp_group_id_found =
        std::find(metadata->kvp_group_ids.begin(),
                  metadata->kvp_group_ids.end(),
                  kvp_group_id_) != metadata->kvp_group_ids.end();
    if (!kvp_group_id_found) {
      if (seq->GetPromptProcessingFinished()) {
        // do nothing
        // if prompt processing has finished, all KVP workers are active and
        // should be in kvp_group_ids. so if this worker is not in the active
        // KVP group, the sequence will never use this worker.
      } else {
        if (!enable_sequence_pipeline_parallel_) {
          seq->UpdatePromptTokensStageProcessed(metadata->num_q_tokens);
        }
        seq->UpdatePromptTokensProcessed(metadata->num_q_tokens);
      }
      continue;
    }

    filtered_seq_metadata.emplace_back(metadata);
    sorted_sampler_outputs.emplace_back(sampler_outputs_map[seq->seq_id]);
  }

  BaseSequenceManager::OnStepCompleted(filtered_seq_metadata,
                                       sorted_sampler_outputs);
}
//==============================================================================
OnScheduleResult WorkerSequenceManager::OnSchedule(
    SchedulerOutputPtr scheduler_output) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  std::lock_guard<std::recursive_mutex> lk(mutex_);

  MutableSequences ignored_seqs;
  for (auto seq_id : scheduler_output->ignored_seq_ids) {
    ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                         "sequence {} not found", seq_id);
    auto seq = seq_map_[seq_id];
    seq->SetStatus(SequenceStatus::FinishedIgnored);
    ignored_seqs.emplace_back(seq);
    FreeSeq(seq_id);
  }

  for (auto seq_id : scheduler_output->preempted_seq_ids) {
    PreemptSeq(seq_id);
  }

  SequenceMetadataVector seq_metadata_list;
  for (auto metadata : scheduler_output->seq_schedule_metadata_list) {
    ASSERT_VALID_RUNTIME(seq_map_.find(metadata->seq_id) != seq_map_.end(),
                         "seq_id {} not found in seq_map for rank {}",
                         metadata->seq_id, rank_);

    bool kvp_group_id_found =
        std::find(metadata->kvp_group_ids.begin(),
                  metadata->kvp_group_ids.end(),
                  kvp_group_id_) != metadata->kvp_group_ids.end();
    if (!kvp_group_id_found) continue;

    auto seq = seq_map_.at(metadata->seq_id);
    OnSeqScheduled(metadata);

    const auto kv_cache_info = ComputeKVCacheInfo(seq, metadata->kvp_group_ids);
    if (kv_cache_info.should_save_kv_cache) {
      ASSERT_VALID_RUNTIME(
          (kv_cache_info.kv_cache_length + metadata->num_q_tokens <=
           max_num_tokens_per_kvp_group_) ||
              (kvp_group_id_ == metadata->kvp_group_ids.back()),
          "Sequence KV cache length exceeds KVP group limit "
          "seq_id: {}, kv_cache_len: {}, num_q_tokens: {}, "
          "num_processed_tokens: "
          "{}, kvp_group_id: {}, max_num_tokens_per_kvp_group: {}",
          seq->seq_id, kv_cache_info.kv_cache_length, metadata->num_q_tokens,
          seq->GetNumTokensStageProcessed(), kvp_group_id_,
          max_num_tokens_per_kvp_group_);
    }

    auto seq_metadata = std::make_shared<SequenceMetadata>(SequenceMetadata(
        metadata->schedule_id, seq->seq_id, metadata->num_q_tokens,
        kv_cache_info.kv_cache_length, GetBlockTable(seq),
        metadata->kvp_group_ids, kv_cache_info.should_save_kv_cache));
    seq_metadata_list.emplace_back(seq_metadata);
  }

  auto seq_arrangement = SequenceArrangement();
  seq_arrangement.Extend(seq_metadata_list);
  seq_metadata_list = seq_arrangement.GetArranged();

  MutableSequences scheduled_seqs;
  scheduled_seqs.reserve(seq_metadata_list.size());
  for (auto metadata : seq_metadata_list) {
    scheduled_seqs.emplace_back(seq_map_[metadata->seq_id]);
  }

  return OnScheduleResult(ignored_seqs, scheduled_seqs, seq_metadata_list);
}
//==============================================================================
void WorkerSequenceManager::FreeSeq(const SeqId& seq_id) {
  ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                       "sequence {} not found", seq_id);
  auto seq = seq_map_[seq_id];
  if (block_manager_.IsAllocated(seq)) {
    block_manager_.Free(seq);
  }
  BaseSequenceManager::FreeSeq(seq_id);
}
//==============================================================================
void WorkerSequenceManager::PreemptSeq(const SeqId& seq_id) {
  BaseSequenceManager::PreemptSeq(seq_id);
  auto seq = seq_map_[seq_id];
  if (block_manager_.IsAllocated(seq)) {
    block_manager_.Free(seq);
  }
}
//==============================================================================
void WorkerSequenceManager::OnSeqScheduled(
    SequenceScheduleMetadataPtr seq_sched_metadata) {
  ASSERT_VALID_POINTER_ARGUMENT(seq_sched_metadata);

  ASSERT_VALID_RUNTIME(
      seq_map_.find(seq_sched_metadata->seq_id) != seq_map_.end(),
      "sequence {} not found", seq_sched_metadata->seq_id);
  ResumeSeq(seq_sched_metadata->seq_id);
  auto seq = seq_map_[seq_sched_metadata->seq_id];
  auto num_total_blocks =
      seq_sched_metadata->kvp_group_block_counter.at(kvp_group_id_);
  LOG_DEBUG("Allocating {} blocks for seq {} in group {}", num_total_blocks,
            seq->seq_id, kvp_group_id_);
  block_manager_.AllocateDelta(seq, num_total_blocks);
}
//==============================================================================
std::vector<int> WorkerSequenceManager::GetBlockTable(SequencePtr seq) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  return *block_manager_.GetBlockTable(seq);
}
//==============================================================================
KVCacheInfo WorkerSequenceManager::ComputeKVCacheInfo(
    SequencePtr seq, const KvpGroupIds& kvp_group_ids) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  auto num_processed_tokens = seq->GetNumTokensStageProcessed();
  for (std::size_t i = 0; i < kvp_group_ids.size(); i++) {
    if (kvp_group_ids[i] == kvp_group_id_) {
      auto num_tokens_in_prev_kvp_ranks = i * max_num_tokens_per_kvp_group_;
      if (num_processed_tokens < num_tokens_in_prev_kvp_ranks) {
        // this KVP rank does not have any processed tokens for this sequence
        return KVCacheInfo(0, false);
      }

      auto num_tokens_remaining =
          num_processed_tokens - num_tokens_in_prev_kvp_ranks;
      if (i != kvp_group_ids.size() - 1 &&
          num_tokens_remaining >= max_num_tokens_per_kvp_group_) {
        // All KVP ranks except the last one, have a limit on KV tokens
        return KVCacheInfo(max_num_tokens_per_kvp_group_, false);
      }
      // some budget remains for KV tokens in this KVP rank
      return KVCacheInfo(num_tokens_remaining, true);
    }
  }
  THROW_RUNTIME_ERROR(
      "Found sequence (id:{}) with KVP Group Ids: {}, on KVP rank: {}",
      seq->seq_id, JoinStrings(kvp_group_ids, ","), kvp_group_id_);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
