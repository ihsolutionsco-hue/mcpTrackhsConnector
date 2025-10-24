"""
Herramienta MCP para realizar análisis de negocio sobre amenidades.
Utiliza la herramienta search_amenities para obtener datos y luego aplica lógica
de negocio para identificar oportunidades y recomendaciones.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_amenities import SearchAmenitiesUseCase
from ...domain.entities.amenities import SearchAmenitiesParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler


def register_analyze_amenities_business(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta analyze_amenities_business"""

    @mcp.tool(name="analyze_amenities_business")
    @error_handler("analyze_amenities_business")
    async def analyze_amenities_business(
        search: Optional[str] = Field(
            default=None,
            description="Optional full-text search term to narrow down amenities for analysis. E.g., 'pool', 'wifi', 'kitchen'.",
            max_length=200,
        ),
        group_id: Optional[int] = Field(
            default=None,
            description="Optional filter by amenity group ID for focused analysis. E.g., 4 for Family, 7 for Accessibility, 14 for Pool.",
            ge=1,
        ),
        is_public: Optional[int] = Field(
            default=None,
            description="Filter by public status: 0=private, 1=public. Use 1 to analyze guest-visible amenities.",
            ge=0,
            le=1,
        ),
        public_searchable: Optional[int] = Field(
            default=None,
            description="Filter by searchable status: 0=not searchable, 1=searchable. Use 1 to analyze amenities guests can actively search for.",
            ge=0,
            le=1,
        ),
        is_filterable: Optional[int] = Field(
            default=None,
            description="Filter by filterable status: 0=not filterable, 1=filterable. Use 1 to analyze amenities usable as search filters.",
            ge=0,
            le=1,
        ),
    ) -> Dict[str, Any]:
        """
        Performs a business-oriented analysis of amenities, identifying opportunities
        for marketing, revenue optimization, and guest experience improvement.

        This tool leverages the `search_amenities` functionality to retrieve amenity data
        and then applies business logic to provide actionable insights.

        BUSINESS USE CASES:
        - Identify premium amenities for luxury positioning.
        - Discover family-friendly amenities for targeted marketing.
        - Analyze accessibility features to promote inclusive hospitality.
        - Pinpoint amenities that are publicly searchable to improve guest visibility.
        - Detect gaps in amenity offerings (e.g., pet-friendly options).
        - Evaluate potential for new amenity packages (e.g., "Work From Paradise").

        Args:
            search (Optional[str]): A search term to filter amenities before analysis.
            group_id (Optional[int]): Filter amenities by a specific group ID.
            is_public (Optional[int]): Filter by public visibility (0=private, 1=public).
            public_searchable (Optional[int]): Filter by public searchability (0=not searchable, 1=searchable).
            is_filterable (Optional[int]): Filter by filterability (0=not filterable, 1=filterable).

        Returns:
            Dict[str, Any]: A dictionary containing the business analysis, including counts
                            of different amenity types, identified opportunities, revenue impact,
                            target audience, and marketing recommendations.
        """
        try:
            # Usar search_amenities para obtener todas las amenidades relevantes
            search_params = SearchAmenitiesParams(
                page=1,
                size=1000,  # Max size to get as many amenities as possible for analysis
                sort_column="id",
                sort_direction="asc",
                search=search,
                group_id=group_id,
                is_public=is_public,
                public_searchable=public_searchable,
                is_filterable=is_filterable,
            )

            use_case = SearchAmenitiesUseCase(api_client)
            search_result = await use_case.execute(search_params)

            amenities_data: List[Dict[str, Any]] = search_result.get(
                "_embedded", {}
            ).get("amenities", [])

            # Realizar el análisis de negocio
            analysis = _perform_simple_business_analysis(amenities_data, search_params)

            return analysis

        except Exception as e:
            # Re-lanzar errores de validación o API
            raise ValidationError(
                f"Error during amenity business analysis: {str(e)}", "analysis"
            )


def _perform_simple_business_analysis(
    amenities: List[Dict[str, Any]], params: SearchAmenitiesParams
) -> Dict[str, Any]:
    """
    Realizar análisis de negocio simplificado de las amenidades.
    """
    # Inicializar contadores
    total_amenities = len(amenities)
    premium_count = 0
    family_count = 0
    accessibility_count = 0
    searchable_count = 0

    # Palabras clave para categorización
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

    # Analizar cada amenidad
    for amenity in amenities:
        name = amenity.get("name", "").lower()

        # Contar por categorías
        if any(keyword in name for keyword in premium_keywords):
            premium_count += 1
        if any(keyword in name for keyword in family_keywords):
            family_count += 1
        if any(keyword in name for keyword in accessibility_keywords):
            accessibility_count += 1
        if amenity.get("publicSearchable"):
            searchable_count += 1

    # Construir análisis base
    analysis = {
        "total_amenities": total_amenities,
        "premium_count": premium_count,
        "family_count": family_count,
        "accessibility_count": accessibility_count,
        "searchable_count": searchable_count,
        "business_opportunities": [],
        "revenue_impact": "Standard",
        "target_audience": "All guests",
        "marketing_recommendations": [],
    }

    # Generar oportunidades de negocio
    if premium_count > 0:
        analysis["business_opportunities"].append(
            "Premium amenities identified for luxury positioning"
        )
        analysis["marketing_recommendations"].append(
            "Create 'Luxury Escape' packages highlighting premium amenities"
        )
        analysis["revenue_impact"] = "High (+50-100%)"

    if family_count > 0:
        analysis["business_opportunities"].append(
            "Family-friendly amenities available for targeted marketing"
        )
        analysis["marketing_recommendations"].append(
            "Develop 'Family Paradise' packages with family amenities"
        )
        if analysis["revenue_impact"] == "Standard":
            analysis["revenue_impact"] = "Medium (+25-50%)"

    if accessibility_count > 0:
        analysis["business_opportunities"].append(
            "Accessibility features present for inclusive hospitality"
        )
        analysis["marketing_recommendations"].append(
            "Promote accessibility features to guests with special needs"
        )
        if analysis["revenue_impact"] == "Standard":
            analysis["revenue_impact"] = "Market expansion"

    if searchable_count == 0 and total_amenities > 0:
        analysis["business_opportunities"].append(
            "Critical: Most amenities are not publicly searchable, limiting guest discovery"
        )
        analysis["marketing_recommendations"].append(
            "Prioritize marking key amenities as 'publicSearchable=1'"
        )
        analysis["revenue_impact"] = "Significant missed opportunity"

    return analysis
