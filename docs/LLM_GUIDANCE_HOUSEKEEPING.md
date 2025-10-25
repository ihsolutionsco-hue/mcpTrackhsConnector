# 🤖 Guía para LLMs: create_housekeeping_work_order

## 📋 RESUMEN EJECUTIVO

**Tool**: `create_housekeeping_work_order`
**Propósito**: Crear órdenes de trabajo de housekeeping en TrackHS
**Audiencia**: LLMs, Agentes de IA, Sistemas de automatización

## ⚠️ REGLAS CRÍTICAS PARA LLMs

### **1. TIPOS DE DATOS OBLIGATORIOS**

| Parámetro | Tipo Correcto | ❌ Incorrecto | ✅ Correcto |
|-----------|---------------|---------------|-------------|
| `unit_id` | `int` | `"123"` | `123` |
| `user_id` | `int` | `"789"` | `789` |
| `vendor_id` | `int` | `"321"` | `321` |
| `reservation_id` | `int` | `"987654"` | `987654` |
| `clean_type_id` | `int` | `"5"` | `5` |
| `is_inspection` | `bool` | `"true"` | `true` |
| `is_turn` | `bool` | `"false"` | `false` |
| `charge_owner` | `bool` | `"true"` | `true` |
| `cost` | `float` | `"125.50"` | `125.50` |

### **2. EJEMPLOS DE USO CORRECTO**

#### ✅ **Limpieza Estándar**
```python
create_housekeeping_work_order(
    scheduled_at="2024-01-16T12:00:00Z",
    status="pending",
    unit_id=123,  # ✅ Integer
    is_inspection=false,  # ✅ Boolean
    clean_type_id=5  # ✅ Integer
)
```

#### ✅ **Inspección**
```python
create_housekeeping_work_order(
    scheduled_at="2024-01-16T14:30:00Z",
    status="pending",
    unit_id=456,  # ✅ Integer
    is_inspection=true,  # ✅ Boolean
    user_id=789  # ✅ Integer
)
```

#### ✅ **Limpieza con Costo**
```python
create_housekeeping_work_order(
    scheduled_at="2024-01-16T10:00:00Z",
    status="pending",
    unit_id=789,  # ✅ Integer
    clean_type_id=3,  # ✅ Integer
    cost=125.50,  # ✅ Float
    comments="Limpieza profunda post-evento"
)
```

### **3. EJEMPLOS DE USO INCORRECTO**

#### ❌ **Strings en lugar de Integers**
```python
# ❌ INCORRECTO - Causa error
create_housekeeping_work_order(
    unit_id="123",  # ❌ String
    user_id="789",  # ❌ String
    clean_type_id="5"  # ❌ String
)
```

#### ❌ **Strings en lugar de Booleans**
```python
# ❌ INCORRECTO - Causa error
create_housekeeping_work_order(
    is_inspection="true",  # ❌ String
    is_turn="false",  # ❌ String
    charge_owner="true"  # ❌ String
)
```

#### ❌ **Strings en lugar de Floats**
```python
# ❌ INCORRECTO - Causa error
create_housekeeping_work_order(
    cost="125.50"  # ❌ String
)
```

## 🎯 CASOS DE USO COMUNES

### **📞 Escenario 1: Limpieza de Check-out**
```python
# Cliente: "El huésped se va mañana, necesito programar la limpieza"
create_housekeeping_work_order(
    scheduled_at="2024-01-16T12:00:00Z",
    status="pending",
    unit_id=123,
    clean_type_id=3,  # Departure Clean
    comments="Limpieza post check-out"
)
```

### **📞 Escenario 2: Inspección de Calidad**
```python
# Cliente: "El cliente se quejó de la limpieza, necesito una inspección"
create_housekeeping_work_order(
    scheduled_at="2024-01-16T14:30:00Z",
    status="pending",
    unit_id=456,
    is_inspection=true,
    user_id=789
)
```

### **📞 Escenario 3: Limpieza Adicional**
```python
# Cliente: "El huésped pidió limpieza adicional durante su estancia"
create_housekeeping_work_order(
    scheduled_at="2024-01-16T09:00:00Z",
    status="pending",
    unit_id=321,
    clean_type_id=4,  # Guest Request
    reservation_id=987654,
    cost=50.00
)
```

### **📞 Escenario 4: Limpieza Post-Evento**
```python
# Cliente: "Hubo un evento, necesito limpieza especial"
create_housekeeping_work_order(
    scheduled_at="2024-01-16T08:00:00Z",
    status="pending",
    unit_id=555,
    clean_type_id=2,  # Deep Clean
    cost=200.00,
    comments="Limpieza profunda post-evento de boda"
)
```

## 🔧 RESTRICCIONES ESPECIALES

### **⚠️ Unidad 1 - Restricción Crítica**
```python
# ❌ INCORRECTO - Causa error 500 del servidor
create_housekeeping_work_order(
    unit_id=1,
    is_inspection=true  # ❌ Unidad 1 no permite inspecciones
)

# ✅ CORRECTO - Usar clean_type_id
create_housekeeping_work_order(
    unit_id=1,
    clean_type_id=6  # ✅ Pre-Arrival Inspection
)
```

### **📋 Clean Types Disponibles**
- `1` = Carpet Cleaning
- `2` = Deep Clean
- `3` = Departure Clean
- `4` = Guest Request
- `5` = Pack and Play
- `6` = Pre-Arrival Inspection
- `7` = Refresh Clean

## 🚨 MENSAJES DE ERROR COMUNES

### **Error de Tipo de Datos**
```
❌ Error: Parameter 'unit_id' must be one of types [integer, null], got string
🔧 Solución: Use unit_id=123 (integer), no unit_id="123" (string)
```

### **Error de Validación**
```
❌ Error: unit_id debe ser un entero positivo
🔧 Solución: Asegúrese de que unit_id sea un número entero positivo
```

### **Error de Restricción Unidad 1**
```
❌ Error: La unidad 1 no permite inspecciones (is_inspection=true)
🔧 Solución: Use clean_type_id en lugar de is_inspection para la unidad 1
```

## 📝 CHECKLIST PARA LLMs

### **Antes de llamar al tool:**
- [ ] ¿Todos los IDs son integers? (no strings)
- [ ] ¿Los booleanos son true/false? (no "true"/"false")
- [ ] ¿Las fechas están en formato ISO 8601?
- [ ] ¿Si es unidad 1, uso clean_type_id en lugar de is_inspection?
- [ ] ¿Al menos uno de is_inspection o clean_type_id está presente?
- [ ] ¿No estoy usando ambos is_inspection y clean_type_id?

### **Después de llamar al tool:**
- [ ] ¿El resultado fue exitoso?
- [ ] ¿Necesito informar al cliente sobre el costo?
- [ ] ¿Necesito coordinar con housekeeping?
- [ ] ¿Hay restricciones especiales que mencionar?

## 🎓 MEJORES PRÁCTICAS

### **1. Siempre validar tipos antes de llamar**
```python
# ✅ Verificar que los IDs sean integers
if isinstance(unit_id, str):
    unit_id = int(unit_id)
```

### **2. Usar clean_type_id para unidad 1**
```python
# ✅ Detectar unidad 1 y usar clean_type_id
if unit_id == 1:
    clean_type_id = 6  # Pre-Arrival Inspection
    is_inspection = None
```

### **3. Proporcionar comentarios descriptivos**
```python
# ✅ Comentarios útiles para housekeeping
comments = "Limpieza profunda post-evento de boda - atención especial a salón principal"
```

### **4. Validar fechas ISO 8601**
```python
# ✅ Formato correcto
scheduled_at = "2024-01-16T12:00:00Z"  # ✅ Correcto
scheduled_at = "2024-01-16 12:00:00"   # ✅ También correcto
scheduled_at = "16-01-2024"            # ❌ Incorrecto
```

## 📚 REFERENCIAS

- **Tool**: `create_housekeeping_work_order`
- **API**: TrackHS Housekeeping Work Orders
- **Formato de fechas**: ISO 8601
- **Restricciones**: Unidad 1 no permite inspecciones
- **Clean Types**: 7 tipos disponibles (1-7)

---

**Última actualización**: 2025-10-25
**Versión**: 1.0
**Estado**: Activo y en producción
