"""
Servidor FastMCP principal para Track HS API
"""

import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from .core.api_client import TrackHSApiClient
from .core.types import TrackHSConfig

# Cargar variables de entorno
load_dotenv()

# Configurar cliente API
config = TrackHSConfig(
    base_url=os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api"),
    username=os.getenv("TRACKHS_USERNAME", ""),
    password=os.getenv("TRACKHS_PASSWORD", ""),
    timeout=int(os.getenv("TRACKHS_TIMEOUT", "30"))
)

# Crear cliente API
api_client = TrackHSApiClient(config)

# Crear servidor FastMCP
mcp = FastMCP("TrackHS MCP Server")

# Registrar todas las herramientas, resources y prompts
def register_all_components():
    """Registra todos los componentes del servidor MCP"""
    from .tools import register_all_tools
    from .resources import register_all_resources
    from .prompts import register_all_prompts
    
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
