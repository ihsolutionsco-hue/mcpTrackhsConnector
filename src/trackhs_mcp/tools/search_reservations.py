"""
Herramienta MCP para buscar reservas en Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

from typing import Optional, List, Union, Literal
from ..core.api_client import TrackHSApiClient
from ..types.reservations import SearchReservationsParams
from ..core.error_handling import (
    error_handler, ValidationError, validate_required_params,
    validate_param_types
)

def register_search_reservations(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta search_reservations"""
    
    @mcp.tool()
    @error_handler("search_reservations")
    async def search_reservations(
        page: int = 1,
        size: int = 10,
        sort_column: Literal["name", "status", "altConf", "agreementStatus", "type", "guest", "guests", "unit", "units", "checkin", "checkout", "nights"] = "name",
        sort_direction: Literal["asc", "desc"] = "asc",
        search: Optional[str] = None,
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
        updated_since: Optional[str] = None,
        scroll: Optional[Union[int, str]] = None,
        in_house_today: Optional[Literal[0, 1]] = None,
        status: Optional[Union[Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"], List[str]]] = None,
        group_id: Optional[int] = None,
        checkin_office_id: Optional[int] = None
    ):
        """
        Search reservations in Track HS API V2 with comprehensive filtering options
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10, limitado a 10k resultados totales)
            sort_column: Columna para ordenar (default: "name")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Búsqueda por substring en nombre o descripciones
            tags: Búsqueda por ID de tag
            node_id: ID(s) del nodo específico
            unit_id: ID(s) de la unidad específica
            reservation_type_id: ID(s) del tipo de reserva específico
            contact_id: ID(s) del contacto específico
            travel_agent_id: ID(s) del agente de viajes específico
            campaign_id: ID(s) de la campaña específica
            user_id: ID(s) del usuario específico
            unit_type_id: ID(s) del tipo de unidad específico
            rate_type_id: ID(s) del tipo de tarifa específico
            booked_start: Fecha de inicio de reserva (ISO 8601)
            booked_end: Fecha de fin de reserva (ISO 8601)
            arrival_start: Fecha de inicio de llegada (ISO 8601)
            arrival_end: Fecha de fin de llegada (ISO 8601)
            departure_start: Fecha de inicio de salida (ISO 8601)
            departure_end: Fecha de fin de salida (ISO 8601)
            updated_since: Fecha de actualización desde (ISO 8601)
            scroll: Scroll de Elasticsearch (1 para empezar, string para continuar)
            in_house_today: Filtrar por en casa hoy (0 o 1)
            status: Estado(s) de la reserva
            group_id: ID del grupo conectado
            checkin_office_id: ID de la oficina de check-in
        """
        # Validar parámetros básicos
        if page < 1:
            raise ValidationError("Page must be >= 1", "page")
        if size < 1 or size > 1000:
            raise ValidationError("Size must be between 1 and 1000", "size")
        
        # Validar fechas si se proporcionan
        date_params = {
            'booked_start': booked_start,
            'booked_end': booked_end,
            'arrival_start': arrival_start,
            'arrival_end': arrival_end,
            'departure_start': departure_start,
            'departure_end': departure_end,
            'updated_since': updated_since
        }
        
        for param_name, param_value in date_params.items():
            if param_value and not _is_valid_date_format(param_value):
                raise ValidationError(f"Invalid date format for {param_name}. Use ISO 8601 format.", param_name)
        
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        # Agregar parámetros opcionales
        if search:
            query_params["search"] = search
        if tags:
            query_params["tags"] = tags
        if node_id:
            query_params["nodeId"] = node_id
        if unit_id:
            query_params["unitId"] = unit_id
        if reservation_type_id:
            query_params["reservationTypeId"] = reservation_type_id
        if contact_id:
            query_params["contactId"] = contact_id
        if travel_agent_id:
            query_params["travelAgentId"] = travel_agent_id
        if campaign_id:
            query_params["campaignId"] = campaign_id
        if user_id:
            query_params["userId"] = user_id
        if unit_type_id:
            query_params["unitTypeId"] = unit_type_id
        if rate_type_id:
            query_params["rateTypeId"] = rate_type_id
        if booked_start:
            query_params["bookedStart"] = booked_start
        if booked_end:
            query_params["bookedEnd"] = booked_end
        if arrival_start:
            query_params["arrivalStart"] = arrival_start
        if arrival_end:
            query_params["arrivalEnd"] = arrival_end
        if departure_start:
            query_params["departureStart"] = departure_start
        if departure_end:
            query_params["departureEnd"] = departure_end
        if updated_since:
            query_params["updatedSince"] = updated_since
        if scroll:
            query_params["scroll"] = scroll
        if in_house_today is not None:
            query_params["inHouseToday"] = in_house_today
        if status:
            query_params["status"] = status
        if group_id:
            query_params["groupId"] = group_id
        if checkin_office_id:
            query_params["checkinOfficeId"] = checkin_office_id
        
        endpoint = "/v2/pms/reservations"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        result = await api_client.get(endpoint)
        return result

def _is_valid_date_format(date_string: str) -> bool:
    """Valida formato de fecha ISO 8601"""
    try:
        from datetime import datetime
        # Intentar parsear como ISO 8601
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False