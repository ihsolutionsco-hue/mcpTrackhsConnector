"""
Type definitions for TrackHS MCP Connector

Contiene todos los modelos Pydantic para la API de Track HS.
"""

# Reviews
from .reviews import Review, GetReviewsParams, ReviewsResponse, ReviewFilters

# Reservations  
from .reservations import Reservation, GetReservationParams, SearchReservationsParams, SearchReservationsResponse, ReservationResponse, ReservationFilters

# Units
from .units import Unit, GetUnitsParams, GetUnitParams, GetUnitsResponse, UnitFilters

# Contacts
from .contacts import Contact, GetContactsParams, ContactsResponse, ContactFilters

# Folios
from .folios import Folio, GetFoliosCollectionParams, GetFoliosCollectionResponse

# Ledger Accounts
from .ledger_accounts import LedgerAccount, GetLedgerAccountsParams, GetLedgerAccountParams, LedgerAccountsResponse, LedgerAccountResponse, LedgerAccountFilters

# Reservation Notes
from .reservation_notes import ReservationNote, GetReservationNotesParams, ReservationNotesResponse, CreateReservationNoteRequest, UpdateReservationNoteRequest, ReservationNoteResponse

# Nodes
from .nodes import Node, GetNodesParams, GetNodeParams, GetNodesResponse, GetNodeResponse, NodeFilters

# Maintenance Work Orders
from .maintenance_work_orders import MaintenanceWorkOrder, GetMaintenanceWorkOrdersParams, MaintenanceWorkOrdersResponse

__all__ = [
    # Reviews
    "Review", "GetReviewsParams", "ReviewsResponse", "ReviewFilters",
    # Reservations
    "Reservation", "GetReservationParams", "SearchReservationsParams", "SearchReservationsResponse", "ReservationResponse", "ReservationFilters",
    # Units
    "Unit", "GetUnitsParams", "GetUnitParams", "GetUnitsResponse", "UnitFilters",
    # Contacts
    "Contact", "GetContactsParams", "ContactsResponse", "ContactFilters",
    # Folios
    "Folio", "GetFoliosCollectionParams", "GetFoliosCollectionResponse",
    # Ledger Accounts
    "LedgerAccount", "GetLedgerAccountsParams", "GetLedgerAccountParams", "LedgerAccountsResponse", "LedgerAccountResponse", "LedgerAccountFilters",
    # Reservation Notes
    "ReservationNote", "GetReservationNotesParams", "ReservationNotesResponse", "CreateReservationNoteRequest", "UpdateReservationNoteRequest", "ReservationNoteResponse",
    # Nodes
    "Node", "GetNodesParams", "GetNodeParams", "GetNodesResponse", "GetNodeResponse", "NodeFilters",
    # Maintenance Work Orders
    "MaintenanceWorkOrder", "GetMaintenanceWorkOrdersParams", "MaintenanceWorkOrdersResponse"
]
