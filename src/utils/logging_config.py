"""
Configuración avanzada de logging para debugging
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from pythonjsonlogger import jsonlogger


class TrackHSLogFormatter(jsonlogger.JsonFormatter):
    """Formateador JSON personalizado para logs de TrackHS"""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Agregar campos estándar de TrackHS
        log_record["service"] = "trackhs-mcp-connector"
        log_record["version"] = "2.0.0"

        # Agregar timestamp en formato ISO
        if not hasattr(log_record, "timestamp"):
            log_record["timestamp"] = record.created

        # Agregar nivel de log
        log_record["level"] = record.levelname

        # Agregar logger name
        log_record["logger"] = record.name


def setup_logging(
    level: str = "INFO", log_file: Optional[str] = None, console_output: bool = True
) -> logging.Logger:
    """
    Configura el sistema de logging para TrackHS MCP Connector

    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Archivo de log (opcional)
        console_output: Si mostrar logs en consola

    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Limpiar handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configurar formateador JSON
    json_formatter = TrackHSLogFormatter(
        "%(timestamp)s %(level)s %(logger)s %(message)s"
    )

    # Handler para consola
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(json_formatter)
        console_handler.setLevel(getattr(logging, level.upper()))
        root_logger.addHandler(console_handler)

    # Handler para archivo
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(json_formatter)
        file_handler.setLevel(getattr(logging, level.upper()))
        root_logger.addHandler(file_handler)

    return root_logger


def get_debug_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para debugging

    Args:
        name: Nombre del logger

    Returns:
        Logger configurado para debugging
    """
    logger = logging.getLogger(name)

    # Configurar nivel DEBUG si no está configurado
    if logger.level == logging.NOTSET:
        logger.setLevel(logging.DEBUG)

    return logger


def log_api_call(logger: logging.Logger, method: str, endpoint: str, **kwargs):
    """
    Log especializado para llamadas a API

    Args:
        logger: Logger a usar
        method: Método HTTP
        endpoint: Endpoint de la API
        **kwargs: Parámetros adicionales
    """
    logger.info(
        f"API Call: {method} {endpoint}",
        extra={"api_call": True, "method": method, "endpoint": endpoint, **kwargs},
    )


def log_search_operation(logger: logging.Logger, operation: str, **kwargs):
    """
    Log especializado para operaciones de búsqueda

    Args:
        logger: Logger a usar
        operation: Tipo de operación
        **kwargs: Parámetros adicionales
    """
    logger.info(
        f"Search Operation: {operation}",
        extra={"search_operation": True, "operation": operation, **kwargs},
    )


def log_debugging_metrics(logger: logging.Logger, metrics: dict):
    """
    Log especializado para métricas de debugging

    Args:
        logger: Logger a usar
        metrics: Diccionario de métricas
    """
    logger.info(
        "Debugging Metrics", extra={"debugging_metrics": True, "metrics": metrics}
    )
