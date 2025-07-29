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
#include "commons/StdCommon.h"
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
// MPI/Rank Constants
constexpr Rank kRootRank = 0;
//==============================================================================
// Display Constants
constexpr std::size_t kMaxTokenPreviewCount = 5;
constexpr const char* kNullString = "null";
constexpr const char* kNoneString = "none";
constexpr const char* kEllipsis = "...";
//==============================================================================
// KVP Group Constants
constexpr KvpGroupId kInvalidKvpGroupId =
    std::numeric_limits<KvpGroupId>::max();
//==============================================================================
// Sampling Constants
constexpr float kSamplingEps = 1e-5f;
//==============================================================================
}  // namespace vajra
//==============================================================================
