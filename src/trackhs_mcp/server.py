"""
FastMCP Cloud entrypoint for TrackHS MCP Connector
This file is required by FastMCP Cloud deployment
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

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
from trackhs_mcp.infrastructure.mcp.server import register_all_components

# Load environment variables
load_dotenv()

# Create dependencies
config = TrackHSConfig.from_env()
api_client = TrackHSApiClient(config)

# Create MCP server instance
mcp = FastMCP("TrackHS MCP Server")

# Register all components
register_all_components(mcp, api_client)

# Start the server
if __name__ == "__main__":
    mcp.run()
