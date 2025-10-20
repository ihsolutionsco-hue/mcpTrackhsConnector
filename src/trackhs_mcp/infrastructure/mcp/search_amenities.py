"""
Herramienta MCP para buscar amenidades en Track HS Channel API
Basado en la especificación completa de la API Get Unit Amenities Collection
"""

from typing import TYPE_CHECKING, Literal, Optional, Union

from pydantic import BaseModel, Field

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
        page: Union[int, float, str] = 1,
        size: Union[int, float, str] = 25,
        sort_column: Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ] = "order",
        sort_direction: Literal["asc", "desc"] = "asc",
        search: Optional[str] = None,
        group_id: Optional[Union[int, float, str]] = None,
        is_public: Optional[Union[int, float, str]] = None,
        public_searchable: Optional[Union[int, float, str]] = None,
        is_filterable: Optional[Union[int, float, str]] = None,
    ):
        """
        Search amenities in Track HS Channel API with comprehensive filtering options.

        This MCP tool provides advanced amenity search capabilities with full Channel API
        compatibility, including pagination, filtering, sorting, and comprehensive
        amenity information retrieval.

        **Key Features:**
        - ✅ Full Channel API compatibility with all parameters
        - ✅ Advanced pagination (limited to 10k total results)
        - ✅ Comprehensive filtering (groups, public status, etc.)
        - ✅ Flexible sorting options
        - ✅ Robust error handling
        - ✅ MCP-optimized for AI model integration

        **Examples:**

        # Basic search
        search_amenities(page=1, size=25)

        # Search by group
        search_amenities(
            group_id=1,
            is_public=1,
            public_searchable=1
        )

        # Search with sorting
        search_amenities(
            sort_column="name",
            sort_direction="asc",
            search="pool"
        )

        # Search with filters
        search_amenities(
            is_public=1,
            is_filterable=1,
            public_searchable=1
        )

        **Parameters:**
        - page: Page number (1-based, max 10k total results)
        - size: Page size (max 1000, limited to 10k total results)
        - sort_column: Sort by field (id, order, isPublic, publicSearchable, isFilterable, createdAt)
        - sort_direction: Sort direction (asc/desc)
        - search: Text search in id and/or name
        - group_id: Filter by group ID
        - is_public: Public amenities (0/1)
        - public_searchable: Publicly searchable amenities (0/1)
        - is_filterable: Filterable amenities (0/1)

        **Returns:**
        Complete amenity data with embedded objects and pagination information.

        **Error Handling:**
        - Validates all parameters according to Channel API specification
        - Handles API errors (401, 403, 500) with descriptive messages
        - Validates parameter formats strictly
        - Enforces 10k total results limit
        - Validates boolean parameters (0/1 only)

        **Common Errors:**
        - Page/size: Must be positive integers (page=1, size=25)
        - Boolean flags: Use 0 or 1 (is_public=1, public_searchable=1)
        - Sort column: Must be one of: id, order, isPublic, publicSearchable, isFilterable, createdAt
        - Group ID: Must be positive integer (group_id=1)
        """
        # Normalizar parámetros numéricos primero (para compatibilidad JSON-RPC)
        page = normalize_int(page, "page")
        size = normalize_int(size, "size")
        group_id = normalize_int(group_id, "group_id")

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
                        "Common issues:\n"
                        "- Page must be >= 1 (1-based pagination)\n"
                        "- Numeric parameters (group_id) must be integers or convertible strings\n"
                        "- Boolean parameters (is_public, public_searchable, is_filterable) must be 0 or 1\n"
                        "- Sort column must be one of: id, order, isPublic, publicSearchable, isFilterable, createdAt\n"
                        "- Sort direction must be 'asc' or 'desc'\n"
                        "- Group ID must be a positive integer\n"
                        "- Empty string parameters are converted to None automatically\n"
                        f"Error details: {str(e)}",
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
