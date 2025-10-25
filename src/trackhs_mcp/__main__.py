from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from .client import trackhs_client
from .tools.reservations import register_reservation_tools
from .tools.units import register_unit_tools
from .tools.amenities import register_amenity_tools
from .tools.folios import register_folio_tools
from .tools.maintenance import register_maintenance_tools

# Crear servidor FastMCP
mcp = FastMCP("TrackHS Hotel MCP")

# Middleware mínimo
mcp.add_middleware(LoggingMiddleware(include_payloads=True))
mcp.add_middleware(ErrorHandlingMiddleware(transform_errors=True))

# Registrar tools
register_reservation_tools(mcp, trackhs_client)
register_unit_tools(mcp, trackhs_client)
register_amenity_tools(mcp, trackhs_client)
register_folio_tools(mcp, trackhs_client)
register_maintenance_tools(mcp, trackhs_client)

if __name__ == "__main__":
    mcp.run()