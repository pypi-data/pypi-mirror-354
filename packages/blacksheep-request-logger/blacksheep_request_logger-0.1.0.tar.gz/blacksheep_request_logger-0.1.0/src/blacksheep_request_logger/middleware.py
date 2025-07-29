"""
Request logging middleware for BlackSheep web framework.

This middleware provides efficient HTTP request logging with configurable detail levels.
"""

import json
import logging
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Tuple, Union

from blacksheep import Request, Response


class RequestLoggingMiddleware:
    """
    Efficient request logging middleware for BlackSheep.

    Always logs:
    - HTTP method
    - Request URL
    - Response status code
    - Request duration

    In debug mode also logs:
    - Request headers (configurable set)

    Args:
        logger: Logger instance to use (defaults to module logger)
        debug_mode: Enable debug logging (defaults to False)
        headers_to_log: Headers to log in debug mode (defaults to common headers)
        sensitive_headers: Headers to redact (defaults to auth-related headers)
        log_level_request: Log level for request info (defaults to INFO)
        log_level_response: Log level for response info (defaults to INFO)
        log_level_error: Log level for errors (defaults to ERROR)
        log_level_headers: Log level for headers in debug mode (defaults to DEBUG)
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        debug_mode: bool = False,
        headers_to_log: Optional[List[Union[str, bytes]]] = None,
        sensitive_headers: Optional[Set[str]] = None,
        log_level_request: int = logging.INFO,
        log_level_response: int = logging.INFO,
        log_level_error: int = logging.ERROR,
        log_level_headers: int = logging.DEBUG,
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.debug_mode = debug_mode
        self.log_level_request = log_level_request
        self.log_level_response = log_level_response
        self.log_level_error = log_level_error
        self.log_level_headers = log_level_headers

        # Default headers to log
        default_headers = [
            "Accept",
            "Accept-Encoding",
            "Authorization",
            "Content-Type",
            "Content-Length",
            "User-Agent",
            "Host",
            "Referer",
            "Cookie",
            "X-API-Key",
            "X-Requested-With",
        ]

        # Convert headers to (bytes, str) tuples for efficiency
        self.headers_to_log: List[Tuple[bytes, str]] = []
        headers_list = headers_to_log or default_headers

        for header in headers_list:
            if isinstance(header, str):
                self.headers_to_log.append((header.encode("utf-8"), header))
            elif isinstance(header, bytes):
                self.headers_to_log.append((header, header.decode("utf-8")))
            else:
                raise ValueError(f"Invalid header type: {type(header)}")

        # Default sensitive headers
        default_sensitive = {"authorization", "cookie", "x-api-key", "x-auth-token"}
        self.sensitive_headers = sensitive_headers or default_sensitive

    async def __call__(
        self, request: Request, handler: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request and log details."""
        start_time = time.time()

        # Log basic request info
        self.logger.log(self.log_level_request, "→ %s %s", request.method, request.url)

        # Log headers in debug mode
        if self.debug_mode:
            self._log_request_headers(request)

        try:
            # Process the request
            response = await handler(request)

            # Calculate request duration
            duration = time.time() - start_time

            # Log response info
            self.logger.log(
                self.log_level_response,
                "← %s %s - %s (%.3fs)",
                request.method,
                request.url,
                response.status,
                duration,
            )

            return response

        except Exception as e:
            # Log errors
            duration = time.time() - start_time
            self.logger.log(
                self.log_level_error,
                "← %s %s - ERROR: %s (%.3fs)",
                request.method,
                request.url,
                str(e),
                duration,
            )
            # Re-raise the exception to maintain proper error handling
            raise

    def _log_request_headers(self, request: Request) -> None:
        """Log request headers efficiently."""
        headers_dict: Dict[str, str] = {}

        # Check each configured header
        for header_bytes, header_name in self.headers_to_log:
            try:
                header_value = request.headers.get_first(header_bytes)
                if header_value:
                    value = (
                        header_value.decode("utf-8")
                        if isinstance(header_value, bytes)
                        else str(header_value)
                    )

                    # Redact sensitive headers
                    if header_name.lower() in self.sensitive_headers:
                        headers_dict[header_name] = "[REDACTED]"
                    else:
                        headers_dict[header_name] = value
            except Exception as e:
                # Skip if header access fails, log at debug level
                self.logger.debug("Failed to access header %s: %s", header_name, e)
                continue

        if headers_dict:
            self.logger.log(
                self.log_level_headers,
                "  Headers: %s",
                json.dumps(headers_dict, indent=2),
            )


def create_request_logging_middleware(
    logger: Optional[logging.Logger] = None, debug_mode: bool = False, **kwargs: Any
) -> RequestLoggingMiddleware:
    """
    Create and configure the request logging middleware.

    Args:
        logger: Logger instance to use
        debug_mode: Enable debug logging
        **kwargs: Additional arguments passed to RequestLoggingMiddleware

    Returns:
        Configured RequestLoggingMiddleware instance
    """
    return RequestLoggingMiddleware(logger=logger, debug_mode=debug_mode, **kwargs)
