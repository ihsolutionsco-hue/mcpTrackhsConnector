"""
TrackHS MCP Connector - Python Package

Servidor MCP para Track HS API implementado con FastMCP.
Proporciona herramientas, resources y prompts para interactuar con la API de Track HS.
"""

__version__ = "1.0.2"
__author__ = "Track HS Team"
__email__ = "team@trackhs.com"

# Imports para compatibilidad
from .domain.value_objects.config import TrackHSConfig

__all__ = ["TrackHSConfig"]
