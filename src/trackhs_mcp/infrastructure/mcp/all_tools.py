"""
Registrador de herramientas MCP simplificado para Track HS API V1 y V2
Solo incluye las herramientas esenciales basadas en la documentación oficial
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from .search_amenities import register_search_amenities
from .search_units import register_search_units


def register_all_tools(mcp, api_client: "ApiClientPort"):
    """
    Registra las herramientas MCP esenciales para Track HS.

    **Herramientas Incluidas:**
    - search_units (Channel API - endpoint /pms/units)
    - search_amenities (Channel API - endpoint /pms/units/amenities)

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar herramientas
    register_search_units(mcp, api_client)  # Expone como "search_units"
    register_search_amenities(mcp, api_client)  # Expone como "search_amenities"
