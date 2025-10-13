# 📋 Guía de Formatos - trackhsMCP

**Para usuarios no técnicos** - Guía rápida de formatos y ejemplos para usar las herramientas de trackhsMCP.

---

## 📅 Formatos de Fecha

### ✅ Formatos Aceptados

| Formato | Ejemplo | Cuándo usar |
|---------|---------|-------------|
| `YYYY-MM-DD` | `2025-01-15` | Solo fecha (más común) |
| `YYYY-MM-DDTHH:MM:SSZ` | `2025-01-15T14:30:00Z` | Fecha y hora completa |
| `YYYY-MM-DDTHH:MM:SS` | `2025-01-15T14:30:00` | Fecha y hora sin zona horaria |

### ❌ Formatos NO Aceptados

- ❌ `15/01/2025` (formato europeo)
- ❌ `01/15/2025` (formato americano)
- ❌ `2025` (solo año)
- ❌ `Enero 15, 2025` (texto)

### 🔧 Ejemplos Prácticos

```bash
# ✅ CORRECTO - Búsqueda de reservaciones en enero 2025
search_reservations_v2(
    arrival_start="2025-01-01",
    arrival_end="2025-01-31"
)

# ✅ CORRECTO - Búsqueda con hora específica
search_reservations_v2(
    arrival_start="2025-01-15T00:00:00Z",
    arrival_end="2025-01-15T23:59:59Z"
)

# ❌ INCORRECTO - Formato inválido
search_reservations_v2(
    arrival_start="2025",  # Solo año
    arrival_end="enero"    # Texto
)
```

---

## 🔢 Tipos de Parámetros

### Números Enteros (Integers)

**Cuándo usar**: Para páginas, tamaños, IDs, habitaciones, baños, etc.

```bash
# ✅ CORRECTO
page=1
size=25
bedrooms=2
bathrooms=1
is_active=1

# ❌ INCORRECTO
page="1"      # String en lugar de número
bedrooms=2.5  # Decimal en lugar de entero
```

### Parámetros Booleanos (0/1)

**Cuándo usar**: Para activar/desactivar filtros

```bash
# ✅ CORRECTO
pets_friendly=1    # Sí permite mascotas
is_active=1        # Sí está activo
smoking_allowed=0  # No permite fumar

# ❌ INCORRECTO
pets_friendly=true   # Usar 1 en lugar de true
is_active="yes"      # Usar 1 en lugar de "yes"
```

### Listas de IDs

**Cuándo usar**: Para buscar múltiples elementos

```bash
# ✅ CORRECTO - Múltiples IDs separados por comas
node_id="1,2,3"
unit_id="10,20,30"

# ✅ CORRECTO - Array en formato string
node_id="[1,2,3]"

# ❌ INCORRECTO
node_id="1 2 3"     # Espacios en lugar de comas
node_id=1,2,3       # Sin comillas
```

---

## 🛠️ Herramientas y Sus Parámetros

### 🔍 search_reservations_v2

**Parámetros principales**:
- `page`: Número de página (empezar en 1)
- `size`: Cantidad de resultados (máximo 1000)
- `arrival_start/end`: Rango de fechas de llegada
- `status`: Estado de reservación (ej: "Confirmed", "Cancelled")

**Ejemplo completo**:
```bash
search_reservations_v2(
    page=1,
    size=10,
    arrival_start="2025-01-01",
    arrival_end="2025-01-31",
    status="Confirmed"
)
```

### 🏠 search_units

**Parámetros principales**:
- `page`: Número de página (empezar en 1)
- `size`: Cantidad de resultados (máximo 1000)
- `bedrooms`: Número exacto de habitaciones
- `is_active`: Solo unidades activas (1) o todas (0)
- `pets_friendly`: Permite mascotas (1) o no (0)

**Ejemplo completo**:
```bash
search_units(
    page=1,
    size=25,
    bedrooms=2,
    bathrooms=1,
    is_active=1,
    pets_friendly=1
)
```

### 📋 get_reservation_v2

**Parámetros**:
- `reservation_id`: ID de la reservación (número entero)

**Ejemplo**:
```bash
get_reservation_v2(reservation_id="37152796")
```

### 💰 get_folio

**Parámetros**:
- `folio_id`: ID del folio (número entero)

**Ejemplo**:
```bash
get_folio(folio_id="37152796")
```

---

## ⚠️ Errores Comunes y Cómo Corregirlos

### Error: "Formato de fecha inválido"

**Problema**: Usaste un formato de fecha incorrecto

**Solución**:
```bash
# ❌ INCORRECTO
arrival_start="15/01/2025"

# ✅ CORRECTO
arrival_start="2025-01-15"
```

### Error: "Parameter 'page' must be one of types [integer, string], got number"

**Problema**: Este error ya está corregido en la versión actual

**Solución**: Usar números directamente:
```bash
# ✅ CORRECTO
page=1
size=25
```

### Error: "Valor inválido para 'bedrooms'"

**Problema**: Usaste un valor no numérico para habitaciones

**Solución**:
```bash
# ❌ INCORRECTO
bedrooms="dos"

# ✅ CORRECTO
bedrooms=2
```

### Error: "reservation_id es requerido"

**Problema**: No proporcionaste el ID de la reservación

**Solución**:
```bash
# ❌ INCORRECTO
get_reservation_v2()

# ✅ CORRECTO
get_reservation_v2(reservation_id="37152796")
```

---

## 🎯 Casos de Uso Comunes

### 1. Buscar Reservaciones del Día

```bash
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status="Confirmed"
)
```

### 2. Buscar Unidades Disponibles

```bash
search_units(
    bedrooms=2,
    bathrooms=1,
    is_active=1,
    is_bookable=1
)
```

### 3. Ver Detalle de Reservación

```bash
get_reservation_v2(reservation_id="37152796")
```

### 4. Ver Estado Financiero

```bash
get_folio(folio_id="37152796")
```

---

## 🆘 Troubleshooting Rápido

| Error | Causa Probable | Solución |
|-------|----------------|----------|
| "Formato de fecha inválido" | Fecha en formato incorrecto | Usar `YYYY-MM-DD` |
| "Valor inválido para 'page'" | Número como string | Usar `page=1` no `page="1"` |
| "reservation_id es requerido" | Falta el ID | Agregar `reservation_id="12345"` |
| "No autorizado" | Credenciales incorrectas | Verificar TRACKHS_USERNAME y TRACKHS_PASSWORD |

---

## 📞 Soporte

Si encuentras errores que no están en esta guía:

1. **Verifica los formatos** usando esta guía
2. **Revisa los ejemplos** de casos de uso comunes
3. **Contacta soporte técnico** con el mensaje de error completo

---

**Última actualización**: 13 de Octubre, 2025
**Versión**: 1.0
