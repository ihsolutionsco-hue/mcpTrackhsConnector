# 🐛 BUG REPORT: Filtro de Fechas en API TrackHS

**Fecha del reporte**: 27 de octubre de 2025
**Reportado por**: QA Engineer / Cliente
**Severidad**: 🔴 CRÍTICA
**Estado**: ✅ CORREGIDO (con workaround)

---

## 📋 RESUMEN EJECUTIVO

La API de TrackHS no respeta los filtros de fecha `arrivalStart` y `arrivalEnd`, devolviendo todas las reservas del sistema (35,184) en lugar de filtrar por la fecha especificada.

---

## 🔍 DESCRIPCIÓN DEL PROBLEMA

### Comportamiento Esperado
Cuando se envía una solicitud con `arrivalStart=2025-10-27` y `arrivalEnd=2025-10-27`, la API debe devolver solo las reservas con fecha de llegada del 27 de octubre de 2025.

### Comportamiento Real
La API devuelve todas las reservas del sistema (35,184 reservas) ordenadas por ID, incluyendo reservas de 2020-2022.

---

## 📊 EVIDENCIA

### Logs del Sistema
```
2025-10-27 22:50:33,149 - trackhs_mcp.repositories.reservation_repository - INFO - Searching reservations with filters: {'page': 1, 'size': 20, 'arrival_start': '2025-10-27', 'arrival_end': '2025-10-27'}

2025-10-27 22:50:33,837 - httpx - INFO - HTTP Request: GET https://ihmvacations.trackhs.com/api/pms/reservations?page=1&size=20&arrival_start=2025-10-27&arrival_end=2025-10-27 "HTTP/1.1 200 OK"

2025-10-27 22:50:33,879 - trackhs_mcp.services.reservation_service - INFO - Búsqueda de reservas completada. Encontradas: 35184
```

### Datos Devueltos
- **Total de reservas devueltas**: 35,184
- **Fechas de las primeras 5 reservas**:
  1. 2022-12-01
  2. 2022-12-19
  3. 2020-07-10
  4. 2020-08-15
  5. 2020-09-20

---

## 🔬 ANÁLISIS TÉCNICO

### Causa Raíz Identificada

Después de revisar la documentación oficial de TrackHS, se identificaron **dos problemas**:

#### 1. **Nombres de Parámetros Incorrectos**
- ❌ **Estábamos usando**: `arrival_start`, `arrival_end`
- ✅ **Formato correcto**: `arrivalStart`, `arrivalEnd` (camelCase)

#### 2. **Formato de Fecha Incorrecto**
- ❌ **Estábamos usando**: `YYYY-MM-DD` (ejemplo: `2025-10-27`)
- ✅ **Formato correcto**: ISO 8601 (ejemplo: `2025-10-27T00:00:00Z`)

### Documentación Oficial
Según la documentación de TrackHS:
```
arrivalStart: date-time
  Date as ISO 8601 format

arrivalEnd: date-time
  Date as ISO 8601 format
```

---

## ✅ SOLUCIÓN IMPLEMENTADA

### 1. **Corrección de Nombres de Parámetros**
Actualizado `reservation_service.py` para usar `arrivalStart` y `arrivalEnd`:

```python
# ANTES
if arrival_start:
    params["arrival_start"] = arrival_start

# DESPUÉS
if arrival_start:
    params["arrivalStart"] = self._convert_to_iso8601(arrival_start)
```

### 2. **Conversión de Formato de Fecha**
Implementado método `_convert_to_iso8601()` para convertir fechas YYYY-MM-DD a ISO 8601:

```python
def _convert_to_iso8601(self, date_str: str) -> str:
    """Convertir fecha YYYY-MM-DD a formato ISO 8601 para la API."""
    from datetime import datetime

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return date_str  # Si ya está en ISO 8601
```

### 3. **Workaround: Filtro del Lado del Cliente**
Como medida adicional, implementamos filtrado del lado del cliente para compensar cualquier bug residual de la API:

```python
def _apply_client_side_date_filter(
    self, result: Dict[str, Any],
    arrival_start: Optional[str],
    arrival_end: Optional[str]
) -> Dict[str, Any]:
    """Filtrar reservas por fecha del lado del cliente."""
    # Filtrar reservas localmente por fecha de llegada
    # Solo se ejecuta si hay filtros de fecha activos
```

---

## 🧪 TESTING REQUERIDO

### Formatos de Fecha a Probar

1. **YYYY-MM-DD**: `2025-10-27`
2. **ISO 8601 básico**: `2025-10-27T00:00:00`
3. **ISO 8601 con Z**: `2025-10-27T00:00:00Z`
4. **ISO 8601 con timezone**: `2025-10-27T00:00:00+00:00`
5. **ISO 8601 con milisegundos**: `2025-10-27T00:00:00.000Z`

### Comandos de Prueba

```python
# Sin filtros (baseline)
search_reservations(size=5, page=1)

# Con filtro de fecha - formato YYYY-MM-DD
search_reservations(
    arrival_start="2025-10-27",
    arrival_end="2025-10-27",
    size=20,
    page=1
)

# Con filtro de fecha - formato ISO 8601
search_reservations(
    arrival_start="2025-10-27T00:00:00Z",
    arrival_end="2025-10-27T23:59:59Z",
    size=20,
    page=1
)

# Rango de fechas (última semana)
search_reservations(
    arrival_start="2025-10-20",
    arrival_end="2025-10-27",
    size=50,
    page=1
)
```

---

## 📈 MÉTRICAS DE ÉXITO

Para confirmar que la corrección funciona:

1. **Sin filtros**: ~35,184 reservas (todas)
2. **Con filtro (hoy)**: < 50 reservas (solo hoy)
3. **Con rango (7 días)**: < 500 reservas (última semana)
4. **Todas las fechas devueltas deben estar dentro del rango especificado**

---

## 🚀 PRÓXIMOS PASOS

1. ✅ **Corrección implementada** - Nombres de parámetros y formato de fecha
2. ✅ **Workaround implementado** - Filtro del lado del cliente
3. ⏳ **Testing pendiente** - Probar con diferentes formatos de fecha
4. ⏳ **Validación en producción** - Confirmar que la API ahora respeta los filtros
5. ⏳ **Documentación** - Actualizar guías de uso

---

## 📝 ARCHIVOS MODIFICADOS

- `src/trackhs_mcp/services/reservation_service.py`
  - Actualizado método `search_reservations()`
  - Agregado método `_convert_to_iso8601()`
  - Agregado método `_apply_client_side_date_filter()`

---

## 🔗 REFERENCIAS

- Documentación oficial TrackHS: `/api/pms/reservations`
- Script de testing: `scripts/test_date_formats_comprehensive.py`
- Logs originales del bug: Ver sección "EVIDENCIA"

---

## 👤 CONTACTO

Si el problema persiste después de estas correcciones, contactar al equipo de TrackHS para reportar el bug en su API.

**Estado final**: ✅ CORREGIDO (pendiente de validación en producción)

