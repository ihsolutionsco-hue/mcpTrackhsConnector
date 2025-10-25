"""
Configuración centralizada de logging para TrackHS MCP Server
Proporciona configuración consistente para FastMCP Cloud
"""

import logging
import os
import sys
from typing import Optional


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configura el sistema de logging para TrackHS MCP Server

    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger configurado
    """
    # Obtener nivel de logging
    if log_level is None:
        log_level = os.getenv("FASTMCP_LOG_LEVEL", "INFO").upper()

    # Convertir string a nivel de logging
    numeric_level = getattr(logging, log_level, logging.INFO)

    # Configurar formato de logging
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configurar logging básico
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,  # Forzar reconfiguración
    )

    # Configurar loggers específicos
    loggers_to_configure = [
        "trackhs_mcp",
        "fastmcp",
        "fastmcp.server",
        "fastmcp.server.middleware",
        "fastmcp.server.tools",
        "fastmcp.server.resources",
        "fastmcp.server.prompts",
    ]

    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(numeric_level)

        # Asegurar que no se propague a handlers superiores
        logger.propagate = False

        # Agregar handler si no tiene uno
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter(log_format))
            logger.addHandler(handler)

    # Logger principal
    main_logger = logging.getLogger("trackhs_mcp")
    main_logger.info(f"Logging configurado con nivel: {log_level}")

    return main_logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado

    Args:
        name: Nombre del logger

    Returns:
        Logger configurado
    """
    return logging.getLogger(f"trackhs_mcp.{name}")


def log_mcp_request(method: str, params: dict = None, logger: logging.Logger = None):
    """
    Log específico para requests MCP

    Args:
        method: Método MCP llamado
        params: Parámetros de la llamada
        logger: Logger a usar
    """
    if logger is None:
        logger = get_logger("mcp")

    log_data = {"method": method, "type": "mcp_request"}

    if params:
        # Sanitizar parámetros sensibles
        sanitized_params = {}
        sensitive_keys = {"password", "token", "secret", "key", "auth"}

        for key, value in params.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized_params[key] = "[REDACTED]"
            else:
                sanitized_params[key] = value

        log_data["params"] = sanitized_params

    logger.info(f"MCP Request: {method}", extra=log_data)


def log_mcp_response(
    method: str,
    execution_time: float,
    result_type: str = None,
    logger: logging.Logger = None,
):
    """
    Log específico para responses MCP

    Args:
        method: Método MCP
        execution_time: Tiempo de ejecución en segundos
        result_type: Tipo de resultado
        logger: Logger a usar
    """
    if logger is None:
        logger = get_logger("mcp")

    log_data = {
        "method": method,
        "execution_time": execution_time,
        "type": "mcp_response",
    }

    if result_type:
        log_data["result_type"] = result_type

    logger.info(f"MCP Response: {method} ({execution_time:.3f}s)", extra=log_data)


def log_mcp_error(
    method: str, error: Exception, execution_time: float, logger: logging.Logger = None
):
    """
    Log específico para errores MCP

    Args:
        method: Método MCP
        error: Excepción ocurrida
        execution_time: Tiempo de ejecución en segundos
        logger: Logger a usar
    """
    if logger is None:
        logger = get_logger("mcp")

    log_data = {
        "method": method,
        "execution_time": execution_time,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "type": "mcp_error",
    }

    logger.error(
        f"MCP Error: {method} - {type(error).__name__}: {error}", extra=log_data
    )
