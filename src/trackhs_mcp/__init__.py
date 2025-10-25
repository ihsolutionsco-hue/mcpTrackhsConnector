"""
TrackHS MCP Connector v2.0 - FastMCP Native

Servidor MCP simplificado para Track HS API usando FastMCP nativo.
Elimina Clean Architecture y usa estructura minimalista.
"""

__version__ = "2.0.0"
__author__ = "Track HS Team"
__email__ = "team@trackhs.com"

# FastMCP native imports
from .config import settings
from .client import trackhs_client

__all__ = ["settings", "trackhs_client"]