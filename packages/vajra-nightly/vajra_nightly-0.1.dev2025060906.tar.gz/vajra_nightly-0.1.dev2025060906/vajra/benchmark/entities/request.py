import logging
from typing import Tuple

from vajra.benchmark.entities.base_entity import BaseEntity

logger = logging.getLogger(__name__)


class Request(BaseEntity):
    """Represents a benchmark request for performance evaluation.

    A Request encapsulates the essential parameters of an inference request
    used in benchmarking scenarios. It tracks when the request arrived and
    the token counts for both prefill (prompt) and decode (generation) phases.

    This class is primarily used by the benchmark runner to simulate realistic
    workloads and measure system performance under various request patterns.

    Attributes:
        arrived_at: Timestamp when the request arrived (in seconds).
        num_prefill_tokens: Number of tokens in the prompt/prefill phase.
        num_decode_tokens: Number of tokens to generate in the decode phase.

    Properties:
        size: Tuple of (prefill_tokens, decode_tokens).
        pd_ratio: Prefill-to-decode ratio, useful for workload characterization.
        total_tokens: Sum of prefill and decode tokens.

    Example:
        >>> request = Request(
        ...     arrived_at=1234567890.5,
        ...     num_prefill_tokens=512,
        ...     num_decode_tokens=128
        ... )
        >>> print(request.pd_ratio)
        4.0
        >>> print(request.total_tokens)
        640
    """

    def __init__(
        self,
        arrived_at: float,
        num_prefill_tokens: int,
        num_decode_tokens: int,
    ):
        self._id = Request.generate_id()
        self._arrived_at = arrived_at
        self._num_prefill_tokens = num_prefill_tokens
        self._num_decode_tokens = num_decode_tokens
        assert num_prefill_tokens > 0
        assert num_decode_tokens > 0

    @property
    def size(self) -> Tuple[int, int]:
        return self._num_prefill_tokens, self._num_decode_tokens

    @property
    def arrived_at(self) -> float:
        return self._arrived_at

    @property
    def num_prefill_tokens(self) -> int:
        return self._num_prefill_tokens

    @property
    def num_decode_tokens(self) -> int:
        return self._num_decode_tokens

    @property
    def pd_ratio(self) -> float:
        return self._num_prefill_tokens / self._num_decode_tokens

    @property
    def total_tokens(self) -> int:
        return self._num_prefill_tokens + self._num_decode_tokens

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "arrived_at": self._arrived_at,
            "num_prefill_tokens": self._num_prefill_tokens,
            "num_decode_tokens": self._num_decode_tokens,
        }
