"""
Herramienta MCP para buscar reservas en Track HS
"""

from typing import Optional, Literal, List, Union
from .core.api_client import TrackHSApiClient
from ..types import SearchReservationsResponse, SearchReservationsParams

async def search_reservations(
    page: int = 1,
    size: int = 10,
    sort_column: Optional[Literal["name", "status", "altConf", "agreementStatus", "type", "guest", "guests", "unit", "units", "checkin", "checkout", "nights"]] = "name",
    sort_direction: Optional[Literal["asc", "desc"]] = "asc",
    search: Optional[str] = None,
    updated_since: Optional[str] = None,
    tags: Optional[str] = None,
    node_id: Optional[Union[int, List[int]]] = None,
    unit_id: Optional[Union[int, List[int]]] = None,
    reservation_type_id: Optional[Union[int, List[int]]] = None,
    contact_id: Optional[Union[int, List[int]]] = None,
    travel_agent_id: Optional[Union[int, List[int]]] = None,
    campaign_id: Optional[Union[int, List[int]]] = None,
    user_id: Optional[Union[int, List[int]]] = None,
    unit_type_id: Optional[Union[int, List[int]]] = None,
    rate_type_id: Optional[Union[int, List[int]]] = None,
    booked_start: Optional[str] = None,
    booked_end: Optional[str] = None,
    arrival_start: Optional[str] = None,
    arrival_end: Optional[str] = None,
    departure_start: Optional[str] = None,
    departure_end: Optional[str] = None,
    in_house_today: Optional[Literal[0, 1]] = None,
    status: Optional[Union[Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"], List[str]]] = None,
    group_id: Optional[int] = None,
    checkin_office_id: Optional[int] = None
) -> SearchReservationsResponse:
    """
    Search reservations in Track HS with various filters
    
    Args:
        page: Page number
        size: Page size
        sort_column: Column to sort by
        sort_direction: Sort direction
        search: Search term
        updated_since: Filter by update date
        tags: Filter by tags
        node_id: Filter by node ID(s)
        unit_id: Filter by unit ID(s)
        reservation_type_id: Filter by reservation type ID(s)
        contact_id: Filter by contact ID(s)
        travel_agent_id: Filter by travel agent ID(s)
        campaign_id: Filter by campaign ID(s)
        user_id: Filter by user ID(s)
        unit_type_id: Filter by unit type ID(s)
        rate_type_id: Filter by rate type ID(s)
        booked_start: Filter by booking start date
        booked_end: Filter by booking end date
        arrival_start: Filter by arrival start date
        arrival_end: Filter by arrival end date
        departure_start: Filter by departure start date
        departure_end: Filter by departure end date
        in_house_today: Filter by in-house today
        status: Filter by status
        group_id: Filter by group ID
        checkin_office_id: Filter by check-in office ID
    
    Returns:
        SearchReservationsResponse: Search results
    """
    # Esta función será implementada cuando se registre con el cliente API
    pass
