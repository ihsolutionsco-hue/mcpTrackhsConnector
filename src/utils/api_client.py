"""
Cliente API para TrackHS con logging estructurado
"""

import time
from typing import Any, Dict, Optional

import httpx
from httpx import Response

from .exceptions import (
    TrackHSAPIError,
    TrackHSAuthenticationError,
    TrackHSAuthorizationError,
    TrackHSNotFoundError,
)
from .logger import get_logger


class TrackHSAPIClient:
    """Cliente API para TrackHS con logging estructurado"""

    def __init__(self, base_url: str, username: str, password: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout
        self.logger = get_logger(__name__)

        # Configurar cliente HTTP
        self.client = httpx.Client(
            base_url=self.base_url, auth=(username, password), timeout=timeout
        )

        self.logger.info(
            "TrackHSAPIClient inicializado",
            extra={"base_url": self.base_url, "username": username, "timeout": timeout},
        )

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición GET a la API

        Args:
            endpoint: Endpoint de la API
            params: Parámetros de consulta

        Returns:
            Respuesta de la API como diccionario

        Raises:
            TrackHSAPIError: Si hay error en la petición
        """
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición POST a la API

        Args:
            endpoint: Endpoint de la API
            data: Datos a enviar

        Returns:
            Respuesta de la API como diccionario

        Raises:
            TrackHSAPIError: Si hay error en la petición
        """
        return self._make_request("POST", endpoint, json=data)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición PUT a la API

        Args:
            endpoint: Endpoint de la API
            data: Datos a enviar

        Returns:
            Respuesta de la API como diccionario

        Raises:
            TrackHSAPIError: Si hay error en la petición
        """
        return self._make_request("PUT", endpoint, json=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Realiza una petición DELETE a la API

        Args:
            endpoint: Endpoint de la API

        Returns:
            Respuesta de la API como diccionario

        Raises:
            TrackHSAPIError: Si hay error en la petición
        """
        return self._make_request("DELETE", endpoint)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API

        Args:
            method: Método HTTP
            endpoint: Endpoint de la API
            params: Parámetros de consulta
            json: Datos JSON a enviar

        Returns:
            Respuesta de la API como diccionario

        Raises:
            TrackHSAPIError: Si hay error en la petición
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start_time = time.time()

        try:
            response: Response = self.client.request(
                method=method, url=endpoint, params=params, json=json
            )

            response_time = (time.time() - start_time) * 1000

            # Log de la llamada API
            self.logger.info(
                f"API Call: {method} {endpoint}",
                extra={
                    "method": method,
                    "endpoint": endpoint,
                    "url": url,
                    "status_code": response.status_code,
                    "response_time_ms": response_time,
                    "params": params,
                    "has_json_data": json is not None,
                },
            )

            # Manejar errores HTTP
            if response.status_code == 401:
                raise TrackHSAuthenticationError("Credenciales inválidas")
            elif response.status_code == 403:
                raise TrackHSAuthorizationError("Sin permisos para acceder al recurso")
            elif response.status_code == 404:
                raise TrackHSNotFoundError("Recurso", endpoint)
            elif not response.is_success:
                raise TrackHSAPIError(
                    f"Error HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code,
                    response_data={"text": response.text},
                )

            # Parsear respuesta JSON
            try:
                return response.json()
            except Exception as e:
                raise TrackHSAPIError(f"Error parseando respuesta JSON: {str(e)}")

        except httpx.RequestError as e:
            response_time = (time.time() - start_time) * 1000
            self.logger.error(
                f"Error de conexión: {method} {endpoint}",
                extra={
                    "method": method,
                    "endpoint": endpoint,
                    "url": url,
                    "error": str(e),
                    "response_time_ms": response_time,
                },
            )
            raise TrackHSAPIError(f"Error de conexión: {str(e)}")

        except TrackHSError:
            # Re-lanzar errores de TrackHS
            raise

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            self.logger.error(
                f"Error inesperado: {method} {endpoint}",
                extra={
                    "method": method,
                    "endpoint": endpoint,
                    "url": url,
                    "error": str(e),
                    "response_time_ms": response_time,
                },
            )
            raise TrackHSAPIError(f"Error inesperado: {str(e)}")

    def close(self) -> None:
        """Cierra el cliente HTTP"""
        self.client.close()
        self.logger.info("TrackHSAPIClient cerrado")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
