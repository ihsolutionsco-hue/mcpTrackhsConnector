"""
TrackHS MCP Connector - Python Package

Servidor MCP para Track HS API implementado con FastMCP.
Proporciona herramientas, resources y prompts para interactuar con la API de Track HS.
"""

__version__ = "1.0.0"
__author__ = "Track HS Team"
__email__ = "team@trackhs.com"

# Imports para compatibilidad
from .infrastructure.adapters.config import TrackHSConfig
from .infrastructure.adapters.trackhs_api_client import TrackHSApiClient

__all__ = ["TrackHSConfig", "TrackHSApiClient"]
