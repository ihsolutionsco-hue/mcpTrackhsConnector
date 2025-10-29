"""
Herramienta para buscar unidades de alojamiento
"""

from typing import Any, Dict, List, Optional

from schemas.unit import UnitSearchParams, UnitSearchResponse
from utils.exceptions import TrackHSAPIError
from utils.response_validators import ResponseValidator

from .base import BaseTool


class SearchUnitsTool(BaseTool):
    """Herramienta para buscar unidades de alojamiento en TrackHS"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = ResponseValidator()
        self.validator.set_logger(self.logger)

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
        # Log de inicio de búsqueda
        self.logger.info(
            "Iniciando búsqueda de unidades",
            extra={
                "input_params": validated_input.model_dump(),
                "has_filters": self._has_meaningful_filters(validated_input),
                "filter_count": self._count_filters(validated_input),
            },
        )

        # Preparar parámetros para la API
        params = self._prepare_api_params(validated_input)

        # Log de parámetros preparados
        self.logger.info(
            "Parámetros preparados para API",
            extra={
                "api_params": params,
                "param_count": len(params),
                "boolean_conversions": self._get_boolean_conversions(validated_input),
                "range_filters": self._get_range_filters(validated_input),
            },
        )

        # Realizar llamada a la API
        try:
            result = self.api_client.get("api/pms/units", params)

            # Log de respuesta de API
            self.logger.info(
                "Respuesta recibida de API",
                extra={
                    "response_type": type(result).__name__,
                    "response_keys": (
                        list(result.keys()) if isinstance(result, dict) else "not_dict"
                    ),
                    "has_units": (
                        "units" in result if isinstance(result, dict) else False
                    ),
                    "units_count": (
                        len(result.get("units", [])) if isinstance(result, dict) else 0
                    ),
                    "total_items": (
                        result.get("total_items", "not_found")
                        if isinstance(result, dict)
                        else "not_found"
                    ),
                },
            )

            # Procesar resultado
            processed_result = self._process_api_response(result)

            # Validar respuesta contra filtros aplicados
            validation_report = self._validate_response_against_filters(
                processed_result.get("units", []), params
            )

            # Log de resultado final
            self.logger.info(
                "Búsqueda completada exitosamente",
                extra={
                    "final_units_count": len(processed_result.get("units", [])),
                    "total_items": processed_result.get("total_items", 0),
                    "total_pages": processed_result.get("total_pages", 0),
                    "current_page": processed_result.get("current_page", 0),
                    "has_next": processed_result.get("has_next", False),
                    "has_prev": processed_result.get("has_prev", False),
                    "validation_summary": validation_report.summary,
                    "validation_issues": validation_report.has_issues,
                },
            )

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error en búsqueda de unidades",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "search_params": params,
                    "input_params": validated_input.model_dump(),
                },
            )
            raise TrackHSAPIError(f"Error buscando unidades: {str(e)}")

    def _has_meaningful_filters(self, validated_input: UnitSearchParams) -> bool:
        """Verifica si hay filtros significativos aplicados"""
        meaningful_fields = [
            "search",
            "term",
            "unit_code",
            "short_name",
            "bedrooms",
            "bathrooms",
            "occupancy",
            "min_bedrooms",
            "max_bedrooms",
            "min_bathrooms",
            "max_bathrooms",
            "min_occupancy",
            "max_occupancy",
            "is_active",
            "is_bookable",
            "pets_friendly",
            "unit_status",
            "arrival",
            "departure",
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
        ]

        return any(
            getattr(validated_input, field) is not None for field in meaningful_fields
        )

    def _count_filters(self, validated_input: UnitSearchParams) -> int:
        """Cuenta el número de filtros aplicados"""
        meaningful_fields = [
            "search",
            "term",
            "unit_code",
            "short_name",
            "bedrooms",
            "bathrooms",
            "occupancy",
            "min_bedrooms",
            "max_bedrooms",
            "min_bathrooms",
            "max_bathrooms",
            "min_occupancy",
            "max_occupancy",
            "is_active",
            "is_bookable",
            "pets_friendly",
            "unit_status",
            "arrival",
            "departure",
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
        ]

        return sum(
            1
            for field in meaningful_fields
            if getattr(validated_input, field) is not None
        )

    def _get_boolean_conversions(
        self, validated_input: UnitSearchParams
    ) -> Dict[str, Any]:
        """Obtiene las conversiones booleanas aplicadas"""
        conversions = {}
        boolean_fields = [
            "is_active",
            "is_bookable",
            "pets_friendly",
            "allow_unit_rates",
        ]

        for field in boolean_fields:
            value = getattr(validated_input, field)
            if value is not None:
                conversions[field] = {"original": value, "converted": 1 if value else 0}

        return conversions

    def _get_range_filters(self, validated_input: UnitSearchParams) -> Dict[str, Any]:
        """Obtiene los filtros de rango aplicados"""
        range_filters = {}
        range_fields = [
            "min_bedrooms",
            "max_bedrooms",
            "min_bathrooms",
            "max_bathrooms",
            "min_occupancy",
            "max_occupancy",
        ]

        for field in range_fields:
            value = getattr(validated_input, field)
            if value is not None:
                range_filters[field] = value

        return range_filters

    def _validate_response_against_filters(
        self, units: List[Dict[str, Any]], search_params: Dict[str, Any]
    ) -> Any:
        """
        Valida que la respuesta de la API cumpla con los filtros aplicados

        Args:
            units: Lista de unidades devueltas por la API
            search_params: Parámetros de búsqueda enviados a la API

        Returns:
            ValidationReport con el resultado de las validaciones
        """
        try:
            validation_report = self.validator.validate_units_response(
                units, search_params
            )

            # Log detallado de validación
            if validation_report.has_issues:
                self.logger.warning(
                    "Se detectaron inconsistencias en la respuesta de la API",
                    extra={
                        "validation_summary": validation_report.summary,
                        "failed_validations": validation_report.failed_validations,
                        "total_validations": validation_report.total_validations,
                        "issues": [
                            {
                                "field": r.field_name,
                                "message": r.message,
                                "invalid_count": r.invalid_count,
                            }
                            for r in validation_report.results
                            if not r.is_valid
                        ],
                    },
                )
            else:
                self.logger.debug(
                    "Validación de respuesta exitosa",
                    extra={
                        "validation_summary": validation_report.summary,
                        "total_validations": validation_report.total_validations,
                    },
                )

            return validation_report

        except Exception as e:
            self.logger.error(
                f"Error durante validación de respuesta: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "units_count": len(units),
                    "search_params": search_params,
                },
            )
            # Retornar un reporte vacío en caso de error
            from utils.response_validators import ValidationReport

            return ValidationReport(
                total_validations=0,
                passed_validations=0,
                failed_validations=0,
                results=[],
                summary="Error durante validación",
                has_issues=True,
            )

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

        # Parámetros de características físicas (camelCase según documentación oficial)
        if validated_input.bedrooms is not None:
            params["bedrooms"] = validated_input.bedrooms
        if validated_input.min_bedrooms is not None:
            params["minBedrooms"] = validated_input.min_bedrooms  # camelCase
        if validated_input.max_bedrooms is not None:
            params["maxBedrooms"] = validated_input.max_bedrooms  # camelCase
        if validated_input.bathrooms is not None:
            params["bathrooms"] = validated_input.bathrooms
        if validated_input.min_bathrooms is not None:
            params["minBathrooms"] = validated_input.min_bathrooms  # camelCase
        if validated_input.max_bathrooms is not None:
            params["maxBathrooms"] = validated_input.max_bathrooms  # camelCase
        if validated_input.occupancy is not None:
            params["occupancy"] = validated_input.occupancy
        if validated_input.min_occupancy is not None:
            params["minOccupancy"] = validated_input.min_occupancy  # camelCase
        if validated_input.max_occupancy is not None:
            params["maxOccupancy"] = validated_input.max_occupancy  # camelCase

        # Parámetros de estado (camelCase según documentación oficial)
        if validated_input.is_active is not None:
            params["isActive"] = 1 if validated_input.is_active else 0  # camelCase
        if validated_input.is_bookable is not None:
            params["isBookable"] = 1 if validated_input.is_bookable else 0  # camelCase
        if validated_input.pets_friendly is not None:
            params["petsFriendly"] = (
                1 if validated_input.pets_friendly else 0
            )  # camelCase
        if validated_input.unit_status:
            params["unitStatus"] = validated_input.unit_status  # camelCase

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
        # Manejar diferentes estructuras de respuesta de la API
        if "_embedded" in api_result:
            # Estructura con _embedded
            embedded_data = api_result.get("_embedded", {})
            units = embedded_data.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
        elif "embedded" in api_result:
            # Estructura con embedded (sin guión bajo)
            embedded_data = api_result.get("embedded", {})
            units = embedded_data.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)
        elif "data" in api_result:
            # Estructura con data
            data = api_result.get("data", {})
            units = data.get("units", [])
            total_items = data.get("total_items", 0)
            current_page = data.get("page", 1)
            page_size = data.get("size", 10)
        else:
            # Estructura directa
            units = api_result.get("units", [])
            total_items = api_result.get("total_items", 0)
            current_page = api_result.get("page", 1)
            page_size = api_result.get("size", 10)

        # Calcular información de paginación
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar unidades
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
