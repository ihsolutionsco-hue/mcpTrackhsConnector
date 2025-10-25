"""
Middleware de logging específico para FastMCP Cloud
Asegura que los logs se registren correctamente en FastMCP Cloud
"""

import logging
import sys
import time
from typing import Any

from fastmcp.server.middleware import Middleware, MiddlewareContext

logger = logging.getLogger(__name__)


class FastMCPCloudLoggingMiddleware(Middleware):
    """
    Middleware específico para logging en FastMCP Cloud
    Usa múltiples métodos para asegurar que los logs se registren
    """

    def __init__(self):
        self.request_count = 0
        self.start_time = time.time()

    async def on_message(self, context: MiddlewareContext, call_next):
        """
        Intercepta mensajes MCP y registra logs en FastMCP Cloud
        """
        self.request_count += 1
        start_time = time.time()

        # Log usando múltiples métodos para asegurar visibilidad
        self._log_to_fastmcp_cloud(
            f"🔄 MCP Request #{self.request_count}: {context.method}"
        )

        try:
            # Ejecutar siguiente middleware/handler
            result = await call_next(context)

            # Log de respuesta
            execution_time = time.time() - start_time
            self._log_to_fastmcp_cloud(
                f"✅ MCP Response #{self.request_count}: {context.method} ({execution_time:.3f}s)"
            )

            return result

        except Exception as error:
            # Log de error
            execution_time = time.time() - start_time
            self._log_to_fastmcp_cloud(
                f"❌ MCP Error #{self.request_count}: {context.method} - {type(error).__name__}: {error} ({execution_time:.3f}s)"
            )
            raise

    def _log_to_fastmcp_cloud(self, message: str):
        """
        Registra logs usando múltiples métodos para asegurar visibilidad en FastMCP Cloud
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        # Método 1: Logger estándar
        logger.info(formatted_message)

        # Método 2: Print directo (más confiable en FastMCP Cloud)
        print(formatted_message)

        # Método 3: sys.stdout directo
        sys.stdout.write(f"{formatted_message}\n")
        sys.stdout.flush()

        # Método 4: sys.stderr como backup
        sys.stderr.write(f"{formatted_message}\n")
        sys.stderr.flush()

    def get_stats(self) -> dict:
        """
        Retorna estadísticas del middleware
        """
        uptime = time.time() - self.start_time
        return {
            "request_count": self.request_count,
            "uptime_seconds": uptime,
            "requests_per_second": self.request_count / uptime if uptime > 0 else 0,
        }
