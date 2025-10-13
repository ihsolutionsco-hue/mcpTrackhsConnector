"""
Registrador de herramientas MCP simplificado para Track HS API V1 y V2
Solo incluye las herramientas esenciales basadas en la documentación oficial
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from .get_folio import register_get_folio
from .get_reservation_v2 import register_get_reservation_v2

# Importar solo las herramientas V1 y V2
from .search_reservations_v1 import register_search_reservations_v1
from .search_reservations_v2 import register_search_reservations_v2
from .search_units import register_search_units
from .search_units_from_reservations import register_search_units_from_reservations


def register_all_tools(mcp, api_client: "ApiClientPort"):
    """
    Registra las herramientas MCP esenciales para Track HS.

    **Herramientas Incluidas:**
    - search_reservations_v1 (API V1 - endpoint /pms/reservations)
    - search_reservations_v2 (API V2 - endpoint /v2/pms/reservations)
    - get_reservation_v2 (API V2 - endpoint /v2/pms/reservations/{id})
    - get_folio (API - endpoint /pms/folios/{id})
    - search_units (Channel API - endpoint /pms/units) - PROBLEMA: 400 Bad Request
    - search_units_from_reservations (ALTERNATIVA - usa datos embebidos de reservaciones)

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar solo las herramientas V1 y V2
    register_search_reservations_v1(mcp, api_client)
    register_search_reservations_v2(mcp, api_client)
    register_get_reservation_v2(mcp, api_client)
    register_get_folio(mcp, api_client)

    # Registrar ambas herramientas de units
    register_search_units(mcp, api_client)  # Original (con problemas)
    register_search_units_from_reservations(mcp, api_client)  # Alternativa (funcional)
