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
#include "native/core/block_space_manager/BlockSpaceManager.h"

#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
BlockSpaceManager::BlockSpaceManager(std::size_t block_size /*[in]*/,
                                     std::size_t num_gpu_blocks /*[in]*/,
                                     std::size_t max_model_len /*[in]*/,
                                     float watermark /*[in]*/)
    : block_size_(block_size),
      num_total_gpu_blocks_(num_gpu_blocks),
      max_model_len_(max_model_len),
      watermark_(watermark) {
  ASSERT_VALID_ARGUMENTS(watermark_ >= 0.0f && watermark_ <= 1.0f,
                         "Watermark must be in [0,1], got {}", watermark_);

  watermark_blocks_ = static_cast<std::size_t>(watermark_ * num_gpu_blocks);

  LOG_INFO("Initializing BlockSpaceManager with watermark: {}",
           watermark_blocks_);

  // Initialize the free blocks
  free_blocks_.reserve(num_gpu_blocks);
  for (std::size_t block_id = 0; block_id < num_gpu_blocks; ++block_id) {
    free_blocks_.push_back(static_cast<BlockId>(block_id));
  }
}
//==============================================================================
bool BlockSpaceManager::CanAllocateBlocks(
    std::size_t num_required_blocks /*[in]*/) const {
  // Use watermark to avoid frequent cache eviction
  return free_blocks_.size() >= watermark_blocks_ + num_required_blocks;
}
//==============================================================================
BlockId BlockSpaceManager::AllocateFreeBlock() {
  ASSERT_VALID_RUNTIME(!free_blocks_.empty(),
                       "Out of memory! No free blocks are available!");

  BlockId block = free_blocks_.back();
  free_blocks_.pop_back();
  return block;
}
//==============================================================================
void BlockSpaceManager::Allocate(const SequencePtr seq /*[in]*/,
                                 std::size_t num_blocks /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);
  // Make sure that seq is not already allocated
  ASSERT_VALID_RUNTIME(block_tables_.find(seq->seq_id) == block_tables_.end(),
                       "Sequence {} already allocated!", seq->seq_id);

  // Emplace the block table inside the map
  block_tables_.emplace(seq->seq_id, std::make_shared<BlockTable>());
  auto block_table = block_tables_[seq->seq_id];

  // Allocate new physical token blocks that will store the prompt tokens
  block_table->reserve(num_blocks);
  for (std::size_t i = 0; i < num_blocks; ++i) {
    BlockId block = AllocateFreeBlock();
    block_table->push_back(block);
  }
}
//==============================================================================
void BlockSpaceManager::AllocateDelta(const SequencePtr seq /*[in]*/,
                                      std::size_t total_num_blocks /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Allocate new physical token blocks that will store the prompt tokens
  if (block_tables_.find(seq->seq_id) == block_tables_.end()) {
    Allocate(seq, total_num_blocks);
    return;
  }

  std::size_t num_existing_blocks = block_tables_[seq->seq_id]->size();

  ASSERT_VALID_ARGUMENTS(
      total_num_blocks >= num_existing_blocks,
      "Requested total blocks ({}) is smaller than currently "
      "allocated ({}) for sequence {}",
      total_num_blocks, num_existing_blocks, seq->seq_id);

  std::size_t num_new_blocks = total_num_blocks - num_existing_blocks;

  for (std::size_t i = 0; i < num_new_blocks; ++i) {
    BlockId block = AllocateFreeBlock();
    block_tables_[seq->seq_id]->push_back(block);
  }
}
//==============================================================================
bool BlockSpaceManager::CanAppendSlot() const { return !free_blocks_.empty(); }

bool BlockSpaceManager::AppendSlot(const SequencePtr seq /*[in]*/,
                                   std::size_t num_total_blocks /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // make sure that seq is present in block_tables_
  auto block_table_it = block_tables_.find(seq->seq_id);
  ASSERT_VALID_RUNTIME(block_table_it != block_tables_.end(),
                       "Sequence {} not found in block tables!", seq->seq_id);

  auto block_table = block_table_it->second;

  const auto& logical_blocks = seq->GetLogicalTokenBlocks();
  if (num_total_blocks < logical_blocks.size()) {
    // The sequence has a new logical block.
    // Allocate a new physical block.
    BlockId block = AllocateFreeBlock();
    block_table->push_back(block);
    return true;
  }

  return false;
}
//==============================================================================
void BlockSpaceManager::Free(const SequencePtr seq /*[in]*/) {
  auto it = block_tables_.find(seq->seq_id);
  if (it == block_tables_.end()) {
    // Already freed or haven't been scheduled yet.
    return;
  }

  auto block_table = it->second;
  free_blocks_.insert(free_blocks_.end(), block_table->begin(),
                      block_table->end());
  block_tables_.erase(it);
}
//==============================================================================
const BlockTablePtr BlockSpaceManager::GetBlockTable(
    const SequencePtr seq /*[in]*/) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  auto it = block_tables_.find(seq->seq_id);
  ASSERT_VALID_ARGUMENTS(it != block_tables_.end(),
                         "Sequence {} does not have an allocated block table",
                         seq->seq_id);

  return it->second;
}
//==============================================================================
BlockTable BlockSpaceManager::GetBlockTableCopy(
    const SequencePtr seq /*[in]*/) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  auto it = block_tables_.find(seq->seq_id);
  ASSERT_VALID_ARGUMENTS(it != block_tables_.end(),
                         "Sequence {} does not have an allocated block table",
                         seq->seq_id);

  auto block_table = it->second;
  BlockTable block_table_copy(*block_table);
  return block_table_copy;
}
//==============================================================================
bool BlockSpaceManager::IsAllocated(const SequencePtr seq /*[in]*/) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  return block_tables_.find(seq->seq_id) != block_tables_.end();
}
//==============================================================================
}  // namespace vajra
//==============================================================================
