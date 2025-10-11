"""
Servidor FastMCP principal para Track HS API
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env PRIMERO
load_dotenv()

# Agregar el directorio src al path para importaciones absolutas
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastmcp import FastMCP

from trackhs_mcp.core.api_client import TrackHSApiClient
from trackhs_mcp.core.types import TrackHSConfig
from trackhs_mcp.config import TrackHSConfig as CentralizedConfig

# Configurar cliente API usando configuración centralizada
config = CentralizedConfig.from_env()

# Validar que la URL sea la correcta
if not config.validate_url():
    print(f"ADVERTENCIA: URL configurada ({config.base_url}) no es la URL oficial de IHVM")
    print(f"   URL oficial: {CentralizedConfig.DEFAULT_URL}")
    print(f"   Configura TRACKHS_API_URL en .env si necesitas usar otra URL")

# Crear cliente API
api_client = TrackHSApiClient(config)

# Crear servidor FastMCP
mcp = FastMCP("TrackHS MCP Server")

# Registrar todas las herramientas, resources y prompts
def register_all_components():
    """Registra todos los componentes del servidor MCP"""
    from trackhs_mcp.tools import register_all_tools
    from trackhs_mcp.resources import register_all_resources
    from trackhs_mcp.prompts import register_all_prompts
    
    # Registrar herramientas
    register_all_tools(mcp, api_client)
    
    # Registrar resources
    register_all_resources(mcp, api_client)
    
    # Registrar prompts
    register_all_prompts(mcp, api_client)

# Registrar componentes
register_all_components()

def main():
    """Función principal para ejecutar el servidor"""
    mcp.run()

if __name__ == "__main__":
    main()
