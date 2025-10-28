"""
TrackHS MCP Connector - Arquitectura FastMCP

Un conector MCP (Model Context Protocol) para interactuar con la API de TrackHS.
Arquitectura simplificada siguiendo las mejores prácticas de FastMCP.

Proporciona herramientas para:
- Buscar y consultar reservas
- Gestionar unidades de alojamiento
- Consultar amenidades disponibles
- Obtener información financiera (folios)
- Crear órdenes de trabajo (mantenimiento y housekeeping)
"""

__version__ = "2.0.0"
__author__ = "IHSolutions"
__email__ = "ihsolutionsco@gmail.com"

# Export principal del servidor MCP
from .server import mcp

__all__ = ["mcp"]
