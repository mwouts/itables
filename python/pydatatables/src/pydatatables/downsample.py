"""Downsampling functions - these now live in itables_core.downsample"""

from itables_core.downsample import (
    as_nbytes,
    downsample,
    nbytes,
    shrink_towards_target_aspect_ratio,
)

__all__ = [
    "as_nbytes",
    "downsample",
    "nbytes",
    "shrink_towards_target_aspect_ratio",
]
