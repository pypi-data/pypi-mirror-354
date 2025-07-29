# Copyright 2023 The Vajra team.
# Adapted from https://github.com/NVIDIA/Megatron-LM/blob/main/megatron/core/tensor_parallel/layers.py
# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.


# Parts of the code here are adapted from PyTorch
# repo: https://github.com/pytorch/pytorch
from typing import Optional, Tuple, Union

import torch
import torch.nn.functional as F
from torch.nn.parameter import Parameter

# Add type: ignore to suppress missing stubs.
from vajra._native.model_executor.layers import (
    ColumnParallelLinear as ColumnParallelLinearC,
)
from vajra._native.model_executor.layers import RowParallelLinear as RowParallelLinearC
from vajra._native.model_executor.layers import (
    VocabParallelEmbedding as VocabParallelEmbeddingC,
)
from vajra.logger import init_logger
from vajra.metrics_store import CudaTimer, MetricType
from vajra.model_executor.parallel_utils.parallel_state import (
    get_process_group_wrapper,
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
)
from vajra.model_executor.utils import use_native_backend
from vajra.model_executor.weight_utils import (
    convert_pyslice_to_tensor,
)

from .mappings import (
    gather_from_tensor_model_parallel_region,
    reduce_from_tensor_model_parallel_region,
    scatter_to_tensor_model_parallel_region,
)
from .utils import VocabUtility, divide

logger = init_logger(__name__)


class VocabParallelEmbedding(torch.nn.Module):
    """Embedding parallelized in the vocabulary dimension.

    This is mainly adapted from torch.nn.Embedding and all the default
    values are kept.
    Arguments:
        num_embeddings: vocabulary size.
        embedding_dim: size of hidden state.

    Keyword Arguments:
        params_dtype
    """

    def __init__(
        self,
        num_embeddings: int,
        embedding_dim: int,
        params_dtype: Optional[torch.dtype] = None,
        linear_op_metric: Optional[MetricType] = None,
        communication_op_metric: Optional[MetricType] = None,
        reduce_results: Optional[bool] = True,
        world_size: Optional[int] = None,
        rank: Optional[int] = None,
        use_native_execution_backend: Optional[bool] = False,
    ):
        super(VocabParallelEmbedding, self).__init__()

        # Keep the input dimensions.
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        if params_dtype is None:
            params_dtype = torch.get_default_dtype()

        # Set the defaults for compatibility.
        self.padding_idx = None
        self.max_norm = None
        self.norm_type = 2.0
        self.scale_grad_by_freq = False
        self.sparse = False
        self._weight = None
        self.tensor_model_parallel_size = (
            get_tensor_model_parallel_world_size() if world_size is None else world_size
        )
        self.rank = get_tensor_model_parallel_rank() if rank is None else rank
        self.reduce_results = reduce_results
        # Divide the weight matrix along the vocaburaly dimension.
        self.vocab_start_index, self.vocab_end_index = (
            VocabUtility.vocab_range_from_global_vocab_size(
                self.num_embeddings, self.rank, self.tensor_model_parallel_size
            )
        )
        self.num_embeddings_per_partition = (
            self.vocab_end_index - self.vocab_start_index
        )
        self.use_native_execution_backend = use_native_execution_backend

        self.weight = Parameter(
            torch.empty(
                self.num_embeddings_per_partition,
                self.embedding_dim,
                device=torch.cuda.current_device(),
                dtype=params_dtype,
            )
        )

        self._linear_timer = CudaTimer(linear_op_metric)
        self._communication_timer = CudaTimer(communication_op_metric)

        if use_native_execution_backend:
            self.native_handle = VocabParallelEmbeddingC(
                self.num_embeddings,
                self.embedding_dim,
                self.tensor_model_parallel_size,
                self.rank,
                self.reduce_results,
                self.vocab_start_index,
                self.vocab_end_index,
                self.num_embeddings_per_partition,
                self.weight,
                get_process_group_wrapper(),
            )

    @use_native_backend
    def forward(self, input_):
        if self.tensor_model_parallel_size > 1:
            # Build the mask.
            input_mask = (input_ < self.vocab_start_index) | (
                input_ >= self.vocab_end_index
            )
            # Mask the input.
            masked_input = input_.clone() - self.vocab_start_index
            masked_input[input_mask] = 0
        else:
            masked_input = input_
            # Get the embeddings.
        with self._linear_timer:
            output_parallel = F.embedding(
                masked_input,
                self.weight,
                self.padding_idx,
                self.max_norm,
                self.norm_type,
                self.scale_grad_by_freq,
                self.sparse,
            )

        # Mask the output embedding.
        if self.tensor_model_parallel_size > 1:
            output_parallel[input_mask, :] = 0.0  # type: ignore
        if self.reduce_results:
            # Reduce across all the model parallel GPUs.
            with self._communication_timer:
                output = reduce_from_tensor_model_parallel_region(output_parallel)
        else:
            output = output_parallel
        return output


class ColumnParallelLinear(torch.nn.Module):
    """Linear layer with column parallelism.

    The linear layer is defined as Y = XA + b. A is parallelized along
    its second dimension as A = [A_1, ..., A_p].

    Arguments:
        input_size: first dimension of matrix A.
        output_size: second dimension of matrix A.

    Keyword Arguments
        bias: If true, add bias
        gather_output: If true, call all-gather on output and make Y available
                       to all GPUs, otherwise, every GPU will have its output
                       which is Y_i = XA_i
        skip_bias_add: This was added to enable performance optimations where bias
                       can be fused with other elementwise operations. we skip
                       adding bias but instead return it.
        params_dtype:
    """

    def __init__(
        self,
        input_size,
        output_size,
        *,
        bias=True,
        gather_output=True,
        skip_bias_add=False,
        params_dtype=None,
        linear_op_metric: Optional[MetricType] = None,
        communication_op_metric: Optional[MetricType] = None,
        world_size: Optional[int] = None,
        layer_id: Optional[int] = None,
        use_native_execution_backend: Optional[bool] = False,
    ):
        super(ColumnParallelLinear, self).__init__()

        # Keep input parameters
        self.input_size = input_size
        self.output_size = output_size
        self.gather_output = gather_output
        # Divide the weight matrix along the last dimension.
        self.world_size = (
            get_tensor_model_parallel_world_size() if world_size is None else world_size
        )
        self.output_size_per_partition = divide(output_size, self.world_size)
        self.skip_bias_add = skip_bias_add

        if params_dtype is None:
            params_dtype = torch.get_default_dtype()

        self.use_native_execution_backend = use_native_execution_backend

        # Parameters.
        # Note: torch.nn.functional.linear performs XA^T + b and as a result
        # we allocate the transpose.
        self.create_weights(params_dtype)

        if bias:
            self.bias = Parameter(
                torch.empty(
                    self.output_size_per_partition,
                    device=torch.cuda.current_device(),
                    dtype=params_dtype,
                )
            )
            # Always initialize bias to zero.
            with torch.no_grad():
                self.bias.zero_()
        else:
            self.register_parameter("bias", None)

        self._linear_timer = CudaTimer(linear_op_metric, layer_id=layer_id)
        self._communication_timer = CudaTimer(
            communication_op_metric, layer_id=layer_id
        )

        if use_native_execution_backend:
            self.native_handle = ColumnParallelLinearC(
                self.input_size,
                self.output_size,
                self.gather_output,
                self.world_size,
                self.skip_bias_add,
                self.weight,
                self.bias,
                get_process_group_wrapper(),
            )

    def create_weights(self, dtype: torch.dtype) -> None:
        self.weight = Parameter(
            torch.empty(
                self.output_size_per_partition,
                self.input_size,
                device=torch.cuda.current_device(),
                dtype=dtype,
            )
        )
        setattr(self.weight, "weight_loader", self.weight_loader)

    @use_native_backend
    def forward(self, input_):
        """Forward of ColumnParallelLinear

        Args:
            input_: 3D tensor whose order of dimension is [sequence, batch, hidden]

        Returns:
            - output
            - bias
        """
        bias = self.bias if not self.skip_bias_add else None

        input_parallel = input_
        # Matrix multiply.
        with self._linear_timer:
            output_parallel = F.linear(input_parallel, self.weight, bias)

        if self.gather_output:
            # All-gather across the partitions.
            with self._communication_timer:
                # Start async gather without waiting
                output = gather_from_tensor_model_parallel_region(output_parallel)
        else:
            output = output_parallel
        output_bias = self.bias if self.skip_bias_add else None
        return output

    def weight_loader(
        self,
        param,
        param_name,
        loaded_weight,
        tp_rank,
        shard_size=None,
        param_slice_offset=None,
    ):
        if shard_size == None:
            shard_size = param.shape[0]
        start_idx = tp_rank * shard_size
        end_idx = (tp_rank + 1) * shard_size
        loaded_weight = loaded_weight[start_idx:end_idx]
        loaded_weight = convert_pyslice_to_tensor(loaded_weight)

        param_slice = param.data
        if param_slice_offset != None:
            param_slice = param.data[
                param_slice_offset : param_slice_offset + shard_size
            ]

        assert param_slice.shape == loaded_weight.shape, (
            f"{param_name} shape mismatch between model and checkpoint: "
            f"{param_slice.shape} != {loaded_weight.shape}"
        )
        param_slice.copy_(loaded_weight)


class RowParallelLinear(torch.nn.Module):
    """Linear layer with row parallelism.

    The linear layer is defined as Y = XA + b. A is parallelized along
    its first dimension and X along its second dimension as:
               -   -
              | A_1 |
              | .   |
          A = | .   |        X = [X_1, ..., X_p]
              | .   |
              | A_p |
               -   -
    Arguments:
        input_size: first dimension of matrix A.
        output_size: second dimension of matrix A.

    Keyword Arguments:
        bias: If true, add bias. Note that bias is not parallelized.
        input_is_parallel: If true, we assume that the input is already
                           split across the GPUs and we do not split
                           again.
        init_method: method to initialize weights. Note that bias is always set
                     to zero.
        stride: For the strided linear layers.
        keep_master_weight_for_test: This was added for testing and should be
                                     set to False. It returns the master weights
                                     used for initialization.
        skip_bias_add: This was added to enable performance optimization where bias
                       can be fused with other elementwise operations. We skip
                       adding bias but instead return it.
        params_dtype:
        reduce_results:
    """

    def __init__(
        self,
        input_size,
        output_size,
        *,
        bias=True,
        input_is_parallel=False,
        skip_bias_add=False,
        params_dtype=None,
        reduce_results=True,
        linear_op_metric: Optional[MetricType] = None,
        communication_op_metric: Optional[MetricType] = None,
        world_size: Optional[int] = None,
        layer_id: Optional[int] = None,
        use_native_execution_backend: Optional[bool] = False,
    ):
        super(RowParallelLinear, self).__init__()

        # Keep input parameters
        self.input_size = input_size
        self.output_size = output_size
        self.input_is_parallel = input_is_parallel
        self.reduce_results = reduce_results
        if params_dtype is None:
            params_dtype = torch.get_default_dtype()

        # Divide the weight matrix along the last dimension.
        self.world_size = (
            get_tensor_model_parallel_world_size() if world_size is None else world_size
        )
        self.input_size_per_partition = divide(input_size, self.world_size)
        self.skip_bias_add = skip_bias_add

        self.use_native_execution_backend = use_native_execution_backend

        self.create_weights(params_dtype)

        if not reduce_results and (bias and not skip_bias_add):
            logger.warning(
                "When not reduce the results, adding bias to the "
                "results can lead to incorrect results"
            )

        if bias:
            self.bias = Parameter(
                torch.empty(
                    self.output_size,
                    device=torch.cuda.current_device(),
                    dtype=params_dtype,
                )
            )

            # Always initialize bias to zero.
            with torch.no_grad():
                self.bias.zero_()
        else:
            self.register_parameter("bias", None)

        self._linear_timer = CudaTimer(linear_op_metric, layer_id=layer_id)
        self._communication_timer = CudaTimer(
            communication_op_metric, layer_id=layer_id
        )
        if use_native_execution_backend:
            self.native_handle = RowParallelLinearC(
                self.input_size,
                self.output_size,
                self.input_is_parallel,
                self.reduce_results,
                self.world_size,
                self.input_size_per_partition,
                self.skip_bias_add,
                self.weight,
                self.bias,
                get_process_group_wrapper(),
            )

    def create_weights(self, dtype: torch.dtype) -> None:
        self.weight = Parameter(
            torch.empty(
                self.output_size,
                self.input_size_per_partition,
                device=torch.cuda.current_device(),
                dtype=dtype,
            )
        )
        setattr(self.weight, "weight_loader", self.weight_loader)

    @use_native_backend
    def forward(self, input_):
        """Forward of RowParallelLinear

        Args:
            input_: 3D tensor whose order of dimension is [sequence, batch, hidden]

        Returns:
            - output
            - bias
        """
        # Set up backprop all-reduce.
        if self.input_is_parallel:
            input_parallel = input_
        else:
            input_parallel = scatter_to_tensor_model_parallel_region(input_)

        # Matrix multiply.
        with self._linear_timer:
            output_parallel = F.linear(input_parallel, self.weight)

        if self.reduce_results and self.world_size > 1:
            with self._communication_timer:
                output_ = reduce_from_tensor_model_parallel_region(output_parallel)
        else:
            output_ = output_parallel

        if not self.skip_bias_add:
            output = output_ + self.bias if self.bias is not None else output_
            output_bias = None
        else:
            output = output_
            output_bias = self.bias
        return output

    def weight_loader(self, param, param_name, loaded_weight, tp_rank):
        shard_size = param.shape[1]
        start_idx = tp_rank * shard_size
        end_idx = (tp_rank + 1) * shard_size
        loaded_weight = loaded_weight[:, start_idx:end_idx]
        loaded_weight = convert_pyslice_to_tensor(loaded_weight)
        assert param.shape == loaded_weight.shape, (
            f"{param_name} shape mismatch between model and checkpoint: "
            f"{param.shape} != {loaded_weight.shape}"
        )
        param.data.copy_(loaded_weight)


class ReplicatedLinear(torch.nn.Module):
    """Replicated linear layer.

    Args:
        input_size: input dimension of the linear layer.
        output_size: output dimension of the linear layer.
        bias: If true, add bias.
        skip_bias_add: If true, skip adding bias but instead return it.
        params_dtype: Data type for the parameters.
    """

    def __init__(
        self,
        input_size: int,
        output_size: int,
        bias: bool = True,
        skip_bias_add: bool = False,
        params_dtype: Optional[torch.dtype] = None,
        metric_op: Optional[MetricType] = None,
        layer_id: Optional[int] = None,
    ):
        super(ReplicatedLinear, self).__init__()

        # Keep input parameters
        self.input_size = input_size
        self.output_size = output_size
        self.skip_bias_add = skip_bias_add
        if params_dtype is None:
            params_dtype = torch.get_default_dtype()
        self.create_weights(params_dtype)

        if bias:
            self.bias = Parameter(
                torch.empty(
                    self.output_size,
                    device=torch.cuda.current_device(),
                    dtype=params_dtype,
                )
            )

            # Always initialize bias to zero
            with torch.no_grad():
                self.bias.zero_()
        else:
            self.register_parameter("bias", None)

        self._timer = CudaTimer(metric_op, layer_id=layer_id)

    def create_weights(self, dtype: torch.dtype) -> None:
        self.weight = Parameter(
            torch.empty(
                self.output_size,
                self.input_size,
                device=torch.cuda.current_device(),
                dtype=dtype,
            )
        )

    def forward(
        self, x: torch.Tensor
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Parameter]]:
        # Matrix multiply.
        with self._timer:
            output = F.linear(x, self.weight)

        if not self.skip_bias_add:
            if self.bias is not None:
                output = output + self.bias
            return output
        else:
            return output, self.bias
