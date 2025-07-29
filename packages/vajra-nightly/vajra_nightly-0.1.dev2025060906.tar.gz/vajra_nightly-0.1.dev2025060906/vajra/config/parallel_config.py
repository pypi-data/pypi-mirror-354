from dataclasses import field

from vajra._native.configs import ParallelConfig as ParallelConfig_C
from vajra.logger import init_logger
from vajra.utils.dataclasses import frozen_dataclass

logger = init_logger(__name__)


@frozen_dataclass
class ParallelConfig:
    """Configuration for distributed parallelism strategies.

    This class defines the parallelism configuration for distributed inference,
    supporting multiple parallelism strategies that can be combined:

    - **Pipeline Parallelism**: Splits the model layers across devices
    - **Tensor Parallelism**: Splits individual layers/tensors across devices
    - **Expert Parallelism**: Distributes MoE experts across devices
    - **KV Parallelism**: Distributes key-value cache across devices

    The total world size is computed as:
    pipeline_parallel_size × tensor_parallel_size × kv_parallel_size

    Attributes:
        pipeline_parallel_size: Number of pipeline stages. Model layers are
                               evenly distributed across stages.
        tensor_parallel_size: Number of devices for tensor parallelism.
                             Attention heads and FFN are split across devices.
        enable_expert_parallel: Enable expert parallelism for MoE models.
        enable_sequence_pipeline_parallel: Enable sequence-level pipeline
                                          parallelism for better throughput.
        enable_chunked_pipeline_comm_opt: Enable communication optimization
                                         for pipeline parallelism with chunking.
        kv_parallel_size: Number of devices for KV cache parallelism.
        max_num_tokens_per_kvp_group: Maximum tokens per KV parallel group.
                                     0 means no limit.

    Example:
        >>> parallel_config = ParallelConfig(
        ...     pipeline_parallel_size=2,
        ...     tensor_parallel_size=4
        ... )
        >>> print(parallel_config.world_size)
        8
    """

    pipeline_parallel_size: int = field(
        default=1, metadata={"help": "Number of pipeline parallel groups."}
    )
    tensor_parallel_size: int = field(
        default=1, metadata={"help": "Number of tensor parallel groups."}
    )
    enable_expert_parallel: bool = field(
        default=False, metadata={"help": "Enable expert parallelism."}
    )
    enable_sequence_pipeline_parallel: bool = field(
        default=False, metadata={"help": "Enable sequence pipeline parallelism."}
    )
    enable_chunked_pipeline_comm_opt: bool = field(
        default=False,
        metadata={"help": "Enable chunked pipeline communication optimization."},
    )
    kv_parallel_size: int = field(
        default=1, metadata={"help": "Number of KV parallel groups."}
    )
    max_num_tokens_per_kvp_group: int = field(
        default=0,
        metadata={
            "help": "Maximum number of tokens per KV parallel group. 0 means no limit."
        },
    )

    def __post_init__(self):
        if self.enable_sequence_pipeline_parallel and self.pipeline_parallel_size == 1:
            logger.warning(
                "Sequence pipeline parallelism is enabled but pipeline_parallel_size is 1."
            )
            self.enable_sequence_pipeline_parallel = False

        if self.enable_chunked_pipeline_comm_opt and not (
            self.pipeline_parallel_size > 1 and self.tensor_parallel_size > 1
        ):
            logger.warning(
                "Chunked pipeline communication optimization is enabled but pipeline_parallel_size "
                "or tensor_parallel_size is not greater than 1."
            )
            self.enable_chunked_pipeline_comm_opt = False

        self.world_size = (
            self.pipeline_parallel_size
            * self.tensor_parallel_size
            * self.kv_parallel_size
        )

        self.native_handle = ParallelConfig_C(
            self.pipeline_parallel_size,
            self.tensor_parallel_size,
            self.enable_expert_parallel,
            self.enable_sequence_pipeline_parallel,
            self.enable_chunked_pipeline_comm_opt,
            self.kv_parallel_size,
            self.max_num_tokens_per_kvp_group,
        )
