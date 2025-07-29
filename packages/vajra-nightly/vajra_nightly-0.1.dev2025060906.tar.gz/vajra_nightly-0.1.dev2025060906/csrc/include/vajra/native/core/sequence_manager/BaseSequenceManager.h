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
#include "commons/ClassTraits.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/core/Types.h"
#include "native/datatypes/RequestOutput.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Result of OnSchedule operation containing ignored and scheduled
 * sequences
 */
struct OnScheduleResult {
  OnScheduleResult(MutableSequences ignored_seqs,
                   MutableSequences scheduled_seqs,
                   std::optional<SequenceMetadataVector>
                       sequence_metadata_list = std::nullopt)
      : ignored_seqs(std::move(ignored_seqs)),
        scheduled_seqs(std::move(scheduled_seqs)),
        sequence_metadata_list(std::move(sequence_metadata_list)) {}

  MutableSequences ignored_seqs;
  MutableSequences scheduled_seqs;
  std::optional<SequenceMetadataVector> sequence_metadata_list;
};
//==============================================================================
class BaseSequenceManager : public NonCopyableNonMovable {
 public:
  explicit BaseSequenceManager(bool enable_sequence_pipeline_parallel)
      : enable_sequence_pipeline_parallel_(enable_sequence_pipeline_parallel) {}

  virtual ~BaseSequenceManager() = default;
  virtual inline void AddSequence(MutableSequencePtr seq) {
    ASSERT_VALID_POINTER_ARGUMENT(seq);

    std::lock_guard<std::recursive_mutex> lk(mutex_);

    ASSERT_VALID_RUNTIME(seq_map_.find(seq->seq_id) == seq_map_.end(),
                         "sequence {} already added ", seq->seq_id);
    seq_map_[seq->seq_id] = seq;
  }

  [[nodiscard]] virtual inline SequencePtr GetSequence(
      const SeqId& seq_id) const {
    return seq_map_.at(seq_id);
  }

  [[nodiscard]] virtual inline MutableSequencePtr GetMutableSequence(
      const SeqId& seq_id) {
    return seq_map_.at(seq_id);
  }

  [[nodiscard]] virtual OnScheduleResult OnSchedule(
      SchedulerOutputPtr scheduler_output);

  virtual void OnStepCompleted(const std::vector<SequenceScheduleMetadataPtr>&
                                   seq_schedule_metadata_list,
                               const ValidSamplerOutputs& sampler_outputs);

  virtual void OnStageCompleted(SchedulerOutputPtr scheduler_output);

  [[nodiscard]] virtual std::vector<RequestOutputPtr> GenerateRequestOutputs(
      const Sequences& ignored_seqs, const Sequences& scheduled_seqs);

  virtual void OnGenerateRequestOutput(MutableSequencePtr) {
    // No-op by default
    // This is only defined for engine sequence manager
  }

 protected:
  virtual inline void FreeSeq(const SeqId& seq_id) {
    ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                         "sequence {} not found", seq_id);
    seq_map_.erase(seq_id);
  }

  virtual void PreemptSeq(const SeqId& seq_id);

  virtual void PauseSeq(const SeqId& seq_id);

  virtual void ResumeSeq(const SeqId& seq_id);

  virtual inline void OnSeqScheduled(
      SequenceScheduleMetadataPtr seq_sched_metadata) {
    ASSERT_VALID_POINTER_ARGUMENT(seq_sched_metadata);
    ResumeSeq(seq_sched_metadata->seq_id);
  }

  [[nodiscard]] virtual BlockTable GetBlockTable(SequencePtr seq) const = 0;

  virtual void ProcessSeqOutput(MutableSequencePtr seq,
                                SamplerOutputPtr sample);

  std::unordered_map<SeqId, MutableSequencePtr> seq_map_;
  bool enable_sequence_pipeline_parallel_;
  std::recursive_mutex mutex_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
