"""
Documentation resources para API V1
Información concisa de la documentación de API V1
"""

from typing import Any, Dict

from ....application.ports.api_client_port import ApiClientPort


def register_api_v1_documentation(mcp, api_client: ApiClientPort):
    """Registra la documentación de API V1"""

    @mcp.resource(
        "trackhs://docs/api-v1",
        name="API V1 Documentation",
        description="Essential documentation for API V1",
        mime_type="text/plain",
    )
    async def api_v1_docs() -> str:
        """Documentación concisa de API V1"""
        return """# TrackHS API V1 - Search Reservations

## Endpoint
- **URL**: `GET /pms/reservations`
- **Versión**: 1.0

## Parámetros Principales

### Paginación
- `page`: Número de página (0-based, max 10k total)
- `size`: Tamaño de página (max 1000)

### Filtros
- `search`: Búsqueda por texto
- `status`: Estado de reserva (Hold|Confirmed|Checked In|Checked Out|Cancelled)
- `arrivalStart/End`: Rango de fechas de llegada
- `departureStart/End`: Rango de fechas de salida
- `nodeId`: ID del nodo/propiedad
- `unitId`: ID de la unidad
- `contactId`: ID del contacto

### Ordenamiento
- `sortColumn`: name|status|checkin|checkout|nights
- `sortDirection`: asc|desc

## Límites
- Máximo 10,000 resultados totales
- Máximo 1,000 elementos por página
- Scroll timeout de 1 minuto

## Ejemplos de Uso

### Búsqueda Básica
```
GET /pms/reservations?page=1&size=10&sortColumn=name&sortDirection=asc
```

### Búsqueda con Filtros
```
GET /pms/reservations?status=Confirmed&arrivalStart=2024-01-01&arrivalEnd=2024-12-31
```

### Scroll para Grandes Conjuntos
```
GET /pms/reservations?scroll=1&size=100
```
"""
