"""
Examples resources para Search Queries
Ejemplos de búsquedas comunes para las APIs
"""

from typing import Any, Dict

from ....application.ports.api_client_port import ApiClientPort


def register_search_examples(mcp, api_client: ApiClientPort):
    """Registra los ejemplos de búsquedas"""

    @mcp.resource(
        "trackhs://examples/search-queries",
        name="Search Query Examples",
        description="Common search query examples for TrackHS APIs",
        mime_type="text/plain",
    )
    async def search_examples() -> str:
        """Ejemplos de búsquedas comunes"""
        return """# TrackHS Search Query Examples

## Búsquedas Comunes

### 1. Reservas por Rango de Fechas
```python
# V1
search_reservations_v1(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    sort_column="checkin",
    sort_direction="asc"
)

# V2
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    sort_column="checkin",
    sort_direction="asc"
)
```

### 2. Reservas por Estado
```python
# V1
search_reservations_v1(
    status="Confirmed",
    sort_column="checkin",
    sort_direction="desc"
)

# V2 - Múltiples estados
search_reservations_v2(
    status=["Confirmed", "Checked In"],
    sort_column="checkin",
    sort_direction="desc"
)
```

### 3. Reservas por Unidad/Nodo
```python
# V1
search_reservations_v1(
    unit_id="123",
    node_id="456"
)

# V2 - Múltiples IDs
search_reservations_v2(
    unit_id="123,124,125",
    node_id="456,457"
)
```

### 4. Scroll para Grandes Datasets
```python
# V1 y V2 - Mismo comportamiento
search_reservations_v2(
    scroll=1,
    size=1000
)

# Continuar con scroll
search_reservations_v2(
    scroll="scroll_token_from_previous_response",
    size=1000
)
```

### 5. Búsqueda Combinada
```python
# V2 - Filtros múltiples
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    status=["Confirmed", "Checked In"],
    node_id="1,2,3",
    unit_type_id="10",
    sort_column="checkin",
    sort_direction="asc"
)
```

### 6. Reservas Actualizadas
```python
# V2 - Nuevo en V2
search_reservations_v2(
    updated_since="2024-01-01T00:00:00Z",
    sort_column="updated_at",
    sort_direction="desc"
)
```

## Casos de Uso Comunes

### Reportes Mensuales
```python
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    status="Confirmed",
    sort_column="checkin",
    sort_direction="asc"
)
```

### Huéspedes Actualmente en Casa
```python
search_reservations_v2(
    status="Checked In",
    in_house_today=1,
    sort_column="checkin",
    sort_direction="asc"
)
```

### Exportación Masiva
```python
search_reservations_v2(
    scroll=1,
    size=1000
)
```

### Análisis por Canal
```python
search_reservations_v2(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    channel_id="1,2,3",  # Múltiples canales
    sort_column="channel_id",
    sort_direction="asc"
)
```
"""
