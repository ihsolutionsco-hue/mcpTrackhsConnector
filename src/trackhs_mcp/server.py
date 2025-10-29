"""
TrackHS MCP Server - Versión Simple
Servidor minimalista siguiendo las mejores prácticas de FastMCP
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

from .amenities_error_handler import AmenitiesErrorHandler
from .amenities_logging import amenities_logger
from .amenities_models import AmenitiesSearchParams
from .amenities_service import AmenitiesService
from .client import TrackHSClient
from .config import get_settings, validate_configuration
from .middleware import validate_and_coerce_tool_input
from .schemas import (
    AMENITIES_OUTPUT_SCHEMA,
    FOLIO_DETAIL_OUTPUT_SCHEMA,
    RESERVATION_DETAIL_OUTPUT_SCHEMA,
    RESERVATION_SEARCH_OUTPUT_SCHEMA,
    UNIT_SEARCH_OUTPUT_SCHEMA,
    WORK_ORDER_DETAIL_OUTPUT_SCHEMA,
)
from .utils import build_units_search_params, clean_unit_data

# Configuración centralizada
settings = get_settings()


# Función de validación para parámetros numéricos flexibles
def validate_flexible_int(v):
    """Valida y convierte parámetros que pueden ser int o str"""
    if v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"No se puede convertir '{v}' a entero")
    raise ValueError(f"Tipo no soportado: {type(v)}")


# Alias para usar en las anotaciones
FlexibleIntType = Union[int, str, None]

# Validar configuración al inicio
if not validate_configuration():
    sys.exit(1)

# Configuración de logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Inicializar cliente API
api_client = None
if settings.trackhs_username and settings.trackhs_password:
    api_client = TrackHSClient(
        base_url=settings.trackhs_api_url,
        username=settings.trackhs_username,
        password=settings.trackhs_password,
        timeout=settings.request_timeout,
    )
    logger.info("Cliente API TrackHS inicializado")
else:
    logger.warning("Credenciales no configuradas - servidor iniciará sin funcionalidad")


# Server Lifespan
@asynccontextmanager
async def lifespan(server):
    """Maneja el ciclo de vida del servidor MCP."""
    logger.info("TrackHS MCP Server iniciando...")
    logger.info(f"Base URL: {settings.trackhs_api_url}")
    logger.info(
        f"Username: {'Configurado' if settings.trackhs_username else 'No configurado'}"
    )

    # Verificar conexión API
    if api_client:
        try:
            # Test simple de conectividad
            api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
            logger.info("API TrackHS conectada")
        except Exception as e:
            logger.error(f"API TrackHS no disponible: {e}")
    else:
        logger.warning("Cliente API no disponible")

    logger.info("Servidor listo")
    yield

    # Limpieza
    logger.info("TrackHS MCP Server cerrando...")
    if api_client:
        api_client.close()
    logger.info("Servidor cerrado")


# Crear servidor FastMCP
mcp = FastMCP(
    name="TrackHS API",
    instructions="""
    Servidor MCP para interactuar con la API de TrackHS.

    Proporciona herramientas para:
    - Buscar y consultar reservas
    - Gestionar unidades de alojamiento
    - Consultar amenidades disponibles
    - Obtener información financiera (folios)
    - Crear órdenes de trabajo (mantenimiento y housekeeping)

    Todas las herramientas incluyen validación robusta y documentación completa.
    """,
    strict_input_validation=False,  # CRÍTICO: Permite coerción de tipos: "10" → 10
    mask_error_details=True,
    lifespan=lifespan,
)

# Verificación de configuración crítica
logger.info("🔧 CONFIGURACIÓN FASTMCP VERIFICADA:")
logger.info(f"   ✅ strict_input_validation: {mcp.strict_input_validation}")
logger.info(f"   ✅ force_input_coercion: {settings.force_input_coercion}")

# Verificar atributos opcionales
try:
    logger.info(f"   ✅ mask_error_details: {mcp.mask_error_details}")
except AttributeError:
    logger.info("   ⚠️ mask_error_details: No disponible en esta versión")

# Verificación adicional de que la configuración se aplicó
if mcp.strict_input_validation:
    logger.error("❌ ERROR CRÍTICO: strict_input_validation está en True!")
    logger.error("   Esto causará fallos en la validación de tipos de parámetros")
    logger.error("   Los parámetros numéricos enviados como strings fallarán")
    logger.error("   Se activará middleware de coerción como respaldo")
else:
    logger.info("✅ CONFIGURACIÓN CORRECTA: strict_input_validation=False")
    logger.info(
        "   Los parámetros numéricos como strings serán convertidos automáticamente"
    )

# Verificación de configuración de coerción
if settings.force_input_coercion:
    logger.info("✅ MIDDLEWARE DE COERCIÓN ACTIVADO")
    logger.info("   Garantiza conversión de tipos incluso si FastMCP falla")
else:
    logger.warning("⚠️ MIDDLEWARE DE COERCIÓN DESACTIVADO")
    logger.warning("   Depende completamente de la configuración de FastMCP")

logger.info("Servidor configurado correctamente")


# =============================================================================
# HERRAMIENTAS MCP - ESTILO FASTMCP IDIOMÁTICO
# =============================================================================


@mcp.tool(output_schema=RESERVATION_SEARCH_OUTPUT_SCHEMA)
def search_reservations(
    page: Annotated[
        int, Field(ge=1, le=10000, description="Número de página (1-based)")
    ] = 1,
    size: Annotated[
        int, Field(ge=1, le=100, description="Tamaño de página (1-100)")
    ] = 10,
    search: Annotated[
        Optional[str], Field(max_length=200, description="Búsqueda de texto completo")
    ] = None,
    arrival_start: Annotated[
        Optional[str],
        Field(
            description="Fecha de llegada inicio (YYYY-MM-DD)",
        ),
    ] = None,
    arrival_end: Annotated[
        Optional[str],
        Field(
            description="Fecha de llegada fin (YYYY-MM-DD)",
        ),
    ] = None,
    status: Annotated[
        Optional[str], Field(max_length=50, description="Estado de reserva")
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar reservas en TrackHS con filtros avanzados.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    # Construir parámetros
    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if arrival_start and arrival_start != "null" and arrival_start.strip():
        # Validar formato de fecha
        import re

        if re.match(r"^\d{4}-\d{2}-\d{2}$", arrival_start):
            params["arrivalStart"] = arrival_start
        else:
            logger.warning(
                f"Formato de fecha inválido para arrival_start: {arrival_start}"
            )
    if arrival_end and arrival_end != "null" and arrival_end.strip():
        # Validar formato de fecha
        import re

        if re.match(r"^\d{4}-\d{2}-\d{2}$", arrival_end):
            params["arrivalEnd"] = arrival_end
        else:
            logger.warning(f"Formato de fecha inválido para arrival_end: {arrival_end}")
    if status:
        params["status"] = status

    logger.info(f"Buscando reservas: página {page}, tamaño {size}")

    try:
        result = api_client.get("api/pms/reservations", params)
        total_items = result.get("total_items", 0)
        logger.info(f"Encontradas {total_items} reservas")
        return result
    except Exception as e:
        logger.error(f"Error buscando reservas: {str(e)}")
        raise ToolError(f"Error buscando reservas: {str(e)}")


@mcp.tool(output_schema=RESERVATION_DETAIL_OUTPUT_SCHEMA)
def get_reservation(
    reservation_id: Annotated[
        int, Field(gt=0, description="ID único de la reserva en TrackHS")
    ],
) -> Dict[str, Any]:
    """
    Obtener detalles completos de una reserva específica por ID.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    logger.info(f"Obteniendo reserva {reservation_id}")

    try:
        result = api_client.get(f"api/pms/reservations/{reservation_id}")
        logger.info(f"Reserva {reservation_id} obtenida exitosamente")
        return result
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            raise ToolError(f"Reserva {reservation_id} no encontrada en TrackHS")
        logger.error(f"Error obteniendo reserva {reservation_id}: {str(e)}")
        raise ToolError(f"Error obteniendo reserva: {str(e)}")


@mcp.tool(output_schema=UNIT_SEARCH_OUTPUT_SCHEMA)
def search_units(
    # Parámetros de paginación
    page: Annotated[
        Any,
        Field(
            description="Número de página (1-based). Límite máximo: 10k total results",
        ),
    ] = 1,
    size: Annotated[
        Any,
        Field(
            description="Tamaño de página (1-100). Límite: 10k total results",
        ),
    ] = 10,
    # Parámetros de ordenamiento
    sort_column: Annotated[
        Optional[Literal["id", "name", "nodeName", "unitTypeName"]],
        Field(description="Columna para ordenar resultados. Default: name"),
    ] = None,
    sort_direction: Annotated[
        Optional[Literal["asc", "desc"]],
        Field(description="Dirección de ordenamiento. Default: asc"),
    ] = None,
    # Parámetros de búsqueda de texto
    search: Annotated[
        Optional[str],
        Field(
            max_length=200, description="Búsqueda de texto en nombre o descripciones"
        ),
    ] = None,
    term: Annotated[
        Optional[str],
        Field(max_length=200, description="Búsqueda de texto en término específico"),
    ] = None,
    unit_code: Annotated[
        Optional[str],
        Field(
            max_length=100,
            description="Búsqueda en código de unidad (exacta o con % para wildcard)",
        ),
    ] = None,
    short_name: Annotated[
        Optional[str],
        Field(
            max_length=100,
            description="Búsqueda en nombre corto (exacta o con % para wildcard)",
        ),
    ] = None,
    # Parámetros de filtros por ID
    node_id: Annotated[
        Optional[Union[int, List[int]]],
        Field(description="ID(s) de nodo - unidades descendientes"),
    ] = None,
    amenity_id: Annotated[
        Optional[Union[int, List[int]]],
        Field(description="ID(s) de amenidad - unidades que tienen estas amenidades"),
    ] = None,
    unit_type_id: Annotated[
        Optional[Union[int, List[int]]], Field(description="ID(s) de tipo de unidad")
    ] = None,
    owner_id: Annotated[
        Optional[Union[int, List[int]]], Field(description="ID(s) del propietario")
    ] = None,
    company_id: Annotated[
        Optional[Union[int, List[int]]], Field(description="ID(s) de la empresa")
    ] = None,
    channel_id: Annotated[
        Optional[Union[int, List[int]]], Field(description="ID(s) del canal activo")
    ] = None,
    lodging_type_id: Annotated[
        Optional[Union[int, List[int]]],
        Field(description="ID(s) del tipo de alojamiento"),
    ] = None,
    bed_type_id: Annotated[
        Optional[Union[int, List[int]]], Field(description="ID(s) del tipo de cama")
    ] = None,
    amenity_all: Annotated[
        Optional[List[int]],
        Field(description="Filtrar unidades que tengan TODAS estas amenidades"),
    ] = None,
    unit_ids: Annotated[
        Optional[List[int]],
        Field(description="Filtrar por IDs específicos de unidades"),
    ] = None,
    # Parámetros de dormitorios
    bedrooms: Annotated[
        Optional[Any], Field(description="Número exacto de dormitorios")
    ] = None,
    min_bedrooms: Annotated[
        Optional[Any], Field(description="Número mínimo de dormitorios")
    ] = None,
    max_bedrooms: Annotated[
        Optional[Any], Field(description="Número máximo de dormitorios")
    ] = None,
    # Parámetros de baños
    bathrooms: Annotated[
        Optional[Any], Field(description="Número exacto de baños")
    ] = None,
    min_bathrooms: Annotated[
        Optional[Any], Field(description="Número mínimo de baños")
    ] = None,
    max_bathrooms: Annotated[
        Optional[Any], Field(description="Número máximo de baños")
    ] = None,
    # Parámetros de capacidad
    occupancy: Annotated[Optional[Any], Field(description="Capacidad exacta")] = None,
    min_occupancy: Annotated[
        Optional[Any], Field(description="Capacidad mínima")
    ] = None,
    max_occupancy: Annotated[
        Optional[Any], Field(description="Capacidad máxima")
    ] = None,
    # Parámetros de fechas
    arrival: Annotated[
        Optional[str],
        Field(
            description="Fecha de llegada (YYYY-MM-DD) para verificar disponibilidad",
        ),
    ] = None,
    departure: Annotated[
        Optional[str],
        Field(
            description="Fecha de salida (YYYY-MM-DD) para verificar disponibilidad",
        ),
    ] = None,
    content_updated_since: Annotated[
        Optional[str],
        Field(description="Fecha ISO 8601 - unidades con cambios desde esta fecha"),
    ] = None,
    # Parámetros de estado y características
    is_active: Annotated[
        Optional[Any],
        Field(description="Unidades activas (1) o inactivas (0)"),
    ] = None,
    is_bookable: Annotated[
        Optional[Any],
        Field(description="Unidades reservables (1) o no (0)"),
    ] = None,
    pets_friendly: Annotated[
        Optional[Any],
        Field(description="Unidades pet-friendly (1) o no (0)"),
    ] = None,
    unit_status: Annotated[
        Optional[Literal["clean", "dirty", "occupied", "inspection", "inprogress"]],
        Field(description="Estado de la unidad"),
    ] = None,
    # Parámetros de funcionalidad adicional
    computed: Annotated[
        Optional[FlexibleIntType],
        Field(
            ge=0,
            le=1,
            description="Incluir valores computados adicionales (1) o no (0)",
        ),
    ] = None,
    inherited: Annotated[
        Optional[FlexibleIntType],
        Field(ge=0, le=1, description="Incluir atributos heredados (1) o no (0)"),
    ] = None,
    limited: Annotated[
        Optional[FlexibleIntType],
        Field(
            ge=0, le=1, description="Retornar atributos limitados (1) o completos (0)"
        ),
    ] = None,
    include_descriptions: Annotated[
        Optional[FlexibleIntType],
        Field(ge=0, le=1, description="Incluir descripciones de unidades (1) o no (0)"),
    ] = None,
    # Parámetros de filtros adicionales
    calendar_id: Annotated[
        Optional[FlexibleIntType], Field(gt=0, description="ID del grupo de calendario")
    ] = None,
    role_id: Annotated[
        Optional[FlexibleIntType], Field(gt=0, description="ID del rol específico")
    ] = None,
    promo_code_id: Annotated[
        Optional[FlexibleIntType],
        Field(gt=0, description="ID del código promocional válido"),
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar unidades de alojamiento disponibles en TrackHS con filtros avanzados.

    Esta herramienta implementa la API completa de búsqueda de unidades de TrackHS
    con todos los parámetros disponibles según la documentación oficial.

    FUNCIONALIDADES PRINCIPALES:
    - Búsqueda por características físicas (dormitorios, baños, capacidad)
    - Filtros por estado (activa, reservable, pet-friendly, estado de limpieza)
    - Búsqueda de texto (nombre, descripción, código, término)
    - Filtros por fechas de disponibilidad (arrival/departure)
    - Filtros por IDs (nodo, amenidad, tipo de unidad, propietario, etc.)
    - Ordenamiento personalizable
    - Paginación flexible

    PARÁMETROS DE BÚSQUEDA DE TEXTO:
    - search: Búsqueda en nombre o descripciones
    - term: Búsqueda en término específico
    - unit_code: Búsqueda exacta en código (con % para wildcard)
    - short_name: Búsqueda exacta en nombre corto (con % para wildcard)

    PARÁMETROS DE CAPACIDAD:
    - bedrooms/min_bedrooms/max_bedrooms: Filtros de dormitorios
    - bathrooms/min_bathrooms/max_bathrooms: Filtros de baños
    - occupancy/min_occupancy/max_occupancy: Filtros de capacidad

    PARÁMETROS DE DISPONIBILIDAD:
    - arrival/departure: Verificar disponibilidad en fechas específicas
    - is_bookable: Solo unidades disponibles para reservar
    - is_active: Solo unidades activas

    PARÁMETROS DE CARACTERÍSTICAS:
    - pets_friendly: Unidades que permiten mascotas
    - unit_status: Estado de limpieza (clean, dirty, occupied, etc.)
    - amenity_id: Unidades con amenidades específicas
    - amenity_all: Unidades con TODAS las amenidades especificadas

    PARÁMETROS DE ORDENAMIENTO:
    - sort_column: id, name, nodeName, unitTypeName
    - sort_direction: asc, desc

    EJEMPLOS DE USO:
    - search_units(page=1, size=10) # Primera página, 10 unidades
    - search_units(bedrooms=2, bathrooms=1) # Apartamentos 2D/1B
    - search_units(is_active=1, is_bookable=1) # Unidades activas y disponibles
    - search_units(search="penthouse") # Buscar por nombre
    - search_units(arrival="2024-01-15", departure="2024-01-20") # Disponibles en fechas
    - search_units(amenity_id=[1,2,3]) # Con amenidades específicas
    - search_units(pets_friendly=1, min_bedrooms=2) # Pet-friendly con 2+ dormitorios
    - search_units(unit_status="clean", is_bookable=1) # Limpias y disponibles
    - search_units(sort_column="name", sort_direction="asc") # Ordenadas por nombre
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    # Convertir parámetros Any a enteros usando nuestra función de validación
    page = validate_flexible_int(page) if page is not None else 1
    size = validate_flexible_int(size) if size is not None else 10
    bedrooms = validate_flexible_int(bedrooms) if bedrooms is not None else None
    min_bedrooms = (
        validate_flexible_int(min_bedrooms) if min_bedrooms is not None else None
    )
    max_bedrooms = (
        validate_flexible_int(max_bedrooms) if max_bedrooms is not None else None
    )
    bathrooms = validate_flexible_int(bathrooms) if bathrooms is not None else None
    min_bathrooms = (
        validate_flexible_int(min_bathrooms) if min_bathrooms is not None else None
    )
    max_bathrooms = (
        validate_flexible_int(max_bathrooms) if max_bathrooms is not None else None
    )
    occupancy = validate_flexible_int(occupancy) if occupancy is not None else None
    min_occupancy = (
        validate_flexible_int(min_occupancy) if min_occupancy is not None else None
    )
    max_occupancy = (
        validate_flexible_int(max_occupancy) if max_occupancy is not None else None
    )
    is_active = validate_flexible_int(is_active) if is_active is not None else None
    is_bookable = (
        validate_flexible_int(is_bookable) if is_bookable is not None else None
    )
    pets_friendly = (
        validate_flexible_int(pets_friendly) if pets_friendly is not None else None
    )

    # Aplicar middleware de coerción de tipos como respaldo adicional
    params_dict = {
        "page": page,
        "size": size,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        "search": search,
        "term": term,
        "unit_code": unit_code,
        "short_name": short_name,
        "node_id": node_id,
        "amenity_id": amenity_id,
        "unit_type_id": unit_type_id,
        "bedrooms": bedrooms,
        "min_bedrooms": min_bedrooms,
        "max_bedrooms": max_bedrooms,
        "bathrooms": bathrooms,
        "min_bathrooms": min_bathrooms,
        "max_bathrooms": max_bathrooms,
        "occupancy": occupancy,
        "min_occupancy": min_occupancy,
        "max_occupancy": max_occupancy,
        "arrival": arrival,
        "departure": departure,
        "content_updated_since": content_updated_since,
        "is_active": is_active,
        "is_bookable": is_bookable,
        "pets_friendly": pets_friendly,
        "unit_status": unit_status,
        "computed": computed,
        "inherited": inherited,
        "limited": limited,
        "include_descriptions": include_descriptions,
        "calendar_id": calendar_id,
        "role_id": role_id,
        "promo_code_id": promo_code_id,
        "owner_id": owner_id,
        "company_id": company_id,
        "channel_id": channel_id,
        "lodging_type_id": lodging_type_id,
        "bed_type_id": bed_type_id,
        "amenity_all": amenity_all,
        "unit_ids": unit_ids,
    }

    # Aplicar coerción de tipos
    coerced_params = validate_and_coerce_tool_input("search_units", params_dict)

    # Extraer parámetros convertidos
    page = coerced_params.get("page", page)
    size = coerced_params.get("size", size)
    sort_column = coerced_params.get("sort_column", sort_column)
    sort_direction = coerced_params.get("sort_direction", sort_direction)
    search = coerced_params.get("search", search)
    term = coerced_params.get("term", term)
    unit_code = coerced_params.get("unit_code", unit_code)
    short_name = coerced_params.get("short_name", short_name)
    node_id = coerced_params.get("node_id", node_id)
    amenity_id = coerced_params.get("amenity_id", amenity_id)
    unit_type_id = coerced_params.get("unit_type_id", unit_type_id)
    bedrooms = coerced_params.get("bedrooms", bedrooms)
    min_bedrooms = coerced_params.get("min_bedrooms", min_bedrooms)
    max_bedrooms = coerced_params.get("max_bedrooms", max_bedrooms)
    bathrooms = coerced_params.get("bathrooms", bathrooms)
    min_bathrooms = coerced_params.get("min_bathrooms", min_bathrooms)
    max_bathrooms = coerced_params.get("max_bathrooms", max_bathrooms)
    occupancy = coerced_params.get("occupancy", occupancy)
    min_occupancy = coerced_params.get("min_occupancy", min_occupancy)
    max_occupancy = coerced_params.get("max_occupancy", max_occupancy)
    arrival = coerced_params.get("arrival", arrival)
    departure = coerced_params.get("departure", departure)
    content_updated_since = coerced_params.get(
        "content_updated_since", content_updated_since
    )
    is_active = coerced_params.get("is_active", is_active)
    is_bookable = coerced_params.get("is_bookable", is_bookable)
    pets_friendly = coerced_params.get("pets_friendly", pets_friendly)
    unit_status = coerced_params.get("unit_status", unit_status)
    computed = coerced_params.get("computed", computed)
    inherited = coerced_params.get("inherited", inherited)
    limited = coerced_params.get("limited", limited)
    include_descriptions = coerced_params.get(
        "include_descriptions", include_descriptions
    )
    calendar_id = coerced_params.get("calendar_id", calendar_id)
    role_id = coerced_params.get("role_id", role_id)
    promo_code_id = coerced_params.get("promo_code_id", promo_code_id)
    owner_id = coerced_params.get("owner_id", owner_id)
    company_id = coerced_params.get("company_id", company_id)
    channel_id = coerced_params.get("channel_id", channel_id)
    lodging_type_id = coerced_params.get("lodging_type_id", lodging_type_id)
    bed_type_id = coerced_params.get("bed_type_id", bed_type_id)
    amenity_all = coerced_params.get("amenity_all", amenity_all)
    unit_ids = coerced_params.get("unit_ids", unit_ids)

    logger.info(f"Buscando unidades: página {page}, tamaño {size}")

    try:
        # Construir parámetros usando helper con todos los nuevos parámetros
        api_params = build_units_search_params(
            # Parámetros de paginación
            page=page,
            size=size,
            # Parámetros de ordenamiento
            sort_column=sort_column,
            sort_direction=sort_direction,
            # Parámetros de búsqueda de texto
            search=search,
            term=term,
            unit_code=unit_code,
            short_name=short_name,
            # Parámetros de filtros por ID
            node_id=node_id,
            amenity_id=amenity_id,
            unit_type_id=unit_type_id,
            owner_id=owner_id,
            company_id=company_id,
            channel_id=channel_id,
            lodging_type_id=lodging_type_id,
            bed_type_id=bed_type_id,
            amenity_all=amenity_all,
            unit_ids=unit_ids,
            # Parámetros de dormitorios
            bedrooms=bedrooms,
            min_bedrooms=min_bedrooms,
            max_bedrooms=max_bedrooms,
            # Parámetros de baños
            bathrooms=bathrooms,
            min_bathrooms=min_bathrooms,
            max_bathrooms=max_bathrooms,
            # Parámetros de capacidad
            occupancy=occupancy,
            min_occupancy=min_occupancy,
            max_occupancy=max_occupancy,
            # Parámetros de fechas
            arrival=arrival,
            departure=departure,
            content_updated_since=content_updated_since,
            # Parámetros de estado y características
            is_active=is_active,
            is_bookable=is_bookable,
            pets_friendly=pets_friendly,
            unit_status=unit_status,
            # Parámetros de funcionalidad adicional
            computed=computed,
            inherited=inherited,
            limited=limited,
            include_descriptions=include_descriptions,
            # Parámetros de filtros adicionales
            calendar_id=calendar_id,
            role_id=role_id,
            promo_code_id=promo_code_id,
        )

        # Realizar búsqueda
        result = api_client.get("api/pms/units", api_params)

        # Limpiar datos de respuesta
        if "_embedded" in result and "units" in result["_embedded"]:
            original_units = result["_embedded"]["units"]
            cleaned_units = []

            for unit in original_units:
                try:
                    cleaned_unit = clean_unit_data(unit)
                    cleaned_units.append(cleaned_unit)
                except Exception as e:
                    logger.warning(f"Error limpiando unidad: {e}")
                    cleaned_units.append(unit)  # Mantener original si falla limpieza

            result["_embedded"]["units"] = cleaned_units

        total_items = result.get("total_items", 0)
        logger.info(f"Encontradas {total_items} unidades")
        return result
    except Exception as e:
        logger.error(f"Error buscando unidades: {str(e)}")
        raise ToolError(f"Error buscando unidades: {str(e)}")


@mcp.tool(
    output_schema=AMENITIES_OUTPUT_SCHEMA,
    annotations={
        "title": "Buscar Amenidades de TrackHS",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def search_amenities(
    # Parámetros de paginación
    page: Annotated[
        int, Field(ge=1, le=10000, description="Número de página (1-based)")
    ] = 1,
    size: Annotated[int, Field(ge=1, le=100, description="Tamaño de página")] = 10,
    # Parámetros de ordenamiento (usando camelCase como en la API)
    sortColumn: Annotated[
        Optional[
            Literal[
                "id",
                "order",
                "isPublic",
                "publicSearchable",
                "isFilterable",
                "createdAt",
            ]
        ],
        Field(description="Columna para ordenar resultados. Default: order"),
    ] = None,
    sortDirection: Annotated[
        Optional[Literal["asc", "desc"]],
        Field(description="Dirección de ordenamiento. Default: asc"),
    ] = None,
    # Parámetros de búsqueda
    search: Annotated[
        Optional[str],
        Field(max_length=200, description="Búsqueda en nombre de amenidad"),
    ] = None,
    # Parámetros de filtrado
    groupId: Annotated[
        Optional[int],
        Field(description="Filtrar por ID de grupo"),
    ] = None,
    isPublic: Annotated[
        Optional[Any],
        Field(description="Filtrar por amenidades públicas (1) o privadas (0)"),
    ] = None,
    publicSearchable: Annotated[
        Optional[Any],
        Field(description="Filtrar por amenidades buscables públicamente (1) o no (0)"),
    ] = None,
    isFilterable: Annotated[
        Optional[Any],
        Field(description="Filtrar por amenidades filtrables (1) o no (0)"),
    ] = None,
    # Parámetros de tipos de plataformas OTA
    homeawayType: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Buscar por tipo de HomeAway (soporta % para wildcard)",
        ),
    ] = None,
    airbnbType: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Buscar por tipo de Airbnb (soporta % para wildcard)",
        ),
    ] = None,
    tripadvisorType: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Buscar por tipo de TripAdvisor (soporta % para wildcard)",
        ),
    ] = None,
    marriottType: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Buscar por tipo de Marriott (soporta % para wildcard)",
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar amenidades/servicios disponibles en el sistema TrackHS.

    Esta herramienta implementa la API completa de búsqueda de amenidades de TrackHS
    con validación robusta, manejo de errores mejorado, logging estructurado y
    siguiendo las mejores prácticas de FastMCP 2.0+.

    FUNCIONALIDADES PRINCIPALES:
    - Búsqueda por texto en nombre de amenidad
    - Filtros por características (público, filtrable, buscable)
    - Filtros por grupo de amenidades
    - Búsqueda por tipos de plataformas OTA (Airbnb, HomeAway, TripAdvisor, Marriott)
    - Ordenamiento personalizable
    - Paginación flexible
    - Validación robusta de parámetros
    - Manejo de errores específico por tipo
    - Logging estructurado para observabilidad
    - Arquitectura modular y mantenible

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
    - search_amenities(sortColumn="id", sortDirection="asc") # Ordenadas por ID
    - search_amenities(groupId=2) # Solo amenidades del grupo 2
    - search_amenities(tripadvisorType="pool%") # Buscar por tipo de TripAdvisor con wildcard

    Returns:
        Dict[str, Any]: Respuesta de la API con amenidades encontradas

    Raises:
        ToolError: Si hay error de validación, autenticación, autorización o conexión
    """
    # Convertir y validar parámetros de filtrado booleanos
    if isPublic is not None:
        if isinstance(isPublic, str):
            isPublic = int(isPublic)
        if isPublic not in [0, 1]:
            raise ToolError("isPublic debe ser 0 o 1")

    if publicSearchable is not None:
        if isinstance(publicSearchable, str):
            publicSearchable = int(publicSearchable)
        if publicSearchable not in [0, 1]:
            raise ToolError("publicSearchable debe ser 0 o 1")

    if isFilterable is not None:
        if isinstance(isFilterable, str):
            isFilterable = int(isFilterable)
        if isFilterable not in [0, 1]:
            raise ToolError("isFilterable debe ser 0 o 1")

    # Inicializar servicio de amenidades
    amenities_service = AmenitiesService(api_client)

    # Log del inicio de la operación
    amenities_logger.log_search_start(
        page=page,
        size=size,
        search_params={
            "search": search,
            "groupId": groupId,
            "isPublic": isPublic,
            "sortColumn": sortColumn,
            "sortDirection": sortDirection,
        },
    )

    try:
        # Delegar la búsqueda al servicio
        result = amenities_service.search_amenities(
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

        # Log del éxito de la operación
        total_items = result.get("total_items", 0)
        amenities_logger.log_search_success(
            total_items=total_items, page=page, size=size
        )

        return result

    except Exception as e:
        # El servicio ya maneja el logging de errores
        raise


@mcp.tool(output_schema=FOLIO_DETAIL_OUTPUT_SCHEMA)
def get_folio(
    reservation_id: Annotated[
        int,
        Field(gt=0, description="ID de la reserva para obtener su folio financiero"),
    ],
) -> Dict[str, Any]:
    """
    Obtener el folio financiero completo de una reserva.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    logger.info(f"Obteniendo folio de reserva {reservation_id}")

    try:
        result = api_client.get(f"api/pms/reservations/{reservation_id}/folio")
        logger.info(f"Folio de reserva {reservation_id} obtenido exitosamente")
        return result
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            logger.warning(f"Folio de reserva {reservation_id} no encontrado")
            return {
                "error": "Folio no encontrado",
                "message": f"El folio financiero para la reserva {reservation_id} no está disponible.",
                "reservation_id": reservation_id,
                "status": "not_found",
            }

        logger.error(f"Error obteniendo folio de reserva {reservation_id}: {str(e)}")
        raise ToolError(f"Error obteniendo folio: {str(e)}")


@mcp.tool(output_schema=WORK_ORDER_DETAIL_OUTPUT_SCHEMA)
def create_maintenance_work_order(
    unit_id: Annotated[
        int, Field(gt=0, description="ID de la unidad que requiere mantenimiento")
    ],
    summary: Annotated[
        str,
        Field(min_length=1, max_length=500, description="Resumen breve del problema"),
    ],
    description: Annotated[
        str, Field(min_length=1, max_length=5000, description="Descripción detallada")
    ],
    priority: Annotated[
        Literal[1, 3, 5], Field(description="Prioridad: 1=Baja, 3=Media, 5=Alta")
    ] = 3,
    estimated_cost: Annotated[
        Optional[float], Field(ge=0, description="Costo estimado")
    ] = None,
    estimated_time: Annotated[
        Optional[int], Field(ge=0, description="Tiempo estimado en minutos")
    ] = None,
    date_received: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha de recepción (YYYY-MM-DD)",
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    Crear una orden de trabajo de mantenimiento para una unidad.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    logger.info(f"Creando orden de mantenimiento para unidad {unit_id}")

    try:
        # Construir datos para la API
        work_order_data = {
            "unitId": unit_id,
            "summary": summary,
            "description": description,
            "priority": priority,
            "status": "pending",
            "dateReceived": date_received or datetime.now().strftime("%Y-%m-%d"),
        }

        if estimated_cost is not None:
            work_order_data["estimatedCost"] = estimated_cost
        if estimated_time is not None:
            work_order_data["estimatedTime"] = estimated_time

        result = api_client.post("api/pms/work-orders/maintenance", work_order_data)
        logger.info(f"Orden de mantenimiento creada: ID {result.get('id', 'unknown')}")
        return result
    except Exception as e:
        logger.error(f"Error creando orden de mantenimiento: {str(e)}")
        raise ToolError(f"Error creando orden de mantenimiento: {str(e)}")


@mcp.tool(output_schema=WORK_ORDER_DETAIL_OUTPUT_SCHEMA)
def create_housekeeping_work_order(
    unit_id: Annotated[
        int, Field(gt=0, description="ID de la unidad que requiere limpieza")
    ],
    scheduled_at: Annotated[
        str,
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha programada (YYYY-MM-DD)"
        ),
    ],
    is_inspection: Annotated[
        bool, Field(description="True si es inspección, False si es limpieza")
    ] = False,
    clean_type_id: Annotated[
        Optional[int], Field(gt=0, description="ID del tipo de limpieza")
    ] = None,
    comments: Annotated[
        Optional[str], Field(max_length=2000, description="Comentarios especiales")
    ] = None,
    cost: Annotated[
        Optional[float], Field(ge=0, description="Costo del servicio")
    ] = None,
) -> Dict[str, Any]:
    """
    Crear una orden de trabajo de housekeeping (limpieza) para una unidad.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    # Validar clean_type_id si no es inspección
    if not is_inspection and clean_type_id is None:
        raise ToolError("clean_type_id es requerido cuando is_inspection=False")

    logger.info(f"Creando orden de housekeeping para unidad {unit_id}")

    try:
        # Construir datos para la API
        work_order_data = {
            "unitId": unit_id,
            "scheduledAt": scheduled_at,
            "status": "pending",
            "isInspection": is_inspection,
        }

        if clean_type_id is not None:
            work_order_data["cleanTypeId"] = clean_type_id
        if comments is not None:
            work_order_data["comments"] = comments
        if cost is not None:
            work_order_data["cost"] = cost

        result = api_client.post("api/pms/work-orders/housekeeping", work_order_data)
        logger.info(f"Orden de housekeeping creada: ID {result.get('id', 'unknown')}")
        return result
    except Exception as e:
        logger.error(f"Error creando orden de housekeeping: {str(e)}")
        raise ToolError(f"Error creando orden de housekeeping: {str(e)}")


# =============================================================================
# RESOURCES (HEALTH CHECK SIMPLIFICADO)
# =============================================================================


@mcp.resource("https://trackhs-mcp.local/health")
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint para monitoreo del servidor.
    """
    try:
        # Verificar conexión con API TrackHS
        api_status = "healthy"
        api_response_time = None

        if api_client:
            try:
                import time

                start_time = time.time()
                api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
                api_response_time = round((time.time() - start_time) * 1000, 2)
            except Exception as e:
                api_status = "unhealthy"
                logger.warning(f"API TrackHS no disponible: {str(e)}")
        else:
            api_status = "not_configured"

        health_data = {
            "status": (
                "healthy" if api_status in ["healthy", "not_configured"] else "degraded"
            ),
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "dependencies": {
                "trackhs_api": {
                    "status": api_status,
                    "response_time_ms": api_response_time,
                    "base_url": settings.trackhs_api_url,
                    "credentials_configured": settings.trackhs_username is not None
                    and settings.trackhs_password is not None,
                }
            },
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
            },
        }

        logger.debug(f"Health check: {health_data['status']}")
        return health_data

    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    logger.info("Iniciando servidor TrackHS MCP en modo HTTP")
    mcp.run(transport="http", host="0.0.0.0", port=8000)
