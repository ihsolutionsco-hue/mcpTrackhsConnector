"""
Caso de uso para buscar amenidades
MEJORAS IMPLEMENTADAS:
- Mejor logging con información de negocio
- Validaciones más robustas
- Manejo de errores específicos
- Optimizaciones de rendimiento
- Documentación de casos de uso
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

        # Realizar petición a la API con logging mejorado
        import logging

        logger = logging.getLogger(__name__)

        # Log de información de negocio
        business_context = self._get_business_context(params)
        logger.info("🏠 AMENITIES SEARCH - Business Context:")
        logger.info(f"  📊 Search Type: {business_context['search_type']}")
        logger.info(f"  🎯 Target Audience: {business_context['target_audience']}")
        logger.info(f"  💰 Revenue Impact: {business_context['revenue_impact']}")
        logger.info(f"  🔍 Search Strategy: {business_context['search_strategy']}")

        # Log técnico
        logger.info("🔧 AMENITIES API Request - Technical Details:")
        logger.info(f"  📡 Endpoint: /api/pms/units/amenities")
        logger.info(f"  📋 Params: {request_params}")
        logger.info(f"  📊 Params count: {len(request_params)}")
        logger.info(f"  🔍 Search term: {params.search or 'None'}")
        logger.info(f"  📂 Group filter: {params.group_id or 'None'}")
        logger.info(f"  👁️ Public filter: {params.is_public or 'None'}")
        logger.info(f"  🔎 Searchable filter: {params.public_searchable or 'None'}")

        response = await self.api_client.get(
            "/api/pms/units/amenities", params=request_params
        )

        # Procesar respuesta con análisis de negocio
        result = self._process_response(response)

        # Log de resultados con contexto de negocio
        if result and "_embedded" in result and "amenities" in result["_embedded"]:
            amenities = result["_embedded"]["amenities"]
            business_analysis = self._analyze_business_impact(amenities, params)

            logger.info("📈 AMENITIES SEARCH - Business Analysis:")
            logger.info(f"  📊 Total found: {len(amenities)} amenities")
            logger.info(f"  🎯 Premium amenities: {business_analysis['premium_count']}")
            logger.info(
                f"  👨‍👩‍👧 Family amenities: {business_analysis['family_count']}"
            )
            logger.info(
                f"  ♿ Accessibility amenities: {business_analysis['accessibility_count']}"
            )
            logger.info(
                f"  🔍 Guest-searchable: {business_analysis['searchable_count']}"
            )
            logger.info(
                f"  💡 Business opportunities: {business_analysis['opportunities']}"
            )

        return result

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

    def _get_business_context(self, params: SearchAmenitiesParams) -> Dict[str, str]:
        """Analizar el contexto de negocio de la búsqueda"""
        context = {
            "search_type": "General",
            "target_audience": "All guests",
            "revenue_impact": "Standard",
            "search_strategy": "Basic search",
        }

        # Analizar tipo de búsqueda
        if params.search:
            search_term = params.search.lower()
            if search_term in ["pool", "hot tub", "sauna", "gym", "concierge", "chef"]:
                context["search_type"] = "Premium amenities"
                context["target_audience"] = "Luxury guests"
                context["revenue_impact"] = "High (+50-100%)"
                context["search_strategy"] = "Premium positioning"
            elif search_term in ["wifi", "internet", "desk", "printer"]:
                context["search_type"] = "Work amenities"
                context["target_audience"] = "Remote workers"
                context["revenue_impact"] = "Medium (+20%)"
                context["search_strategy"] = "Work from paradise"
            elif search_term in ["baby", "children", "family", "crib"]:
                context["search_type"] = "Family amenities"
                context["target_audience"] = "Families with children"
                context["revenue_impact"] = "Medium (+25-50%)"
                context["search_strategy"] = "Family-friendly positioning"
            elif search_term in ["accessible", "wheelchair", "mobility"]:
                context["search_type"] = "Accessibility amenities"
                context["target_audience"] = "Guests with disabilities"
                context["revenue_impact"] = "Market expansion"
                context["search_strategy"] = "Inclusive hospitality"

        # Analizar filtros de grupo
        if params.group_id:
            group_mapping = {
                2: ("Essentials", "All guests", "Standard", "Basic amenities"),
                4: (
                    "Family amenities",
                    "Families",
                    "Medium (+25-50%)",
                    "Family positioning",
                ),
                7: (
                    "Accessibility",
                    "Guests with disabilities",
                    "Market expansion",
                    "Inclusive hospitality",
                ),
                10: (
                    "Kitchen amenities",
                    "Self-catering guests",
                    "Medium (+15-30%)",
                    "Kitchen positioning",
                ),
                14: (
                    "Pool amenities",
                    "Leisure guests",
                    "High (+30-60%)",
                    "Pool positioning",
                ),
                19: (
                    "Entertainment",
                    "Groups/families",
                    "Medium (+20-40%)",
                    "Entertainment positioning",
                ),
            }
            if params.group_id in group_mapping:
                (
                    context["search_type"],
                    context["target_audience"],
                    context["revenue_impact"],
                    context["search_strategy"],
                ) = group_mapping[params.group_id]

        # Analizar filtros de visibilidad
        if params.public_searchable == 1:
            context["search_strategy"] = "Guest-searchable amenities"
        if params.is_public == 1:
            context["search_strategy"] = "Public marketing amenities"

        return context

    def _analyze_business_impact(
        self, amenities: list, params: SearchAmenitiesParams
    ) -> Dict[str, Any]:
        """Analizar el impacto de negocio de los resultados"""
        analysis = {
            "premium_count": 0,
            "family_count": 0,
            "accessibility_count": 0,
            "searchable_count": 0,
            "opportunities": [],
        }

        premium_keywords = [
            "hot tub",
            "sauna",
            "gym",
            "concierge",
            "chef",
            "massage",
            "ocean",
            "private pool",
        ]
        family_keywords = ["baby", "children", "crib", "high chair", "toys", "family"]
        accessibility_keywords = [
            "accessible",
            "wheelchair",
            "mobility",
            "height",
            "grab rails",
        ]

        for amenity in amenities:
            name = amenity.get("name", "").lower()

            # Contar amenidades premium
            if any(keyword in name for keyword in premium_keywords):
                analysis["premium_count"] += 1

            # Contar amenidades familiares
            if any(keyword in name for keyword in family_keywords):
                analysis["family_count"] += 1

            # Contar amenidades de accesibilidad
            if any(keyword in name for keyword in accessibility_keywords):
                analysis["accessibility_count"] += 1

            # Contar amenidades buscables
            if amenity.get("publicSearchable"):
                analysis["searchable_count"] += 1

        # Generar oportunidades de negocio
        if analysis["premium_count"] > 0:
            analysis["opportunities"].append(
                "Premium amenities available for luxury positioning"
            )
        if analysis["family_count"] > 0:
            analysis["opportunities"].append(
                "Family amenities for family-friendly marketing"
            )
        if analysis["accessibility_count"] > 0:
            analysis["opportunities"].append(
                "Accessibility amenities for inclusive hospitality"
            )
        if analysis["searchable_count"] == 0 and len(amenities) > 0:
            analysis["opportunities"].append(
                "Consider enabling publicSearchable for better guest visibility"
            )

        return analysis
