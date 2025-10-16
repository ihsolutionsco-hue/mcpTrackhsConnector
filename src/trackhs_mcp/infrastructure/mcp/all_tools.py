"""
Registrador de herramientas MCP simplificado para Track HS API V1 y V2
Solo incluye las herramientas esenciales basadas en la documentación oficial
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from .create_maintenance_work_order import register_create_maintenance_work_order
from .get_folio import register_get_folio
from .get_reservation_v2 import register_get_reservation_v2

# Importar herramientas
from .search_amenities import register_search_amenities
from .search_reservations_v2 import register_search_reservations_v2
from .search_units import register_search_units


def register_all_tools(mcp, api_client: "ApiClientPort"):
    """
    Registra las herramientas MCP esenciales para Track HS.

    **Herramientas Incluidas:**
    - search_reservations (API V2 - endpoint /v2/pms/reservations)
    - get_reservation (API V2 - endpoint /v2/pms/reservations/{id})
    - get_folio (API - endpoint /pms/folios/{id})
    - search_units (Channel API - endpoint /pms/units)
    - search_amenities (Channel API - endpoint /pms/units/amenities)
    - create_maintenance_work_order (API - endpoint /pms/maintenance/work-orders)

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar herramientas
    register_search_reservations_v2(
        mcp, api_client
    )  # Expone como "search_reservations"
    register_get_reservation_v2(mcp, api_client)  # Expone como "get_reservation"
    register_get_folio(mcp, api_client)  # Expone como "get_folio"
    register_search_units(mcp, api_client)  # Expone como "search_units"
    register_search_amenities(mcp, api_client)  # Expone como "search_amenities"
    register_create_maintenance_work_order(
        mcp, api_client
    )  # Expone como "create_maintenance_work_order"
