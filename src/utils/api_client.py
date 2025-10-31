"""
Cliente API para TrackHS con logging estructurado
"""

import time
from enum import Enum
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

    def _is_empty_value(self, value: Any) -> bool:
        """Verifica si un valor debe considerarse vacío y no incluirse en la query"""
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, tuple, dict)) and len(value) == 0:
            return True
        return False

    def _get_enum_value(self, value: Any) -> Any:
        """Convierte un enum a su valor, o retorna el valor si no es enum"""
        if isinstance(value, Enum):
            return value.value
        return value

    def _serialize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Serializa parámetros convirtiendo objetos date a strings ISO y enums a valores"""
        from datetime import date, datetime

        serialized = {}
        for key, value in params.items():
            if isinstance(value, date):
                serialized[key] = value.isoformat()
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            else:
                # Convertir enums a valores si es necesario
                serialized[key] = self._get_enum_value(value)
        return serialized

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

    def search_units(self, params) -> Dict[str, Any]:
        """
        DEPRECADO: Usa la Tool MCP `search_units` (src/tools/search_units.py).
        """
        raise TrackHSAPIError(
            "Deprecated: usa la Tool MCP 'search_units' en src/tools/search_units.py"
        )

    def build_units_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construye los parámetros de consulta (camelCase) para /api/pms/units

        Acepta snake_case o camelCase y devuelve camelCase con booleanos 1/0.
        """
        if params is None:
            return {}

        # Asegurar base
        page = params.get("page", 1)
        size = params.get("size", 10)
        out: Dict[str, Any] = {"page": page, "size": size}

        mapping = {
            # texto
            "unit_code": "unitCode",
            "short_name": "shortName",
            # rangos
            "min_bedrooms": "minBedrooms",
            "max_bedrooms": "maxBedrooms",
            "min_bathrooms": "minBathrooms",
            "max_bathrooms": "maxBathrooms",
            "min_occupancy": "minOccupancy",
            "max_occupancy": "maxOccupancy",
            # booleanos/estado
            "is_active": "isActive",
            "is_bookable": "isBookable",
            "pets_friendly": "petsFriendly",
            "unit_status": "unitStatus",
            "allow_unit_rates": "allowUnitRates",
            # ids/listas
            "amenity_id": "amenityId",
            "node_id": "nodeId",
            "unit_type_id": "unitTypeId",
            "owner_id": "ownerId",
            "company_id": "companyId",
            "channel_id": "channelId",
            "lodging_type_id": "lodgingTypeId",
            "bed_type_id": "bedTypeId",
            "amenity_all": "amenityAll",
            "unit_ids": "unitIds",
            # ordenamiento
            "sort_column": "sortColumn",
            "sort_direction": "sortDirection",
        }

        # Campos que ya están en camelCase y se copian tal cual si existen
        passthrough = {
            "search",
            "term",
            "unitCode",
            "shortName",
            "bedrooms",
            "bathrooms",
            "occupancy",
            "arrival",
            "departure",
            "content_updated_since",
            "sortColumn",
            "sortDirection",
        }

        # Incluir primero los passthrough
        for k in passthrough:
            if k in params and not self._is_empty_value(params[k]):
                out[k] = self._get_enum_value(params[k])

        # Función simple para convertir string a bool
        def _str_to_bool(s):
            if isinstance(s, bool):
                return s
            if isinstance(s, (int, float)):
                return bool(int(s))
            if isinstance(s, str):
                s_lower = s.strip().lower()
                return s_lower in {"true", "1", "yes", "y", "si", "sí"}
            return False

        # Función simple para convertir string a int
        def _str_to_int(s):
            if isinstance(s, int):
                return s
            if isinstance(s, float):
                return int(s)
            if isinstance(s, str) and s.strip():
                try:
                    return int(s.strip())
                except ValueError:
                    return None
            return None

        # Función simple para convertir string a lista de ints
        def _str_to_list_int(s):
            import json

            if isinstance(s, list):
                return s
            if isinstance(s, str):
                s_stripped = s.strip()
                # JSON array: "[1,2,3]"
                if s_stripped.startswith("[") and s_stripped.endswith("]"):
                    try:
                        parsed = json.loads(s_stripped)
                        if isinstance(parsed, list):
                            return parsed
                    except json.JSONDecodeError:
                        pass
                # Separado por comas: "1,2,3"
                if "," in s_stripped:
                    items = [item.strip() for item in s_stripped.split(",")]
                    coerced = []
                    for item in items:
                        try:
                            coerced.append(int(item))
                        except ValueError:
                            pass
                    return coerced if coerced else None
            return None

        # Mapear snake_case -> camelCase
        for k, v in params.items():
            if k in ("page", "size"):
                continue
            if self._is_empty_value(v):
                continue
            ck = mapping.get(k)
            if ck:
                # Convertir enums a valores
                v = self._get_enum_value(v)
                # convertir booleanos (1/0) donde aplique
                if k in {
                    "is_active",
                    "is_bookable",
                    "pets_friendly",
                    "allow_unit_rates",
                }:
                    out[ck] = 1 if _str_to_bool(v) else 0
                # convertir strings a ints para campos numéricos
                elif k in {
                    "bedrooms",
                    "min_bedrooms",
                    "max_bedrooms",
                    "bathrooms",
                    "min_bathrooms",
                    "max_bathrooms",
                    "occupancy",
                    "min_occupancy",
                    "max_occupancy",
                    "calendar_id",
                    "role_id",
                }:
                    coerced = _str_to_int(v)
                    if coerced is not None:
                        out[ck] = coerced
                # convertir strings a listas para campos de lista
                elif k in {
                    "amenity_id",
                    "node_id",
                    "unit_type_id",
                    "owner_id",
                    "company_id",
                    "channel_id",
                    "lodging_type_id",
                    "bed_type_id",
                    "amenity_all",
                    "unit_ids",
                }:
                    coerced = _str_to_list_int(v)
                    if coerced is not None:
                        out[ck] = coerced
                else:
                    out[ck] = v
                continue

        # Si el caller pasó campos camelCase booleanos, respetarlos y convertirlos
        for ck in ("isActive", "isBookable", "petsFriendly", "allowUnitRates"):
            if ck in params and not self._is_empty_value(params[ck]):
                out[ck] = 1 if _str_to_bool(params[ck]) else 0

        # Asegurar que search y term desde snake_case también pasen
        if "search" not in out and not self._is_empty_value(params.get("search")):
            out["search"] = params.get("search")
        if "term" not in out and not self._is_empty_value(params.get("term")):
            out["term"] = params.get("term")

        return out

    def _convert_camelcase_to_snakecase(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte parámetros camelCase a snake_case para compatibilidad con API TrackHS

        Args:
            params: Parámetros en camelCase

        Returns:
            Parámetros convertidos a snake_case
        """
        converted = {}
        camelcase_to_snakecase = {
            "unitCode": "unit_code",
            "shortName": "short_name",
            "minBedrooms": "min_bedrooms",
            "maxBedrooms": "max_bedrooms",
            "minBathrooms": "min_bathrooms",
            "maxBathrooms": "max_bathrooms",
            "minOccupancy": "min_occupancy",
            "maxOccupancy": "max_occupancy",
            "isActive": "is_active",
            "isBookable": "is_bookable",
            "petsFriendly": "pets_friendly",
            "unitStatus": "unit_status",
            "allowUnitRates": "allow_unit_rates",
            "amenityId": "amenity_id",
            "nodeId": "node_id",
            "unitTypeId": "unit_type_id",
            "ownerId": "owner_id",
            "companyId": "company_id",
            "channelId": "channel_id",
            "lodgingTypeId": "lodging_type_id",
            "bedTypeId": "bed_type_id",
            "amenityAll": "amenity_all",
            "unitIds": "unit_ids",
            "sortColumn": "sort_column",
            "sortDirection": "sort_direction",
            "arrivalStart": "arrival_start",
            "arrivalEnd": "arrival_end",
        }

        for key, value in params.items():
            if key in camelcase_to_snakecase:
                converted[camelcase_to_snakecase[key]] = value
            else:
                converted[key] = value

        return converted

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
            # snake_case (legacy)
            "is_active",
            "is_bookable",
            "pets_friendly",
            "allow_unit_rates",
            "computed",
            "inherited",
            "limited",
            "include_descriptions",
            # camelCase (current)
            "isActive",
            "isBookable",
            "petsFriendly",
            "allowUnitRates",
        }

        for key, value in params.items():
            # Filtrar valores vacíos, None, o strings vacíos
            if value is None or value == "" or value == "None" or value == "null":
                continue

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

    def search_amenities(self, params) -> Dict[str, Any]:
        """
        Busca amenidades con filtros avanzados

        Args:
            params: Parámetros de búsqueda de amenidades (dict o Pydantic model)

        Returns:
            Respuesta de la API con amenidades encontradas
        """
        # Convertir a diccionario si es un modelo Pydantic
        if hasattr(params, "model_dump"):
            params_dict = params.model_dump()
        else:
            params_dict = params

        # Log de parámetros de entrada
        self.logger.info(
            "Iniciando búsqueda de amenidades",
            extra={
                "original_params": params_dict,
                "param_count": len(params_dict),
            },
        )

        # Realizar llamada a la API
        result = self.get("api/pms/units/amenities", params_dict)

        # Log de respuesta cruda de la API
        self.logger.info(
            "Respuesta cruda de amenidades API",
            extra={
                "api_response_keys": (
                    list(result.keys()) if isinstance(result, dict) else "not_dict"
                ),
                "has_amenities": (
                    "amenities" in result if isinstance(result, dict) else False
                ),
                "amenities_count": (
                    len(result.get("amenities", [])) if isinstance(result, dict) else 0
                ),
            },
        )

        # Procesar respuesta
        processed_result = self._process_amenities_response(result)

        # Log de resultado final
        self.logger.info(
            "Resultado procesado de búsqueda de amenidades",
            extra={
                "processed_amenities_count": len(processed_result.get("amenities", [])),
                "total_items": processed_result.get("total_items", 0),
                "total_pages": processed_result.get("total_pages", 0),
            },
        )

        return processed_result

    def search_reservations(self, params) -> Dict[str, Any]:
        """
        Busca reservas con filtros avanzados

        Args:
            params: Parámetros de búsqueda de reservas (dict o Pydantic model)

        Returns:
            Respuesta de la API con reservas encontradas
        """
        # Convertir a diccionario si es un modelo Pydantic
        if hasattr(params, "model_dump"):
            params_dict = params.model_dump()
        else:
            params_dict = params

        # Log de parámetros de entrada
        self.logger.info(
            "Iniciando búsqueda de reservas",
            extra={
                "original_params": params_dict,
                "param_count": len(params_dict),
            },
        )

        # Realizar llamada a la API
        result = self.get("api/pms/reservations", params_dict)

        # Log de respuesta cruda de la API
        self.logger.info(
            "Respuesta cruda de reservas API",
            extra={
                "api_response_keys": (
                    list(result.keys()) if isinstance(result, dict) else "not_dict"
                ),
                "has_reservations": (
                    "reservations" in result if isinstance(result, dict) else False
                ),
                "reservations_count": (
                    len(result.get("reservations", []))
                    if isinstance(result, dict)
                    else 0
                ),
            },
        )

        # Procesar respuesta
        processed_result = self._process_reservations_response(result)

        # Log de resultado final
        self.logger.info(
            "Resultado procesado de búsqueda de reservas",
            extra={
                "processed_reservations_count": len(
                    processed_result.get("reservations", [])
                ),
                "total_items": processed_result.get("total_items", 0),
                "total_pages": processed_result.get("total_pages", 0),
            },
        )

        return processed_result

    def get_reservation(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtiene una reserva específica por ID

        Args:
            reservation_id: ID de la reserva

        Returns:
            Datos de la reserva
        """
        self.logger.info(
            "Obteniendo reserva",
            extra={"reservation_id": reservation_id},
        )

        result = self.get(f"api/pms/reservations/{reservation_id}")

        self.logger.info(
            "Reserva obtenida exitosamente",
            extra={"reservation_id": reservation_id},
        )

        return result

    def get_folio(self, folio_id: int) -> Dict[str, Any]:
        """
        Obtiene un folio financiero por su ID según documentación oficial de TrackHS

        Args:
            folio_id: ID del folio (no de la reserva)

        Returns:
            Datos del folio financiero
        """
        self.logger.info(
            "Obteniendo folio financiero",
            extra={"folio_id": folio_id},
        )

        result = self.get(f"api/pms/folios/{folio_id}")

        self.logger.info(
            "Folio financiero obtenido exitosamente",
            extra={"folio_id": folio_id},
        )

        return result

    def create_maintenance_work_order(self, params) -> Dict[str, Any]:
        """
        Crea una orden de trabajo de mantenimiento

        Args:
            params: Parámetros de la orden de trabajo (dict o Pydantic model)

        Returns:
            Datos de la orden creada
        """
        # Convertir a diccionario si es un modelo Pydantic
        if hasattr(params, "model_dump"):
            params_dict = params.model_dump()
        else:
            params_dict = params

        # Serializar parámetros para convertir objetos date a strings ISO
        params_dict = self._serialize_params(params_dict)

        # Agregar status por defecto si no existe
        if "status" not in params_dict:
            params_dict["status"] = "not-started"

        self.logger.info(
            "Creando orden de mantenimiento",
            extra={"unit_id": params_dict.get("unit_id")},
        )

        result = self.post("api/pms/maintenance/work-orders", params_dict)

        self.logger.info(
            "Orden de mantenimiento creada exitosamente",
            extra={"work_order_id": result.get("id")},
        )

        return result

    def create_housekeeping_work_order(self, params) -> Dict[str, Any]:
        """
        Crea una orden de trabajo de housekeeping

        Args:
            params: Parámetros de la orden de trabajo (dict o Pydantic model)

        Returns:
            Datos de la orden creada
        """
        # Convertir a diccionario si es un modelo Pydantic
        if hasattr(params, "model_dump"):
            params_dict = params.model_dump()
        else:
            params_dict = params

        # Serializar parámetros para convertir objetos date a strings ISO
        params_dict = self._serialize_params(params_dict)

        # Agregar status por defecto si no existe
        if "status" not in params_dict:
            params_dict["status"] = "pending"

        self.logger.info(
            "Creando orden de housekeeping",
            extra={"unit_id": params_dict.get("unit_id")},
        )

        result = self.post("api/pms/housekeeping/work-orders", params_dict)

        self.logger.info(
            "Orden de housekeeping creada exitosamente",
            extra={"work_order_id": result.get("id")},
        )

        return result

    def _process_amenities_response(self, api_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API de amenidades

        Args:
            api_result: Respuesta cruda de la API

        Returns:
            Respuesta procesada
        """
        # Extraer datos de paginación
        amenities, total_items, current_page, page_size = (
            self._extract_amenities_pagination_data(api_result)
        )

        # Calcular información de paginación
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar amenidades
        processed_amenities = []
        for amenity in amenities:
            try:
                processed_amenity = self._process_amenity(amenity)
                processed_amenities.append(processed_amenity)
            except Exception as e:
                self.logger.warning(
                    f"Error procesando amenidad: {str(e)}",
                    extra={"amenity_data": amenity, "error_type": type(e).__name__},
                )

        return {
            "amenities": processed_amenities,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _process_reservations_response(
        self, api_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API de reservas

        Args:
            api_result: Respuesta cruda de la API

        Returns:
            Respuesta procesada
        """
        # Extraer datos de paginación
        reservations, total_items, current_page, page_size = (
            self._extract_reservations_pagination_data(api_result)
        )

        # Calcular información de paginación
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar reservas
        processed_reservations = []
        for reservation in reservations:
            try:
                processed_reservation = self._process_reservation(reservation)
                processed_reservations.append(processed_reservation)
            except Exception as e:
                self.logger.warning(
                    f"Error procesando reserva: {str(e)}",
                    extra={
                        "reservation_data": reservation,
                        "error_type": type(e).__name__,
                    },
                )

        return {
            "reservations": processed_reservations,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _extract_amenities_pagination_data(self, api_result: Dict[str, Any]) -> tuple:
        """
        Extrae datos de paginación de la respuesta de amenidades

        Returns:
            tuple: (amenities, total_items, current_page, page_size)
        """
        if not isinstance(api_result, dict):
            return [], 0, 1, 10

        # Intentar diferentes estructuras de respuesta
        if "_embedded" in api_result:
            embedded_data = api_result.get("_embedded", {})
            amenities = embedded_data.get("amenities", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
        else:
            amenities = api_result.get("amenities", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)

        if not isinstance(amenities, list):
            amenities = []

        return amenities, total_items, current_page, page_size

    def _extract_reservations_pagination_data(
        self, api_result: Dict[str, Any]
    ) -> tuple:
        """
        Extrae datos de paginación de la respuesta de reservas

        Returns:
            tuple: (reservations, total_items, current_page, page_size)
        """
        if not isinstance(api_result, dict):
            return [], 0, 1, 10

        # Intentar diferentes estructuras de respuesta
        if "_embedded" in api_result:
            embedded_data = api_result.get("_embedded", {})
            reservations = embedded_data.get("reservations", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
        else:
            reservations = api_result.get("reservations", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)

        if not isinstance(reservations, list):
            reservations = []

        return reservations, total_items, current_page, page_size

    def _process_amenity(self, amenity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una amenidad individual

        Args:
            amenity: Datos de la amenidad

        Returns:
            Amenidad procesada
        """
        processed = {
            "id": amenity.get("id"),
            "name": amenity.get("name"),
            "description": amenity.get("description"),
            "group_id": amenity.get("groupId"),
            "group_name": amenity.get("groupName"),
            "order": amenity.get("order"),
            "is_public": amenity.get("isPublic"),
            "public_searchable": amenity.get("publicSearchable"),
            "is_filterable": amenity.get("isFilterable"),
            "homeaway_type": amenity.get("homeawayType"),
            "airbnb_type": amenity.get("airbnbType"),
            "tripadvisor_type": amenity.get("tripadvisorType"),
            "marriott_type": amenity.get("marriottType"),
            "created_at": amenity.get("createdAt"),
            "updated_at": amenity.get("updatedAt"),
            "links": amenity.get("links"),
        }

        return {k: v for k, v in processed.items() if v is not None}

    def _process_reservation(self, reservation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una reserva individual

        Args:
            reservation: Datos de la reserva

        Returns:
            Reserva procesada
        """
        processed = {
            "id": reservation.get("id"),
            "confirmation_number": reservation.get("confirmation_number"),
            "currency": reservation.get("currency"),
            "unit_id": reservation.get("unitId"),
            "unit_type_id": reservation.get("unitTypeId"),
            "arrival_date": reservation.get("arrival"),
            "departure_date": reservation.get("departure"),
            "status": reservation.get("status"),
            "total_amount": reservation.get("totalAmount"),
            "guest_count": reservation.get("guestCount"),
            "alternates": reservation.get("alternates"),
            "created_at": reservation.get("createdAt"),
            "updated_at": reservation.get("updatedAt"),
            "unit": reservation.get("unit"),
            "contact": reservation.get("contact"),
            "policies": reservation.get("policies"),
            "links": reservation.get("links"),
        }

        return {k: v for k, v in processed.items() if v is not None}

    def close(self) -> None:
        """Cierra el cliente HTTP"""
        self.client.close()
        self.logger.info("TrackHSAPIClient cerrado")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
