"""
Resources module - Exporta todos los resources MCP organizados por categoría
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_all_resources(mcp, api_client: "ApiClientPort"):
    """Registra todos los resources MCP organizados por categoría"""
    from .documentation import register_documentation_resources
    from .examples import register_example_resources
    from .references import register_reference_resources
    from .schemas import register_schema_resources

    # Registrar resources por categoría
    register_schema_resources(mcp, api_client)
    register_documentation_resources(mcp, api_client)
    register_reference_resources(mcp, api_client)
    register_example_resources(mcp, api_client)
