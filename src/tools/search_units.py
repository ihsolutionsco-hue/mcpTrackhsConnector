"""
Herramienta para buscar unidades de alojamiento
"""

from typing import Any, Dict, List, Optional

from schemas.unit import UnitSearchParams, UnitSearchResponse
from utils.exceptions import TrackHSAPIError

from .base import BaseTool


class SearchUnitsTool(BaseTool):
    """Herramienta para buscar unidades de alojamiento en TrackHS"""

    @property
    def name(self) -> str:
        return "search_units"

    @property
    def description(self) -> str:
        return """
        Buscar unidades de alojamiento disponibles en TrackHS con filtros avanzados.

        Esta herramienta implementa la API completa de búsqueda de unidades de TrackHS
        con todos los parámetros disponibles según la documentación oficial.

        FUNCIONALIDADES PRINCIPALES:
        - Búsqueda por características físicas (dormitorios, baños, capacidad)
        - Filtros por estado (activa, reservable, pet-friendly, estado de limpieza)
        - Búsqueda de texto (nombre, descripción, código, término)
        - Filtros por fechas de disponibilidad (arrival/departure)
        - Filtros por IDs (nodo, amenidad, tipo de unidad, propietario, etc.)
        - Ordenamiento personalizable
        - Paginación flexible

        Args:
            page: Número de página (1-based)
            size: Tamaño de página (1-100)
            search: Búsqueda de texto en nombre o descripciones
            bedrooms: Número exacto de dormitorios
            bathrooms: Número exacto de baños
            min_occupancy: Capacidad mínima
            max_occupancy: Capacidad máxima
            is_active: Solo unidades activas
            is_bookable: Solo unidades reservables
            pets_friendly: Solo unidades pet-friendly
            unit_status: Estado de la unidad
            arrival: Fecha de llegada para verificar disponibilidad
            departure: Fecha de salida para verificar disponibilidad
            amenity_id: IDs de amenidades requeridas
            node_id: IDs de nodos
            unit_type_id: IDs de tipos de unidad
            sort_column: Columna para ordenar
            sort_direction: Dirección de ordenamiento

        Returns:
            Lista de unidades encontradas con información detallada
        """

    @property
    def input_schema(self) -> type:
        return UnitSearchParams

    @property
    def output_schema(self) -> type:
        return UnitSearchResponse

    def _execute_logic(self, validated_input: UnitSearchParams) -> Dict[str, Any]:
        """
        Ejecuta la búsqueda de unidades

        Args:
            validated_input: Parámetros de búsqueda validados

        Returns:
            Resultado de la búsqueda
        """
        # Preparar parámetros para la API
        params = self._prepare_api_params(validated_input)

        # Realizar llamada a la API
        try:
            result = self.api_client.get("api/pms/units", params)

            # Procesar resultado
            processed_result = self._process_api_response(result)

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error en búsqueda de unidades",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "search_params": params,
                },
            )
            raise TrackHSAPIError(f"Error buscando unidades: {str(e)}")

    def _prepare_api_params(self, validated_input: UnitSearchParams) -> Dict[str, Any]:
        """
        Prepara parámetros para la llamada a la API

        Args:
            validated_input: Parámetros validados

        Returns:
            Parámetros formateados para la API
        """
        params = {"page": validated_input.page, "size": validated_input.size}

        # Parámetros de búsqueda de texto
        if validated_input.search:
            params["search"] = validated_input.search
        if validated_input.term:
            params["term"] = validated_input.term
        if validated_input.unit_code:
            params["unit_code"] = validated_input.unit_code
        if validated_input.short_name:
            params["short_name"] = validated_input.short_name

        # Parámetros de características físicas
        if validated_input.bedrooms is not None:
            params["bedrooms"] = validated_input.bedrooms
        if validated_input.bathrooms is not None:
            params["bathrooms"] = validated_input.bathrooms
        if validated_input.min_occupancy is not None:
            params["min_occupancy"] = validated_input.min_occupancy
        if validated_input.max_occupancy is not None:
            params["max_occupancy"] = validated_input.max_occupancy

        # Parámetros de estado
        if validated_input.is_active is not None:
            params["is_active"] = 1 if validated_input.is_active else 0
        if validated_input.is_bookable is not None:
            params["is_bookable"] = 1 if validated_input.is_bookable else 0
        if validated_input.pets_friendly is not None:
            params["pets_friendly"] = 1 if validated_input.pets_friendly else 0
        if validated_input.unit_status:
            params["unit_status"] = validated_input.unit_status

        # Parámetros de fechas
        if validated_input.arrival:
            params["arrival"] = validated_input.arrival
        if validated_input.departure:
            params["departure"] = validated_input.departure

        # Parámetros de IDs
        if validated_input.amenity_id:
            params["amenity_id"] = validated_input.amenity_id
        if validated_input.node_id:
            params["node_id"] = validated_input.node_id
        if validated_input.unit_type_id:
            params["unit_type_id"] = validated_input.unit_type_id
        if validated_input.owner_id:
            params["owner_id"] = validated_input.owner_id
        if validated_input.company_id:
            params["company_id"] = validated_input.company_id
        if validated_input.channel_id:
            params["channel_id"] = validated_input.channel_id
        if validated_input.lodging_type_id:
            params["lodging_type_id"] = validated_input.lodging_type_id
        if validated_input.bed_type_id:
            params["bed_type_id"] = validated_input.bed_type_id
        if validated_input.amenity_all:
            params["amenity_all"] = validated_input.amenity_all
        if validated_input.unit_ids:
            params["unit_ids"] = validated_input.unit_ids

        # Parámetros de ordenamiento
        if validated_input.sort_column:
            params["sort_column"] = validated_input.sort_column
        if validated_input.sort_direction:
            params["sort_direction"] = validated_input.sort_direction

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
