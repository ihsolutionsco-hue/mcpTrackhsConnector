"""
Herramienta MCP para buscar reservas en Track HS API V2
Versión mejorada con tipos específicos siguiendo mejores prácticas MCP
"""

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union

from pydantic import Field, field_validator

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_reservations import SearchReservationsUseCase
from ...domain.entities.reservations import SearchReservationsParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.date_validation import is_valid_iso8601_date
from ..utils.error_handling import error_handler
from ..utils.type_normalization import (
    normalize_binary_int,
    normalize_int,
    normalize_optional_string,
)
from ..utils.user_friendly_messages import format_date_error

# from ..utils.validation_decorator import validate_search_reservations_params  # Removed: causes *args issue with FastMCP
from ..validation.date_validators import DateValidator


def _parse_id_string(
    id_value: Optional[Union[str, int]],
) -> Optional[Union[int, List[int]]]:
    """
    Parse ID string to int or list of ints.

    Args:
        id_value: String que puede ser "123" o "1,2,3", o int directo

    Returns:
        int si es un solo ID, List[int] si son múltiples, None si está vacío
    """
    if id_value is None:
        return None

    # Si ya es un int, retornarlo directamente
    if isinstance(id_value, int):
        return id_value

    # Si es string, procesar
    if isinstance(id_value, str):
        id_value = id_value.strip()
        if not id_value:
            return None

        # Si contiene comas, parsear como lista
        if "," in id_value:
            try:
                return [int(id.strip()) for id in id_value.split(",") if id.strip()]
            except ValueError:
                # Si no se puede convertir a int, retornar None
                return None

        # Si es un solo ID, retornar como int
        try:
            return int(id_value)
        except ValueError:
            return None

    # Si no es ni string ni int, retornar None
    return None


@error_handler("search_reservations")
async def search_reservations_v2(
    api_client: "ApiClientPort",
    # Parámetros de paginación
    page: int = Field(
        default=0,
        description=(
            "Page number for pagination. Use 0-based indexing (0, 1, 2, ...). "
            "Range: 0-9999. Examples: 0 (first page), 1 (second page). "
            "Default: 0. Max total results: 10,000."
        ),
        ge=0,
        le=9999,
    ),
    size: int = Field(
        default=10,
        description=(
            "Number of results per page. Range: 1-100. "
            "Examples: 10 (default), 25, 50, 100. "
            "Use smaller values for faster responses."
        ),
        ge=1,
        le=100,
    ),
    # Parámetros de ordenamiento
    sort_column: Literal[
        "name",
        "status",
        "altConf",
        "agreementStatus",
        "type",
        "guest",
        "guests",
        "unit",
        "units",
        "checkin",
        "checkout",
        "nights",
    ] = Field(
        default="name",
        description=(
            "Column to sort results by. Valid options: 'name' (reservation name), 'status' (reservation status), "
            "'checkin' (check-in date), 'checkout' (check-out date), 'guest' (guest name), 'unit' (unit name), "
            "'nights' (number of nights). Default: 'name'. Disabled when using scroll parameter."
        ),
    ),
    sort_direction: Literal["asc", "desc"] = Field(
        default="asc",
        description=(
            "Sort direction. Use 'asc' for ascending (A-Z, 0-9) or 'desc' for descending (Z-A, 9-0). "
            "Default: 'asc'. Disabled when using scroll parameter."
        ),
    ),
    # Parámetros de búsqueda de texto
    search: Optional[str] = Field(
        default=None,
        description=(
            "Full-text search across reservation names, guest names, and descriptions. "
            "Examples: 'John Smith' (guest name), 'Villa Paradise' (property name), 'Beach House' (description). "
            "To omit this filter, simply don't include this parameter. Max length: 200 characters."
        ),
        max_length=200,
    ),
    # Filtros por IDs (strings que pueden contener valores separados por comas)
    tags: Optional[str] = Field(
        default=None,
        description=(
            "Filter by tag IDs. Use comma-separated values for multiple tags. "
            "Examples: '1' (single tag) or '1,2,3' (multiple tags). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    node_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by node IDs. Use comma-separated values for multiple nodes. "
            "Examples: '1' (single node) or '1,2,3' (multiple nodes). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    unit_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by unit IDs. Use comma-separated values for multiple units. "
            "Examples: '10' (single unit) or '10,20,30' (multiple units). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    contact_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by contact IDs. Use comma-separated values for multiple contacts. "
            "Examples: '123' (single contact) or '123,456,789' (multiple contacts). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    travel_agent_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by travel agent IDs. Use comma-separated values for multiple agents. "
            "Examples: '5' (single agent) or '5,10,15' (multiple agents). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    campaign_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by campaign IDs. Use comma-separated values for multiple campaigns. "
            "Examples: '1' (single campaign) or '1,2,3' (multiple campaigns). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    user_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by user IDs. Use comma-separated values for multiple users. "
            "Examples: '5' (single user) or '5,10,15' (multiple users). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    unit_type_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by unit type IDs. Use comma-separated values for multiple types. "
            "Examples: '1' (single type) or '1,2,3' (multiple types). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    rate_type_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by rate type IDs. Use comma-separated values for multiple rate types. "
            "Examples: '1' (single rate type) or '1,2,3' (multiple rate types). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    reservation_type_id: Optional[str] = Field(
        default=None,
        description=(
            "Filter by reservation type IDs. Use comma-separated values for multiple types. "
            "Examples: '1' (single type) or '1,2,3' (multiple types). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    # Filtros de fechas (ISO 8601)
    booked_start: Optional[str] = Field(
        default=None,
        description=(
            "Filter by booking date start. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    booked_end: Optional[str] = Field(
        default=None,
        description=(
            "Filter by booking date end. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-12-31'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    arrival_start: Optional[str] = Field(
        default=None,
        description=(
            "Filter by arrival date start. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    arrival_end: Optional[str] = Field(
        default=None,
        description=(
            "Filter by arrival date end. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-12-31'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    departure_start: Optional[str] = Field(
        default=None,
        description=(
            "Filter by departure date start. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    departure_end: Optional[str] = Field(
        default=None,
        description=(
            "Filter by departure date end. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-12-31'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    updated_since: Optional[str] = Field(
        default=None,
        description=(
            "Filter by last update date. Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15'). "
            "To omit this filter, simply don't include this parameter. "
            "Examples: '2024-01-01', '2024-12-31'. Do NOT use 'null' or timestamps."
        ),
    ),
    # Otros filtros
    status: Optional[str] = Field(
        default=None,
        description=(
            "Filter by reservation status. Valid statuses: Hold, Confirmed, "
            "Cancelled, Checked In, Checked Out. For multiple statuses, "
            "use comma-separated values like 'Confirmed,Hold'"
        ),
    ),
    in_house_today: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "Filter by in-house today status. Use 0 (not in house) or 1 (in house). "
            "Accepts: 0, 1, '0', '1'. Examples: 1 (guests currently in house), 0 (not in house). "
            "To omit this filter, simply don't include this parameter."
        ),
    ),
    group_id: Optional[int] = Field(
        default=None,
        description=(
            "Filter by group ID. Use integer format. "
            "Examples: 123. To omit this filter, simply don't include this parameter."
        ),
    ),
    checkin_office_id: Optional[int] = Field(
        default=None,
        description=(
            "Filter by check-in office ID. Use integer format. "
            "Examples: 1. To omit this filter, simply don't include this parameter."
        ),
    ),
    # Elasticsearch scroll para grandes conjuntos de datos
    scroll: Optional[str] = Field(
        default=None,
        description=(
            "Elasticsearch scroll for large datasets. Use '1' to start a new "
            "scroll, or provide the scroll ID from previous response to continue. "
            "Disables sorting when active. Example: '1' to start or 'scroll_id_123' to continue"
        ),
    ),
) -> Dict[str, Any]:
    """
    Search reservations in Track HS API with advanced filtering and pagination.

    This tool provides comprehensive reservation search capabilities with support for
    full-text search, date range filtering, status filtering, and pagination. It's
    optimized for AI model integration with the MCP protocol.

    🎯 KEY FEATURES:
    - Full API V2 compatibility with 25+ filter parameters
    - Standard pagination and Elasticsearch scroll for large datasets
    - Comprehensive date range filtering (booking, arrival, departure)
    - Multiple ID filtering with comma-separated values
    - Flexible status and text search

    📋 AVAILABLE PARAMETERS:
    - Pagination: page (0-based), size (1-100)
    - Sorting: sort_column, sort_direction
    - Text Search: search, tags
    - ID Filters: node_id, unit_id, contact_id, travel_agent_id, campaign_id, user_id, unit_type_id, rate_type_id, reservation_type_id
    - Date Filters: booked_start, booked_end, arrival_start, arrival_end, departure_start, departure_end, updated_since
    - Status Filters: status (single or comma-separated), in_house_today
    - Other: group_id, checkin_office_id, scroll

    📅 DATE FORMAT REQUIREMENTS:
    - Use ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-15')
    - Do NOT use timestamps or 'null' values
    - To omit date filters, simply don't include the parameter
    - Examples: '2024-03-01' for March 1, 2024
    - ❌ WRONG: arrival_start="null" (will be ignored)
    - ✅ CORRECT: arrival_start="2024-03-01" (will filter correctly)

    🔍 STATUS FILTERING:
    - Single status: 'Confirmed'
    - Multiple statuses: 'Confirmed,Cancelled'
    - Valid statuses: 'Hold', 'Confirmed', 'Cancelled', 'Checked In', 'Checked Out'

    📊 PAGINATION:
    - page: 0-based indexing (0, 1, 2, ...)
    - size: 1-100 results per page
    - Default: page=0, size=10

    Returns:
        JSON string with reservation data including guest information, unit details,
        pricing, policies, and pagination metadata.

    Raises:
        ValidationError: If parameters are invalid (e.g., invalid date format)
        APIError: If the API request fails (e.g., 401 Unauthorized, 500 Server Error)
    """
    # Detectar y convertir FieldInfo objects (cuando se llama directamente sin FastMCP)
    if type(sort_column).__name__ == "FieldInfo":
        sort_column = "name"
    if type(sort_direction).__name__ == "FieldInfo":
        sort_direction = "asc"
    if type(search).__name__ == "FieldInfo":
        search = None
    if type(tags).__name__ == "FieldInfo":
        tags = None
    if type(node_id).__name__ == "FieldInfo":
        node_id = None
    if type(unit_id).__name__ == "FieldInfo":
        unit_id = None
    if type(contact_id).__name__ == "FieldInfo":
        contact_id = None
    if type(travel_agent_id).__name__ == "FieldInfo":
        travel_agent_id = None
    if type(campaign_id).__name__ == "FieldInfo":
        campaign_id = None
    if type(user_id).__name__ == "FieldInfo":
        user_id = None
    if type(unit_type_id).__name__ == "FieldInfo":
        unit_type_id = None
    if type(rate_type_id).__name__ == "FieldInfo":
        rate_type_id = None
    if type(reservation_type_id).__name__ == "FieldInfo":
        reservation_type_id = None
    if type(booked_start).__name__ == "FieldInfo":
        booked_start = None
    if type(booked_end).__name__ == "FieldInfo":
        booked_end = None
    if type(arrival_start).__name__ == "FieldInfo":
        arrival_start = None
    if type(arrival_end).__name__ == "FieldInfo":
        arrival_end = None
    if type(departure_start).__name__ == "FieldInfo":
        departure_start = None
    if type(departure_end).__name__ == "FieldInfo":
        departure_end = None
    if type(updated_since).__name__ == "FieldInfo":
        updated_since = None
    if type(status).__name__ == "FieldInfo":
        status = None
    if type(scroll).__name__ == "FieldInfo":
        scroll = None

    # Normalizar parámetros numéricos para backward compatibility
    # (en caso de que vengan como string de otros sistemas)
    page_normalized = normalize_int(page, "page")
    size_normalized = normalize_int(size, "size")
    in_house_today_normalized = normalize_binary_int(in_house_today, "in_house_today")
    group_id_normalized = normalize_int(group_id, "group_id")
    checkin_office_id_normalized = normalize_int(checkin_office_id, "checkin_office_id")

    # Asegurar defaults para page y size si normalize_int retorna None (FieldInfo objects)
    if page_normalized is None:
        page_normalized = 0  # Default: 0 (0-based pagination)
    if size_normalized is None:
        size_normalized = 10  # Default: 10

    # Validar parámetros de paginación según documentación API V2
    if page_normalized < 0:
        raise ValidationError(
            f"Page must be >= 0 (0-based indexing). Received: {page_normalized}", "page"
        )
    if size_normalized < 1:
        raise ValidationError(f"Size must be >= 1. Received: {size_normalized}", "size")
    if size_normalized > 100:
        raise ValidationError(
            f"Size must be <= 100. Received: {size_normalized}", "size"
        )

    # Normalizar todos los parámetros string opcionales
    # Esto convierte "null", "None", "", etc. a None real ANTES de validar
    # Esto es especialmente importante para LLMs que pueden pasar "null" como string

    # Parámetros de fecha
    arrival_start = normalize_optional_string(arrival_start, "arrival_start")
    arrival_end = normalize_optional_string(arrival_end, "arrival_end")
    departure_start = normalize_optional_string(departure_start, "departure_start")
    departure_end = normalize_optional_string(departure_end, "departure_end")
    updated_since = normalize_optional_string(updated_since, "updated_since")
    booked_start = normalize_optional_string(booked_start, "booked_start")
    booked_end = normalize_optional_string(booked_end, "booked_end")

    # Parámetros de búsqueda y filtros de texto
    search = normalize_optional_string(search, "search")
    tags = normalize_optional_string(tags, "tags")
    node_id = normalize_optional_string(node_id, "node_id")
    unit_id = normalize_optional_string(unit_id, "unit_id")
    contact_id = normalize_optional_string(contact_id, "contact_id")
    travel_agent_id = normalize_optional_string(travel_agent_id, "travel_agent_id")
    campaign_id = normalize_optional_string(campaign_id, "campaign_id")
    user_id = normalize_optional_string(user_id, "user_id")
    unit_type_id = normalize_optional_string(unit_type_id, "unit_type_id")
    rate_type_id = normalize_optional_string(rate_type_id, "rate_type_id")
    reservation_type_id = normalize_optional_string(
        reservation_type_id, "reservation_type_id"
    )
    status = normalize_optional_string(status, "status")
    scroll = normalize_optional_string(scroll, "scroll")

    # Validar fechas opcionales después de normalizar
    date_params = {
        "arrival_start": arrival_start,
        "arrival_end": arrival_end,
        "departure_start": departure_start,
        "departure_end": departure_end,
        "updated_since": updated_since,
        "booked_start": booked_start,
        "booked_end": booked_end,
    }

    for param_name, param_value in date_params.items():
        # Después de normalizar, si el parámetro no es None, validar formato
        if param_value is not None:
            # Validar formato de fecha ISO 8601
            if not is_valid_iso8601_date(param_value):
                raise ValidationError(
                    format_date_error(param_name),
                    param_name,
                )

    # Validar estados múltiples
    valid_statuses = {"Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"}
    if status:
        status_list = [s.strip() for s in status.split(",") if s.strip()]
        invalid_statuses = [s for s in status_list if s not in valid_statuses]
        if invalid_statuses:
            raise ValidationError(
                f"❌ Invalid status values: {invalid_statuses}. "
                f"✅ Valid statuses: {', '.join(sorted(valid_statuses))}. "
                f"💡 Examples: 'Confirmed' (single) or 'Confirmed,Cancelled' (multiple).",
                "status",
            )
    else:
        status_list = None

    # Validar límite total de resultados (10k máximo)
    # Para 0-based indexing: (page + 1) * size <= 10000
    if (page_normalized + 1) * size_normalized > 10000:
        raise ValidationError(
            "Total results ((page + 1) * size) must be <= 10,000", "page"
        )

    # Validar parámetro scroll según documentación API V2
    scroll_normalized = None
    if scroll is not None:
        # Convertir scroll a formato apropiado
        if scroll == "1" or scroll == 1:
            scroll_normalized = 1
        elif isinstance(scroll, str) and scroll.strip():
            scroll_normalized = scroll.strip()
        elif isinstance(scroll, int):
            scroll_normalized = scroll
        else:
            raise ValidationError("Scroll string cannot be empty", "scroll")

        # Cuando se usa scroll, el sorting se deshabilita según documentación
        # Pero permitimos que la API maneje esto en lugar de validar estrictamente
        if sort_column != "name" or sort_direction != "asc":
            # Solo advertir, no fallar
            pass

    # Usar lista de estados ya validada anteriormente

    try:
        # Crear caso de uso
        use_case = SearchReservationsUseCase(api_client)

        # Crear parámetros de búsqueda
        search_params = SearchReservationsParams(
            page=page_normalized,
            size=size_normalized,
            sort_column=sort_column,  # Usar valor original, la API manejará el mapeo
            sort_direction=sort_direction,
            search=search,
            tags=tags,
            node_id=_parse_id_string(node_id),
            unit_id=_parse_id_string(unit_id),
            reservation_type_id=_parse_id_string(reservation_type_id),
            contact_id=_parse_id_string(contact_id),
            travel_agent_id=_parse_id_string(travel_agent_id),
            campaign_id=_parse_id_string(campaign_id),
            user_id=_parse_id_string(user_id),
            unit_type_id=_parse_id_string(unit_type_id),
            rate_type_id=_parse_id_string(rate_type_id),
            booked_start=booked_start,
            booked_end=booked_end,
            arrival_start=arrival_start,
            arrival_end=arrival_end,
            departure_start=departure_start,
            departure_end=departure_end,
            updated_since=updated_since,
            scroll=scroll_normalized,
            in_house_today=in_house_today_normalized,
            status=status_list,
            group_id=group_id_normalized,
            checkin_office_id=checkin_office_id_normalized,
        )

        # Ejecutar caso de uso
        result = await use_case.execute(search_params)

        return result

    except Exception as e:
        # Manejar errores específicos de la API según documentación
        if hasattr(e, "status_code"):
            if e.status_code == 400:
                raise ValidationError(
                    "Bad Request: Invalid parameters sent to Reservations API. "
                    "Common issues:\n"
                    "- Page must be >= 0 (0-based pagination)\n"
                    "- Numeric parameters must be integers or convertible strings\n"
                    "- Boolean parameters must be 0 or 1\n"
                    "- Date parameters must be in ISO 8601 format\n"
                    f"Error details: {str(e)}",
                    "parameters",
                )
            elif e.status_code == 401:
                raise ValidationError(
                    "Unauthorized: Invalid authentication credentials. "
                    "Please verify your TRACKHS_USERNAME and TRACKHS_PASSWORD "
                    "are correct and not expired.",
                    "auth",
                )
            elif e.status_code == 403:
                raise ValidationError(
                    "Forbidden: Insufficient permissions for this operation. "
                    "Please verify your account has access to "
                    "API V2/Reservations endpoints. "
                    "Contact your administrator to enable API V2 access.",
                    "permissions",
                )
            elif e.status_code == 404:
                raise ValidationError(
                    "Endpoint not found: /pms/reservations. "
                    "Please verify the API URL and endpoint path are correct. "
                    "The API V2 endpoint might not be available in your environment.",
                    "endpoint",
                )
            elif e.status_code == 500:
                raise ValidationError(
                    "Internal Server Error: API temporarily unavailable. "
                    "Please try again later or contact TrackHS support. "
                    "If the problem persists, check the TrackHS service status.",
                    "api",
                )
        # El error_handler wrapper se encargará de formatear el error
        raise


def register_search_reservations_v2(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_reservations_v2 mejorada"""

    # Crear una función wrapper que capture api_client en el closure
    async def wrapped_search_reservations_v2(
        # ===========================================
        # PAGINATION PARAMETERS
        # ===========================================
        page: int = Field(
            default=0,
            description=(
                "Page number (0-based indexing). Max total results: 10,000. "
                "Maps to API parameter 'page'."
            ),
            ge=0,
            le=10000,
        ),
        size: int = Field(
            default=10,
            description=(
                "Number of results per page (1-100). "
                "Maps to API parameter 'size'."
            ),
            ge=1,
            le=100,
        ),
        # ===========================================
        # SORTING PARAMETERS
        # ===========================================
        sort_column: Literal[
            "name",
            "status",
            "altConf",
            "agreementStatus",
            "type",
            "guest",
            "guests",
            "unit",
            "units",
            "checkin",
            "checkout",
            "nights",
        ] = Field(
            default="name",
            description=(
                "Column to sort by. Valid values: name, status, altConf, "
                "agreementStatus, type, guest, guests, unit, units, checkin, "
                "checkout, nights. Disabled when using scroll. Maps to API parameter 'sortColumn'."
            ),
        ),
        sort_direction: Literal["asc", "desc"] = Field(
            default="asc",
            description=(
                "Sort direction: 'asc' or 'desc'. Disabled when using scroll. "
                "Maps to API parameter 'sortDirection'."
            ),
        ),
        # ===========================================
        # SEARCH PARAMETERS
        # ===========================================
        search: Optional[str] = Field(
            default=None,
            description=(
                "Full-text search in reservation names, guest names, and descriptions. "
                "Example: 'John Smith' or 'Villa Paradise'. Maximum 200 characters. "
                "Maps to API parameter 'search'."
            ),
            max_length=200,
        ),
        # ===========================================
        # ID FILTERS
        # ===========================================
        tags: Optional[str] = Field(
            default=None,
            description="Filter by tag IDs (comma-separated: '1,2,3'). Maps to API parameter 'tags'.",
        ),
        node_id: Optional[str] = Field(
            default=None,
            description="Filter by node IDs (property locations). Example: '1' for single node or '1,2,3' for multiple nodes. Maps to API parameter 'nodeId'.",
        ),
        unit_id: Optional[str] = Field(
            default=None,
            description="Filter by unit IDs (specific rental units). Example: '10' for single unit or '10,20,30' for multiple units. Maps to API parameter 'unitId'.",
        ),
        contact_id: Optional[str] = Field(
            default=None,
            description="Filter by contact IDs (guest contacts). Example: '123' for single contact or '123,456' for multiple contacts. Maps to API parameter 'contactId'.",
        ),
        travel_agent_id: Optional[str] = Field(
            default=None,
            description="Filter by travel agent IDs (booking agents). Example: '21' for single agent or '21,22' for multiple agents. Maps to API parameter 'travelAgentId'.",
        ),
        campaign_id: Optional[str] = Field(
            default=None,
            description="Filter by campaign IDs (marketing campaigns). Example: '5' for single campaign or '5,6' for multiple campaigns. Maps to API parameter 'campaignId'.",
        ),
        user_id: Optional[str] = Field(
            default=None,
            description="Filter by user IDs (system users). Example: '100' for single user or '100,101' for multiple users. Maps to API parameter 'userId'.",
        ),
        unit_type_id: Optional[str] = Field(
            default=None,
            description="Filter by unit type IDs (property types). Example: '2' for single type or '2,3' for multiple types. Maps to API parameter 'unitTypeId'.",
        ),
        rate_type_id: Optional[str] = Field(
            default=None,
            description="Filter by rate type IDs (pricing types). Example: '1' for single rate type or '1,2' for multiple rate types. Maps to API parameter 'rateTypeId'.",
        ),
        reservation_type_id: Optional[str] = Field(
            default=None,
            description="Filter by reservation type IDs (booking types). Example: '3' for single type or '3,4' for multiple types. Maps to API parameter 'reservationTypeId'.",
        ),
        # ===========================================
        # DATE RANGE FILTERS
        # ===========================================
        # Booking date range
        booked_start: Optional[str] = Field(
            default=None,
            description=(
                "Filter by booking date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15'. To omit this filter, simply don't include this parameter. "
                "Do NOT use 'null'. Maps to API parameter 'bookedStart'."
            ),
        ),
        booked_end: Optional[str] = Field(
            default=None,
            description=(
                "Filter by booking date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-12-31'. To omit this filter, simply don't include this parameter. "
                "Do NOT use 'null'. Maps to API parameter 'bookedEnd'."
            ),
        ),
        # Arrival date range
        arrival_start: Optional[str] = Field(
            default=None,
            description=(
                "Filter by arrival date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. To omit this filter, "
                "simply don't include this parameter. Do NOT use 'null'. "
                "Maps to API parameter 'arrivalStart'."
            ),
        ),
        arrival_end: Optional[str] = Field(
            default=None,
            description=(
                "Filter by arrival date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. To omit this filter, "
                "simply don't include this parameter. Do NOT use 'null'. "
                "Maps to API parameter 'arrivalEnd'."
            ),
        ),
        # Departure date range
        departure_start: Optional[str] = Field(
            default=None,
            description=(
                "Filter by departure date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. To omit this filter, "
                "simply don't include this parameter. Do NOT use 'null'. "
                "Maps to API parameter 'departureStart'."
            ),
        ),
        departure_end: Optional[str] = Field(
            default=None,
            description=(
                "Filter by departure date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. To omit this filter, "
                "simply don't include this parameter. Do NOT use 'null'. "
                "Maps to API parameter 'departureEnd'."
            ),
        ),
        # Last update filter
        updated_since: Optional[str] = Field(
            default=None,
            description=(
                "Filter by last update date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). "
                "Example: '2024-01-15' or '2024-01-15T10:00:00Z'. To omit this filter, "
                "simply don't include this parameter. Do NOT use 'null'. "
                "Maps to API parameter 'updatedSince'."
            ),
        ),
        # Otros filtros
        status: Optional[str] = Field(
            default=None,
            description=(
                "Filter by reservation status. Use single status or comma-separated for multiple. "
                "Valid statuses: 'Hold', 'Confirmed', 'Cancelled', 'Checked In', 'Checked Out'. "
                "Examples: 'Confirmed' (single) or 'Confirmed,Cancelled' (multiple). "
                "To omit this filter, simply don't include this parameter."
            ),
        ),
        in_house_today: Optional[Union[int, str]] = Field(
            default=None,
            description="Filter by in-house today (0=not in house, 1=in house). Accepts: 0, 1, '0', '1'. Maps to API parameter 'inHouseToday'.",
        ),
        group_id: Optional[Union[int, str]] = Field(
            default=None, description="Filter by group ID. Accepts: integer or string"
        ),
        checkin_office_id: Optional[Union[int, str]] = Field(
            default=None,
            description="Filter by check-in office ID. Accepts: integer or string",
        ),
        # Elasticsearch scroll para grandes conjuntos de datos
        scroll: Optional[str] = Field(
            default=None,
            description=(
                "Elasticsearch scroll for large datasets. Use '1' to start a new "
                "scroll, or provide the scroll ID from previous response to continue. "
                "Disables sorting when active. Example: '1' to start or 'scroll_id_123' to continue"
            ),
        ),
    ) -> Dict[str, Any]:
        """Search reservations in Track HS API with advanced filtering and pagination."""
        # Convertir parámetros numéricos a enteros si vienen como strings
        page_int = int(page) if isinstance(page, str) else page
        size_int = int(size) if isinstance(size, str) else size
        group_id_int = (
            int(group_id) if isinstance(group_id, str) and group_id is not None else group_id
        )
        checkin_office_id_int = (
            int(checkin_office_id)
            if isinstance(checkin_office_id, str) and checkin_office_id is not None
            else checkin_office_id
        )

        return await search_reservations_v2(
            api_client,
            page=page_int,
            size=size_int,
            sort_column=sort_column,
            sort_direction=sort_direction,
            search=search,
            tags=tags,
            node_id=node_id,
            unit_id=unit_id,
            contact_id=contact_id,
            travel_agent_id=travel_agent_id,
            campaign_id=campaign_id,
            user_id=user_id,
            unit_type_id=unit_type_id,
            rate_type_id=rate_type_id,
            reservation_type_id=reservation_type_id,
            booked_start=booked_start,
            booked_end=booked_end,
            arrival_start=arrival_start,
            arrival_end=arrival_end,
            departure_start=departure_start,
            departure_end=departure_end,
            updated_since=updated_since,
            status=status,
            in_house_today=in_house_today,
            group_id=group_id_int,
            checkin_office_id=checkin_office_id_int,
            scroll=scroll,
        )

    mcp.tool(name="search_reservations")(wrapped_search_reservations_v2)
