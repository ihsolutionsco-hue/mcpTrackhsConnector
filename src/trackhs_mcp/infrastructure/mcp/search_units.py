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
        page: int = 0,
        size: int = 25,
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
        calendar_id: Optional[int] = None,
        role_id: Optional[int] = None,
        bedrooms: Optional[int] = None,
        min_bedrooms: Optional[int] = None,
        max_bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        min_bathrooms: Optional[int] = None,
        max_bathrooms: Optional[int] = None,
        pets_friendly: Optional[Literal[0, 1]] = None,
        allow_unit_rates: Optional[Literal[0, 1]] = None,
        computed: Optional[Literal[0, 1]] = None,
        inherited: Optional[Literal[0, 1]] = None,
        limited: Optional[Literal[0, 1]] = None,
        is_bookable: Optional[Literal[0, 1]] = None,
        include_descriptions: Optional[Literal[0, 1]] = None,
        is_active: Optional[Literal[0, 1]] = None,
        events_allowed: Optional[Literal[0, 1]] = None,
        smoking_allowed: Optional[Literal[0, 1]] = None,
        children_allowed: Optional[Literal[0, 1]] = None,
        is_accessible: Optional[Literal[0, 1]] = None,
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
        search_units(page=0, size=25)

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
        - page: Page number (0-based, max 10k total results)
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
        if page * size > 10000:
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

            # Crear parámetros de búsqueda
            search_params = SearchUnitsParams(
                page=page,
                size=size,
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
                    # Logging adicional para 400 Bad Request
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"400 Bad Request - Params enviados: {search_params.model_dump()}"
                    )
                    logger.error(f"400 Bad Request - Error details: {str(e)}")
                    # Capturar error body si está disponible
                    error_body = getattr(e, "response_text", str(e))
                    logger.error(f"400 Bad Request - Response body: {error_body}")
                    raise ValidationError(
                        "Bad Request: Invalid parameters sent to Units API. "
                        "Please check the parameter format and values. "
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
                        "Channel API/Units endpoints.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        "Endpoint not found: /pms/units. "
                        "Please verify the API URL and endpoint path are correct.",
                        "endpoint",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Internal Server Error: API temporarily unavailable. "
                        "Please try again later or contact support.",
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
