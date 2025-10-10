"""
Herramienta MCP para obtener órdenes de trabajo de mantenimiento de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_maintenance_work_orders(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_maintenance_work_orders"""
    
    @mcp.tool()
    async def get_maintenance_work_orders(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        updated_since: str = None,
        is_scheduled: int = None,
        unit_id: str = None,
        user_id: str = None,
        node_id: int = None,
        role_id: int = None,
        owner_id: int = None,
        priority: str = None,
        reservation_id: int = None,
        vendor_id: int = None,
        status: str = None,
        date_scheduled: str = None,
        start_date: str = None,
        end_date: str = None,
        problems: str = None
    ):
        """
        Get maintenance work orders from Track HS
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            updated_since: Filtro por fecha de actualización (opcional)
            is_scheduled: Si está programado (opcional)
            unit_id: ID de la unidad (opcional)
            user_id: ID del usuario (opcional)
            node_id: ID del nodo (opcional)
            role_id: ID del rol (opcional)
            owner_id: ID del propietario (opcional)
            priority: Prioridad (opcional)
            reservation_id: ID de la reserva (opcional)
            vendor_id: ID del proveedor (opcional)
            status: Estado (opcional)
            date_scheduled: Fecha programada (opcional)
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
            problems: Problemas (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        if search:
            query_params["search"] = search
        if updated_since:
            query_params["updatedSince"] = updated_since
        if is_scheduled is not None:
            query_params["isScheduled"] = is_scheduled
        if unit_id:
            query_params["unitId"] = unit_id
        if user_id:
            query_params["userId"] = user_id
        if node_id:
            query_params["nodeId"] = node_id
        if role_id:
            query_params["roleId"] = role_id
        if owner_id:
            query_params["ownerId"] = owner_id
        if priority:
            query_params["priority"] = priority
        if reservation_id:
            query_params["reservationId"] = reservation_id
        if vendor_id:
            query_params["vendorId"] = vendor_id
        if status:
            query_params["status"] = status
        if date_scheduled:
            query_params["dateScheduled"] = date_scheduled
        if start_date:
            query_params["startDate"] = start_date
        if end_date:
            query_params["endDate"] = end_date
        if problems:
            query_params["problems"] = problems
        
        endpoint = f"/maintenance/work-orders"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener órdenes de trabajo: {str(e)}"}
