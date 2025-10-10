"""
Herramienta MCP para obtener nodos de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_nodes(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_nodes"""
    
    @mcp.tool()
    async def get_nodes(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        term: str = None,
        parent_id: int = None,
        type_id: int = None,
        computed: int = None,
        inherited: int = None,
        include_descriptions: int = None
    ):
        """
        Get nodes from Track HS
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            term: Término específico (opcional)
            parent_id: ID del nodo padre (opcional)
            type_id: ID del tipo de nodo (opcional)
            computed: Si es computado (opcional)
            inherited: Si es heredado (opcional)
            include_descriptions: Si incluir descripciones (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        if search:
            query_params["search"] = search
        if term:
            query_params["term"] = term
        if parent_id:
            query_params["parentId"] = parent_id
        if type_id:
            query_params["typeId"] = type_id
        if computed is not None:
            query_params["computed"] = computed
        if inherited is not None:
            query_params["inherited"] = inherited
        if include_descriptions is not None:
            query_params["includeDescriptions"] = include_descriptions
        
        endpoint = f"/nodes"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener nodos: {str(e)}"}
