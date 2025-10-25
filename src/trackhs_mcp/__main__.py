"""
FastMCP Cloud entrypoint for TrackHS MCP Connector
This file is required by FastMCP Cloud deployment
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

# Agregar el directorio src al PYTHONPATH para que FastMCP pueda encontrar el módulo
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Configurar logging estándar para FastMCP Cloud
import logging

# Configurar logging específico para FastMCP Cloud
import sys

# Usar middleware nativo de FastMCP
from fastmcp.server.middleware.logging import (
    LoggingMiddleware,
    StructuredLoggingMiddleware,
)
from fastmcp.server.middleware.timing import TimingMiddleware

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.middleware import TrackHSErrorHandlingMiddleware
from trackhs_mcp.infrastructure.prompts import register_all_prompts
from trackhs_mcp.infrastructure.tools.registry import register_all_tools
from trackhs_mcp.infrastructure.tools.resources import register_all_resources

# Configurar logging simple para FastMCP Cloud
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Función principal para el servidor MCP"""
    try:
        # Load environment variables
        load_dotenv()

        logger.info("Iniciando TrackHS MCP Server...")

        # Validar variables de entorno críticas
        required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            logger.error(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
            logger.error("Configura las variables de entorno en FastMCP Cloud")
            sys.exit(1)

        # Create dependencies
        logger.info("Creando configuración...")
        config = TrackHSConfig.from_env()

        logger.info("Inicializando cliente API...")
        api_client = TrackHSApiClient(config)

        # Create MCP server instance with FastMCP best practices
        logger.info("Creando servidor MCP...")

        # Usar variables de entorno estándar de FastMCP
        mask_error_details = (
            os.getenv("FASTMCP_MASK_ERROR_DETAILS", "false").lower() == "true"
        )
        include_fastmcp_meta = (
            os.getenv("FASTMCP_INCLUDE_FASTMCP_META", "true").lower() == "true"
        )
        strict_input_validation = (
            os.getenv("FASTMCP_STRICT_INPUT_VALIDATION", "true").lower() == "true"
        )

        mcp = FastMCP(
            name="TrackHS MCP Server",
            mask_error_details=mask_error_details,
            include_fastmcp_meta=include_fastmcp_meta,
        )

        # Register all components
        logger.info("Registrando componentes...")
        register_all_tools(mcp, api_client)
        register_all_resources(mcp, api_client)
        register_all_prompts(mcp, api_client)

        # Configure logging level from environment
        log_level = os.getenv("FASTMCP_LOG_LEVEL", "INFO").upper()
        logger.info(f"Configurando logging con nivel: {log_level}")

        # Add middleware (order matters: logging first, then error handling)
        logger.info("Configurando middleware...")

        # Usar solo middleware esencial
        mcp.add_middleware(TimingMiddleware())
        mcp.add_middleware(LoggingMiddleware())

        # Error handling middleware personalizado
        error_middleware = TrackHSErrorHandlingMiddleware(
            include_traceback=os.getenv("FASTMCP_INCLUDE_TRACEBACK", "false").lower()
            == "true",
            transform_errors=True,
        )
        mcp.add_middleware(error_middleware)

        logger.info(f"Servidor MCP configurado correctamente (log_level={log_level})")

        # Log básico para debugging
        logger.info(f"Servidor configurado: {mcp.name}")
        logger.info(f"FastMCP Version: {__import__('fastmcp').__version__}")
        logger.info("Middleware configurado correctamente")

        return mcp

    except Exception as e:
        logger.error(f"Error al inicializar el servidor: {e}")
        sys.exit(1)


# Crear instancia del servidor
mcp = main()

# Start the server
if __name__ == "__main__":
    try:
        logger.info("Iniciando servidor MCP...")
        logger.info(f"Servidor: {mcp.name}")
        logger.info("Transport: HTTP")

        # FastMCP Cloud maneja automáticamente el transporte HTTP
        mcp.run(transport="http")
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el servidor: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
