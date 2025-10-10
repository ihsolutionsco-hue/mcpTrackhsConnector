"""
Cliente HTTP para Track HS API usando httpx
"""

import httpx
from typing import Any, Dict, Optional, TypeVar
from .auth import TrackHSAuth
from .types import TrackHSConfig, RequestOptions, ApiError, TrackHSResponse

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
    
    async def request(
        self, 
        endpoint: str, 
        options: Optional[RequestOptions] = None
    ) -> Any:
        """
        Realiza una petición HTTP a la API de Track HS
        
        Args:
            endpoint: Endpoint de la API
            options: Opciones de la petición
            
        Returns:
            Respuesta de la API
            
        Raises:
            ApiError: Si la petición falla
        """
        url = f"{self.config.base_url}{endpoint}"
        
        try:
            # Preparar opciones de la petición
            request_kwargs = {
                "method": options.method if options else "GET",
                "headers": self.auth.get_headers()
            }
            
            if options and options.headers:
                request_kwargs["headers"].update(options.headers)
            
            if options and options.body:
                request_kwargs["data"] = options.body
            
            # Realizar petición
            response = await self.client.request(**request_kwargs)
            
            # Verificar si la respuesta es exitosa
            if not response.is_success:
                error_message = f"Track HS API Error: {response.status_code} {response.reason_phrase}"
                raise ApiError(
                    message=error_message,
                    status=response.status_code,
                    status_text=response.reason_phrase
                )
            
            # Determinar tipo de contenido
            content_type = response.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                return response.json()
            else:
                return response.text
                
        except httpx.RequestError as e:
            raise ApiError(f"Error en petición a Track HS: {str(e)}")
        except Exception as e:
            raise ApiError(f"Error desconocido en petición a Track HS: {str(e)}")
    
    async def get(self, endpoint: str, options: Optional[RequestOptions] = None) -> Any:
        """Realiza una petición GET"""
        if options is None:
            options = RequestOptions(method="GET")
        else:
            options.method = "GET"
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
