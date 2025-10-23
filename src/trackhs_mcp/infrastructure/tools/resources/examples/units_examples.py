"""
Examples resources para Units
Ejemplos de uso para la herramienta search_units
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_units_examples(mcp, api_client: "ApiClientPort"):
    """Registra los ejemplos de búsqueda de unidades"""

    @mcp.resource(
        "trackhs://examples/units",
        name="Units Examples",
        description="Common units search examples",
        mime_type="text/plain",
    )
    async def units_examples() -> str:
        """Ejemplos de búsquedas de unidades"""
        return """# TrackHS Units Search Examples

## ¿Qué son las Unidades?

Las **unidades** son propiedades individuales que se pueden reservar (casas, apartamentos, villas, etc.). TrackHS las organiza con:

- **Características**: Habitaciones, baños, capacidad
- **Amenidades**: WiFi, piscina, gimnasio, etc.
- **Disponibilidad**: Fechas libres y ocupadas
- **Ubicación**: Nodos y oficinas locales
- **Estado**: Limpia, sucia, ocupada, en mantenimiento

## Para Principiantes - Primeros Pasos

### 1. Mi Primera Búsqueda (Más Simple)
```python
# Obtener las primeras 3 unidades
search_units(
    page=1,
    size=3
)
```
**¿Qué hace?** Obtiene las primeras 3 unidades del sistema.
**¿Cuándo usarlo?** Para ver qué unidades están disponibles.

### 2. Buscar por Características Básicas
```python
# Buscar unidades con 2 habitaciones
search_units(
    bedrooms="2",
    page=1,
    size=10
)

# Buscar unidades con 2 baños
search_units(
    bathrooms="2",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades por número de habitaciones o baños.
**¿Cuándo usarlo?** Para filtrar por características básicas.

### 3. Buscar Unidades Activas
```python
# Buscar solo unidades activas
search_units(
    is_active="1",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca solo unidades que están activas y disponibles.
**¿Cuándo usarlo?** Para mostrar unidades disponibles para reservas.

## Búsquedas Comunes

### 4. Búsqueda por Características Detalladas
```python
# Unidades con 3+ habitaciones y 2+ baños
search_units(
    min_bedrooms="3",
    min_bathrooms="2",
    page=1,
    size=20
)

# Unidades exactas: 2 habitaciones, 1 baño
search_units(
    bedrooms="2",
    bathrooms="1",
    page=1,
    size=15
)
```
**¿Qué hace?** Busca unidades con características específicas.
**¿Cuándo usarlo?** Para encontrar unidades que cumplan requisitos específicos.

### 5. Búsqueda por Amenidades
```python
# Unidades con WiFi
search_units(
    amenity_id="1",  # ID de amenidad WiFi
    is_active="1",
    page=1,
    size=10
)

# Unidades con piscina
search_units(
    amenity_id="5",  # ID de amenidad piscina
    is_active="1",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades que tengan amenidades específicas.
**¿Cuándo usarlo?** Para filtrar por servicios disponibles.

### 6. Búsqueda por Disponibilidad
```python
# Unidades disponibles en fechas específicas
search_units(
    arrival="2024-06-15",
    departure="2024-06-20",
    is_active="1",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades disponibles en fechas específicas.
**¿Cuándo usarlo?** Para verificar disponibilidad en fechas de viaje.

### 7. Búsqueda por Ubicación
```python
# Unidades en nodo específico
search_units(
    node_id="1",
    is_active="1",
    page=1,
    size=20
)

# Unidades de tipo específico
search_units(
    unit_type_id="2",  # Ej: villas
    is_active="1",
    page=1,
    size=15
)
```
**¿Qué hace?** Busca unidades por ubicación o tipo.
**¿Cuándo usarlo?** Para filtrar por ubicación geográfica o tipo de propiedad.

### 8. Búsqueda por Estado de Limpieza
```python
# Unidades limpias
search_units(
    unit_status="clean",
    is_active="1",
    page=1,
    size=10
)

# Unidades ocupadas
search_units(
    unit_status="occupied",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades por estado de housekeeping.
**¿Cuándo usarlo?** Para gestión de limpieza y mantenimiento.

## Casos de Uso Típicos

### Búsqueda para Huéspedes
```python
# Buscar unidades disponibles para 4 personas
search_units(
    min_bedrooms="2",
    min_bathrooms="1",
    arrival="2024-06-15",
    departure="2024-06-20",
    is_active="1",
    is_bookable="1",
    page=1,
    size=20
)
```
**¿Qué hace?** Busca unidades disponibles para huéspedes.
**¿Cuándo usarlo?** Para mostrar opciones de alojamiento a huéspedes.

### Búsqueda por Amenidades Específicas
```python
# Unidades con WiFi y piscina
search_units(
    amenity_id="1,5",  # WiFi y piscina
    is_active="1",
    is_bookable="1",
    page=1,
    size=15
)

# Unidades pet-friendly
search_units(
    pets_friendly="1",
    is_active="1",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades con amenidades específicas.
**¿Cuándo usarlo?** Para filtros de búsqueda avanzados.

### Búsqueda por Características de Accesibilidad
```python
# Unidades accesibles
search_units(
    is_accessible="1",
    is_active="1",
    page=1,
    size=10
)

# Unidades que permiten eventos
search_units(
    events_allowed="1",
    is_active="1",
    page=1,
    size=10
)
```
**¿Qué hace?** Busca unidades con características especiales.
**¿Cuándo usarlo?** Para necesidades específicas de accesibilidad o eventos.

### Búsqueda para Administración
```python
# Todas las unidades (administración)
search_units(
    page=1,
    size=100,
    sort_column="name",
    sort_direction="asc"
)

# Unidades actualizadas recientemente
search_units(
    updated_since="2024-01-01T00:00:00Z",
    page=1,
    size=50
)
```
**¿Qué hace?** Obtiene unidades para administración.
**¿Cuándo usarlo?** Para gestión y administración de propiedades.

## Tabla de Referencia Rápida

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `page` | int | Número de página | 1, 2, 3... |
| `size` | int | Resultados por página | 1-25 |
| `search` | string | Búsqueda por texto | "villa", "apartment" |
| `bedrooms` | string | Habitaciones exactas | "1", "2", "3" |
| `min_bedrooms` | string | Mínimo de habitaciones | "2", "3" |
| `max_bedrooms` | string | Máximo de habitaciones | "4", "5" |
| `bathrooms` | string | Baños exactos | "1", "2" |
| `min_bathrooms` | string | Mínimo de baños | "1", "2" |
| `max_bathrooms` | string | Máximo de baños | "3", "4" |
| `pets_friendly` | string | Permite mascotas | "0"=No, "1"=Sí |
| `is_active` | string | Unidad activa | "0"=No, "1"=Sí |
| `is_bookable` | string | Reservable | "0"=No, "1"=Sí |
| `is_accessible` | string | Accesible | "0"=No, "1"=Sí |
| `events_allowed` | string | Permite eventos | "0"=No, "1"=Sí |
| `smoking_allowed` | string | Permite fumar | "0"=No, "1"=Sí |
| `children_allowed` | string | Permite niños | "0"=No, "1"=Sí |
| `arrival` | string | Fecha de llegada | "2024-06-15" |
| `departure` | string | Fecha de salida | "2024-06-20" |
| `unit_status` | string | Estado de limpieza | "clean", "dirty", "occupied" |
| `node_id` | string | ID del nodo | "1", "2", "3" |
| `unit_type_id` | string | ID del tipo | "1", "2", "3" |
| `amenity_id` | string | ID de amenidad | "1", "2", "3" |

## Filtros Booleanos Explicados

### `pets_friendly` (Permite Mascotas)
- **"0"**: No permite mascotas
- **"1"**: Permite mascotas

### `is_active` (Unidad Activa)
- **"0"**: Unidad inactiva (no disponible)
- **"1"**: Unidad activa (disponible)

### `is_bookable` (Reservable)
- **"0"**: No se puede reservar
- **"1"**: Se puede reservar

### `is_accessible` (Accesible)
- **"0"**: No accesible para sillas de ruedas
- **"1"**: Accesible para sillas de ruedas

### `events_allowed` (Permite Eventos)
- **"0"**: No permite eventos
- **"1"**: Permite eventos

### `smoking_allowed` (Permite Fumar)
- **"0"**: No permite fumar
- **"1"**: Permite fumar

### `children_allowed` (Permite Niños)
- **"0"**: No permite niños
- **"1"**: Permite niños

## Estados de Unidad

| Estado | Descripción | Cuándo Aparece |
|--------|-------------|----------------|
| `"clean"` | Unidad limpia y lista | Después de limpieza |
| `"dirty"` | Unidad sucia | Después de checkout |
| `"occupied"` | Unidad ocupada | Durante estadía |
| `"inspection"` | En inspección | Durante revisión |
| `"inprogress"` | En mantenimiento | Durante reparaciones |

## Mejores Prácticas

### 1. Búsqueda Eficiente
```python
# Para búsquedas públicas (pocos resultados)
search_units(
    is_active="1",
    is_bookable="1",
    page=1,
    size=10
)

# Para administración (más resultados)
search_units(
    page=1,
    size=25
)
```

### 2. Filtros Combinados
```python
# Combinar múltiples filtros
search_units(
    min_bedrooms="2",
    min_bathrooms="1",
    pets_friendly="1",
    is_active="1",
    is_bookable="1",
    page=1,
    size=15
)
```

### 3. Búsqueda por Disponibilidad
```python
# Verificar disponibilidad en fechas específicas
search_units(
    arrival="2024-06-15",
    departure="2024-06-20",
    is_active="1",
    is_bookable="1",
    page=1,
    size=20
)
```

## Respuestas Esperadas

### Respuesta Básica
```json
{
  "_embedded": {
    "units": [
      {
        "id": 101,
        "name": "Villa Paradise",
        "code": "VP001",
                    "bedrooms": 3,
        "bathrooms": 2,
        "maxOccupancy": 6,
        "isActive": true,
        "isBookable": true,
        "petsFriendly": true,
        "isAccessible": false,
        "eventsAllowed": true,
        "smokingAllowed": false,
        "childrenAllowed": true,
        "unitStatus": "clean",
        "node": {
          "id": 1,
          "name": "Beach Resort"
        },
        "unitType": {
          "id": 2,
          "name": "Villa"
        },
        "amenities": [
          {
            "id": 1,
            "name": "WiFi"
          },
          {
            "id": 5,
            "name": "Swimming Pool"
          }
        ]
      }
    ]
  },
  "page": 1,
  "page_count": 1,
  "page_size": 10,
  "total_items": 1
}
```

### Respuesta con Disponibilidad
```json
{
                    "_embedded": {
                        "units": [
                            {
        "id": 102,
        "name": "Beach House",
        "availability": {
          "2024-06-15": "available",
          "2024-06-16": "available",
          "2024-06-17": "occupied"
        }
      }
    ]
  }
}
```

## Errores Comunes y Soluciones

### Error: "Page must be >= 1"
```python
# ❌ Incorrecto
search_units(page=0)

# ✅ Correcto
search_units(page=1)
```

### Error: "Size must be between 1 and 25"
```python
# ❌ Incorrecto
search_units(size=50)

# ✅ Correcto
search_units(size=10)
```

### Error: "Invalid date format"
```python
# ❌ Incorrecto
search_units(arrival="06/15/2024")

# ✅ Correcto
search_units(arrival="2024-06-15")
```

### Error: "Invalid unit status"
```python
# ❌ Incorrecto
search_units(unit_status="available")

# ✅ Correcto
search_units(unit_status="clean")
```

## Campos de Ordenamiento Válidos

- `"id"` - Por ID numérico
- `"name"` - Por nombre alfabético
- `"nodeName"` - Por nombre del nodo
- `"unitTypeName"` - Por tipo de unidad

## Casos de Uso Avanzados

### Búsqueda por Rango de Características
```python
# Unidades entre 2-4 habitaciones
search_units(
    min_bedrooms="2",
    max_bedrooms="4",
    is_active="1",
    page=1,
    size=20
)
```

### Búsqueda por Múltiples Amenidades
```python
# Unidades con WiFi, piscina y gimnasio
search_units(
    amenity_id="1,5,10",  # WiFi, piscina, gimnasio
    is_active="1",
    page=1,
    size=15
)
```

### Búsqueda por Texto
```python
# Buscar por nombre o descripción
search_units(
    search="villa",
    is_active="1",
    page=1,
    size=10
)
```

### Búsqueda por Código de Unidad
```python
# Buscar unidad específica por código
search_units(
    unit_code="VP001",
    page=1,
    size=1
)
```
"""
