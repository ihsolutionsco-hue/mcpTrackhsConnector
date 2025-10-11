"""
Type definitions for TrackHS MCP Connector

Contiene todos los modelos Pydantic para la API de Track HS.
"""

# Reservations  
from .reservations import Reservation, SearchReservationsParams

# Base types
from .base import PaginationParams, SearchParams, TrackHSResponse

__all__ = [
    # Reservations
    "Reservation", "SearchReservationsParams",
    # Base types
    "PaginationParams", "SearchParams", "TrackHSResponse"
]