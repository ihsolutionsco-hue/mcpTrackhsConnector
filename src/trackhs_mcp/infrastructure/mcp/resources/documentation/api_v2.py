"""
Documentation resources para API V2
Información concisa de la documentación de API V2
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_api_v2_documentation(mcp, api_client: "ApiClientPort"):
    """Registra la documentación de API V2"""

    @mcp.resource(
        "trackhs://docs/api-v2",
        name="API V2 Documentation",
        description="Essential documentation for API V2",
        mime_type="text/plain",
    )
    async def api_v2_docs() -> str:
        """Documentación concisa de API V2"""
        return """# TrackHS API V2 - Search Reservations (Recomendado)

## Endpoint
- **URL**: `GET /v2/pms/reservations`
- **Versión**: 2.0

## Parámetros Principales

### Paginación
- `page`: Número de página (0-based, max 10k total)
- `size`: Tamaño de página (max 1000)

### Filtros Básicos
- `search`: Búsqueda por texto
- `status`: Estado(s) de reserva (múltiples valores soportados)
- `arrivalStart/End`: Rango de fechas de llegada
- `departureStart/End`: Rango de fechas de salida
- `bookedStart/End`: Rango de fechas de reserva
- `updatedSince`: Actualizadas desde fecha

### Filtros por ID
- `nodeId`: ID(s) del nodo/propiedad
- `unitId`: ID(s) de la unidad
- `contactId`: ID(s) del contacto
- `travelAgentId`: ID(s) del agente de viajes
- `campaignId`: ID(s) de la campaña
- `userId`: ID(s) del usuario
- `unitTypeId`: ID(s) del tipo de unidad
- `rateTypeId`: ID(s) del tipo de tarifa
- `reservationTypeId`: ID(s) del tipo de reserva

### Filtros Adicionales
- `groupId`: ID del grupo
- `checkinOfficeId`: ID de la oficina de check-in
- `inHouseToday`: 0|1 - Huéspedes en casa hoy
- `scroll`: Scroll de Elasticsearch

### Ordenamiento
- `sortColumn`: name|status|checkin|checkout|nights
- `sortDirection`: asc|desc

## Mejoras V2 vs V1
- **Más parámetros**: 25+ vs 20 en V1
- **Mejor rendimiento**: Consultas optimizadas
- **Datos enriquecidos**: Información financiera completa
- **Flexibilidad**: Múltiples valores para algunos parámetros

## Límites
- Máximo 10,000 resultados totales
- Máximo 1,000 elementos por página
- Scroll timeout de 1 minuto

## Ejemplos de Uso

### Búsqueda Básica
```
GET /v2/pms/reservations?page=1&size=10&sortColumn=name&sortDirection=asc
```

### Búsqueda con Filtros Múltiples
```
GET /v2/pms/reservations?status=Confirmed,Checked In&arrivalStart=2024-01-01&nodeId=1,2,3
```

### Scroll para Grandes Conjuntos
```
GET /v2/pms/reservations?scroll=1&size=100
```
"""
