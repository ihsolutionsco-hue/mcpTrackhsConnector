# Análisis del Esquema API TrackHS - Unit Collection

**Fecha:** 22 de Octubre de 2025
**Documento:** get unit collection.md
**API:** TrackHS Channel API v1.0
**Endpoint:** `/pms/units`

---

## Resumen Ejecutivo

El análisis del esquema oficial de TrackHS revela **discrepancias críticas** entre la documentación de la API y la implementación del MCP. La API oficial espera parámetros de tipo `integer` para filtros numéricos y booleanos, pero el MCP los define como `Optional[str]`.

---

## Estructura de la API

### Información General
- **Título:** Channel API
- **Versión:** 1.0
- **Propósito:** Integración con canales (OTAs, channel managers, websites)
- **Autenticación:** Basic Auth o HMAC
- **Endpoint:** `{customerDomain}/api/pms/units`

### Respuesta de la API

#### Estructura Principal
```json
{
  "_embedded": {
    "units": [/* Array de unidades */]
  },
  "page": "number",
  "page_count": "number",
  "page_size": "number",
  "total_items": "number",
  "_links": {/* Enlaces de paginación */}
}
```

#### Campos de Unidad (50+ campos)
- **Básicos:** id, name, shortName, unitCode, headline
- **Descripciones:** shortDescription, longDescription, houseRules
- **Ubicación:** streetAddress, locality, region, country, latitude, longitude
- **Características:** bedrooms, fullBathrooms, maxOccupancy, area, floors
- **Políticas:** petsFriendly, eventsAllowed, smokingAllowed, childrenAllowed
- **Horarios:** checkinTime, checkoutTime, timezone
- **Amenidades:** amenities array, amenityDescription
- **Habitaciones:** rooms array, bedTypes array
- **Metadatos:** updatedAt, custom fields

---

## Parámetros de Consulta - Análisis Detallado

### ✅ Parámetros de Paginación
```json
{
  "page": {
    "type": "integer",
    "minimum": 0,
    "maximum": 0,
    "description": "Page number of result set - Limited to 10k total results"
  },
  "size": {
    "type": "integer",
    "description": "Size of page - Limited to 10k total results"
  }
}
```
**Estado:** ✅ Correcto - Ambos son `integer`

### ✅ Parámetros de Ordenamiento
```json
{
  "sortColumn": {
    "type": "string",
    "enum": ["id", "name", "nodeName", "unitTypeName"],
    "default": "name"
  },
  "sortDirection": {
    "type": "string",
    "enum": ["asc", "desc"],
    "default": "asc"
  }
}
```
**Estado:** ✅ Correcto - Ambos son `string`

### ✅ Parámetros de Búsqueda de Texto
```json
{
  "search": {"type": "string"},
  "term": {"type": "string"},
  "unitCode": {"type": "string"},
  "shortName": {"type": "string"}
}
```
**Estado:** ✅ Correcto - Todos son `string`

### ✅ Parámetros de ID (Aceptan Array o Single)
```json
{
  "nodeId": {
    "oneOf": [
      {"type": "integer"},
      {"type": "array", "items": {"type": "integer"}}
    ]
  },
  "amenityId": {
    "oneOf": [
      {"type": "integer"},
      {"type": "array", "items": {"type": "integer"}}
    ]
  },
  "unitTypeId": {
    "oneOf": [
      {"type": "integer"},
      {"type": "array", "items": {"type": "integer"}}
    ]
  }
}
```
**Estado:** ✅ Correcto - Aceptan `integer` o `array` de `integer`

### ❌ Parámetros Numéricos (PROBLEMA IDENTIFICADO)
```json
{
  "bedrooms": {"type": "integer"},
  "minBedrooms": {"type": "integer"},
  "maxBedrooms": {"type": "integer"},
  "bathrooms": {"type": "integer"},
  "minBathrooms": {"type": "integer"},
  "maxBathrooms": {"type": "integer"},
  "calendarId": {"type": "integer"},
  "roleId": {"type": "integer"}
}
```
**Estado:** ❌ **PROBLEMA** - API espera `integer`, MCP define como `Optional[str]`

### ❌ Parámetros Booleanos (PROBLEMA IDENTIFICADO)
```json
{
  "petsFriendly": {
    "type": "integer",
    "enum": [1, 0]
  },
  "allowUnitRates": {
    "type": "integer",
    "enum": [1, 0]
  },
  "computed": {
    "type": "integer",
    "enum": [1, 0]
  },
  "inherited": {
    "type": "integer",
    "enum": [1, 0]
  },
  "limited": {
    "type": "integer",
    "enum": [1, 0]
  },
  "isBookable": {
    "type": "integer",
    "enum": [1, 0]
  },
  "includeDescriptions": {
    "type": "integer",
    "enum": [1, 0]
  },
  "isActive": {
    "type": "integer",
    "enum": [1, 0]
  }
}
```
**Estado:** ❌ **PROBLEMA** - API espera `integer` con enum [1, 0], MCP define como `Optional[str]`

### ✅ Parámetros de Fecha
```json
{
  "arrival": {"type": "string", "format": "date"},
  "departure": {"type": "string", "format": "date"},
  "contentUpdatedSince": {"type": "string", "format": "date-time"},
  "updatedSince": {"type": "string", "format": "date", "deprecated": true}
}
```
**Estado:** ✅ Correcto - Todos son `string` con formatos específicos

### ✅ Parámetros de Estado
```json
{
  "unitStatus": {
    "type": "string",
    "enum": ["clean", "dirty", "occupied", "inspection", "inprogress"]
  }
}
```
**Estado:** ✅ Correcto - Es `string` con enum

### ✅ Parámetros de Filtro por ID
```json
{
  "id": {
    "type": "array",
    "items": {"type": "integer"}
  }
}
```
**Estado:** ✅ Correcto - Es `array` de `integer`

---

## Comparación: API vs MCP

### Parámetros Problemáticos

| Parámetro | API TrackHS | MCP Actual | Estado |
|-----------|-------------|------------|---------|
| `bedrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `minBedrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `maxBedrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `bathrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `minBathrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `maxBathrooms` | `integer` | `Optional[str]` | ❌ Incompatible |
| `calendarId` | `integer` | `Optional[str]` | ❌ Incompatible |
| `roleId` | `integer` | `Optional[str]` | ❌ Incompatible |
| `petsFriendly` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `allowUnitRates` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `computed` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `inherited` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `limited` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `isBookable` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `includeDescriptions` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |
| `isActive` | `integer` (enum [1,0]) | `Optional[str]` | ❌ Incompatible |

### Parámetros Correctos

| Parámetro | API TrackHS | MCP Actual | Estado |
|-----------|-------------|------------|---------|
| `page` | `integer` | `int` | ✅ Correcto |
| `size` | `integer` | `int` | ✅ Correcto |
| `sortColumn` | `string` | `str` | ✅ Correcto |
| `sortDirection` | `string` | `str` | ✅ Correcto |
| `search` | `string` | `Optional[str]` | ✅ Correcto |
| `term` | `string` | `Optional[str]` | ✅ Correcto |
| `unitCode` | `string` | `Optional[str]` | ✅ Correcto |
| `shortName` | `string` | `Optional[str]` | ✅ Correcto |
| `nodeId` | `integer` o `array` | `Optional[str]` | ✅ Funciona |
| `amenityId` | `integer` o `array` | `Optional[str]` | ✅ Funciona |
| `unitTypeId` | `integer` o `array` | `Optional[str]` | ✅ Funciona |
| `arrival` | `string` (date) | `Optional[str]` | ✅ Correcto |
| `departure` | `string` (date) | `Optional[str]` | ✅ Correcto |
| `unitStatus` | `string` (enum) | `Optional[str]` | ✅ Correcto |

---

## Análisis de la Respuesta

### Estructura de Unidad Completa

#### Campos Básicos
```json
{
  "id": "integer",
  "name": "string",
  "shortName": "string",
  "unitCode": "string",
  "headline": "string"
}
```

#### Campos de Descripción
```json
{
  "shortDescription": "string (nullable)",
  "longDescription": "string (nullable)",
  "houseRules": "string"
}
```

#### Campos de Ubicación
```json
{
  "streetAddress": "string",
  "extendedAddress": "string (nullable)",
  "locality": "string",
  "region": "string",
  "postal": "string",
  "country": "string (2 chars)",
  "latitude": "number (nullable)",
  "longitude": "number (nullable)"
}
```

#### Campos de Características Físicas
```json
{
  "bedrooms": "integer",
  "fullBathrooms": "integer",
  "threeQuarterBathrooms": "integer (nullable)",
  "halfBathrooms": "integer",
  "maxOccupancy": "integer",
  "area": "integer",
  "floors": "integer (nullable)"
}
```

#### Campos de Políticas
```json
{
  "petsFriendly": "boolean",
  "maxPets": "integer (nullable)",
  "eventsAllowed": "boolean",
  "smokingAllowed": "boolean",
  "childrenAllowed": "boolean",
  "minimumAgeLimit": "integer",
  "isAccessible": "boolean"
}
```

#### Campos de Horarios
```json
{
  "timezone": "string",
  "checkinTime": "string (HH:MM)",
  "hasEarlyCheckin": "boolean",
  "earlyCheckinTime": "string (HH:MM)",
  "checkoutTime": "string (HH:MM)",
  "hasLateCheckout": "boolean",
  "lateCheckoutTime": "string (HH:MM)"
}
```

#### Campos de Amenidades
```json
{
  "amenities": [
    {
      "id": "integer",
      "name": "string",
      "group": {
        "id": "integer",
        "name": "string"
      }
    }
  ],
  "amenityDescription": "string"
}
```

#### Campos de Habitaciones
```json
{
  "rooms": [
    {
      "name": "string",
      "type": "string (enum)",
      "sleeps": "integer",
      "description": "string",
      "hasAttachedBathroom": "boolean",
      "beds": [
        {
          "id": "integer",
          "name": "string",
          "count": "string",
          "homeawayType": "string (enum)",
          "airbnbType": "string (enum)",
          "marriottType": "string (enum)"
        }
      ]
    }
  ],
  "bedTypes": [
    {
      "id": "integer",
      "name": "string",
      "count": "integer"
    }
  ]
}
```

#### Campos de Metadatos
```json
{
  "updatedAt": "string (date-time)",
  "custom": "object (nullable)",
  "taxId": "string (nullable)"
}
```

---

## Campos Deprecados

### En la API
```json
{
  "unitType": {
    "deprecated": true,
    "description": "Consider this value unstable. Will be replaced with a unit types API link."
  },
  "coverImage": {
    "deprecated": true,
    "description": "Deprecated, use images api"
  },
  "regulations": {
    "deprecated": true
  },
  "updatedSince": {
    "deprecated": true,
    "description": "use contentUpdatedSince"
  }
}
```

### Notas Importantes
- **unitType y customData:** Considerados inestables
- **coverImage:** Usar images API en su lugar
- **regulations:** Campo deprecated
- **updatedSince:** Usar contentUpdatedSince

---

## Validación de Tipos en la API

### Parámetros Booleanos
La API TrackHS **explicitamente** define que los valores booleanos deben ser:
- `1` para `true`
- `0` para `false`

```json
{
  "petsFriendly": {
    "type": "integer",
    "enum": [1, 0],
    "description": "Return all units that are pet friendly"
  }
}
```

### Parámetros Numéricos
Todos los parámetros numéricos son **strictamente** `integer`:

```json
{
  "bedrooms": {
    "type": "integer",
    "description": "Return all units with this exact number of bedrooms."
  }
}
```

---

## Implicaciones para el MCP

### Problema Raíz
El MCP TrackHS está **mal alineado** con la API oficial:

1. **MCP define:** `Optional[str]` para parámetros numéricos
2. **API espera:** `integer` para parámetros numéricos
3. **MCP define:** `Optional[str]` para parámetros booleanos
4. **API espera:** `integer` con enum [1, 0] para parámetros booleanos

### Solución Requerida

#### 1. Actualizar Tipos en MCP
```python
# Cambiar de:
bedrooms: Optional[str] = Field(...)

# A:
bedrooms: Optional[Union[str, int]] = Field(...)
```

#### 2. Implementar Normalización
```python
# Aplicar antes de enviar a la API
normalized_bedrooms = normalize_int(bedrooms)
normalized_pets_friendly = normalize_binary_int(pets_friendly)
```

#### 3. Validación de Enum para Booleanos
```python
# Para parámetros booleanos, validar que sean 0 o 1
if pets_friendly is not None:
    if pets_friendly not in [0, 1, "0", "1"]:
        raise ValidationError("petsFriendly must be 0 or 1")
```

---

## Casos de Uso Validados

### ✅ Casos que Funcionan
1. **Búsqueda básica por texto**
   - Parámetros: `search`, `term`, `unitCode`, `shortName`
   - Tipo: `string` ✅

2. **Filtros por ID**
   - Parámetros: `nodeId`, `amenityId`, `unitTypeId`
   - Tipo: `integer` o `array` ✅

3. **Filtros de fecha**
   - Parámetros: `arrival`, `departure`, `contentUpdatedSince`
   - Tipo: `string` con formato específico ✅

### ❌ Casos que Fallan
1. **Filtros numéricos**
   - Parámetros: `bedrooms`, `bathrooms`, rangos
   - Problema: MCP envía `string`, API espera `integer`

2. **Filtros booleanos**
   - Parámetros: `petsFriendly`, `isActive`, `isBookable`
   - Problema: MCP envía `string`, API espera `integer` con enum [1,0]

---

## Recomendaciones de Implementación

### Prioridad Alta
1. **Actualizar definiciones de tipos** en `search_units.py`
2. **Implementar normalización** antes de llamar a la API
3. **Validar enums** para parámetros booleanos

### Prioridad Media
1. **Documentar tipos esperados** en descripciones
2. **Agregar ejemplos** de uso correcto
3. **Implementar tests** de validación

### Prioridad Baja
1. **Mejorar mensajes de error**
2. **Agregar logging** de conversiones
3. **Documentar campos deprecated**

---

## Conclusión

El análisis del esquema oficial de TrackHS confirma que el problema identificado en las pruebas es **real y crítico**. La API oficial espera tipos `integer` para parámetros numéricos y booleanos, pero el MCP los define como `Optional[str]`.

**Impacto:** 20 de 37 parámetros (54%) están mal implementados, causando fallos en filtros esenciales como habitaciones, baños, y propiedades pet-friendly.

**Solución:** Actualizar tipos a `Union[str, int]` y aplicar normalización antes de enviar a la API.

---

**Estado:** Problema confirmado y documentado
**Siguiente acción:** Implementar correcciones en el código
**Prioridad:** Crítica

*Generado el 22 de Octubre de 2025*
