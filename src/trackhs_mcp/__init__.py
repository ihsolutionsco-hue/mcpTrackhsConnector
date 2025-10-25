"""
TrackHS MCP Connector - Python Package

Servidor MCP simple para TrackHS API implementado con FastMCP.
Proporciona herramientas para interactuar con la API de TrackHS.
"""

__version__ = "2.0.0"
__author__ = "Track HS Team"
__email__ = "team@trackhs.com"

# Imports para compatibilidad
from .server import mcp

__all__ = ["mcp"]
