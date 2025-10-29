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

        except (
            TrackHSAPIError,
            TrackHSAuthenticationError,
            TrackHSAuthorizationError,
            TrackHSNotFoundError,
        ):
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
        # Log de parámetros de entrada
        self.logger.info(
            "Iniciando búsqueda de unidades",
            extra={
                "original_params": params,
                "param_count": len(params),
                "has_filters": any(
                    v is not None for v in params.values() if v != 1 and v != 0
                ),
            },
        )

        # Convertir parámetros booleanos a enteros (1/0) según la API
        api_params = self._convert_boolean_params(params)

        # Log de parámetros convertidos
        self.logger.info(
            "Parámetros convertidos para API",
            extra={
                "converted_params": api_params,
                "conversion_changes": {
                    k: {"original": params.get(k), "converted": v}
                    for k, v in api_params.items()
                    if k in params and params[k] != v
                },
            },
        )

        # Realizar llamada a la API
        result = self.get("api/pms/units", api_params)

        # Log de respuesta cruda de la API
        self.logger.info(
            "Respuesta cruda de la API",
            extra={
                "api_response_keys": (
                    list(result.keys()) if isinstance(result, dict) else "not_dict"
                ),
                "has_units": "units" in result if isinstance(result, dict) else False,
                "units_count": (
                    len(result.get("units", [])) if isinstance(result, dict) else 0
                ),
                "total_items": (
                    result.get("total_items", "not_found")
                    if isinstance(result, dict)
                    else "not_found"
                ),
                "response_structure": (
                    "embedded"
                    if "_embedded" in result
                    else "direct" if isinstance(result, dict) else "unknown"
                ),
            },
        )

        # Procesar respuesta
        processed_result = self._process_units_response(result)

        # Log de resultado final
        self.logger.info(
            "Resultado procesado de búsqueda",
            extra={
                "processed_units_count": len(processed_result.get("units", [])),
                "total_items": processed_result.get("total_items", 0),
                "total_pages": processed_result.get("total_pages", 0),
                "current_page": processed_result.get("current_page", 0),
                "has_next": processed_result.get("has_next", False),
                "has_prev": processed_result.get("has_prev", False),
            },
        )

        return processed_result

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
        # Log de estructura de respuesta para debugging
        self.logger.info(
            "Procesando respuesta de API",
            extra={
                "response_type": type(api_result).__name__,
                "response_keys": (
                    list(api_result.keys())
                    if isinstance(api_result, dict)
                    else "not_dict"
                ),
                "has_units_key": (
                    "units" in api_result if isinstance(api_result, dict) else False
                ),
                "has_embedded": (
                    "_embedded" in api_result if isinstance(api_result, dict) else False
                ),
                "has_data": (
                    "data" in api_result if isinstance(api_result, dict) else False
                ),
            },
        )

        # Detectar estructura de respuesta y extraer datos
        units, total_items, current_page, page_size = self._extract_pagination_data(
            api_result
        )

        # Calcular información de paginación
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar unidades
        processed_units = []
        for unit in units:
            try:
                processed_unit = self._process_unit(unit)
                processed_units.append(processed_unit)
            except Exception as e:
                self.logger.warning(
                    f"Error procesando unidad: {str(e)}",
                    extra={"unit_data": unit, "error_type": type(e).__name__},
                )
                # Continuar con las demás unidades

        # Log de resultado del procesamiento
        self.logger.info(
            "Procesamiento completado",
            extra={
                "original_units_count": len(units),
                "processed_units_count": len(processed_units),
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": current_page,
                "page_size": page_size,
            },
        )

        return {
            "units": processed_units,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _extract_pagination_data(self, api_result: Dict[str, Any]) -> tuple:
        """
        Extrae datos de paginación de diferentes estructuras de respuesta

        Returns:
            tuple: (units, total_items, current_page, page_size)
        """
        if not isinstance(api_result, dict):
            self.logger.warning(
                "Respuesta de API no es un diccionario",
                extra={"response": str(api_result)[:200]},
            )
            return [], 0, 1, 10

        # Intentar diferentes estructuras de respuesta
        if "_embedded" in api_result:
            # Estructura con _embedded
            embedded_data = api_result.get("_embedded", {})
            units = embedded_data.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
            self.logger.debug("Usando estructura _embedded")

        elif "embedded" in api_result:
            # Estructura con embedded (sin guión bajo)
            embedded_data = api_result.get("embedded", {})
            units = embedded_data.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
            self.logger.debug("Usando estructura embedded")

        elif "data" in api_result:
            # Estructura con data
            data = api_result.get("data", {})
            units = data.get("units", [])
            total_items = data.get("total_items", 0)
            current_page = data.get("page", 1)
            page_size = data.get("size", 10)
            self.logger.debug("Usando estructura data")

        else:
            # Estructura directa
            units = api_result.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
            self.logger.debug("Usando estructura directa")

        # Validar que units es una lista
        if not isinstance(units, list):
            self.logger.warning(
                "Units no es una lista",
                extra={
                    "units_type": type(units).__name__,
                    "units_value": str(units)[:200],
                },
            )
            units = []

        return units, total_items, current_page, page_size

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
