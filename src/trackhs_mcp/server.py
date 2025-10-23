"""
FastMCP Cloud entrypoint for TrackHS MCP Connector
This file is required by FastMCP Cloud deployment
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Agregar el directorio src al PYTHONPATH para que FastMCP pueda encontrar el módulo
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# También agregar el directorio raíz del proyecto
project_root = src_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.prompts import register_all_prompts
from trackhs_mcp.infrastructure.tools.registry import register_all_tools
from trackhs_mcp.infrastructure.tools.resources import register_all_resources

# Load environment variables
load_dotenv()

# Create dependencies
config = TrackHSConfig.from_env()
api_client = TrackHSApiClient(config)

# Create MCP server instance
from fastmcp import FastMCP

mcp = FastMCP(
    name="TrackHS MCP Server",
    mask_error_details=False,
    include_fastmcp_meta=True,
)

# Register all components
register_all_tools(mcp, api_client)
register_all_resources(mcp, api_client)
register_all_prompts(mcp, api_client)

# Start the server
if __name__ == "__main__":
    # Especificar transport="http" para compatibilidad con ElevenLabs y FastMCP Cloud
    mcp.run(transport="http")
