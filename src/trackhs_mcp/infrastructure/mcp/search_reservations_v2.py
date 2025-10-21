"""
Herramienta MCP para buscar reservas en Track HS API V2
Versión mejorada con tipos específicos siguiendo mejores prácticas MCP
"""

from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_reservations import SearchReservationsUseCase
from ...domain.entities.reservations import SearchReservationsParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.date_validation import is_valid_iso8601_date
from ..utils.error_handling import error_handler
from ..utils.type_normalization import normalize_binary_int, normalize_int
from ..utils.user_friendly_messages import format_date_error


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


def register_search_reservations_v2(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_reservations_v2 mejorada"""

    @mcp.tool(name="search_reservations")
    @error_handler("search_reservations")
    async def search_reservations_v2(
        # Parámetros de paginación
        page: int = Field(
            default=1,
            description="Page number (0-based indexing). Max total results: 10,000.",
            ge=0,
            le=10000,
        ),
        size: int = Field(
            default=10, description="Number of results per page (1-1000)", ge=1, le=1000
        ),
        # Parámetros de ordenamiento
        sort_column: str = Field(
            default="name",
            description=(
                "Column to sort by. Valid values: name, status, altConf, "
                "agreementStatus, type, guest, guests, unit, units, checkin, "
                "checkout, nights. Disabled when using scroll."
            ),
        ),
        sort_direction: str = Field(
            default="asc",
            description="Sort direction: 'asc' or 'desc'. Disabled when using scroll.",
        ),
        # Parámetros de búsqueda de texto
        search: Optional[str] = Field(
            default=None,
            description="Full-text search in reservation names, guest names, and descriptions",
            max_length=200,
        ),
        # Filtros por IDs (strings que pueden contener valores separados por comas)
        tags: Optional[str] = Field(
            default=None, description="Filter by tag IDs (comma-separated: '1,2,3')"
        ),
        node_id: Optional[str] = Field(
            default=None, description="Filter by node IDs (comma-separated: '1,2,3')"
        ),
        unit_id: Optional[str] = Field(
            default=None, description="Filter by unit IDs (comma-separated: '10,20,30')"
        ),
        contact_id: Optional[str] = Field(
            default=None, description="Filter by contact IDs (comma-separated)"
        ),
        travel_agent_id: Optional[str] = Field(
            default=None, description="Filter by travel agent IDs (comma-separated)"
        ),
        campaign_id: Optional[str] = Field(
            default=None, description="Filter by campaign IDs (comma-separated)"
        ),
        user_id: Optional[str] = Field(
            default=None, description="Filter by user IDs (comma-separated)"
        ),
        unit_type_id: Optional[str] = Field(
            default=None, description="Filter by unit type IDs (comma-separated)"
        ),
        rate_type_id: Optional[str] = Field(
            default=None, description="Filter by rate type IDs (comma-separated)"
        ),
        reservation_type_id: Optional[str] = Field(
            default=None, description="Filter by reservation type IDs (comma-separated)"
        ),
        # Filtros de fechas (ISO 8601)
        booked_start: Optional[str] = Field(
            default=None,
            description="Filter by booking date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        booked_end: Optional[str] = Field(
            default=None,
            description="Filter by booking date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        arrival_start: Optional[str] = Field(
            default=None,
            description="Filter by arrival date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        arrival_end: Optional[str] = Field(
            default=None,
            description="Filter by arrival date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        departure_start: Optional[str] = Field(
            default=None,
            description="Filter by departure date start (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        departure_end: Optional[str] = Field(
            default=None,
            description="Filter by departure date end (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        updated_since: Optional[str] = Field(
            default=None,
            description="Filter by last update date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        # Otros filtros
        status: Optional[str] = Field(
            default=None,
            description=(
                "Filter by reservation status. Comma-separated values: "
                "'Confirmed,Cancelled,Pending'. Valid statuses: Hold, Confirmed, "
                "Cancelled, Checked In, Checked Out, No Show, Pending"
            ),
        ),
        in_house_today: Optional[int] = Field(
            default=None,
            description="Filter by in-house today (0=not in house, 1=in house)",
            ge=0,
            le=1,
        ),
        group_id: Optional[int] = Field(default=None, description="Filter by group ID"),
        checkin_office_id: Optional[int] = Field(
            default=None, description="Filter by check-in office ID"
        ),
        # Elasticsearch scroll para grandes conjuntos de datos
        scroll: Optional[str] = Field(
            default=None,
            description=(
                "Elasticsearch scroll for large datasets. Use '1' to start a new "
                "scroll, or provide the scroll ID from previous response to continue. "
                "Disables sorting when active."
            ),
        ),
    ) -> str:
        """
        Search reservations in Track HS API with advanced filtering and pagination.

        This tool provides comprehensive reservation search capabilities with support for
        full-text search, date range filtering, status filtering, and pagination. It's
        optimized for AI model integration with the MCP protocol.

        Key features:
        - Full API V2 compatibility with 25+ filter parameters
        - Standard pagination and Elasticsearch scroll for large datasets
        - Comprehensive date range filtering (booking, arrival, departure)
        - Multiple ID filtering with comma-separated values
        - Flexible status and text search

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
        in_house_today_normalized = normalize_binary_int(
            in_house_today, "in_house_today"
        )
        group_id_normalized = normalize_int(group_id, "group_id")
        checkin_office_id_normalized = normalize_int(
            checkin_office_id, "checkin_office_id"
        )

        # Asegurar defaults para page y size si normalize_int retorna None (FieldInfo objects)
        if page_normalized is None:
            page_normalized = 0
        if size_normalized is None:
            size_normalized = 10

        # Validar parámetros básicos según documentación API V2
        if page_normalized < 0:
            raise ValidationError("Page must be >= 0", "page")
        if size_normalized < 1:
            raise ValidationError("Size must be >= 1", "size")
        if size_normalized > 1000:
            raise ValidationError("Size must be <= 1000", "size")

        # Validar límite total de resultados (10k máximo)
        if page_normalized * size_normalized > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
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

            # Cuando se usa scroll, el sorting se deshabilita
            if sort_column != "name" or sort_direction != "asc":
                raise ValidationError(
                    "When using scroll, sorting is disabled. Use default sort_column='name' and sort_direction='asc'",
                    "scroll",
                )

        # Validar fechas si se proporcionan
        date_params = {
            "booked_start": booked_start,
            "booked_end": booked_end,
            "arrival_start": arrival_start,
            "arrival_end": arrival_end,
            "departure_start": departure_start,
            "departure_end": departure_end,
            "updated_since": updated_since,
        }

        for param_name, param_value in date_params.items():
            if param_value and not is_valid_iso8601_date(param_value):
                raise ValidationError(
                    format_date_error(param_name),
                    param_name,
                )

        # Parsear status (puede venir como string con comas o como lista)
        status_list = None
        if status:
            if isinstance(status, list):
                status_list = status
            else:
                status_list = [s.strip() for s in status.split(",") if s.strip()]

        try:
            # Crear caso de uso
            use_case = SearchReservationsUseCase(api_client)

            # Crear parámetros de búsqueda
            search_params = SearchReservationsParams(
                page=page_normalized,
                size=size_normalized,
                sort_column=sort_column if sort_column != "altConf" else "altCon",
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
