"""
Documentation module - Exporta todos los documentation resources
"""

from .amenities_api import register_amenities_api_documentation
from .api_v2 import register_api_v2_documentation
from .folio_api import register_folio_api_documentation
from .work_orders_api import register_work_orders_api_documentation


def register_documentation_resources(mcp, api_client):
    """Registra todos los documentation resources"""
    register_api_v2_documentation(mcp, api_client)
    register_folio_api_documentation(mcp, api_client)
    register_amenities_api_documentation(mcp, api_client)
    register_work_orders_api_documentation(mcp, api_client)
