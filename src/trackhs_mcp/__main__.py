"""
TrackHS MCP Server - Entry Point
Punto de entrada para FastMCP Cloud
"""

import logging
import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importaciones
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

# Configurar logging básico para FastMCP Cloud
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

try:
    from trackhs_mcp.simple_server import mcp

    logger.info("TrackHS Simple MCP Server importado correctamente")
except Exception as e:
    logger.error(f"Error importando TrackHS Simple MCP Server: {e}")
    raise

if __name__ == "__main__":
    logger.info("Iniciando TrackHS MCP Server...")
    # FastMCP Cloud maneja automáticamente la configuración HTTP
    # No especificar transport, host, port manualmente
    mcp.run()
