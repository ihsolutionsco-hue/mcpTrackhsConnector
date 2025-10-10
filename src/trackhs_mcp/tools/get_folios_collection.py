"""
Herramienta MCP para obtener colección de folios de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_folios_collection(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_folios_collection"""
    
    @mcp.tool()
    async def get_folios_collection(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        type: str = None,
        status: str = None,
        master_folio_id: int = None,
        contact_id: int = None,
        company_id: int = None
    ):
        """
        Get folios collection from Track HS
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            type: Tipo de folio (opcional)
            status: Estado del folio (opcional)
            master_folio_id: ID del folio maestro (opcional)
            contact_id: ID del contacto (opcional)
            company_id: ID de la empresa (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        if search:
            query_params["search"] = search
        if type:
            query_params["type"] = type
        if status:
            query_params["status"] = status
        if master_folio_id:
            query_params["masterFolioId"] = master_folio_id
        if contact_id:
            query_params["contactId"] = contact_id
        if company_id:
            query_params["companyId"] = company_id
        
        endpoint = f"/pms/accounting/folios"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener folios: {str(e)}"}
