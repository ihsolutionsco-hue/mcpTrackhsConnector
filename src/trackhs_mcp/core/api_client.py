"""
Cliente HTTP para Track HS API usando httpx
"""

import httpx
import asyncio
from typing import Any, Dict, Optional, TypeVar
from .auth import TrackHSAuth
from .types import TrackHSConfig, RequestOptions, TrackHSResponse
from .error_handling import (
    ApiError, AuthenticationError, NetworkError, TimeoutError,
    error_handler, validate_required_params
)

T = TypeVar('T')

class TrackHSApiClient:
    """Cliente HTTP asíncrono para Track HS API"""
    
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.auth = TrackHSAuth(config)
        
        if not self.auth.validate_credentials():
            raise ValueError("Credenciales de Track HS no configuradas correctamente")
        
        # Configurar cliente httpx
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout or 30,
            headers=self.auth.get_headers()
        )
    
    async def __aenter__(self):
        """Context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose()
    
    @error_handler("api_request")
    async def request(
        self, 
        endpoint: str, 
        options: Optional[RequestOptions] = None,
        max_retries: int = 3
    ) -> Any:
        """
        Realiza una petición HTTP a la API de Track HS con reintentos
        
        Args:
            endpoint: Endpoint de la API
            options: Opciones de la petición
            max_retries: Número máximo de reintentos
            
        Returns:
            Respuesta de la API
            
        Raises:
            ApiError: Si la petición falla después de todos los reintentos
        """
        url = f"{self.config.base_url}{endpoint}"
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                # Preparar opciones de la petición
                method = options.method if options else "GET"
                headers = self.auth.get_headers()
                
                if options and options.headers:
                    headers.update(options.headers)
                
                request_kwargs = {"headers": headers}
                
                if options and options.body:
                    request_kwargs["data"] = options.body
                
                # Realizar petición
                response = await self.client.request(method, url, **request_kwargs)
                
                # Verificar si la respuesta es exitosa
                if not response.is_success:
                    if response.status_code == 401:
                        raise AuthenticationError("Invalid credentials")
                    elif response.status_code == 403:
                        raise AuthenticationError("Access forbidden")
                    elif response.status_code == 404:
                        raise ApiError(f"Endpoint not found: {endpoint}", 404, endpoint)
                    elif response.status_code >= 500:
                        # Error del servidor, reintentar
                        if attempt < max_retries:
                            await asyncio.sleep(2 ** attempt)  # Backoff exponencial
                            continue
                        else:
                            raise ApiError(
                                f"Server error: {response.status_code} {response.reason_phrase}",
                                response.status_code,
                                endpoint
                            )
                    else:
                        raise ApiError(
                            f"API Error: {response.status_code} {response.reason_phrase}",
                            response.status_code,
                            endpoint
                        )
                
                # Determinar tipo de contenido
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    return response.json()
                else:
                    return response.text
                    
            except httpx.TimeoutException as e:
                last_error = TimeoutError(f"Request timeout: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise last_error
                    
            except httpx.ConnectError as e:
                last_error = NetworkError(f"Connection error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise last_error
                    
            except httpx.RequestError as e:
                last_error = NetworkError(f"Request error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise last_error
                    
            except (ApiError, AuthenticationError):
                # No reintentar errores de API o autenticación
                raise
                
            except Exception as e:
                last_error = ApiError(f"Unexpected error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise last_error
        
        # Si llegamos aquí, todos los reintentos fallaron
        if last_error:
            raise last_error
        else:
            raise ApiError("All retry attempts failed")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, options: Optional[RequestOptions] = None) -> Any:
        """Realiza una petición GET"""
        if options is None:
            options = RequestOptions(method="GET")
        else:
            options.method = "GET"
        
        # Agregar parámetros de consulta si se proporcionan
        if params:
            # Construir query string
            query_parts = []
            for key, value in params.items():
                if value is not None:
                    if isinstance(value, list):
                        for item in value:
                            query_parts.append(f"{key}={item}")
                    else:
                        query_parts.append(f"{key}={value}")
            
            if query_parts:
                query_string = "&".join(query_parts)
                if "?" in endpoint:
                    endpoint += f"&{query_string}"
                else:
                    endpoint += f"?{query_string}"
        
        return await self.request(endpoint, options)
    
    async def post(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOptions] = None
    ) -> Any:
        """Realiza una petición POST"""
        if options is None:
            options = RequestOptions(method="POST")
        else:
            options.method = "POST"
        
        if data is not None:
            import json
            options.body = json.dumps(data)
        
        return await self.request(endpoint, options)
