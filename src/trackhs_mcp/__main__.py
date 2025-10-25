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
        # Verificar variables de entorno críticas (solo en modo debug)
        required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            logger.warning(f"Variables de entorno faltantes: {missing_vars}")
            logger.warning(
                "Continuando sin verificación estricta de variables de entorno"
            )
        else:
            logger.info("Variables de entorno verificadas correctamente")

        # HTTP transport según fastmcp.json
        logger.info("Iniciando servidor HTTP en puerto 8080...")
        mcp.run(transport="http", host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error iniciando servidor: {e}")
        # En lugar de hacer raise, log el error y continuar
        logger.error("Servidor no pudo iniciar, pero continuando para debugging")
        import traceback

        logger.error(traceback.format_exc())
