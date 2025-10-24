"""
Middleware personalizado para TrackHS MCP Server
Implementa manejo de errores, logging estructurado y compactación de respuestas
"""

from .error_handling import TrackHSErrorHandlingMiddleware
from .logging import TrackHSLoggingMiddleware
from .response_compactor import (
    ResponseCompactor,
    compact_for_voice_agent,
    estimate_token_count,
    should_compact_response,
)

__all__ = [
    "TrackHSErrorHandlingMiddleware",
    "TrackHSLoggingMiddleware",
    "ResponseCompactor",
    "compact_for_voice_agent",
    "estimate_token_count",
    "should_compact_response",
]
