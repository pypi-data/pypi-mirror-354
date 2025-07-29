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
#include "native/datatypes/DecodeStream.h"
//==============================================================================
#include "commons/Logging.h"
#include "native/core/tokenizer/Tokenizer.h"
//==============================================================================
namespace vajra {
//==============================================================================
void DecodeStream::DecodeIncremental(std::shared_ptr<Tokenizer> tokenizer,
                                     const TokenIdsPtr& token_ids) {
  auto result =
      tokenizer->PartialDecode(token_ids, prefix_offset_, read_offset_);

  if (!result.decoded_text.empty()) {
    output_text_ += result.decoded_text;
    prefix_offset_ = result.new_prefix_offset;
    read_offset_ = result.new_read_offset;
  }
}
//==============================================================================
void DecodeStream::Reset() {
  output_text_.clear();
  prefix_offset_ = 0;
  read_offset_ = 0;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
