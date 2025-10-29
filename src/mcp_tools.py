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
        search: Optional[str] = Field(
            default=None, max_length=200, description="Búsqueda de texto"
        ),
        bedrooms: Optional[int] = Field(
            default=None, ge=0, description="Número de dormitorios"
        ),
        bathrooms: Optional[int] = Field(
            default=None, ge=0, description="Número de baños"
        ),
        occupancy: Optional[int] = Field(default=None, ge=0, description="Capacidad"),
        is_active: Optional[bool] = Field(
            default=None, description="Solo unidades activas"
        ),
        is_bookable: Optional[bool] = Field(
            default=None, description="Solo unidades reservables"
        ),
        pets_friendly: Optional[bool] = Field(
            default=None, description="Solo unidades pet-friendly"
        ),
    ) -> Dict[str, Any]:
        """
        Buscar unidades de alojamiento disponibles en TrackHS con filtros avanzados.
        """
        if not api_client:
            raise TrackHSAPIError("Cliente API no configurado")

        try:
            # Validar parámetros
            params = UnitSearchParams(
                page=page,
                size=size,
                search=search,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                occupancy=occupancy,
                is_active=is_active,
                is_bookable=is_bookable,
                pets_friendly=pets_friendly,
            )

            # Realizar búsqueda
            response = api_client.search_units(params)

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
