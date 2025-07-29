# BlackSheep Request Logger

[![PyPI version](https://badge.fury.io/py/blacksheep-request-logger.svg)](https://badge.fury.io/py/blacksheep-request-logger)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Efficient request logging middleware for [BlackSheep](https://github.com/Neoteroi/BlackSheep) web framework.

## Features

- 🚀 **High Performance**: Minimal overhead with pre-computed configurations
- 🔒 **Security**: Automatic redaction of sensitive headers (Authorization, Cookie, etc.)
- ⚙️ **Configurable**: Customize log levels, headers, and output format
- 📝 **Clean Logs**: Structured request/response logging with duration tracking
- 🐍 **Type Safe**: Full type hints and mypy support

## Installation

```bash
# With UV (recommended)
uv add blacksheep-request-logger

# With pip
pip install blacksheep-request-logger
```

## Quick Start

```python
from blacksheep import Application
from blacksheep_request_logger import RequestLoggingMiddleware

app = Application()

# Add the middleware
app.middlewares.append(RequestLoggingMiddleware(debug_mode=True))

# Your routes here...
```

## Configuration

### Basic Usage

```python
from blacksheep_request_logger import RequestLoggingMiddleware
import logging

# Simple usage with debug mode
middleware = RequestLoggingMiddleware(debug_mode=True)

# Custom logger
logger = logging.getLogger("my_app.requests")
middleware = RequestLoggingMiddleware(logger=logger, debug_mode=True)
```

### Advanced Configuration

```python
middleware = RequestLoggingMiddleware(
    debug_mode=True,
    headers_to_log=["Accept", "Content-Type", "User-Agent", "X-Custom-Header"],
    sensitive_headers={"authorization", "x-api-key", "cookie"},
    log_level_request=logging.INFO,
    log_level_response=logging.INFO,
    log_level_error=logging.ERROR,
    log_level_headers=logging.DEBUG,
)
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `logger` | `logging.Logger` | `None` | Custom logger instance |
| `debug_mode` | `bool` | `False` | Enable header logging |
| `headers_to_log` | `List[str]` | Common headers | Headers to log in debug mode |
| `sensitive_headers` | `Set[str]` | Auth headers | Headers to redact |
| `log_level_request` | `int` | `INFO` | Log level for requests |
| `log_level_response` | `int` | `INFO` | Log level for responses |
| `log_level_error` | `int` | `ERROR` | Log level for errors |
| `log_level_headers` | `int` | `DEBUG` | Log level for headers |

## Log Output

### Normal Mode (Always logged)
```
→ GET /api/users
← GET /api/users - 200 (0.045s)
```

### Debug Mode (Additional headers)
```
→ GET /api/users
  Headers: {
    "Accept": "application/json",
    "User-Agent": "curl/7.68.0",
    "Authorization": "[REDACTED]"
  }
← GET /api/users - 200 (0.045s)
```

## Integration Examples

### With Environment-Based Configuration

```python
import os
from blacksheep import Application
from blacksheep_request_logger import RequestLoggingMiddleware

app = Application()

# Enable debug mode based on environment
debug_mode = os.getenv("APP_ENV") == "development"

app.middlewares.append(
    RequestLoggingMiddleware(debug_mode=debug_mode)
)
```

### With Custom Logger Configuration

```python
import logging
from blacksheep import Application
from blacksheep_request_logger import RequestLoggingMiddleware

# Configure custom logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

request_logger = logging.getLogger("myapp.requests")
app = Application()

app.middlewares.append(
    RequestLoggingMiddleware(
        logger=request_logger,
        debug_mode=True
    )
)
```

### Production Configuration

```python
from blacksheep_request_logger import RequestLoggingMiddleware

# Production-optimized setup
middleware = RequestLoggingMiddleware(
    debug_mode=False,  # No header logging
    log_level_request=logging.INFO,
    log_level_response=logging.WARNING,  # Only log slow requests
    sensitive_headers={
        "authorization", "cookie", "x-api-key", 
        "x-auth-token", "session-id"
    }
)
```

## Security

The middleware automatically redacts sensitive headers:
- `Authorization`
- `Cookie` 
- `X-API-Key`
- `X-Auth-Token`

You can customize this by passing your own `sensitive_headers` set.

## Performance

This middleware is designed for high performance:
- Pre-computed header lists
- Minimal memory allocations
- No regular expressions
- Efficient string formatting
- No request body reading

Typical overhead: **< 0.1ms per request**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

```bash
# Clone the repository
git clone https://github.com/kinsyudev/blacksheep-request-logger.git
cd blacksheep-request-logger

# Install with UV (recommended)
uv sync --dev

# Or install with pip
pip install -e ".[dev]"

# Run tests
uv run pytest
# or: pytest

# Format and lint code
uv run ruff format .
uv run ruff check --fix .

# Type checking
uv run mypy src/
# or: mypy src/
```

### Quick Development Commands

For convenience, you can use the provided Makefile:

```bash
# Install dependencies
make install

# Run tests
make test

# Format code
make format

# Run all checks (lint, format check, type check)
make check

# Build package
make build

# Clean build artifacts
make clean
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0
- Initial release
- Efficient request/response logging
- Configurable debug mode with header logging
- Automatic sensitive header redaction
- Full type hint support 