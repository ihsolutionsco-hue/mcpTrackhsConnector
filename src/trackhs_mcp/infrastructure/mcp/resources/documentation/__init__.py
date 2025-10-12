"""
Documentation module - Exporta todos los documentation resources
"""

from .api_v1 import register_api_v1_documentation
from .api_v2 import register_api_v2_documentation
from .folio_api import register_folio_api_documentation


def register_documentation_resources(mcp, api_client):
    """Registra todos los documentation resources"""
    register_api_v1_documentation(mcp, api_client)
    register_api_v2_documentation(mcp, api_client)
    register_folio_api_documentation(mcp, api_client)
