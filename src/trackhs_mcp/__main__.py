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
from fastmcp.exceptions import ResourceError, ToolError
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

# Agregar el directorio src al PYTHONPATH para que FastMCP pueda encontrar el módulo
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.server import register_all_components

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

        # Create MCP server instance with error masking for production
        logger.info("Creando servidor MCP...")
        mcp = FastMCP("TrackHS MCP Server", mask_error_details=True)

        # Add middleware for error handling
        logger.info("Agregando middleware...")
        mcp.add_middleware(
            ErrorHandlingMiddleware(
                include_traceback=False, transform_errors=True  # En producción
            )
        )

        # Register all components
        logger.info("Registrando componentes...")
        register_all_components(mcp, api_client)

        logger.info("Servidor MCP configurado correctamente")
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
