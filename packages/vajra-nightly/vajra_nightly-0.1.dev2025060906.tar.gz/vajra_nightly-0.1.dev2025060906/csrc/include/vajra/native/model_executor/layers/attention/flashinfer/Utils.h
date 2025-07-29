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
#include "FlashinferAll.h"
//==============================================================================
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
#include "native/utils/CUDAUtils.h"
#include "native/utils/TorchUtils.h"
//==============================================================================
namespace vajra::flashinfer {
//==============================================================================
struct SplitKVTensor {
  torch::Tensor k_tensor;
  torch::Tensor v_tensor;

  SplitKVTensor(torch::Tensor k_tensor_param, torch::Tensor v_tensor_param)
      : k_tensor(std::move(k_tensor_param)),
        v_tensor(std::move(v_tensor_param)) {}
};
//==============================================================================
struct SegmentPackbitsResult {
  SegmentPackbitsResult(torch::Tensor packed_segments_param,
                        torch::Tensor segment_indices_param)
      : packed_segments(std::move(packed_segments_param)),
        segment_indices(std::move(segment_indices_param)) {}

  torch::Tensor packed_segments;
  torch::Tensor segment_indices;
};
//==============================================================================
struct AttentionOutput {
  torch::Tensor logits;
  std::optional<torch::Tensor> lse;

  AttentionOutput(torch::Tensor logits_param,
                  std::optional<torch::Tensor> lse_param)
      : logits(std::move(logits_param)), lse(std::move(lse_param)) {}
};
//==============================================================================
using UnifiedKVTensor = torch::Tensor;
using KVTensor = std::variant<SplitKVTensor, UnifiedKVTensor>;
//==============================================================================
struct PosEncodingMode {
  enum Type { NONE = 0, ROPE_LLAMA = 1, ALIBI = 2 };

  Type type;

  [[nodiscard]] static Type FromString(const std::string& str /*[in]*/) {
    ASSERT_VALID_RUNTIME(str == "NONE" || str == "ROPE_LLAMA" || str == "ALIBI",
                         "Invalid pos encoding mode: {}", str);
    if (str == "NONE") {
      return Type::NONE;
    } else if (str == "ROPE_LLAMA") {
      return Type::ROPE_LLAMA;
    } else {
      return Type::ALIBI;
    }
  }
};
//==============================================================================
enum MaskMode { NON_CAUSAL = 0, CAUSAL = 1, CUSTOM = 2 };
//==============================================================================
struct TensorLayout {
  enum Type { NHD = 0, HND = 1 };
  Type type;

  [[nodiscard]] static Type FromString(const std::string& str /*[in]*/) {
    ASSERT_VALID_RUNTIME(str == "NHD" || str == "HND",
                         "Invalid tensor layout: {}", str);
    if (str == "NHD") {
      return Type::NHD;
    } else {
      return Type::HND;
    }
  }
};
//==============================================================================
[[nodiscard]] bool IsFa3BackendSupported(int pos_encoding_mode /*[in]*/,
                                         bool use_fp16_qk_reduction /*[in]*/,
                                         bool use_custom_mask /*[in]*/,
                                         at::ScalarType dtype_q /*[in]*/,
                                         at::ScalarType dtype_kv /*[in]*/
);
//==============================================================================
[[nodiscard]] std::string DetermineAttentionBackend(
    torch::Device device /*[in]*/, int pos_encoding_mode /*[in]*/,
    bool use_fp16_qk_reduction /*[in]*/, bool use_custom_mask /*[in]*/,
    at::ScalarType dtype_q /*[in]*/, at::ScalarType dtype_kv /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor ComputePageMaskIndptr(
    const torch::Tensor& qo_indptr /*[in]*/,
    const torch::Tensor& paged_kv_indptr /*[in]*/,
    const torch::Tensor& paged_kv_last_page_len /*[in]*/,
    int64_t page_size /*[in]*/
);
//==============================================================================
[[nodiscard]] SegmentPackbitsResult SegmentPackbits(
    const torch::Tensor& x /*[in]*/, const torch::Tensor& indptr /*[in]*/,
    const std::string& bitorder = "big" /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor GetSeqLens(
    const torch::Tensor& kv_indptr /*[in]*/,
    const torch::Tensor& kv_last_page_len /*[in]*/, int64_t page_size /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor Expand4D(const torch::Tensor& x /*[in]*/,
                                     const std::string& kv_layout /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor Expand5D(const torch::Tensor& x /*[in]*/,
                                     const std::string& kv_layout /*[in]*/
);
//==============================================================================
[[nodiscard]] SplitKVTensor UnpackPagedKVCache(
    const KVTensor& paged_kv_cache /*[in]*/,
    const std::string& kv_layout /*[in]*/
);
//==============================================================================
void CheckCachedQKVDataType(const torch::Tensor& q /*[in]*/,
                            const torch::Tensor& k /*[in]*/,
                            at::ScalarType dtype_q /*[in]*/,
                            at::ScalarType dtype_kv /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor BlockSparseIndicesToVectorSparseOffsets(
    const torch::Tensor& block_sparse_indices /*[in]*/,
    const torch::Tensor& block_sparse_indptr /*[in]*/,
    torch::Tensor& vector_sparse_offsets /*[out]*/,
    torch::Tensor& vector_sparse_indptr /*[out]*/,
    const torch::Tensor& kv_lens /*[in]*/, int64_t stride_block /*[in]*/,
    int64_t stride_n /*[in]*/, int64_t block_size /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor GetAlibiSlopesBuf(int64_t num_heads /*[in]*/,
                                              torch::Device device /*[in]*/
);
//==============================================================================
[[nodiscard]] torch::Tensor GetCacheAlibiSlopesBuf(
    int64_t num_qo_heads /*[in]*/, torch::Device device /*[in]*/
);
//==============================================================================
torch::Tensor TopKTopPSamplingFromLogits(const torch::Tensor& logits,
                                         const torch::Tensor& top_k_tensor,
                                         const torch::Tensor& top_p_tensor);
//==============================================================================
}  // namespace vajra::flashinfer
//==============================================================================
