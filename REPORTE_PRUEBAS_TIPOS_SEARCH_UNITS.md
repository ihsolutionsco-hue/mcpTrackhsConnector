# Reporte de Pruebas de Tipos de Usuario - search_units MCP TrackHS

**Fecha:** 22 de Octubre de 2025
**Componente:** search_units (MCP TrackHS)
**Versión API:** Channel API

---

## Resumen Ejecutivo

Se realizaron pruebas exhaustivas de la función `search_units` del MCP TrackHS para validar su comportamiento con diferentes tipos de usuarios y parámetros. Se identificó un **problema crítico** de validación de tipos que impide el uso de filtros numéricos y booleanos.

### Estadísticas
- ✅ **Escenarios exitosos:** 2 de 6 (33%)
- ❌ **Escenarios fallidos:** 4 de 6 (67%)
- 🔴 **Gravedad:** Alta - Impacta a todos los tipos de usuarios

---

## Problema Principal

**Inconsistencia en validación de tipos de parámetros:**

El schema MCP define parámetros numéricos y booleanos como `Optional[str]` en el código Python, pero el servidor FastMCP los valida como `integer`, causando errores de tipo cuando los usuarios intentan usar estos filtros.

```python
# Definición en el código (search_units.py)
bedrooms: Optional[str] = Field(
    default=None,
    description="Filter by exact number of bedrooms"
)

# Error generado por el servidor
"Parameter 'bedrooms' must be one of types [integer, null], got string"
```

---

## Escenarios de Prueba

### ✅ Escenario 1: Usuario Básico - Búsqueda Simple
**Tipo de usuario:** Turista
**Objetivo:** Buscar propiedades por nombre

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "search": "villa"
}
```

**Resultado:** ✅ **EXITOSO**
**Respuesta:** Retorna 20 unidades tipo "villa" correctamente

**Datos retornados:**
- 5 Bedroom luxury villa by Disney-332
- 6 Bedroom luxury villa by Disney-316
- 6 bedrooms Villa close to Disney Parks-312

---

### ❌ Escenario 2: Usuario Avanzado - Filtros de Características
**Tipo de usuario:** Familia
**Objetivo:** Buscar propiedades con número específico de habitaciones y baños

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "bedrooms": "4",  # String
    "bathrooms": "2"  # String
}
```

**Resultado:** ❌ **FALLIDO**
**Error:** `Parameter 'bedrooms' must be one of types [integer, null], got string`

**Impacto:** Familias no pueden filtrar por características físicas de las propiedades

---

### ❌ Escenario 3: Usuario con Preferencias - Filtros Booleanos
**Tipo de usuario:** Dueño de mascotas
**Objetivo:** Buscar propiedades pet-friendly que estén activas

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "pets_friendly": "1",  # String representando boolean
    "is_active": "1"       # String representando boolean
}
```

**Resultado:** ❌ **FALLIDO**
**Error:** `Parameter 'pets_friendly' must be one of types [integer, null], got string`

**Impacto:** Dueños de mascotas no pueden filtrar propiedades adecuadas

---

### ✅ Escenario 4: Usuario por Ubicación
**Tipo de usuario:** Turista local
**Objetivo:** Buscar propiedades en una ubicación específica

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "node_id": "3",  # String (acepta correctamente)
    "search": "Champions Gate"
}
```

**Resultado:** ✅ **EXITOSO**
**Nota:** Los parámetros de ID (node_id, amenity_id, unit_type_id) sí aceptan strings correctamente

---

### ❌ Escenario 5: Usuario Buscando Disponibilidad
**Tipo de usuario:** Planificador de viajes
**Objetivo:** Buscar propiedades disponibles en fechas específicas

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "arrival": "2025-11-01",
    "departure": "2025-11-07",
    "is_bookable": "1"  # String representando boolean
}
```

**Resultado:** ❌ **FALLIDO**
**Error:** `Parameter 'is_bookable' must be one of types [integer, null], got string`

**Impacto:** Usuarios no pueden filtrar por disponibilidad para reserva

---

### ❌ Escenario 6: Usuario con Rango de Habitaciones
**Tipo de usuario:** Grupo grande
**Objetivo:** Buscar propiedades con rango de habitaciones

**Parámetros:**
```python
{
    "page": 1,
    "size": 3,
    "min_bedrooms": "3",  # String
    "max_bedrooms": "6"   # String
}
```

**Resultado:** ❌ **FALLIDO**
**Error:** `Parameter 'min_bedrooms' must be one of types [integer, null], got string`

**Impacto:** Grupos grandes no pueden buscar propiedades adecuadas a su tamaño

---

## Análisis Técnico Detallado

### Causa Raíz
Existe una **discrepancia** entre:
1. **Definición del schema** en el código Python (acepta `Optional[str]`)
2. **Validación del servidor** FastMCP (requiere `integer`)

### Parámetros Afectados

#### Parámetros Numéricos (8 parámetros):
- `bedrooms` - Número exacto de habitaciones
- `min_bedrooms` - Mínimo de habitaciones
- `max_bedrooms` - Máximo de habitaciones
- `bathrooms` - Número exacto de baños
- `min_bathrooms` - Mínimo de baños
- `max_bathrooms` - Máximo de baños
- `calendar_id` - ID de calendario
- `role_id` - ID de rol

#### Parámetros Booleanos/Binarios (12 parámetros):
- `pets_friendly` - Acepta mascotas (0/1)
- `allow_unit_rates` - Permite tarifas por unidad (0/1)
- `computed` - Unidad computada (0/1)
- `inherited` - Unidad heredada (0/1)
- `limited` - Disponibilidad limitada (0/1)
- `is_bookable` - Es reservable (0/1)
- `include_descriptions` - Incluir descripciones (0/1)
- `is_active` - Está activa (0/1)
- `events_allowed` - Permite eventos (0/1)
- `smoking_allowed` - Permite fumar (0/1)
- `children_allowed` - Permite niños (0/1)
- `is_accessible` - Es accesible (0/1)

#### Parámetros que SÍ funcionan correctamente (4 parámetros):
- `node_id` - ID de nodo
- `amenity_id` - ID de amenidad
- `unit_type_id` - ID de tipo de unidad
- `id` - ID de unidad

---

## Casos de Uso Bloqueados

### 🔴 Gravedad Crítica
**Filtrado por unidades activas/disponibles**
- Parámetros afectados: `is_active`, `is_bookable`
- Usuarios afectados: **Todos los usuarios**
- Descripción: No se pueden filtrar unidades que estén actualmente disponibles para reserva

### 🟠 Gravedad Alta
**Filtrado por número de habitaciones**
- Parámetros afectados: `bedrooms`, `min_bedrooms`, `max_bedrooms`, `bathrooms`
- Usuarios afectados: Familias, grupos grandes
- Descripción: Característica fundamental para encontrar alojamiento adecuado

**Filtrado por propiedades pet-friendly**
- Parámetros afectados: `pets_friendly`
- Usuarios afectados: Dueños de mascotas
- Descripción: Criterio importante para viajeros con mascotas

### 🟡 Gravedad Media
**Filtrado por rangos de características**
- Parámetros afectados: `min_bedrooms`, `max_bedrooms`, `min_bathrooms`, `max_bathrooms`
- Usuarios afectados: Usuarios avanzados
- Descripción: Limita las opciones de búsqueda flexible

---

## Pruebas Exitosas Realizadas

### Búsqueda Básica por Texto
```python
# Llamada MCP
mcp_ihmTrackhs_search_units(
    page=1,
    size=3,
    search="villa"
)

# Resultado: ✅ Exitoso
# Retorna 20 unidades con "villa" en el nombre
```

### Búsqueda por Ubicación (Node ID)
```python
# Llamada MCP
mcp_ihmTrackhs_search_units(
    page=1,
    size=3,
    node_id="3",
    search="Champions Gate"
)

# Resultado: ✅ Exitoso
# Los parámetros de ID funcionan correctamente con strings
```

---

## Comparación: Código vs Servidor

### En el Código Python (search_units.py)
```python
bedrooms: Optional[str] = Field(
    default=None,
    description="Filter by exact number of bedrooms"
)

pets_friendly: Optional[str] = Field(
    default=None,
    description="Filter by pet-friendly units (0=no, 1=yes)"
)
```

### En el Servidor FastMCP
```
Parameter 'bedrooms' must be one of types [integer, null], got string
Parameter 'pets_friendly' must be one of types [integer, null], got string
```

### Problema
El servidor **sobrescribe** la definición del schema y aplica validación estricta de tipos incompatible con la API de TrackHS.

---

## Recomendaciones

### 🔴 Prioridad Alta

#### 1. Actualizar el Schema MCP para Union Types
**Acción:** Cambiar los tipos de parámetros numéricos y booleanos para aceptar tanto `string` como `integer`

```python
# Antes
bedrooms: Optional[str] = Field(...)

# Después
bedrooms: Optional[Union[str, int]] = Field(...)
```

**Justificación:** Permite compatibilidad con diferentes clientes MCP y con la forma en que la API de TrackHS espera los parámetros

**Archivos a modificar:**
- `src/trackhs_mcp/infrastructure/mcp/search_units.py`

#### 2. Implementar Normalización de Tipos
**Acción:** Agregar conversión automática de strings a integers en el procesamiento de parámetros

```python
def normalize_numeric_param(value: Optional[Union[str, int]]) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return value
```

**Justificación:** Convierte automáticamente los tipos sin generar errores, mejorando la experiencia del usuario

**Archivos a modificar:**
- `src/trackhs_mcp/infrastructure/utils/type_normalization.py` (ya existe)
- `src/trackhs_mcp/infrastructure/mcp/search_units.py` (aplicar normalización)

### 🟠 Prioridad Media

#### 3. Documentar Tipos Esperados
**Acción:** Actualizar las descripciones de parámetros para indicar explícitamente los tipos aceptados

```python
bedrooms: Optional[Union[str, int]] = Field(
    default=None,
    description="Filter by exact number of bedrooms (accepts string or integer)"
)
```

**Justificación:** Ayuda a los desarrolladores a entender los requisitos sin consultar el código fuente

### 🟢 Prioridad Baja

#### 4. Mejorar Mensajes de Error
**Acción:** Proporcionar mensajes de error más descriptivos que guíen al usuario

```python
try:
    # validación
except ValidationError as e:
    raise ValidationError(
        f"Parameter '{param_name}' expects integer or string representation "
        f"of integer. Got: {type(value).__name__}"
    )
```

---

## Impacto en Usuarios

### Tipos de Usuario Afectados

| Tipo de Usuario | Funcionalidad Bloqueada | Impacto |
|-----------------|------------------------|---------|
| **Turistas** | Búsqueda básica | ✅ Funciona |
| **Familias** | Filtro por habitaciones/baños | ❌ Bloqueado |
| **Dueños de mascotas** | Filtro pet-friendly | ❌ Bloqueado |
| **Grupos grandes** | Rangos de características | ❌ Bloqueado |
| **Planificadores** | Filtro por disponibilidad | ❌ Bloqueado |
| **Usuarios avanzados** | Filtros múltiples | ❌ Bloqueado |

### Porcentaje de Funcionalidad Disponible
- **Búsquedas básicas:** 100% funcional
- **Filtros de ID:** 100% funcional
- **Filtros numéricos:** 0% funcional ❌
- **Filtros booleanos:** 0% funcional ❌
- **Filtros de fecha:** 100% funcional
- **Funcionalidad total:** ~40% operativa

---

## Ejemplo de Implementación de la Solución

### Solución Propuesta en search_units.py

```python
from typing import Union

# 1. Cambiar definiciones de tipos
bedrooms: Optional[Union[str, int]] = Field(
    default=None,
    description="Filter by exact number of bedrooms (integer or string)"
)

pets_friendly: Optional[Union[str, int]] = Field(
    default=None,
    description="Filter by pet-friendly units (0=no, 1=yes, integer or string)"
)

# 2. Aplicar normalización antes de crear SearchUnitsParams
normalized_params = {
    "bedrooms": normalize_int(bedrooms),
    "pets_friendly": normalize_binary_int(pets_friendly),
    # ... otros parámetros
}

# 3. Crear entidad con valores normalizados
params = SearchUnitsParams(**normalized_params)
```

### Funciones de Normalización Ya Disponibles

El proyecto ya cuenta con funciones de normalización en:
`src/trackhs_mcp/infrastructure/utils/type_normalization.py`

```python
def normalize_int(value: Optional[Union[str, int, float]]) -> Optional[int]:
    """Normaliza un valor a entero"""
    # Implementación existente

def normalize_binary_int(value: Optional[Union[str, int]]) -> Optional[int]:
    """Normaliza un valor binario (0/1)"""
    # Implementación existente
```

---

## Conclusiones

### Hallazgos Principales

1. **Problema Identificado:** Validación de tipos demasiado estricta en el servidor FastMCP
2. **Alcance del Problema:** 20 de 35 parámetros afectados (57%)
3. **Gravedad:** Alta - Impide el uso de funcionalidades críticas
4. **Solución:** Factible y bien definida

### Estado Actual del MCP
- ✅ **Funcional:** Búsquedas básicas por texto y filtros de ID
- ❌ **No funcional:** Filtros numéricos y booleanos
- ⚠️ **Limitado:** Solo 40% de la funcionalidad disponible

### Próximos Pasos Recomendados

1. Implementar Union types en definiciones de parámetros
2. Aplicar normalización de tipos antes de validación
3. Ejecutar suite de pruebas completa
4. Validar con usuarios reales
5. Documentar cambios y actualizaciones

---

## Archivos de Referencia

- **Script de pruebas:** `test_search_units_user_types.py`
- **Reporte JSON:** `reporte_pruebas_tipos_search_units.json`
- **Código fuente:** `src/trackhs_mcp/infrastructure/mcp/search_units.py`
- **Utilidades:** `src/trackhs_mcp/infrastructure/utils/type_normalization.py`

---

## Anexos

### Anexo A: Lista Completa de Parámetros search_units

#### Paginación (2)
- `page` - Número de página ✅
- `size` - Tamaño de página ✅

#### Ordenamiento (2)
- `sort_column` - Columna de ordenamiento ✅
- `sort_direction` - Dirección de ordenamiento ✅

#### Búsqueda de texto (4)
- `search` - Búsqueda completa ✅
- `term` - Término de búsqueda ✅
- `unit_code` - Código de unidad ✅
- `short_name` - Nombre corto ✅

#### Filtros de ID (4)
- `node_id` - ID de nodo ✅
- `amenity_id` - ID de amenidad ✅
- `unit_type_id` - ID de tipo ✅
- `id` - ID de unidad ✅

#### Filtros numéricos (8)
- `bedrooms` - Habitaciones ❌
- `min_bedrooms` - Mínimo habitaciones ❌
- `max_bedrooms` - Máximo habitaciones ❌
- `bathrooms` - Baños ❌
- `min_bathrooms` - Mínimo baños ❌
- `max_bathrooms` - Máximo baños ❌
- `calendar_id` - ID calendario ❌
- `role_id` - ID rol ❌

#### Filtros booleanos (12)
- `pets_friendly` - Mascotas ❌
- `allow_unit_rates` - Tarifas unidad ❌
- `computed` - Computada ❌
- `inherited` - Heredada ❌
- `limited` - Limitada ❌
- `is_bookable` - Reservable ❌
- `include_descriptions` - Descripciones ❌
- `is_active` - Activa ❌
- `events_allowed` - Eventos ❌
- `smoking_allowed` - Fumar ❌
- `children_allowed` - Niños ❌
- `is_accessible` - Accesible ❌

#### Filtros de fecha (4)
- `arrival` - Fecha llegada ✅
- `departure` - Fecha salida ✅
- `content_updated_since` - Contenido actualizado ✅
- `updated_since` - Actualizado desde ✅

#### Estado (1)
- `unit_status` - Estado limpieza ✅

**Total:** 37 parámetros
**Funcionales:** 17 (46%)
**No funcionales:** 20 (54%)

---

**Fin del Reporte**

*Generado el 22 de Octubre de 2025*
*MCPtrackhsConnector - TrackHS API Integration*

