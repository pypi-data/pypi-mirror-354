"""
Integration tests for Semcache client.

These tests require a running Semcache server at http://localhost:8080.
Run with: pytest tests/test_integration.py -v -s
"""

import time

import pytest

from semcache import Semcache, SemcacheConnectionError


class TestSemcacheIntegration:
    @pytest.fixture
    def client(self):
        client = Semcache(base_url="http://localhost:8080")
        yield client
        client.close()

    @pytest.fixture(autouse=True)
    def check_server_available(self, client):
        """Skip tests if Semcache server is not available."""
        try:
            # Try a simple operation to check if server is running
            # This should return None or a string, but not raise ConnectionError
            _ = client.get("test")
        except SemcacheConnectionError:
            pytest.skip("Semcache server not available at http://localhost:8080")

    def test_put_and_get(self, client):
        client.put("What is Python?", "Python is a programming language")

        time.sleep(0.1)

        result = client.get("What is Python?")
        assert result == "Python is a programming language"

    def test_semantic_similarity(self, client):
        client.put("What is the capital of France?", "Paris is the capital of France")

        time.sleep(0.1)

        # Try similar keys
        similar_keys = [
            "What's the capital city of France?",
            "Tell me the capital of France",
            "France's capital is?",
        ]

        for key in similar_keys:
            result = client.get(key)
            assert result == "Paris is the capital of France", f"Failed for key: {key}"

    def test_get_nonexistent(self, client):
        result = client.get("This key definitely doesn't exist in the cache")
        assert result is None

    def test_overwrite_value(self, client):
        client.put("test key", "initial value")
        time.sleep(0.1)

        client.put("test key", "updated value")
        time.sleep(0.1)

        # Verify new value is returned
        result = client.get("test key")
        assert result == "updated value"

    def test_unicode_content(self, client):
        unicode_key = "What is café?"
        unicode_data = "Café is coffee in French ☕"

        client.put(unicode_key, unicode_data)
        time.sleep(0.1)

        result = client.get(unicode_key)
        assert result == unicode_data

    def test_large_content(self, client):
        large_data = "x" * 10000  # 10KB of text

        client.put("large content test", large_data)
        time.sleep(0.1)

        result = client.get("large content test")
        assert result == large_data
        assert len(result) == 10000
