"""
Herramienta MCP para obtener cuentas contables de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_ledger_accounts(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_ledger_accounts"""
    
    @mcp.tool()
    async def get_ledger_accounts(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        is_active: int = None,
        category: str = None,
        account_type: str = None,
        parent_id: int = None
    ):
        """
        Get ledger accounts from Track HS
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            is_active: Si está activo (opcional)
            category: Categoría de la cuenta (opcional)
            account_type: Tipo de cuenta (opcional)
            parent_id: ID de la cuenta padre (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        if search:
            query_params["search"] = search
        if is_active is not None:
            query_params["isActive"] = is_active
        if category:
            query_params["category"] = category
        if account_type:
            query_params["accountType"] = account_type
        if parent_id:
            query_params["parentId"] = parent_id
        
        endpoint = f"/pms/accounting/accounts"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener cuentas contables: {str(e)}"}
