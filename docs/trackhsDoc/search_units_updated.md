# Search Units - TrackHS Channel API

## Descripción General

La herramienta `search_units` proporciona capacidades avanzadas de búsqueda de unidades en la API Channel de TrackHS, con soporte para filtrado por características de propiedades, disponibilidad, ubicación y más. Optimizada para integración con modelos de IA.

## Características Principales

- **Compatibilidad completa con Channel API** con 35+ parámetros de filtrado
- **Filtrado por características de propiedades** (dormitorios, baños, mascotas, accesibilidad)
- **Verificación de disponibilidad** con rangos de fechas
- **Filtrado por ubicación y amenidades**
- **Filtrado por estado de limpieza**
- **Detalles completos de unidades** incluyendo descripciones, imágenes y tarifas
- **Tipos de parámetros flexibles** (acepta tanto string como integer para filtros numéricos/booleanos)

## Parámetros de Entrada

### Paginación
- `page` (int): Número de página (indexación basada en 1). Máximo 10,000 resultados totales.
- `size` (int): Número de resultados por página (1-25).

### Ordenamiento
- `sort_column` (str): Columna para ordenar. Valores válidos: id, name, nodeName, unitTypeName
- `sort_direction` (str): Dirección de ordenamiento. Valores: 'asc' o 'desc'

### Búsqueda de Texto
- `search` (str, opcional): Búsqueda de texto completo en nombres, códigos y descripciones de unidades
- `term` (str, opcional): Término de búsqueda para nombres y descripciones de unidades
- `unit_code` (str, opcional): Código exacto de unidad para buscar
- `short_name` (str, opcional): Búsqueda por nombre corto de unidad

### Filtros por IDs
- `node_id` (str, opcional): Filtrar por IDs de nodo (separados por comas: '1,2,3')
- `amenity_id` (str, opcional): Filtrar por IDs de amenidades (separados por comas: '1,2,3')
- `unit_type_id` (str, opcional): Filtrar por IDs de tipo de unidad (separados por comas: '1,2,3')
- `id` (str, opcional): Filtrar por IDs de unidad (separados por comas: '1,2,3')

### Filtros Numéricos
- `calendar_id` (int, opcional): Filtrar por ID de calendario (entero positivo)
- `role_id` (int, opcional): Filtrar por ID de rol (entero positivo)

### Filtros de Habitaciones y Baños
- `bedrooms` (str, opcional): Filtrar por número exacto de dormitorios
- `min_bedrooms` (str, opcional): Filtrar por número mínimo de dormitorios
- `max_bedrooms` (str, opcional): Filtrar por número máximo de dormitorios
- `bathrooms` (str, opcional): Filtrar por número exacto de baños
- `min_bathrooms` (str, opcional): Filtrar por número mínimo de baños
- `max_bathrooms` (str, opcional): Filtrar por número máximo de baños

### Filtros Booleanos (0/1)
- `pets_friendly` (str, opcional): Filtrar unidades que permiten mascotas
- `allow_unit_rates` (str, opcional): Filtrar unidades que permiten tarifas específicas
- `computed` (str, opcional): Filtrar unidades computadas
- `inherited` (str, opcional): Filtrar unidades heredadas
- `limited` (str, opcional): Filtrar unidades de disponibilidad limitada
- `is_bookable` (str, opcional): Filtrar unidades reservables
- `include_descriptions` (str, opcional): Incluir descripciones de unidades
- `is_active` (str, opcional): Filtrar por unidades activas
- `events_allowed` (str, opcional): Filtrar unidades que permiten eventos
- `smoking_allowed` (str, opcional): Filtrar unidades que permiten fumar
- `children_allowed` (str, opcional): Filtrar unidades que permiten niños
- `is_accessible` (str, opcional): Filtrar unidades accesibles para sillas de ruedas

### Filtros de Fechas (ISO 8601)
- `arrival` (str, opcional): Filtrar por fecha de llegada
- `departure` (str, opcional): Filtrar por fecha de salida
- `content_updated_since` (str, opcional): Filtrar por fecha de actualización de contenido
- `updated_since` (str, opcional): Filtrar por fecha de última actualización

### Estado de Limpieza
- `unit_status` (str, opcional): Filtrar por estado de limpieza. Valores válidos: clean, dirty, occupied, inspection, inprogress

## Respuesta

### Estructura de Respuesta
```json
{
  "_links": {
    "self": {"href": "..."},
    "first": {"href": "..."},
    "last": {"href": "..."},
    "next": {"href": "..."}
  },
  "_embedded": {
    "units": [
      {
        "id": 215,
        "name": "5 Bedroom luxury home by Disney-338",
        "shortName": "1145 KINGSBARN ST",
        "unitCode": "338",
        "bedrooms": 5,
        "fullBathrooms": 5,
        "maxOccupancy": 15,
        "petFriendly": true,
        "smokingAllowed": false,
        "childrenAllowed": true,
        "isAccessible": false,
        "isActive": true,
        "isBookable": true,
        "nodeId": 3,
        "lodgingType": {
          "id": 1,
          "name": "House"
        },
        "amenitiesIds": [1, 66, 77, 96, 97, 101, 166, 189, 243, ...],
        "_embedded": {
          "node": {
            "id": 3,
            "name": "Champions Gate"
          }
        }
      }
    ]
  },
  "page_count": 29,
  "page_size": 5,
  "total_items": 141,
  "page": 1
}
```

### Campos Principales de Unidad
- `id`: ID único de la unidad
- `name`: Nombre de la unidad
- `shortName`: Nombre corto de la unidad
- `unitCode`: Código de la unidad
- `bedrooms`: Número de dormitorios
- `fullBathrooms`: Número de baños completos
- `maxOccupancy`: Ocupación máxima
- `petFriendly`: Permite mascotas
- `smokingAllowed`: Permite fumar
- `childrenAllowed`: Permite niños
- `isAccessible`: Accesible para sillas de ruedas
- `isActive`: Unidad activa
- `isBookable`: Unidad reservable
- `nodeId`: ID del nodo (ubicación)
- `lodgingType`: Tipo de alojamiento
- `amenitiesIds`: IDs de amenidades

## Casos de Uso Comunes

### 1. Búsqueda por Características
```python
# Buscar propiedades de 3 dormitorios, pet-friendly y activas
search_units(
    bedrooms="3",
    pets_friendly="1",
    is_active="1"
)
```

### 2. Búsqueda por Ubicación
```python
# Buscar propiedades en Champions Gate
search_units(node_id="3")
```

### 3. Búsqueda por Amenidades
```python
# Buscar propiedades con piscina (amenidad 77)
search_units(amenity_id="77")
```

### 4. Búsqueda por Disponibilidad
```python
# Buscar propiedades disponibles en fechas específicas
search_units(
    arrival="2024-01-15",
    departure="2024-01-20"
)
```

### 5. Búsqueda de Texto
```python
# Buscar villas
search_units(search="Villa")
```

## Validaciones y Errores

### Validaciones de Entrada
- **Fechas**: Deben estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)
- **Parámetros numéricos**: Deben ser enteros o strings convertibles a enteros
- **Parámetros booleanos**: Deben ser '0' o '1'
- **Límite total**: page * size debe ser <= 10,000
- **Rangos**: min_bedrooms no puede ser mayor que max_bedrooms

### Códigos de Error Comunes
- **400 Bad Request**: Parámetros inválidos
- **401 Unauthorized**: Credenciales de autenticación inválidas
- **403 Forbidden**: Permisos insuficientes
- **404 Not Found**: Endpoint no encontrado
- **500 Internal Server Error**: Error interno del servidor

## Ejemplos de Respuestas del Testing

### Resultado de Búsqueda por Características
```json
{
  "total_items": 5,
  "_embedded": {
    "units": [
      {
        "id": 200,
        "name": "2 Bedroom Condo minutes from Disney 325",
        "bedrooms": 2,
        "fullBathrooms": 2,
        "petFriendly": true,
        "isActive": true,
        "isBookable": true
      }
    ]
  }
}
```

### Resultado de Búsqueda por Ubicación
```json
{
  "total_items": 141,
  "_embedded": {
    "units": [
      {
        "id": 215,
        "name": "5 Bedroom luxury home by Disney-338",
        "nodeId": 3,
        "bedrooms": 5,
        "fullBathrooms": 5,
        "maxOccupancy": 15
      }
    ]
  }
}
```

### Resultado de Búsqueda por Amenidades
```json
{
  "total_items": 115,
  "_embedded": {
    "units": [
      {
        "id": 200,
        "name": "2 Bedroom Condo minutes from Disney 325",
        "amenitiesIds": [77, 63, 72, 84, 101, 115, 118, 138, 140, 174, 180, 198, 220, 221, 229, ...]
      }
    ]
  }
}
```

## Mejores Prácticas

1. **Paginación**: Use `size` pequeño (3-5) para respuestas rápidas
2. **Filtros específicos**: Combine múltiples filtros para resultados precisos
3. **Validación de fechas**: Siempre use formato ISO 8601 para fechas
4. **Manejo de errores**: Implemente manejo robusto de errores HTTP
5. **Caché**: Considere cachear resultados para consultas frecuentes

## Limitaciones

- Máximo 10,000 resultados totales (page * size)
- Máximo 25 resultados por página
- Fechas deben estar en formato ISO 8601
- Parámetros booleanos solo aceptan '0' o '1'
- IDs múltiples deben estar separados por comas

## Notas de Implementación

- La API usa paginación basada en 1 (page=1 es la primera página)
- Los parámetros numéricos pueden pasarse como strings o enteros
- Los parámetros booleanos deben pasarse como strings '0' o '1'
- Las fechas deben estar en formato ISO 8601 con validación de patrón
- Los IDs múltiples se pasan como strings separados por comas
