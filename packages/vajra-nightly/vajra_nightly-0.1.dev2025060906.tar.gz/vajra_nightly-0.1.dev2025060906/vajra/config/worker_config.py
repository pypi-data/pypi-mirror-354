from dataclasses import field

from vajra._native.configs import WorkerConfig as WorkerConfig_C
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class WorkerConfig:
    """Configuration for worker processes that execute model inference.

    Workers are the execution units that run model computations on GPUs.
    This configuration controls resource allocation and execution backend
    settings for each worker process.

    The gpu_memory_utilization parameter is crucial for balancing between
    maximizing memory for KV cache and leaving headroom for dynamic allocations
    for other libraries during inference. A value of 0.85 (85%) is typically safe
    for most workloads while preventing OOM errors.

    Attributes:
        gpu_memory_utilization: Fraction of GPU memory to allocate for model
                               and KV cache (0.0 to 1.0). The remaining memory
                               is reserved for activation tensors and other
                               dynamic allocations. Default is 0.85 (85%).
        use_native_execution_backend: Whether to use the optimized C++ backend
                                     for model execution. The native backend
                                     provides better performance but may have
                                     limited model support. Default is True.

    Example:
        >>> worker_config = WorkerConfig(
        ...     gpu_memory_utilization=0.9,
        ...     use_native_execution_backend=True
        ... )

    Raises:
        ValueError: If gpu_memory_utilization is not between 0.0 and 1.0.
    """

    gpu_memory_utilization: float = field(
        default=0.85, metadata={"help": "GPU memory utilization fraction (0.0 to 1.0)."}
    )
    use_native_execution_backend: bool = field(
        default=True,
        metadata={"help": "Use native execution backend for the replica."},
    )

    def __post_init__(self):
        self._verify_args()
        # Create native handler
        self.native_handle = WorkerConfig_C(
            self.gpu_memory_utilization,
            self.use_native_execution_backend,
        )

    def _verify_args(self) -> None:
        if not (0.0 <= self.gpu_memory_utilization <= 1.0):
            raise ValueError(
                f"GPU memory utilization ({self.gpu_memory_utilization}) must be "
                "between 0.0 and 1.0."
            )
