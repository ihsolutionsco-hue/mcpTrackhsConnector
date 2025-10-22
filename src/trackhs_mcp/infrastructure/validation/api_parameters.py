"""
Validación de parámetros de API para TrackHS
Asegura que solo se usen parámetros soportados por la API oficial
"""

from enum import Enum
from typing import Any, Dict, Optional, Set


class TrackHSAPIVersion(Enum):
    """Versiones de API soportadas"""

    V2 = "v2"


class SearchReservationsV2Parameters:
    """
    Parámetros oficiales soportados por la API TrackHS V2 para search_reservations
    Basado en la documentación oficial: search reservations v2.md
    """

    # Parámetros de paginación
    PAGINATION = {"page", "size"}

    # Parámetros de ordenamiento
    SORTING = {"sortColumn", "sortDirection"}

    # Parámetros de búsqueda
    SEARCH = {"search", "tags"}

    # Filtros por IDs
    ID_FILTERS = {
        "nodeId",
        "unitId",
        "reservationTypeId",
        "contactId",
        "travelAgentId",
        "campaignId",
        "userId",
        "unitTypeId",
        "rateTypeId",
    }

    # Filtros de fechas
    DATE_FILTERS = {
        "bookedStart",
        "bookedEnd",
        "arrivalStart",
        "arrivalEnd",
        "departureStart",
        "departureEnd",
        "updatedSince",
    }

    # Otros filtros
    OTHER_FILTERS = {"status", "inHouseToday", "groupId", "checkinOfficeId", "scroll"}

    # Todos los parámetros soportados
    ALL_SUPPORTED = (
        PAGINATION | SORTING | SEARCH | ID_FILTERS | DATE_FILTERS | OTHER_FILTERS
    )

    # Parámetros NO soportados (que fueron removidos)
    NOT_SUPPORTED = {"folioId"}  # No soportado por la API oficial


def validate_search_reservations_parameters(
    parameters: Dict[str, Any], api_version: TrackHSAPIVersion = TrackHSAPIVersion.V2
) -> Dict[str, Any]:
    """
    Valida que los parámetros sean compatibles con la API oficial de TrackHS

    Args:
        parameters: Diccionario de parámetros a validar
        api_version: Versión de API a validar

    Returns:
        Diccionario con parámetros válidos

    Raises:
        ValueError: Si se encuentran parámetros no soportados
    """
    if api_version == TrackHSAPIVersion.V2:
        supported_params = SearchReservationsV2Parameters.ALL_SUPPORTED
        not_supported = SearchReservationsV2Parameters.NOT_SUPPORTED
    else:
        raise ValueError(f"API version {api_version} not supported")

    # Verificar parámetros no soportados
    invalid_params = []
    for param in parameters.keys():
        if param in not_supported:
            invalid_params.append(param)

    if invalid_params:
        raise ValueError(
            f"Parámetros no soportados por la API {api_version.value}: {invalid_params}. "
            f"Parámetros soportados: {sorted(supported_params)}"
        )

    # Filtrar solo parámetros soportados
    valid_parameters = {
        param: value for param, value in parameters.items() if param in supported_params
    }

    return valid_parameters


def get_supported_parameters(
    api_version: TrackHSAPIVersion = TrackHSAPIVersion.V2,
) -> Set[str]:
    """
    Obtiene la lista de parámetros soportados para la versión de API especificada

    Args:
        api_version: Versión de API

    Returns:
        Conjunto de parámetros soportados
    """
    if api_version == TrackHSAPIVersion.V2:
        return SearchReservationsV2Parameters.ALL_SUPPORTED
    else:
        raise ValueError(f"API version {api_version} not supported")


def get_parameter_description(
    parameter: str, api_version: TrackHSAPIVersion = TrackHSAPIVersion.V2
) -> Optional[str]:
    """
    Obtiene la descripción de un parámetro según la documentación oficial

    Args:
        parameter: Nombre del parámetro
        api_version: Versión de API

    Returns:
        Descripción del parámetro o None si no está soportado
    """
    descriptions = {
        "page": "Page number (0-based indexing). Max total results: 10,000.",
        "size": "Number of results per page (1-100).",
        "sortColumn": "Column to sort by. Valid values: name, status, altConf, agreementStatus, type, guest, guests, unit, units, checkin, checkout, nights.",
        "sortDirection": "Sort direction: 'asc' or 'desc'.",
        "search": "Full-text search in reservation names, guest names, and descriptions.",
        "tags": "Filter by tag IDs (comma-separated).",
        "nodeId": "Filter by node IDs (property locations).",
        "unitId": "Filter by unit IDs (specific rental units).",
        "contactId": "Filter by contact IDs (guest contacts).",
        "travelAgentId": "Filter by travel agent IDs (booking agents).",
        "campaignId": "Filter by campaign IDs (marketing campaigns).",
        "userId": "Filter by user IDs (system users).",
        "unitTypeId": "Filter by unit type IDs (property types).",
        "rateTypeId": "Filter by rate type IDs (pricing types).",
        "reservationTypeId": "Filter by reservation type IDs (booking types).",
        "bookedStart": "Filter by booking date start (ISO 8601).",
        "bookedEnd": "Filter by booking date end (ISO 8601).",
        "arrivalStart": "Filter by arrival date start (ISO 8601).",
        "arrivalEnd": "Filter by arrival date end (ISO 8601).",
        "departureStart": "Filter by departure date start (ISO 8601).",
        "departureEnd": "Filter by departure date end (ISO 8601).",
        "updatedSince": "Filter by last update date (ISO 8601).",
        "status": "Filter by reservation status. Valid statuses: Hold, Confirmed, Cancelled, Checked In, Checked Out.",
        "inHouseToday": "Filter by in-house today (0=not in house, 1=in house).",
        "groupId": "Filter by group ID.",
        "checkinOfficeId": "Filter by check-in office ID.",
        "scroll": "Elasticsearch scroll for large datasets.",
    }

    if parameter in get_supported_parameters(api_version):
        return descriptions.get(parameter, "Parameter description not available")

    return None
