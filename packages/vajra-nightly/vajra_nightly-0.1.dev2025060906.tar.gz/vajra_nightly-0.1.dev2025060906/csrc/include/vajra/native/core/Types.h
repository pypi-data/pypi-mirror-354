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
//==============================================================================
namespace vajra {
//==============================================================================
using TimeS = double;  // time in seconds
using TokenId = std::int32_t;
using TokenIds = std::vector<TokenId>;
using TokenIdsPtr = std::shared_ptr<TokenIds>;
using BlockId = std::int32_t;
using BlockTable = std::vector<BlockId>;
using BlockTablePtr = std::shared_ptr<BlockTable>;
// Note: BlockNumber is the serial order of the block in the sequence
// where as the BlockId is a unique identifier for the block.
using BlockNumber = std::size_t;
using ReplicaId = std::size_t;
using SeqId = std::string;
using ScheduleId = std::size_t;
using LayerId = std::size_t;
using Rank = std::size_t;
using TensorSize = std::int64_t;
using KvpGroupId = std::size_t;
using KvpGroupIds = std::vector<KvpGroupId>;
//==============================================================================
}  // namespace vajra
//==============================================================================
