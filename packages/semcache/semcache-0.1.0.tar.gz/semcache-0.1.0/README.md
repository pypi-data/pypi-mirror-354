# Semcache Python SDK

A Python client library for [Semcache](https://github.com/sensoris/semcache)

## Installation

```bash
pip install semcache
```

## Quick Start

```python
from semcache import Semcache

# Initialize the client
client = Semcache(base_url="http://localhost:8080")

# Store a key-data pair
client.put("What is the capital of France?", "Paris")

# Retrieve data by semantic similarity
response = client.get("What's the capital city of France?")
print(response)  # "Paris"
```

The above snippet requires a running Semcache server. You can start one using Docker:

```bash
docker run -p 8080:8080 ghcr.io/sensoris/semcache:latest
````

## Configuration

```python
client = Semcache(
    base_url="http://localhost:8080",  # Semcache server URL
    timeout=30,                         # Request timeout in seconds
)
```

## Usage Examples

### Basic Usage

```python
from semcache import Semcache

# Create a client instance
client = Semcache()

# Store some key-data pairs
client.put("What is Python?", "Python is a high-level programming language")
client.put("What is machine learning?", "Machine learning is a subset of AI that enables systems to learn from data")

# Retrieve data - exact match not required
response = client.get("Tell me about Python")
print(response)  # "Python is a high-level programming language"
```

### Error Handling

```python
from semcache import Semcache, SemcacheConnectionError, SemcacheTimeoutError

client = Semcache(base_url="http://localhost:8080", timeout=5)

try:
    client.put("test query", "test response")
except SemcacheConnectionError:
    print("Failed to connect to Semcache server")
except SemcacheTimeoutError:
    print("Request timed out")
```

## API Reference

### `Semcache(base_url="http://localhost:8080", timeout=30)`

Initialize a new Semcache client.

**Parameters:**
- `base_url` (str): The base URL of the Semcache server
- `timeout` (int): Request timeout in seconds

### `put(key: str, data: str) -> None`

Store a key-data pair in the cache.

**Parameters:**
- `key` (str): The key/query to cache
- `data` (str): The data/response to cache

**Raises:**
- `SemcacheError`: If the request fails

### `get(key: str) -> Optional[str]`

Retrieve cached data for a key using semantic similarity.

**Parameters:**
- `key` (str): The key/query to look up

**Returns:**
- `Optional[str]`: The cached data if found, None otherwise

**Raises:**
- `SemcacheError`: If the request fails

## Exceptions

- `SemcacheError`: Base exception for all Semcache errors
- `SemcacheConnectionError`: Raised when unable to connect to the server
- `SemcacheTimeoutError`: Raised when a request times out
- `SemcacheAPIError`: Raised when the API returns an error response

## Development

### Setup Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black src tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.