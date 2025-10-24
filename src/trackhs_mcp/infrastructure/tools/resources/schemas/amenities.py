"""
Schema resources para Amenities
Información esencial del esquema de datos para la API de Amenidades
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_amenities_schema(mcp, api_client: "ApiClientPort"):
    """Registra el schema de Amenities"""

    @mcp.resource(
        "trackhs://schema/amenities",
        name="Amenities Schema",
        description="Schema for Amenities API (Channel API)",
        mime_type="application/json",
    )
    async def amenities_schema() -> Dict[str, Any]:
        """Schema esencial para Amenities API"""
        return {
            "endpoint": "/api/pms/units/amenities",
            "method": "GET",
            "api": "Channel API",
            "version": "1.0",
            "description": "Search amenities with comprehensive filtering options",
            "fields": {
                "id": "integer - ID único de la amenidad",
                "name": "string - Nombre de la amenidad",
                "order": "integer - Orden de visualización",
                "isPublic": "boolean - Si es pública",
                "publicSearchable": "boolean - Si es buscable públicamente",
                "isFilterable": "boolean - Si es filtrable",
                "groupId": "integer - ID del grupo de amenidades",
                "createdAt": "string - Fecha de creación (ISO 8601)",
                "updatedAt": "string - Fecha de actualización (ISO 8601)",
            },
            "pagination": {
                "page": "integer - Número de página (1-based, max 10k total)",
                "size": "integer - Tamaño de página (max 1000)",
            },
            "filtering": {
                "search": "string - Búsqueda por texto en id y/o nombre",
                "groupId": "integer - Filtrar por ID de grupo",
                "isPublic": "integer - Amenidades públicas (0/1)",
                "publicSearchable": "integer - Amenidades buscables públicamente (0/1)",
                "isFilterable": "integer - Amenidades filtrables (0/1)",
            },
            "sorting": {
                "sortColumn": "string - id|order|isPublic|publicSearchable|isFilterable|createdAt",
                "sortDirection": "string - asc|desc",
            },
            "limits": {
                "max_total_results": 10000,
                "max_page_size": 1000,
            },
            "best_practices": [
                "Usar paginación para grandes conjuntos de datos",
                "Valores booleanos deben ser 0 o 1",
                "Filtrar por grupo para resultados más específicos",
                "Usar isPublic=1 para amenidades visibles al público",
                "Ordenar por 'order' para obtener amenidades en el orden de visualización",
            ],
        }
