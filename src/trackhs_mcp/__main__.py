import os
import logging
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

# Configurar logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    from trackhs_mcp.client import trackhs_client
    from trackhs_mcp.tools.reservations import register_reservation_tools
    from trackhs_mcp.tools.units import register_unit_tools
    from trackhs_mcp.tools.amenities import register_amenity_tools
    from trackhs_mcp.tools.folios import register_folio_tools
    from trackhs_mcp.tools.maintenance import register_maintenance_tools
except ImportError as e:
    logger.error(f"Error importing modules: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error during import: {e}")
    raise

# Crear servidor FastMCP
mcp = FastMCP("TrackHS Hotel MCP")

# Middleware mínimo
mcp.add_middleware(LoggingMiddleware(include_payloads=True))
mcp.add_middleware(ErrorHandlingMiddleware(transform_errors=True))

# Registrar tools
try:
    register_reservation_tools(mcp, trackhs_client)
    register_unit_tools(mcp, trackhs_client)
    register_amenity_tools(mcp, trackhs_client)
    register_folio_tools(mcp, trackhs_client)
    register_maintenance_tools(mcp, trackhs_client)
    logger.info("All tools registered successfully")
except Exception as e:
    logger.error(f"Error registering tools: {e}")
    raise

if __name__ == "__main__":
    mcp.run()