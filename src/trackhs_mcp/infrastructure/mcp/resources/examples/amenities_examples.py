"""
Examples resources para Amenities
Ejemplos de uso para la herramienta search_amenities
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_amenities_examples(mcp, api_client: "ApiClientPort"):
    """Registra los ejemplos de amenidades"""

    @mcp.resource(
        "trackhs://examples/amenities",
        name="Amenities Examples",
        description="Common amenities query examples",
        mime_type="text/plain",
    )
    async def amenities_examples() -> str:
        """Ejemplos de búsquedas de amenidades"""
        return """# TrackHS Amenities Query Examples

## Búsquedas Comunes

### 1. Búsqueda Básica
```python
# Obtener las primeras 25 amenidades ordenadas por 'order'
search_amenities(
    page=1,
    size=25,
    sort_column="order",
    sort_direction="asc"
)
```

### 2. Amenidades Públicas
```python
# Obtener amenidades visibles al público
search_amenities(
    is_public=1,
    public_searchable=1,
    sort_column="order",
    sort_direction="asc"
)
```

### 3. Amenidades Filtrables
```python
# Obtener amenidades que se pueden usar como filtros
search_amenities(
    is_filterable=1,
    is_public=1,
    sort_column="name",
    sort_direction="asc"
)
```

### 4. Búsqueda por Texto
```python
# Buscar amenidades por nombre
search_amenities(
    search="pool",
    is_public=1,
    sort_column="name"
)
```

### 5. Amenidades por Grupo
```python
# Obtener amenidades de un grupo específico
search_amenities(
    group_id=1,
    is_public=1,
    sort_column="order",
    sort_direction="asc"
)
```

### 6. Todas las Amenidades Activas
```python
# Obtener todas las amenidades públicas y buscables
search_amenities(
    is_public=1,
    public_searchable=1,
    is_filterable=1
)
```

## Casos de Uso Comunes

### Filtros de Búsqueda de Unidades
```python
# Obtener amenidades para usar como filtros en búsqueda de unidades
search_amenities(
    is_filterable=1,
    is_public=1,
    sort_column="order",
    sort_direction="asc",
    size=100
)
```

### Listado Público de Amenidades
```python
# Amenidades para mostrar en sitio web público
search_amenities(
    is_public=1,
    public_searchable=1,
    sort_column="order",
    sort_direction="asc"
)
```

### Búsqueda de Amenidad Específica
```python
# Buscar wifi o internet
search_amenities(
    search="wifi",
    is_public=1
)

# Buscar piscina
search_amenities(
    search="pool",
    is_public=1
)
```

### Amenidades para Administración
```python
# Obtener todas las amenidades (públicas y privadas)
search_amenities(
    size=1000,
    sort_column="id",
    sort_direction="asc"
)
```

### Amenidades Actualizadas Recientemente
```python
# Ordenar por fecha de actualización
search_amenities(
    is_public=1,
    sort_column="createdAt",
    sort_direction="desc"
)
```

## Ejemplos de Filtrado Avanzado

### Amenidades Premium
```python
# Amenidades de grupos específicos (ej: premium)
search_amenities(
    group_id=5,
    is_public=1,
    is_filterable=1,
    sort_column="order"
)
```

### Amenidades para OTAs
```python
# Amenidades públicas y buscables para canales de distribución
search_amenities(
    is_public=1,
    public_searchable=1,
    is_filterable=1,
    sort_column="order",
    size=100
)
```

## Mejores Prácticas

### 1. Paginación Eficiente
```python
# Usar tamaño de página apropiado
search_amenities(
    page=1,
    size=50,  # Ajustar según necesidades
    is_public=1
)
```

### 2. Ordenamiento Correcto
```python
# Ordenar por 'order' para visualización
search_amenities(
    is_public=1,
    sort_column="order",  # Orden de visualización
    sort_direction="asc"
)

# Ordenar por nombre para listas alfabéticas
search_amenities(
    is_public=1,
    sort_column="name",
    sort_direction="asc"
)
```

### 3. Filtros Combinados
```python
# Combinar múltiples filtros
search_amenities(
    group_id=1,
    is_public=1,
    is_filterable=1,
    public_searchable=1,
    sort_column="order"
)
```

## Respuesta Esperada

```json
{
  "_embedded": {
    "amenities": [
      {
        "id": 1,
        "name": "Swimming Pool",
        "order": 1,
        "isPublic": true,
        "publicSearchable": true,
        "isFilterable": true,
        "groupId": 5,
        "createdAt": "2024-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "name": "WiFi",
        "order": 2,
        "isPublic": true,
        "publicSearchable": true,
        "isFilterable": true,
        "groupId": 1,
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ]
  },
  "page": 1,
  "page_count": 2,
  "page_size": 25,
  "total_items": 45
}
```
"""
