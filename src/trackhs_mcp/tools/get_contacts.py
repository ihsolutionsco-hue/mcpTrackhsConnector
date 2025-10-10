"""
Herramienta MCP para obtener contactos de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_contacts(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_contacts"""
    
    @mcp.tool()
    async def get_contacts(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        term: str = None,
        email: str = None,
        updated_since: str = None
    ):
        """
        Get contacts from Track HS
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            term: Término específico (opcional)
            email: Email del contacto (opcional)
            updated_since: Filtro por fecha de actualización (opcional)
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
        if email:
            query_params["email"] = email
        if updated_since:
            query_params["updatedSince"] = updated_since
        
        endpoint = f"/crm/contacts"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener contactos: {str(e)}"}
