"""
Herramienta MCP para buscar unidades en Track HS Channel API
Versión mejorada con tipos específicos siguiendo mejores prácticas MCP
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_units import SearchUnitsUseCase
from ...domain.entities.units import SearchUnitsParams
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


def register_search_units(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_units mejorada"""

    @mcp.tool(name="search_units")
    @error_handler("search_units")
    async def search_units(
        # Parámetros de paginación
        page: int = Field(
            default=1,
            description="Page number (1-based indexing). Max total results: 10,000.",
            ge=1,
            le=10000,
        ),
        size: int = Field(
            default=3, description="Number of results per page (1-5)", ge=1, le=5
        ),
        # Parámetros de ordenamiento
        sort_column: str = Field(
            default="name",
            description="Column to sort by. Valid values: id, name, nodeName, unitTypeName",
        ),
        sort_direction: str = Field(
            default="asc", description="Sort direction: 'asc' or 'desc'"
        ),
        # Parámetros de búsqueda de texto
        search: Optional[str] = Field(
            default=None,
            description="Full-text search in unit names, codes, and descriptions",
            max_length=200,
        ),
        term: Optional[str] = Field(
            default=None,
            description="Search term for unit names and descriptions",
            max_length=200,
        ),
        unit_code: Optional[str] = Field(
            default=None, description="Exact unit code to search for", max_length=50
        ),
        short_name: Optional[str] = Field(
            default=None, description="Search by unit short name", max_length=100
        ),
        # Filtros por IDs (strings que pueden contener valores separados por comas)
        node_id: Optional[str] = Field(
            default=None, description="Filter by node IDs (comma-separated: '1,2,3')"
        ),
        amenity_id: Optional[str] = Field(
            default=None, description="Filter by amenity IDs (comma-separated: '1,2,3')"
        ),
        unit_type_id: Optional[str] = Field(
            default=None,
            description="Filter by unit type IDs (comma-separated: '1,2,3')",
        ),
        id: Optional[str] = Field(
            default=None, description="Filter by unit IDs (comma-separated: '1,2,3')"
        ),
        # Filtros numéricos
        calendar_id: Optional[int] = Field(
            default=None, description="Filter by calendar ID"
        ),
        role_id: Optional[int] = Field(default=None, description="Filter by role ID"),
        # Filtros de habitaciones y baños
        bedrooms: Optional[int] = Field(
            default=None, description="Filter by exact number of bedrooms", ge=0
        ),
        min_bedrooms: Optional[int] = Field(
            default=None, description="Filter by minimum number of bedrooms", ge=0
        ),
        max_bedrooms: Optional[int] = Field(
            default=None, description="Filter by maximum number of bedrooms", ge=0
        ),
        bathrooms: Optional[int] = Field(
            default=None, description="Filter by exact number of bathrooms", ge=0
        ),
        min_bathrooms: Optional[int] = Field(
            default=None, description="Filter by minimum number of bathrooms", ge=0
        ),
        max_bathrooms: Optional[int] = Field(
            default=None, description="Filter by maximum number of bathrooms", ge=0
        ),
        # Filtros booleanos (0/1)
        pets_friendly: Optional[int] = Field(
            default=None,
            description="Filter by pet-friendly units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        allow_unit_rates: Optional[int] = Field(
            default=None,
            description="Filter by units that allow unit-specific rates (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        computed: Optional[int] = Field(
            default=None,
            description="Filter by computed units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        inherited: Optional[int] = Field(
            default=None,
            description="Filter by inherited units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        limited: Optional[int] = Field(
            default=None,
            description="Filter by limited availability units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        is_bookable: Optional[int] = Field(
            default=None,
            description="Filter by bookable units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        include_descriptions: Optional[int] = Field(
            default=None,
            description="Include unit descriptions in response (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        is_active: Optional[int] = Field(
            default=None,
            description="Filter by active units (0=inactive, 1=active)",
            ge=0,
            le=1,
        ),
        events_allowed: Optional[int] = Field(
            default=None,
            description="Filter by units allowing events (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        smoking_allowed: Optional[int] = Field(
            default=None,
            description="Filter by units allowing smoking (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        children_allowed: Optional[int] = Field(
            default=None,
            description="Filter by units allowing children (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        is_accessible: Optional[int] = Field(
            default=None,
            description="Filter by accessible/wheelchair-friendly units (0=no, 1=yes)",
            ge=0,
            le=1,
        ),
        # Filtros de fechas (ISO 8601)
        arrival: Optional[str] = Field(
            default=None,
            description="Filter by arrival date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        departure: Optional[str] = Field(
            default=None,
            description="Filter by departure date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        content_updated_since: Optional[str] = Field(
            default=None,
            description="Filter by content update date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        updated_since: Optional[str] = Field(
            default=None,
            description="Filter by last update date (ISO 8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
        ),
        # Estado de limpieza
        unit_status: Optional[str] = Field(
            default=None,
            description=(
                "Filter by housekeeping status. Valid values: "
                "clean, dirty, occupied, inspection, inprogress"
            ),
        ),
    ) -> Dict[str, Any]:
        """
        Search units in Track HS Channel API with advanced filtering and pagination.

        This tool provides comprehensive unit search capabilities with support for
        property features filtering (bedrooms, bathrooms, amenities), availability
        checks, location filtering, and more. Optimized for AI model integration.

        Key features:
        - Full Channel API compatibility with 35+ filter parameters
        - Property features filtering (bedrooms, bathrooms, pets, accessibility)
        - Availability checks with date ranges
        - Location and amenity filtering
        - Housekeeping status filtering
        - Comprehensive unit details including descriptions, images, and rates

        Returns:
            JSON string with unit data including property features, amenities,
            images, rates, availability calendar, and pagination metadata.

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
        if type(term).__name__ == "FieldInfo":
            term = None
        if type(unit_code).__name__ == "FieldInfo":
            unit_code = None
        if type(short_name).__name__ == "FieldInfo":
            short_name = None
        if type(node_id).__name__ == "FieldInfo":
            node_id = None
        if type(amenity_id).__name__ == "FieldInfo":
            amenity_id = None
        if type(unit_type_id).__name__ == "FieldInfo":
            unit_type_id = None
        if type(id).__name__ == "FieldInfo":
            id = None
        if type(arrival).__name__ == "FieldInfo":
            arrival = None
        if type(departure).__name__ == "FieldInfo":
            departure = None
        if type(content_updated_since).__name__ == "FieldInfo":
            content_updated_since = None
        if type(updated_since).__name__ == "FieldInfo":
            updated_since = None
        if type(unit_status).__name__ == "FieldInfo":
            unit_status = None

        # Normalizar parámetros numéricos para backward compatibility
        page_normalized = normalize_int(page, "page")
        size_normalized = normalize_int(size, "size")

        # Validar parámetros antes de aplicar defaults
        if page_normalized is not None and page_normalized < 1:
            raise ValidationError("Page must be >= 1", "page")
        if size_normalized is not None and size_normalized < 1:
            raise ValidationError("Size must be >= 1", "size")
        if size_normalized is not None and size_normalized > 5:
            raise ValidationError("Size must be <= 5", "size")

        # Aplicar valores por defecto cuando se detectan FieldInfo objects
        page_normalized = page_normalized or 1  # Default: 1
        size_normalized = size_normalized or 3  # Default: 3
        calendar_id_normalized = normalize_int(calendar_id, "calendar_id")
        role_id_normalized = normalize_int(role_id, "role_id")
        bedrooms_normalized = normalize_int(bedrooms, "bedrooms")
        min_bedrooms_normalized = normalize_int(min_bedrooms, "min_bedrooms")
        max_bedrooms_normalized = normalize_int(max_bedrooms, "max_bedrooms")
        bathrooms_normalized = normalize_int(bathrooms, "bathrooms")
        min_bathrooms_normalized = normalize_int(min_bathrooms, "min_bathrooms")
        max_bathrooms_normalized = normalize_int(max_bathrooms, "max_bathrooms")
        pets_friendly_normalized = normalize_binary_int(pets_friendly, "pets_friendly")
        allow_unit_rates_normalized = normalize_binary_int(
            allow_unit_rates, "allow_unit_rates"
        )
        computed_normalized = normalize_binary_int(computed, "computed")
        inherited_normalized = normalize_binary_int(inherited, "inherited")
        limited_normalized = normalize_binary_int(limited, "limited")
        is_bookable_normalized = normalize_binary_int(is_bookable, "is_bookable")
        include_descriptions_normalized = normalize_binary_int(
            include_descriptions, "include_descriptions"
        )
        is_active_normalized = normalize_binary_int(is_active, "is_active")
        events_allowed_normalized = normalize_binary_int(
            events_allowed, "events_allowed"
        )
        smoking_allowed_normalized = normalize_binary_int(
            smoking_allowed, "smoking_allowed"
        )
        children_allowed_normalized = normalize_binary_int(
            children_allowed, "children_allowed"
        )
        is_accessible_normalized = normalize_binary_int(is_accessible, "is_accessible")

        # Asegurar que los valores sean enteros para comparaciones
        try:
            page_normalized = int(page_normalized)
            size_normalized = int(size_normalized)
        except (ValueError, TypeError):
            raise ValidationError("Page and size must be valid integers", "parameters")

        # Validar límite total de resultados (10k máximo)
        if page_normalized * size_normalized > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
            )

        # Validar rango de habitaciones
        if (
            min_bedrooms_normalized is not None
            and max_bedrooms_normalized is not None
            and min_bedrooms_normalized > max_bedrooms_normalized
        ):
            raise ValidationError(
                "min_bedrooms cannot be greater than max_bedrooms", "min_bedrooms"
            )

        # Validar rango de baños
        if (
            min_bathrooms_normalized is not None
            and max_bathrooms_normalized is not None
            and min_bathrooms_normalized > max_bathrooms_normalized
        ):
            raise ValidationError(
                "min_bathrooms cannot be greater than max_bathrooms", "min_bathrooms"
            )

        # Validar fechas si se proporcionan
        date_params = {
            "arrival": arrival,
            "departure": departure,
            "content_updated_since": content_updated_since,
            "updated_since": updated_since,
        }

        for param_name, param_value in date_params.items():
            if param_value and not is_valid_iso8601_date(param_value):
                raise ValidationError(
                    format_date_error(param_name),
                    param_name,
                )

        # Validar unit_status
        valid_statuses = ["clean", "dirty", "occupied", "inspection", "inprogress"]
        if unit_status and unit_status not in valid_statuses:
            raise ValidationError(
                f"Invalid unit_status. Must be one of: {', '.join(valid_statuses)}",
                "unit_status",
            )

        try:
            # Crear caso de uso
            use_case = SearchUnitsUseCase(api_client)

            # La API de TrackHS usa paginación 1-based, no necesitamos conversión
            # El usuario envía page=1 para la primera página, y la API también espera page=1
            page_for_api = page_normalized

            # Crear parámetros de búsqueda
            search_params = SearchUnitsParams(
                page=page_for_api,
                size=size_normalized,
                sort_column=sort_column,
                sort_direction=sort_direction,
                search=search,
                term=term,
                unit_code=unit_code,
                short_name=short_name,
                node_id=_parse_id_string(node_id),
                amenity_id=_parse_id_string(amenity_id),
                unit_type_id=_parse_id_string(unit_type_id),
                id=_parse_id_string(id),
                calendar_id=calendar_id_normalized,
                role_id=role_id_normalized,
                bedrooms=bedrooms_normalized,
                min_bedrooms=min_bedrooms_normalized,
                max_bedrooms=max_bedrooms_normalized,
                bathrooms=bathrooms_normalized,
                min_bathrooms=min_bathrooms_normalized,
                max_bathrooms=max_bathrooms_normalized,
                pets_friendly=pets_friendly_normalized,
                allow_unit_rates=allow_unit_rates_normalized,
                computed=computed_normalized,
                inherited=inherited_normalized,
                limited=limited_normalized,
                is_bookable=is_bookable_normalized,
                include_descriptions=include_descriptions_normalized,
                is_active=is_active_normalized,
                events_allowed=events_allowed_normalized,
                smoking_allowed=smoking_allowed_normalized,
                children_allowed=children_allowed_normalized,
                is_accessible=is_accessible_normalized,
                arrival=arrival,
                departure=departure,
                content_updated_since=content_updated_since,
                updated_since=updated_since,
                unit_status=unit_status,
            )

            # Ejecutar caso de uso
            result = await use_case.execute(search_params)

            return result

        except Exception as e:
            # Manejar errores específicos de la API según documentación
            if hasattr(e, "status_code"):
                if e.status_code == 400:
                    raise ValidationError(
                        "Bad Request: Invalid parameters sent to Units API. "
                        "Common issues:\n"
                        "- Page must be >= 1 (1-based pagination)\n"
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
                        "Channel API/Units endpoints. "
                        "Contact your administrator to enable Channel API access.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        "Endpoint not found: /pms/units. "
                        "Please verify the API URL and endpoint path are correct. "
                        "The Channel API endpoint might not be available in your environment.",
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
