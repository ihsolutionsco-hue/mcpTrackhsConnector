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

    def search_units(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca unidades de alojamiento con filtros avanzados

        Args:
            params: Parámetros de búsqueda de unidades

        Returns:
            Respuesta de la API con unidades encontradas
        """
        # Convertir parámetros booleanos a enteros (1/0) según la API
        api_params = self._convert_boolean_params(params)

        # Realizar llamada a la API
        result = self.get("api/pms/units", api_params)

        # Procesar respuesta
        return self._process_units_response(result)

    def _convert_boolean_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte parámetros booleanos a enteros según la API TrackHS

        Args:
            params: Parámetros originales

        Returns:
            Parámetros convertidos
        """
        converted = {}
        boolean_fields = {
            "is_active",
            "is_bookable",
            "pets_friendly",
            "allow_unit_rates",
            "computed",
            "inherited",
            "limited",
            "include_descriptions",
        }

        for key, value in params.items():
            if key in boolean_fields and value is not None:
                converted[key] = 1 if value else 0
            else:
                converted[key] = value

        return converted

    def _process_units_response(self, api_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API de unidades

        Args:
            api_result: Respuesta cruda de la API

        Returns:
            Respuesta procesada
        """
        # Calcular información de paginación
        total_items = api_result.get("total_items", 0)
        current_page = api_result.get("page", 1)
        page_size = api_result.get("size", 10)
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar unidades
        units = api_result.get("units", [])
        processed_units = []

        for unit in units:
            processed_unit = self._process_unit(unit)
            processed_units.append(processed_unit)

        return {
            "units": processed_units,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _process_unit(self, unit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una unidad individual

        Args:
            unit: Datos de la unidad

        Returns:
            Unidad procesada
        """
        # Mapear campos de la API al schema
        processed = {
            "id": unit.get("id"),
            "name": unit.get("name"),
            "unit_code": unit.get("unitCode"),
            "short_name": unit.get("shortName"),
            "description": unit.get("description"),
            "bedrooms": unit.get("bedrooms"),
            "bathrooms": unit.get("bathrooms"),
            "occupancy": unit.get("occupancy"),
            "unit_type_id": unit.get("unitTypeId"),
            "unit_type_name": unit.get("unitTypeName"),
            "node_id": unit.get("nodeId"),
            "node_name": unit.get("nodeName"),
            "is_active": unit.get("isActive"),
            "is_bookable": unit.get("isBookable"),
            "pets_friendly": unit.get("petsFriendly"),
            "unit_status": unit.get("unitStatus"),
            "amenities": unit.get("amenities"),
            "base_price": unit.get("basePrice"),
            "currency": unit.get("currency"),
            "address": unit.get("address"),
            "coordinates": unit.get("coordinates"),
            "created_at": unit.get("createdAt"),
            "updated_at": unit.get("updatedAt"),
            "links": unit.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}

    def close(self) -> None:
        """Cierra el cliente HTTP"""
        self.client.close()
        self.logger.info("TrackHSAPIClient cerrado")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
