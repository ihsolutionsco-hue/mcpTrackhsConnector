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

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

try:
    from trackhs_mcp.server import mcp

    logger.info("TrackHS MCP Server importado correctamente")
except Exception as e:
    logger.error(f"Error importando TrackHS MCP Server: {e}")
    raise

if __name__ == "__main__":
    logger.info("Iniciando TrackHS MCP Server...")
    try:
        # Verificar variables de entorno críticas
        required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            logger.error(f"Variables de entorno faltantes: {missing_vars}")
            raise ValueError(f"Variables de entorno requeridas: {missing_vars}")

        logger.info("Variables de entorno verificadas correctamente")

        # HTTP transport según fastmcp.json
        mcp.run(transport="http", host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error iniciando servidor: {e}")
        raise
