"""
Herramientas MCP para TrackHS
Funciones individuales para compatibilidad con FastMCP
"""

import os
import sys
from typing import Any, Dict, List, Optional

from pydantic import Field

from schemas.amenity import AmenitySearchParams, AmenitySearchResponse
from schemas.folio import FolioResponse
from schemas.reservation import (
    ReservationDetailResponse,
    ReservationSearchParams,
    ReservationSearchResponse,
)
from schemas.unit import UnitSearchParams, UnitSearchResponse
from schemas.work_order import (
    HousekeepingWorkOrderParams,
    MaintenanceWorkOrderParams,
    WorkOrderResponse,
)
from utils.api_client import TrackHSAPIClient
from utils.exceptions import TrackHSAPIError, TrackHSNotFoundError
from utils.logger import get_logger
from utils.validators import validate_positive_integer

# Logger global
logger = get_logger(__name__)

# Cliente API global (se inicializará en setup_tools)
api_client: Optional[TrackHSAPIClient] = None


def setup_tools(client: TrackHSAPIClient) -> None:
    """Configura el cliente API para las herramientas"""
    global api_client
    api_client = client
    logger.info("Cliente API configurado para herramientas MCP")


def register_tools_with_mcp(mcp_server) -> None:
    """Registra las herramientas con la instancia de FastMCP"""

    @mcp_server.tool()
    def search_reservations(
        page: int = Field(default=1, ge=1, description="Número de página (1-based)"),
        size: int = Field(
            default=10, ge=1, le=100, description="Tamaño de página (1-100)"
        ),
        search: Optional[str] = Field(
            default=None, max_length=200, description="Búsqueda de texto"
        ),
        arrival_start: Optional[str] = Field(
            default=None, description="Fecha de llegada inicio (YYYY-MM-DD)"
        ),
        arrival_end: Optional[str] = Field(
            default=None, description="Fecha de llegada fin (YYYY-MM-DD)"
        ),
        status: Optional[str] = Field(
            default=None, max_length=50, description="Estado de reserva"
        ),
    ) -> Dict[str, Any]:
        """
        Buscar reservas en TrackHS con filtros avanzados.

        Esta herramienta implementa la API completa de búsqueda de reservas de TrackHS
        con todos los parámetros disponibles según la documentación oficial.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = ReservationSearchParams(
                page=page,
                size=size,
                search=search,
                arrival_start=arrival_start,
                arrival_end=arrival_end,
                status=status,
            )

            # Realizar búsqueda
            response = api_client.search_reservations(params)

            logger.info(
                f"Búsqueda de reservas exitosa: {response.get('total_items', 0)} resultados",
                extra={
                    "page": page,
                    "size": size,
                    "search": search,
                    "total_items": response.get("total_items", 0),
                },
            )

            return response

        except Exception as e:
            logger.error(f"Error buscando reservas: {str(e)}")
            raise TrackHSAPIError(f"Error buscando reservas: {str(e)}")

    @mcp_server.tool()
    def get_reservation(
        reservation_id: int = Field(
            gt=0, description="ID único de la reserva en TrackHS"
        )
    ) -> Dict[str, Any]:
        """
        Obtener detalles completos de una reserva específica por ID.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar ID
            validate_positive_integer(reservation_id, "reservation_id")

            # Obtener reserva
            response = api_client.get_reservation(reservation_id)

            logger.info(
                f"Reserva obtenida exitosamente: {reservation_id}",
                extra={"reservation_id": reservation_id},
            )

            return response

        except TrackHSNotFoundError:
            logger.warning(f"Reserva no encontrada: {reservation_id}")
            raise
        except Exception as e:
            logger.error(f"Error obteniendo reserva {reservation_id}: {str(e)}")
            raise TrackHSAPIError(f"Error obteniendo reserva: {str(e)}")

    @mcp_server.tool()
    def search_units(
        page: int = Field(default=1, ge=1, description="Número de página (1-based)"),
        size: int = Field(
            default=10, ge=1, le=100, description="Tamaño de página (1-100)"
        ),
        # Parámetros de búsqueda de texto
        search: Optional[str] = Field(
            default=None,
            max_length=200,
            description="Búsqueda de texto en nombre o descripciones",
        ),
        term: Optional[str] = Field(
            default=None,
            max_length=200,
            description="Búsqueda de texto en término específico",
        ),
        unit_code: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Búsqueda en código de unidad (exacta o con % para wildcard)",
        ),
        short_name: Optional[str] = Field(
            default=None,
            max_length=100,
            description="Búsqueda en nombre corto (exacta o con % para wildcard)",
        ),
        # Parámetros de características físicas
        bedrooms: Optional[int] = Field(
            default=None, ge=0, description="Número exacto de dormitorios"
        ),
        min_bedrooms: Optional[int] = Field(
            default=None, ge=0, description="Número mínimo de dormitorios"
        ),
        max_bedrooms: Optional[int] = Field(
            default=None, ge=0, description="Número máximo de dormitorios"
        ),
        bathrooms: Optional[int] = Field(
            default=None, ge=0, description="Número exacto de baños"
        ),
        min_bathrooms: Optional[int] = Field(
            default=None, ge=0, description="Número mínimo de baños"
        ),
        max_bathrooms: Optional[int] = Field(
            default=None, ge=0, description="Número máximo de baños"
        ),
        occupancy: Optional[int] = Field(
            default=None, ge=0, description="Capacidad exacta"
        ),
        min_occupancy: Optional[int] = Field(
            default=None, ge=0, description="Capacidad mínima"
        ),
        max_occupancy: Optional[int] = Field(
            default=None, ge=0, description="Capacidad máxima"
        ),
        # Parámetros de estado
        is_active: Optional[bool] = Field(
            default=None, description="Solo unidades activas (1) o inactivas (0)"
        ),
        is_bookable: Optional[bool] = Field(
            default=None, description="Solo unidades reservables (1) o no (0)"
        ),
        pets_friendly: Optional[bool] = Field(
            default=None, description="Solo unidades pet-friendly (1) o no (0)"
        ),
        unit_status: Optional[str] = Field(
            default=None,
            description="Estado de la unidad (clean, dirty, occupied, inspection, inprogress)",
        ),
        allow_unit_rates: Optional[bool] = Field(
            default=None,
            description="Solo unidades que permiten tarifas por unidad (1) o no (0)",
        ),
        # Parámetros de disponibilidad
        arrival: Optional[str] = Field(
            default=None,
            description="Fecha de llegada (YYYY-MM-DD) para verificar disponibilidad",
        ),
        departure: Optional[str] = Field(
            default=None,
            description="Fecha de salida (YYYY-MM-DD) para verificar disponibilidad",
        ),
        # Parámetros de contenido
        computed: Optional[bool] = Field(
            default=None,
            description="Incluir valores computados adicionales (1) o no (0)",
        ),
        inherited: Optional[bool] = Field(
            default=None, description="Incluir atributos heredados (1) o no (0)"
        ),
        limited: Optional[bool] = Field(
            default=None, description="Retornar atributos limitados (1) o completos (0)"
        ),
        include_descriptions: Optional[bool] = Field(
            default=None, description="Incluir descripciones de unidades (1) o no (0)"
        ),
        content_updated_since: Optional[str] = Field(
            default=None,
            description="Fecha ISO 8601 - unidades con cambios desde esta fecha",
        ),
        # Parámetros de IDs
        amenity_id: Optional[List[int]] = Field(
            default=None,
            description="IDs de amenidades - unidades que tienen estas amenidades",
        ),
        node_id: Optional[List[int]] = Field(
            default=None, description="IDs de nodo - unidades descendientes"
        ),
        unit_type_id: Optional[List[int]] = Field(
            default=None, description="IDs de tipo de unidad"
        ),
        owner_id: Optional[List[int]] = Field(
            default=None, description="IDs del propietario"
        ),
        company_id: Optional[List[int]] = Field(
            default=None, description="IDs de la empresa"
        ),
        channel_id: Optional[List[int]] = Field(
            default=None, description="IDs del canal activo"
        ),
        lodging_type_id: Optional[List[int]] = Field(
            default=None, description="IDs del tipo de alojamiento"
        ),
        bed_type_id: Optional[List[int]] = Field(
            default=None, description="IDs del tipo de cama"
        ),
        amenity_all: Optional[List[int]] = Field(
            default=None,
            description="Filtrar unidades que tengan TODAS estas amenidades",
        ),
        unit_ids: Optional[List[int]] = Field(
            default=None, description="Filtrar por IDs específicos de unidades"
        ),
        calendar_id: Optional[int] = Field(
            default=None, gt=0, description="ID del grupo de calendario"
        ),
        role_id: Optional[int] = Field(
            default=None, gt=0, description="ID del rol específico"
        ),
        # Parámetros de ordenamiento
        sort_column: Optional[str] = Field(
            default="name",
            description="Columna para ordenar resultados (id, name, nodeName, unitTypeName)",
        ),
        sort_direction: Optional[str] = Field(
            default="asc", description="Dirección de ordenamiento (asc, desc)"
        ),
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
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = UnitSearchParams(
                page=page,
                size=size,
                search=search,
                term=term,
                unit_code=unit_code,
                short_name=short_name,
                bedrooms=bedrooms,
                min_bedrooms=min_bedrooms,
                max_bedrooms=max_bedrooms,
                bathrooms=bathrooms,
                min_bathrooms=min_bathrooms,
                max_bathrooms=max_bathrooms,
                occupancy=occupancy,
                min_occupancy=min_occupancy,
                max_occupancy=max_occupancy,
                is_active=is_active,
                is_bookable=is_bookable,
                pets_friendly=pets_friendly,
                unit_status=unit_status,
                allow_unit_rates=allow_unit_rates,
                arrival=arrival,
                departure=departure,
                computed=computed,
                inherited=inherited,
                limited=limited,
                include_descriptions=include_descriptions,
                content_updated_since=content_updated_since,
                amenity_id=amenity_id,
                node_id=node_id,
                unit_type_id=unit_type_id,
                owner_id=owner_id,
                company_id=company_id,
                channel_id=channel_id,
                lodging_type_id=lodging_type_id,
                bed_type_id=bed_type_id,
                amenity_all=amenity_all,
                unit_ids=unit_ids,
                calendar_id=calendar_id,
                role_id=role_id,
                sort_column=sort_column,
                sort_direction=sort_direction,
            )

            # Realizar búsqueda
            response = api_client.search_units(params.model_dump())

            logger.info(
                f"Búsqueda de unidades exitosa: {response.get('total_items', 0)} resultados",
                extra={
                    "page": page,
                    "size": size,
                    "search": search,
                    "total_items": response.get("total_items", 0),
                },
            )

            return response

        except Exception as e:
            logger.error(f"Error buscando unidades: {str(e)}")
            raise TrackHSAPIError(f"Error buscando unidades: {str(e)}")

    @mcp_server.tool()
    def search_amenities(
        page: int = Field(default=1, ge=1, description="Número de página (1-based)"),
        size: int = Field(
            default=10, ge=1, le=100, description="Tamaño de página (1-100)"
        ),
        search: Optional[str] = Field(
            default=None, max_length=200, description="Búsqueda de texto"
        ),
        group_id: Optional[int] = Field(
            default=None, gt=0, description="ID del grupo de amenidades"
        ),
        is_public: Optional[bool] = Field(
            default=None, description="Solo amenidades públicas"
        ),
        public_searchable: Optional[bool] = Field(
            default=None, description="Solo amenidades buscables públicamente"
        ),
        is_filterable: Optional[bool] = Field(
            default=None, description="Solo amenidades filtrables"
        ),
    ) -> Dict[str, Any]:
        """
        Buscar amenidades/servicios disponibles en el sistema TrackHS.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = AmenitySearchParams(
                page=page,
                size=size,
                search=search,
                group_id=group_id,
                is_public=is_public,
                public_searchable=public_searchable,
                is_filterable=is_filterable,
            )

            # Realizar búsqueda
            response = api_client.search_amenities(params)

            logger.info(
                f"Búsqueda de amenidades exitosa: {response.get('total_items', 0)} resultados",
                extra={
                    "page": page,
                    "size": size,
                    "search": search,
                    "total_items": response.get("total_items", 0),
                },
            )

            return response

        except Exception as e:
            logger.error(f"Error buscando amenidades: {str(e)}")
            raise TrackHSAPIError(f"Error buscando amenidades: {str(e)}")

    @mcp_server.tool()
    def get_folio(
        reservation_id: int = Field(
            gt=0, description="ID de la reserva para obtener su folio financiero"
        )
    ) -> Dict[str, Any]:
        """
        Obtener el folio financiero completo de una reserva.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar ID
            validate_positive_integer(reservation_id, "reservation_id")

            # Obtener folio
            response = api_client.get_folio(reservation_id)

            logger.info(
                f"Folio obtenido exitosamente para reserva: {reservation_id}",
                extra={"reservation_id": reservation_id},
            )

            return response

        except TrackHSNotFoundError:
            logger.warning(f"Folio no encontrado para reserva: {reservation_id}")
            raise
        except Exception as e:
            logger.error(
                f"Error obteniendo folio para reserva {reservation_id}: {str(e)}"
            )
            raise TrackHSAPIError(f"Error obteniendo folio: {str(e)}")

    @mcp_server.tool()
    def create_maintenance_work_order(
        unit_id: int = Field(
            gt=0, description="ID de la unidad que requiere mantenimiento"
        ),
        summary: str = Field(
            min_length=1, max_length=500, description="Resumen breve del problema"
        ),
        description: str = Field(
            min_length=1, max_length=5000, description="Descripción detallada"
        ),
        priority: int = Field(
            default=3, description="Prioridad: 1=Baja, 3=Media, 5=Alta"
        ),
        estimated_cost: Optional[float] = Field(
            default=None, ge=0, description="Costo estimado"
        ),
        estimated_time: Optional[int] = Field(
            default=None, ge=0, description="Tiempo estimado en minutos"
        ),
        date_received: Optional[str] = Field(
            default=None, description="Fecha de recepción (YYYY-MM-DD)"
        ),
    ) -> Dict[str, Any]:
        """
        Crear una orden de trabajo de mantenimiento para una unidad.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = MaintenanceWorkOrderParams(
                unit_id=unit_id,
                summary=summary,
                description=description,
                priority=priority,
                estimated_cost=estimated_cost,
                estimated_time=estimated_time,
                date_received=date_received,
            )

            # Crear orden de trabajo
            response = api_client.create_maintenance_work_order(params)

            logger.info(
                f"Orden de mantenimiento creada exitosamente: {response.get('id')}",
                extra={
                    "unit_id": unit_id,
                    "work_order_id": response.get("id"),
                    "priority": priority,
                },
            )

            return response

        except Exception as e:
            logger.error(f"Error creando orden de mantenimiento: {str(e)}")
            raise TrackHSAPIError(f"Error creando orden de mantenimiento: {str(e)}")

    @mcp_server.tool()
    def create_housekeeping_work_order(
        unit_id: int = Field(gt=0, description="ID de la unidad que requiere limpieza"),
        scheduled_at: str = Field(description="Fecha programada (YYYY-MM-DD)"),
        is_inspection: bool = Field(
            default=False, description="True si es inspección, False si es limpieza"
        ),
        clean_type_id: Optional[int] = Field(
            default=None, gt=0, description="ID del tipo de limpieza"
        ),
        comments: Optional[str] = Field(
            default=None, max_length=2000, description="Comentarios especiales"
        ),
        cost: Optional[float] = Field(
            default=None, ge=0, description="Costo del servicio"
        ),
    ) -> Dict[str, Any]:
        """
        Crear una orden de trabajo de housekeeping (limpieza) para una unidad.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = HousekeepingWorkOrderParams(
                unit_id=unit_id,
                scheduled_at=scheduled_at,
                is_inspection=is_inspection,
                clean_type_id=clean_type_id,
                comments=comments,
                cost=cost,
            )

            # Crear orden de trabajo
            response = api_client.create_housekeeping_work_order(params)

            logger.info(
                f"Orden de housekeeping creada exitosamente: {response.get('id')}",
                extra={
                    "unit_id": unit_id,
                    "work_order_id": response.get("id"),
                    "scheduled_at": scheduled_at,
                    "is_inspection": is_inspection,
                },
            )

            return response

        except Exception as e:
            logger.error(f"Error creando orden de housekeeping: {str(e)}")
            raise TrackHSAPIError(f"Error creando orden de housekeeping: {str(e)}")
