"""
TrackHS HTTP Client - Simple httpx-based client
Reemplaza el Repository Layer con cliente HTTP directo
"""

import logging
from typing import Any, Dict, Optional

import httpx
from fastmcp.exceptions import ToolError

logger = logging.getLogger(__name__)


class TrackHSClient:
    """
    Cliente HTTP simple para TrackHS API usando httpx.

    Reemplaza la complejidad del Repository Layer con llamadas HTTP directas.
    """

    def __init__(
        self, base_url: str, username: str, password: str, timeout: float = 30.0
    ):
        """
        Inicializar cliente HTTP.

        Args:
            base_url: URL base de la API TrackHS
            username: Usuario de autenticación
            password: Contraseña de autenticación
            timeout: Timeout en segundos
        """
        self.base_url = base_url.rstrip("/")
        self.auth = (username, password)
        self.timeout = timeout

        # Cliente HTTP con configuración
        self.client = httpx.Client(
            auth=self.auth,
            timeout=timeout,
            headers={
                "User-Agent": "TrackHS-MCP-Client/2.0.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        logger.info(f"TrackHSClient inicializado para {base_url}")

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realizar GET request a la API TrackHS.

        Args:
            endpoint: Endpoint relativo (ej: "api/pms/reservations")
            params: Parámetros de query string

        Returns:
            Respuesta JSON de la API

        Raises:
            ToolError: Si hay error HTTP o de conexión
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.debug(f"GET {url} con params: {params}")

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Respuesta exitosa: {len(str(data))} caracteres")

            return data

        except httpx.HTTPStatusError as e:
            error_msg = self._handle_http_error(e, url)
            raise ToolError(error_msg)

        except httpx.RequestError as e:
            error_msg = f"Error de conexión con TrackHS: {str(e)}"
            logger.error(error_msg)
            raise ToolError(error_msg)

        except Exception as e:
            error_msg = f"Error inesperado en GET {url}: {str(e)}"
            logger.error(error_msg)
            raise ToolError(error_msg)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realizar POST request a la API TrackHS.

        Args:
            endpoint: Endpoint relativo (ej: "api/pms/work-orders")
            data: Datos JSON a enviar

        Returns:
            Respuesta JSON de la API

        Raises:
            ToolError: Si hay error HTTP o de conexión
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.debug(f"POST {url} con data: {data}")

        try:
            response = self.client.post(url, json=data)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Respuesta exitosa: {len(str(data))} caracteres")

            return data

        except httpx.HTTPStatusError as e:
            error_msg = self._handle_http_error(e, url)
            raise ToolError(error_msg)

        except httpx.RequestError as e:
            error_msg = f"Error de conexión con TrackHS: {str(e)}"
            logger.error(error_msg)
            raise ToolError(error_msg)

        except Exception as e:
            error_msg = f"Error inesperado en POST {url}: {str(e)}"
            logger.error(error_msg)
            raise ToolError(error_msg)

    def _handle_http_error(self, error: httpx.HTTPStatusError, url: str) -> str:
        """
        Manejar errores HTTP y convertirlos a mensajes de ToolError.

        Args:
            error: Excepción HTTP
            url: URL que causó el error

        Returns:
            Mensaje de error para ToolError
        """
        status_code = error.response.status_code

        # Verificar si la respuesta es HTML (endpoint no encontrado)
        content_type = error.response.headers.get("content-type", "")
        if "text/html" in content_type:
            return f"Endpoint no encontrado: {url} (respuesta HTML)"

        # Mapear códigos de estado a mensajes específicos
        if status_code == 401:
            return "Error de autenticación: Credenciales inválidas"
        elif status_code == 403:
            return "Error de autorización: Acceso denegado"
        elif status_code == 404:
            return f"Recurso no encontrado: {url}"
        elif status_code == 422:
            return f"Error de validación: {error.response.text}"
        elif status_code >= 500:
            return f"Error del servidor TrackHS: {status_code}"
        else:
            return f"Error de API TrackHS: {status_code} - {error.response.text}"

    def close(self):
        """Cerrar el cliente HTTP."""
        if hasattr(self, "client"):
            self.client.close()
            logger.debug("Cliente HTTP cerrado")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
