"""
Herramienta MCP para obtener una reserva específica de Track HS API
"""

from ..core.api_client import TrackHSApiClient

def register_get_reservation(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_reservation"""
    
    @mcp.tool()
    async def get_reservation(reservation_id: int):
        """
        Get a specific reservation by ID from Track HS
        
        Args:
            reservation_id: ID de la reserva a obtener
        """
        try:
            result = await api_client.get(f"/reservations/{reservation_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener reserva: {str(e)}"}