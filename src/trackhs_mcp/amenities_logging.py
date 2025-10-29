"""
Logging estructurado para el servicio de amenidades.
Implementa logging detallado y estructurado siguiendo mejores prácticas.
"""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Niveles de log personalizados para amenidades."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AmenitiesLogger:
    """
    Logger estructurado para operaciones de amenidades.

    Proporciona logging detallado y estructurado para todas las operaciones
    relacionadas con la búsqueda de amenidades.
    """

    def __init__(self, context: str = "amenities"):
        """
        Inicializar logger de amenidades.

        Args:
            context: Contexto de la operación
        """
        self.context = context
        self.logger = logger

    def _create_log_entry(
        self, level: LogLevel, message: str, operation: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Crear entrada de log estructurada.

        Args:
            level: Nivel de log
            message: Mensaje principal
            operation: Operación específica
            **kwargs: Datos adicionales

        Returns:
            Entrada de log estructurada
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "context": self.context,
            "operation": operation,
            "message": message,
            **kwargs,
        }

    def log_search_start(
        self, page: int, size: int, search_params: Optional[Dict[str, Any]] = None
    ):
        """
        Log del inicio de búsqueda de amenidades.

        Args:
            page: Número de página
            size: Tamaño de página
            search_params: Parámetros de búsqueda
        """
        log_entry = self._create_log_entry(
            LogLevel.INFO,
            f"Iniciando búsqueda de amenidades: página {page}, tamaño {size}",
            "search_start",
            page=page,
            size=size,
            search_params=search_params or {},
        )

        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_search_success(
        self,
        total_items: int,
        page: int,
        size: int,
        response_time_ms: Optional[float] = None,
    ):
        """
        Log de búsqueda exitosa.

        Args:
            total_items: Total de amenidades encontradas
            page: Número de página
            size: Tamaño de página
            response_time_ms: Tiempo de respuesta en milisegundos
        """
        log_entry = self._create_log_entry(
            LogLevel.INFO,
            f"Búsqueda exitosa: {total_items} amenidades encontradas",
            "search_success",
            total_items=total_items,
            page=page,
            size=size,
            response_time_ms=response_time_ms,
        )

        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_validation_error(
        self,
        error_message: str,
        parameters: Dict[str, Any],
        validation_errors: Optional[list] = None,
    ):
        """
        Log de error de validación.

        Args:
            error_message: Mensaje de error
            parameters: Parámetros que causaron el error
            validation_errors: Errores específicos de validación
        """
        log_entry = self._create_log_entry(
            LogLevel.WARNING,
            f"Error de validación: {error_message}",
            "validation_error",
            error_message=error_message,
            parameters=parameters,
            validation_errors=validation_errors or [],
        )

        self.logger.warning(json.dumps(log_entry, ensure_ascii=False))

    def log_http_error(
        self,
        status_code: int,
        error_message: str,
        parameters: Dict[str, Any],
        response_text: Optional[str] = None,
    ):
        """
        Log de error HTTP.

        Args:
            status_code: Código de estado HTTP
            error_message: Mensaje de error
            parameters: Parámetros de la solicitud
            response_text: Texto de respuesta del servidor
        """
        log_entry = self._create_log_entry(
            LogLevel.ERROR if status_code >= 500 else LogLevel.WARNING,
            f"Error HTTP {status_code}: {error_message}",
            "http_error",
            status_code=status_code,
            error_message=error_message,
            parameters=parameters,
            response_text=response_text,
        )

        if status_code >= 500:
            self.logger.error(json.dumps(log_entry, ensure_ascii=False))
        else:
            self.logger.warning(json.dumps(log_entry, ensure_ascii=False))

    def log_connection_error(self, error_message: str, parameters: Dict[str, Any]):
        """
        Log de error de conexión.

        Args:
            error_message: Mensaje de error
            parameters: Parámetros de la solicitud
        """
        log_entry = self._create_log_entry(
            LogLevel.ERROR,
            f"Error de conexión: {error_message}",
            "connection_error",
            error_message=error_message,
            parameters=parameters,
        )

        self.logger.error(json.dumps(log_entry, ensure_ascii=False))

    def log_unexpected_error(
        self,
        error_message: str,
        parameters: Dict[str, Any],
        exception_type: str,
        exception_details: Optional[str] = None,
    ):
        """
        Log de error inesperado.

        Args:
            error_message: Mensaje de error
            parameters: Parámetros de la solicitud
            exception_type: Tipo de excepción
            exception_details: Detalles de la excepción
        """
        log_entry = self._create_log_entry(
            LogLevel.ERROR,
            f"Error inesperado: {error_message}",
            "unexpected_error",
            error_message=error_message,
            parameters=parameters,
            exception_type=exception_type,
            exception_details=exception_details,
        )

        self.logger.error(json.dumps(log_entry, ensure_ascii=False))

    def log_performance_metrics(
        self,
        operation: str,
        duration_ms: float,
        total_items: int,
        page_size: int,
        **additional_metrics,
    ):
        """
        Log de métricas de rendimiento.

        Args:
            operation: Operación realizada
            duration_ms: Duración en milisegundos
            total_items: Total de elementos procesados
            page_size: Tamaño de página
            **additional_metrics: Métricas adicionales
        """
        log_entry = self._create_log_entry(
            LogLevel.INFO,
            f"Métricas de rendimiento: {operation} completada en {duration_ms}ms",
            "performance_metrics",
            duration_ms=duration_ms,
            total_items=total_items,
            page_size=page_size,
            **additional_metrics,
        )

        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_api_call(
        self,
        endpoint: str,
        parameters: Dict[str, Any],
        response_size: Optional[int] = None,
    ):
        """
        Log de llamada a la API.

        Args:
            endpoint: Endpoint de la API
            parameters: Parámetros enviados
            response_size: Tamaño de la respuesta
        """
        log_entry = self._create_log_entry(
            LogLevel.DEBUG,
            f"Llamada a API: {endpoint}",
            "api_call",
            endpoint=endpoint,
            parameters=parameters,
            response_size=response_size,
        )

        self.logger.debug(json.dumps(log_entry, ensure_ascii=False))

    def log_parameter_validation(
        self,
        parameters: Dict[str, Any],
        validation_result: bool,
        validation_details: Optional[Dict[str, Any]] = None,
    ):
        """
        Log de validación de parámetros.

        Args:
            parameters: Parámetros validados
            validation_result: Resultado de la validación
            validation_details: Detalles de la validación
        """
        log_entry = self._create_log_entry(
            LogLevel.DEBUG,
            f"Validación de parámetros: {'exitosa' if validation_result else 'fallida'}",
            "parameter_validation",
            parameters=parameters,
            validation_result=validation_result,
            validation_details=validation_details or {},
        )

        self.logger.debug(json.dumps(log_entry, ensure_ascii=False))


# Instancia global del logger de amenidades
amenities_logger = AmenitiesLogger("amenities_service")
