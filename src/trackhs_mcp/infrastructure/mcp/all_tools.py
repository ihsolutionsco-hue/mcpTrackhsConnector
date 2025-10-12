"""
Registrador de herramientas MCP mejorado para Track HS API V1 y V2
Incluye herramientas optimizadas, recursos dinámicos y prompts especializados
Siguiendo las mejores prácticas MCP para servidores empresariales
"""

from ...application.ports.api_client_port import ApiClientPort

# Importar recursos mejorados
from .resources_enhanced import register_enhanced_resources

# Importar las herramientas básicas
from .search_reservations import register_search_reservations
from .search_reservations_advanced import register_search_reservations_advanced

# Importar las herramientas mejoradas
from .search_reservations_enhanced import (
    register_metrics_tool,
    register_search_reservations_enhanced,
)
from .search_reservations_v1 import register_search_reservations_v1


def register_all_tools(mcp, api_client: ApiClientPort):
    """
    Registra todas las herramientas MCP mejoradas para Track HS.

    **Herramientas Incluidas:**
    - search_reservations (V2 básico)
    - search_reservations_v1 (V1 básico)
    - search_reservations_enhanced (V2 optimizado)
    - search_reservations_advanced (V2 avanzado)
    - Herramientas de métricas y caché
    - Recursos dinámicos
    - Prompts especializados

    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar herramientas básicas (compatibilidad)
    register_search_reservations(mcp, api_client)
    register_search_reservations_v1(mcp, api_client)

    # Registrar herramientas mejoradas
    register_search_reservations_enhanced(mcp, api_client)
    register_search_reservations_advanced(mcp, api_client)

    # Registrar herramientas de utilidad
    register_metrics_tool(mcp)

    # Registrar recursos mejorados
    register_enhanced_resources(mcp, api_client)

    # Los prompts se registran en register_all_prompts
