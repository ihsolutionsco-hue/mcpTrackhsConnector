"""
Schemas module - Exporta todos los schemas de resources
"""

from .amenities import register_amenities_schema
from .folio import register_folio_schema
from .reservation_detail_v2 import register_reservation_detail_v2_schema
from .reservations_v2 import register_reservations_v2_schema
from .units import register_units_schema
from .work_orders import register_work_orders_schema


def register_schema_resources(mcp, api_client):
    """Registra todos los schema resources"""
    register_reservations_v2_schema(mcp, api_client)
    register_reservation_detail_v2_schema(mcp, api_client)
    register_folio_schema(mcp, api_client)
    register_units_schema(mcp, api_client)
    register_amenities_schema(mcp, api_client)
    register_work_orders_schema(mcp, api_client)
