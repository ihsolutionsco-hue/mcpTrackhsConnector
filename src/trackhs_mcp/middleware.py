"""
Middleware FastMCP-compatible para TrackHS MCP Server.
Implementa logging, autenticación con cache, y métricas usando el sistema de middleware nativo de FastMCP 2.9+.
"""

import logging
import time
from typing import Any, Dict, Optional

from fastmcp.server.middleware import Middleware, MiddlewareContext

logger = logging.getLogger(__name__)


class TrackHSMiddleware(Middleware):
    """
    Middleware unificado para logging, autenticación y métricas.
    Compatible con FastMCP 2.9+ usando el sistema de middleware nativo.

    Características:
    - Logging automático de todas las operaciones
    - Validación de autenticación con cache (evita verificar en cada request)
    - Métricas de rendimiento (requests, errores, tiempos de respuesta)
    - Compatible con el sistema de middleware de FastMCP

    Args:
        api_client: Cliente de API TrackHS (opcional durante inicialización)
        auth_cache_ttl: Tiempo de vida del cache de autenticación en segundos (default: 300 = 5 minutos)
    """

    def __init__(self, api_client=None, auth_cache_ttl: int = 300):
        super().__init__()
        self.api_client = api_client
        self.auth_cache_ttl = auth_cache_ttl
        self.last_auth_check: Optional[float] = None
        self.is_authenticated = False

        # Métricas
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }
        self.response_times: list[float] = []

    def _check_authentication(self) -> bool:
        """
        Verifica autenticación con cache para evitar validaciones innecesarias.

        Solo hace una petición a la API si:
        - Es la primera vez
        - El cache expiró (después de auth_cache_ttl segundos)

        Returns:
            True si está autenticado

        Raises:
            AuthenticationError: Si las credenciales son inválidas
        """
        import os

        from .exceptions import AuthenticationError

        # En modo testing o sin credenciales, no fallar inmediatamente
        if self.api_client is None:
            # Permitir operación en modo testing
            if os.getenv("TESTING") == "1" or os.getenv("PYTEST_CURRENT_TEST"):
                logger.warning("⚠️  Running in test mode without API client")
                self.is_authenticated = False
                return False

            raise AuthenticationError(
                "Cliente API no disponible. Configure TRACKHS_USERNAME y TRACKHS_PASSWORD"
            )

        now = time.time()

        # Verificar si necesitamos refrescar el cache
        needs_refresh = (
            self.last_auth_check is None
            or (now - self.last_auth_check) > self.auth_cache_ttl
        )

        if needs_refresh:
            try:
                # Verificación ligera de conectividad y autenticación
                self.api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
                self.is_authenticated = True
                self.last_auth_check = now
                logger.debug(
                    f"Authentication cache refreshed (TTL: {self.auth_cache_ttl}s)"
                )
            except Exception as e:
                self.is_authenticated = False
                logger.error(f"Authentication failed: {str(e)}")
                raise AuthenticationError(f"Credenciales inválidas: {str(e)}")

        if not self.is_authenticated:
            raise AuthenticationError("No autenticado con TrackHS API")

        return True

    async def on_message(self, context: MiddlewareContext, call_next):
        """
        Intercepta cada mensaje MCP para aplicar logging, autenticación y métricas.

        Este método se ejecuta automáticamente en cada llamada a una tool gracias
        al sistema de middleware de FastMCP.

        Args:
            context: Contexto del mensaje MCP con información del request
            call_next: Función para continuar con el siguiente middleware/tool

        Returns:
            Resultado de la tool

        Raises:
            AuthenticationError: Si la autenticación falla
            Exception: Cualquier error de la tool se propaga después de registrarse
        """
        self.metrics["total_requests"] += 1
        start_time = time.time()

        # 1. Verificar autenticación (con cache) - solo para tools/call, no para metadatos
        # Métodos que NO requieren autenticación (descubrimiento del servidor):
        NO_AUTH_METHODS = {
            "initialize",  # Inicialización del protocolo MCP
            "ping",  # Verificación de conectividad
            "tools/list",  # Listar herramientas disponibles
            "resources/list",  # Listar recursos disponibles
            "resources/templates/list",  # Listar templates de recursos
            "prompts/list",  # Listar prompts disponibles
        }

        if context.method not in NO_AUTH_METHODS:
            try:
                self._check_authentication()
            except Exception as e:
                # Error de autenticación - no continuar
                duration = time.time() - start_time
                self.metrics["failed_requests"] += 1
                logger.error(
                    f"❌ Auth failed | "
                    f"Duration: {duration:.2f}s | "
                    f"Error: {type(e).__name__}: {str(e)}"
                )
                raise

        # 2. Logging de request
        logger.info(
            f"🔧 Tool called: {context.method} | Request #{self.metrics['total_requests']}"
        )

        # 3. Ejecutar la herramienta
        try:
            result = await call_next(context)

            # 4. Métricas de éxito
            duration = time.time() - start_time
            self.response_times.append(duration)
            self.metrics["successful_requests"] += 1

            avg_time = sum(self.response_times) / len(self.response_times)

            logger.info(
                f"✅ Success | "
                f"Tool: {context.method} | "
                f"Duration: {duration:.2f}s | "
                f"Avg: {avg_time:.2f}s"
            )

            return result

        except Exception as e:
            # 5. Métricas de error
            duration = time.time() - start_time
            self.metrics["failed_requests"] += 1
            error_rate = (
                self.metrics["failed_requests"] / self.metrics["total_requests"]
            ) * 100

            logger.error(
                f"❌ Error | "
                f"Tool: {context.method} | "
                f"Duration: {duration:.2f}s | "
                f"Error rate: {error_rate:.1f}% | "
                f"Error: {type(e).__name__}: {str(e)}"
            )

            raise

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas actuales del middleware.

        Returns:
            Dict con métricas de requests, éxitos, errores y tiempos de respuesta
        """
        avg_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0
        )

        error_rate = (
            (self.metrics["failed_requests"] / self.metrics["total_requests"]) * 100
            if self.metrics["total_requests"] > 0
            else 0
        )

        return {
            **self.metrics,
            "average_response_time_seconds": round(avg_time, 2),
            "error_rate_percentage": round(error_rate, 2),
            "total_response_times_recorded": len(self.response_times),
        }

    def reset_metrics(self):
        """Resetea las métricas (útil para testing)"""
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }
        self.response_times = []
        logger.info("Middleware metrics reset")


# Mantener clases antiguas para compatibilidad temporal durante la transición
# TODO: Eliminar después de completar la refactorización


class LoggingMiddleware:
    """
    DEPRECATED: Usar TrackHSMiddleware en su lugar.
    Esta clase se mantiene temporalmente para compatibilidad.
    """

    def __init__(self):
        logger.warning(
            "LoggingMiddleware está deprecated. Use TrackHSMiddleware con mcp.add_middleware()"
        )
        self.request_count = 0
        self.error_count = 0


class AuthenticationMiddleware:
    """
    DEPRECATED: Usar TrackHSMiddleware en su lugar.
    Esta clase se mantiene temporalmente para compatibilidad.
    """

    def __init__(self, api_client):
        logger.warning(
            "AuthenticationMiddleware está deprecated. Use TrackHSMiddleware con mcp.add_middleware()"
        )
        self.api_client = api_client


class MetricsMiddleware:
    """
    DEPRECATED: Usar TrackHSMiddleware en su lugar.
    Esta clase se mantiene temporalmente para compatibilidad.
    """

    def __init__(self):
        logger.warning(
            "MetricsMiddleware está deprecated. Use TrackHSMiddleware con mcp.add_middleware()"
        )
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "error_rate": 0,
            "start_time": time.time(),
        }
        self.response_times = []
