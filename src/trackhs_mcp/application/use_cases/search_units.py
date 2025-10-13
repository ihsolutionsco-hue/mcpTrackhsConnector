"""
Caso de uso para buscar unidades
"""

from typing import TYPE_CHECKING, Any, Dict, List, Union

from ...domain.entities.units import SearchUnitsParams
from ...domain.exceptions.api_exceptions import ValidationError

if TYPE_CHECKING:
    from ..ports.api_client_port import ApiClientPort


class SearchUnitsUseCase:
    """Caso de uso para buscar unidades"""

    def __init__(self, api_client: "ApiClientPort"):
        self.api_client = api_client

    async def execute(self, params: SearchUnitsParams) -> Dict[str, Any]:
        """
        Ejecutar búsqueda de unidades

        Args:
            params: Parámetros de búsqueda

        Returns:
            Respuesta con las unidades encontradas

        Raises:
            ValidationError: Si los parámetros son inválidos
        """
        # Validar parámetros
        self._validate_params(params)

        # Construir parámetros de la petición
        request_params = self._build_request_params(params)

        # Realizar petición a la API
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Units API Request - Endpoint: /pms/units")
        logger.info(f"Units API Request - Params: {request_params}")
        logger.info(f"Units API Request - Params count: {len(request_params)}")
        logger.info(
            f"Units API Request - Params types: {[(k, type(v).__name__, v) for k, v in request_params.items()]}"
        )

        response = await self.api_client.get("/pms/units", params=request_params)

        # Procesar respuesta
        return self._process_response(response)

    def _validate_params(self, params: SearchUnitsParams) -> None:
        """Validar parámetros de entrada"""
        if params.page and params.page < 1:
            raise ValidationError("Page debe ser mayor o igual a 1")

        if params.size and (params.size < 1 or params.size > 1000):
            raise ValidationError("Size debe estar entre 1 y 1000")

        # Validar límite total de resultados (10k máximo)
        # Ajustar page para cálculo (API usa 1-based, pero calculamos con 0-based)
        adjusted_page = (
            max(0, params.page - 1) if params.page and params.page > 0 else 0
        )
        if params.page and params.size and adjusted_page * params.size > 10000:
            raise ValidationError("Total results (page * size) must be <= 10,000")

        # Validar fechas si están presentes
        if params.arrival and params.departure:
            if params.arrival > params.departure:
                raise ValidationError("arrival debe ser anterior a departure")

        # Validar rangos de habitaciones y baños
        if params.min_bedrooms and params.max_bedrooms:
            if params.min_bedrooms > params.max_bedrooms:
                raise ValidationError(
                    "min_bedrooms debe ser menor o igual a max_bedrooms"
                )

        if params.min_bathrooms and params.max_bathrooms:
            if params.min_bathrooms > params.max_bathrooms:
                raise ValidationError(
                    "min_bathrooms debe ser menor o igual a max_bathrooms"
                )

    def _build_request_params(self, params: SearchUnitsParams) -> Dict[str, Any]:
        """Construir parámetros para la petición HTTP"""
        request_params = {}

        # Parámetros de paginación
        if params.page is not None:
            request_params["page"] = params.page
        if params.size:
            request_params["size"] = params.size

        # Parámetros de ordenamiento (siempre incluir valores por defecto según la API)
        request_params["sortColumn"] = params.sort_column or "name"
        request_params["sortDirection"] = params.sort_direction or "asc"

        # Parámetros de búsqueda
        if params.search:
            request_params["search"] = params.search
        if params.term:
            request_params["term"] = params.term
        if params.unit_code:
            request_params["unitCode"] = params.unit_code
        if params.short_name:
            request_params["shortName"] = params.short_name

        # Parámetros de filtrado por ID
        if params.node_id:
            request_params["nodeId"] = self._format_id_list(params.node_id)
        if params.amenity_id:
            request_params["amenityId"] = self._format_id_list(params.amenity_id)
        if params.unit_type_id:
            request_params["unitTypeId"] = self._format_id_list(params.unit_type_id)
        if params.id:
            request_params["id"] = params.id
        if params.calendar_id:
            request_params["calendarId"] = params.calendar_id
        if params.role_id:
            request_params["roleId"] = params.role_id

        # Parámetros de habitaciones y baños
        if params.bedrooms is not None:
            request_params["bedrooms"] = params.bedrooms
        if params.min_bedrooms is not None:
            request_params["minBedrooms"] = params.min_bedrooms
        if params.max_bedrooms is not None:
            request_params["maxBedrooms"] = params.max_bedrooms
        if params.bathrooms is not None:
            request_params["bathrooms"] = params.bathrooms
        if params.min_bathrooms is not None:
            request_params["minBathrooms"] = params.min_bathrooms
        if params.max_bathrooms is not None:
            request_params["maxBathrooms"] = params.max_bathrooms

        # Parámetros booleanos (convertir a 0/1)
        if params.pets_friendly is not None:
            request_params["petsFriendly"] = params.pets_friendly
        if params.allow_unit_rates is not None:
            request_params["allowUnitRates"] = params.allow_unit_rates
        if params.computed is not None:
            request_params["computed"] = params.computed
        if params.inherited is not None:
            request_params["inherited"] = params.inherited
        if params.limited is not None:
            request_params["limited"] = params.limited
        if params.is_bookable is not None:
            request_params["isBookable"] = params.is_bookable
        if params.include_descriptions is not None:
            request_params["includeDescriptions"] = params.include_descriptions
        if params.is_active is not None:
            request_params["isActive"] = params.is_active
        if params.events_allowed is not None:
            request_params["eventsAllowed"] = params.events_allowed
        if params.smoking_allowed is not None:
            request_params["smokingAllowed"] = params.smoking_allowed
        if params.children_allowed is not None:
            request_params["childrenAllowed"] = params.children_allowed
        if params.is_accessible is not None:
            request_params["isAccessible"] = params.is_accessible

        # Parámetros de fechas
        if params.arrival:
            request_params["arrival"] = params.arrival
        if params.departure:
            request_params["departure"] = params.departure
        if params.content_updated_since:
            request_params["contentUpdatedSince"] = params.content_updated_since
        if params.updated_since:
            request_params["updatedSince"] = params.updated_since

        # Parámetros adicionales
        if params.unit_status:
            request_params["unitStatus"] = params.unit_status

        return request_params

    def _format_id_list(self, ids: Union[int, List[int]]) -> Union[int, List[int]]:
        """Formatear lista de IDs para la API"""
        if isinstance(ids, int):
            return ids
        if isinstance(ids, list):
            return ids if len(ids) > 1 else ids[0]
        return ids

    def _process_response(self, response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Procesar respuesta de la API"""
        # Si la respuesta es un string JSON, parsearlo
        if isinstance(response, str):
            import json

            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON response from API: {e}")

        # Si ya es un diccionario, retornarlo directamente
        return response
