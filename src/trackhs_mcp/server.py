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
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .client import TrackHSClient
from .config import get_settings, validate_configuration
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
    strict_input_validation=False,  # Permite coerción de tipos: "10" → 10
    mask_error_details=True,
    lifespan=lifespan,
)

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
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha de llegada inicio (YYYY-MM-DD)",
        ),
    ] = None,
    arrival_end: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
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
    if arrival_start:
        params["arrivalStart"] = arrival_start
    if arrival_end:
        params["arrivalEnd"] = arrival_end
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
        int,
        Field(
            ge=1,
            le=10000,
            description="Número de página (1-based). Límite máximo: 10k total results",
        ),
    ] = 1,
    size: Annotated[
        int,
        Field(
            ge=1,
            le=100,
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
        Optional[int], Field(ge=0, le=20, description="Número exacto de dormitorios")
    ] = None,
    min_bedrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número mínimo de dormitorios")
    ] = None,
    max_bedrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número máximo de dormitorios")
    ] = None,
    # Parámetros de baños
    bathrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número exacto de baños")
    ] = None,
    min_bathrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número mínimo de baños")
    ] = None,
    max_bathrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número máximo de baños")
    ] = None,
    # Parámetros de capacidad
    occupancy: Annotated[
        Optional[int], Field(ge=1, le=50, description="Capacidad exacta")
    ] = None,
    min_occupancy: Annotated[
        Optional[int], Field(ge=1, le=50, description="Capacidad mínima")
    ] = None,
    max_occupancy: Annotated[
        Optional[int], Field(ge=1, le=50, description="Capacidad máxima")
    ] = None,
    # Parámetros de fechas
    arrival: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha de llegada (YYYY-MM-DD) para verificar disponibilidad",
        ),
    ] = None,
    departure: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha de salida (YYYY-MM-DD) para verificar disponibilidad",
        ),
    ] = None,
    content_updated_since: Annotated[
        Optional[str],
        Field(description="Fecha ISO 8601 - unidades con cambios desde esta fecha"),
    ] = None,
    # Parámetros de estado y características
    is_active: Annotated[
        Optional[int],
        Field(ge=0, le=1, description="Unidades activas (1) o inactivas (0)"),
    ] = None,
    is_bookable: Annotated[
        Optional[int],
        Field(ge=0, le=1, description="Unidades reservables (1) o no (0)"),
    ] = None,
    pets_friendly: Annotated[
        Optional[int],
        Field(ge=0, le=1, description="Unidades pet-friendly (1) o no (0)"),
    ] = None,
    unit_status: Annotated[
        Optional[Literal["clean", "dirty", "occupied", "inspection", "inprogress"]],
        Field(description="Estado de la unidad"),
    ] = None,
    # Parámetros de funcionalidad adicional
    computed: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=1,
            description="Incluir valores computados adicionales (1) o no (0)",
        ),
    ] = None,
    inherited: Annotated[
        Optional[int],
        Field(ge=0, le=1, description="Incluir atributos heredados (1) o no (0)"),
    ] = None,
    limited: Annotated[
        Optional[int],
        Field(
            ge=0, le=1, description="Retornar atributos limitados (1) o completos (0)"
        ),
    ] = None,
    include_descriptions: Annotated[
        Optional[int],
        Field(ge=0, le=1, description="Incluir descripciones de unidades (1) o no (0)"),
    ] = None,
    # Parámetros de filtros adicionales
    calendar_id: Annotated[
        Optional[int], Field(gt=0, description="ID del grupo de calendario")
    ] = None,
    role_id: Annotated[
        Optional[int], Field(gt=0, description="ID del rol específico")
    ] = None,
    promo_code_id: Annotated[
        Optional[int], Field(gt=0, description="ID del código promocional válido")
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


@mcp.tool(output_schema=AMENITIES_OUTPUT_SCHEMA)
def search_amenities(
    page: Annotated[int, Field(ge=1, le=1000, description="Número de página")] = 1,
    size: Annotated[int, Field(ge=1, le=100, description="Tamaño de página")] = 10,
    search: Annotated[
        Optional[str],
        Field(max_length=200, description="Búsqueda en nombre de amenidad"),
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar amenidades/servicios disponibles en el sistema TrackHS.
    """
    if api_client is None:
        raise ToolError("Cliente API no disponible. Verifique las credenciales.")

    logger.info(f"Buscando amenidades: página {page}, tamaño {size}")

    try:
        params = {"page": page, "size": size}
        if search:
            params["search"] = search

        result = api_client.get("api/pms/units/amenities", params)
        total_items = result.get("total_items", 0)
        logger.info(f"Encontradas {total_items} amenidades")
        return result
    except Exception as e:
        logger.error(f"Error buscando amenidades: {str(e)}")
        raise ToolError(f"Error buscando amenidades: {str(e)}")


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
