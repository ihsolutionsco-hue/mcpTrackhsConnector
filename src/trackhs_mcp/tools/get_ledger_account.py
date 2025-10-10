"""
Herramienta MCP para obtener una cuenta contable específica de Track HS API
"""

from ..core.api_client import TrackHSApiClient

def register_get_ledger_account(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_ledger_account"""
    
    @mcp.tool()
    async def get_ledger_account(account_id: int):
        """
        Get a specific ledger account by ID from Track HS
        
        Args:
            account_id: ID de la cuenta contable a obtener
        """
        try:
            result = await api_client.get(f"/pms/accounting/accounts/{account_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener cuenta contable: {str(e)}"}
