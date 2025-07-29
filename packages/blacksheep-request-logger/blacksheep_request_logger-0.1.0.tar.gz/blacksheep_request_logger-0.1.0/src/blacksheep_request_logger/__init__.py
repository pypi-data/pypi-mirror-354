"""
BlackSheep Request Logger

Efficient request logging middleware for BlackSheep web framework.
"""

__version__ = "0.1.0"

from .middleware import RequestLoggingMiddleware

__all__ = ["RequestLoggingMiddleware"]
