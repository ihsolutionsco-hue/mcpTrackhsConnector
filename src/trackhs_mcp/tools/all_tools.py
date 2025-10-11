"""
Registrador de herramientas MCP para Track HS API V1 y V2
Registra las herramientas search_reservations V1 y V2
"""

from trackhs_mcp.core.api_client import TrackHSApiClient

# Importar las herramientas search_reservations V1 y V2
from trackhs_mcp.tools.search_reservations import register_search_reservations
from trackhs_mcp.tools.search_reservations_v1 import register_search_reservations_v1


def register_all_tools(mcp, api_client: TrackHSApiClient):
    """
    Registra las herramientas search_reservations V1 y V2 con el cliente API

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar la herramienta search_reservations V2
    register_search_reservations(mcp, api_client)

    # Registrar la herramienta search_reservations V1
    register_search_reservations_v1(mcp, api_client)
