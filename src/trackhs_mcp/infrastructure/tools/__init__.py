"""
Herramientas MCP para TrackHS MCP Connector
Implementa todas las herramientas MCP siguiendo el protocolo FastMCP
"""

from .registry import register_all_tools

__all__ = ["register_all_tools"]
