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
from ..utils.type_normalization import normalize_int

# Las funciones de normalización ya no son necesarias
# FastMCP maneja la validación automáticamente con Field constraints
from ..utils.user_friendly_messages import format_date_error


def _parse_id_string(
    id_value: Optional[Union[str, int, float]],
) -> Optional[Union[int, List[int]]]:
    """
    Parse ID string to int or list of ints.

    Args:
        id_value: String que puede ser "123" o "1,2,3", int directo, o float

    Returns:
        int si es un solo ID, List[int] si son múltiples, None si está vacío
    """
    if id_value is None:
        return None

    # Si ya es un int, retornarlo directamente
    if isinstance(id_value, int):
        return id_value

    # Si es float, convertir a int si no tiene decimales
    if isinstance(id_value, float):
        if id_value.is_integer():
            return int(id_value)
        return None

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

    # Si no es ni string ni int ni float, retornar None
    return None


def register_search_units(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_units mejorada"""

    @mcp.tool(name="search_units")
    @error_handler("search_units")
    async def search_units(
        # Parámetros de paginación
        page: int = Field(
            default=1,
            description="Page number (1-based indexing). Max total results: 10,000 (400 pages × 25 results max).",
            ge=1,
            le=400,
        ),
        size: int = Field(
            default=2,
            description=(
                "Number of results per page (1-25). "
                "⚠️ Para agentes de voz: usa 2-3 máximo. Las unidades tienen MUCHA información "
                "(imágenes, amenidades, descripciones). Default: 2 (optimizado para conversaciones)."
            ),
            ge=1,
            le=25,
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
        # Filtros numéricos - Usar tipos específicos con Field constraints
        calendar_id: Optional[int] = Field(
            default=None, description="Filter by calendar ID (positive integer)", ge=1
        ),
        role_id: Optional[int] = Field(
            default=None, description="Filter by role ID (positive integer)", ge=1
        ),
        # Filtros de habitaciones y baños - Tipos string con conversión interna
        bedrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by exact number of bedrooms. "
                "Pass the number as a string. "
                "Examples: '2' for 2 bedrooms, '4' for 4 bedrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        min_bedrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by minimum number of bedrooms. "
                "Pass the number as a string. "
                "Examples: '1' for 1+ bedrooms, '3' for 3+ bedrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        max_bedrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by maximum number of bedrooms. "
                "Pass the number as a string. "
                "Examples: '2' for up to 2 bedrooms, '5' for up to 5 bedrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        bathrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by exact number of bathrooms. "
                "Pass the number as a string. "
                "Examples: '1' for 1 bathroom, '3' for 3 bathrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        min_bathrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by minimum number of bathrooms. "
                "Pass the number as a string. "
                "Examples: '1' for 1+ bathrooms, '2' for 2+ bathrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        max_bathrooms: Optional[str] = Field(
            default=None,
            description=(
                "Filter by maximum number of bathrooms. "
                "Pass the number as a string. "
                "Examples: '2' for up to 2 bathrooms, '4' for up to 4 bathrooms. "
                "Valid range: 0 or greater."
            ),
        ),
        # Filtros booleanos (0/1) - Tipos string con conversión interna
        pets_friendly: Optional[str] = Field(
            default=None,
            description=(
                "Filter units that allow pets. "
                "Pass '1' for pet-friendly units, '0' for units that don't allow pets. "
                "Leave empty to show all units regardless of pet policy."
            ),
        ),
        allow_unit_rates: Optional[str] = Field(
            default=None,
            description=(
                "Filter units that allow unit-specific rates. "
                "Pass '1' for units with custom rates, '0' for standard rates only. "
                "Leave empty to show all units regardless of rate type."
            ),
        ),
        computed: Optional[str] = Field(
            default=None,
            description=(
                "Filter computed units (units with calculated attributes). "
                "Pass '1' for computed units, '0' for non-computed units. "
                "Leave empty to show all units regardless of computation status."
            ),
        ),
        inherited: Optional[str] = Field(
            default=None,
            description=(
                "Filter inherited units (units with inherited attributes). "
                "Pass '1' for inherited units, '0' for non-inherited units. "
                "Leave empty to show all units regardless of inheritance status."
            ),
        ),
        limited: Optional[str] = Field(
            default=None,
            description=(
                "Filter limited availability units. "
                "Pass '1' for limited units, '0' for unlimited units. "
                "Leave empty to show all units regardless of availability limits."
            ),
        ),
        is_bookable: Optional[str] = Field(
            default=None,
            description=(
                "Filter bookable units. "
                "Pass '1' for bookable units, '0' for non-bookable units. "
                "Leave empty to show all units regardless of booking status."
            ),
        ),
        include_descriptions: Optional[str] = Field(
            default=None,
            description=(
                "Include unit descriptions in response. "
                "Pass '1' to include descriptions, '0' to exclude them. "
                "Leave empty to use default behavior."
            ),
        ),
        is_active: Optional[str] = Field(
            default=None,
            description=(
                "Filter by active units. "
                "Pass '1' for active units, '0' for inactive units. "
                "Leave empty to show all units regardless of status."
            ),
        ),
        events_allowed: Optional[str] = Field(
            default=None,
            description=(
                "Filter units that allow events. "
                "Pass '1' for units allowing events, '0' for units that don't allow events. "
                "Leave empty to show all units regardless of event policy."
            ),
        ),
        smoking_allowed: Optional[str] = Field(
            default=None,
            description=(
                "Filter units that allow smoking. "
                "Pass '1' for units allowing smoking, '0' for non-smoking units. "
                "Leave empty to show all units regardless of smoking policy."
            ),
        ),
        children_allowed: Optional[str] = Field(
            default=None,
            description=(
                "Filter units that allow children. "
                "Pass '1' for units allowing children, '0' for adults-only units. "
                "Leave empty to show all units regardless of children policy."
            ),
        ),
        is_accessible: Optional[str] = Field(
            default=None,
            description=(
                "Filter accessible/wheelchair-friendly units. "
                "Pass '1' for accessible units, '0' for non-accessible units. "
                "Leave empty to show all units regardless of accessibility."
            ),
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
        - Flexible parameter types (accepts both string and integer for numeric/boolean filters)

        Parameter Types:
        - Numeric parameters (bedrooms, bathrooms, etc.): Accept numeric strings (e.g., '3', '4') with automatic conversion
        - Boolean parameters (pets_friendly, is_active, etc.): Accept '0'/'1' as strings with automatic conversion
        - Text parameters (search, term, etc.): Accept string only
        - Date parameters: Accept ISO 8601 formatted strings with pattern validation
        - ID parameters: Accept integer, string, or comma-separated strings

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

        # Convertir parámetros numéricos de string a int
        bedrooms = normalize_int(bedrooms, "bedrooms")
        min_bedrooms = normalize_int(min_bedrooms, "min_bedrooms")
        max_bedrooms = normalize_int(max_bedrooms, "max_bedrooms")
        bathrooms = normalize_int(bathrooms, "bathrooms")
        min_bathrooms = normalize_int(min_bathrooms, "min_bathrooms")
        max_bathrooms = normalize_int(max_bathrooms, "max_bathrooms")
        calendar_id = normalize_int(calendar_id, "calendar_id")
        role_id = normalize_int(role_id, "role_id")

        # Convertir parámetros booleanos (0/1)
        pets_friendly = normalize_int(pets_friendly, "pets_friendly")
        allow_unit_rates = normalize_int(allow_unit_rates, "allow_unit_rates")
        computed = normalize_int(computed, "computed")
        inherited = normalize_int(inherited, "inherited")
        limited = normalize_int(limited, "limited")
        is_bookable = normalize_int(is_bookable, "is_bookable")
        include_descriptions = normalize_int(
            include_descriptions, "include_descriptions"
        )
        is_active = normalize_int(is_active, "is_active")
        events_allowed = normalize_int(events_allowed, "events_allowed")
        smoking_allowed = normalize_int(smoking_allowed, "smoking_allowed")
        children_allowed = normalize_int(children_allowed, "children_allowed")
        is_accessible = normalize_int(is_accessible, "is_accessible")

        # Validar límite total de resultados (10k máximo)
        if page * size > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
            )

        # Validar rango de habitaciones
        if (
            min_bedrooms is not None
            and max_bedrooms is not None
            and min_bedrooms > max_bedrooms
        ):
            raise ValidationError(
                "min_bedrooms cannot be greater than max_bedrooms", "min_bedrooms"
            )

        # Validar rango de baños
        if (
            min_bathrooms is not None
            and max_bathrooms is not None
            and min_bathrooms > max_bathrooms
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
            page_for_api = page

            # Crear parámetros de búsqueda
            search_params = SearchUnitsParams(
                page=page_for_api,
                size=size,
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
                calendar_id=calendar_id,
                role_id=role_id,
                bedrooms=bedrooms,
                min_bedrooms=min_bedrooms,
                max_bedrooms=max_bedrooms,
                bathrooms=bathrooms,
                min_bathrooms=min_bathrooms,
                max_bathrooms=max_bathrooms,
                pets_friendly=pets_friendly,
                allow_unit_rates=allow_unit_rates,
                computed=computed,
                inherited=inherited,
                limited=limited,
                is_bookable=is_bookable,
                include_descriptions=include_descriptions,
                is_active=is_active,
                events_allowed=events_allowed,
                smoking_allowed=smoking_allowed,
                children_allowed=children_allowed,
                is_accessible=is_accessible,
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
