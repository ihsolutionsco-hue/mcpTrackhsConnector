"""
Schemas module - Exporta todos los schemas de resources
"""

from .folio import register_folio_schema
from .reservation_detail_v2 import register_reservation_detail_v2_schema
from .reservations_v1 import register_reservations_v1_schema
from .reservations_v2 import register_reservations_v2_schema
from .units import register_units_schema


def register_schema_resources(mcp, api_client):
    """Registra todos los schema resources"""
    register_reservations_v1_schema(mcp, api_client)
    register_reservations_v2_schema(mcp, api_client)
    register_reservation_detail_v2_schema(mcp, api_client)
    register_folio_schema(mcp, api_client)
    register_units_schema(mcp, api_client)
