"""
Middleware para TrackHS MCP Server
Implementa logging, autenticación y métricas
"""

import logging
import time
from typing import Any, Dict

from .exceptions import APIError, AuthenticationError, ConnectionError

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Middleware de logging para todas las operaciones"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0

    async def __call__(self, request, next_handler):
        """Intercepta requests y responses para logging"""
        self.request_count += 1
        start_time = time.time()

        # Log del request
        logger.info(f"Request #{self.request_count}: {request}")

        try:
            # Procesar request
            response = await next_handler(request)

            # Log del response exitoso
            duration = round((time.time() - start_time) * 1000, 2)
            logger.info(f"Response #{self.request_count}: Success in {duration}ms")

            return response

        except Exception as e:
            # Log del error
            self.error_count += 1
            duration = round((time.time() - start_time) * 1000, 2)
            error_rate = (self.error_count / self.request_count) * 100

            logger.error(f"Error #{self.request_count}: {str(e)} in {duration}ms")
            logger.error(f"Error rate: {error_rate:.2f}%")

            raise


class AuthenticationMiddleware:
    """Middleware de autenticación para verificar credenciales"""

    def __init__(self, api_client):
        self.api_client = api_client

    async def __call__(self, request, next_handler):
        """Verifica que el cliente API esté disponible"""
        if self.api_client is None:
            raise AuthenticationError(
                "Cliente API no está disponible. Verifique las credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD."
            )

        # Verificar conectividad básica
        try:
            # Hacer una petición simple para verificar autenticación
            self.api_client.get("pms/units/amenities", {"page": 1, "size": 1})
        except Exception as e:
            if "401" in str(e) or "403" in str(e):
                raise AuthenticationError(f"Credenciales inválidas: {str(e)}")
            elif "timeout" in str(e).lower() or "connection" in str(e).lower():
                raise ConnectionError(f"Error de conexión: {str(e)}")
            else:
                raise APIError(f"Error de API: {str(e)}")

        # Si la autenticación es exitosa, procesar el request
        return await next_handler(request)


class MetricsMiddleware:
    """Middleware de métricas para monitoreo"""

    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "error_rate": 0,
            "start_time": time.time(),
        }
        self.response_times = []

    async def __call__(self, request, next_handler):
        """Recopila métricas de rendimiento"""
        start_time = time.time()
        self.metrics["total_requests"] += 1

        try:
            response = await next_handler(request)

            # Métricas de éxito
            duration = time.time() - start_time
            self.response_times.append(duration)
            self.metrics["successful_requests"] += 1

            # Calcular promedio de tiempo de respuesta
            self.metrics["average_response_time"] = sum(self.response_times) / len(
                self.response_times
            )

            return response

        except Exception as e:
            # Métricas de error
            self.metrics["failed_requests"] += 1
            self.metrics["error_rate"] = (
                self.metrics["failed_requests"] / self.metrics["total_requests"]
            ) * 100

            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas actuales"""
        uptime = time.time() - self.metrics["start_time"]
        return {
            **self.metrics,
            "uptime_seconds": uptime,
            "requests_per_minute": (
                (self.metrics["total_requests"] / uptime) * 60 if uptime > 0 else 0
            ),
        }
