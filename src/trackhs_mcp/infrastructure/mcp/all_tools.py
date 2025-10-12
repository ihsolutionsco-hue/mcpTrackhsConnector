"""
Registrador de herramientas MCP simplificado para Track HS API V1 y V2
Solo incluye las herramientas esenciales basadas en la documentación oficial
"""

from ...application.ports.api_client_port import ApiClientPort
from .get_reservation_v2 import register_get_reservation_v2

# Importar solo las herramientas V1 y V2
from .search_reservations_v1 import register_search_reservations_v1
from .search_reservations_v2 import register_search_reservations_v2


def register_all_tools(mcp, api_client: ApiClientPort):
    """
    Registra las herramientas MCP esenciales para Track HS.

    **Herramientas Incluidas:**
    - search_reservations_v1 (API V1 - endpoint /pms/reservations)
    - search_reservations_v2 (API V2 - endpoint /v2/pms/reservations)

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar solo las herramientas V1 y V2
    register_search_reservations_v1(mcp, api_client)
    register_search_reservations_v2(mcp, api_client)
    register_get_reservation_v2(mcp, api_client)
