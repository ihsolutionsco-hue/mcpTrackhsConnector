"""
TrackHS MCP Server - Mejores Prácticas FastMCP
Servidor MCP robusto con validación Pydantic y documentación completa para LLM
"""

import json
import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field
from typing_extensions import Annotated

from .cache import get_cache
from .config import get_settings, validate_configuration
from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    TrackHSError,
    ValidationError,
)
from .metrics import get_metrics
from .middleware_native import (
    TrackHSAuthMiddleware,
    TrackHSLoggingMiddleware,
    TrackHSMetricsMiddleware,
    TrackHSRateLimitMiddleware,
)
from .repositories import (
    ReservationRepository,
    UnitRepository,
    WorkOrderRepository,
)
from .schemas import (
    AMENITIES_OUTPUT_SCHEMA,
    FOLIO_DETAIL_OUTPUT_SCHEMA,
    RESERVATION_DETAIL_OUTPUT_SCHEMA,
    RESERVATION_SEARCH_OUTPUT_SCHEMA,
    UNIT_SEARCH_OUTPUT_SCHEMA,
    WORK_ORDER_DETAIL_OUTPUT_SCHEMA,
    CollectionResponse,
    FolioResponse,
    ReservationResponse,
    UnitResponse,
    WorkOrderPriority,
    WorkOrderResponse,
)
from .services import (
    ReservationService,
    UnitService,
    WorkOrderService,
)

# Obtener configuración centralizada
settings = get_settings()

# Validar configuración al inicio
if not validate_configuration():
    sys.exit(1)

# Configuración de logging estructurado
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configuración de la API desde settings
API_BASE_URL = settings.trackhs_api_url
API_USERNAME = settings.trackhs_username
API_PASSWORD = settings.trackhs_password

logger.info(f"TrackHS MCP Server iniciando - Base URL: {API_BASE_URL}")
logger.info(f"Username configurado: {'Sí' if API_USERNAME else 'No'}")
logger.info(f"Password configurado: {'Sí' if API_PASSWORD else 'No'}")
logger.info(f"Log Level: {settings.log_level}")
logger.info(f"Strict Validation: {settings.strict_validation}")


# Datos sensibles que deben ser sanitizados en logs
SENSITIVE_KEYS = {
    "email",
    "phone",
    "telephone",
    "mobile",
    "password",
    "pwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "card",
    "credit",
    "creditcard",
    "ssn",
    "social_security",
    "address",
    "street",
    "postal",
    "zip",
    "payment",
}


def sanitize_for_log(data: Any, max_depth: int = 10) -> Any:
    """
    Sanitiza datos sensibles para logging seguro.

    Oculta valores de campos que puedan contener información personal
    o sensible como emails, teléfonos, direcciones, etc.

    Args:
        data: Datos a sanitizar (dict, list, str, etc.)
        max_depth: Profundidad máxima de recursión

    Returns:
        Datos sanitizados con valores sensibles reemplazados por '***REDACTED***'
    """
    if max_depth <= 0:
        return "***MAX_DEPTH***"

    if data is None:
        return None

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            # Verificar si la clave contiene alguna palabra sensible
            is_sensitive = any(sensitive in key_lower for sensitive in SENSITIVE_KEYS)

            if is_sensitive:
                sanitized[key] = "***REDACTED***"
            else:
                sanitized[key] = sanitize_for_log(value, max_depth - 1)
        return sanitized

    elif isinstance(data, (list, tuple)):
        return [sanitize_for_log(item, max_depth - 1) for item in data]

    elif isinstance(data, str):
        # Detectar si parece un email o teléfono en el string
        if "@" in data and "." in data:  # Posible email
            return "***EMAIL_REDACTED***"
        # No sanitizar otros strings por defecto
        return data

    else:
        # Para otros tipos (int, float, bool, etc.) retornar tal cual
        return data


# ✅ ELIMINADO: retry_with_backoff()
# FastMCP RetryMiddleware maneja reintentos automáticamente con backoff exponencial
# No se necesita reimplementar esta funcionalidad


# Función helper para validación de respuestas
def validate_response(
    data: Dict[str, Any], model_class: type, strict: Optional[bool] = None
):
    """
    Valida datos de respuesta contra un modelo Pydantic.

    MEJOR PRÁCTICA: Validación robusta con transformación automática de tipos.
    Convierte tipos incorrectos automáticamente cuando es posible.

    Args:
        data: Datos a validar
        model_class: Clase del modelo Pydantic
        strict: Si True, lanza excepción en caso de error. Si None, usa configuración global.

    Returns:
        Datos validados (modelo Pydantic) si tiene éxito, o datos originales si falla en modo no-strict

    Raises:
        ValidationError: Si strict=True y la validación falla
    """
    # Usar configuración global si no se especifica strict
    if strict is None:
        strict = settings.strict_validation

    try:
        # Intentar validación con transformación automática de tipos
        validated = model_class.model_validate(data, strict=False)
        logger.debug(f"Response validated successfully against {model_class.__name__}")
        return validated.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        if strict:
            logger.error(f"Response validation failed: {str(e)}")
            raise ValidationError(f"Respuesta de API no válida: {str(e)}")
        else:
            logger.warning(f"Response validation warning (non-strict): {str(e)}")
            # En modo no-strict, intentar limpiar datos básicos
            return _clean_response_data(data, model_class)


def _clean_response_data(data: Dict[str, Any], model_class: type) -> Dict[str, Any]:
    """
    Limpia datos de respuesta básicos para evitar errores de tipo.

    MEJOR PRÁCTICA: Transformación automática de tipos comunes.
    """
    cleaned = data.copy()

    # Limpiar campos comunes que causan problemas
    if "confirmation_number" in cleaned and cleaned["confirmation_number"] is not None:
        cleaned["confirmation_number"] = str(cleaned["confirmation_number"])

    if "unit_id" in cleaned and cleaned["unit_id"] is not None:
        try:
            cleaned["unit_id"] = int(cleaned["unit_id"])
        except (ValueError, TypeError):
            cleaned["unit_id"] = None

    # Limpiar campos numéricos
    for field in ["bedrooms", "bathrooms", "max_occupancy", "priority"]:
        if field in cleaned and cleaned[field] is not None:
            try:
                cleaned[field] = int(cleaned[field])
            except (ValueError, TypeError):
                cleaned[field] = None

    # Limpiar campos de fecha
    for field in ["arrival_date", "departure_date", "date_received", "date_completed"]:
        if field in cleaned and cleaned[field] is not None:
            cleaned[field] = str(cleaned[field])

    return cleaned


# Cliente HTTP robusto
class TrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)
        self.client = httpx.Client(auth=self.auth, timeout=settings.request_timeout)
        logger.info(
            f"TrackHSClient inicializado para {base_url} (timeout: {settings.request_timeout}s)"
        )

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        GET request to TrackHS API with error handling.

        Reintentos automáticos manejados por FastMCP RetryMiddleware.
        """
        full_url = f"{self.base_url}/{endpoint}"
        sanitized_params = sanitize_for_log(params)
        logger.debug(f"GET request to {full_url} with params: {sanitized_params}")

        try:
            response = self.client.get(full_url, params=params)
            logger.debug(f"Response status: {response.status_code}")

            response.raise_for_status()

            # Parsear respuesta
            response_data = response.json()
            sanitized_response = sanitize_for_log(response_data)
            logger.debug(f"Response preview: {str(sanitized_response)[:300]}")

            return response_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code} - {full_url}")

            # Check if response is HTML
            if "text/html" in e.response.headers.get("content-type", ""):
                raise NotFoundError(
                    f"Endpoint no encontrado: {full_url} (respuesta HTML)"
                )

            # Mapear status codes a excepciones específicas
            if e.response.status_code == 401:
                raise AuthenticationError(f"Credenciales inválidas: {e.response.text}")
            elif e.response.status_code == 403:
                raise AuthenticationError(f"Acceso denegado: {e.response.text}")
            elif e.response.status_code == 404:
                raise NotFoundError(f"Recurso no encontrado: {e.response.text}")
            elif e.response.status_code == 422:
                raise ValidationError(f"Error de validación: {e.response.text}")
            elif e.response.status_code >= 500:
                # RetryMiddleware reintentará estos errores automáticamente
                raise APIError(f"Error del servidor TrackHS: {e.response.status_code}")
            else:
                raise APIError(
                    f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
                )

        except httpx.RequestError as e:
            # RetryMiddleware reintentará estos errores automáticamente
            logger.error(f"Request error: {str(e)}")
            raise ConnectionError(f"Error de conexión con TrackHS: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrackHSError(f"Error inesperado: {str(e)}")

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        POST request to TrackHS API with error handling.

        Reintentos automáticos manejados por FastMCP RetryMiddleware.
        """
        full_url = f"{self.base_url}/{endpoint}"
        sanitized_data = sanitize_for_log(data)
        logger.debug(f"POST request to {full_url} with data: {sanitized_data}")

        try:
            response = self.client.post(full_url, json=data)
            logger.debug(f"Response status: {response.status_code}")

            response.raise_for_status()

            # Parsear respuesta
            response_data = response.json()
            sanitized_response = sanitize_for_log(response_data)
            logger.debug(f"Response preview: {str(sanitized_response)[:300]}")

            return response_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code} - {full_url}")

            # Check if response is HTML
            if "text/html" in e.response.headers.get("content-type", ""):
                raise NotFoundError(
                    f"Endpoint no encontrado: {full_url} (respuesta HTML)"
                )

            # Mapear status codes a excepciones específicas
            if e.response.status_code == 401:
                raise AuthenticationError(f"Credenciales inválidas: {e.response.text}")
            elif e.response.status_code == 404:
                raise NotFoundError(f"Recurso no encontrado: {e.response.text}")
            elif e.response.status_code >= 500:
                # RetryMiddleware reintentará estos errores automáticamente
                raise APIError(f"Error del servidor TrackHS: {e.response.status_code}")
            else:
                raise APIError(
                    f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
                )

        except httpx.RequestError as e:
            # RetryMiddleware reintentará estos errores automáticamente
            logger.error(f"Request error: {str(e)}")
            raise ConnectionError(f"Error de conexión con TrackHS: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TrackHSError(f"Error inesperado: {str(e)}")


# Inicializar cliente API con manejo robusto para FastMCP Cloud
try:
    if not API_USERNAME or not API_PASSWORD:
        logger.warning("TRACKHS_USERNAME y TRACKHS_PASSWORD no están configurados")
        logger.warning(
            "El servidor se iniciará pero las herramientas no funcionarán sin credenciales"
        )
        api_client = None
        # Inicializar repositories sin cliente API
        reservation_repo = None
        unit_repo = None
        work_order_repo = None
    else:
        api_client = TrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)
        logger.info("Cliente API TrackHS inicializado correctamente")

        # Inicializar repositories
        reservation_repo = ReservationRepository(
            api_client, cache_ttl=settings.auth_cache_ttl
        )
        unit_repo = UnitRepository(api_client, cache_ttl=settings.auth_cache_ttl)
        work_order_repo = WorkOrderRepository(
            api_client, cache_ttl=settings.auth_cache_ttl
        )
        logger.info("Repositories inicializados correctamente")

        # Inicializar servicios de negocio
        reservation_service = ReservationService(reservation_repo)
        unit_service = UnitService(unit_repo)
        work_order_service = WorkOrderService(work_order_repo)
        logger.info("Servicios de negocio inicializados correctamente")

except Exception as e:
    logger.error(f"Error inicializando cliente API: {e}")
    logger.warning("Continuando sin cliente API funcional")
    api_client = None
    reservation_repo = None
    unit_repo = None
    work_order_repo = None
    reservation_service = None
    unit_service = None
    work_order_service = None


# Función helper para verificar cliente API
def check_api_client():
    """Verificar que el cliente API esté disponible"""
    if api_client is None:
        raise AuthenticationError(
            "Cliente API no está disponible. Verifique las credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD."
        )


# Server Lifespan para inicialización y limpieza ordenada
@asynccontextmanager
async def lifespan(server):
    """
    Maneja el ciclo de vida del servidor MCP.
    Se ejecuta una vez al inicio y al final del servidor.

    FastMCP 2.13+ feature: Server Lifespans
    """
    # ✅ INICIALIZACIÓN
    logger.info("=" * 60)
    logger.info("🚀 TrackHS MCP Server iniciando...")
    logger.info("=" * 60)
    logger.info(f"📍 Base URL: {API_BASE_URL}")
    logger.info(f"👤 Username: {API_USERNAME if API_USERNAME else 'No configurado'}")

    # Verificar conexión API al inicio
    if api_client:
        try:
            start = time.time()
            api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
            duration = time.time() - start
            logger.info(f"✅ API TrackHS conectada ({duration:.2f}s)")
        except Exception as e:
            logger.error(f"❌ API TrackHS no disponible: {e}")
            logger.warning(
                "⚠️  El servidor iniciará pero las herramientas fallarán sin conectividad"
            )
    else:
        logger.warning("⚠️  Credenciales no configuradas")
        logger.warning("   Configure TRACKHS_USERNAME y TRACKHS_PASSWORD")

    logger.info("✅ Servidor listo para recibir requests")
    logger.info("=" * 60)

    yield  # ✅ Servidor corriendo

    # ✅ LIMPIEZA
    logger.info("=" * 60)
    logger.info("🛑 TrackHS MCP Server cerrando...")
    if api_client and hasattr(api_client, "client"):
        try:
            api_client.client.close()
            logger.info("✅ Conexiones HTTP cerradas correctamente")
        except Exception as e:
            logger.warning(f"⚠️  Error cerrando conexiones: {e}")
    logger.info("👋 Servidor cerrado")
    logger.info("=" * 60)


# Crear servidor MCP con validación estricta y características de FastMCP 2.13
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
    strict_input_validation=True,  # ✅ Validación estricta Pydantic
    mask_error_details=True,  # ✅ Seguridad: ocultar errores internos en producción
    lifespan=lifespan,  # ✅ FastMCP 2.13: Server Lifespan
)

# ✅ Registrar middleware nativo de FastMCP 2.9+
try:
    from fastmcp.server.middleware.error_handling import (
        ErrorHandlingMiddleware,
        RetryMiddleware,
    )

    # Error handling con traceback para debugging
    mcp.add_middleware(
        ErrorHandlingMiddleware(
            include_traceback=True,
            transform_errors=True,
        )
    )
    logger.info("✅ ErrorHandlingMiddleware registrado")

    # Reintentos automáticos con backoff exponencial (built-in)
    mcp.add_middleware(
        RetryMiddleware(
            max_retries=settings.max_retries,
            retry_exceptions=(httpx.RequestError, httpx.HTTPStatusError),
        )
    )
    logger.info(f"✅ RetryMiddleware registrado (max_retries={settings.max_retries})")

except ImportError as e:
    logger.warning(f"⚠️  Middleware nativo de FastMCP no disponible: {e}")
    logger.warning("   Continuando sin ErrorHandlingMiddleware y RetryMiddleware")

# ✅ Middleware personalizado nativo FastMCP
# 1. Logging middleware
logging_middleware = TrackHSLoggingMiddleware()
mcp.add_middleware(logging_middleware)
logger.info("✅ TrackHSLoggingMiddleware registrado")

# 2. Auth middleware
auth_middleware = TrackHSAuthMiddleware(api_client=api_client)
mcp.add_middleware(auth_middleware)
logger.info("✅ TrackHSAuthMiddleware registrado")

# 3. Metrics middleware
metrics_middleware = TrackHSMetricsMiddleware()
mcp.add_middleware(metrics_middleware)
logger.info("✅ TrackHSMetricsMiddleware registrado")

# 4. Rate limiting middleware (opcional)
if settings.metrics_enabled:
    rate_limit_middleware = TrackHSRateLimitMiddleware(
        requests_per_minute=60, burst_size=10
    )
    mcp.add_middleware(rate_limit_middleware)
    logger.info("✅ TrackHSRateLimitMiddleware registrado")

logger.info("=" * 60)
logger.info("✅ Todos los middleware nativos registrados correctamente")
logger.info("=" * 60)


@mcp.tool(output_schema=RESERVATION_SEARCH_OUTPUT_SCHEMA)
def search_reservations(
    page: Annotated[
        int,
        Field(
            ge=1,
            le=10000,
            description="Número de página (1-based). Límite máximo: 10000 páginas",
        ),
    ] = 1,
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
    # ✅ Middleware se aplica automáticamente (logging, auth, métricas, reintentos)

    # Verificar que el servicio esté disponible
    if reservation_service is None:
        raise AuthenticationError(
            "Servicio de reservas no disponible. Verifique las credenciales."
        )

    # Usar servicio de negocio para búsqueda
    result = reservation_service.search_reservations(
        page=page,
        size=size,
        search=search,
        arrival_start=arrival_start,
        arrival_end=arrival_end,
        status=status,
    )

    return result


@mcp.tool(output_schema=RESERVATION_DETAIL_OUTPUT_SCHEMA)
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
    try:
        # Verificar que el servicio esté disponible
        if reservation_service is None:
            raise AuthenticationError(
                "Servicio de reservas no disponible. Verifique las credenciales."
            )

        # Usar servicio de negocio para obtener reserva
        result = reservation_service.get_reservation_by_id(reservation_id)

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, ReservationResponse, strict=False)

        return validated_result

    except NotFoundError:
        # ✅ ToolError: Mensaje claro para el cliente (siempre se muestra)
        raise ToolError(
            f"Reserva {reservation_id} no encontrada en TrackHS. "
            f"Verifique el ID e intente nuevamente."
        )
    except AuthenticationError as e:
        # ✅ ToolError para errores resolubles por el usuario
        raise ToolError(
            f"Error de autenticación: {str(e)}. "
            f"Contacte al administrador del sistema."
        )
    except Exception as e:
        # ⚠️ Exception genérica: detalles ocultos con mask_error_details=True
        # El cliente solo verá: "Error interno del servidor"
        logger.error(f"Error obteniendo reserva {reservation_id}: {str(e)}")
        raise


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
        Optional[int],
        Field(ge=0, le=20, description="Número exacto de dormitorios"),
    ] = None,
    bathrooms: Annotated[
        Optional[int],
        Field(ge=0, le=20, description="Número exacto de baños"),
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
    - search_units(is_active=True, is_bookable=True) # Unidades activas y disponibles
    - search_units(search="penthouse") # Buscar por nombre o descripción
    """
    # ✅ Middleware se aplica automáticamente (logging, auth, métricas, reintentos)

    # Los parámetros ya están validados por FastMCP como int

    # Verificar que el servicio esté disponible
    if unit_service is None:
        raise AuthenticationError(
            "Servicio de unidades no disponible. Verifique las credenciales."
        )

    # Usar servicio de negocio para búsqueda
    result = unit_service.search_units(
        page=page,
        size=size,
        search=search,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        is_active=is_active,
        is_bookable=is_bookable,
    )

    return result


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

    Las amenidades son características o servicios que pueden tener las unidades
    (ej: WiFi, piscina, aire acondicionado, estacionamiento, etc.)

    Respuesta incluye:
    - id: Identificador único de la amenidad
    - name: Nombre descriptivo de la amenidad
    - group: Grupo/categoría a la que pertenece
    - isPublic: Si es visible públicamente
    - isFilterable: Si se puede usar como filtro de búsqueda
    - description: Descripción detallada de la amenidad
    - homeawayType, airbnbType, marriottType: Mapeos para plataformas OTA

    Útil para:
    - Conocer amenidades disponibles en unidades
    - Filtrar unidades por amenidades específicas
    - Configuración de filtros de búsqueda
    - Catálogo de servicios disponibles
    - Verificar qué amenidades tiene una unidad
    - Integración con plataformas OTA (Airbnb, HomeAway, Marriott)

    Ejemplos de uso:
    - search_amenities(search="wifi") # Buscar amenidades relacionadas con WiFi
    - search_amenities(size=50) # Obtener catálogo completo de amenidades
    - search_amenities(search="pool") # Buscar amenidades de piscina
    """
    # Verificar que el servicio esté disponible
    if unit_service is None:
        raise AuthenticationError(
            "Servicio de unidades no disponible. Verifique las credenciales."
        )

    # Usar servicio de negocio para búsqueda de amenidades
    return unit_service.search_amenities(page=page, size=size, search=search)


@mcp.tool(output_schema=FOLIO_DETAIL_OUTPUT_SCHEMA)
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
    try:
        # Verificar que el servicio esté disponible
        if reservation_service is None:
            raise AuthenticationError(
                "Servicio de reservas no disponible. Verifique las credenciales."
            )

        # Usar servicio de negocio para obtener folio
        result = reservation_service.get_folio(reservation_id)

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, FolioResponse, strict=False)

        return validated_result

    except NotFoundError:
        # ✅ ToolError: Mensaje claro para el cliente
        raise ToolError(
            f"Folio para reserva {reservation_id} no encontrado. "
            f"Verifique que la reserva existe."
        )
    except AuthenticationError as e:
        raise ToolError(f"Error de autenticación: {str(e)}")
    except Exception as e:
        logger.error(f"Error obteniendo folio de reserva {reservation_id}: {str(e)}")
        raise


@mcp.tool(output_schema=WORK_ORDER_DETAIL_OUTPUT_SCHEMA)
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
        Optional[float],
        Field(ge=0, description="Costo estimado en moneda local"),
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

    # Los parámetros ya están validados por FastMCP

    # Verificar que el servicio esté disponible
    if work_order_service is None:
        raise AuthenticationError(
            "Servicio de work orders no disponible. Verifique las credenciales."
        )

    try:
        # Usar servicio de negocio para crear work order
        result = work_order_service.create_maintenance_work_order(
            unit_id=unit_id,
            summary=summary,
            description=description,
            priority=priority,
            estimated_cost=estimated_cost,
            estimated_time=estimated_time,
            date_received=date_received,
        )

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, WorkOrderResponse, strict=False)

        return validated_result
    except Exception as e:
        logger.error(f"Error creando orden de mantenimiento: {str(e)}")
        raise


@mcp.tool(output_schema=WORK_ORDER_DETAIL_OUTPUT_SCHEMA)
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
            gt=0,
            description="ID del tipo de limpieza (requerido si no es inspección). Tipos disponibles: 3=Inspection, 4=Departure Clean, 5=Deep Clean, 6=Pre-Arrival Inspection, 7=Refresh Clean, 8=Carpet Cleaning, 9=Guest Request, 10=Pack and Play",
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

    # Los parámetros ya están validados por FastMCP

    # Verificar que el servicio esté disponible
    if work_order_service is None:
        raise AuthenticationError(
            "Servicio de work orders no disponible. Verifique las credenciales."
        )

    try:
        # Usar servicio de negocio para crear work order
        result = work_order_service.create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=scheduled_at,
            is_inspection=is_inspection,
            clean_type_id=clean_type_id,
            comments=comments,
            cost=cost,
        )

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, WorkOrderResponse, strict=False)

        return validated_result
    except ValueError:
        # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Error creando orden de housekeeping: {str(e)}")
        raise


# Endpoint de métricas Prometheus
@mcp.resource("https://trackhs-mcp.local/metrics")
def prometheus_metrics() -> str:
    """
    Endpoint de métricas en formato Prometheus.

    Retorna métricas del servidor en formato compatible con Prometheus
    para monitoreo y alertas.

    Returns:
        Métricas en formato Prometheus
    """
    try:
        metrics = get_metrics()
        return metrics.export_prometheus_format()
    except Exception as e:
        logger.error(f"Error generando métricas Prometheus: {str(e)}")
        return f"# ERROR: {str(e)}"


# Health check endpoint con métricas dinámicas
@mcp.resource("https://trackhs-mcp.local/health")
def health_check() -> str:
    """
    Health check endpoint para monitoreo del servidor.

    Retorna estado del servidor, dependencias, métricas y versiones.

    Returns:
        JSON string con información completa del estado del servidor
    """
    try:
        # Verificar conexión con API TrackHS
        api_status = "healthy"
        api_response_time = None

        if api_client:
            try:
                start_time = time.time()
                api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
                api_response_time = round((time.time() - start_time) * 1000, 2)
            except Exception as e:
                api_status = "unhealthy"
                logger.warning(f"API TrackHS no disponible: {str(e)}")
        else:
            api_status = "not_configured"

        # Obtener métricas del middleware
        middleware_metrics = (
            metrics_middleware.get_metrics()
            if "metrics_middleware" in locals()
            else {"note": "Middleware metrics not available"}
        )

        # Obtener métricas del cache
        cache_metrics = get_cache().get_metrics()

        # Obtener métricas avanzadas
        advanced_metrics = get_metrics().get_metrics_summary()

        # Obtener versión de FastMCP dinámicamente
        try:
            import fastmcp

            fastmcp_version = fastmcp.__version__
        except Exception:
            fastmcp_version = "2.13.0"  # fallback

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
                    "base_url": API_BASE_URL,
                    "credentials_configured": API_USERNAME is not None
                    and API_PASSWORD is not None,
                }
            },
            "metrics": {
                "middleware": middleware_metrics,
                "cache": cache_metrics,
                "advanced": advanced_metrics,
            },
            "environment": {
                "python_version": sys.version,
                "fastmcp_version": fastmcp_version,
                "platform": sys.platform,
            },
        }

        logger.debug(f"Health check: {health_data['status']}")

        # ✅ Retornar diccionario (FastMCP maneja la serialización)
        return health_data

    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        error_data = {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }
        return error_data


# Configuración HTTP manejada por FastMCP Cloud
if __name__ == "__main__":
    logger.info("Iniciando servidor TrackHS MCP")
    # FastMCP Cloud maneja automáticamente la configuración HTTP
    mcp.run()
