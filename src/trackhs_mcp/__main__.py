"""
TrackHS MCP Server - Entry Point
Punto de entrada para FastMCP Cloud
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importaciones
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from trackhs_mcp.server import mcp

if __name__ == "__main__":
    # HTTP transport según fastmcp.json
    mcp.run(transport="http", host="0.0.0.0", port=8080)
