"""
Utilities package for rapid framework
"""

# JSON utilities with performance tracking
from .json import (
    clear_performance_stats,
    dumps,
    dumps_bytes,
    get_performance_stats,
    loads,
)

# Memory pools available but not auto-imported to avoid circular imports
# Use: from rapid.utils.memory import RequestPool, ResponsePool

__all__ = [
    "dumps",
    "dumps_bytes",
    "loads",
    "get_performance_stats",
    "clear_performance_stats",
]
