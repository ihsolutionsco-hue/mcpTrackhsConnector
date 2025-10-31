"""
Logger estructurado para TrackHS MCP Server
Usa FastMCP logging utilities siguiendo mejores prácticas
"""

import logging
import sys
from typing import Any, Dict, Optional

# Intentar usar FastMCP logging utilities, fallback a logging estándar
try:
    from fastmcp.utilities.logging import get_logger as fastmcp_get_logger

    def get_logger(name: str) -> logging.Logger:
        """
        Obtiene un logger configurado usando FastMCP utilities

        Args:
            name: Nombre del logger (usualmente __name__)

        Returns:
            Logger configurado con FastMCP
        """
        return fastmcp_get_logger(name)

except ImportError:
    # Fallback si FastMCP no está disponible
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    def get_logger(name: str) -> logging.Logger:
        """
        Obtiene un logger configurado con logging estándar (fallback)

        Args:
            name: Nombre del logger (usualmente __name__)

        Returns:
            Logger configurado
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger


def log_tool_execution(
    logger: logging.Logger,
    tool_name: str,
    action: str,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log estructurado para ejecución de herramientas

    Args:
        logger: Logger instance
        tool_name: Nombre de la herramienta
        action: Acción realizada (start, success, error)
        extra: Datos adicionales
    """
    log_data = {"tool_name": tool_name, "action": action, **(extra or {})}

    if action == "start":
        logger.info(f"Iniciando ejecución de herramienta: {tool_name}", extra=log_data)
    elif action == "success":
        logger.info(f"Herramienta ejecutada exitosamente: {tool_name}", extra=log_data)
    elif action == "error":
        logger.error(f"Error en herramienta: {tool_name}", extra=log_data)


def log_api_call(
    logger: logging.Logger,
    method: str,
    url: str,
    status_code: int,
    response_time_ms: float,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log estructurado para llamadas API

    Args:
        logger: Logger instance
        method: Método HTTP
        url: URL de la API
        status_code: Código de respuesta HTTP
        response_time_ms: Tiempo de respuesta en milisegundos
        extra: Datos adicionales
    """
    log_data = {
        "api_call": True,
        "method": method,
        "url": url,
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        **(extra or {}),
    }

    if 200 <= status_code < 300:
        logger.info(f"API Call exitoso: {method} {url} - {status_code}", extra=log_data)
    else:
        logger.warning(
            f"API Call fallido: {method} {url} - {status_code}", extra=log_data
        )


def log_validation_error(
    logger: logging.Logger,
    field: str,
    value: Any,
    error_message: str,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log estructurado para errores de validación

    Args:
        logger: Logger instance
        field: Campo con error
        value: Valor que causó el error
        error_message: Mensaje de error
        extra: Datos adicionales
    """
    log_data = {
        "validation_error": True,
        "field": field,
        "value": str(value),
        "error_message": error_message,
        **(extra or {}),
    }

    logger.warning(
        f"Error de validación en campo '{field}': {error_message}", extra=log_data
    )
