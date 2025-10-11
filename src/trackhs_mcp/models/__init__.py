"""
Type definitions for TrackHS MCP Connector

Contiene todos los modelos Pydantic para la API de Track HS.
"""

# Base types
from .base import PaginationParams, SearchParams, TrackHSResponse

# Reservations
from .reservations import Reservation, SearchReservationsParams

__all__ = [
    # Reservations
    "Reservation",
    "SearchReservationsParams",
    # Base types
    "PaginationParams",
    "SearchParams",
    "TrackHSResponse",
]
