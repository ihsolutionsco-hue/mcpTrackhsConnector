"""
Implementación mejorada de search_amenities siguiendo mejores prácticas de FastMCP 2.0+
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union

import httpx
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field, ValidationError, field_validator

logger = logging.getLogger(__name__)


class AmenitiesSearchParams(BaseModel):
    """Modelo Pydantic para validación de parámetros de búsqueda de amenidades."""

    # Parámetros de paginación
    page: int = Field(
        ge=1, le=10000, default=1, description="Número de página (1-based)"
    )
    size: int = Field(ge=1, le=100, default=10, description="Tamaño de página")

    # Parámetros de ordenamiento
    sortColumn: Optional[
        Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ]
    ] = Field(default=None, description="Columna para ordenar resultados")
    sortDirection: Optional[Literal["asc", "desc"]] = Field(
        default=None, description="Dirección de ordenamiento"
    )

    # Parámetros de búsqueda
    search: Optional[str] = Field(
        max_length=200, default=None, description="Búsqueda en nombre de amenidad"
    )

    # Parámetros de filtrado
    groupId: Optional[int] = Field(
        gt=0, default=None, description="Filtrar por ID de grupo"
    )
    isPublic: Optional[int] = Field(
        ge=0, le=1, default=None, description="Filtrar por amenidades públicas"
    )
    publicSearchable: Optional[int] = Field(
        ge=0,
        le=1,
        default=None,
        description="Filtrar por amenidades buscables públicamente",
    )
    isFilterable: Optional[int] = Field(
        ge=0, le=1, default=None, description="Filtrar por amenidades filtrables"
    )

    # Parámetros de tipos OTA
    homeawayType: Optional[str] = Field(
        max_length=200, default=None, description="Buscar por tipo de HomeAway"
    )
    airbnbType: Optional[str] = Field(
        max_length=200, default=None, description="Buscar por tipo de Airbnb"
    )
    tripadvisorType: Optional[str] = Field(
        max_length=200, default=None, description="Buscar por tipo de TripAdvisor"
    )
    marriottType: Optional[str] = Field(
        max_length=200, default=None, description="Buscar por tipo de Marriott"
    )

    @field_validator(
        "search", "homeawayType", "airbnbType", "tripadvisorType", "marriottType"
    )
    @classmethod
    def validate_string_fields(cls, v):
        """Validar campos de texto - convertir strings vacíos a None."""
        if v is not None and v.strip() == "":
            return None
        return v

    @field_validator("search")
    @classmethod
    def validate_search_term(cls, v):
        """Validar término de búsqueda."""
        if v is not None:
            # Limpiar y normalizar término de búsqueda
            cleaned = v.strip()
            if len(cleaned) < 2:
                raise ValueError("Término de búsqueda debe tener al menos 2 caracteres")
            return cleaned
        return v


def _build_amenities_params(params: AmenitiesSearchParams) -> Dict[str, Any]:
    """
    Construir parámetros para la API de amenidades.

    Args:
        params: Parámetros validados de búsqueda

    Returns:
        Diccionario de parámetros para la API
    """
    api_params = {"page": params.page, "size": params.size}

    # Parámetros opcionales - solo agregar si no son None
    optional_params = {
        "sortColumn": params.sortColumn,
        "sortDirection": params.sortDirection,
        "search": params.search,
        "groupId": params.groupId,
        "isPublic": params.isPublic,
        "publicSearchable": params.publicSearchable,
        "isFilterable": params.isFilterable,
        "homeawayType": params.homeawayType,
        "airbnbType": params.airbnbType,
        "tripadvisorType": params.tripadvisorType,
        "marriottType": params.marriottType,
    }

    for key, value in optional_params.items():
        if value is not None:
            api_params[key] = value

    return api_params


def _handle_amenities_error(error: Exception, context: str = "") -> ToolError:
    """
    Manejar errores específicos de la API de amenidades.

    Args:
        error: Excepción capturada
        context: Contexto adicional del error

    Returns:
        ToolError apropiado para el cliente
    """
    if isinstance(error, ValidationError):
        error_details = []
        for err in error.errors():
            field = err.get("loc", ["unknown"])[-1]
            message = err.get("msg", "Error de validación")
            error_details.append(f"{field}: {message}")

        return ToolError(f"Parámetros inválidos: {'; '.join(error_details)}")

    if isinstance(error, httpx.HTTPStatusError):
        status_code = error.response.status_code

        if status_code == 401:
            return ToolError(
                "Error de autenticación: Credenciales inválidas o expiradas"
            )
        elif status_code == 403:
            return ToolError(
                "Error de autorización: No tiene permisos para acceder a las amenidades"
            )
        elif status_code == 404:
            return ToolError(
                "Endpoint de amenidades no encontrado en el servidor TrackHS"
            )
        elif status_code == 422:
            return ToolError("Parámetros de búsqueda inválidos para la API de TrackHS")
        elif status_code >= 500:
            return ToolError(
                f"Error del servidor TrackHS ({status_code}): Servicio temporalmente no disponible"
            )
        else:
            return ToolError(
                f"Error de API TrackHS ({status_code}): {error.response.text}"
            )

    if isinstance(error, httpx.RequestError):
        return ToolError(f"Error de conexión con TrackHS: {str(error)}")

    # Error inesperado
    logger.error(f"Error inesperado en búsqueda de amenidades: {str(error)}")
    return ToolError("Error interno del servidor al buscar amenidades")


def search_amenities_improved(
    api_client,
    page: int = 1,
    size: int = 10,
    sortColumn: Optional[
        Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ]
    ] = None,
    sortDirection: Optional[Literal["asc", "desc"]] = None,
    search: Optional[str] = None,
    groupId: Optional[int] = None,
    isPublic: Optional[int] = None,
    publicSearchable: Optional[int] = None,
    isFilterable: Optional[int] = None,
    homeawayType: Optional[str] = None,
    airbnbType: Optional[str] = None,
    tripadvisorType: Optional[str] = None,
    marriottType: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Buscar amenidades/servicios disponibles en el sistema TrackHS.

    Esta función implementa la API completa de búsqueda de amenidades de TrackHS
    con validación robusta, manejo de errores mejorado y siguiendo las mejores
    prácticas de FastMCP 2.0+.

    FUNCIONALIDADES PRINCIPALES:
    - Búsqueda por texto en nombre de amenidad
    - Filtros por características (público, filtrable, buscable)
    - Filtros por grupo de amenidades
    - Búsqueda por tipos de plataformas OTA (Airbnb, HomeAway, TripAdvisor, Marriott)
    - Ordenamiento personalizable
    - Paginación flexible
    - Validación robusta de parámetros
    - Manejo de errores específico por tipo

    PARÁMETROS DE BÚSQUEDA:
    - search: Búsqueda en nombre de amenidad (mínimo 2 caracteres)
    - homeawayType, airbnbType, tripadvisorType, marriottType: Búsqueda por tipos OTA

    PARÁMETROS DE FILTRADO:
    - groupId: Filtrar por ID de grupo específico (debe ser > 0)
    - isPublic: Solo amenidades públicas (1) o privadas (0)
    - publicSearchable: Solo amenidades buscables públicamente (1) o no (0)
    - isFilterable: Solo amenidades filtrables (1) o no (0)

    PARÁMETROS DE ORDENAMIENTO:
    - sortColumn: id, order, isPublic, publicSearchable, isFilterable, createdAt
    - sortDirection: asc, desc

    EJEMPLOS DE USO:
    - search_amenities(page=1, size=10) # Primera página, 10 amenidades
    - search_amenities(search="wifi") # Buscar amenidades con "wifi"
    - search_amenities(isPublic=1, isFilterable=1) # Solo públicas y filtrables
    - search_amenities(airbnbType="ac") # Buscar por tipo de Airbnb
    - search_amenities(sortColumn="name", sortDirection="asc") # Ordenadas por nombre
    - search_amenities(groupId=2) # Solo amenidades del grupo 2
    - search_amenities(tripadvisorType="pool%") # Buscar por tipo de TripAdvisor con wildcard

    Returns:
        Dict[str, Any]: Respuesta de la API con amenidades encontradas

    Raises:
        ToolError: Si hay error de validación, autenticación, autorización o conexión
    """
    if api_client is None:
        raise ToolError(
            "Cliente API no disponible. Verifique las credenciales de TrackHS."
        )

    # Validar parámetros usando Pydantic
    try:
        params = AmenitiesSearchParams(
            page=page,
            size=size,
            sortColumn=sortColumn,
            sortDirection=sortDirection,
            search=search,
            groupId=groupId,
            isPublic=isPublic,
            publicSearchable=publicSearchable,
            isFilterable=isFilterable,
            homeawayType=homeawayType,
            airbnbType=airbnbType,
            tripadvisorType=tripadvisorType,
            marriottType=marriottType,
        )
    except ValidationError as e:
        raise _handle_amenities_error(e, "validación de parámetros")

    logger.info(f"Buscando amenidades: página {params.page}, tamaño {params.size}")

    try:
        # Construir parámetros para la API
        api_params = _build_amenities_params(params)

        # Realizar llamada a la API
        result = api_client.get("api/pms/units/amenities", api_params)

        # Validar respuesta
        if not isinstance(result, dict):
            raise ToolError("Respuesta inesperada de la API de TrackHS")

        total_items = result.get("total_items", 0)
        logger.info(f"Encontradas {total_items} amenidades")

        return result

    except ToolError:
        # Re-lanzar ToolError tal como están
        raise
    except Exception as e:
        # Manejar otros errores
        raise _handle_amenities_error(e, "llamada a la API")


# Ejemplo de uso con FastMCP
def create_amenities_tool(mcp, api_client):
    """
    Crear herramienta de amenidades con anotaciones mejoradas.

    Args:
        mcp: Instancia de FastMCP
        api_client: Cliente API de TrackHS
    """

    @mcp.tool(
        output_schema=AMENITIES_OUTPUT_SCHEMA,  # Definido en schemas.py
        annotations={
            "title": "Buscar Amenidades de TrackHS",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    def search_amenities(
        page: int = 1,
        size: int = 10,
        sortColumn: Optional[
            Literal[
                "id",
                "order",
                "isPublic",
                "publicSearchable",
                "isFilterable",
                "createdAt",
            ]
        ] = None,
        sortDirection: Optional[Literal["asc", "desc"]] = None,
        search: Optional[str] = None,
        groupId: Optional[int] = None,
        isPublic: Optional[int] = None,
        publicSearchable: Optional[int] = None,
        isFilterable: Optional[int] = None,
        homeawayType: Optional[str] = None,
        airbnbType: Optional[str] = None,
        tripadvisorType: Optional[str] = None,
        marriottType: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Buscar amenidades/servicios disponibles en el sistema TrackHS.

        [Documentación detallada...]
        """
        return search_amenities_improved(
            api_client=api_client,
            page=page,
            size=size,
            sortColumn=sortColumn,
            sortDirection=sortDirection,
            search=search,
            groupId=groupId,
            isPublic=isPublic,
            publicSearchable=publicSearchable,
            isFilterable=isFilterable,
            homeawayType=homeawayType,
            airbnbType=airbnbType,
            tripadvisorType=tripadvisorType,
            marriottType=marriottType,
        )

    return search_amenities
