"""
Manejo de errores específico para la función search_amenities.
Implementa manejo robusto de errores siguiendo mejores prácticas de FastMCP.
"""

import logging
from typing import Optional

import httpx
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from .amenities_models import AmenitiesErrorInfo

logger = logging.getLogger(__name__)


class AmenitiesErrorHandler:
    """
    Manejador de errores específico para la función search_amenities.

    Proporciona manejo estructurado y específico de errores con logging
    detallado y mensajes de error apropiados para el usuario.
    """

    def __init__(self, context: str = "search_amenities"):
        """
        Inicializar manejador de errores.

        Args:
            context: Contexto de la operación para logging
        """
        self.context = context
        self.logger = logger

    def handle_validation_error(
        self, error: ValidationError, parameters: Optional[dict] = None
    ) -> ToolError:
        """
        Manejar errores de validación de parámetros.

        Args:
            error: Error de validación de Pydantic
            parameters: Parámetros que causaron el error

        Returns:
            ToolError apropiado para el cliente
        """
        error_details = []
        for err in error.errors():
            field = err.get("loc", ["unknown"])[-1]
            message = err.get("msg", "Error de validación")
            error_type = err.get("type", "validation_error")
            error_details.append(f"{field}: {message}")

        error_info = AmenitiesErrorInfo(
            error_type="validation_error",
            error_message=f"Parámetros inválidos: {'; '.join(error_details)}",
            context=self.context,
            parameters=parameters,
        )

        self.logger.warning(
            "Error de validación en search_amenities", extra=error_info.to_log_dict()
        )

        return ToolError(error_info.error_message)

    def handle_http_error(
        self, error: httpx.HTTPStatusError, parameters: Optional[dict] = None
    ) -> ToolError:
        """
        Manejar errores HTTP específicos.

        Args:
            error: Error HTTP de httpx
            parameters: Parámetros de la solicitud

        Returns:
            ToolError apropiado para el cliente
        """
        status_code = error.response.status_code

        # Mapear códigos de estado a mensajes específicos
        if status_code == 401:
            error_info = AmenitiesErrorInfo(
                error_type="authentication_error",
                error_message="Error de autenticación: Credenciales inválidas o expiradas",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )
        elif status_code == 403:
            error_info = AmenitiesErrorInfo(
                error_type="authorization_error",
                error_message="Error de autorización: No tiene permisos para acceder a las amenidades",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )
        elif status_code == 404:
            error_info = AmenitiesErrorInfo(
                error_type="not_found_error",
                error_message="Endpoint de amenidades no encontrado en el servidor TrackHS",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )
        elif status_code == 422:
            error_info = AmenitiesErrorInfo(
                error_type="validation_error",
                error_message="Parámetros de búsqueda inválidos para la API de TrackHS",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )
        elif status_code >= 500:
            error_info = AmenitiesErrorInfo(
                error_type="server_error",
                error_message=f"Error del servidor TrackHS ({status_code}): Servicio temporalmente no disponible",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )
        else:
            error_info = AmenitiesErrorInfo(
                error_type="http_error",
                error_message=f"Error de API TrackHS ({status_code}): {error.response.text}",
                status_code=status_code,
                context=self.context,
                parameters=parameters,
            )

        # Log del error con nivel apropiado
        if status_code >= 500:
            self.logger.error(
                f"Error del servidor en {self.context}", extra=error_info.to_log_dict()
            )
        else:
            self.logger.warning(
                f"Error HTTP en {self.context}", extra=error_info.to_log_dict()
            )

        return ToolError(error_info.error_message)

    def handle_request_error(
        self, error: httpx.RequestError, parameters: Optional[dict] = None
    ) -> ToolError:
        """
        Manejar errores de conexión.

        Args:
            error: Error de conexión de httpx
            parameters: Parámetros de la solicitud

        Returns:
            ToolError apropiado para el cliente
        """
        error_info = AmenitiesErrorInfo(
            error_type="connection_error",
            error_message=f"Error de conexión con TrackHS: {str(error)}",
            context=self.context,
            parameters=parameters,
        )

        self.logger.error(
            f"Error de conexión en {self.context}", extra=error_info.to_log_dict()
        )

        return ToolError(error_info.error_message)

    def handle_unexpected_error(
        self, error: Exception, parameters: Optional[dict] = None
    ) -> ToolError:
        """
        Manejar errores inesperados.

        Args:
            error: Excepción inesperada
            parameters: Parámetros de la solicitud

        Returns:
            ToolError genérico para el cliente
        """
        error_info = AmenitiesErrorInfo(
            error_type="unexpected_error",
            error_message="Error interno del servidor al buscar amenidades",
            context=self.context,
            parameters=parameters,
        )

        self.logger.error(
            f"Error inesperado en {self.context}: {str(error)}",
            extra=error_info.to_log_dict(),
            exc_info=True,
        )

        return ToolError(error_info.error_message)

    def handle_error(
        self, error: Exception, parameters: Optional[dict] = None
    ) -> ToolError:
        """
        Manejar cualquier tipo de error de forma unificada.

        Args:
            error: Excepción a manejar
            parameters: Parámetros de la solicitud

        Returns:
            ToolError apropiado para el cliente
        """
        if isinstance(error, ValidationError):
            return self.handle_validation_error(error, parameters)
        elif isinstance(error, httpx.HTTPStatusError):
            return self.handle_http_error(error, parameters)
        elif isinstance(error, httpx.RequestError):
            return self.handle_request_error(error, parameters)
        else:
            return self.handle_unexpected_error(error, parameters)
