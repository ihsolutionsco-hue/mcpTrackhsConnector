"""
Registrador de herramientas MCP para Track HS API V1 y V2
Registra únicamente las herramientas search_reservations V1 y V2
Siguiendo las mejores prácticas MCP para servidores enfocados
"""

from ...application.ports.api_client_port import ApiClientPort

# Importar las herramientas search_reservations V1 y V2
from .search_reservations import register_search_reservations
from .search_reservations_v1 import register_search_reservations_v1


def register_all_tools(mcp, api_client: ApiClientPort):
    """
    Registra las herramientas search_reservations V1 y V2 con el cliente API.

    Este servidor MCP está enfocado únicamente en la búsqueda de reservas,
    siguiendo las mejores prácticas de simplicidad y mantenibilidad.

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar la herramienta search_reservations V2 (principal)
    register_search_reservations(mcp, api_client)

    # Registrar la herramienta search_reservations V1 (compatibilidad legacy)
    register_search_reservations_v1(mcp, api_client)
