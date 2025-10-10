"""
Registrador de todas las herramientas MCP para Track HS API
"""

from ..core.api_client import TrackHSApiClient

# Importar todas las herramientas individuales
from .get_reviews import register_get_reviews
from .get_reservation import register_get_reservation
from .search_reservations import register_search_reservations
from .get_units import register_get_units
from .get_unit import register_get_unit
from .get_folios_collection import register_get_folios_collection
from .get_contacts import register_get_contacts
from .get_ledger_accounts import register_get_ledger_accounts
from .get_ledger_account import register_get_ledger_account
from .get_reservation_notes import register_get_reservation_notes
from .get_nodes import register_get_nodes
from .get_node import register_get_node
from .get_maintenance_work_orders import register_get_maintenance_work_orders

def register_all_tools(mcp, api_client: TrackHSApiClient):
    """
    Registra todas las 13 herramientas MCP con el cliente API
    
    Args:
        mcp: Instancia del servidor FastMCP
        api_client: Cliente API de Track HS
    """
    # Registrar todas las herramientas individuales
    register_get_reviews(mcp, api_client)
    register_get_reservation(mcp, api_client)
    register_search_reservations(mcp, api_client)
    register_get_units(mcp, api_client)
    register_get_unit(mcp, api_client)
    register_get_folios_collection(mcp, api_client)
    register_get_contacts(mcp, api_client)
    register_get_ledger_accounts(mcp, api_client)
    register_get_ledger_account(mcp, api_client)
    register_get_reservation_notes(mcp, api_client)
    register_get_nodes(mcp, api_client)
    register_get_node(mcp, api_client)
    register_get_maintenance_work_orders(mcp, api_client)
