"""
Examples resources para Search Queries
Ejemplos de búsquedas comunes para las APIs
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_search_examples(mcp, api_client: "ApiClientPort"):
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

## Para Principiantes - Primeros Pasos

### 1. Mi Primera Búsqueda (Más Simple)
```python
# Obtener las primeras 10 reservas confirmadas
search_reservations(
    status="Confirmed",
    page=0,
    size=10
)
```
**¿Qué hace?** Busca reservas con estado "Confirmed", página 0, 10 resultados.
**¿Cuándo usarlo?** Cuando necesitas ver rápidamente las reservas confirmadas.

### 2. Búsqueda por Fechas (Básica)
```python
# Reservas que llegan en enero 2024
search_reservations(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    page=0,
    size=10
)
```
**¿Qué hace?** Busca reservas con llegada entre el 1 y 31 de enero 2024.
**¿Cuándo usarlo?** Para reportes mensuales o análisis por período.

### 3. Ver Huéspedes Actuales
```python
# Huéspedes que están en casa hoy
search_reservations(
    status="Checked In",
    in_house_today=1,
    page=0,
    size=20
)
```
**¿Qué hace?** Busca huéspedes que están actualmente en la propiedad.
**¿Cuándo usarlo?** Para verificar ocupación actual o contactar huéspedes.

## Búsquedas Comunes

### 4. Reservas por Estado (Detallado)
```python
# Estado único
search_reservations(
    status="Confirmed",
    sort_column="checkin",
    sort_direction="desc",
    page=0,
    size=25
)

# Múltiples estados (separados por comas)
search_reservations(
    status="Confirmed,Checked In",
    sort_column="checkin",
    sort_direction="desc",
    page=0,
    size=25
)
```
**¿Qué hace?** Busca reservas en estados específicos, ordenadas por fecha de check-in.
**¿Cuándo usarlo?** Para filtrar por estado de reserva.

### 5. Reservas por Unidad/Nodo
```python
# ID único
search_reservations(
    unit_id="123",
    node_id="456",
    page=0,
    size=10
)

# Múltiples IDs (separados por comas)
search_reservations(
    unit_id="123,124,125",
    node_id="456,457",
    page=0,
    size=50
)
```
**¿Qué hace?** Busca reservas de unidades o nodos específicos.
**¿Cuándo usarlo?** Para analizar reservas de propiedades específicas.

### 6. Scroll para Grandes Datasets
```python
# Iniciar scroll (para obtener muchos datos)
search_reservations(
    scroll=1,
    size=1000
)

# Continuar con scroll (usar token de respuesta anterior)
search_reservations(
    scroll="scroll_token_from_previous_response",
    size=1000
)
```
**¿Qué hace?** Permite obtener grandes cantidades de datos de forma eficiente.
**¿Cuándo usarlo?** Para exportaciones masivas o análisis completos.

### 7. Búsqueda Combinada (Avanzada)
```python
# Filtros múltiples
search_reservations(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    status="Confirmed,Checked In",
    node_id="1,2,3",
    unit_type_id="10",
    sort_column="checkin",
    sort_direction="asc",
    page=0,
    size=100
)
```
**¿Qué hace?** Combina múltiples filtros para búsquedas específicas.
**¿Cuándo usarlo?** Para análisis detallados con criterios múltiples.

### 8. Reservas Actualizadas
```python
# Buscar reservas modificadas recientemente
search_reservations(
    updated_since="2024-01-01T00:00:00Z",
    sort_column="updated_at",
    sort_direction="desc",
    page=0,
    size=50
)
```
**¿Qué hace?** Busca reservas que han sido modificadas desde una fecha específica.
**¿Cuándo usarlo?** Para sincronización de datos o auditorías.

## Casos de Uso Comunes

### Reportes Mensuales
```python
search_reservations(
    arrival_start="2024-01-01",
    arrival_end="2024-01-31",
    status="Confirmed",
    sort_column="checkin",
    sort_direction="asc",
    page=0,
    size=100
)
```
**¿Qué hace?** Obtiene todas las reservas confirmadas de enero 2024.
**¿Cuándo usarlo?** Para reportes mensuales de ocupación.

### Huéspedes Actualmente en Casa
```python
search_reservations(
    status="Checked In",
    in_house_today=1,
    sort_column="checkin",
    sort_direction="asc",
    page=0,
    size=50
)
```
**¿Qué hace?** Lista todos los huéspedes que están actualmente en la propiedad.
**¿Cuándo usarlo?** Para verificar ocupación actual.

### Exportación Masiva
```python
search_reservations(
    scroll=1,
    size=1000
)
```
**¿Qué hace?** Inicia una exportación masiva de todas las reservas.
**¿Cuándo usarlo?** Para respaldos o migración de datos.

### Análisis por Canal
```python
search_reservations(
    arrival_start="2024-01-01",
    arrival_end="2024-12-31",
    channel_id="1,2,3",  # Múltiples canales
    sort_column="channel_id",
    sort_direction="asc",
    page=0,
    size=100
)
```
**¿Qué hace?** Analiza reservas por canal de distribución.
**¿Cuándo usarlo?** Para análisis de rendimiento por canal.

## Respuestas Esperadas

### Respuesta Básica
```json
{
  "_embedded": {
    "reservations": [
      {
        "id": 12345,
        "name": "Reservation #12345",
        "status": "Confirmed",
        "checkin": "2024-01-15",
        "checkout": "2024-01-20",
        "guests": 2,
        "unit": {
          "id": 101,
          "name": "Villa Paradise"
        }
      }
    ]
  },
  "page": 0,
  "page_count": 1,
  "page_size": 10,
  "total_items": 1
}
```

### Respuesta con Scroll
```json
{
  "_embedded": {
    "reservations": [...]
  },
  "page": 0,
  "page_count": 1,
  "page_size": 1000,
  "total_items": 5000,
  "_scroll": "scroll_token_12345"
}
```

## Errores Comunes y Soluciones

### Error: "Invalid date format"
```python
# ❌ Incorrecto
search_reservations(arrival_start="01/01/2024")

# ✅ Correcto
search_reservations(arrival_start="2024-01-01")
```

### Error: "Invalid status value"
```python
# ❌ Incorrecto
search_reservations(status="confirm")

# ✅ Correcto
search_reservations(status="Confirmed")
```

### Error: "Page must be >= 0"
```python
# ❌ Incorrecto
search_reservations(page=1)

# ✅ Correcto
search_reservations(page=0)
```

### Error: "Size must be between 1 and 100"
```python
# ❌ Incorrecto
search_reservations(size=200)

# ✅ Correcto
search_reservations(size=50)
```

## Estados Válidos de Reservas

- `"Hold"` - Reserva en espera
- `"Confirmed"` - Reserva confirmada
- `"Cancelled"` - Reserva cancelada
- `"Checked In"` - Huésped registrado
- `"Checked Out"` - Huésped salió

## Parámetros de Ordenamiento

- `"name"` - Por nombre de reserva
- `"status"` - Por estado
- `"checkin"` - Por fecha de llegada
- `"checkout"` - Por fecha de salida
- `"guests"` - Por número de huéspedes
- `"nights"` - Por número de noches
"""
