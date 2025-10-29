"""
Herramienta para buscar amenidades
"""

from typing import Any, Dict

from ..schemas.amenity import AmenitySearchParams, AmenitySearchResponse
from ..utils.exceptions import TrackHSAPIError
from .base import BaseTool


class SearchAmenitiesTool(BaseTool):
    """Herramienta para buscar amenidades en TrackHS"""

    @property
    def name(self) -> str:
        return "search_amenities"

    @property
    def description(self) -> str:
        return """
        Buscar amenidades/servicios disponibles en el sistema TrackHS.

        Esta herramienta implementa la API completa de búsqueda de amenidades de TrackHS
        con validación robusta, manejo de errores mejorado, logging estructurado y
        siguiendo las mejores prácticas de FastMCP 2.0+.

        FUNCIONALIDADES PRINCIPALES:
        - Búsqueda por texto en nombre de amenidad
        - Filtros por características (público, filtrable, buscable)
        - Filtros por grupo de amenidades
        - Búsqueda por tipos de plataformas OTA (Airbnb, HomeAway, TripAdvisor, Marriott)
        - Ordenamiento personalizable
        - Paginación flexible

        Args:
            page: Número de página (1-based)
            size: Tamaño de página (1-100)
            search: Búsqueda en nombre de amenidad
            group_id: Filtrar por ID de grupo específico
            is_public: Solo amenidades públicas
            public_searchable: Solo amenidades buscables públicamente
            is_filterable: Solo amenidades filtrables
            homeaway_type: Buscar por tipo de HomeAway
            airbnb_type: Buscar por tipo de Airbnb
            tripadvisor_type: Buscar por tipo de TripAdvisor
            marriott_type: Buscar por tipo de Marriott
            sort_column: Columna para ordenar
            sort_direction: Dirección de ordenamiento

        Returns:
            Lista de amenidades encontradas
        """

    @property
    def input_schema(self) -> type:
        return AmenitySearchParams

    @property
    def output_schema(self) -> type:
        return AmenitySearchResponse

    def _execute_logic(self, validated_input: AmenitySearchParams) -> Dict[str, Any]:
        """
        Ejecuta la búsqueda de amenidades

        Args:
            validated_input: Parámetros de búsqueda validados

        Returns:
            Resultado de la búsqueda
        """
        # Preparar parámetros para la API
        params = self._prepare_api_params(validated_input)

        # Realizar llamada a la API
        try:
            result = self.api_client.get("api/pms/units/amenities", params)

            # Procesar resultado
            processed_result = self._process_api_response(result)

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error en búsqueda de amenidades",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "search_params": params,
                },
            )
            raise TrackHSAPIError(f"Error buscando amenidades: {str(e)}")

    def _prepare_api_params(
        self, validated_input: AmenitySearchParams
    ) -> Dict[str, Any]:
        """
        Prepara parámetros para la llamada a la API

        Args:
            validated_input: Parámetros validados

        Returns:
            Parámetros formateados para la API
        """
        params = {"page": validated_input.page, "size": validated_input.size}

        if validated_input.search:
            params["search"] = validated_input.search
        if validated_input.group_id:
            params["groupId"] = validated_input.group_id
        if validated_input.is_public is not None:
            params["isPublic"] = 1 if validated_input.is_public else 0
        if validated_input.public_searchable is not None:
            params["publicSearchable"] = 1 if validated_input.public_searchable else 0
        if validated_input.is_filterable is not None:
            params["isFilterable"] = 1 if validated_input.is_filterable else 0
        if validated_input.homeaway_type:
            params["homeawayType"] = validated_input.homeaway_type
        if validated_input.airbnb_type:
            params["airbnbType"] = validated_input.airbnb_type
        if validated_input.tripadvisor_type:
            params["tripadvisorType"] = validated_input.tripadvisor_type
        if validated_input.marriott_type:
            params["marriottType"] = validated_input.marriott_type
        if validated_input.sort_column:
            params["sortColumn"] = validated_input.sort_column
        if validated_input.sort_direction:
            params["sortDirection"] = validated_input.sort_direction

        return params

    def _process_api_response(self, api_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API

        Args:
            api_result: Respuesta de la API

        Returns:
            Resultado procesado
        """
        # Calcular información de paginación
        total_items = api_result.get("total_items", 0)
        current_page = api_result.get("page", 1)
        page_size = api_result.get("size", 10)
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar amenidades
        amenities = api_result.get("amenities", [])
        processed_amenities = []

        for amenity in amenities:
            processed_amenity = self._process_amenity(amenity)
            processed_amenities.append(processed_amenity)

        return {
            "amenities": processed_amenities,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _process_amenity(self, amenity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una amenidad individual

        Args:
            amenity: Datos de la amenidad

        Returns:
            Amenidad procesada
        """
        # Mapear campos de la API al schema
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

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}
