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

## ¿Qué son las Amenidades?

Las **amenidades** son características y servicios que ofrece una propiedad (WiFi, piscina, gimnasio, etc.). TrackHS las organiza para:

- **Filtros de búsqueda**: Los huéspedes pueden buscar propiedades por amenidades
- **Listados públicos**: Mostrar qué servicios están disponibles
- **Administración**: Gestionar qué amenidades están activas

## Para Principiantes - Primeros Pasos

### 1. Mi Primera Búsqueda (Más Simple)
```python
# Obtener las primeras 25 amenidades
search_amenities(
    page=1,
    size=25
)
```
**¿Qué hace?** Obtiene las primeras 25 amenidades del sistema.
**¿Cuándo usarlo?** Para ver qué amenidades están disponibles.

### 2. Amenidades Públicas (Básico)
```python
# Obtener amenidades visibles al público
search_amenities(
    is_public=1,
    page=1,
    size=25
)
```
**¿Qué hace?** Busca solo amenidades que son visibles para los huéspedes.
**¿Cuándo usarlo?** Para mostrar amenidades en sitio web público.

### 3. Buscar Amenidad Específica
```python
# Buscar WiFi
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
**¿Qué hace?** Busca amenidades que contengan la palabra especificada.
**¿Cuándo usarlo?** Para encontrar amenidades específicas.

## Búsquedas Comunes

### 4. Amenidades para Filtros
```python
# Obtener amenidades que se pueden usar como filtros
search_amenities(
    is_filterable=1,
    is_public=1,
    sort_column="order",
    sort_direction="asc",
    page=1,
    size=50
)
```
**¿Qué hace?** Busca amenidades que los huéspedes pueden usar para filtrar búsquedas.
**¿Cuándo usarlo?** Para configurar filtros de búsqueda en sitio web.

### 5. Amenidades por Grupo
```python
# Amenidades de grupo específico (ej: comodidades básicas)
search_amenities(
    group_id=1,
    is_public=1,
    sort_column="order",
    sort_direction="asc"
)
```
**¿Qué hace?** Busca amenidades de un grupo específico.
**¿Cuándo usarlo?** Para mostrar amenidades por categoría.

### 6. Amenidades Completamente Activas
```python
# Amenidades públicas, buscables y filtrables
search_amenities(
    is_public=1,
    public_searchable=1,
    is_filterable=1,
    sort_column="order",
    sort_direction="asc"
)
```
**¿Qué hace?** Busca amenidades que están completamente activas para huéspedes.
**¿Cuándo usarlo?** Para listados públicos completos.

### 7. Búsqueda por Texto Avanzada
```python
# Buscar múltiples términos
search_amenities(
    search="wifi internet",
    is_public=1,
    sort_column="name"
)

# Buscar por tipo de amenidad
search_amenities(
    search="kitchen",
    is_public=1,
    sort_column="name"
)
```
**¿Qué hace?** Busca amenidades que contengan los términos especificados.
**¿Cuándo usarlo?** Para encontrar amenidades relacionadas.

## Casos de Uso Típicos

### Listado Público de Amenidades
```python
# Amenidades para mostrar en sitio web público
search_amenities(
    is_public=1,
    public_searchable=1,
    sort_column="order",
    sort_direction="asc",
    page=1,
    size=100
)
```
**¿Qué hace?** Obtiene amenidades para mostrar a huéspedes potenciales.
**¿Cuándo usarlo?** Para páginas de "Servicios y Amenidades" del sitio web.

### Filtros de Búsqueda de Unidades
```python
# Amenidades para filtros de búsqueda
search_amenities(
    is_filterable=1,
    is_public=1,
    sort_column="order",
    sort_direction="asc",
    size=50
)
```
**¿Qué hace?** Obtiene amenidades para usar como filtros en búsqueda de propiedades.
**¿Cuándo usarlo?** Para configurar filtros "WiFi", "Piscina", "Gimnasio", etc.

### Amenidades por Categoría
```python
# Amenidades básicas (grupo 1)
search_amenities(
    group_id=1,
    is_public=1,
    sort_column="order"
)

# Amenidades premium (grupo 5)
search_amenities(
    group_id=5,
    is_public=1,
    sort_column="order"
)
```
**¿Qué hace?** Organiza amenidades por categorías o grupos.
**¿Cuándo usarlo?** Para mostrar amenidades por tipo (básicas, premium, etc.).

### Búsqueda de Amenidades Específicas
```python
# Buscar amenidades de conectividad
search_amenities(
    search="wifi internet",
    is_public=1
)

# Buscar amenidades de entretenimiento
search_amenities(
    search="tv entertainment",
    is_public=1
)

# Buscar amenidades de cocina
search_amenities(
    search="kitchen cooking",
    is_public=1
)
```
**¿Qué hace?** Busca amenidades por tipo o función específica.
**¿Cuándo usarlo?** Para encontrar amenidades relacionadas con un tema.

### Administración de Amenidades
```python
# Todas las amenidades (públicas y privadas)
search_amenities(
    size=1000,
    sort_column="id",
    sort_direction="asc"
)

# Amenidades recientemente creadas
search_amenities(
    is_public=1,
    sort_column="createdAt",
    sort_direction="desc",
    page=1,
    size=50
)
```
**¿Qué hace?** Obtiene amenidades para administración y gestión.
**¿Cuándo usarlo?** Para configurar y administrar amenidades del sistema.

## Tabla de Referencia Rápida

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `page` | int | Número de página | 1, 2, 3... |
| `size` | int | Resultados por página | 1-1000 |
| `search` | string | Búsqueda por texto | "wifi", "pool" |
| `group_id` | int | ID del grupo | 1, 2, 3... |
| `is_public` | int | Visible al público | 0=No, 1=Sí |
| `public_searchable` | int | Buscable públicamente | 0=No, 1=Sí |
| `is_filterable` | int | Usable como filtro | 0=No, 1=Sí |
| `sort_column` | string | Campo de ordenamiento | "id", "name", "order", "createdAt" |
| `sort_direction` | string | Dirección de ordenamiento | "asc", "desc" |

## Filtros Booleanos Explicados

### `is_public` (Visible al Público)
- **0**: Amenidad privada (solo administradores)
- **1**: Amenidad visible para huéspedes

### `public_searchable` (Buscable Públicamente)
- **0**: No aparece en búsquedas de huéspedes
- **1**: Aparece en búsquedas de huéspedes

### `is_filterable` (Usable como Filtro)
- **0**: No se puede usar como filtro de búsqueda
- **1**: Se puede usar como filtro de búsqueda

## Mejores Prácticas

### 1. Paginación Eficiente
```python
# Para listados públicos (pocos resultados)
search_amenities(
    is_public=1,
    page=1,
    size=25
)

# Para administración (más resultados)
search_amenities(
    page=1,
    size=100
)
```

### 2. Ordenamiento Correcto
```python
# Para visualización (orden lógico)
search_amenities(
    is_public=1,
    sort_column="order",
    sort_direction="asc"
)

# Para listas alfabéticas
search_amenities(
    is_public=1,
    sort_column="name",
    sort_direction="asc"
)
```

### 3. Filtros Combinados
```python
# Amenidades completamente activas
search_amenities(
    is_public=1,
    public_searchable=1,
    is_filterable=1,
    sort_column="order"
)
```

## Respuestas Esperadas

### Respuesta Básica
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

### Respuesta con Búsqueda
```json
{
  "_embedded": {
    "amenities": [
      {
        "id": 15,
        "name": "Free WiFi",
        "order": 15,
        "isPublic": true,
        "publicSearchable": true,
        "isFilterable": true,
        "groupId": 1,
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ]
  },
  "page": 1,
  "page_count": 1,
  "page_size": 25,
  "total_items": 1
}
```

## Errores Comunes y Soluciones

### Error: "Page must be >= 1"
```python
# ❌ Incorrecto
search_amenities(page=0)

# ✅ Correcto
search_amenities(page=1)
```

### Error: "Size must be between 1 and 1000"
```python
# ❌ Incorrecto
search_amenities(size=2000)

# ✅ Correcto
search_amenities(size=100)
```

### Error: "Invalid sort column"
```python
# ❌ Incorrecto
search_amenities(sort_column="invalid")

# ✅ Correcto
search_amenities(sort_column="name")
```

## Campos de Ordenamiento Válidos

- `"id"` - Por ID numérico
- `"name"` - Por nombre alfabético
- `"order"` - Por orden de visualización
- `"isPublic"` - Por visibilidad pública
- `"publicSearchable"` - Por capacidad de búsqueda
- `"isFilterable"` - Por capacidad de filtrado
- `"createdAt"` - Por fecha de creación
"""
