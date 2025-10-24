"""
Registrador de herramientas MCP simplificado para Track HS API V1 y V2
Solo incluye las herramientas esenciales basadas en la documentación oficial
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from .create_housekeeping_work_order import register_create_housekeeping_work_order
from .create_maintenance_work_order import register_create_maintenance_work_order
from .get_folio import register_get_folio
from .get_reservation_v2 import register_get_reservation_v2
from .search_amenities import register_search_amenities
from .search_reservations_v2 import register_search_reservations_v2
from .search_units import register_search_units


def register_all_tools(mcp, api_client: "ApiClientPort"):
    """
    Registra las herramientas MCP esenciales para Track HS.

    **Herramientas Incluidas:**
    - search_reservations (API V2 - endpoint /api/v2/pms/reservations)
    - get_reservation (API V2 - endpoint /api/v2/pms/reservations/{id})
    - get_folio (API - endpoint /api/pms/folios/{id})
    - search_units (Channel API - endpoint /api/pms/units)
    - search_amenities (Channel API - endpoint /api/pms/units/amenities)
    - create_maintenance_work_order (API - endpoint /api/pms/maintenance/work-orders)
    - create_housekeeping_work_order (API - endpoint /api/pms/housekeeping/work-orders)

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS

    Raises:
        TypeError: Si api_client es None
        AttributeError: Si api_client no tiene los métodos requeridos
    """
    if api_client is None:
        raise TypeError("api_client cannot be None")

    # Verificar que api_client tiene los métodos requeridos
    required_methods = ["get", "post"]
    for method in required_methods:
        if not hasattr(api_client, method):
            raise AttributeError(f"api_client must have '{method}' method")

    # Verificar que los métodos son callable
    for method in required_methods:
        if not callable(getattr(api_client, method)):
            raise AttributeError(f"api_client.{method} must be callable")

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
    register_create_housekeeping_work_order(
        mcp, api_client
    )  # Expone como "create_housekeeping_work_order"
