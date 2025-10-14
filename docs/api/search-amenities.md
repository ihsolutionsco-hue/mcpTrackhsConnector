# Search Amenities API

## Descripción

La herramienta `search_amenities` permite buscar y filtrar amenidades disponibles en el sistema TrackHS. Esta herramienta proporciona acceso completo al catálogo de amenidades con soporte de paginación, filtrado y ordenamiento.

## Endpoint

```
GET /pms/units/amenities
```

## Parámetros

### Parámetros de Paginación

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `page` | int | No | Número de página (1-based) | `1` |
| `size` | int | No | Tamaño de página (1-1000) | `25` |

### Parámetros de Ordenamiento

| Parámetro | Tipo | Requerido | Descripción | Valores Válidos |
|-----------|------|-----------|-------------|-----------------|
| `sort_column` | string | No | Columna para ordenar | `id`, `order`, `isPublic`, `publicSearchable`, `isFilterable`, `createdAt` |
| `sort_direction` | string | No | Dirección de ordenamiento | `asc`, `desc` |

### Parámetros de Búsqueda

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `search` | string | No | Búsqueda en id y/o name | `"pool"` |

### Parámetros de Filtrado

| Parámetro | Tipo | Requerido | Descripción | Valores Válidos |
|-----------|------|-----------|-------------|-----------------|
| `group_id` | int | No | Filtro por ID de grupo | Entero positivo |
| `is_public` | int | No | Amenidades públicas | `0`, `1` |
| `public_searchable` | int | No | Amenidades buscables públicamente | `0`, `1` |
| `is_filterable` | int | No | Amenidades filtrables | `0`, `1` |

## Ejemplos de Uso

### Búsqueda Básica

```python
# Obtener primera página de amenidades
search_amenities(page=1, size=25)
```

### Búsqueda con Filtros

```python
# Buscar amenidades públicas del grupo 1
search_amenities(
    page=1,
    size=50,
    group_id=1,
    is_public=1,
    public_searchable=1
)
```

### Búsqueda con Ordenamiento

```python
# Buscar amenidades ordenadas por nombre
search_amenities(
    sort_column="name",
    sort_direction="asc",
    search="pool"
)
```

### Búsqueda Completa

```python
# Búsqueda con todos los parámetros
search_amenities(
    page=2,
    size=50,
    sort_column="isPublic",
    sort_direction="desc",
    search="pool",
    group_id=1,
    is_public=1,
    public_searchable=1,
    is_filterable=1
)
```

## Respuesta

### Estructura de Respuesta

```json
{
  "_embedded": {
    "amenities": [
      {
        "id": 1,
        "name": "Air Conditioning",
        "groupId": 1,
        "groupName": "Additional Amenities",
        "homeawayType": "AMENITIES_AIR_CONDITIONING",
        "airbnbType": "ac",
        "tripadvisorType": "AIR_CONDITIONING",
        "updatedAt": "2020-08-25T12:41:07-04:00",
        "_links": {
          "self": {
            "href": "https://api.example.com/api/pms/units/amenities/1/"
          },
          "group": {
            "href": "https://api.example.com/api/pms/units/amenity-groups/1/"
          }
        }
      }
    ]
  },
  "page": 1,
  "page_count": 8,
  "page_size": 25,
  "total_items": 185,
  "_links": {
    "self": {
      "href": "https://api.example.com/api/pms/units/amenities/?page=1"
    },
    "first": {
      "href": "https://api.example.com/api/pms/units/amenities/"
    },
    "last": {
      "href": "https://api.example.com/api/pms/units/amenities/?page=8"
    },
    "next": {
      "href": "https://api.example.com/api/pms/units/amenities/?page=2"
    }
  }
}
```

### Campos de Amenidad

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | int | ID único de la amenidad |
| `name` | string | Nombre de la amenidad |
| `groupId` | int | ID del grupo al que pertenece |
| `groupName` | string | Nombre del grupo |
| `homeawayType` | string | Tipo para HomeAway (opcional) |
| `airbnbType` | string | Tipo para Airbnb (opcional) |
| `tripadvisorType` | string | Tipo para TripAdvisor (opcional) |
| `updatedAt` | string | Fecha de última actualización (ISO 8601) |
| `_links` | object | Enlaces relacionados |

### Campos de Paginación

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `page` | int | Página actual |
| `page_count` | int | Total de páginas |
| `page_size` | int | Tamaño de página |
| `total_items` | int | Total de elementos |

## Códigos de Error

### 400 Bad Request
- **Causa**: Parámetros inválidos
- **Solución**: Verificar formato y valores de parámetros

### 401 Unauthorized
- **Causa**: Credenciales inválidas o expiradas
- **Solución**: Verificar `TRACKHS_USERNAME` y `TRACKHS_PASSWORD`

### 403 Forbidden
- **Causa**: Permisos insuficientes
- **Solución**: Contactar administrador para habilitar acceso a Channel API

### 404 Not Found
- **Causa**: Endpoint no encontrado
- **Solución**: Verificar URL y disponibilidad del endpoint

### 500 Internal Server Error
- **Causa**: Error interno del servidor
- **Solución**: Reintentar más tarde o contactar soporte

## Validaciones

### Parámetros Obligatorios
- Ningún parámetro es obligatorio (todos tienen valores por defecto)

### Límites
- `page`: Debe ser >= 1
- `size`: Debe estar entre 1 y 1000
- Total de resultados: Máximo 10,000 (page * size <= 10,000)

### Valores Válidos
- `sort_column`: Debe ser uno de los valores permitidos
- `sort_direction`: Debe ser `asc` o `desc`
- `is_public`, `public_searchable`, `is_filterable`: Deben ser 0 o 1
- `group_id`: Debe ser un entero positivo

## Casos de Uso Comunes

### 1. Obtener Todas las Amenidades
```python
search_amenities()
```

### 2. Buscar Amenidades por Nombre
```python
search_amenities(search="pool")
```

### 3. Filtrar Amenidades Públicas
```python
search_amenities(is_public=1, public_searchable=1)
```

### 4. Obtener Amenidades de un Grupo Específico
```python
search_amenities(group_id=1)
```

### 5. Paginación Avanzada
```python
# Página 3 con 50 elementos por página
search_amenities(page=3, size=50)
```

## Notas Técnicas

- La paginación es 1-based (primera página es 1)
- Los parámetros booleanos aceptan 0/1, no true/false
- La búsqueda es case-insensitive
- Los resultados se ordenan por defecto por `order` en dirección `asc`
- El límite de 10,000 resultados totales se aplica para evitar sobrecarga
