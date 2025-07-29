"""
Tests for the BlackSheep request logging middleware.
"""

import logging
from io import StringIO
from typing import Dict, Optional
from unittest.mock import AsyncMock, Mock

import pytest
from blacksheep import Headers, Request

from blacksheep_request_logger import RequestLoggingMiddleware


def create_mock_request(
    method: str = "GET", url: str = "/test", headers: Optional[Dict[str, str]] = None
):
    """Create a mock request for testing."""
    mock_request = Mock(spec=Request)
    mock_request.method = method
    mock_request.url = url
    mock_request.headers = Headers()

    # Add headers if provided
    if headers:
        for name, value in headers.items():
            mock_request.headers.add(name.encode(), value.encode())

    return mock_request


class MockResponse:
    """Mock response for testing."""

    def __init__(self, status: int = 200):
        self.status = status


@pytest.fixture
def log_stream():
    """Create a string stream to capture log output."""
    return StringIO()


@pytest.fixture
def test_logger(log_stream):
    """Create a test logger that writes to the stream."""
    logger = logging.getLogger("test_middleware")
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add stream handler
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


@pytest.fixture
def mock_handler():
    """Create a mock async handler."""
    handler = AsyncMock()
    handler.return_value = MockResponse(200)
    return handler


class TestRequestLoggingMiddleware:
    """Test cases for RequestLoggingMiddleware."""

    async def test_basic_request_logging(self, test_logger, log_stream, mock_handler):
        """Test basic request/response logging."""
        middleware = RequestLoggingMiddleware(logger=test_logger)
        request = create_mock_request("GET", "/api/users")

        response = await middleware(request, mock_handler)

        assert response.status == 200
        mock_handler.assert_called_once_with(request)

        log_output = log_stream.getvalue()
        assert "→ GET /api/users" in log_output
        assert "← GET /api/users - 200" in log_output
        assert "s)" in log_output  # Duration should be logged

    async def test_debug_mode_headers(self, test_logger, log_stream, mock_handler):
        """Test header logging in debug mode."""
        middleware = RequestLoggingMiddleware(
            logger=test_logger,
            debug_mode=True,
            headers_to_log=["Content-Type", "User-Agent"],
        )

        request = create_mock_request(
            "POST",
            "/api/data",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "test-client/1.0",
            },
        )

        await middleware(request, mock_handler)

        log_output = log_stream.getvalue()
        assert "Content-Type" in log_output
        assert "application/json" in log_output
        assert "User-Agent" in log_output
        assert "test-client/1.0" in log_output

    async def test_sensitive_header_redaction(
        self, test_logger, log_stream, mock_handler
    ):
        """Test that sensitive headers are redacted."""
        middleware = RequestLoggingMiddleware(
            logger=test_logger,
            debug_mode=True,
            headers_to_log=["Authorization", "Content-Type"],
            sensitive_headers={"authorization"},
        )

        request = create_mock_request(
            "GET",
            "/api/secret",
            headers={
                "Authorization": "Bearer secret-token",
                "Content-Type": "application/json",
            },
        )

        await middleware(request, mock_handler)

        log_output = log_stream.getvalue()
        assert "[REDACTED]" in log_output
        assert "secret-token" not in log_output
        assert "application/json" in log_output

    async def test_exception_handling(self, test_logger, log_stream):
        """Test error logging when handler raises exception."""
        middleware = RequestLoggingMiddleware(logger=test_logger)
        request = create_mock_request("POST", "/api/error")

        async def failing_handler(req):
            raise ValueError("Something went wrong")

        with pytest.raises(ValueError, match="Something went wrong"):
            await middleware(request, failing_handler)

        log_output = log_stream.getvalue()
        assert "→ POST /api/error" in log_output
        assert "ERROR: Something went wrong" in log_output
        assert "s)" in log_output  # Duration should be logged

    def test_custom_log_levels(self, test_logger, log_stream, mock_handler):
        """Test custom log levels configuration."""
        middleware = RequestLoggingMiddleware(
            logger=test_logger,
            log_level_request=logging.WARNING,
            log_level_response=logging.ERROR,
        )

        # Should not log anything at INFO level
        test_logger.setLevel(logging.ERROR)

        _request = create_mock_request("GET", "/test")
        # Note: We can't easily test async in non-async test, so this is a basic check
        assert middleware.log_level_request == logging.WARNING
        assert middleware.log_level_response == logging.ERROR

    def test_custom_headers_configuration(self):
        """Test custom headers configuration."""
        custom_headers = ["X-Custom", "X-Another"]
        middleware = RequestLoggingMiddleware(headers_to_log=custom_headers)  # type: ignore

        # Check that headers were converted to bytes/str tuples
        header_names = [header[1] for header in middleware.headers_to_log]
        assert "X-Custom" in header_names
        assert "X-Another" in header_names

    def test_bytes_headers_configuration(self):
        """Test configuration with bytes headers."""
        custom_headers = [b"X-Custom", b"X-Another"]
        middleware = RequestLoggingMiddleware(headers_to_log=custom_headers)  # type: ignore

        # Check that headers were converted properly
        header_names = [header[1] for header in middleware.headers_to_log]
        assert "X-Custom" in header_names
        assert "X-Another" in header_names

    def test_invalid_header_type(self):
        """Test that invalid header types raise ValueError."""
        with pytest.raises(ValueError, match="Invalid header type"):
            RequestLoggingMiddleware(headers_to_log=[123])  # type: ignore # Invalid type

    async def test_missing_headers(self, test_logger, log_stream, mock_handler):
        """Test behavior when requested headers are missing."""
        middleware = RequestLoggingMiddleware(
            logger=test_logger,
            debug_mode=True,
            headers_to_log=["Missing-Header", "Content-Type"],
        )

        request = create_mock_request(
            "GET", "/test", headers={"Content-Type": "text/plain"}
        )

        await middleware(request, mock_handler)

        log_output = log_stream.getvalue()
        # Should only log existing headers
        assert "Content-Type" in log_output
        assert "Missing-Header" not in log_output

    def test_default_configuration(self):
        """Test that default configuration is sensible."""
        middleware = RequestLoggingMiddleware()

        assert middleware.debug_mode is False
        assert middleware.log_level_request == logging.INFO
        assert middleware.log_level_response == logging.INFO
        assert middleware.log_level_error == logging.ERROR
        assert middleware.log_level_headers == logging.DEBUG

        # Check default sensitive headers
        assert "authorization" in middleware.sensitive_headers
        assert "cookie" in middleware.sensitive_headers
        assert "x-api-key" in middleware.sensitive_headers

        # Check default headers to log
        header_names = [header[1] for header in middleware.headers_to_log]
        assert "Content-Type" in header_names
        assert "User-Agent" in header_names
        assert "Authorization" in header_names
