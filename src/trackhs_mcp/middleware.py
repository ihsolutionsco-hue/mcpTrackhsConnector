"""
Middleware esencial para FastMCP
Solo AuthMiddleware y LoggingMiddleware - eliminando complejidad innecesaria
"""

import logging
import time
from typing import Any, Dict, Optional

from fastmcp.server.middleware import Middleware, MiddlewareContext

logger = logging.getLogger(__name__)


class LoggingMiddleware(Middleware):
    """
    Middleware de logging estructurado simple.

    Logs básicos de requests y responses sin complejidad excesiva.
    """

    def __init__(self, log_level: str = "INFO"):
        """
            Inicializar middleware de logging.

        Args:
                log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_level = getattr(logging, log_level.upper())
        self.logger = logging.getLogger("trackhs_mcp.middleware")

    async def __call__(self, context: MiddlewareContext, call_next) -> Any:
        """
        Procesar request a través del middleware de logging.

        Args:
            context: Contexto del middleware
            call_next: Función para continuar la cadena

        Returns:
            Respuesta procesada
        """
        # Log de inicio de request
        start_time = time.time()

        # Verificar que context.message existe y es un dict
        if hasattr(context, "message") and isinstance(context.message, dict):
            method = context.message.get("method", "unknown")
            self.logger.info(f"MCP Request iniciado: {method}")

            if self.log_level <= logging.DEBUG:
                self.logger.debug(f"Request context: {context.message}")
        else:
            self.logger.info("MCP Request iniciado")

        try:
            # Continuar con el siguiente middleware/handler
            response = await call_next(context)

            # Log de éxito
            duration = time.time() - start_time
            self.logger.info(f"MCP Request completado en {duration:.3f}s")

            if self.log_level <= logging.DEBUG:
                self.logger.debug(f"Response: {response}")

            return response

        except Exception as e:
            # Log de error
            duration = time.time() - start_time
            self.logger.error(
                f"MCP Request falló en {duration:.3f}s: {type(e).__name__}: {str(e)}"
            )

            if self.log_level <= logging.DEBUG:
                self.logger.debug(f"Error details: {e}", exc_info=True)

            # Re-lanzar la excepción
            raise


class AuthMiddleware(Middleware):
    """
    Middleware de autenticación simple.

    Verifica que las credenciales estén configuradas antes de procesar requests.
    """

    def __init__(self, api_client: Optional[Any] = None):
        """
        Inicializar middleware de autenticación.

        Args:
            api_client: Cliente API para verificar conectividad (opcional)
        """
        self.api_client = api_client
        self.logger = logging.getLogger("trackhs_mcp.auth")

    async def __call__(self, context: MiddlewareContext, call_next) -> Any:
        """
        Procesar request a través del middleware de autenticación.

        Args:
            context: Contexto del middleware
            call_next: Función para continuar la cadena

        Returns:
            Respuesta procesada

        Raises:
            ToolError: Si las credenciales no están configuradas
        """
        # Verificar que el cliente API esté disponible
        if self.api_client is None:
            from fastmcp.exceptions import ToolError

            raise ToolError(
                "Cliente API no está disponible. Verifique las credenciales "
                "TRACKHS_USERNAME y TRACKHS_PASSWORD."
            )

        # Log de verificación de auth
        self.logger.debug("Verificando autenticación...")

        try:
            # Continuar con el siguiente middleware/handler
            response = await call_next(context)
            self.logger.debug("Autenticación verificada correctamente")
            return response
        except Exception as e:
            self.logger.error(f"Error en autenticación: {str(e)}")
            raise


class SimpleMetricsMiddleware(Middleware):
    """
    Middleware de métricas simple (opcional).

    Métricas básicas sin complejidad de Prometheus.
    """

    def __init__(self):
        """Inicializar middleware de métricas."""
        self.request_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self.logger = logging.getLogger("trackhs_mcp.metrics")

    async def __call__(self, context: MiddlewareContext, call_next) -> Any:
        """
        Procesar request a través del middleware de métricas.

        Args:
            context: Contexto del middleware
            call_next: Función para continuar la cadena

        Returns:
            Respuesta procesada
        """
        start_time = time.time()
        self.request_count += 1

        try:
            response = await call_next(context)

            duration = time.time() - start_time
            self.total_duration += duration

            # Log de métricas cada 10 requests
            if self.request_count % 10 == 0:
                avg_duration = self.total_duration / self.request_count
                error_rate = (self.error_count / self.request_count) * 100

                self.logger.info(
                    f"Métricas: {self.request_count} requests, "
                    f"avg: {avg_duration:.3f}s, error_rate: {error_rate:.1f}%"
                )

            return response

        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error en request #{self.request_count}: {str(e)}")
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtener métricas actuales.

        Returns:
            Diccionario con métricas básicas
        """
        avg_duration = (
            self.total_duration / self.request_count if self.request_count > 0 else 0.0
        )

        error_rate = (
            (self.error_count / self.request_count) * 100
            if self.request_count > 0
            else 0.0
        )

        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "average_duration_seconds": avg_duration,
            "error_rate_percent": error_rate,
            "total_duration_seconds": self.total_duration,
        }
