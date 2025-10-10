"""
Herramienta MCP para obtener notas de reserva de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_reservation_notes(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_reservation_notes"""
    
    @mcp.tool()
    async def get_reservation_notes(
        reservation_id: int,
        page: int = 1,
        size: int = 10,
        is_internal: bool = None,
        note_type: str = None,
        priority: str = None,
        author: str = None,
        sort_by: str = "createdAt",
        sort_direction: str = "desc",
        search: str = None,
        date_from: str = None,
        date_to: str = None
    ):
        """
        Get reservation notes from Track HS
        
        Args:
            reservation_id: ID de la reserva
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            is_internal: Si es nota interna (opcional)
            note_type: Tipo de nota (opcional)
            priority: Prioridad de la nota (opcional)
            author: Autor de la nota (opcional)
            sort_by: Campo para ordenar (default: "createdAt")
            sort_direction: Dirección de ordenamiento (default: "desc")
            search: Término de búsqueda (opcional)
            date_from: Fecha desde (opcional)
            date_to: Fecha hasta (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortBy": sort_by,
            "sortDirection": sort_direction
        }
        
        if is_internal is not None:
            query_params["isInternal"] = is_internal
        if note_type:
            query_params["noteType"] = note_type
        if priority:
            query_params["priority"] = priority
        if author:
            query_params["author"] = author
        if search:
            query_params["search"] = search
        if date_from:
            query_params["dateFrom"] = date_from
        if date_to:
            query_params["dateTo"] = date_to
        
        endpoint = f"/reservations/{reservation_id}/notes"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener notas de reserva: {str(e)}"}
