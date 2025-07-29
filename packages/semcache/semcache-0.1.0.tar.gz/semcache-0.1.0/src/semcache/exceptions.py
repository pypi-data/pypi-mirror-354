"""
Custom exceptions for the Semcache Python SDK.
"""


class SemcacheError(Exception):
    """Base exception for all Semcache errors."""

    pass


class SemcacheConnectionError(SemcacheError):
    """Raised when unable to connect to the Semcache server."""

    pass


class SemcacheTimeoutError(SemcacheError):
    """Raised when a request to the Semcache server times out."""

    pass


class SemcacheAPIError(SemcacheError):
    """Raised when the Semcache API returns an error response."""

    pass
