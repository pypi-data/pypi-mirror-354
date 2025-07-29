from dataclasses import field

from vajra._native.configs import CacheConfig as CacheConfig_C
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class CacheConfig:
    """Configuration for the KV cache used in attention mechanisms.

    The cache is divided into fixed-size blocks, where each block can store
    a certain number of tokens' key-value pairs. This block-based approach
    allows for efficient memory management and allocation.

    Attributes:
        block_size: Number of tokens that can be stored in each cache block.
                   Larger blocks may improve memory locality but can lead to
                   internal fragmentation. Default is 16 tokens per block.

    Example:
        >>> cache_config = CacheConfig(block_size=32)
        >>> print(cache_config.block_size)
        32
    """

    block_size: int = field(
        default=16, metadata={"help": "Size of a cache block in number of tokens."}
    )

    def __post_init__(self):
        # Create native handler
        self.native_handle = CacheConfig_C(
            self.block_size,
        )
