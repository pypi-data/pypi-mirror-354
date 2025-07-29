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
#include "commons/Constants.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Sampling strategy for token generation.
 */
enum class SamplingType {
  Greedy,  ///< Always select the most probable token
  Random   ///< Sample from the probability distribution
};
//==============================================================================
/**
 * @brief Parameters controlling text generation sampling behavior.
 *
 * SamplingParams encapsulates all parameters that control how tokens are
 * sampled during text generation. It supports both greedy decoding (for
 * deterministic output) and various random sampling strategies (for more
 * diverse outputs).
 *
 * The sampling strategy is automatically determined based on temperature:
 * - Temperature < 0.00001 (kSamplingEps): Greedy sampling
 * - Temperature >= 0.00001: Random sampling with temperature, top-p, top-k
 *
 * @note All parameters are immutable after construction to ensure thread
 * safety.
 */
class SamplingParams {
 public:
  SamplingParams(float temperature_param = 1.0f /*[in]*/,
                 float top_p_param = 1.0f /*[in]*/,
                 int top_k_param = -1 /*[in]*/,
                 bool ignore_eos_param = false /*[in]*/,
                 std::size_t max_tokens_param = 2048 /*[in]*/)
      : temperature(temperature_param),
        top_p(top_p_param),
        top_k(top_k_param),
        ignore_eos(ignore_eos_param),
        max_tokens(max_tokens_param) {
    VerifyArgs();
    if (temperature < kSamplingEps) VerifyGreedySampling();
  }

  // define copy constructor
  SamplingParams(const SamplingParams& other)
      : temperature(other.temperature),
        top_p(other.top_p),
        top_k(other.top_k),
        ignore_eos(other.ignore_eos),
        max_tokens(other.max_tokens) {}

  inline SamplingType GetSamplingType() const {
    return (temperature < kSamplingEps) ? SamplingType::Greedy
                                        : SamplingType::Random;
  }

  std::string ToString() const {
    return std::format(
        "SamplingParams("
        "Temperature: {},"
        "TopP: {},"
        "TopK: {},"
        "IgnoreEos: {},"
        "NumMaxtokens: {})",
        temperature, top_p, top_k, ignore_eos, max_tokens);
  }

  const float temperature;  ///< Controls randomness (0=deterministic,
                            ///< higher=more random)
  const float top_p;        ///< Nucleus sampling threshold (0-1, 1=disabled)
  const int top_k;          ///< Top-k sampling limit (-1=disabled)
  const bool ignore_eos;    ///< Whether to continue generation past EOS token
  const std::size_t max_tokens;  ///< Maximum number of tokens to generate

 private:
  void VerifyArgs() const;
  void VerifyGreedySampling() const;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
