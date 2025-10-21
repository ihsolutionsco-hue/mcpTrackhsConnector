"""
Middleware personalizado de manejo de errores para TrackHS MCP Server
Integra con el sistema de logging existente y maneja errores específicos de TrackHS API
"""

import logging
from typing import Any, Dict, Optional

from fastmcp.server.middleware import Middleware, MiddlewareContext

from ..utils.error_handling import ErrorHandler

logger = logging.getLogger(__name__)


class TrackHSErrorHandlingMiddleware(Middleware):
    """
    Middleware de manejo de errores específico para TrackHS API
    Integra con el sistema de error handling existente
    """

    def __init__(self, include_traceback: bool = False, transform_errors: bool = True):
        """
        Inicializa el middleware de manejo de errores

        Args:
            include_traceback: Si incluir traceback en logs
            transform_errors: Si transformar errores a mensajes amigables
        """
        self.include_traceback = include_traceback
        self.transform_errors = transform_errors
        self.error_counts: Dict[str, int] = {}
        self.error_handler = ErrorHandler()

    async def on_message(self, context: MiddlewareContext, call_next):
        """
        Intercepta mensajes MCP y maneja errores
        """
        try:
            return await call_next(context)
        except Exception as error:
            # Contar errores por tipo
            error_key = f"{type(error).__name__}:{context.method}"
            self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1

            # Log del error con contexto
            self._log_error(context, error)

            # Transformar error si está habilitado
            if self.transform_errors:
                transformed_error = self._transform_error(error, context)
                if transformed_error:
                    raise transformed_error

            # Re-lanzar error original
            raise error

    def _log_error(self, context: MiddlewareContext, error: Exception):
        """
        Log estructurado del error con contexto
        """
        error_data = {
            "method": context.method,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "error_count": self.error_counts.get(
                f"{type(error).__name__}:{context.method}", 0
            ),
        }

        if self.include_traceback:
            import traceback

            error_data["traceback"] = traceback.format_exc()

        # Log con nivel apropiado según tipo de error
        if isinstance(error, (ValueError, TypeError)):
            logger.warning(
                f"Validation error in {context.method}: {error}", extra=error_data
            )
        elif isinstance(error, ConnectionError):
            logger.error(
                f"Connection error in {context.method}: {error}", extra=error_data
            )
        else:
            logger.error(
                f"Unexpected error in {context.method}: {error}", extra=error_data
            )

    def _transform_error(
        self, error: Exception, context: MiddlewareContext
    ) -> Optional[Exception]:
        """
        Transforma errores a mensajes más amigables
        """
        try:
            # Transformar errores comunes a mensajes más amigables
            error_message = str(error)

            # Mapear errores comunes
            if "ValidationError" in str(type(error)):
                friendly_message = f"Error de validación: {error_message}"
            elif "ConnectionError" in str(type(error)):
                friendly_message = "Error de conexión con TrackHS API. Verifica tu conexión a internet."
            elif "TimeoutError" in str(type(error)):
                friendly_message = (
                    "Tiempo de espera agotado. La operación tardó demasiado."
                )
            else:
                friendly_message = error_message

            if friendly_message != error_message:
                # Crear nuevo error con mensaje amigable
                from fastmcp.exceptions import ToolError

                return ToolError(friendly_message)

        except Exception as transform_error:
            logger.warning(f"Error transforming error message: {transform_error}")

        return None

    def get_error_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de errores
        """
        return {
            "error_counts": self.error_counts.copy(),
            "total_errors": sum(self.error_counts.values()),
            "unique_error_types": len(self.error_counts),
        }

    def reset_error_stats(self):
        """
        Resetea estadísticas de errores
        """
        self.error_counts.clear()
        logger.info("Error statistics reset")
