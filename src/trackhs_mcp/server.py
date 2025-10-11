"""
Servidor FastMCP principal para Track HS API
"""

import os
import sys
from pathlib import Path
from fastmcp import FastMCP

# Agregar el directorio src al path para importaciones absolutas
sys.path.insert(0, str(Path(__file__).parent.parent))

from trackhs_mcp.core.api_client import TrackHSApiClient
from trackhs_mcp.core.types import TrackHSConfig

# Configurar cliente API
config = TrackHSConfig(
    base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
    username=os.getenv("TRACKHS_USERNAME", "test_user"),
    password=os.getenv("TRACKHS_PASSWORD", "test_password"),
    timeout=int(os.getenv("TRACKHS_TIMEOUT", "30"))
)

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
