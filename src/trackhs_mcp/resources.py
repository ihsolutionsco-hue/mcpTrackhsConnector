"""
Resources MCP para Track HS API
"""

from typing import Dict, Any
from .core.api_client import TrackHSApiClient

def register_all_resources(mcp, api_client: TrackHSApiClient):
    """Registra todos los resources MCP"""
    
    @mcp.resource("trackhs://schema/reservations")
    async def reservations_schema() -> Dict[str, Any]:
        """Esquema de datos para reservas en TrackHS"""
        return {
            "schema": {
                "id": "string",
                "guestName": "string", 
                "checkIn": "date",
                "checkOut": "date",
                "status": "enum[confirmed, pending, cancelled]",
                "totalAmount": "number",
                "unitId": "string",
                "nodeId": "string"
            },
            "description": "Estructura de datos para reservas en TrackHS"
        }
    
    @mcp.resource("trackhs://schema/units")
    async def units_schema() -> Dict[str, Any]:
        """Esquema de datos para unidades en TrackHS"""
        return {
            "schema": {
                "id": "string",
                "name": "string",
                "type": "enum[apartment, house, room]",
                "capacity": "number",
                "status": "enum[available, occupied, maintenance]",
                "nodeId": "string",
                "amenities": "array[string]"
            },
            "description": "Estructura de datos para unidades en TrackHS"
        }
    
    @mcp.resource("trackhs://status/system")
    async def system_status() -> Dict[str, Any]:
        """Estado actual del sistema TrackHS y configuración"""
        return {
            "status": "operational",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0",
            "apiUrl": api_client.config.base_url,
            "toolsCount": 13,
            "capabilities": ["tools", "resources", "prompts"]
        }
    
    @mcp.resource("trackhs://docs/api")
    async def api_documentation() -> str:
        """Documentación de la API de TrackHS"""
        return """# TrackHS API Documentation

## Endpoints Disponibles

### Reservas
- `GET /reservations` - Listar reservas
- `GET /reservations/{id}` - Obtener reserva específica
- `GET /reservations/search` - Buscar reservas

### Unidades
- `GET /units` - Listar unidades
- `GET /units/{id}` - Obtener unidad específica

### Contactos
- `GET /crm/contacts` - Listar contactos

### Contabilidad
- `GET /pms/accounting/accounts` - Listar cuentas contables
- `GET /pms/accounting/folios` - Listar folios

### Mantenimiento
- `GET /maintenance/work-orders` - Listar órdenes de trabajo

## Autenticación
Todas las peticiones requieren autenticación Basic Auth con las credenciales configuradas.
"""
