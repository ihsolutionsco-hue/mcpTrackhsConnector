"""
Middleware de logging estructurado para TrackHS MCP Server
Integra con el sistema de logging existente y proporciona contexto de llamadas API
"""

import json
import logging
import time
from typing import Any, Dict, Optional

from fastmcp.server.middleware import Middleware, MiddlewareContext

logger = logging.getLogger(__name__)


class TrackHSLoggingMiddleware(Middleware):
    """
    Middleware de logging estructurado para TrackHS MCP Server
    Proporciona logging detallado de requests/responses con contexto de API
    """

    def __init__(
        self,
        log_requests: bool = True,
        log_responses: bool = True,
        log_timing: bool = True,
        log_level: str = "INFO",
    ):
        """
        Inicializa el middleware de logging

        Args:
            log_requests: Si loggear requests entrantes
            log_responses: Si loggear responses salientes
            log_timing: Si loggear tiempos de ejecución
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_timing = log_timing
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)

        # Estadísticas de requests
        self.request_count = 0
        self.total_time = 0.0

    async def on_message(self, context: MiddlewareContext, call_next):
        """
        Intercepta mensajes MCP y proporciona logging estructurado
        """
        start_time = time.time()
        self.request_count += 1

        # Log del request
        if self.log_requests:
            self._log_request(context)

        try:
            # Ejecutar siguiente middleware/handler
            result = await call_next(context)

            # Log del response
            if self.log_responses:
                self._log_response(context, result, start_time)

            return result

        except Exception as error:
            # Log del error
            self._log_error(context, error, start_time)
            raise

    def _log_request(self, context: MiddlewareContext):
        """
        Log estructurado del request
        """
        request_data = {
            "type": "mcp_request",
            "method": context.method,
            "request_id": self.request_count,
            "timestamp": time.time(),
        }

        # Agregar parámetros si es una llamada a tool
        if hasattr(context, "params") and context.params:
            request_data["params"] = self._sanitize_params(context.params)

        logger.log(self.log_level, f"MCP Request: {context.method}", extra=request_data)

    def _log_response(self, context: MiddlewareContext, result: Any, start_time: float):
        """
        Log estructurado del response
        """
        execution_time = time.time() - start_time
        self.total_time += execution_time

        response_data = {
            "type": "mcp_response",
            "method": context.method,
            "request_id": self.request_count,
            "execution_time": execution_time,
            "timestamp": time.time(),
        }

        # Agregar información del resultado si es relevante
        if isinstance(result, dict) and "content" in result:
            response_data["result_type"] = "content"
            response_data["content_length"] = len(str(result.get("content", "")))
        elif isinstance(result, list):
            response_data["result_type"] = "list"
            response_data["item_count"] = len(result)

        logger.log(
            self.log_level,
            f"MCP Response: {context.method} ({execution_time:.3f}s)",
            extra=response_data,
        )

    def _log_error(
        self, context: MiddlewareContext, error: Exception, start_time: float
    ):
        """
        Log estructurado del error
        """
        execution_time = time.time() - start_time

        error_data = {
            "type": "mcp_error",
            "method": context.method,
            "request_id": self.request_count,
            "execution_time": execution_time,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": time.time(),
        }

        logger.error(
            f"MCP Error: {context.method} - {type(error).__name__}: {error}",
            extra=error_data,
        )

    def _sanitize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitiza parámetros para logging (remueve información sensible)
        """
        sanitized = {}
        sensitive_keys = {"password", "token", "secret", "key", "auth"}

        for key, value in params.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_params(value)
            else:
                sanitized[key] = str(type(value).__name__)

        return sanitized

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de logging
        """
        avg_time = self.total_time / self.request_count if self.request_count > 0 else 0

        return {
            "request_count": self.request_count,
            "total_time": self.total_time,
            "average_time": avg_time,
            "log_level": logging.getLevelName(self.log_level),
        }

    def reset_stats(self):
        """
        Resetea estadísticas
        """
        self.request_count = 0
        self.total_time = 0.0
        logger.info("Logging statistics reset")
