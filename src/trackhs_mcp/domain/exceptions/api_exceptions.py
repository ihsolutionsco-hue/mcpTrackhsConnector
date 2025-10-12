"""
Excepciones del dominio para la API
Siguiendo Clean Architecture - Domain Layer
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class ErrorSeverity(Enum):
    """Niveles de severidad de errores"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TrackHSError(Exception):
    """Error base para Track HS MCP Connector"""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.severity = severity
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)
        super().__init__(self.message)


class ApiError(TrackHSError):
    """Error relacionado con la API de Track HS"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        status_text: Optional[str] = None,
        **kwargs,
    ):
        context = kwargs.get("context", {})
        if status_code:
            context["status_code"] = status_code
        if endpoint:
            context["endpoint"] = endpoint

        # Agregar atributos para compatibilidad con tests
        self.status = status_code
        self.status_code = status_code
        self.status_text = status_text

        super().__init__(message, ErrorSeverity.HIGH, context)


class AuthenticationError(TrackHSError):
    """Error de autenticación"""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, ErrorSeverity.CRITICAL, kwargs.get("context", {}))


class ValidationError(TrackHSError):
    """Error de validación de parámetros"""

    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        context = kwargs.get("context", {})
        if field:
            context["field"] = field

        super().__init__(message, ErrorSeverity.MEDIUM, context)


class NetworkError(TrackHSError):
    """Error de red"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, ErrorSeverity.HIGH, kwargs.get("context", {}))


class TimeoutError(TrackHSError):
    """Error de timeout"""

    def __init__(self, message: str, timeout_seconds: Optional[float] = None, **kwargs):
        context = kwargs.get("context", {})
        if timeout_seconds:
            context["timeout_seconds"] = timeout_seconds

        super().__init__(message, ErrorSeverity.MEDIUM, context)
