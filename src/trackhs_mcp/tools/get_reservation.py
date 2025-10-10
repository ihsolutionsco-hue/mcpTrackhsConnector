"""
Herramienta MCP para obtener una reserva específica de Track HS
"""

from .core.api_client import TrackHSApiClient
from ..types import ReservationResponse, GetReservationParams

async def get_reservation(reservation_id: int) -> ReservationResponse:
    """
    Get a specific reservation by ID from Track HS
    
    Args:
        reservation_id: ID of the reservation to retrieve
    
    Returns:
        ReservationResponse: Reservation data
    """
    # Esta función será implementada cuando se registre con el cliente API
    pass
