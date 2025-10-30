"""
Herramientas MCP para TrackHS
Funciones individuales para compatibilidad con FastMCP
"""

import json
import os
import re
import sys
from datetime import datetime
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

    # Utilidades simples de coerción de tipos para entradas del MCP
    def _coerce_bool(value: Any) -> Optional[bool]:
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(int(value))
        if isinstance(value, str):
            v = value.strip().lower()
            if v in {"true", "1", "yes", "y", "si", "sí"}:
                return True
            if v in {"false", "0", "no", "n"}:
                return False
        return None

    def _coerce_int(value: Any) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str) and value.strip() != "":
            try:
                return int(value.strip())
            except ValueError:
                return None
        return None

    def _coerce_float(value: Any) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and value.strip() != "":
            try:
                return float(value.strip())
            except ValueError:
                return None
        return None

    def _coerce_date_str(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            # Solo aceptar fechas completas YYYY-MM-DD
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                return v
            # Si es solo año (2024), devolver None para evitar errores
            if re.fullmatch(r"\d{4}", v):
                return None
        return None

    def _coerce_list_int(value: Any) -> Optional[List[int]]:
        if value is None:
            return None
        if isinstance(value, list):
            result: List[int] = []
            for x in value:
                i = _coerce_int(x)
                if i is not None:
                    result.append(i)
            return result if result else None
        if isinstance(value, str):
            s = value.strip()
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return _coerce_list_int(parsed)
            except Exception:
                parts = [p for p in re.split(r"[\s,]+", s.strip("[]")) if p]
                result = []
                for p in parts:
                    i = _coerce_int(p)
                    if i is not None:
                        result.append(i)
                return result if result else None
        return None

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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

        try:
            # Coerción simple de tipos de entrada
            page_c = _coerce_int(page) or 1
            size_c = _coerce_int(size) or 10
            arrival_start_c = _coerce_date_str(arrival_start)
            arrival_end_c = _coerce_date_str(arrival_end)

            # Validar parámetros
            params = ReservationSearchParams(
                page=page_c,
                size=size_c,
                search=search,
                arrival_start=arrival_start_c,
                arrival_end=arrival_end_c,
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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

        try:
            # Coerción simple de tipos de entrada
            page_c = _coerce_int(page) or 1
            size_c = _coerce_int(size) or 10
            bedrooms_c = _coerce_int(bedrooms)
            min_bedrooms_c = _coerce_int(min_bedrooms)
            max_bedrooms_c = _coerce_int(max_bedrooms)
            bathrooms_c = _coerce_int(bathrooms)
            min_bathrooms_c = _coerce_int(min_bathrooms)
            max_bathrooms_c = _coerce_int(max_bathrooms)
            occupancy_c = _coerce_int(occupancy)
            min_occupancy_c = _coerce_int(min_occupancy)
            max_occupancy_c = _coerce_int(max_occupancy)
            is_active_c = _coerce_bool(is_active)
            is_bookable_c = _coerce_bool(is_bookable)
            pets_friendly_c = _coerce_bool(pets_friendly)
            allow_unit_rates_c = _coerce_bool(allow_unit_rates)
            computed_c = _coerce_bool(computed)
            inherited_c = _coerce_bool(inherited)
            limited_c = _coerce_bool(limited)
            include_descriptions_c = _coerce_bool(include_descriptions)
            arrival_c = _coerce_date_str(arrival)
            departure_c = _coerce_date_str(departure)
            content_updated_since_c = content_updated_since
            amenity_id_c = _coerce_list_int(amenity_id)
            node_id_c = _coerce_list_int(node_id)
            unit_type_id_c = _coerce_list_int(unit_type_id)
            owner_id_c = _coerce_list_int(owner_id)
            company_id_c = _coerce_list_int(company_id)
            channel_id_c = _coerce_list_int(channel_id)
            lodging_type_id_c = _coerce_list_int(lodging_type_id)
            bed_type_id_c = _coerce_list_int(bed_type_id)
            amenity_all_c = _coerce_list_int(amenity_all)
            unit_ids_c = _coerce_list_int(unit_ids)
            calendar_id_c = _coerce_int(calendar_id)
            role_id_c = _coerce_int(role_id)

            # Validar parámetros
            params = UnitSearchParams(
                page=page_c,
                size=size_c,
                search=search,
                term=term,
                unit_code=unit_code,
                short_name=short_name,
                bedrooms=bedrooms_c,
                min_bedrooms=min_bedrooms_c,
                max_bedrooms=max_bedrooms_c,
                bathrooms=bathrooms_c,
                min_bathrooms=min_bathrooms_c,
                max_bathrooms=max_bathrooms_c,
                occupancy=occupancy_c,
                min_occupancy=min_occupancy_c,
                max_occupancy=max_occupancy_c,
                is_active=is_active_c,
                is_bookable=is_bookable_c,
                pets_friendly=pets_friendly_c,
                unit_status=unit_status,
                allow_unit_rates=allow_unit_rates_c,
                arrival=arrival_c,
                departure=departure_c,
                computed=computed_c,
                inherited=inherited_c,
                limited=limited_c,
                include_descriptions=include_descriptions_c,
                content_updated_since=content_updated_since_c,
                amenity_id=amenity_id_c,
                node_id=node_id_c,
                unit_type_id=unit_type_id_c,
                owner_id=owner_id_c,
                company_id=company_id_c,
                channel_id=channel_id_c,
                lodging_type_id=lodging_type_id_c,
                bed_type_id=bed_type_id_c,
                amenity_all=amenity_all_c,
                unit_ids=unit_ids_c,
                calendar_id=calendar_id_c,
                role_id=role_id_c,
                sort_column=sort_column,
                sort_direction=sort_direction,
            )

            # Realizar búsqueda
            response = api_client.search_units(params.model_dump())

            # Fallback simple de filtrado del lado cliente si el API no respeta filtros
            units = response.get("units") or response.get("_embedded", {}).get("units")
            if isinstance(units, list):
                applied = False

                def _matches(u: Dict[str, Any]) -> bool:
                    def gv(keys: List[str]) -> Any:
                        for k in keys:
                            if k in u:
                                return u[k]
                        return None

                    # Booleanos (camelCase según API TrackHS)
                    if is_active_c is not None:
                        applied = True
                        if gv(["isActive"]) is not is_active_c:
                            return False
                    if is_bookable_c is not None:
                        applied = True
                        if gv(["isBookable"]) is not is_bookable_c:
                            return False
                    if pets_friendly_c is not None:
                        applied = True
                        if gv(["petFriendly"]) is not pets_friendly_c:
                            return False

                    # Numéricos: bedrooms/bathrooms/occupancy (camelCase según API TrackHS)
                    b = gv(["bedrooms"]) or 0
                    ba = (
                        gv(["fullBathrooms"]) or 0
                    )  # API usa fullBathrooms, no bathrooms
                    oc = gv(["maxOccupancy"]) or 0
                    if bedrooms_c is not None:
                        applied = True
                        if b != bedrooms_c:
                            return False
                    if min_bedrooms_c is not None and b < min_bedrooms_c:
                        applied = True
                        return False
                    if max_bedrooms_c is not None and b > max_bedrooms_c:
                        applied = True
                        return False
                    if bathrooms_c is not None and ba != bathrooms_c:
                        applied = True
                        return False
                    if min_bathrooms_c is not None and ba < min_bathrooms_c:
                        applied = True
                        return False
                    if max_bathrooms_c is not None and ba > max_bathrooms_c:
                        applied = True
                        return False
                    if occupancy_c is not None and oc != occupancy_c:
                        applied = True
                        return False
                    if min_occupancy_c is not None and oc < min_occupancy_c:
                        applied = True
                        return False
                    if max_occupancy_c is not None and oc > max_occupancy_c:
                        applied = True
                        return False

                    # unit_ids
                    if unit_ids_c:
                        applied = True
                        if gv(["id"]) not in set(unit_ids_c):
                            return False

                    return True

                filtered = [u for u in units if _matches(u)]
                if applied and len(filtered) != len(units):
                    response["units"] = filtered
                    response["filtersAppliedClientSide"] = True
                    response["total_items_client_page"] = len(filtered)

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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

        try:
            # Coerción simple
            page_c = _coerce_int(page) or 1
            size_c = _coerce_int(size) or 10
            group_id_c = _coerce_int(group_id)
            is_public_c = _coerce_bool(is_public)
            public_searchable_c = _coerce_bool(public_searchable)
            is_filterable_c = _coerce_bool(is_filterable)

            # Validar parámetros
            params = AmenitySearchParams(
                page=page_c,
                size=size_c,
                search=search,
                group_id=group_id_c,
                is_public=is_public_c,
                public_searchable=public_searchable_c,
                is_filterable=is_filterable_c,
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
        folio_id: int = Field(
            gt=0,
            description="ID único del folio financiero en TrackHS. IMPORTANTE: Este es el ID del folio, NO el ID de la reserva. Para obtener el folio de una reserva, primero usa get_reservation para obtener el folio_id.",
        )
    ) -> Dict[str, Any]:
        """
        Obtener información completa de un folio financiero por su ID.

        Un folio financiero es un documento que registra todas las transacciones financieras
        asociadas a una reserva o cuenta de huésped, incluyendo cargos, pagos, comisiones
        y balances.

        ⚠️  IMPORTANTE: Este endpoint requiere el ID del folio, NO el ID de la reserva.

        CÓMO OBTENER EL FOLIO_ID:
        1. Usa get_reservation(reservation_id=123) para obtener detalles de la reserva
        2. En la respuesta, busca el campo 'folio_id'
        3. Usa ese folio_id con esta herramienta: get_folio(folio_id=456)

        PARÁMETROS:
        - folio_id: ID único del folio en el sistema TrackHS (requerido)

        INFORMACIÓN DEVUELTA:
        - Datos básicos: ID, estado (open/closed), tipo (guest/master)
        - Balances: balance actual, balance realizado
        - Fechas: inicio, fin, cierre, check-in, check-out
        - Información de contacto y empresa asociada
        - Comisiones de agente y propietario
        - Datos embebidos: contacto, empresa, agente de viajes
        - Enlaces relacionados

        EJEMPLO DE USO:
        1. get_reservation(reservation_id=123) → obtiene folio_id: 456
        2. get_folio(folio_id=456) → obtiene detalles financieros

        CÓDIGOS DE ERROR:
        - 404: Folio no encontrado (folio_id no existe)
        - 401: Credenciales inválidas
        - 403: Sin permisos para acceder al folio
        - 500: Error interno del servidor
        """
        if not api_client:
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

        try:
            # Validar que no se pase reservation_id por error
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                local_vars = frame.f_back.f_locals
                if "reservation_id" in local_vars:
                    raise ValueError(
                        "❌ ERROR: Usaste 'reservation_id' pero esta herramienta requiere 'folio_id'. "
                        "Para obtener el folio de una reserva:\n"
                        "1. Usa get_reservation(reservation_id=123) para obtener detalles de la reserva\n"
                        "2. En la respuesta, busca el campo 'folio_id'\n"
                        "3. Usa get_folio(folio_id=456) con ese ID"
                    )

            # Validar ID
            validate_positive_integer(folio_id, "folio_id")

            # Obtener folio
            response = api_client.get_folio(folio_id)

            # Validar que la respuesta tiene la estructura esperada
            if not isinstance(response, dict):
                raise TrackHSAPIError("Respuesta del API no es un diccionario válido")

            # Verificar campos básicos requeridos
            if "id" not in response:
                raise TrackHSAPIError("Respuesta del API no contiene ID del folio")

            if "status" not in response:
                raise TrackHSAPIError("Respuesta del API no contiene estado del folio")

            # Log de información útil para debugging
            logger.info(
                f"Folio obtenido exitosamente: {folio_id}",
                extra={
                    "folio_id": folio_id,
                    "folio_status": response.get("status"),
                    "folio_type": response.get("type"),
                    "has_embedded_data": "_embedded" in response,
                    "has_links": "_links" in response,
                },
            )

            # Agregar metadatos útiles a la respuesta
            response["_metadata"] = {
                "retrieved_at": datetime.now().isoformat(),
                "folio_id": folio_id,
                "api_version": "1.0",
                "source": "TrackHS API",
            }

            return response

        except TrackHSNotFoundError:
            logger.warning(f"Folio no encontrado: {folio_id}")
            raise TrackHSNotFoundError(
                f"Folio con ID {folio_id} no encontrado en el sistema TrackHS"
            )
        except TrackHSAuthenticationError as e:
            logger.error(
                f"Error de autenticación obteniendo folio {folio_id}: {str(e)}"
            )
            raise TrackHSAuthenticationError(f"Error de autenticación: {str(e)}")
        except TrackHSAuthorizationError as e:
            logger.error(f"Error de autorización obteniendo folio {folio_id}: {str(e)}")
            raise TrackHSAuthorizationError(
                f"No tienes permisos para acceder al folio {folio_id}"
            )
        except TrackHSAPIError as e:
            logger.error(f"Error de API obteniendo folio {folio_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado obteniendo folio {folio_id}: {str(e)}")
            raise TrackHSAPIError(f"Error inesperado obteniendo folio: {str(e)}")

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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

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
            error_msg = (
                "Cliente API no configurado. "
                "Esto indica que las credenciales de TrackHS no están configuradas. "
                "Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno o archivo .env"
            )
            raise TrackHSAPIError(error_msg)

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
