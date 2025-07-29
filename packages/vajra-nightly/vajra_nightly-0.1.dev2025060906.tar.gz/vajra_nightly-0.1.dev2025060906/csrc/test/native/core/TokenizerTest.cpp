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

#include "commons/StdCommon.h"
#include "native/core/tokenizer/Tokenizer.h"

namespace vajra {
class TokenizerTest : public ::testing::Test {
 public:
  const std::vector<std::int32_t> INPUT_TOKENS = {
      40914, 11,   1618,  596,   264,   2875,  14646, 922,   43465, 11,   1405,
      1855,  3492, 374,   8272,  555,   459,   43465, 1473,  19182, 1070, 0,
      62904, 233,  358,   2846,  1618,  311,   1520,  4320,  904,   4860, 499,
      617,   922,  43465, 11410, 97,    242,   13,    14910, 499,   1440, 430,
      43465, 649,  387,   1511,  311,   20599, 21958, 323,   16024, 304,  264,
      2523,  323,  57169, 1648,  30,    27623, 226,   2435,  649,   1101, 387,
      1511,  311,  923,   264,   5916,  315,   17743, 311,   701,   6743, 323,
      8158,  13,   64139, 243,   1628,  11,    1550,  499,   1440,  430,  1070,
      527,   1524, 43465, 3953,  323,   7640,  499,   649,   1514,  30,   11410,
      236,   106,  9468,  239,   222,   2100,  11,    733,   8469,  323,  636,
      11782, 449,  43465, 0,     64139, 98,    9468,  236,   101};

  const std::string DECODED =
      "Sure, here's a short paragraph about emoji, "
      "where each word is followed by an emoji:\n\n"
      "Hey there! 👋 I'm here to help answer any questions you have about "
      "emoji 🤔. "
      "Did you know that emoji can be used to convey emotions and feelings in "
      "a "
      "fun and playful way? 😄 "
      "They can also be used to add a touch of personality to your messages "
      "and posts. 💕 "
      "And, did you know that there are even emoji games and activities you "
      "can play? 🎮👀 "
      "So, go ahead and get creative with emoji! 💥🎨";

 protected:
  void SetUp() override {}
};

TEST_F(TokenizerTest, BasicTokenizerTest) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);

  auto input_text = "hello, there";
  auto token_ids = tokenizer->Encode(input_text);
  auto text = tokenizer->Decode(token_ids);

  ASSERT_EQ(input_text, text);
}

// The count in this test refers to the number of times an intermediate decoding
// ended with the unicode replacement character.
//
// The count was verified through a Python script that compared the number of
// times the cursor advanced in the old `detokenize_incrementally` function
TEST_F(TokenizerTest, PartialDecodeTest) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);

  std::size_t c = 0;
  std::string output = "";

  auto tokens_ptr = std::make_shared<std::vector<std::int32_t>>(
      INPUT_TOKENS.begin(), INPUT_TOKENS.begin() + 5);
  auto result = tokenizer->PartialDecode(tokens_ptr, 0, 0);
  output += result.decoded_text;
  std::size_t prefix_offset = result.new_prefix_offset;
  std::size_t read_offset = result.new_read_offset;

  // Simulate adding new tokens, one token at a time
  for (std::size_t i = 6; i <= INPUT_TOKENS.size(); ++i) {
    auto current_tokens = std::make_shared<std::vector<std::int32_t>>(
        INPUT_TOKENS.begin(), INPUT_TOKENS.begin() + i);
    result =
        tokenizer->PartialDecode(current_tokens, prefix_offset, read_offset);
    if (result.decoded_text.length() == 0) {
      c += 1;
    }
    output += result.decoded_text;
    prefix_offset = result.new_prefix_offset;
    read_offset = result.new_read_offset;
  }

  ASSERT_EQ(c, 12);
  ASSERT_EQ(output, DECODED);
}

TEST_F(TokenizerTest, PartialDecodeTestEmpty) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);
  auto empty_tokens = std::make_shared<std::vector<std::int32_t>>();
  auto result = tokenizer->PartialDecode(empty_tokens, 0, 0);
  ASSERT_EQ(result.decoded_text.length(), 0);
  ASSERT_EQ(result.new_prefix_offset, 0);
  ASSERT_EQ(result.new_read_offset, 0);
}

TEST_F(TokenizerTest, PartialDecodeTestIdempotent) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);

  auto tokens =
      std::vector<std::int32_t>(INPUT_TOKENS.begin(), INPUT_TOKENS.begin() + 5);
  auto tokens_ptr = std::make_shared<std::vector<std::int32_t>>(tokens);
  auto result = tokenizer->PartialDecode(tokens_ptr, 0, 0);
  ASSERT_EQ(result.decoded_text.length(), 14);
  ASSERT_EQ(result.new_prefix_offset, 0);
  ASSERT_EQ(result.new_read_offset, 5);

  result = tokenizer->PartialDecode(tokens_ptr, result.new_prefix_offset,
                                    result.new_read_offset);
  ASSERT_EQ(result.decoded_text.length(), 0);
  ASSERT_EQ(result.new_prefix_offset, 0);
  ASSERT_EQ(result.new_read_offset, 5);
}

TEST_F(TokenizerTest, PartialDecodeTestBadArguments) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);
  auto tokens =
      std::vector<std::int32_t>(INPUT_TOKENS.begin(), INPUT_TOKENS.begin() + 5);

  auto tokens_ptr = std::make_shared<std::vector<std::int32_t>>(tokens);
  EXPECT_THROW(tokenizer->PartialDecode(tokens_ptr, 100, 0),
               std::runtime_error);
  EXPECT_THROW(tokenizer->PartialDecode(tokens_ptr, 0, 20), std::runtime_error);
  EXPECT_THROW(tokenizer->PartialDecode(tokens_ptr, 4, 0), std::runtime_error);
}

TEST_F(TokenizerTest, PartialDecodeTestEmoji) {
  auto filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);

  auto tokens1 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 5809, 9468, 239, 222});
  auto result = tokenizer->PartialDecode(tokens1, 0, 0);
  ASSERT_EQ(result.decoded_text, "<|begin_of_text|>�👀");  // NOLINT

  auto tokens2 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 9468, 239, 222, 9468, 239,
                                          222});
  result = tokenizer->PartialDecode(tokens2, 0, 0);
  ASSERT_EQ(result.decoded_text, "<|begin_of_text|>👀👀");  // NOLINT

  auto tokens3 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 9468, 239, 222, 9468, 239,
                                          222, 9468, 239, 222});
  result = tokenizer->PartialDecode(tokens3, 0, 0);
  ASSERT_EQ(result.decoded_text, "<|begin_of_text|>👀👀👀");  // NOLINT

  auto tokens4 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 9468, 239, 222, 58432, 9468,
                                          239, 222});
  result = tokenizer->PartialDecode(tokens4, 0, 0);
  ASSERT_EQ(result.decoded_text, "<|begin_of_text|>👀���👀");  // NOLINT

  auto tokens5 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 9468, 239, 222, 24378,
                                          58432});
  result = tokenizer->PartialDecode(tokens5, 0, 0);
  ASSERT_EQ(result.decoded_text,
            "");  // NOLINT underlying string is "👀�������", but it
                  // ends with the replacement character, which results
                  // in the empty string being returned

  auto tokens6 = std::make_shared<std::vector<std::int32_t>>(
      std::initializer_list<std::int32_t>{128000, 9468, 239, 222, 58432, 617,
                                          9468, 239, 222});
  result = tokenizer->PartialDecode(tokens6, 0, 0);
  ASSERT_EQ(result.decoded_text, "<|begin_of_text|>👀��� have👀");  // NOLINT
}

}  // namespace vajra
