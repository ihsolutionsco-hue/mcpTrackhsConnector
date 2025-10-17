"""
Examples module - Exporta todos los example resources
"""

from .amenities_examples import register_amenities_examples
from .folio_examples import register_folio_examples
from .search_examples import register_search_examples
from .work_orders_examples import register_work_orders_examples


def register_example_resources(mcp, api_client):
    """Registra todos los example resources"""
    register_search_examples(mcp, api_client)
    register_folio_examples(mcp, api_client)
    register_amenities_examples(mcp, api_client)
    register_work_orders_examples(mcp, api_client)
