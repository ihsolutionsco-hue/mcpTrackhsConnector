"""
TrackHS MCP Server - Entry Point
Punto de entrada para FastMCP Cloud - Arquitectura Simplificada
"""

import logging
import sys
from pathlib import Path

# Agregar el directorio src al path para importaciones
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

try:
    from trackhs_mcp.server import mcp

    logger.info("✅ TrackHS MCP Server (v2.0.0) importado correctamente")
except Exception as e:
    logger.error(f"❌ Error importando TrackHS MCP Server: {e}")
    raise

if __name__ == "__main__":
    logger.info("🚀 Iniciando TrackHS MCP Server...")
    # FastMCP maneja automáticamente la configuración HTTP
    mcp.run()
