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
#include <gtest/gtest.h>
//==============================================================================
#include "commons/StdCommon.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
using vajra::MutableSequencePtr;
using vajra::SamplingParams;
using vajra::Sequence;
using vajra::TimeS;
using vajra::TokenIds;
//==============================================================================
namespace vajra {
// Test helper class that has friend access to Sequence
class TestSequenceManager {
 public:
  static void UpdateTokensProcessed(MutableSequencePtr seq,
                                    std::size_t num_tokens) {
    seq->UpdateTokensProcessed(num_tokens);
  }

  static void UpdatePromptTokensProcessed(MutableSequencePtr seq,
                                          std::size_t num_tokens) {
    seq->UpdatePromptTokensProcessed(num_tokens);
  }

  static void UpdatePromptTokensStageProcessed(MutableSequencePtr seq,
                                               std::size_t num_tokens) {
    seq->UpdatePromptTokensStageProcessed(num_tokens);
  }

  static void AppendTokenId(MutableSequencePtr seq, vajra::TokenId token_id) {
    seq->AppendTokenId(token_id);
  }
};
}  // namespace vajra
//==============================================================================
using vajra::TestSequenceManager;
//==============================================================================
class SequenceTest : public ::testing::Test {
 protected:
  void SetUp() override {
    // Common setup for tests
    std::string seq_id = "test_sequence";
    std::string prompt = "This is a test prompt";
    std::shared_ptr<TokenIds> prompt_tokens = std::make_shared<TokenIds>();
    prompt_tokens->insert(prompt_tokens->end(), {1, 2, 3, 4, 5});
    std::size_t block_size = 1024;
    std::size_t eos_token_id = 0;
    TimeS arrival_time = 0.0;
    SamplingParams sampling_params;  // Default sampling params

    test_sequence = std::make_shared<Sequence>(
        vajra::SequenceParams(seq_id, prompt, prompt_tokens, block_size,
                              eos_token_id, arrival_time, sampling_params));
  }

  MutableSequencePtr test_sequence;
};
//==============================================================================
// Test token processing workflow: unprocessed -> stage processed -> processed
TEST_F(SequenceTest, TokenProcessingWorkflow) {
  // Initially no tokens processed
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 0);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(test_sequence->GetPromptProcessingFinished());

  // Step 1: Stage process first 2 tokens
  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(test_sequence->GetPromptStageProcessingFinished());

  // Step 2: Fully process first token
  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 1);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 1);

  // Step 3: Stage process all prompt tokens
  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 3);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 5);
  EXPECT_TRUE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(test_sequence->GetPromptProcessingFinished());

  // Step 4: Process all prompt tokens
  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 4);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 5);
  EXPECT_TRUE(test_sequence->GetPromptProcessingFinished());
}
//==============================================================================
// Test TestAppendTokenId
TEST_F(SequenceTest, TestAppendTokenId) {
  // process prompt tokens
  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 5);
  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 5);
  EXPECT_TRUE(test_sequence->GetPromptProcessingFinished());
  EXPECT_EQ(test_sequence->GetNumTokensProcessed(), 5);

  // Add output tokens
  TestSequenceManager::AppendTokenId(test_sequence, 10);
  TestSequenceManager::AppendTokenId(test_sequence, 20);
  // Verify they're added but not processed
  EXPECT_EQ(test_sequence->GetOutputLength(), 2);
  EXPECT_EQ(test_sequence->GetOutputTokenIds()->at(0), 10);
  EXPECT_EQ(test_sequence->GetOutputTokenIds()->at(1), 20);
  // should not affect number of processed tokens
  EXPECT_EQ(test_sequence->GetNumTokensProcessed(), 5);
  EXPECT_EQ(test_sequence->GetNumTokensStageProcessed(), 5);

  // process output tokens
  TestSequenceManager::UpdateTokensProcessed(test_sequence, 2);
  EXPECT_EQ(test_sequence->GetNumTokensProcessed(), 7);
}
//==============================================================================
TEST_F(SequenceTest, OutOfBoundsUpdate) {
  // Try to stage process more tokens than exist
  EXPECT_THROW(
      TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 10),
      std::runtime_error);

  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 4);
  EXPECT_THROW(
      TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 2),
      std::runtime_error);

  // Try to append tokens before processing prompt
  EXPECT_THROW(TestSequenceManager::AppendTokenId(test_sequence, 10),
               std::runtime_error);

  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 1);
  EXPECT_TRUE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(test_sequence->GetPromptProcessingFinished());
  EXPECT_THROW(TestSequenceManager::AppendTokenId(test_sequence, 10),
               std::runtime_error);

  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 4);
  EXPECT_THROW(
      TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 2),
      std::runtime_error);

  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 1);
  TestSequenceManager::AppendTokenId(test_sequence, 10);
  EXPECT_EQ(test_sequence->GetNumTokensProcessed(), 5);
  TestSequenceManager::UpdateTokensProcessed(test_sequence, 1);
  EXPECT_EQ(test_sequence->GetNumTokensProcessed(), 6);
}
//==============================================================================
TEST_F(SequenceTest, NumQTokens) {
  EXPECT_EQ(test_sequence->GetNumProcessableTokens(), 5);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 0);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(test_sequence->GetPromptProcessingFinished());

  // Step 1: Stage process first 2 tokens
  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_EQ(test_sequence->GetNumProcessableTokens(), 3);

  // Step 2: Fully process first token
  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 1);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 1);
  EXPECT_EQ(test_sequence->GetNumProcessableTokens(), 3);

  // Step 3: Stage process all prompt tokens
  TestSequenceManager::UpdatePromptTokensStageProcessed(test_sequence, 3);
  EXPECT_EQ(test_sequence->GetNumPromptTokensStageProcessed(), 5);
  EXPECT_TRUE(test_sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(test_sequence->GetPromptProcessingFinished());
  EXPECT_EQ(test_sequence->GetNumProcessableTokens(), 0);

  // Step 4: Process all prompt tokens
  TestSequenceManager::UpdatePromptTokensProcessed(test_sequence, 4);
  EXPECT_EQ(test_sequence->GetNumPromptTokensProcessed(), 5);
  EXPECT_TRUE(test_sequence->GetPromptProcessingFinished());

  // Step 5: Append tokens
  TestSequenceManager::AppendTokenId(test_sequence, 10);
  TestSequenceManager::AppendTokenId(test_sequence, 20);
  EXPECT_EQ(test_sequence->GetNumProcessableTokens(), 2);
}
//==============================================================================
