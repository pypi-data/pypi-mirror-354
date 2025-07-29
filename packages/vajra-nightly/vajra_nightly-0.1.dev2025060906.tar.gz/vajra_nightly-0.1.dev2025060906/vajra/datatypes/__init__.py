from typing import Dict, List, Tuple

from vajra._native.datatypes import (
    BaseSequenceWithPriority,
    CommInfo,
    LogicalTokenBlock,
    PendingStepOutput,
    RequestOutput,
    SamplerOutput,
    SamplingParams,
    SamplingType,
    SchedulerOutput,
    Sequence,
    SequenceMetadata,
    SequenceParams,
    SequenceScheduleMetadata,
    SequenceState,
    SequenceStatus,
    StepInputs,
    StepMicrobatchOutputs,
    StepOutputs,
    UserSequenceParams,
)

# Type aliases for resource allocation and GPU management
GPULocation = Tuple[str, int]  # (node_ip, gpu_id)
"""Represents a GPU's location as a tuple of (node_ip, gpu_id).

Example: ("192.168.1.10", 0) represents GPU 0 on node 192.168.1.10
"""

ResourceMapping = List[GPULocation]
"""List of GPU locations assigned to a single replica.

For a replica with tensor parallelism across 4 GPUs, this might be:
[("node1", 0), ("node1", 1), ("node1", 2), ("node1", 3)]
"""

GlobalResourceMapping = Dict[str, ResourceMapping]
"""Maps replica IDs to their assigned GPU resources across the cluster.

Example:
{
    "replica_0": [("node1", 0), ("node1", 1)],
    "replica_1": [("node2", 0), ("node2", 1)]
}
"""

SamplerOutputs = List[SamplerOutput]
"""List of sampler outputs from a batch of sequences."""

ModelParallelRank = Tuple[int, int, int]
"""Represents a model's parallel rank as (pipeline_rank, tensor_rank, data_rank).

Used to identify a worker's position in the distributed model parallel setup.
"""


__all__ = [
    "LogicalTokenBlock",
    "CommInfo",
    "RequestOutput",
    "SamplerOutput",
    "SamplerOutputs",
    "SamplingParams",
    "SchedulerOutput",
    "SequenceScheduleMetadata",
    "SequenceState",
    "SequenceStatus",
    "Sequence",
    "BaseSequenceWithPriority",
    "StepInputs",
    "StepMicrobatchOutputs",
    "StepOutputs",
    "SamplingType",
    "GPULocation",
    "ResourceMapping",
    "GlobalResourceMapping",
    "SequenceMetadata",
    "SequenceParams",
    "UserSequenceParams",
    "ModelParallelRank",
    "SamplerOutputs",
    "StepOutputs",
    "StepMicrobatchOutputs",
    "StepInputs",
    "CommInfo",
    "PendingStepOutput",
]
