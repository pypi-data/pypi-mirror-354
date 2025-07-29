"""
Semcache Python SDK

A Python library for the Semcache API.
"""

from .client import Semcache
from .exceptions import (
    SemcacheError,
    SemcacheConnectionError,
    SemcacheTimeoutError,
    SemcacheAPIError,
)

__version__ = "0.1.0"
__all__ = [
    "Semcache",
    "SemcacheError",
    "SemcacheConnectionError",
    "SemcacheTimeoutError",
    "SemcacheAPIError",
]
