"""
Herramienta MCP para obtener un nodo específico de Track HS API
"""

from ..core.api_client import TrackHSApiClient

def register_get_node(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_node"""
    
    @mcp.tool()
    async def get_node(node_id: int):
        """
        Get a specific node by ID from Track HS
        
        Args:
            node_id: ID del nodo a obtener
        """
        try:
            result = await api_client.get(f"/nodes/{node_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener nodo: {str(e)}"}
