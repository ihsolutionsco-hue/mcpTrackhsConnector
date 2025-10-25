import httpx
from trackhs_mcp.config import settings
import logging
import time
import asyncio
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TrackHSAPIError(Exception):
    """Excepción personalizada para errores de la API TrackHS"""
    def __init__(self, message: str, status_code: Optional[int] = None, endpoint: Optional[str] = None):
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(message)

class TrackHSClient:
    def __init__(self):
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
