"""
Herramienta MCP para buscar amenidades en Track HS Channel API
Basado en la especificación completa de la API Get Unit Amenities Collection

MEJORAS IMPLEMENTADAS:
- Descripciones mejoradas basadas en testing real
- Validaciones más robustas
- Mejor manejo de errores específicos
- Documentación de casos de uso de negocio
- Optimizaciones de rendimiento
"""

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.search_amenities import SearchAmenitiesUseCase
from ...domain.entities.amenities import SearchAmenitiesParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler
from ..utils.type_normalization import normalize_binary_int, normalize_int


def register_search_amenities(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_amenities"""

    @mcp.tool(name="search_amenities")
    @error_handler("search_amenities")
    async def search_amenities(
        page: int = Field(
            default=1,
            description="Page number (1-based indexing). Max 10,000 total results (10,000 pages max). Example: 1 for first page, 2 for second page.",
            ge=1,
            le=10000,
        ),
        size: int = Field(
            default=25,
            description="Items per page. Max 1,000 per page. Recommended: 25-100 for optimal performance. Example: 25 for standard pagination, 100 for bulk analysis.",
            ge=1,
            le=1000,
        ),
        sort_column: Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ] = Field(
            default="order",
            description="Field to sort by. Options: id (by ID), order (by display order), isPublic (by public status), publicSearchable (by searchability), isFilterable (by filterability), createdAt (by creation date). Use 'createdAt' to find newest amenities.",
        ),
        sort_direction: Literal["asc", "desc"] = Field(
            default="asc",
            description="Sort direction: 'asc' (ascending) or 'desc' (descending). Use 'desc' with 'createdAt' to find newest amenities first.",
        ),
        search: Optional[str] = Field(
            default=None,
            description="Full-text search in amenity ID and name fields. Examples: 'pool' (finds pool-related amenities), 'wifi' (finds internet amenities), 'kitchen' (finds kitchen amenities), 'accessible' (finds accessibility amenities). Maximum 200 characters.",
            max_length=200,
        ),
        group_id: Optional[int] = Field(
            default=None,
            description="Filter by amenity group ID (positive integer). Common groups: 2=Essentials, 4=Family, 7=Accessibility, 10=Kitchen, 14=Pool, 19=Entertainment. Use to find amenities by category.",
            ge=1,
        ),
        is_public: Optional[int] = Field(
            default=None,
            description="Filter by public status: 0=private (internal only), 1=public (visible to guests). Use 1 to find guest-visible amenities for marketing.",
            ge=0,
            le=1,
        ),
        public_searchable: Optional[int] = Field(
            default=None,
            description="Filter by searchable status: 0=not searchable (not in guest filters), 1=searchable (appears in guest search filters). Use 1 to find amenities that guests can actively search for.",
            ge=0,
            le=1,
        ),
        is_filterable: Optional[int] = Field(
            default=None,
            description="Filter by filterable status: 0=not filterable (not in filters), 1=filterable (appears in filter options). Use 1 to find amenities that can be used as search filters.",
            ge=0,
            le=1,
        ),
    ) -> Dict[str, Any]:
        """
        Search amenities in Track HS Channel API with advanced filtering and pagination.

        BUSINESS USE CASES:
        🏠 PROPERTY MANAGEMENT:
        - Find all amenities for property setup: search="", group_id=2 (Essentials)
        - Find family-friendly amenities: group_id=4 (Family)
        - Find accessibility amenities: group_id=7 (Accessibility)
        - Find premium amenities: search="hot tub" or search="sauna"

        📊 MARKETING & COMPETITIVE ANALYSIS:
        - Find guest-searchable amenities: public_searchable=1
        - Find public amenities for marketing: is_public=1
        - Find newest amenities: sort_column="createdAt", sort_direction="desc"

        💰 REVENUE OPTIMIZATION:
        - Find WiFi amenities: search="wifi" (9 different speed options)
        - Find pool amenities: search="pool" (8 different types)
        - Find luxury amenities: search="concierge" or search="chef"

        🎯 GUEST EXPERIENCE:
        - Find family amenities: search="baby" or search="children"
        - Find workspace amenities: search="desk" or search="printer"
        - Find entertainment: group_id=19 (Entertainment)

        TECHNICAL FEATURES:
        - Comprehensive filtering by group, public status, searchability, filterability
        - Flexible sorting options (id, order, isPublic, publicSearchable, isFilterable, createdAt)
        - Pagination support (max 10k results, 1k per page)
        - Full-text search in amenity names and IDs
        - Complete amenity data with embedded objects and OTA compatibility

        RETURNS: Complete amenity data including:
        - Basic info (id, name, group)
        - OTA compatibility (Airbnb, HomeAway, Marriott, Booking.com, Expedia)
        - Public visibility settings (isPublic, publicSearchable, isFilterable)
        - Creation and update timestamps
        - Pagination metadata
        """
        # Detectar y aplicar defaults para FieldInfo objects (cuando se llama directamente sin FastMCP)
        if type(sort_column).__name__ == "FieldInfo":
            sort_column = "order"
        if type(sort_direction).__name__ == "FieldInfo":
            sort_direction = "asc"
        if type(search).__name__ == "FieldInfo":
            search = None

        # Normalizar parámetros numéricos primero (para compatibilidad JSON-RPC)
        page = normalize_int(page, "page")
        size = normalize_int(size, "size")
        group_id = normalize_int(group_id, "group_id")

        # Asegurar defaults para page y size si normalize_int retorna None (FieldInfo objects)
        if page is None:
            page = 1
        if size is None:
            size = 25

        # Normalizar flags booleanos (0/1)
        is_public = normalize_binary_int(is_public, "is_public")
        public_searchable = normalize_binary_int(public_searchable, "public_searchable")
        is_filterable = normalize_binary_int(is_filterable, "is_filterable")

        # Validar límite total de resultados (10k máximo) - validación de negocio
        # Ajustar page para cálculo (API usa 1-based, pero calculamos con 0-based)
        adjusted_page = max(0, page - 1) if page > 0 else 0
        if adjusted_page * size > 10000:
            raise ValidationError(
                "Total results (page * size) must be <= 10,000", "page"
            )

        try:
            # Log de parámetros recibidos para debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.info("Search amenities called with parameters:")
            logger.info(f"  - page: {page} (type: {type(page)})")
            logger.info(f"  - size: {size} (type: {type(size)})")
            logger.info(f"  - group_id: {group_id} (type: {type(group_id)})")
            logger.info(f"  - is_public: {is_public} (type: {type(is_public)})")
            logger.info(
                f"  - public_searchable: {public_searchable} (type: {type(public_searchable)})"
            )
            logger.info(
                f"  - is_filterable: {is_filterable} (type: {type(is_filterable)})"
            )

            # Crear caso de uso
            use_case = SearchAmenitiesUseCase(api_client)

            # Crear parámetros de búsqueda
            search_params = SearchAmenitiesParams(
                page=page,
                size=size,
                sort_column=sort_column,
                sort_direction=sort_direction,
                search=search,
                group_id=group_id,
                is_public=is_public,
                public_searchable=public_searchable,
                is_filterable=is_filterable,
            )

            # Ejecutar caso de uso
            result = await use_case.execute(search_params)
            return result
        except Exception as e:
            # Manejar errores específicos de la API según documentación
            if hasattr(e, "status_code"):
                if e.status_code == 400:
                    # Logging adicional para 400 Bad Request
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"400 Bad Request - Params enviados: {search_params.model_dump()}"
                    )
                    logger.error(f"400 Bad Request - Error details: {str(e)}")
                    logger.error(f"400 Bad Request - Error type: {type(e).__name__}")
                    logger.error(f"400 Bad Request - Error attributes: {dir(e)}")

                    # Capturar error body si está disponible
                    error_body = getattr(e, "response_text", str(e))
                    logger.error(f"400 Bad Request - Response body: {error_body}")

                    # Intentar obtener más información del error
                    if hasattr(e, "args") and e.args:
                        logger.error(f"400 Bad Request - Error args: {e.args}")

                    raise ValidationError(
                        "Bad Request: Invalid parameters sent to Amenities API. "
                        "Common issues and solutions:\n"
                        "🔧 PAGINATION:\n"
                        "- Page must be >= 1 (1-based pagination)\n"
                        "- Size must be 1-1000 (recommended: 25-100)\n"
                        "- Total results (page * size) must be <= 10,000\n"
                        "\n🔧 FILTERING:\n"
                        "- group_id: Must be positive integer (2=Essentials, 4=Family, 7=Accessibility, 10=Kitchen, 14=Pool, 19=Entertainment)\n"
                        "- is_public: Must be 0 (private) or 1 (public)\n"
                        "- public_searchable: Must be 0 (not searchable) or 1 (searchable)\n"
                        "- is_filterable: Must be 0 (not filterable) or 1 (filterable)\n"
                        "\n🔧 SORTING:\n"
                        "- sort_column: Must be one of: id, order, isPublic, publicSearchable, isFilterable, createdAt\n"
                        "- sort_direction: Must be 'asc' or 'desc'\n"
                        "\n🔧 SEARCH:\n"
                        "- search: Maximum 200 characters\n"
                        "- Examples: 'pool', 'wifi', 'kitchen', 'accessible', 'baby'\n"
                        "\n💡 BUSINESS TIPS:\n"
                        "- Use public_searchable=1 to find guest-searchable amenities\n"
                        "- Use sort_column='createdAt' with sort_direction='desc' to find newest amenities\n"
                        "- Use group_id filters to find amenities by category\n"
                        f"\nError details: {str(e)}",
                        "parameters",
                    )
                elif e.status_code == 401:
                    raise ValidationError(
                        "Unauthorized: Invalid authentication credentials. "
                        "Please verify your TRACKHS_USERNAME and TRACKHS_PASSWORD "
                        "are correct and not expired.",
                        "auth",
                    )
                elif e.status_code == 403:
                    raise ValidationError(
                        "Forbidden: Insufficient permissions for this operation. "
                        "Please verify your account has access to "
                        "Channel API/Amenities endpoints. "
                        "Contact your administrator to enable Channel API access.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        "Endpoint not found: /pms/units/amenities. "
                        "Please verify the API URL and endpoint path are correct. "
                        "The Channel API endpoint might not be available in your environment.",
                        "endpoint",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Internal Server Error: API temporarily unavailable. "
                        "Please try again later or contact TrackHS support. "
                        "If the problem persists, check the TrackHS service status.",
                        "api",
                    )
            raise ValidationError(f"API request failed: {str(e)}", "api")
