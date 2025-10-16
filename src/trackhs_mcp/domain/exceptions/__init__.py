"""
Excepciones del dominio
"""

from .api_exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ErrorSeverity,
    NetworkError,
    ServerError,
    TimeoutError,
    TrackHSError,
    ValidationError,
)

__all__ = [
    "TrackHSError",
    "ApiError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NetworkError",
    "TimeoutError",
    "ServerError",
    "ErrorSeverity",
]
