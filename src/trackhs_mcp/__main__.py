"""
Entry point principal para TrackHS MCP Connector
Implementa inyección de dependencias siguiendo Clean Architecture
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Cargar variables de entorno
load_dotenv()

# Imports absolutos después de agregar al path
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig  # noqa: E402
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import (  # noqa: E402
    TrackHSApiClient,
)
from trackhs_mcp.infrastructure.mcp.server import register_all_components  # noqa: E402
from trackhs_mcp.infrastructure.utils.logging import get_logger  # noqa: E402

logger = get_logger(__name__)


def create_dependencies():
    """Crear y configurar todas las dependencias"""
    # Configuración
    config = TrackHSConfig.from_env()

    # Validar URL
    if not config.validate_url():
        logger.warning(
            f"URL configurada ({config.base_url}) no es la URL oficial de IHVM"
        )
        logger.warning(f"URL oficial: {TrackHSConfig.DEFAULT_URL}")
        logger.warning("Configura TRACKHS_API_URL en .env si necesitas usar otra URL")

    # Cliente API
    api_client = TrackHSApiClient(config)

    return config, api_client


def main():
    """Función principal con inyección de dependencias"""
    # Crear dependencias
    config, api_client = create_dependencies()

    # Crear servidor MCP
    mcp = FastMCP("TrackHS MCP Server")

    # Registrar componentes con inyección de dependencias
    register_all_components(mcp, api_client)

    # Ejecutar servidor
    mcp.run()


# Crear instancia del servidor para FastMCP Cloud
try:
    # Crear dependencias
    config, api_client = create_dependencies()

    # Crear servidor MCP
    mcp = FastMCP("TrackHS MCP Server")

    # Registrar componentes con inyección de dependencias
    register_all_components(mcp, api_client)
except Exception as e:
    # Si hay error en la inicialización, crear un servidor vacío
    logger.error(f"Error inicializando servidor: {e}")
    mcp = FastMCP("TrackHS MCP Server")


if __name__ == "__main__":
    main()
