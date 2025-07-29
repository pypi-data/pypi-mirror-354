from typing import Optional, Any

import requests

from .exceptions import (
    SemcacheError,
    SemcacheConnectionError,
    SemcacheTimeoutError,
    SemcacheAPIError,
)


class Semcache:
    """
    Client for interacting with the Semcache server.

    Args:
        base_url: The base URL of the Semcache server (default: "http://localhost:8080")
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> from semcache import Semcache
        >>> client = Semcache()
        >>> client.put("What is the capital of France?", "Paris")
        >>> result = client.get("What is the capital of France?")
        >>> print(result)
        Paris
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def put(self, key: str, data: str) -> None:
        """
        Store a key-data pair in the cache.

        Args:
            key: The key/prompt to cache
            data: The data/response to cache

        Raises:
            SemcacheError: If the request fails
        """
        url = f"{self.base_url}/semcache/v1/put"
        json_data = {"key": key, "data": data}

        try:
            response = self.session.put(url, json=json_data, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise SemcacheTimeoutError(
                f"Request timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError:
            raise SemcacheConnectionError(
                f"Failed to connect to Semcache server at {url}"
            )
        except requests.exceptions.HTTPError as e:
            raise SemcacheAPIError(f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            raise SemcacheError(f"Unexpected error: {str(e)}")

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a cached value for a key.

        Args:
            key: The key/prompt to look up

        Returns:
            The cached data if found, None if not found

        Raises:
            SemcacheError: If the request fails
        """
        url = f"{self.base_url}/semcache/v1/get"
        json_data = {"key": key}

        try:
            response = self.session.post(url, json=json_data, timeout=self.timeout)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return response.text

        except requests.exceptions.Timeout:
            raise SemcacheTimeoutError(
                f"Request timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError:
            raise SemcacheConnectionError(
                f"Failed to connect to Semcache server at {url}"
            )
        except requests.exceptions.HTTPError:
            raise SemcacheAPIError(f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            raise SemcacheError(f"Unexpected error: {str(e)}")

    def __enter__(self) -> "Semcache":
        """Context manager support."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Close session on context exit."""
        self.session.close()

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()
