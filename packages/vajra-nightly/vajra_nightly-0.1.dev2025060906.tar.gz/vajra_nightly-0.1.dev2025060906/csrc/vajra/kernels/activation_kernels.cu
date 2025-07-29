#include <ATen/cuda/CUDAContext.h>
#include <torch/all.h>

#include "kernels/dispatch_utils.h"

namespace vajra {

template<typename T>
__device__ __forceinline__ T silu(const T& x) {
  // x * sigmoid(x)
  return (T) (((float) x) / (1.0f + expf((float) -x)));
}

template<typename scalar_t>
__global__ void silu_and_mul_kernel(
  scalar_t* __restrict__ out,               // [num_tokens, d]
  const scalar_t* __restrict__ input,       // [num_tokens, 2, d]
  const int d) {
  const int64_t token_idx = blockIdx.x;
  for (int64_t idx = threadIdx.x; idx < d; idx += blockDim.x) {
    const scalar_t x = __ldg(&input[token_idx * 2 * d + idx]);
    const scalar_t y = __ldg(&input[token_idx * 2 * d + d + idx]);
    out[token_idx * d + idx] = silu(x) * y;
  }
}

} // namespace vajra

void silu_and_mul(
  torch::Tensor& out,      // [num_tokens, d]
  const torch::Tensor& input)    // [num_tokens, 2 * d]
{
  int64_t num_tokens = input.size(0);
  int d = input.size(1) / 2;

  dim3 grid(num_tokens);
  dim3 block(std::min(d, 1024));
  const cudaStream_t stream = at::cuda::getCurrentCUDAStream();
  VAJRA_DISPATCH_FLOATING_TYPES(
    input.scalar_type(),
    "silu_and_mul_kernel",
    [&] {
      vajra::silu_and_mul_kernel<scalar_t><<<grid, block, 0, stream>>>(
        out.data_ptr<scalar_t>(),
        input.data_ptr<scalar_t>(),
        d);
    });
}

namespace vajra {

// Element-wise activation kernel template.
template<typename scalar_t, scalar_t (*ACT_FN)(const scalar_t&)>
__global__ void activation_kernel(
  scalar_t* __restrict__ out,               // [num_tokens, d]
  const scalar_t* __restrict__ input,       // [num_tokens, d]
  const int d) {
  const int64_t token_idx = blockIdx.x;
  for (int64_t idx = threadIdx.x; idx < d; idx += blockDim.x) {
    const scalar_t x = __ldg(&input[token_idx * d + idx]);
    out[token_idx * d + idx] = ACT_FN(x);
  }
}

} // namespace vajra

// Launch element-wise activation kernel.
#define LAUNCH_ACTIVATION_KERNEL(KERNEL)                                                  \
  int64_t num_tokens = input.size(0);                                                         \
  int d = input.size(1);                                                                  \
  dim3 grid(num_tokens);                                                                  \
  dim3 block(std::min(d, 1024));                                                          \
  const cudaStream_t stream = at::cuda::getCurrentCUDAStream();                           \
  VAJRA_DISPATCH_FLOATING_TYPES(                                                           \
    input.scalar_type(),                                                                  \
    "activation_kernel",                                                                  \
    [&] {                                                                                 \
      vajra::activation_kernel<scalar_t, KERNEL<scalar_t>><<<grid, block, 0, stream>>>(    \
        out.data_ptr<scalar_t>(),                                                         \
        input.data_ptr<scalar_t>(),                                                       \
        d);                                                                               \
    });

namespace vajra {

template<typename T>
__device__ __forceinline__ T gelu_new_kernel(const T& x) {
  const float x3 = (float) (x * x * x);
  const T t = (T) tanhf((T) (0.79788456f * (float) (x + (T) (0.044715f * x3))));
  return ((T) 0.5) * x * (((T) 1.0) + t);
}

template<typename T>
__device__ __forceinline__ T gelu_fast_kernel(const T& x) {
  const float f = (float) x;
  const T t = (T) tanhf(((T) (f * 0.79788456f)) * (((T) 1.0) + (T) (0.044715f * f) * x));
  return ((T) 0.5) * x * (((T) 1.0) + t);
}

} // namespace vajra

void gelu_new(
  torch::Tensor& out,     // [num_tokens, d]
  const torch::Tensor& input)   // [num_tokens, d]
{
  LAUNCH_ACTIVATION_KERNEL(vajra::gelu_new_kernel);
}

void gelu_fast(
  torch::Tensor& out,     // [num_tokens, d]
  const torch::Tensor& input)   // [num_tokens, d]
{
  LAUNCH_ACTIVATION_KERNEL(vajra::gelu_fast_kernel);
}
