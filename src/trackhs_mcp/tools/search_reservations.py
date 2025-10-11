"""
Herramienta MCP para buscar reservas en Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

from typing import Optional, List, Union, Literal
from ..core.api_client import TrackHSApiClient
from ..models.reservations import SearchReservationsParams
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
        node_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        reservation_type_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        travel_agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        user_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        rate_type_id: Optional[str] = None,
        booked_start: Optional[str] = None,
        booked_end: Optional[str] = None,
        arrival_start: Optional[str] = None,
        arrival_end: Optional[str] = None,
        departure_start: Optional[str] = None,
        departure_end: Optional[str] = None,
        updated_since: Optional[str] = None,
        scroll: Optional[Union[int, str]] = None,
        in_house_today: Optional[Literal[0, 1]] = None,
        status: Optional[Union[str, List[str]]] = None,
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
            node_id: ID(s) del nodo específico (entero, array o string separado por comas)
            unit_id: ID(s) de la unidad específica (entero, array o string separado por comas)
            reservation_type_id: ID(s) del tipo de reserva específico (entero, array o string separado por comas)
            contact_id: ID(s) del contacto específico (entero, array o string separado por comas)
            travel_agent_id: ID(s) del agente de viajes específico (entero, array o string separado por comas)
            campaign_id: ID(s) de la campaña específica (entero, array o string separado por comas)
            user_id: ID(s) del usuario específico (entero, array o string separado por comas)
            unit_type_id: ID(s) del tipo de unidad específico (entero, array o string separado por comas)
            rate_type_id: ID(s) del tipo de tarifa específico (entero, array o string separado por comas)
            booked_start: Fecha de inicio de reserva (ISO 8601)
            booked_end: Fecha de fin de reserva (ISO 8601)
            arrival_start: Fecha de inicio de llegada (ISO 8601)
            arrival_end: Fecha de fin de llegada (ISO 8601)
            departure_start: Fecha de inicio de salida (ISO 8601)
            departure_end: Fecha de fin de salida (ISO 8601)
            updated_since: Fecha de actualización desde (ISO 8601)
            scroll: Scroll de Elasticsearch (1 para empezar, string para continuar)
            in_house_today: Filtrar por en casa hoy (0 o 1)
            status: Estado(s) de la reserva (string individual o lista de strings). Valores válidos: "Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"
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
        
        # Agregar parámetros opcionales con validación correcta
        if search:
            query_params["search"] = search
        if tags:
            query_params["tags"] = tags
        if node_id:
            query_params["nodeId"] = _parse_id_string(node_id)
        if unit_id:
            query_params["unitId"] = _parse_id_string(unit_id)
        if reservation_type_id:
            query_params["reservationTypeId"] = _parse_id_string(reservation_type_id)
        if contact_id:
            query_params["contactId"] = _parse_id_string(contact_id)
        if travel_agent_id:
            query_params["travelAgentId"] = _parse_id_string(travel_agent_id)
        if campaign_id:
            query_params["campaignId"] = _parse_id_string(campaign_id)
        if user_id:
            query_params["userId"] = _parse_id_string(user_id)
        if unit_type_id:
            query_params["unitTypeId"] = _parse_id_string(unit_type_id)
        if rate_type_id:
            query_params["rateTypeId"] = _parse_id_string(rate_type_id)
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
            # Asegurar que in_house_today sea un entero
            query_params["inHouseToday"] = int(in_house_today)
        if status:
            query_params["status"] = _format_status_param(status)
        if group_id:
            query_params["groupId"] = group_id
        if checkin_office_id:
            query_params["checkinOfficeId"] = checkin_office_id
        
        endpoint = "/v2/pms/reservations"
        query_string = _build_query_string(query_params)
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

def _parse_id_string(id_string: str) -> Union[int, List[int]]:
    """
    Parsea un string de ID que puede ser:
    - Un entero simple: "48"
    - Múltiples IDs separados por comas: "48,49,50"
    - Array en formato string: "[48,49,50]"
    """
    if not id_string or not id_string.strip():
        raise ValidationError("ID string cannot be empty", "id")
    
    # Limpiar espacios
    id_string = id_string.strip()
    
    # Si es un array en formato string, parsearlo
    if id_string.startswith('[') and id_string.endswith(']'):
        try:
            # Remover corchetes y dividir por comas
            content = id_string[1:-1].strip()
            if not content:
                raise ValidationError("Empty array not allowed", "id")
            # Dividir por comas y convertir a enteros
            ids = [int(x.strip()) for x in content.split(',')]
            return ids if len(ids) > 1 else ids[0]
        except ValueError as e:
            raise ValidationError(f"Invalid array format: {id_string}", "id")
    
    # Si contiene comas, es una lista de IDs
    if ',' in id_string:
        try:
            ids = [int(x.strip()) for x in id_string.split(',') if x.strip()]
            if not ids:
                raise ValidationError("No valid IDs found", "id")
            return ids if len(ids) > 1 else ids[0]
        except ValueError as e:
            raise ValidationError(f"Invalid ID format: {id_string}", "id")
    
    # Es un ID único
    try:
        return int(id_string)
    except ValueError:
        raise ValidationError(f"Invalid ID format: {id_string}", "id")

def _format_id_param(param_value: Union[int, List[int]]) -> Union[int, List[int]]:
    """
    Formatea parámetros de ID para la API.
    Asegura que los enteros se mantengan como enteros y los arrays como arrays.
    """
    if isinstance(param_value, list):
        # Asegurar que todos los elementos sean enteros
        return [int(x) for x in param_value]
    else:
        # Asegurar que sea entero
        return int(param_value)

def _format_status_param(status_value: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Formatea parámetros de status para la API.
    Valida que los valores sean válidos según la especificación.
    Maneja tanto strings individuales como listas de strings.
    """
    valid_statuses = {"Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"}
    
    if isinstance(status_value, list):
        # Validar cada status en la lista
        for status in status_value:
            if status not in valid_statuses:
                raise ValidationError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}", "status")
        return status_value
    else:
        # Si es un string, verificar si es un array JSON
        if status_value.startswith('[') and status_value.endswith(']'):
            try:
                import json
                # Parsear como JSON array
                statuses = json.loads(status_value)
                if not isinstance(statuses, list):
                    raise ValidationError(f"Invalid status format: {status_value}", "status")
                # Validar cada status
                for status in statuses:
                    if status not in valid_statuses:
                        raise ValidationError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}", "status")
                return statuses if len(statuses) > 1 else statuses[0]
            except (json.JSONDecodeError, ValueError):
                raise ValidationError(f"Invalid status format: {status_value}", "status")
        # Si es un string, verificar si contiene comas (múltiples status)
        elif ',' in status_value:
            # Dividir por comas y limpiar comillas
            statuses = [s.strip().strip('"').strip("'") for s in status_value.split(',') if s.strip()]
            for status in statuses:
                if status not in valid_statuses:
                    raise ValidationError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}", "status")
            return statuses if len(statuses) > 1 else statuses[0]
        else:
            # Validar status único
            if status_value not in valid_statuses:
                raise ValidationError(f"Invalid status: {status_value}. Must be one of: {', '.join(valid_statuses)}", "status")
            return status_value

def _build_query_string(params: dict) -> str:
    """
    Construye la query string correctamente manejando arrays y tipos de datos.
    """
    query_parts = []
    
    for key, value in params.items():
        if value is None:
            continue
            
        if isinstance(value, list):
            # Para arrays, repetir el parámetro con cada valor
            for item in value:
                query_parts.append(f"{key}={item}")
        else:
            # Para valores únicos, usar directamente
            query_parts.append(f"{key}={value}")
    
    return "&".join(query_parts)