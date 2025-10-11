"""
Entry point principal para TrackHS MCP Connector
Implementa inyección de dependencias siguiendo Clean Architecture
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.server import register_all_components

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def create_dependencies():
    """Crear y configurar todas las dependencias"""
    # Configuración
    config = TrackHSConfig.from_env()

    # Validar URL
    if not config.validate_url():
        print(
            f"ADVERTENCIA: URL configurada ({config.base_url}) "
            f"no es la URL oficial de IHVM"
        )
        print(f"   URL oficial: {TrackHSConfig.DEFAULT_URL}")
        print("   Configura TRACKHS_API_URL en .env si necesitas usar otra URL")

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


if __name__ == "__main__":
    main()
