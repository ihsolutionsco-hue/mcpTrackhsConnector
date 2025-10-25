"""
TrackHS MCP Server - Entry Point
Punto de entrada para FastMCP Cloud
"""

from .server import mcp

if __name__ == "__main__":
    # HTTP transport según fastmcp.json
    mcp.run(transport="http", host="0.0.0.0", port=8080)
