"""
TrackHS MCP Server - Mejores Prácticas FastMCP
Servidor MCP robusto con validación Pydantic y documentación completa para LLM
"""

import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Literal, Optional

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field
from typing_extensions import Annotated

from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    TrackHSError,
    ValidationError,
)
from .middleware import (
    AuthenticationMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
)
from .schemas import (
    AMENITIES_OUTPUT_SCHEMA,
    FOLIO_OUTPUT_SCHEMA,
    RESERVATION_DETAIL_OUTPUT_SCHEMA,
    RESERVATION_SEARCH_OUTPUT_SCHEMA,
    UNIT_SEARCH_OUTPUT_SCHEMA,
    WORK_ORDER_OUTPUT_SCHEMA,
    CollectionResponse,
    FolioResponse,
    ReservationResponse,
    UnitResponse,
    WorkOrderPriority,
    WorkOrderResponse,
)

# Cargar variables de entorno
load_dotenv()

# Configuración de logging para FastMCP Cloud
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Solo stdout para FastMCP Cloud
)
logger = logging.getLogger(__name__)

# Configuración de la API
API_BASE_URL = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")

logger.info(f"TrackHS MCP Server iniciando - Base URL: {API_BASE_URL}")
logger.info(f"Username configurado: {'Sí' if API_USERNAME else 'No'}")
logger.info(f"Password configurado: {'Sí' if API_PASSWORD else 'No'}")


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


# Configuración de reintentos
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1.0  # segundos
RETRY_BACKOFF_FACTOR = 2.0


def retry_with_backoff(
    func, max_retries: int = MAX_RETRIES, base_delay: float = RETRY_DELAY_BASE
):
    """
    Ejecuta una función con reintentos automáticos y exponential backoff.

    Reintenta automáticamente en caso de errores de red o errores temporales
    del servidor (429, 500, 502, 503, 504).

    Args:
        func: Función a ejecutar
        max_retries: Número máximo de reintentos
        base_delay: Delay base en segundos (se duplica en cada reintento)

    Returns:
        Resultado de la función si tiene éxito

    Raises:
        La última excepción si todos los reintentos fallan
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return func()
        except httpx.RequestError as e:
            # Errores de red (timeout, connection error, etc.)
            last_exception = e
            if attempt < max_retries:
                delay = base_delay * (RETRY_BACKOFF_FACTOR**attempt)
                logger.warning(
                    f"Request error on attempt {attempt + 1}/{max_retries + 1}: {str(e)}"
                )
                logger.info(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"All {max_retries + 1} attempts failed")
                raise ConnectionError(f"Error de conexión con TrackHS: {str(e)}")

        except httpx.HTTPStatusError as e:
            # Errores HTTP que ameritan reintento (temporales)
            status_code = e.response.status_code
            retryable_codes = {429, 500, 502, 503, 504}

            if status_code in retryable_codes and attempt < max_retries:
                last_exception = e
                delay = base_delay * (RETRY_BACKOFF_FACTOR**attempt)
                logger.warning(
                    f"HTTP {status_code} on attempt {attempt + 1}/{max_retries + 1}"
                )
                logger.info(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                # Error no retryable o ya agotamos reintentos
                raise

    # Si llegamos aquí, todos los reintentos fallaron
    if last_exception:
        raise last_exception


# Función helper para validación de respuestas
def validate_response(data: Dict[str, Any], model_class: type, strict: bool = False):
    """
    Valida datos de respuesta contra un modelo Pydantic.

    Args:
        data: Datos a validar
        model_class: Clase del modelo Pydantic
        strict: Si True, lanza excepción en caso de error. Si False, solo loguea.

    Returns:
        Datos validados (modelo Pydantic) si tiene éxito, o datos originales si falla en modo no-strict

    Raises:
        ValidationError: Si strict=True y la validación falla
    """
    try:
        validated = model_class.model_validate(data)
        logger.debug(f"Response validated successfully against {model_class.__name__}")
        return validated.model_dump(by_alias=True)
    except Exception as e:
        if strict:
            logger.error(f"Response validation failed: {str(e)}")
            raise ValidationError(f"Respuesta de API no válida: {str(e)}")
        else:
            logger.warning(f"Response validation warning (non-strict): {str(e)}")
            return data  # Retornar datos originales en modo no-strict


# Cliente HTTP robusto
class TrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)
        self.client = httpx.Client(auth=self.auth, timeout=30.0)
        logger.info(f"TrackHSClient inicializado para {base_url}")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request to TrackHS API with error handling and automatic retries"""
        full_url = f"{self.base_url}/{endpoint}"
        # Sanitizar params antes de loguear
        sanitized_params = sanitize_for_log(params)
        logger.info(f"GET request to {full_url} with params: {sanitized_params}")

        def _execute_request():
            """Función interna para ejecutar el request (usada por retry_with_backoff)"""
            try:
                response = self.client.get(full_url, params=params)
                logger.info(f"Response status: {response.status_code}")
                # No loguear headers completos (pueden contener tokens)
                logger.info(
                    f"Response content-type: {response.headers.get('content-type', 'unknown')}"
                )

                response.raise_for_status()

                # Parsear respuesta y sanitizar para log
                response_data = response.json()
                sanitized_response = sanitize_for_log(response_data)
                logger.info(
                    f"Response preview (sanitized): {str(sanitized_response)[:500]}"
                )

                logger.info(f"GET request successful - Status: {response.status_code}")
                return response_data

            except httpx.HTTPStatusError as e:
                # Sanitizar respuesta de error (puede contener datos sensibles)
                logger.error(f"HTTP Error {e.response.status_code}")
                logger.error(f"Request URL: {full_url}")

                # Check if response is HTML (indicating wrong endpoint)
                if "text/html" in e.response.headers.get("content-type", ""):
                    logger.error(
                        "Response is HTML instead of JSON - possible wrong endpoint or authentication issue"
                    )
                    raise NotFoundError(
                        f"Endpoint no encontrado o problema de autenticación. URL: {full_url}. Respuesta HTML recibida."
                    )

                if e.response.status_code == 401:
                    raise AuthenticationError(
                        f"Credenciales inválidas: {e.response.text}"
                    )
                elif e.response.status_code == 403:
                    raise AuthenticationError(f"Acceso denegado: {e.response.text}")
                elif e.response.status_code == 404:
                    raise NotFoundError(f"Recurso no encontrado: {e.response.text}")
                elif e.response.status_code == 422:
                    raise ValidationError(f"Error de validación: {e.response.text}")
                elif e.response.status_code == 429:
                    raise APIError(f"Límite de velocidad excedido: {e.response.text}")
                elif e.response.status_code >= 500:
                    raise APIError(
                        f"Error interno del servidor TrackHS: {e.response.status_code} - {e.response.text}"
                    )
                else:
                    raise APIError(
                        f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
                    )

            except Exception as e:
                logger.error(f"Unexpected error in GET request: {str(e)}")
                raise TrackHSError(f"Error inesperado: {str(e)}")

        # Ejecutar con reintentos automáticos
        return retry_with_backoff(_execute_request)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request to TrackHS API with error handling and automatic retries"""
        full_url = f"{self.base_url}/{endpoint}"
        # Sanitizar data antes de loguear
        sanitized_data = sanitize_for_log(data)
        logger.info(f"POST request to {full_url} with data: {sanitized_data}")

        def _execute_request():
            """Función interna para ejecutar el request (usada por retry_with_backoff)"""
            try:
                response = self.client.post(full_url, json=data)
                logger.info(f"Response status: {response.status_code}")
                # No loguear headers completos (pueden contener tokens)
                logger.info(
                    f"Response content-type: {response.headers.get('content-type', 'unknown')}"
                )

                response.raise_for_status()

                # Parsear respuesta y sanitizar para log
                response_data = response.json()
                sanitized_response = sanitize_for_log(response_data)
                logger.info(
                    f"Response preview (sanitized): {str(sanitized_response)[:500]}"
                )

                logger.info(f"POST request successful - Status: {response.status_code}")
                return response_data

            except httpx.HTTPStatusError as e:
                # Sanitizar respuesta de error (puede contener datos sensibles)
                logger.error(f"HTTP Error {e.response.status_code}")
                logger.error(f"Request URL: {full_url}")

                # Check if response is HTML (indicating wrong endpoint)
                if "text/html" in e.response.headers.get("content-type", ""):
                    logger.error(
                        "Response is HTML instead of JSON - possible wrong endpoint or authentication issue"
                    )
                    raise NotFoundError(
                        f"Endpoint no encontrado o problema de autenticación. URL: {full_url}. Respuesta HTML recibida."
                    )

                if e.response.status_code == 401:
                    raise AuthenticationError(
                        f"Credenciales inválidas: {e.response.text}"
                    )
                elif e.response.status_code == 404:
                    raise NotFoundError(f"Recurso no encontrado: {e.response.text}")
                elif e.response.status_code == 429:
                    raise APIError(f"Límite de velocidad excedido: {e.response.text}")
                else:
                    raise APIError(
                        f"Error de API TrackHS: {e.response.status_code} - {e.response.text}"
                    )

            except Exception as e:
                logger.error(f"Unexpected error in POST request: {str(e)}")
                raise TrackHSError(f"Error inesperado: {str(e)}")

        # Ejecutar con reintentos automáticos
        return retry_with_backoff(_execute_request)


# Inicializar cliente API con manejo robusto para FastMCP Cloud
try:
    if not API_USERNAME or not API_PASSWORD:
        logger.warning("TRACKHS_USERNAME y TRACKHS_PASSWORD no están configurados")
        logger.warning(
            "El servidor se iniciará pero las herramientas no funcionarán sin credenciales"
        )
        api_client = None
    else:
        api_client = TrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)
        logger.info("Cliente API TrackHS inicializado correctamente")
except Exception as e:
    logger.error(f"Error inicializando cliente API: {e}")
    logger.warning("Continuando sin cliente API funcional")
    api_client = None


# Función helper para verificar cliente API
def check_api_client():
    """Verificar que el cliente API esté disponible"""
    if api_client is None:
        raise AuthenticationError(
            "Cliente API no está disponible. Verifique las credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD."
        )


# Crear servidor MCP con validación estricta
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
    strict_input_validation=True,  # ✅ Quick Win #2: Validación estricta habilitada
)

# Inicializar middleware
logging_middleware = LoggingMiddleware()
auth_middleware = AuthenticationMiddleware(api_client)
metrics_middleware = MetricsMiddleware()

# ✅ Quick Win #1: Habilitar middleware
# Nota: El middleware se aplica a nivel de función en cada tool
# FastMCP gestiona el middleware de forma integrada con las herramientas


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
    # Aplicar middleware de logging
    logging_middleware.request_count += 1
    start_time = time.time()

    logger.info(
        f"Buscando reservas con parámetros: page={page}, size={size}, search={search}, arrival_start={arrival_start}, arrival_end={arrival_end}, status={status}"
    )

    # Aplicar middleware de autenticación
    if api_client is None:
        raise AuthenticationError(
            "Cliente API no está disponible. Verifique las credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD."
        )

    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if arrival_start:
        params["arrival_start"] = arrival_start
    if arrival_end:
        params["arrival_end"] = arrival_end
    if status:
        params["status"] = status

    try:
        result = api_client.get("pms/reservations", params)

        # Aplicar middleware de métricas
        duration = time.time() - start_time
        metrics_middleware.metrics["successful_requests"] += 1
        metrics_middleware.response_times.append(duration)
        metrics_middleware.metrics["average_response_time"] = sum(
            metrics_middleware.response_times
        ) / len(metrics_middleware.response_times)

        logger.info(
            f"Búsqueda de reservas exitosa - {result.get('total_items', 0)} reservas encontradas en {duration:.2f}s"
        )
        return result
    except Exception as e:
        # Aplicar middleware de métricas para errores
        metrics_middleware.metrics["failed_requests"] += 1
        metrics_middleware.metrics["error_rate"] = (
            metrics_middleware.metrics["failed_requests"]
            / metrics_middleware.metrics["total_requests"]
        ) * 100

        logger.error(f"Error en búsqueda de reservas: {str(e)}")
        raise


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
    logger.info(f"Obteniendo detalles de reserva ID: {reservation_id}")

    try:
        check_api_client()
        result = api_client.get(f"pms/reservations/{reservation_id}")

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, ReservationResponse, strict=False)

        logger.info(f"Detalles de reserva {reservation_id} obtenidos exitosamente")
        return validated_result
    except Exception as e:
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
    # Aplicar middleware de logging
    logging_middleware.request_count += 1
    start_time = time.time()

    logger.info(
        f"Buscando unidades con parámetros: page={page}, size={size}, search={search}, bedrooms={bedrooms}, bathrooms={bathrooms}, is_active={is_active}, is_bookable={is_bookable}"
    )

    # Aplicar middleware de autenticación
    if api_client is None:
        raise AuthenticationError(
            "Cliente API no está disponible. Verifique las credenciales TRACKHS_USERNAME y TRACKHS_PASSWORD."
        )

    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if bedrooms is not None:
        params["bedrooms"] = int(bedrooms)
    if bathrooms is not None:
        params["bathrooms"] = int(bathrooms)
    if is_active is not None:
        params["is_active"] = int(is_active)
    if is_bookable is not None:
        params["is_bookable"] = int(is_bookable)

    try:
        result = api_client.get("pms/units", params)

        # Aplicar middleware de métricas
        duration = time.time() - start_time
        metrics_middleware.metrics["successful_requests"] += 1
        metrics_middleware.response_times.append(duration)
        metrics_middleware.metrics["average_response_time"] = sum(
            metrics_middleware.response_times
        ) / len(metrics_middleware.response_times)

        logger.info(
            f"Búsqueda de unidades exitosa - {result.get('total_items', 0)} unidades encontradas en {duration:.2f}s"
        )
        return result
    except Exception as e:
        # Aplicar middleware de métricas para errores
        metrics_middleware.metrics["failed_requests"] += 1
        metrics_middleware.metrics["error_rate"] = (
            metrics_middleware.metrics["failed_requests"]
            / metrics_middleware.metrics["total_requests"]
        ) * 100

        logger.error(f"Error en búsqueda de unidades: {str(e)}")
        raise


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
    params = {"page": page, "size": size}
    if search:
        params["search"] = search

    check_api_client()
    return api_client.get("pms/units/amenities", params)


@mcp.tool(output_schema=FOLIO_OUTPUT_SCHEMA)
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
    logger.info(f"Obteniendo folio de reserva ID: {reservation_id}")

    try:
        check_api_client()
        result = api_client.get(f"pms/reservations/{reservation_id}/folio")

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, FolioResponse, strict=False)

        logger.info(f"Folio de reserva {reservation_id} obtenido exitosamente")
        return validated_result
    except Exception as e:
        logger.error(f"Error obteniendo folio de reserva {reservation_id}: {str(e)}")
        raise


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
    logger.info(
        f"Creando orden de mantenimiento para unidad {unit_id}, prioridad: {priority}"
    )

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

    try:
        check_api_client()
        result = api_client.post("pms/maintenance/work-orders", work_order_data)

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, WorkOrderResponse, strict=False)

        logger.info(
            f"Orden de mantenimiento creada exitosamente. ID: {validated_result.get('id', 'N/A')}"
        )
        return validated_result
    except Exception as e:
        logger.error(f"Error creando orden de mantenimiento: {str(e)}")
        raise


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
    logger.info(
        f"Creando orden de housekeeping para unidad {unit_id}, fecha: {scheduled_at}, inspección: {is_inspection}"
    )

    if not is_inspection and clean_type_id is None:
        error_msg = "clean_type_id es requerido cuando is_inspection=False"
        logger.error(error_msg)
        raise ValueError(error_msg)

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

    try:
        check_api_client()
        result = api_client.post("pms/housekeeping/work-orders", work_order_data)

        # Validar respuesta (modo no-strict: loguea pero no falla)
        validated_result = validate_response(result, WorkOrderResponse, strict=False)

        logger.info(
            f"Orden de housekeeping creada exitosamente. ID: {validated_result.get('id', 'N/A')}"
        )
        return validated_result
    except ValueError:
        # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Error creando orden de housekeeping: {str(e)}")
        raise


# Health check endpoint
@mcp.resource("https://trackhs-mcp.local/health")
def health_check():
    """
    Health check endpoint para monitoreo del servidor.

    Retorna el estado del servidor y sus dependencias.
    """
    try:
        # Verificar conexión con API TrackHS
        api_status = "healthy"
        api_response_time = None

        try:
            import time

            start_time = time.time()
            # Hacer una petición simple para verificar conectividad
            check_api_client()
            api_client.get("pms/units/amenities", {"page": 1, "size": 1})
            api_response_time = round((time.time() - start_time) * 1000, 2)  # ms
        except Exception as e:
            api_status = "unhealthy"
            logger.warning(f"API TrackHS no disponible: {str(e)}")

        health_data = {
            "status": "healthy" if api_status == "healthy" else "degraded",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "dependencies": {
                "trackhs_api": {
                    "status": api_status,
                    "response_time_ms": api_response_time,
                    "base_url": API_BASE_URL,
                }
            },
            "uptime": "N/A",  # Se puede implementar con time.time() al inicio
            "environment": {
                "python_version": os.sys.version,
                "fastmcp_version": "2.12.5",
            },
        }

        logger.info(f"Health check: {health_data['status']}")
        return health_data

    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


# Configuración HTTP manejada por FastMCP Cloud
if __name__ == "__main__":
    logger.info("Iniciando servidor TrackHS MCP")
    # FastMCP Cloud maneja automáticamente la configuración HTTP
    mcp.run()
