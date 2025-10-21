"""
Herramienta MCP para buscar amenidades en Track HS Channel API
Basado en la especificación completa de la API Get Unit Amenities Collection
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Literal, Optional

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from fastmcp.exceptions import ToolError

from ...application.use_cases.search_amenities import SearchAmenitiesUseCase
from ...domain.entities.amenities import SearchAmenitiesParams
from ..utils.error_handling import error_handler

# Removed type normalization imports - using Pydantic automatic conversion


@dataclass
class SearchAmenitiesResult:
    """Resultado estructurado de búsqueda de amenidades"""

    amenities: List[dict]
    total: int
    page: int
    size: int
    total_pages: int
    has_next: bool
    has_previous: bool


def register_search_amenities(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta search_amenities"""

    @mcp.tool(name="search_amenities")
    @error_handler("search_amenities")
    async def search_amenities(
        page: int = Field(
            default=1,
            description="Page number (1-based indexing). Max 10,000 total results.",
            ge=1,
            le=10000,
        ),
        size: int = Field(
            default=25, description="Items per page. Max 1,000 per page.", ge=1, le=1000
        ),
        sort_column: Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ] = Field(
            default="order",
            description="Field to sort by. Options: id, order, isPublic, publicSearchable, isFilterable, createdAt",
        ),
        sort_direction: Literal["asc", "desc"] = Field(
            default="asc",
            description="Sort direction: 'asc' (ascending) or 'desc' (descending)",
        ),
        search: Optional[str] = Field(
            default=None,
            description="Full-text search in amenity ID and name fields",
            max_length=200,
        ),
        group_id: Optional[int] = Field(
            default=None,
            description="Filter by amenity group ID (positive integer)",
            ge=1,
        ),
        is_public: Optional[int] = Field(
            default=None,
            description="Filter by public status: 0=private, 1=public",
            ge=0,
            le=1,
        ),
        public_searchable: Optional[int] = Field(
            default=None,
            description="Filter by searchable status: 0=not searchable, 1=searchable",
            ge=0,
            le=1,
        ),
        is_filterable: Optional[int] = Field(
            default=None,
            description="Filter by filterable status: 0=not filterable, 1=filterable",
            ge=0,
            le=1,
        ),
    ) -> SearchAmenitiesResult:
        """
        Search amenities in Track HS Channel API with filtering and pagination.

        Provides comprehensive amenity search with filtering by group, public status,
        searchability, and filterability. Supports pagination (max 10k results) and
        flexible sorting options. Returns complete amenity data with embedded objects.
        """
        # Detectar y aplicar defaults para FieldInfo objects (cuando se llama directamente sin FastMCP)
        if type(sort_column).__name__ == "FieldInfo":
            sort_column = "order"
        if type(sort_direction).__name__ == "FieldInfo":
            sort_direction = "asc"
        if type(search).__name__ == "FieldInfo":
            search = None

        # Validar parámetros (Pydantic ya maneja la conversión automática)
        if page is None:
            page = 1
        if size is None:
            size = 25

        # Validar límite total de resultados (10k máximo) - validación de negocio
        # Ajustar page para cálculo (API usa 1-based, pero calculamos con 0-based)
        adjusted_page = max(0, page - 1) if page > 0 else 0
        if adjusted_page * size > 10000:
            raise ToolError("Total results (page * size) must be <= 10,000")

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

            # Convertir resultado a dataclass estructurado
            return SearchAmenitiesResult(
                amenities=result.get("amenities", []),
                total=result.get("total", 0),
                page=result.get("page", 1),
                size=result.get("size", 25),
                total_pages=result.get("total_pages", 1),
                has_next=result.get("has_next", False),
                has_previous=result.get("has_previous", False),
            )
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

                    raise ToolError(
                        "Bad Request: Invalid parameters sent to Amenities API. "
                        "Common issues:\n"
                        "- Page must be >= 1 (1-based pagination)\n"
                        "- Numeric parameters (group_id) must be integers or convertible strings\n"
                        "- Boolean parameters (is_public, public_searchable, is_filterable) must be 0 or 1\n"
                        "- Sort column must be one of: id, order, isPublic, publicSearchable, isFilterable, createdAt\n"
                        "- Sort direction must be 'asc' or 'desc'\n"
                        "- Group ID must be a positive integer\n"
                        "- Empty string parameters are converted to None automatically\n"
                        f"Error details: {str(e)}"
                    )
                elif e.status_code == 401:
                    raise ToolError(
                        "Unauthorized: Invalid authentication credentials. "
                        "Please verify your TRACKHS_USERNAME and TRACKHS_PASSWORD "
                        "are correct and not expired."
                    )
                elif e.status_code == 403:
                    raise ToolError(
                        "Forbidden: Insufficient permissions for this operation. "
                        "Please verify your account has access to "
                        "Channel API/Amenities endpoints. "
                        "Contact your administrator to enable Channel API access."
                    )
                elif e.status_code == 404:
                    raise ToolError(
                        "Endpoint not found: /pms/units/amenities. "
                        "Please verify the API URL and endpoint path are correct. "
                        "The Channel API endpoint might not be available in your environment."
                    )
                elif e.status_code == 500:
                    raise ToolError(
                        "Internal Server Error: API temporarily unavailable. "
                        "Please try again later or contact TrackHS support. "
                        "If the problem persists, check the TrackHS service status."
                    )
            raise ToolError(f"API request failed: {str(e)}")
