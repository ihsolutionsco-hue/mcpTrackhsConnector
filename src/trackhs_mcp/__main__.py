import os
import sys
import logging
import time
import asyncio
import httpx
from datetime import datetime, date
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

# Configurar logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class Settings(BaseModel):
    trackhs_api_url: str
    trackhs_username: str
    trackhs_password: str
    log_level: str = "INFO"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# Lazy loading de settings - solo se carga cuando se necesita
_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

# ============================================================================
# CLIENTE HTTP
# ============================================================================

class TrackHSAPIError(Exception):
    """Excepción personalizada para errores de la API TrackHS"""
    def __init__(self, message: str, status_code: Optional[int] = None, endpoint: Optional[str] = None):
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(message)

class TrackHSClient:
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.trackhs_api_url
        self.auth = (settings.trackhs_username, settings.trackhs_password)
        self.max_retries = 3
        self.retry_delay = 1.0
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Método interno para hacer requests con retry y logging detallado"""
        full_url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(
                        method=method,
                        url=full_url,
                        auth=self.auth,
                        timeout=30.0,
                        **kwargs
                    )
                    
                    duration = time.time() - start_time
                    
                    # Logging estructurado con contexto
                    logger.info(
                        "trackhs_api_request",
                        method=method,
                        endpoint=endpoint,
                        status_code=response.status_code,
                        duration_ms=round(duration * 1000, 2),
                        attempt=attempt + 1
                    )
                    
                    # Manejo específico de errores HTTP
                    if response.status_code == 401:
                        raise TrackHSAPIError(
                            "Autenticación fallida. Verificar credenciales.",
                            status_code=401,
                            endpoint=endpoint
                        )
                    elif response.status_code == 403:
                        raise TrackHSAPIError(
                            "Acceso denegado. Verificar permisos.",
                            status_code=403,
                            endpoint=endpoint
                        )
                    elif response.status_code == 404:
                        raise TrackHSAPIError(
                            "Recurso no encontrado.",
                            status_code=404,
                            endpoint=endpoint
                        )
                    elif response.status_code >= 500:
                        if attempt < self.max_retries - 1:
                            logger.warning(
                                "trackhs_api_retry",
                                status_code=response.status_code,
                                attempt=attempt + 1,
                                next_retry_in=self.retry_delay * (2 ** attempt)
                            )
                            await asyncio.sleep(self.retry_delay * (2 ** attempt))
                            continue
                        else:
                            raise TrackHSAPIError(
                                f"Error del servidor: {response.status_code}",
                                status_code=response.status_code,
                                endpoint=endpoint
                            )
                    
                    response.raise_for_status()
                    return response.json()
                    
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    logger.warning(
                        "trackhs_api_timeout_retry",
                        attempt=attempt + 1,
                        next_retry_in=self.retry_delay * (2 ** attempt)
                    )
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                else:
                    raise TrackHSAPIError(
                        "Timeout en la conexión con TrackHS API",
                        endpoint=endpoint
                    )
            except httpx.ConnectError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(
                        "trackhs_api_connection_retry",
                        error=str(e),
                        attempt=attempt + 1,
                        next_retry_in=self.retry_delay * (2 ** attempt)
                    )
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                else:
                    raise TrackHSAPIError(
                        f"Error de conexión: {str(e)}",
                        endpoint=endpoint
                    )
            except Exception as e:
                logger.error(
                    "trackhs_api_error",
                    method=method,
                    endpoint=endpoint,
                    error=str(e),
                    attempt=attempt + 1
                )
                raise TrackHSAPIError(
                    f"Error inesperado: {str(e)}",
                    endpoint=endpoint
                )
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """GET request a TrackHS API con retry automático"""
        return await self._make_request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, json: Dict[str, Any]) -> dict:
        """POST request a TrackHS API con retry automático"""
        return await self._make_request("POST", endpoint, json=json)

trackhs_client = TrackHSClient()

# ============================================================================
# SCHEMAS DE VALIDACIÓN
# ============================================================================

class SearchReservationsRequest(BaseModel):
    page: int = Field(default=0, ge=0, le=10000, description="Número de página (0-based)")
    size: int = Field(default=3, ge=1, le=100, description="Tamaño de página (1-100)")
    search: Optional[str] = Field(default=None, max_length=200, description="Búsqueda de texto completo")
    arrival_start: Optional[str] = Field(default=None, description="Fecha de llegada inicio (YYYY-MM-DD)")
    arrival_end: Optional[str] = Field(default=None, description="Fecha de llegada fin (YYYY-MM-DD)")
    status: Optional[str] = Field(default=None, description="Estado de reserva")
    
    @field_validator('arrival_start', 'arrival_end')
    @classmethod
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
        return v
    
    @field_validator('arrival_end')
    @classmethod
    def validate_date_range(cls, v, info):
        if v and 'arrival_start' in info.data and info.data['arrival_start']:
            start_date = datetime.strptime(info.data['arrival_start'], "%Y-%m-%d")
            end_date = datetime.strptime(v, "%Y-%m-%d")
            if end_date < start_date:
                raise ValueError("arrival_end debe ser posterior a arrival_start")
        return v

class GetReservationRequest(BaseModel):
    reservation_id: str = Field(description="ID de reserva")
    
    @field_validator('reservation_id')
    @classmethod
    def validate_reservation_id(cls, v):
        if not v.isdigit():
            raise ValueError("ID de reserva debe ser numérico")
        if len(v) > 20:
            raise ValueError("ID de reserva demasiado largo")
        return v

class SearchUnitsRequest(BaseModel):
    page: int = Field(default=1, ge=1, le=400, description="Número de página")
    size: int = Field(default=2, ge=1, le=25, description="Tamaño de página")
    search: Optional[str] = Field(default=None, max_length=200, description="Búsqueda de texto")
    bedrooms: Optional[str] = Field(default=None, description="Número de dormitorios")
    bathrooms: Optional[str] = Field(default=None, description="Número de baños")
    
    @field_validator('bedrooms', 'bathrooms')
    @classmethod
    def validate_numeric_fields(cls, v):
        if v is not None:
            try:
                num = int(v)
                if num < 0 or num > 20:
                    raise ValueError("Valor fuera del rango válido (0-20)")
            except ValueError:
                raise ValueError("Debe ser un número válido")
        return v
    
    @field_validator('bedrooms')
    @classmethod
    def validate_bedrooms_logic(cls, v, info):
        if v is not None and 'bathrooms' in info.data and info.data['bathrooms'] is not None:
            bedrooms = int(v)
            bathrooms = int(info.data['bathrooms'])
            if bedrooms > 0 and bathrooms == 0:
                raise ValueError("Unidades con dormitorios deben tener al menos 1 baño")
        return v

# ============================================================================
# TOOLS
# ============================================================================

@mcp.tool
async def search_reservations(request: SearchReservationsRequest) -> dict:
    """
    Buscar reservas en TrackHS con filtros avanzados.
    
    Permite buscar reservas por fechas, estado, texto libre y otros criterios.
    Incluye paginación y ordenamiento.
    """
    start_time = time.time()
    
    try:
        # Construir parámetros de consulta
        params = {
            "page": request.page,
            "size": request.size,
        }
        
        if request.search:
            params["search"] = request.search
        if request.arrival_start:
            params["arrivalStart"] = request.arrival_start
        if request.arrival_end:
            params["arrivalEnd"] = request.arrival_end
        if request.status:
            params["status"] = request.status
        
        # Llamada a la API
        result = await trackhs_client.get("/api/v2/reservations", params=params)
        
        duration = time.time() - start_time
        
        # Logging estructurado con contexto
        logger.info(
            "search_reservations_success",
            duration_ms=round(duration * 1000, 2),
            result_count=len(result.get("data", [])),
            filters_applied={
                "search": bool(request.search),
                "arrival_start": bool(request.arrival_start),
                "arrival_end": bool(request.arrival_end),
                "status": bool(request.status)
            }
        )
        
        return result
        
    except TrackHSAPIError as e:
        duration = time.time() - start_time
        logger.error(
            "search_reservations_api_error",
            error_type="TrackHSAPIError",
            status_code=e.status_code,
            endpoint=e.endpoint,
            duration_ms=round(duration * 1000, 2)
        )
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "search_reservations_error",
            error_type=type(e).__name__,
            error=str(e),
            duration_ms=round(duration * 1000, 2)
        )
        raise

@mcp.tool
async def get_reservation(request: GetReservationRequest) -> dict:
    """
    Obtener detalles completos de una reserva específica.
    
    Incluye información del huésped, fechas, precios, políticas y más.
    """
    start_time = time.time()
    
    try:
        result = await trackhs_client.get(f"/api/v2/reservations/{request.reservation_id}")
        
        duration = time.time() - start_time
        
        # Logging estructurado con contexto
        logger.info(
            "get_reservation_success",
            reservation_id=request.reservation_id,
            duration_ms=round(duration * 1000, 2),
            has_guest_info=bool(result.get("guest")),
            has_balance=bool(result.get("balance"))
        )
        
        return result
        
    except TrackHSAPIError as e:
        duration = time.time() - start_time
        logger.error(
            "get_reservation_api_error",
            reservation_id=request.reservation_id,
            error_type="TrackHSAPIError",
            status_code=e.status_code,
            endpoint=e.endpoint,
            duration_ms=round(duration * 1000, 2)
        )
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "get_reservation_error",
            reservation_id=request.reservation_id,
            error_type=type(e).__name__,
            error=str(e),
            duration_ms=round(duration * 1000, 2)
        )
        raise

@mcp.tool
async def search_units(request: SearchUnitsRequest) -> dict:
    """
    Buscar unidades disponibles en TrackHS.
    
    Permite filtrar por características como dormitorios, baños, amenidades, etc.
    """
    start_time = time.time()
    
    try:
        # Construir parámetros de consulta
        params = {
            "page": request.page,
            "size": request.size,
        }
        
        if request.search:
            params["search"] = request.search
        if request.bedrooms:
            params["bedrooms"] = request.bedrooms
        if request.bathrooms:
            params["bathrooms"] = request.bathrooms
        
        # Llamada a la API
        result = await trackhs_client.get("/api/v2/units", params=params)
        
        duration = time.time() - start_time
        
        # Logging estructurado con contexto
        logger.info(
            "search_units_success",
            duration_ms=round(duration * 1000, 2),
            result_count=len(result.get("data", [])),
            filters_applied={
                "search": bool(request.search),
                "bedrooms": bool(request.bedrooms),
                "bathrooms": bool(request.bathrooms)
            }
        )
        
        return result
        
    except TrackHSAPIError as e:
        duration = time.time() - start_time
        logger.error(
            "search_units_api_error",
            error_type="TrackHSAPIError",
            status_code=e.status_code,
            endpoint=e.endpoint,
            duration_ms=round(duration * 1000, 2)
        )
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "search_units_error",
            error_type=type(e).__name__,
            error=str(e),
            duration_ms=round(duration * 1000, 2)
        )
        raise

# ============================================================================
# SERVIDOR FASTMCP
# ============================================================================

# Crear servidor FastMCP
mcp = FastMCP("TrackHS Hotel MCP")

# Middleware mínimo
mcp.add_middleware(LoggingMiddleware(include_payloads=True))
mcp.add_middleware(ErrorHandlingMiddleware(transform_errors=True))

logger.info("TrackHS MCP Server initialized successfully")

if __name__ == "__main__":
    mcp.run()