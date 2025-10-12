"""
Examples module - Exporta todos los example resources
"""

from .folio_examples import register_folio_examples
from .search_examples import register_search_examples


def register_example_resources(mcp, api_client):
    """Registra todos los example resources"""
    register_search_examples(mcp, api_client)
    register_folio_examples(mcp, api_client)
