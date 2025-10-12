"""
Manejo de errores para Track HS MCP Connector
Infrastructure Layer - Utilidades para manejo de errores
"""

import functools
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Type

# Importar excepciones del dominio siguiendo Clean Architecture
from ...domain.exceptions.api_exceptions import (
    TrackHSError,
    ApiError,
    AuthenticationError,
    ValidationError,
    NetworkError,
    TimeoutError,
    ErrorSeverity,
)


class ErrorHandler:
    """Manejador de errores con logging y métricas"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self._error_counts: Dict[str, int] = {}

    def handle_error(self, error: TrackHSError, operation: str = "unknown"):
        """Maneja un error con logging y métricas"""
        # Incrementar contador de errores
        error_key = f"{operation}_{error.severity.value}"
        self._error_counts[error_key] = self._error_counts.get(error_key, 0) + 1

        # Log del error
        log_level = self._get_log_level(error.severity)
        self.logger.log(
            log_level,
            f"Error in {operation}: {error.message}",
            extra={
                "error_type": type(error).__name__,
                "severity": error.severity.value,
                "context": error.context,
                "timestamp": error.timestamp.isoformat(),
            },
        )

        # Log crítico para errores de alta severidad
        if error.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            self.logger.critical(
                f"CRITICAL ERROR in {operation}: {error.message}",
                extra={"error": error.__dict__},
            )

    def _get_log_level(self, severity: ErrorSeverity) -> int:
        """Convierte severidad a nivel de log"""
        mapping = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL,
        }
        return mapping.get(severity, logging.ERROR)

    def get_error_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de errores"""
        return {
            "error_counts": self._error_counts.copy(),
            "total_errors": sum(self._error_counts.values()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# Instancia global del manejador de errores
_error_handler = ErrorHandler()


def error_handler(
    operation: str = "unknown", reraise: bool = True, return_default: Any = None
):
    """
    Decorador para manejo automático de errores

    Args:
        operation: Nombre de la operación para logging
        reraise: Si debe re-lanzar la excepción después del logging
        return_default: Valor a retornar en caso de error (si reraise=False)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except TrackHSError as e:
                _error_handler.handle_error(e, operation)
                if reraise:
                    raise
                return return_default
            except Exception as e:
                # Convertir excepciones no controladas a TrackHSError
                trackhs_error = TrackHSError(
                    f"Unexpected error in {operation}: {str(e)}",
                    ErrorSeverity.HIGH,
                    {"original_error": str(e), "error_type": type(e).__name__},
                )
                _error_handler.handle_error(trackhs_error, operation)
                if reraise:
                    raise trackhs_error
                return return_default

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TrackHSError as e:
                _error_handler.handle_error(e, operation)
                if reraise:
                    raise
                return return_default
            except Exception as e:
                # Convertir excepciones no controladas a TrackHSError
                trackhs_error = TrackHSError(
                    f"Unexpected error in {operation}: {str(e)}",
                    ErrorSeverity.HIGH,
                    {"original_error": str(e), "error_type": type(e).__name__},
                )
                _error_handler.handle_error(trackhs_error, operation)
                if reraise:
                    raise trackhs_error
                return return_default

        # Retornar el wrapper apropiado
        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def validate_required_params(params: Dict[str, Any], required: list[str]) -> None:
    """Valida que los parámetros requeridos estén presentes"""
    missing = [
        param for param in required if param not in params or params[param] is None
    ]
    if missing:
        raise ValidationError(
            f"Missing required parameters: {', '.join(missing)}",
            field=missing[0] if len(missing) == 1 else None,
        )


def validate_param_types(params: Dict[str, Any], type_mapping: Dict[str, Type]) -> None:
    """Valida tipos de parámetros"""
    for param, expected_type in type_mapping.items():
        if param in params and params[param] is not None:
            if not isinstance(params[param], expected_type):
                raise ValidationError(
                    f"Parameter '{param}' must be of type {expected_type.__name__}, "
                    f"got {type(params[param]).__name__}",
                    field=param,
                )


def get_error_stats() -> Dict[str, Any]:
    """Obtiene estadísticas de errores globales"""
    return _error_handler.get_error_stats()


# Funciones de conveniencia para errores comunes
def raise_api_error(message: str, status_code: int = None, endpoint: str = None):
    """Lanza un ApiError"""
    raise ApiError(message, status_code, endpoint)


def raise_auth_error(message: str = "Authentication failed"):
    """Lanza un AuthenticationError"""
    raise AuthenticationError(message)


def raise_validation_error(message: str, field: str = None):
    """Lanza un ValidationError"""
    raise ValidationError(message, field)


def raise_network_error(message: str):
    """Lanza un NetworkError"""
    raise NetworkError(message)


def raise_timeout_error(message: str, timeout_seconds: float = None):
    """Lanza un TimeoutError"""
    raise TimeoutError(message, timeout_seconds)
