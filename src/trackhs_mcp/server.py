"""
TrackHS MCP Server - Mejores Prácticas FastMCP
Servidor MCP robusto con validación Pydantic y documentación completa para LLM
"""

import os
from datetime import datetime
from typing import Any, Dict, Literal, Optional

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field
from typing_extensions import Annotated

from .schemas import (
    RESERVATION_SEARCH_OUTPUT_SCHEMA,
    UNIT_SEARCH_OUTPUT_SCHEMA,
    WORK_ORDER_OUTPUT_SCHEMA,
    WorkOrderPriority,
)

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = os.getenv("TRACKHS_BASE_URL", "https://api.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


# Cliente HTTP robusto
class TrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)
        self.client = httpx.Client(auth=self.auth, timeout=30.0)

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request to TrackHS API with error handling"""
        try:
            response = self.client.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con TrackHS: {str(e)}")

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request to TrackHS API with error handling"""
        try:
            response = self.client.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con TrackHS: {str(e)}")


# Inicializar cliente API
if not API_USERNAME or not API_PASSWORD:
    raise ValueError("TRACKHS_USERNAME y TRACKHS_PASSWORD son requeridos")

api_client = TrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)

# Crear servidor MCP
mcp = FastMCP(
    name="TrackHS API",
    instructions="""Servidor MCP para interactuar con la API de TrackHS.

    Proporciona herramientas para:
    - Buscar y consultar reservas
    - Gestionar unidades de alojamiento
    - Consultar amenidades disponibles
    - Obtener información financiera (folios)
    - Crear órdenes de trabajo (mantenimiento y housekeeping)

    Todas las herramientas incluyen validación robusta y documentación completa.""",
)


@mcp.tool(output_schema=RESERVATION_SEARCH_OUTPUT_SCHEMA)
def search_reservations(
    page: Annotated[
        int,
        Field(
            ge=0,
            le=10000,
            description="Número de página (0-based). Límite: page * size <= 10000",
        ),
    ] = 0,
    size: Annotated[
        int, Field(ge=1, le=100, description="Tamaño de página (1-100)")
    ] = 10,
    search: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Búsqueda de texto completo (nombre, email, confirmación)",
        ),
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
        Optional[str],
        Field(
            max_length=50,
            description="Estado de reserva (ej: confirmed, cancelled, checked-in)",
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar reservas en TrackHS con filtros avanzados.

    Esta herramienta permite buscar reservas utilizando múltiples criterios de filtrado.
    Soporta paginación y búsqueda de texto completo.

    Respuesta incluye:
    - _embedded.reservations: Array de objetos de reserva con información completa
    - page, page_count, page_size, total_items: Metadatos de paginación
    - _links: Enlaces HATEOAS para navegación

    Casos de uso comunes:
    - Buscar reservas por fecha de llegada (arrival_start/arrival_end)
    - Filtrar por estado de reserva (confirmed, cancelled, checked-in, etc.)
    - Búsqueda por nombre de huésped o número de confirmación (search)
    - Obtener listado paginado de todas las reservas

    Ejemplos de uso:
    - search_reservations(arrival_start="2024-01-15", arrival_end="2024-01-15") # Llegadas del 15 de enero
    - search_reservations(status="confirmed", size=50) # Reservas confirmadas, 50 por página
    - search_reservations(search="john@email.com") # Buscar por email del huésped
    """
    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if arrival_start:
        params["arrival_start"] = arrival_start
    if arrival_end:
        params["arrival_end"] = arrival_end
    if status:
        params["status"] = status

    return api_client.get("reservations", params)


@mcp.tool
def get_reservation(
    reservation_id: Annotated[
        int, Field(gt=0, description="ID único de la reserva en TrackHS")
    ],
) -> Dict[str, Any]:
    """
    Obtener detalles completos de una reserva específica por ID.

    Retorna información completa incluyendo:
    - Datos del huésped (nombre, email, teléfono, dirección)
    - Fechas de check-in/check-out
    - Unidad asignada con detalles completos
    - Estado de la reserva y historial
    - Información de pago y balance
    - Políticas aplicables (cancelación, depósito, etc.)
    - Enlaces a recursos relacionados (folio, unidad, etc.)

    Útil para:
    - Ver detalles completos de una reserva específica
    - Verificar información antes de check-in
    - Consultar historial y estado de reserva
    - Obtener información de contacto del huésped
    - Revisar políticas y términos aplicables

    Ejemplo de uso:
    - get_reservation(reservation_id=12345) # Obtener detalles de reserva ID 12345
    """
    return api_client.get(f"reservations/{reservation_id}")


@mcp.tool(output_schema=UNIT_SEARCH_OUTPUT_SCHEMA)
def search_units(
    page: Annotated[
        int, Field(ge=1, le=400, description="Número de página (1-based)")
    ] = 1,
    size: Annotated[
        int, Field(ge=1, le=25, description="Tamaño de página (1-25)")
    ] = 10,
    search: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Búsqueda de texto (nombre, descripción, código)",
        ),
    ] = None,
    bedrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número exacto de dormitorios")
    ] = None,
    bathrooms: Annotated[
        Optional[int], Field(ge=0, le=20, description="Número exacto de baños")
    ] = None,
    is_active: Annotated[
        Optional[int],
        Field(
            ge=0, le=1, description="Filtrar por unidades activas (1) o inactivas (0)"
        ),
    ] = None,
    is_bookable: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=1,
            description="Filtrar por unidades disponibles para reservar (1) o no (0)",
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    Buscar unidades de alojamiento disponibles en TrackHS.

    Permite filtrar unidades por características específicas como dormitorios,
    baños, y búsqueda de texto en nombre/descripción.

    Respuesta incluye para cada unidad:
    - Información básica (id, nombre, código)
    - Características físicas (dormitorios, baños, área, capacidad)
    - Ubicación y dirección completa
    - Amenidades disponibles
    - Reglas de la casa y políticas
    - Información de check-in/check-out
    - Estado de disponibilidad

    Casos de uso:
    - Búsqueda de unidades por capacidad (bedrooms/bathrooms)
    - Filtrado por características específicas
    - Listado de inventario disponible
    - Búsqueda por ubicación o nombre
    - Verificar disponibilidad de unidades

    Ejemplos de uso:
    - search_units(bedrooms=2, bathrooms=1) # Unidades de 2 dormitorios, 1 baño
    - search_units(is_active=1, is_bookable=1) # Unidades activas y disponibles
    - search_units(search="penthouse") # Buscar por nombre o descripción
    """
    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if bedrooms is not None:
        params["bedrooms"] = bedrooms
    if bathrooms is not None:
        params["bathrooms"] = bathrooms
    if is_active is not None:
        params["is_active"] = is_active
    if is_bookable is not None:
        params["is_bookable"] = is_bookable

    return api_client.get("units", params)


@mcp.tool
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

    Las amenidades son características o servicios que pueden tener las unidades
    (ej: WiFi, piscina, aire acondicionado, estacionamiento, etc.)

    Respuesta incluye:
    - id: Identificador único de la amenidad
    - name: Nombre descriptivo de la amenidad
    - group: Grupo/categoría a la que pertenece
    - isPublic: Si es visible públicamente
    - isFilterable: Si se puede usar como filtro de búsqueda
    - description: Descripción detallada de la amenidad

    Útil para:
    - Conocer amenidades disponibles en unidades
    - Filtrar unidades por amenidades específicas
    - Configuración de filtros de búsqueda
    - Catálogo de servicios disponibles
    - Verificar qué amenidades tiene una unidad

    Ejemplos de uso:
    - search_amenities(search="wifi") # Buscar amenidades relacionadas con WiFi
    - search_amenities(size=50) # Obtener catálogo completo de amenidades
    """
    params = {"page": page, "size": size}
    if search:
        params["search"] = search

    return api_client.get("amenities", params)


@mcp.tool
def get_folio(
    reservation_id: Annotated[
        int,
        Field(gt=0, description="ID de la reserva para obtener su folio financiero"),
    ],
) -> Dict[str, Any]:
    """
    Obtener el folio financiero completo de una reserva.

    El folio contiene todos los cargos, pagos, ajustes y balance de una reserva.

    Incluye:
    - Cargos de alojamiento (noche por noche)
    - Impuestos aplicables (taxes, fees)
    - Cargos adicionales (limpieza, mascotas, servicios extra)
    - Pagos recibidos (depósitos, pagos parciales, pagos completos)
    - Balance pendiente
    - Historial de transacciones
    - Desglose detallado por concepto

    Casos de uso:
    - Verificar estado de cuenta de reserva
    - Revisar cargos antes del checkout
    - Auditoría financiera de reserva
    - Generar reportes de ingresos
    - Verificar pagos pendientes
    - Reconciliación de pagos

    Ejemplo de uso:
    - get_folio(reservation_id=12345) # Obtener folio financiero de reserva 12345
    """
    return api_client.get(f"reservations/{reservation_id}/folio")


@mcp.tool(output_schema=WORK_ORDER_OUTPUT_SCHEMA)
def create_maintenance_work_order(
    unit_id: Annotated[
        int, Field(gt=0, description="ID de la unidad que requiere mantenimiento")
    ],
    summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=500,
            description="Resumen breve del problema o trabajo requerido",
        ),
    ],
    description: Annotated[
        str,
        Field(
            min_length=1,
            max_length=5000,
            description="Descripción detallada del trabajo de mantenimiento",
        ),
    ],
    priority: Annotated[
        Literal[1, 3, 5], Field(description="Prioridad: 1=Baja, 3=Media, 5=Alta")
    ] = 3,
    estimated_cost: Annotated[
        Optional[float], Field(ge=0, description="Costo estimado en moneda local")
    ] = None,
    estimated_time: Annotated[
        Optional[int], Field(ge=0, description="Tiempo estimado en minutos")
    ] = None,
    date_received: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha de recepción (YYYY-MM-DD, default: hoy)",
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    Crear una orden de trabajo de mantenimiento para una unidad.

    Las órdenes de mantenimiento se usan para:
    - Reparaciones necesarias (plomería, electricidad, HVAC, etc.)
    - Mantenimiento preventivo programado
    - Mejoras o actualizaciones de unidades
    - Problemas reportados por huéspedes
    - Mantenimiento de amenidades (piscina, jacuzzi, etc.)

    La API de TrackHS requiere:
    - dateReceived, priority, status, summary, estimatedCost, estimatedTime

    Respuesta incluye:
    - id: ID de la orden creada
    - status: Estado actual de la orden
    - Información de asignación (usuario/vendor)
    - Fechas y tiempos
    - Enlaces a recursos relacionados

    Prioridades:
    - 1 (Baja): Puede esperar, no urgente, programar en horario normal
    - 3 (Media): Atención normal, programar pronto, dentro de 24-48 horas
    - 5 (Alta): Urgente, atención inmediata, afecta operación

    Ejemplos de uso:
    - create_maintenance_work_order(unit_id=123, summary="Fuga en grifo", description="Grifo del baño principal gotea constantemente", priority=3)
    - create_maintenance_work_order(unit_id=456, summary="Aire acondicionado no funciona", description="AC no enfría, revisar termostato y compresor", priority=5, estimated_cost=150.0)
    """
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

    return api_client.post("maintenance-work-orders", work_order_data)


@mcp.tool(output_schema=WORK_ORDER_OUTPUT_SCHEMA)
def create_housekeeping_work_order(
    unit_id: Annotated[
        int, Field(gt=0, description="ID de la unidad que requiere limpieza")
    ],
    scheduled_at: Annotated[
        str,
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="Fecha programada para la limpieza (YYYY-MM-DD)",
        ),
    ],
    is_inspection: Annotated[
        bool, Field(description="True si es inspección, False si es limpieza")
    ] = False,
    clean_type_id: Annotated[
        Optional[int],
        Field(
            gt=0, description="ID del tipo de limpieza (requerido si no es inspección)"
        ),
    ] = None,
    comments: Annotated[
        Optional[str],
        Field(max_length=2000, description="Comentarios o instrucciones especiales"),
    ] = None,
    cost: Annotated[
        Optional[float], Field(ge=0, description="Costo del servicio")
    ] = None,
) -> Dict[str, Any]:
    """
    Crear una orden de trabajo de housekeeping (limpieza) para una unidad.

    Las órdenes de housekeeping cubren:
    - Limpiezas entre reservas (turnovers)
    - Inspecciones de calidad
    - Limpiezas programadas
    - Reposición de suministros
    - Limpiezas especiales (post-evento, mascotas, etc.)

    Tipos de órdenes:
    - Inspección (is_inspection=True): Verificación de estado sin limpieza
    - Limpieza (is_inspection=False): Requiere especificar clean_type_id

    La API requiere: unitId, scheduledAt, status

    Respuesta incluye:
    - id: ID de la orden creada
    - status: Estado (pending, in-progress, completed, etc.)
    - Información de asignación
    - Fechas y tiempos
    - Costos asociados
    - Enlaces a recursos relacionados

    Estados posibles:
    - pending: Pendiente de asignación
    - not-started: Asignada pero no iniciada
    - in-progress: En proceso de limpieza
    - completed: Completada
    - processed: Procesada administrativamente
    - cancelled: Cancelada
    - exception: Con excepciones/problemas

    Ejemplos de uso:
    - create_housekeeping_work_order(unit_id=123, scheduled_at="2024-01-15", is_inspection=False, clean_type_id=1)
    - create_housekeeping_work_order(unit_id=456, scheduled_at="2024-01-16", is_inspection=True, comments="Verificar estado post-evento")
    """
    if not is_inspection and clean_type_id is None:
        raise ValueError("clean_type_id es requerido cuando is_inspection=False")

    work_order_data = {
        "unitId": unit_id,
        "scheduledAt": scheduled_at,
        "status": "pending",
        "isInspection": is_inspection,
    }

    if clean_type_id is not None:
        work_order_data["cleanTypeId"] = clean_type_id
    if comments:
        work_order_data["comments"] = comments
    if cost is not None:
        work_order_data["cost"] = cost

    return api_client.post("housekeeping-work-orders", work_order_data)


# Configuración HTTP explícita
if __name__ == "__main__":
    # HTTP transport según fastmcp.json
    mcp.run(transport="http", host="0.0.0.0", port=8080)
