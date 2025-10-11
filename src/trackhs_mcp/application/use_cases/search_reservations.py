"""
Caso de uso para buscar reservas
"""

from typing import Any, Dict, List, Union

from ...domain.entities.reservations import (
    SearchReservationsParams,
    SearchReservationsResponse,
)
from ...domain.exceptions.api_exceptions import ValidationError
from ..ports.api_client_port import ApiClientPort


class SearchReservationsUseCase:
    """Caso de uso para buscar reservas"""

    def __init__(self, api_client: ApiClientPort):
        self.api_client = api_client

    async def execute(
        self, params: SearchReservationsParams
    ) -> SearchReservationsResponse:
        """
        Ejecutar búsqueda de reservas

        Args:
            params: Parámetros de búsqueda

        Returns:
            Respuesta con las reservas encontradas

        Raises:
            ValidationError: Si los parámetros son inválidos
        """
        # Validar parámetros
        self._validate_params(params)

        # Construir parámetros de la petición
        request_params = self._build_request_params(params)

        # Realizar petición a la API
        response = await self.api_client.get("/v2/pms/reservations", request_params)

        # Procesar respuesta
        return self._process_response(response)

    def _validate_params(self, params: SearchReservationsParams) -> None:
        """Validar parámetros de entrada"""
        if params.page and params.page < 1:
            raise ValidationError("Page debe ser mayor a 0")

        if params.size and (params.size < 1 or params.size > 100):
            raise ValidationError("Size debe estar entre 1 y 100")

        # Validar fechas si están presentes
        if params.arrival_start and params.arrival_end:
            if params.arrival_start > params.arrival_end:
                raise ValidationError("arrival_start debe ser anterior a arrival_end")

    def _build_request_params(self, params: SearchReservationsParams) -> Dict[str, Any]:
        """Construir parámetros para la petición HTTP"""
        request_params = {}

        # Parámetros de paginación
        if params.page:
            request_params["page"] = params.page
        if params.size:
            request_params["size"] = params.size

        # Parámetros de ordenamiento
        if params.sort_column:
            request_params["sort_column"] = params.sort_column
        if params.sort_direction:
            request_params["sort_direction"] = params.sort_direction

        # Parámetros de búsqueda
        if params.search:
            request_params["search"] = params.search
        if params.tags:
            request_params["tags"] = params.tags

        # Parámetros de filtrado por ID
        if params.node_id:
            request_params["node_id"] = self._format_id_list(params.node_id)
        if params.unit_id:
            request_params["unit_id"] = self._format_id_list(params.unit_id)
        if params.contact_id:
            request_params["contact_id"] = self._format_id_list(params.contact_id)

        # Parámetros de fechas
        if params.booked_start:
            request_params["booked_start"] = params.booked_start
        if params.booked_end:
            request_params["booked_end"] = params.booked_end
        if params.arrival_start:
            request_params["arrival_start"] = params.arrival_start
        if params.arrival_end:
            request_params["arrival_end"] = params.arrival_end
        if params.departure_start:
            request_params["departure_start"] = params.departure_start
        if params.departure_end:
            request_params["departure_end"] = params.departure_end
        if params.updated_since:
            request_params["updated_since"] = params.updated_since

        # Parámetros especiales
        if params.scroll is not None:
            request_params["scroll"] = params.scroll
        if params.in_house_today is not None:
            request_params["in_house_today"] = params.in_house_today
        if params.status:
            request_params["status"] = self._format_status_list(params.status)
        if params.group_id:
            request_params["group_id"] = params.group_id
        if params.checkin_office_id:
            request_params["checkin_office_id"] = params.checkin_office_id

        return request_params

    def _format_id_list(self, ids: Union[int, List[int]]) -> str:
        """Formatear lista de IDs para la API"""
        if isinstance(ids, int):
            return str(ids)
        return ",".join(map(str, ids))

    def _format_status_list(self, status: Union[str, List[str]]) -> str:
        """Formatear lista de estados para la API"""
        if isinstance(status, str):
            return status
        return ",".join(status)

    def _process_response(self, response: Dict[str, Any]) -> SearchReservationsResponse:
        """Procesar respuesta de la API"""
        return SearchReservationsResponse(
            **{
                "_embedded": response.get("_embedded", {}),
                "page": response.get("page", 1),
                "page_count": response.get("page_count", 1),
                "page_size": response.get("page_size", 10),
                "total_items": response.get("total_items", 0),
                "_links": response.get("_links", {}),
            }
        )
