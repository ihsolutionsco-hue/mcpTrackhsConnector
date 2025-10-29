"""
Excepciones personalizadas para TrackHS MCP Server
"""

from typing import Any, Dict, Optional


class TrackHSError(Exception):
    """Excepción base para errores de TrackHS"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class TrackHSAuthenticationError(TrackHSError):
    """Error de autenticación con TrackHS API"""

    def __init__(self, message: str = "Error de autenticación con TrackHS API"):
        super().__init__(message, "AUTH_ERROR")


class TrackHSAuthorizationError(TrackHSError):
    """Error de autorización con TrackHS API"""

    def __init__(self, message: str = "Error de autorización con TrackHS API"):
        super().__init__(message, "AUTHZ_ERROR")


class TrackHSNotFoundError(TrackHSError):
    """Recurso no encontrado en TrackHS"""

    def __init__(self, resource: str, resource_id: Any):
        message = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(
            message, "NOT_FOUND", {"resource": resource, "resource_id": resource_id}
        )


class TrackHSValidationError(TrackHSError):
    """Error de validación de datos"""

    def __init__(self, field: str, value: Any, message: str):
        super().__init__(
            f"Error de validación en campo '{field}': {message}",
            "VALIDATION_ERROR",
            {"field": field, "value": str(value), "validation_message": message},
        )


class TrackHSAPIError(TrackHSError):
    """Error de comunicación con TrackHS API"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message,
            "API_ERROR",
            {"status_code": status_code, "response_data": response_data},
        )
