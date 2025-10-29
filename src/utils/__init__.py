"""
Utilidades comunes para TrackHS MCP Server
"""

from .api_client import TrackHSAPIClient
from .exceptions import (
    TrackHSAPIError,
    TrackHSAuthenticationError,
    TrackHSAuthorizationError,
    TrackHSError,
    TrackHSNotFoundError,
    TrackHSValidationError,
)
from .logger import get_logger
from .validators import validate_date_range, validate_pagination_params

__all__ = [
    # Exceptions
    "TrackHSError",
    "TrackHSAuthenticationError",
    "TrackHSAuthorizationError",
    "TrackHSNotFoundError",
    "TrackHSValidationError",
    "TrackHSAPIError",
    # Logger
    "get_logger",
    # API Client
    "TrackHSAPIClient",
    # Validators
    "validate_date_range",
    "validate_pagination_params",
]
