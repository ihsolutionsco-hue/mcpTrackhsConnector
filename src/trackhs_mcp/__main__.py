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

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.server import register_all_components
from trackhs_mcp.infrastructure.middleware import (
    TrackHSErrorHandlingMiddleware,
    TrackHSLoggingMiddleware,
)

# Configurar logging
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

        # Create MCP server instance with strict validation
        logger.info("Creando servidor MCP...")
        mcp = FastMCP(
            name="TrackHS MCP Server",
            strict_input_validation=True,  # Validación estricta de parámetros
            mask_error_details=False,  # Mostrar detalles de error en desarrollo
            include_fastmcp_meta=True,  # Incluir metadatos FastMCP
        )

        # Register all components
        logger.info("Registrando componentes...")
        register_all_components(mcp, api_client)

        # Configure logging level from environment
        log_level = os.getenv("FASTMCP_LOG_LEVEL", "INFO").upper()
        logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

        # Add middleware (order matters: logging first, then error handling)
        logger.info("Configurando middleware...")

        # Logging middleware
        logging_middleware = TrackHSLoggingMiddleware(
            log_requests=True, log_responses=True, log_timing=True, log_level=log_level
        )
        mcp.add_middleware(logging_middleware)

        # Error handling middleware
        error_middleware = TrackHSErrorHandlingMiddleware(
            include_traceback=os.getenv("FASTMCP_INCLUDE_TRACEBACK", "false").lower()
            == "true",
            transform_errors=True,
        )
        mcp.add_middleware(error_middleware)

        logger.info(f"Servidor MCP configurado correctamente (log_level={log_level})")
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

        # FastMCP Cloud maneja automáticamente el transporte HTTP
        # Especificamos transport="http" para compatibilidad con ElevenLabs y FastMCP Cloud
        # La configuración de host, puerto y CORS está en fastmcp.yaml
        mcp.run(transport="http")
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el servidor: {e}")
        sys.exit(1)
