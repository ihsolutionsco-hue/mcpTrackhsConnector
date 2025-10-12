"""
Cliente HTTP para Track HS API usando httpx
Implementa el puerto ApiClientPort
"""

import asyncio
from typing import Any, Dict, Optional, TypeVar

import httpx

from ...application.ports.api_client_port import ApiClientPort
from ...domain.value_objects.config import TrackHSConfig
from ...domain.value_objects.request import RequestOptions
from ..utils.auth import TrackHSAuth
from ..utils.error_handling import (
    ApiError,
    AuthenticationError,
    NetworkError,
    TimeoutError,
    error_handler,
)

T = TypeVar("T")


class TrackHSApiClient(ApiClientPort):
    """Cliente HTTP asíncrono para Track HS API"""

    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.auth = TrackHSAuth(config)

        if not self.auth.validate_credentials():
            raise ValueError("Credenciales de Track HS no configuradas correctamente")

        # Configurar cliente httpx
        self.client = httpx.AsyncClient(
            base_url=config.base_url, timeout=config.timeout or 30
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
        max_retries: int = 3,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Realiza una petición HTTP a la API de Track HS con reintentos

        Args:
            endpoint: Endpoint de la API
            options: Opciones de la petición
            max_retries: Número máximo de reintentos
            params: Parámetros de consulta para la petición

        Returns:
            Respuesta de la API

        Raises:
            ApiError: Si la petición falla después de todos los reintentos
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # Preparar opciones de la petición
                method = options.method if options else "GET"
                headers = self.auth.get_headers()

                if options and options.headers:
                    headers.update(options.headers)

                request_kwargs = {"headers": headers}

                # Agregar params a request_kwargs si existen
                if params:
                    request_kwargs["params"] = params

                if options and options.body:
                    request_kwargs["data"] = options.body

                # Logging de debug (solo en desarrollo)
                import logging
                import os

                if os.getenv("DEBUG", "false").lower() == "true":
                    logger = logging.getLogger(__name__)
                    logger.debug(f"API Request: {method} {endpoint}")
                    logger.debug(f"Params: {params}")
                    logger.debug(f"Full URL: {self.client.base_url}{endpoint}")

                # Realizar petición usando endpoint relativo
                response = await self.client.request(method, endpoint, **request_kwargs)

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
                            await asyncio.sleep(2**attempt)  # Backoff exponencial
                            continue
                        else:
                            raise ApiError(
                                f"Server error: {response.status_code} "
                                f"{response.reason_phrase}",
                                response.status_code,
                                endpoint,
                            )
                    else:
                        raise ApiError(
                            f"API Error: {response.status_code} "
                            f"{response.reason_phrase}",
                            response.status_code,
                            endpoint,
                        )

                # Determinar tipo de contenido
                content_type = response.headers.get("content-type", "")

                if "application/json" in content_type:
                    return response.json()
                else:
                    return response.text

            except httpx.TimeoutException as e:
                last_error = TimeoutError(f"Request timeout: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    raise last_error

            except httpx.ConnectError as e:
                last_error = NetworkError(f"Connection error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    raise last_error

            except httpx.RequestError as e:
                last_error = NetworkError(f"Request error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    raise last_error

            except (ApiError, AuthenticationError):
                # No reintentar errores de API o autenticación
                raise

            except Exception as e:
                last_error = ApiError(f"Unexpected error: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    raise last_error

        # Si llegamos aquí, todos los reintentos fallaron
        if last_error:
            raise last_error
        else:
            raise ApiError("All retry attempts failed")

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Realiza una petición GET"""
        if options is None:
            options = RequestOptions(method="GET")
        else:
            options.method = "GET"

        # Pasar params directamente a request() sin construcción manual
        return await self.request(endpoint, options, params=params)

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOptions] = None,
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

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Realiza una petición PUT"""
        if options is None:
            options = RequestOptions(method="PUT")
        else:
            options.method = "PUT"

        if data is not None:
            import json

            options.body = json.dumps(data)

        return await self.request(endpoint, options)

    async def delete(
        self,
        endpoint: str,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Realiza una petición DELETE"""
        if options is None:
            options = RequestOptions(method="DELETE")
        else:
            options.method = "DELETE"

        return await self.request(endpoint, options)
