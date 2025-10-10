"""
Todas las herramientas MCP para Track HS API
"""

from typing import Optional, Literal, List, Union, Dict, Any
from ..core.api_client import TrackHSApiClient

def register_all_tools(mcp, api_client: TrackHSApiClient):
    """Registra todas las 13 herramientas MCP con el cliente API"""
    
    # 1. Get Reviews
    @mcp.tool()
    async def get_reviews(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        updated_since: str = None
    ):
        """Retrieve paginated collection of property reviews from Track HS"""
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
        
        endpoint = f"/channel-management/channel/reviews"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener reseñas: {str(e)}"}
    
    # 2. Get Reservation
    @mcp.tool()
    async def get_reservation(reservation_id: int):
        """Get a specific reservation by ID from Track HS"""
        try:
            result = await api_client.get(f"/reservations/{reservation_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener reserva: {str(e)}"}
    
    # 3. Search Reservations
    @mcp.tool()
    async def search_reservations(
        page: int = 1,
        size: int = 10,
        sort_column: str = "name",
        sort_direction: str = "asc",
        search: str = None,
        updated_since: str = None,
        tags: str = None,
        node_id: str = None,
        unit_id: str = None,
        status: str = None
    ):
        """Search reservations in Track HS with various filters"""
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
        if tags:
            query_params["tags"] = tags
        if node_id:
            query_params["nodeId"] = node_id
        if unit_id:
            query_params["unitId"] = unit_id
        if status:
            query_params["status"] = status
        
        endpoint = f"/reservations/search"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al buscar reservas: {str(e)}"}
    
    # 4. Get Units
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
        """Get units from Track HS with various filters"""
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
    
    # 5. Get Unit
    @mcp.tool()
    async def get_unit(unit_id: int):
        """Get a specific unit by ID from Track HS"""
        try:
            result = await api_client.get(f"/units/{unit_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener unidad: {str(e)}"}
    
    # 6. Get Folios Collection
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
        """Get folios collection from Track HS"""
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
    
    # 7. Get Contacts
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
        """Get contacts from Track HS"""
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
    
    # 8. Get Ledger Accounts
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
        """Get ledger accounts from Track HS"""
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
    
    # 9. Get Ledger Account
    @mcp.tool()
    async def get_ledger_account(account_id: int):
        """Get a specific ledger account by ID from Track HS"""
        try:
            result = await api_client.get(f"/pms/accounting/accounts/{account_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener cuenta contable: {str(e)}"}
    
    # 10. Get Reservation Notes
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
        """Get reservation notes from Track HS"""
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
    
    # 11. Get Nodes
    @mcp.tool()
    async def get_nodes(
        page: int = 1,
        size: int = 10,
        sort_column: str = "id",
        sort_direction: str = "asc",
        search: str = None,
        term: str = None,
        parent_id: int = None,
        type_id: int = None,
        computed: int = None,
        inherited: int = None,
        include_descriptions: int = None
    ):
        """Get nodes from Track HS"""
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
        if parent_id:
            query_params["parentId"] = parent_id
        if type_id:
            query_params["typeId"] = type_id
        if computed is not None:
            query_params["computed"] = computed
        if inherited is not None:
            query_params["inherited"] = inherited
        if include_descriptions is not None:
            query_params["includeDescriptions"] = include_descriptions
        
        endpoint = f"/nodes"
        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_string:
            endpoint += f"?{query_string}"
        
        try:
            result = await api_client.get(endpoint)
            return result
        except Exception as e:
            return {"error": f"Error al obtener nodos: {str(e)}"}
    
    # 12. Get Node
    @mcp.tool()
    async def get_node(node_id: int):
        """Get a specific node by ID from Track HS"""
        try:
            result = await api_client.get(f"/nodes/{node_id}")
            return result
        except Exception as e:
            return {"error": f"Error al obtener nodo: {str(e)}"}
    
    # 13. Get Maintenance Work Orders
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
        """Get maintenance work orders from Track HS"""
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
