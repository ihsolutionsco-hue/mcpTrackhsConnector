"""
Herramientas MCP para TrackHS
"""

from .base import BaseTool
from .create_housekeeping_work_order import CreateHousekeepingWorkOrderTool
from .create_maintenance_work_order import CreateMaintenanceWorkOrderTool
from .diagnose_api import DiagnoseAPITool
from .get_folio import GetFolioTool
from .get_reservation import GetReservationTool
from .search_amenities import SearchAmenitiesTool
from .search_reservations import SearchReservationsTool
from .search_units import SearchUnitsTool

# Lista de todas las herramientas disponibles
TOOLS = [
    SearchReservationsTool,
    GetReservationTool,
    SearchUnitsTool,
    SearchAmenitiesTool,
    GetFolioTool,
    CreateMaintenanceWorkOrderTool,
    CreateHousekeepingWorkOrderTool,
    DiagnoseAPITool,
]

__all__ = [
    "BaseTool",
    "SearchReservationsTool",
    "GetReservationTool",
    "SearchUnitsTool",
    "SearchAmenitiesTool",
    "GetFolioTool",
    "CreateMaintenanceWorkOrderTool",
    "CreateHousekeepingWorkOrderTool",
    "DiagnoseAPITool",
    "TOOLS",
]
