# 🎯 Ejemplos de Queries Comunes - trackhsMCP

**Casos de uso reales** para las herramientas de trackhsMCP con ejemplos prácticos.

---

## 📅 Gestión de Llegadas del Día

### Buscar Reservaciones que Llegan Hoy

```bash
# Buscar todas las llegadas del 15 de enero de 2025
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status="Confirmed"
)
```

### Buscar Solo Llegadas Confirmadas

```bash
# Filtrar por estado específico
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status=["Confirmed", "Checked In"]
)
```

### Ver Detalle de una Llegada Específica

```bash
# Obtener información completa de una reservación
get_reservation_v2(reservation_id="37152796")
```

---

## 🏠 Gestión de Unidades

### Buscar Unidades Disponibles

```bash
# Unidades de 2 habitaciones, 1 baño, activas y reservables
search_units(
    bedrooms=2,
    bathrooms=1,
    is_active=1,
    is_bookable=1
)
```

### Buscar Unidades Pet-Friendly

```bash
# Unidades que permiten mascotas
search_units(
    pets_friendly=1,
    is_active=1
)
```

### Buscar Unidades por Rango de Habitaciones

```bash
# Unidades con 2-4 habitaciones
search_units(
    min_bedrooms=2,
    max_bedrooms=4,
    is_active=1
)
```

---

## 💰 Análisis Financiero

### Ver Estado de Pago de una Reservación

```bash
# Obtener folio para ver balance y pagos
get_folio(folio_id="37152796")
```

### Buscar Reservaciones por Estado de Pago

```bash
# Buscar reservaciones confirmadas en un rango de fechas
search_reservations_v2(
    arrival_start="2025-01-01",
    arrival_end="2025-01-31",
    status="Confirmed"
)
```

---

## 📊 Reportes y Análisis

### Reporte de Ocupación por Fecha

```bash
# Reservaciones confirmadas para una fecha específica
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status="Confirmed"
)
```

### Análisis de Canales de Reservación

```bash
# Buscar reservaciones de un canal específico (usando filtros adicionales)
search_reservations_v2(
    arrival_start="2025-01-01",
    arrival_end="2025-01-31",
    status="Confirmed"
)
# Luego filtrar por canal en los resultados
```

### Unidades por Tipo y Características

```bash
# Unidades con características específicas
search_units(
    bedrooms=3,
    bathrooms=2,
    pets_friendly=1,
    events_allowed=1,
    is_active=1
)
```

---

## 🔍 Búsquedas Avanzadas

### Búsqueda por Múltiples IDs

```bash
# Buscar unidades específicas por ID
search_units(
    id="1,2,3,4,5"
)
```

### Búsqueda por Ubicación

```bash
# Buscar unidades en nodos específicos
search_units(
    node_id="1,2,3",
    is_active=1
)
```

### Búsqueda por Amenidades

```bash
# Buscar unidades con amenidades específicas
search_units(
    amenity_id="1,2,3",
    is_active=1
)
```

---

## ⚠️ Casos de Error y Correcciones

### Error: Fecha Inválida

```bash
# ❌ INCORRECTO
search_reservations_v2(
    arrival_start="15/01/2025"  # Formato incorrecto
)

# ✅ CORRECTO
search_reservations_v2(
    arrival_start="2025-01-15"  # Formato ISO 8601
)
```

### Error: Parámetro Faltante

```bash
# ❌ INCORRECTO
get_reservation_v2()  # Falta reservation_id

# ✅ CORRECTO
get_reservation_v2(reservation_id="37152796")
```

### Error: Tipo de Parámetro Incorrecto

```bash
# ❌ INCORRECTO
search_units(
    bedrooms="dos"  # String en lugar de número
)

# ✅ CORRECTO
search_units(
    bedrooms=2  # Número entero
)
```

---

## 🎯 Flujos de Trabajo Completos

### 1. Check-in de Huésped

```bash
# Paso 1: Buscar reservación por ID
get_reservation_v2(reservation_id="37152796")

# Paso 2: Verificar estado financiero
get_folio(folio_id="37152796")

# Paso 3: Buscar unidad asignada
search_units(
    id="[unidad_id_del_paso_1]",
    is_active=1
)
```

### 2. Gestión de Disponibilidad

```bash
# Paso 1: Ver unidades disponibles
search_units(
    bedrooms=2,
    bathrooms=1,
    is_active=1,
    is_bookable=1
)

# Paso 2: Verificar reservaciones existentes
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-20",
    status="Confirmed"
)
```

### 3. Auditoría Financiera

```bash
# Paso 1: Buscar reservaciones en período
search_reservations_v2(
    arrival_start="2025-01-01",
    arrival_end="2025-01-31",
    status="Confirmed"
)

# Paso 2: Verificar folios de reservaciones específicas
get_folio(folio_id="37152796")
get_folio(folio_id="37152797")
# ... continuar con otras reservaciones
```

---

## 📈 Mejores Prácticas

### 1. Siempre Usar Filtros Apropiados

```bash
# ✅ BUENO - Filtros específicos
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status="Confirmed",
    size=50
)

# ❌ MALO - Sin filtros (puede ser lento)
search_reservations_v2()
```

### 2. Usar Tamaños de Página Apropiados

```bash
# ✅ BUENO - Tamaño moderado
search_reservations_v2(
    page=1,
    size=25
)

# ❌ MALO - Tamaño muy grande (puede ser lento)
search_reservations_v2(
    page=1,
    size=1000
)
```

### 3. Validar IDs Antes de Usar

```bash
# ✅ BUENO - Verificar que el ID existe
get_reservation_v2(reservation_id="37152796")

# ❌ MALO - Usar ID sin verificar
get_reservation_v2(reservation_id="99999999")
```

---

## 🚀 Optimizaciones de Performance

### Búsquedas Eficientes

```bash
# Usar filtros específicos para reducir resultados
search_reservations_v2(
    arrival_start="2025-01-15",
    arrival_end="2025-01-15",
    status="Confirmed",
    size=10
)
```

### Paginación Inteligente

```bash
# Primera página
search_reservations_v2(page=1, size=25)

# Segunda página
search_reservations_v2(page=2, size=25)
```

---

## 📞 Soporte y Troubleshooting

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Formato de fecha inválido" | Fecha incorrecta | Usar `YYYY-MM-DD` |
| "reservation_id es requerido" | ID faltante | Agregar `reservation_id="12345"` |
| "No autorizado" | Credenciales | Verificar TRACKHS_USERNAME/PASSWORD |

### Logs Útiles

```bash
# Verificar que las herramientas están disponibles
# (Esto se hace automáticamente en Claude Desktop)
```

---

**Última actualización**: 13 de Octubre, 2025
**Versión**: 1.0
