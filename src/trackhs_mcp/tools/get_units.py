"""
Herramienta MCP para obtener unidades de Track HS API
"""

from typing import Optional
from ..core.api_client import TrackHSApiClient

def register_get_units(mcp, api_client: TrackHSApiClient):
    """Registra la herramienta get_units"""
    
    @mcp.tool()
    async def get_units(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        node_id: str = None,
        unit_type_id: str = None,
        amenity_id: str = None,
        bedrooms: int = None,
        bathrooms: int = None,
        pets_friendly: int = None,
        events_allowed: int = None,
        smoking_allowed: int = None,
        children_allowed: int = None,
        is_active: int = None,
        is_bookable: int = None
    ):
        """
        Get units from Track HS with various filters
        
        Args:
            page: Número de página (default: 1)
            size: Tamaño de página (default: 10)
            sort_column: Columna para ordenar (default: "id")
            sort_direction: Dirección de ordenamiento (default: "asc")
            search: Término de búsqueda (opcional)
            node_id: ID del nodo (opcional)
            unit_type_id: ID del tipo de unidad (opcional)
            amenity_id: ID de amenidad (opcional)
            bedrooms: Número de habitaciones (opcional)
            bathrooms: Número de baños (opcional)
            pets_friendly: Si acepta mascotas (opcional)
            events_allowed: Si se permiten eventos (opcional)
            smoking_allowed: Si se permite fumar (opcional)
            children_allowed: Si se permiten niños (opcional)
            is_active: Si está activo (opcional)
            is_bookable: Si es reservable (opcional)
        """
        query_params = {
            "page": page,
            "size": size,
            "sortColumn": sort_column,
            "sortDirection": sort_direction
        }
        
        if search:
            query_params["search"] = search
        if node_id:
            query_params["nodeId"] = node_id
        if unit_type_id:
            query_params["unitTypeId"] = unit_type_id
        if amenity_id:
            query_params["amenityId"] = amenity_id
        if bedrooms:
            query_params["bedrooms"] = bedrooms
        if bathrooms:
            query_params["bathrooms"] = bathrooms
        if pets_friendly is not None:
            query_params["petsFriendly"] = pets_friendly
        if events_allowed is not None:
            query_params["eventsAllowed"] = events_allowed
        if smoking_allowed is not None:
            query_params["smokingAllowed"] = smoking_allowed
        if children_allowed is not None:
            query_params["childrenAllowed"] = children_allowed
        if is_active is not None:
            query_params["isActive"] = is_active
        if is_bookable is not None:
            query_params["isBookable"] = is_bookable
        
        endpoint = f"/units"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener unidades: {str(e)}"}
