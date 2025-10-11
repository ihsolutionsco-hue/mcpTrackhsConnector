"""
Core modules for TrackHS MCP Connector

Contiene el cliente API, autenticación y tipos base.
"""

from .api_client import TrackHSApiClient
from .auth import TrackHSAuth
from .types import (
    ApiError,
    PaginationParams,
    RequestOptions,
    SearchParams,
    TrackHSConfig,
    TrackHSResponse,
)

__all__ = [
    "TrackHSApiClient",
    "TrackHSAuth",
    "TrackHSConfig",
    "RequestOptions",
    "ApiError",
    "PaginationParams",
    "SearchParams",
    "TrackHSResponse",
]
