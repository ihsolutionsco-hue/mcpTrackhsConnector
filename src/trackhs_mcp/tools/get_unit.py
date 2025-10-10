"""
Herramienta MCP para obtener una unidad específica de Track HS API
"""

from ..core.api_client import TrackHSApiClient

def register_get_unit(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_unit"""
    
    @mcp.tool()
    async def get_unit(unit_id: int):
        """
        Get a specific unit by ID from Track HS
        
        Args:
            unit_id: ID de la unidad a obtener
        """
        try:
            result = await api_client.get(f"/units/{unit_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener unidad: {str(e)}"}
