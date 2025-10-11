"""
Registrador de herramientas MCP para Track HS API V2
Solo registra la herramienta search_reservations V2
"""

from trackhs_mcp.core.api_client import TrackHSApiClient

# Importar solo la herramienta search_reservations V2
from trackhs_mcp.tools.search_reservations import register_search_reservations


def register_all_tools(mcp, api_client: TrackHSApiClient):
    """
    Registra la herramienta search_reservations V2 con el cliente API

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar solo la herramienta search_reservations V2
    register_search_reservations(mcp, api_client)
