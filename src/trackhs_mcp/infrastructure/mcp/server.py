"""
Servidor FastMCP principal para Track HS API
Implementa inyección de dependencias
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort


def register_all_components(mcp, api_client: "ApiClientPort"):
    """Registra todos los componentes del servidor MCP con inyección de dependencias"""
    from .all_tools import register_all_tools
    from .prompts import register_all_prompts
    from .resources import register_all_resources

    # Registrar herramientas
    register_all_tools(mcp, api_client)

    # Registrar resources
    register_all_resources(mcp, api_client)

    # Registrar prompts
    register_all_prompts(mcp, api_client)
