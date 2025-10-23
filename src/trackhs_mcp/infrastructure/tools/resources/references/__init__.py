"""
References module - Exporta todos los reference resources
"""

from .date_formats import register_date_formats
from .error_codes import register_error_codes
from .status_values import register_status_values


def register_reference_resources(mcp, api_client):
    """Registra todos los reference resources"""
    register_status_values(mcp, api_client)
    register_date_formats(mcp, api_client)
    register_error_codes(mcp, api_client)
