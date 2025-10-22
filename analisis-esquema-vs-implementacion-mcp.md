# Análisis: Esquema Oficial TrackHS vs Implementación MCP

**Fecha:** 22 de octubre de 2025
**Objetivo:** Comparar el esquema oficial de TrackHS con la implementación MCP para identificar discrepancias

---

## 🔍 Análisis del Esquema Oficial TrackHS

### Parámetros Booleanos en la API Oficial

Según el esquema oficial (líneas 1085-1086), la documentación establece claramente:

> **"For query parameters, any "boolean" values (true / false), the system will instead take 1 or 0, with 1 == true, and 0 == false."**

### Parámetros Booleanos Definidos en el Esquema

El esquema oficial define los siguientes parámetros booleanos con **enum [1, 0]**:

1. **`petsFriendly`** (líneas 1309-1311)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

2. **`allowUnitRates`** (líneas 1321-1323)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

3. **`computed`** (líneas 1333-1335)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

4. **`inherited`** (líneas 1345-1347)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

5. **`limited`** (líneas 1357-1359)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

6. **`isBookable`** (líneas 1369-1371)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

7. **`includeDescriptions`** (líneas 1381-1383)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

8. **`isActive`** (líneas 1393-1395)
   ```json
   "schema": {
     "type": "integer",
     "enum": [1, 0]
   }
   ```

### Parámetros Integer Sin Enum (Pero Esperados como Integer)

Los siguientes parámetros están definidos como `"type": "integer"` sin enum, pero deberían aceptar valores enteros:

- **`bedrooms`** (líneas 1265-1267)
- **`bathrooms`** (líneas 1289-1291)
- **`minBedrooms`** (líneas 1249-1251)
- **`maxBedrooms`** (líneas 1257-1259)
- **`minBathrooms`** (líneas 1273-1275)
- **`maxBathrooms`** (líneas 1281-1283)

---

## ❌ Problemas Identificados en la Implementación MCP

### 1. **Error de Validación de Tipos**

**Problema:** El servidor MCP rechaza valores enteros con el error:
```
Parameter 'is_active' must be one of types [integer, null], got number
```

**Causa Raíz:**
- El esquema MCP está configurado para aceptar `integer` pero el validador está interpretando los valores `1` y `0` como `number` en lugar de `integer`
- Esto sugiere un problema en la serialización/deserialización JSON o en la validación del esquema

### 2. **Parámetros Faltantes en MCP**

**Parámetros del esquema oficial que NO están disponibles en MCP:**
- `petsFriendly` → MCP tiene `pets_friendly` (naming diferente)
- `allowUnitRates` → No disponible en MCP
- `computed` → No disponible en MCP
- `inherited` → No disponible en MCP
- `limited` → No disponible en MCP
- `includeDescriptions` → No disponible en MCP
- `unitStatus` → No disponible en MCP
- `roleId` → No disponible en MCP

### 3. **Diferencias en Naming Convention**

| Esquema Oficial | MCP Implementation | Estado |
|-----------------|-------------------|---------|
| `petsFriendly` | `pets_friendly` | ✅ Disponible (naming diferente) |
| `isActive` | `is_active` | ✅ Disponible (naming diferente) |
| `isBookable` | `is_bookable` | ✅ Disponible (naming diferente) |
| `allowUnitRates` | ❌ No disponible | ❌ Faltante |
| `computed` | ❌ No disponible | ❌ Faltante |
| `inherited` | ❌ No disponible | ❌ Faltante |
| `limited` | ❌ No disponible | ❌ Faltante |
| `includeDescriptions` | ❌ No disponible | ❌ Faltante |

### 4. **Límite de Paginación**

**Esquema Oficial:** No especifica límite máximo de `size`
**MCP Implementation:** Límite de 5 unidades por página

**Recomendación:** Aumentar el límite a 25-50 unidades por página para uso productivo.

---

## 🔧 Soluciones Recomendadas

### **Prioridad ALTA - Corregir Validación de Tipos**

**Problema:** Los parámetros booleanos no funcionan debido a error de validación
**Solución:**
1. Revisar el esquema de validación en el servidor MCP
2. Asegurar que los valores `1` y `0` sean interpretados como `integer`, no como `number`
3. Considerar aceptar tanto `integer` como `string` para mayor flexibilidad

### **Prioridad MEDIA - Agregar Parámetros Faltantes**

**Parámetros críticos a implementar:**
1. `allowUnitRates` → Para filtrar unidades que permiten tarifas específicas
2. `unitStatus` → Para filtrar por estado de limpieza (clean, dirty, occupied, etc.)
3. `roleId` → Para filtrar por roles específicos
4. `includeDescriptions` → Para incluir descripciones en la respuesta

### **Prioridad BAJA - Mejoras de Naming**

**Estandarizar naming convention:**
- Mantener consistencia entre snake_case (MCP) y camelCase (API oficial)
- Documentar claramente las diferencias de naming

---

## 📊 Comparación de Funcionalidades

| Funcionalidad | Esquema Oficial | MCP Implementation | Estado |
|---------------|-----------------|-------------------|---------|
| **Búsqueda básica** | ✅ | ✅ | ✅ Funcional |
| **Paginación** | ✅ | ✅ | ✅ Funcional |
| **Ordenamiento** | ✅ | ✅ | ✅ Funcional |
| **Filtro por texto** | ✅ | ✅ | ✅ Funcional |
| **Filtro por fechas** | ✅ | ✅ | ✅ Funcional |
| **Filtro por tipo** | ✅ | ✅ | ✅ Funcional |
| **Parámetros booleanos** | ✅ | ❌ | ❌ **ROTO** |
| **Filtro por estado** | ✅ | ❌ | ❌ No disponible |
| **Filtro por roles** | ✅ | ❌ | ❌ No disponible |
| **Filtro por tarifas** | ✅ | ❌ | ❌ No disponible |

---

## 🎯 Plan de Acción Inmediato

### **Fase 1: Corrección Crítica (1-2 días)**
1. ✅ **Corregir validación de tipos integer/booleanos**
   - Investigar y corregir el problema de validación en el servidor MCP
   - Asegurar que `1` y `0` sean aceptados como `integer`
   - Probar todos los parámetros booleanos disponibles

### **Fase 2: Funcionalidades Faltantes (1 semana)**
2. ✅ **Implementar parámetros críticos faltantes**
   - `unitStatus` para filtro por estado de limpieza
   - `roleId` para filtro por roles
   - `allowUnitRates` para filtro por tarifas

### **Fase 3: Mejoras y Optimización (2 semanas)**
3. ✅ **Aumentar límite de paginación**
   - Cambiar de 5 a 25-50 unidades por página
   - Documentar límites claramente

4. ✅ **Mejorar documentación**
   - Documentar diferencias de naming entre API oficial y MCP
   - Proporcionar ejemplos de uso para todos los parámetros
   - Crear guía de migración desde API oficial

---

## 📋 Checklist de Validación

### **Parámetros Booleanos a Probar (Post-Corrección)**
- [ ] `is_active` con valores 0 y 1
- [ ] `pets_friendly` con valores 0 y 1
- [ ] `is_bookable` con valores 0 y 1
- [ ] `smoking_allowed` con valores 0 y 1
- [ ] `children_allowed` con valores 0 y 1
- [ ] `events_allowed` con valores 0 y 1
- [ ] `is_accessible` con valores 0 y 1

### **Parámetros Integer a Probar**
- [ ] `bedrooms` con valores enteros (1, 2, 3, 4, 5)
- [ ] `bathrooms` con valores enteros (1, 2, 3, 4)
- [ ] `min_bedrooms` con valores enteros
- [ ] `max_bedrooms` con valores enteros
- [ ] `min_bathrooms` con valores enteros
- [ ] `max_bathrooms` con valores enteros

### **Nuevos Parámetros a Implementar**
- [ ] `unit_status` con valores: clean, dirty, occupied, inspection, inprogress
- [ ] `role_id` con valores enteros
- [ ] `allow_unit_rates` con valores 0 y 1

---

## 🏆 Conclusión

La implementación MCP tiene una **base sólida** con las funcionalidades principales funcionando correctamente. El principal problema es la **validación incorrecta de tipos integer/booleanos**, que impide usar filtros importantes.

**Puntuación Actual:** 7/10
**Puntuación Post-Corrección:** 9/10

**Acción Inmediata Requerida:**
1. 🔴 **CRÍTICO:** Corregir validación de tipos integer/booleanos
2. 🟡 **IMPORTANTE:** Aumentar límite de paginación
3. 🟢 **MEJORA:** Implementar parámetros faltantes

Una vez corregidos estos problemas, la implementación MCP será **completamente funcional** y compatible con el esquema oficial de TrackHS.

---

**Elaborado por:** Análisis de Esquema vs Implementación
**Fecha:** 22 de octubre de 2025
**Versión:** 1.0
