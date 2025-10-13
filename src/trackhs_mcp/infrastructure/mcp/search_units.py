"""
Herramienta MCP para buscar unidades en Track HS Channel API
Basado en la especificación completa de la API Get Units Collection
"""

from typing import TYPE_CHECKING, List, Literal, Optional, Union

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_units import SearchUnitsUseCase
from ...domain.entities.units import SearchUnitsParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler


def register_search_units(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_units"""

    @mcp.tool
    @error_handler("search_units")
    async def search_units(
        page: Union[int, str] = 1,
        size: Union[int, str] = 25,
        sort_column: Literal["id", "name", "nodeName", "unitTypeName"] = "name",
        sort_direction: Literal["asc", "desc"] = "asc",
        search: Optional[str] = None,
        term: Optional[str] = None,
        unit_code: Optional[str] = None,
        short_name: Optional[str] = None,
        node_id: Optional[str] = None,
        amenity_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        id: Optional[str] = None,
        calendar_id: Union[int, str, None] = None,
        role_id: Union[int, str, None] = None,
        bedrooms: Union[int, str, None] = None,
        min_bedrooms: Union[int, str, None] = None,
        max_bedrooms: Union[int, str, None] = None,
        bathrooms: Union[int, str, None] = None,
        min_bathrooms: Union[int, str, None] = None,
        max_bathrooms: Union[int, str, None] = None,
        pets_friendly: Union[Literal[0, 1], str, None] = None,
        allow_unit_rates: Union[Literal[0, 1], str, None] = None,
        computed: Union[Literal[0, 1], str, None] = None,
        inherited: Union[Literal[0, 1], str, None] = None,
        limited: Union[Literal[0, 1], str, None] = None,
        is_bookable: Union[Literal[0, 1], str, None] = None,
        include_descriptions: Union[Literal[0, 1], str, None] = None,
        is_active: Union[Literal[0, 1], str, None] = None,
        events_allowed: Union[Literal[0, 1], str, None] = None,
        smoking_allowed: Union[Literal[0, 1], str, None] = None,
        children_allowed: Union[Literal[0, 1], str, None] = None,
        is_accessible: Union[Literal[0, 1], str, None] = None,
        arrival: Optional[str] = None,
        departure: Optional[str] = None,
        content_updated_since: Optional[str] = None,
        updated_since: Optional[str] = None,
        unit_status: Optional[
            Literal["clean", "dirty", "occupied", "inspection", "inprogress"]
        ] = None,
    ):
        """
        Search units in Track HS Channel API with comprehensive filtering options.

        This MCP tool provides advanced unit search capabilities with full Channel API
        compatibility, including pagination, filtering, sorting, and comprehensive
        unit information retrieval.

        **Key Features:**
        - ✅ Full Channel API compatibility with all 29+ parameters
        - ✅ Advanced pagination (limited to 10k total results)
        - ✅ Comprehensive filtering (dates, IDs, amenities, etc.)
        - ✅ Flexible sorting options
        - ✅ Robust error handling
        - ✅ MCP-optimized for AI model integration

        **Examples:**

        # Basic search
        search_units(page=1, size=25)

        # Search by property features
        search_units(
            bedrooms=2,
            bathrooms=2,
            pets_friendly=1,
            is_active=1
        )

        # Search by availability
        search_units(
            arrival="2024-01-01",
            departure="2024-01-07",
            is_bookable=1
        )

        # Search by amenities
        search_units(
            amenity_id="1,2,3",
            pets_friendly=1,
            events_allowed=1
        )

        # Search by location
        search_units(
            node_id="1,2,3",
            locality="Miami"
        )

        **Parameters:**
        - page: Page number (1-based, max 10k total results)
        - size: Page size (max 1000, limited to 10k total results)
        - sort_column: Sort by field (id, name, nodeName, unitTypeName)
        - sort_direction: Sort direction (asc/desc)
        - search: Text search in names/descriptions
        - term: Substring search matching on term
        - unit_code: Search on unitCode, exact match or add % for wildcard
        - short_name: Search on shortName, exact match or add % for wildcard
        - node_id: Node ID(s) - single int, comma-separated, or array
        - amenity_id: Amenity ID(s) - single int, comma-separated, or array
        - unit_type_id: Unit type ID(s) - single int, comma-separated, or array
        - id: Filter by Unit IDs
        - calendar_id: Return units matching this unit's type with calendar group id
        - role_id: Return units by specific roleId
        - bedrooms: Exact number of bedrooms
        - min_bedrooms/max_bedrooms: Range of bedrooms
        - bathrooms: Exact number of bathrooms
        - min_bathrooms/max_bathrooms: Range of bathrooms
        - pets_friendly: Pet friendly units (0/1)
        - allow_unit_rates: Units that allow unit rates (0/1)
        - computed: Additional computed values (0/1)
        - inherited: Additional inherited attributes (0/1)
        - limited: Very limited attributes (0/1)
        - is_bookable: Bookable units (0/1)
        - include_descriptions: Include descriptions (0/1)
        - is_active: Active units (0/1)
        - arrival/departure: Availability date range (ISO 8601)
        - content_updated_since: Content changes since timestamp (ISO 8601)
        - updated_since: Updated since timestamp (ISO 8601) - deprecated
        - unit_status: Unit status (clean, dirty, occupied, inspection, inprogress)

        **Returns:**
        Complete unit data with embedded objects (amenities, rooms, bed types, etc.)
        and pagination information.

        **Error Handling:**
        - Validates all parameters according to Channel API specification
        - Handles API errors (401, 403, 500) with descriptive messages
        - Validates ISO 8601 date formats strictly
        - Enforces 10k total results limit
        - Validates boolean parameters (0/1 only)
        """
        # Validar límite total de resultados (10k máximo) - validación de negocio
        # Ajustar page para cálculo (API usa 1-based, pero calculamos con 0-based)
        adjusted_page = max(0, page - 1) if page > 0 else 0
        if adjusted_page * size > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
            )

        # Validar fechas si se proporcionan
        date_params = {
            "arrival": arrival,
            "departure": departure,
            "content_updated_since": content_updated_since,
            "updated_since": updated_since,
        }

        for param_name, param_value in date_params.items():
            if param_value and not _is_valid_date_format(param_value):
                raise ValidationError(
                    f"Invalid date format for {param_name}. Use ISO 8601 format.",
                    param_name,
                )

        # Validar rangos de habitaciones y baños
        if min_bedrooms is not None and max_bedrooms is not None:
            if min_bedrooms > max_bedrooms:
                raise ValidationError(
                    "min_bedrooms must be <= max_bedrooms", "min_bedrooms"
                )

        if min_bathrooms is not None and max_bathrooms is not None:
            if min_bathrooms > max_bathrooms:
                raise ValidationError(
                    "min_bathrooms must be <= max_bathrooms", "min_bathrooms"
                )

        try:
            # Crear caso de uso
            use_case = SearchUnitsUseCase(api_client)

            # Convertir parámetros de string a tipos correctos si es necesario
            def _convert_param(param, target_type):
                """Convierte parámetro a tipo correcto con manejo robusto de strings"""
                if param is None:
                    return None
                if isinstance(param, target_type):
                    return param

                # Si es string, intentar convertir
                if isinstance(param, str):
                    try:
                        if target_type == int:
                            return int(param)
                        elif target_type == str:
                            return str(param)
                        # Para Literal[0, 1], convertir string a int primero
                        elif hasattr(target_type, "__args__") and target_type.__args__:
                            # Es un Union, buscar el tipo int
                            for arg in target_type.__args__:
                                if arg == int or (
                                    hasattr(arg, "__origin__")
                                    and arg.__origin__ is type(None)
                                ):
                                    continue
                                elif hasattr(arg, "__args__") and arg.__args__ == (
                                    0,
                                    1,
                                ):
                                    # Es Literal[0, 1]
                                    converted = int(param)
                                    if converted in [0, 1]:
                                        return converted
                                    else:
                                        raise ValueError(
                                            f"Value {converted} not in Literal[0, 1]"
                                        )
                                elif arg == int:
                                    return int(param)
                            return param
                        else:
                            return param
                    except (ValueError, TypeError) as e:
                        raise ValidationError(
                            f"Invalid parameter value: {param}. Expected {target_type.__name__}",
                            "parameter",
                        )

                # Si no es string, intentar conversión directa
                try:
                    if target_type == int:
                        return int(param)
                    elif target_type == str:
                        return str(param)
                    else:
                        return param
                except (ValueError, TypeError):
                    return param

            # Crear parámetros de búsqueda con conversión de tipos
            search_params = SearchUnitsParams(
                page=_convert_param(page, int),
                size=_convert_param(size, int),
                sort_column=sort_column,
                sort_direction=sort_direction,
                search=search,
                term=term,
                unit_code=unit_code,
                short_name=short_name,
                node_id=_parse_id_string(node_id) if node_id else None,
                amenity_id=_parse_id_string(amenity_id) if amenity_id else None,
                unit_type_id=_parse_id_string(unit_type_id) if unit_type_id else None,
                id=_parse_id_list(id) if id else None,
                calendar_id=_convert_param(calendar_id, int),
                role_id=_convert_param(role_id, int),
                bedrooms=_convert_param(bedrooms, int),
                min_bedrooms=_convert_param(min_bedrooms, int),
                max_bedrooms=_convert_param(max_bedrooms, int),
                bathrooms=_convert_param(bathrooms, int),
                min_bathrooms=_convert_param(min_bathrooms, int),
                max_bathrooms=_convert_param(max_bathrooms, int),
                pets_friendly=_convert_param(pets_friendly, int),
                allow_unit_rates=_convert_param(allow_unit_rates, int),
                computed=_convert_param(computed, int),
                inherited=_convert_param(inherited, int),
                limited=_convert_param(limited, int),
                is_bookable=_convert_param(is_bookable, int),
                include_descriptions=_convert_param(include_descriptions, int),
                is_active=_convert_param(is_active, int),
                events_allowed=_convert_param(events_allowed, int),
                smoking_allowed=_convert_param(smoking_allowed, int),
                children_allowed=_convert_param(children_allowed, int),
                is_accessible=_convert_param(is_accessible, int),
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
                    # Logging adicional para 400 Bad Request
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"400 Bad Request - Params enviados: {search_params.model_dump()}"
                    )
                    logger.error(f"400 Bad Request - Error details: {str(e)}")
                    logger.error(f"400 Bad Request - Error type: {type(e).__name__}")
                    logger.error(f"400 Bad Request - Error attributes: {dir(e)}")

                    # Capturar error body si está disponible
                    error_body = getattr(e, "response_text", str(e))
                    logger.error(f"400 Bad Request - Response body: {error_body}")

                    # Intentar obtener más información del error
                    if hasattr(e, "args") and e.args:
                        logger.error(f"400 Bad Request - Error args: {e.args}")

                    raise ValidationError(
                        "Bad Request: Invalid parameters sent to Units API. "
                        "Common issues:\n"
                        "- Page must be >= 1 (1-based pagination)\n"
                        "- Numeric parameters (bedrooms, bathrooms) must be integers\n"
                        "- Boolean parameters (pets_friendly, is_active) must be 0 or 1\n"
                        "- Date parameters must be in ISO 8601 format (YYYY-MM-DD)\n"
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
            raise ValidationError(f"API request failed: {str(e)}", "api")


def _is_valid_date_format(date_string: str) -> bool:
    """Valida formato de fecha con múltiples formatos soportados"""
    try:
        import re
        from datetime import datetime

        # Patrones de fecha soportados
        patterns = [
            # ISO 8601 completo con timezone
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$",
            # ISO 8601 sin timezone
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$",
            # Solo fecha ISO
            r"^\d{4}-\d{2}-\d{2}$",
            # Formato con espacio (alternativo)
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
        ]

        # Verificar si coincide con algún patrón
        for pattern in patterns:
            if re.match(pattern, date_string):
                # Intentar parsear la fecha
                try:
                    if "T" in date_string:
                        # Formato ISO con tiempo
                        if date_string.endswith("Z"):
                            datetime.fromisoformat(date_string.replace("Z", "+00:00"))
                        elif "+" in date_string or "-" in date_string[-6:]:
                            datetime.fromisoformat(date_string)
                        else:
                            datetime.fromisoformat(date_string)
                    else:
                        # Solo fecha
                        datetime.fromisoformat(date_string)
                    return True
                except ValueError:
                    continue

        return False
    except (ValueError, AttributeError):
        return False


def _parse_id_string(id_string: Union[str, int, List[int]]) -> Union[int, List[int]]:
    """
    Parsea un string de ID que puede ser:
    - Un entero simple: "48" o 48
    - Múltiples IDs separados por comas: "48,49,50"
    - Array en formato string: "[48,49,50]"
    - Lista de Python: [1, 2, 3]
    """
    # Si ya es un entero, devolverlo directamente
    if isinstance(id_string, int):
        return id_string

    # Si ya es una lista, devolverla directamente
    if isinstance(id_string, list):
        return id_string

    if not id_string or not str(id_string).strip():
        raise ValidationError("ID string cannot be empty", "id")

    # Limpiar espacios
    id_string = id_string.strip()

    # Si es un array en formato string, parsearlo
    if id_string.startswith("[") and id_string.endswith("]"):
        try:
            # Remover corchetes y dividir por comas
            content = id_string[1:-1].strip()
            if not content:
                raise ValidationError("Empty array not allowed", "id")
            # Dividir por comas y convertir a enteros
            ids = [int(x.strip()) for x in content.split(",")]
            return ids if len(ids) > 1 else ids[0]
        except ValueError:
            raise ValidationError(f"Invalid array format: {id_string}", "id")

    # Si contiene comas, es una lista de IDs
    if "," in id_string:
        try:
            ids = [int(x.strip()) for x in id_string.split(",") if x.strip()]
            if not ids:
                raise ValidationError("No valid IDs found", "id")
            return ids if len(ids) > 1 else ids[0]
        except ValueError:
            raise ValidationError(f"Invalid ID format: {id_string}", "id")

    # Es un ID único
    try:
        return int(id_string)
    except ValueError:
        raise ValidationError(f"Invalid ID format: {id_string}", "id")


def _parse_id_list(id_string: str) -> List[int]:
    """
    Parsea un string de IDs que puede ser:
    - Múltiples IDs separados por comas: "48,49,50"
    - Array en formato string: "[48,49,50]"
    """
    if not id_string or not str(id_string).strip():
        raise ValidationError("ID string cannot be empty", "id")

    # Limpiar espacios
    id_string = id_string.strip()

    # Si es un array en formato string, parsearlo
    if id_string.startswith("[") and id_string.endswith("]"):
        try:
            # Remover corchetes y dividir por comas
            content = id_string[1:-1].strip()
            if not content:
                raise ValidationError("Empty array not allowed", "id")
            # Dividir por comas y convertir a enteros
            return [int(x.strip()) for x in content.split(",")]
        except ValueError:
            raise ValidationError(f"Invalid array format: {id_string}", "id")

    # Si contiene comas, es una lista de IDs
    if "," in id_string:
        try:
            ids = [int(x.strip()) for x in id_string.split(",") if x.strip()]
            if not ids:
                raise ValidationError("No valid IDs found", "id")
            return ids
        except ValueError:
            raise ValidationError(f"Invalid ID format: {id_string}", "id")

    # Es un ID único, devolver como lista
    try:
        return [int(id_string)]
    except ValueError:
        raise ValidationError(f"Invalid ID format: {id_string}", "id")
