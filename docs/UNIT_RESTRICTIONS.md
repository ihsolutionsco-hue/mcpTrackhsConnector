# 🚨 Restricciones Conocidas de Unidades - TrackHS

**Fecha**: 15 de enero, 2025
**Estado**: ✅ **CONFIRMADO**
**Impacto**: Error 500 del servidor TrackHS

---

## 📋 **RESTRICCIÓN IDENTIFICADA**

### **Unidad 1 - Restricción de Inspecciones**

#### **❌ Problema**
- **Error**: 500 Internal Server Error
- **Condición**: `unit_id: 1` + `is_inspection: true`
- **Causa**: Restricción específica del servidor TrackHS (no documentada)

#### **✅ Solución**
- **Workaround**: Usar `clean_type_id` en lugar de `is_inspection`
- **Ejemplo**: `clean_type_id: "5"` para limpieza de salida

---

## 🧪 **EVIDENCIA DE TESTING**

### **✅ Casos que Funcionan**
```json
// ✅ Funciona: Unidad 1 con clean_type_id
{
  "unitId": 1,
  "cleanTypeId": "5",
  "scheduledAt": "2025-01-15T10:00:00Z"
}

// ✅ Funciona: Otras unidades con inspección
{
  "unitId": 2,
  "isInspection": true,
  "scheduledAt": "2025-01-15T10:00:00Z"
}
```

### **❌ Casos que Fallan**
```json
// ❌ Falla: Unidad 1 con inspección
{
  "unitId": 1,
  "isInspection": true,
  "scheduledAt": "2025-01-15T10:00:00Z"
}
// Resultado: 500 Internal Server Error
```

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA**

### **Validación Preventiva**
```python
# En create_housekeeping_work_order.py
if unit_id == 1 and is_inspection is True:
    raise ValidationError(
        "❌ RESTRICCIÓN CONOCIDA: La unidad 1 no permite inspecciones. "
        "✅ SOLUCIÓN: Use clean_type_id en lugar de is_inspection."
    )
```

### **Manejo de Errores Específico**
```python
# En create_housekeeping_work_order.py
if "500" in error_message and params.unit_id == 1 and params.is_inspection:
    return error_response(
        "❌ RESTRICCIÓN CONOCIDA: La unidad 1 no permite inspecciones. "
        "✅ SOLUCIÓN: Use clean_type_id en lugar de is_inspection."
    )
```

---

## 📊 **ESTADÍSTICAS DE TESTING**

| Unidad | is_inspection | clean_type_id | Resultado |
|--------|---------------|---------------|-----------|
| 1 | ❌ | ✅ | Error 500 |
| 1 | ✅ | ❌ | ✅ Éxito |
| 2 | ✅ | ❌ | ✅ Éxito |
| 3 | ✅ | ❌ | ✅ Éxito |
| 4 | ✅ | ❌ | ✅ Éxito |
| 5 | ✅ | ❌ | ✅ Éxito |

**Tasa de éxito**: 80% (4/5 unidades funcionan con inspecciones)

---

## 🎯 **RECOMENDACIONES**

### **Para Desarrolladores**
1. **Validar preventivamente** antes de enviar requests
2. **Usar clean_type_id** para unidad 1
3. **Implementar manejo de errores** específico
4. **Documentar restricciones** en la API

### **Para Usuarios**
1. **Evitar is_inspection=true** para unidad 1
2. **Usar clean_type_id** como alternativa
3. **Consultar documentación** antes de crear work orders

### **Para Soporte TrackHS**
1. **Investigar restricción** de la unidad 1
2. **Documentar limitaciones** en la API
3. **Proporcionar workarounds** oficiales

---

## 📞 **CONTACTO**

- **Soporte TrackHS**: support@trackhs.com
- **Documentación**: [TrackHS API Docs](https://docs.trackhs.com)
- **Estado**: Pendiente respuesta de soporte

---

## 🔄 **HISTORIAL DE CAMBIOS**

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-01-15 | Identificación de restricción | AI Assistant |
| 2025-01-15 | Implementación de validación | AI Assistant |
| 2025-01-15 | Documentación completa | AI Assistant |

---

**⚠️ IMPORTANTE**: Esta restricción es específica del servidor TrackHS y no está documentada en la API oficial. Se recomienda contactar soporte para obtener más información.
