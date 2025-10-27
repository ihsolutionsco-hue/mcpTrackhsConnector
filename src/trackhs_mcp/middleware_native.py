"""
Middleware nativo FastMCP para TrackHS MCP Server
Implementa logging, autenticación, métricas y rate limiting usando middleware nativo
"""

import logging
import time
from typing import Any, Dict, Optional

from fastmcp.server.middleware import Middleware, MiddlewareContext

from .config import get_settings
from .exceptions import AuthenticationError
from .metrics import (
    get_metrics,
    record_request_metrics,
    record_mcp_tool_metrics,
    record_cache_metrics
)

logger = logging.getLogger(__name__)
settings = get_settings()


class TrackHSLoggingMiddleware(Middleware):
    """
    Middleware de logging nativo FastMCP
    Registra todas las operaciones con información estructurada
    """

    def __init__(self):
        super().__init__()
        self.request_count = 0

    async def on_message(self, context: MiddlewareContext, call_next):
        """Intercepta mensajes para logging estructurado"""
        self.request_count += 1
        start_time = time.time()

        # Log de request
        logger.info(
            f"🔧 Request #{self.request_count}",
            extra={
                "method": context.method,
                "request_id": self.request_count,
                "timestamp": start_time
            }
        )

        try:
            # Ejecutar siguiente middleware/tool
            result = await call_next(context)

            # Log de éxito
            duration = time.time() - start_time
            logger.info(
                f"✅ Success",
                extra={
                    "method": context.method,
                    "duration": duration,
                    "request_id": self.request_count,
                    "status": "success"
                }
            )

            # Registrar métricas
            record_request_metrics(context.method, duration, 200)
            record_mcp_tool_metrics(context.method, duration, True)

            return result

        except Exception as e:
            # Log de error
            duration = time.time() - start_time
            logger.error(
                f"❌ Error: {type(e).__name__}: {str(e)}",
                extra={
                    "method": context.method,
                    "duration": duration,
                    "request_id": self.request_count,
                    "status": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            )

            # Registrar métricas de error
            record_request_metrics(context.method, duration, 500)
            record_mcp_tool_metrics(context.method, duration, False)

            raise


class TrackHSAuthMiddleware(Middleware):
    """
    Middleware de autenticación nativo FastMCP
    Verifica autenticación con cache inteligente
    """

    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.last_auth_check: Optional[float] = None
        self.is_authenticated = False
        self.auth_cache_ttl = settings.auth_cache_ttl

    def _check_authentication(self) -> bool:
        """Verificar autenticación con cache"""
        if self.api_client is None:
            # En modo testing, permitir sin autenticación
            if os.getenv("TESTING") == "1" or os.getenv("PYTEST_CURRENT_TEST"):
                logger.warning("⚠️  Running in test mode without API client")
                return False

            raise AuthenticationError(
                "Cliente API no disponible. Configure TRACKHS_USERNAME y TRACKHS_PASSWORD"
            )

        now = time.time()

        # Verificar si necesitamos refrescar el cache
        needs_refresh = (
            self.last_auth_check is None or
            (now - self.last_auth_check) > self.auth_cache_ttl
        )

        if needs_refresh:
            try:
                # Verificación ligera de conectividad
                self.api_client.get("pms/units/amenities", {"page": 1, "size": 1})
                self.is_authenticated = True
                self.last_auth_check = now
                logger.debug(f"Authentication cache refreshed (TTL: {self.auth_cache_ttl}s)")
            except Exception as e:
                self.is_authenticated = False
                logger.error(f"Authentication failed: {str(e)}")
                raise AuthenticationError(f"Credenciales inválidas: {str(e)}")

        if not self.is_authenticated:
            raise AuthenticationError("No autenticado con TrackHS API")

        return True

    async def on_message(self, context: MiddlewareContext, call_next):
        """Intercepta mensajes para verificar autenticación"""

        # Métodos que NO requieren autenticación
        NO_AUTH_METHODS = {
            "initialize",
            "ping",
            "tools/list",
            "resources/list",
            "resources/templates/list",
            "prompts/list",
        }

        if context.method not in NO_AUTH_METHODS:
            try:
                self._check_authentication()
            except Exception as e:
                logger.error(f"Authentication failed for {context.method}: {str(e)}")
                raise

        # Continuar con el siguiente middleware
        return await call_next(context)


class TrackHSMetricsMiddleware(Middleware):
    """
    Middleware de métricas nativo FastMCP
    Recopila métricas de rendimiento y uso
    """

    def __init__(self):
        super().__init__()
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_duration": 0.0,
            "start_time": time.time()
        }
        self.response_times: list[float] = []

    async def on_message(self, context: MiddlewareContext, call_next):
        """Intercepta mensajes para recopilar métricas"""
        self.metrics["total_requests"] += 1
        start_time = time.time()

        try:
            # Ejecutar siguiente middleware/tool
            result = await call_next(context)

            # Métricas de éxito
            duration = time.time() - start_time
            self.metrics["successful_requests"] += 1
            self.metrics["total_duration"] += duration
            self.response_times.append(duration)

            return result

        except Exception as e:
            # Métricas de error
            duration = time.time() - start_time
            self.metrics["failed_requests"] += 1
            self.metrics["total_duration"] += duration
            self.response_times.append(duration)

            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Obtener métricas actuales"""
        uptime = time.time() - self.metrics["start_time"]
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )

        error_rate = (
            (self.metrics["failed_requests"] / self.metrics["total_requests"]) * 100
            if self.metrics["total_requests"] > 0 else 0
        )

        return {
            **self.metrics,
            "uptime_seconds": round(uptime, 2),
            "average_response_time": round(avg_response_time, 3),
            "error_rate_percentage": round(error_rate, 2),
            "requests_per_minute": round(
                (self.metrics["total_requests"] / uptime) * 60, 2
            ) if uptime > 0 else 0
        }

    def reset_metrics(self):
        """Resetear métricas (útil para testing)"""
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_duration": 0.0,
            "start_time": time.time()
        }
        self.response_times = []


class TrackHSRateLimitMiddleware(Middleware):
    """
    Middleware de rate limiting nativo FastMCP
    Implementa rate limiting simple por IP/usuario
    """

    def __init__(self, requests_per_minute: int = 60, burst_size: int = 10):
        super().__init__()
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.request_counts: Dict[str, list[float]] = {}

    def _is_rate_limited(self, client_id: str) -> bool:
        """Verificar si el cliente está rate limited"""
        now = time.time()
        minute_ago = now - 60

        # Obtener requests del último minuto
        if client_id not in self.request_counts:
            self.request_counts[client_id] = []

        # Filtrar requests del último minuto
        self.request_counts[client_id] = [
            req_time for req_time in self.request_counts[client_id]
            if req_time > minute_ago
        ]

        # Verificar límites
        if len(self.request_counts[client_id]) >= self.requests_per_minute:
            return True

        return False

    async def on_message(self, context: MiddlewareContext, call_next):
        """Intercepta mensajes para aplicar rate limiting"""
        # Obtener identificador del cliente (simplificado)
        client_id = getattr(context, 'client_id', 'default')

        if self._is_rate_limited(client_id):
            from fastmcp.exceptions import ToolError
            raise ToolError(
                f"Rate limit exceeded. Máximo {self.requests_per_minute} requests por minuto."
            )

        # Registrar request
        now = time.time()
        if client_id not in self.request_counts:
            self.request_counts[client_id] = []
        self.request_counts[client_id].append(now)

        # Continuar con el siguiente middleware
        return await call_next(context)
