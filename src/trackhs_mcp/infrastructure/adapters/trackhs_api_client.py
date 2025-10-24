"""
Cliente HTTP para Track HS API usando httpx
Implementa el puerto ApiClientPort
"""

import asyncio
from typing import Any, Dict, Optional, TypeVar

import httpx

from ...application.ports.api_client_port import ApiClientPort
from ...domain.exceptions.api_exceptions import (
    ApiError,
    AuthenticationError,
    NetworkError,
    TimeoutError,
)
from ...domain.value_objects.config import TrackHSConfig
from ...domain.value_objects.request import RequestOptions
from ..utils.auth import TrackHSAuth
from ..utils.error_handling import error_handler

T = TypeVar("T")


class TrackHSApiClient(ApiClientPort):
    """Cliente HTTP asíncrono para Track HS API"""

    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.auth = TrackHSAuth(config)

        if not self.auth.validate_credentials():
            raise ValueError("Credenciales de Track HS no configuradas correctamente")

        # Configurar cliente httpx con timeouts específicos
        timeout_config = httpx.Timeout(
            connect=10.0,  # Timeout para establecer conexión
            read=config.timeout
            or 60.0,  # Timeout para leer respuesta (aumentado para búsquedas complejas)
            write=10.0,  # Timeout para escribir datos
            pool=5.0,  # Timeout para obtener conexión del pool
        )

        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=timeout_config,
            limits=httpx.Limits(
                max_keepalive_connections=20, max_connections=100, keepalive_expiry=30.0
            ),
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

    async def search_request(
        self,
        endpoint: str,
        options: Optional[RequestOptions] = None,
        max_retries: int = 3,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Realiza una petición con timeout extendido para búsquedas complejas
        """
        # Crear timeout específico para búsquedas
        search_timeout = httpx.Timeout(
            connect=10.0, read=self.config.search_timeout or 120.0, write=10.0, pool=5.0
        )

        # Usar el método request normal pero con timeout personalizado
        return await self._request_with_timeout(
            endpoint, options, max_retries, params, search_timeout
        )

    async def _request_with_timeout(
        self,
        endpoint: str,
        options: Optional[RequestOptions] = None,
        max_retries: int = 3,
        params: Optional[Dict[str, Any]] = None,
        custom_timeout: Optional[httpx.Timeout] = None,
    ) -> Any:
        """
        Realiza una petición con timeout personalizado
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

                # Usar timeout personalizado si se proporciona
                if custom_timeout:
                    request_kwargs["timeout"] = custom_timeout

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

                # Asegurar que response no sea una corrutina
                if hasattr(response, "__await__"):
                    response = await response

                # Verificar si la respuesta es exitosa
                if response.status_code >= 200 and response.status_code < 300:
                    # Procesar respuesta JSON
                    try:
                        return response.json()
                    except Exception as json_error:
                        # Si falla el parsing JSON, intentar parsear manualmente
                        import json
                        import os

                        response_text = response.text
                        if os.getenv("DEBUG", "false").lower() == "true":
                            logger = logging.getLogger(__name__)
                            logger.debug(f"JSON parsing failed: {json_error}")
                            logger.debug(
                                f"Response text (first 500 chars): {response_text[:500]}"
                            )

                        # Intentar parsear manualmente
                        try:
                            json_data = json.loads(response_text)
                            return json_data
                        except Exception as manual_parse_error:
                            if os.getenv("DEBUG", "false").lower() == "true":
                                logger = logging.getLogger(__name__)
                                logger.debug(
                                    f"Manual JSON parsing also failed: {manual_parse_error}"
                                )
                                logger.debug(
                                    f"Response text (first 500 chars): {response_text[:500]}"
                                )

                            # Si todo falla, lanzar error en lugar de devolver string
                            raise ApiError(
                                f"Failed to parse JSON response: {manual_parse_error}",
                                response.status_code,
                                endpoint,
                            )
                else:
                    # Para contenido no-JSON, intentar parsear como JSON de todas formas
                    try:
                        response_text = response.text
                        json_data = json.loads(response_text)
                        return json_data
                    except Exception:
                        # Si no es JSON válido, devolver el texto
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
        last_error: Optional[Exception] = None

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

                # Asegurar que response no sea una corrutina
                if hasattr(response, "__await__"):
                    response = await response

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
                    elif response.status_code == 400 or response.status_code == 422:
                        # Agregar log detallado del body de error
                        error_body = response.text
                        logger = logging.getLogger(__name__)
                        status_label = (
                            "400 Bad Request"
                            if response.status_code == 400
                            else "422 Unprocessable Entity"
                        )
                        logger.error(f"{status_label} - URL: {endpoint}")
                        logger.error(
                            f"{status_label} - Full URL: {self.client.base_url}{endpoint}"
                        )
                        logger.error(f"{status_label} - Method: {method}")
                        logger.error(f"{status_label} - Headers: {headers}")
                        logger.error(
                            f"{status_label} - Body: {request_kwargs.get('data')}"
                        )
                        logger.error(
                            f"{status_label} - Params: {request_kwargs.get('params')}"
                        )
                        logger.error(
                            f"{status_label} - Response Status: {response.status_code}"
                        )
                        logger.error(
                            f"{status_label} - Response Headers: {dict(response.headers)}"
                        )
                        logger.error(f"{status_label} - Response Body: {error_body}")

                        # Intentar parsear el error como JSON si es posible
                        error_message = error_body
                        try:
                            import json

                            error_json = response.json()
                            logger.error(f"{status_label} - Parsed Error: {error_json}")
                            # Extraer mensajes de validación si existen
                            if isinstance(error_json, dict):
                                if "validation_messages" in error_json:
                                    error_message = f"{error_json.get('detail', error_body)} - Validation: {error_json['validation_messages']}"
                                elif "detail" in error_json:
                                    error_message = error_json["detail"]
                        except Exception:
                            logger.error(f"{status_label} - Raw Text: {error_body}")

                        raise ApiError(
                            error_message,
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
                    try:
                        # Intentar parsear como JSON
                        json_data = response.json()
                        return json_data
                    except Exception as json_error:
                        # Si falla el parsing JSON, intentar parsear manualmente
                        try:
                            response_text = response.text
                            if os.getenv("DEBUG", "false").lower() == "true":
                                logger = logging.getLogger(__name__)
                                logger.debug(
                                    f"JSON parsing failed, trying manual parse. "
                                    f"Error: {json_error}"
                                )
                                logger.debug(
                                    f"Response text (first 200 chars): "
                                    f"{response_text[:200]}"
                                )

                            json_data = json.loads(response_text)
                            return json_data
                        except Exception as manual_parse_error:
                            if os.getenv("DEBUG", "false").lower() == "true":
                                logger = logging.getLogger(__name__)
                                logger.debug(
                                    f"Manual JSON parsing also failed: "
                                    f"{manual_parse_error}"
                                )
                                logger.debug(
                                    f"Response text (first 500 chars): "
                                    f"{response_text[:500]}"
                                )

                            # Si todo falla, lanzar error en lugar de devolver string
                            raise ApiError(
                                f"Failed to parse JSON response: {manual_parse_error}",
                                response.status_code,
                                endpoint,
                            )
                else:
                    # Para contenido no-JSON, intentar parsear como JSON de todas formas
                    try:
                        response_text = response.text
                        json_data = json.loads(response_text)
                        return json_data
                    except Exception:
                        # Si no es JSON válido, devolver el texto
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

            # Agregar Content-Type para JSON
            if options.headers is None:
                options.headers = {}
            options.headers["Content-Type"] = "application/json"

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

    async def create_housekeeping_work_order(
        self, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crea una nueva orden de trabajo de housekeeping.

        Args:
            data: Datos de la orden de trabajo

        Returns:
            Respuesta de la API con la orden creada

        Raises:
            ApiError: Si ocurre un error en la API
            AuthenticationError: Si las credenciales son inválidas
            NetworkError: Si hay problemas de red
        """
        return await self.post("/api/pms/housekeeping/work-orders", data)
