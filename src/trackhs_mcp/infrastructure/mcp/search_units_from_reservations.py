"""
Herramienta MCP alternativa para buscar unidades usando datos embebidos de reservaciones
Solución para el problema del endpoint /pms/units que devuelve 400 Bad Request
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_reservations import SearchReservationsUseCase
from ...domain.entities.reservations import SearchReservationsParams
from ..utils.error_handling import error_handler


def register_search_units_from_reservations(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta alternativa para buscar unidades"""

    @mcp.tool
    @error_handler("search_units_from_reservations")
    async def search_units_from_reservations(
        page: int = 0,
        size: int = 25,
        search: Optional[str] = None,
        node_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        pets_friendly: Optional[int] = None,
        is_active: Optional[int] = None,
        max_units: int = 1000,
    ):
        """
        Search units using embedded data from reservations.

        This is an alternative to the /pms/units endpoint that returns 400 Bad Request.
        It extracts unit information from reservation data, which includes complete
        unit details in the embedded 'unit' object.

        **Key Features:**
        - ✅ Works with existing PMS API authentication
        - ✅ Provides complete unit information
        - ✅ No additional API configuration required
        - ✅ Data is always up-to-date with reservations

        **Limitations:**
        - Only includes units that have reservations
        - Requires querying reservations first
        - May not include all units in the system

        **Parameters:**
        - page: Page number (0-based)
        - size: Page size (max 1000)
        - search: Text search in unit names
        - node_id: Filter by node ID
        - unit_type_id: Filter by unit type ID
        - bedrooms: Filter by number of bedrooms
        - bathrooms: Filter by number of bathrooms
        - pets_friendly: Filter by pet-friendly units (0/1)
        - is_active: Filter by active units (0/1)
        - max_units: Maximum number of units to return (default: 1000)

        **Returns:**
        Complete unit data with embedded objects (amenities, rooms, bed types, etc.)
        and pagination information.

        **Example Usage:**

        # Basic search
        search_units_from_reservations(page=0, size=25)

        # Search by property features
        search_units_from_reservations(
            bedrooms=2,
            bathrooms=2,
            pets_friendly=1
        )

        # Search by location
        search_units_from_reservations(
            node_id="1,2,3",
            search="pool"
        )
        """

        try:
            # Crear caso de uso para reservaciones
            reservations_use_case = SearchReservationsUseCase(api_client)

            # Construir parámetros para buscar reservaciones
            # Usar un rango amplio de fechas para obtener más unidades
            search_params = SearchReservationsParams(
                page=1,  # Empezar desde la primera página (SearchReservationsParams usa 1-based)
                size=1000,  # Obtener muchas reservaciones para tener más unidades
                # Filtros opcionales
                node_id=node_id,
                unit_type_id=unit_type_id,
            )

            # Ejecutar búsqueda de reservaciones
            reservations_result = await reservations_use_case.execute(search_params)

            # Extraer unidades de las reservaciones
            units = _extract_units_from_reservations(
                reservations_result,
                search=search,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                pets_friendly=pets_friendly,
                is_active=is_active,
                max_units=max_units,
            )

            # Aplicar paginación a las unidades
            start_idx = page * size
            end_idx = start_idx + size
            paginated_units = units[start_idx:end_idx]

            # Construir respuesta en formato similar al endpoint original
            total_units = len(units)
            total_pages = (total_units + size - 1) // size

            response = {
                "_embedded": {"units": paginated_units},
                "page": page,
                "page_count": total_pages,
                "page_size": size,
                "total_items": total_units,
                "_links": {
                    "self": {"href": f"/pms/units?page={page}&size={size}"},
                    "first": {"href": "/pms/units?page=0&size={size}"},
                    "last": {"href": f"/pms/units?page={total_pages-1}&size={size}"},
                },
            }

            # Agregar enlaces de navegación si es necesario
            if page > 0:
                response["_links"]["prev"] = {
                    "href": f"/pms/units?page={page-1}&size={size}"
                }
            if page < total_pages - 1:
                response["_links"]["next"] = {
                    "href": f"/pms/units?page={page+1}&size={size}"
                }

            return response

        except Exception as e:
            # Manejar errores específicos
            if hasattr(e, "status_code"):
                if e.status_code == 401:
                    raise ValueError(
                        "Unauthorized: Invalid authentication credentials. "
                        "Please verify your TRACKHS_USERNAME and TRACKHS_PASSWORD "
                        "are correct and not expired."
                    )
                elif e.status_code == 403:
                    raise ValueError(
                        "Forbidden: Insufficient permissions for this operation. "
                        "Please verify your account has access to reservations."
                    )
                elif e.status_code == 500:
                    raise ValueError(
                        "Internal Server Error: API temporarily unavailable. "
                        "Please try again later or contact support."
                    )
            raise ValueError(f"Failed to search units from reservations: {str(e)}")


def _extract_units_from_reservations(
    reservations_result: Dict[str, Any],
    search: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    pets_friendly: Optional[int] = None,
    is_active: Optional[int] = None,
    max_units: int = 1000,
) -> List[Dict[str, Any]]:
    """
    Extrae y filtra unidades de los datos de reservaciones
    """
    units = {}

    # Obtener reservaciones del resultado
    reservations = reservations_result.get("_embedded", {}).get("reservations", [])

    for reservation in reservations:
        unit_data = reservation.get("unit", {})
        if not unit_data:
            continue

        unit_id = unit_data.get("id")
        if not unit_id or unit_id in units:
            continue

        # Aplicar filtros
        if not _matches_filters(
            unit_data, search, bedrooms, bathrooms, pets_friendly, is_active
        ):
            continue

        # Limpiar y formatear datos de la unidad
        cleaned_unit = _clean_unit_data(unit_data)
        units[unit_id] = cleaned_unit

        # Limitar número de unidades
        if len(units) >= max_units:
            break

    return list(units.values())


def _matches_filters(
    unit_data: Dict[str, Any],
    search: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    pets_friendly: Optional[int] = None,
    is_active: Optional[int] = None,
) -> bool:
    """Verifica si la unidad coincide con los filtros aplicados"""

    # Filtro de búsqueda de texto
    if search:
        search_lower = search.lower()
        unit_name = unit_data.get("name", "").lower()
        unit_code = unit_data.get("unitCode", "").lower()
        if search_lower not in unit_name and search_lower not in unit_code:
            return False

    # Filtro de habitaciones
    if bedrooms is not None:
        unit_bedrooms = unit_data.get("bedrooms", 0)
        if unit_bedrooms != bedrooms:
            return False

    # Filtro de baños
    if bathrooms is not None:
        unit_bathrooms = unit_data.get("bathrooms", 0)
        if unit_bathrooms != bathrooms:
            return False

    # Filtro de mascotas
    if pets_friendly is not None:
        unit_pets_friendly = 1 if unit_data.get("petsFriendly", False) else 0
        if unit_pets_friendly != pets_friendly:
            return False

    # Filtro de estado activo
    if is_active is not None:
        # Asumir que si tiene reservaciones, está activo
        unit_is_active = 1
        if unit_is_active != is_active:
            return False

    return True


def _clean_unit_data(unit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia y formatea los datos de la unidad"""

    # Campos básicos
    cleaned = {
        "id": unit_data.get("id"),
        "name": unit_data.get("name"),
        "shortName": unit_data.get("shortName"),
        "unitCode": unit_data.get("unitCode"),
        "headline": unit_data.get("headline"),
        "shortDescription": unit_data.get("shortDescription"),
        "longDescription": unit_data.get("longDescription"),
        "houseRules": unit_data.get("houseRules"),
        "nodeId": unit_data.get("nodeId"),
        "directions": unit_data.get("directions"),
        "checkinDetails": unit_data.get("checkinDetails"),
        "timezone": unit_data.get("timezone"),
        "checkinTime": unit_data.get("checkinTime"),
        "hasEarlyCheckin": unit_data.get("hasEarlyCheckin"),
        "earlyCheckinTime": unit_data.get("earlyCheckinTime"),
        "checkoutTime": unit_data.get("checkoutTime"),
        "hasLateCheckout": unit_data.get("hasLateCheckout"),
        "lateCheckoutTime": unit_data.get("lateCheckoutTime"),
        "minBookingWindow": unit_data.get("minBookingWindow"),
        "maxBookingWindow": unit_data.get("maxBookingWindow"),
        "website": unit_data.get("website"),
        "phone": unit_data.get("phone"),
        "streetAddress": unit_data.get("streetAddress"),
        "extendedAddress": unit_data.get("extendedAddress"),
        "locality": unit_data.get("locality"),
        "region": unit_data.get("region"),
        "postal": unit_data.get("postal"),
        "country": unit_data.get("country"),
        "latitude": unit_data.get("latitude"),
        "longitude": unit_data.get("longitude"),
        "petsFriendly": unit_data.get("petsFriendly"),
        "maxPets": unit_data.get("maxPets"),
        "eventsAllowed": unit_data.get("eventsAllowed"),
        "smokingAllowed": unit_data.get("smokingAllowed"),
        "childrenAllowed": unit_data.get("childrenAllowed"),
        "minimumAgeLimit": unit_data.get("minimumAgeLimit"),
        "isAccessible": unit_data.get("isAccessible"),
        "area": unit_data.get("area"),
        "floors": unit_data.get("floors"),
        "maxOccupancy": unit_data.get("maxOccupancy"),
        "securityDeposit": unit_data.get("securityDeposit"),
        "bedrooms": unit_data.get("bedrooms"),
        "fullBathrooms": unit_data.get("fullBathrooms"),
        "threeQuarterBathrooms": unit_data.get("threeQuarterBathrooms"),
        "halfBathrooms": unit_data.get("halfBathrooms"),
        "bedTypes": unit_data.get("bedTypes"),
        "rooms": unit_data.get("rooms"),
        "amenities": unit_data.get("amenities"),
        "amenityDescription": unit_data.get("amenityDescription"),
        "custom": unit_data.get("custom"),
        "taxId": unit_data.get("taxId"),
        "localOffice": unit_data.get("localOffice"),
        "updatedAt": unit_data.get("updatedAt"),
    }

    # Remover campos None
    cleaned = {k: v for k, v in cleaned.items() if v is not None}

    return cleaned
