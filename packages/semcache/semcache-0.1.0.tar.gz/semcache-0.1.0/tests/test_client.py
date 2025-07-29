"""
Tests for the Semcache client.
"""

from unittest.mock import Mock, patch

import pytest
import requests

from semcache import (
    Semcache,
    SemcacheConnectionError,
    SemcacheTimeoutError,
    SemcacheAPIError,
)


class TestSemcache:
    """Test cases for the Semcache client."""

    def test_initialization_default(self):
        """Test client initialization with default values."""
        client = Semcache()
        assert client.base_url == "http://localhost:8080"
        assert client.timeout == 30

    def test_initialization_custom(self):
        """Test client initialization with custom values."""
        client = Semcache(base_url="http://example.com:9090", timeout=60)
        assert client.base_url == "http://example.com:9090"
        assert client.timeout == 60

    def test_base_url_trailing_slash(self):
        """Test that trailing slashes are removed from base URL."""
        client = Semcache(base_url="http://localhost:8080/")
        assert client.base_url == "http://localhost:8080"

    @patch("semcache.client.requests.Session")
    def test_put_success(self, mock_session_class):
        """Test successful put operation."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_session.put.return_value = mock_response

        # Test
        client = Semcache()
        client.put("test key", "test data")

        # Verify
        mock_session.put.assert_called_once_with(
            "http://localhost:8080/semcache/v1/put",
            json={"key": "test key", "data": "test data"},
            timeout=30,
        )

    @patch("semcache.client.requests.Session")
    def test_get_success(self, mock_session_class):
        """Test successful get operation."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.text = "test data"
        mock_session.post.return_value = mock_response

        # Test
        client = Semcache()
        result = client.get("test key")

        # Verify
        assert result == "test data"
        mock_session.post.assert_called_once_with(
            "http://localhost:8080/semcache/v1/get",
            json={"key": "test key"},
            timeout=30,
        )

    @patch("semcache.client.requests.Session")
    def test_get_not_found(self, mock_session_class):
        """Test get operation when item is not found (404)."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = 404
        mock_session.post.return_value = mock_response

        # Test
        client = Semcache()
        result = client.get("test key")

        # Verify
        assert result is None

    @patch("semcache.client.requests.Session")
    def test_connection_error(self, mock_session_class):
        """Test connection error handling."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.put.side_effect = requests.exceptions.ConnectionError()

        # Test
        client = Semcache()
        with pytest.raises(SemcacheConnectionError) as exc_info:
            client.put("test", "test")

        assert "Failed to connect to Semcache server" in str(exc_info.value)

    @patch("semcache.client.requests.Session")
    def test_timeout_error(self, mock_session_class):
        """Test timeout error handling."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.post.side_effect = requests.exceptions.Timeout()

        # Test
        client = Semcache()
        with pytest.raises(SemcacheTimeoutError) as exc_info:
            client.get("test")

        assert "Request timed out after 30 seconds" in str(exc_info.value)

    @patch("semcache.client.requests.Session")
    def test_http_error(self, mock_session_class):
        """Test HTTP error handling."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_session.put.return_value = mock_response

        # Test
        client = Semcache()
        with pytest.raises(SemcacheAPIError) as exc_info:
            client.put("test", "test")

        assert "HTTP 400: Bad Request" in str(exc_info.value)

    def test_context_manager(self):
        """Test context manager functionality."""
        with patch("semcache.client.requests.Session") as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session

            with Semcache() as client:
                assert isinstance(client, Semcache)

            mock_session.close.assert_called_once()

    def test_close_method(self):
        """Test close method."""
        with patch("semcache.client.requests.Session") as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session

            client = Semcache()
            client.close()

            mock_session.close.assert_called_once()
