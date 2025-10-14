"""
Caso de uso para buscar amenidades
"""

from typing import TYPE_CHECKING, Any, Dict

from ...domain.entities.amenities import SearchAmenitiesParams
from ...domain.exceptions.api_exceptions import ValidationError

if TYPE_CHECKING:
    from ..ports.api_client_port import ApiClientPort


class SearchAmenitiesUseCase:
    """Caso de uso para buscar amenidades"""

    def __init__(self, api_client: "ApiClientPort"):
        self.api_client = api_client

    async def execute(self, params: SearchAmenitiesParams) -> Dict[str, Any]:
        """
        Ejecutar búsqueda de amenidades

        Args:
            params: Parámetros de búsqueda

        Returns:
            Respuesta con las amenidades encontradas

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
        logger.info(f"Amenities API Request - Endpoint: /pms/units/amenities")
        logger.info(f"Amenities API Request - Params: {request_params}")
        logger.info(f"Amenities API Request - Params count: {len(request_params)}")
        logger.info(
            f"Amenities API Request - Params types: {[(k, type(v).__name__, v) for k, v in request_params.items()]}"
        )

        response = await self.api_client.get(
            "/pms/units/amenities", params=request_params
        )

        # Procesar respuesta
        return self._process_response(response)

    def _validate_params(self, params: SearchAmenitiesParams) -> None:
        """Validar parámetros de entrada"""
        # Convertir page y size a enteros para validación
        if params.page is not None:
            page_val = int(params.page) if isinstance(params.page, str) else params.page
            if page_val < 1:
                raise ValidationError("Page debe ser mayor o igual a 1")

        if params.size is not None:
            size_val = int(params.size) if isinstance(params.size, str) else params.size
            if size_val < 1 or size_val > 1000:
                raise ValidationError("Size debe estar entre 1 y 1000")

        # Validar sortColumn
        valid_sort_columns = [
            "id",
            "order",
            "isPublic",
            "publicSearchable",
            "isFilterable",
            "createdAt",
        ]
        if params.sort_column and params.sort_column not in valid_sort_columns:
            raise ValidationError(
                f"sortColumn debe ser uno de: {', '.join(valid_sort_columns)}"
            )

        # Validar sortDirection
        if params.sort_direction and params.sort_direction not in ["asc", "desc"]:
            raise ValidationError("sortDirection debe ser 'asc' o 'desc'")

        # Validar parámetros booleanos (0/1)
        boolean_params = [
            ("is_public", params.is_public),
            ("public_searchable", params.public_searchable),
            ("is_filterable", params.is_filterable),
        ]

        for param_name, param_value in boolean_params:
            if param_value is not None and param_value not in [0, 1]:
                raise ValidationError(f"{param_name} debe ser 0 o 1")

        # Validar group_id si se proporciona
        if params.group_id is not None:
            group_id_val = (
                int(params.group_id)
                if isinstance(params.group_id, str)
                else params.group_id
            )
            if group_id_val <= 0:
                raise ValidationError("group_id debe ser un entero positivo")

    def _build_request_params(self, params: SearchAmenitiesParams) -> Dict[str, Any]:
        """Construir parámetros para la petición HTTP"""
        request_params = {}

        # Parámetros de paginación
        if params.page is not None:
            request_params["page"] = params.page
        if params.size:
            request_params["size"] = params.size

        # Parámetros de ordenamiento (siempre incluir valores por defecto según la API)
        request_params["sortColumn"] = params.sort_column or "order"
        request_params["sortDirection"] = params.sort_direction or "asc"

        # Parámetros de búsqueda
        if params.search:
            request_params["search"] = params.search

        # Parámetros de filtrado
        if params.group_id is not None:
            request_params["groupId"] = params.group_id

        # Parámetros booleanos (convertir a 0/1)
        if params.is_public is not None:
            request_params["isPublic"] = params.is_public
        if params.public_searchable is not None:
            request_params["publicSearchable"] = params.public_searchable
        if params.is_filterable is not None:
            request_params["isFilterable"] = params.is_filterable

        return request_params

    def _process_response(self, response: Any) -> Dict[str, Any]:
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
