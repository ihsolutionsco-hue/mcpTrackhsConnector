# Reporte: Filtros Booleanos `is_active` e `is_bookable` No Funcionan

## 📋 Resumen Ejecutivo

**Problema Identificado**: Los filtros `is_active` e `is_bookable` en la herramienta `search_units` de TrackHS **NO están funcionando correctamente**. A pesar de que los parámetros se envían correctamente a la API, esta los ignora y retorna todas las unidades sin aplicar el filtro.

## 🔍 Evidencia del Problema

### Test Realizado
- **Fecha**: 2025-10-27
- **Herramienta**: `search_units` de TrackHS MCP
- **Parámetros probados**: `is_active=1`, `is_bookable=1`, y combinaciones

### Resultados del Testing

#### 1. Búsqueda sin filtros
```
Parámetros: page=1, size=10
Resultado: 10 unidades (de 247 totales)
Campos is_active/is_bookable: N/A (no presentes en respuesta)
```

#### 2. Búsqueda con is_active=1
```
Parámetros: page=1, size=10, is_active=1
Resultado: 10 unidades (de 247 totales) - MISMO RESULTADO
Campos is_active/is_bookable: N/A (no presentes en respuesta)
```

#### 3. Búsqueda con is_bookable=1
```
Parámetros: page=1, size=10, is_bookable=1
Resultado: 10 unidades (de 247 totales) - MISMO RESULTADO
Campos is_active/is_bookable: N/A (no presentes en respuesta)
```

#### 4. Búsqueda con ambos filtros
```
Parámetros: page=1, size=10, is_active=1, is_bookable=1
Resultado: 10 unidades (de 247 totales) - MISMO RESULTADO
Campos is_active/is_bookable: N/A (no presentes en respuesta)
```

## 🔧 Análisis Técnico

### 1. Parámetros se Envían Correctamente
Los logs muestran que los parámetros se envían correctamente a la API:
```
📤 Parámetros enviados a API: {'page': 1, 'size': 3, 'is_active': 1}
HTTP Request: GET https://ihmvacations.trackhs.com/api/pms/units?page=1&size=3&is_active=1
```

### 2. API Responde con Éxito
La API responde con HTTP 200 OK, pero **ignora completamente los filtros booleanos**.

### 3. Campos No Están en la Respuesta
Los campos `is_active` e `is_bookable` no están presentes en la respuesta de la API, aparecen como `N/A`.

### 4. Total de Unidades No Cambia
El total de unidades (247) es idéntico en todas las búsquedas, confirmando que los filtros no se aplican.

## 🚨 Impacto del Problema

### Para Usuarios
- **Filtros inútiles**: Los filtros `is_active` e `is_bookable` no sirven para nada
- **Datos incorrectos**: Los usuarios pueden obtener unidades que no están activas o no son reservables
- **Experiencia confusa**: Los filtros aparentan funcionar pero no tienen efecto

### Para Desarrolladores
- **Código engañoso**: El código sugiere que los filtros funcionan pero no es así
- **Validaciones inútiles**: Las validaciones de estos parámetros no tienen sentido
- **Documentación incorrecta**: La documentación promete funcionalidad que no existe

## 🔍 Posibles Causas

### 1. API No Soportada
La API de TrackHS podría no soportar estos parámetros de filtrado.

### 2. Nombres de Parámetros Incorrectos
Los parámetros podrían tener nombres diferentes en la API real.

### 3. Valores Incorrectos
La API podría esperar valores diferentes (ej: `true`/`false` en lugar de `1`/`0`).

### 4. Filtros Ignorados
La API podría estar configurada para ignorar estos filtros por alguna razón.

## 📊 Comparación con Otros Filtros

### Filtros que SÍ Funcionan
- `bedrooms`: ✅ Funciona correctamente
- `bathrooms`: ✅ Funciona correctamente
- `search`: ✅ Funciona correctamente
- `page`/`size`: ✅ Funcionan correctamente

### Filtros que NO Funcionan
- `is_active`: ❌ No funciona
- `is_bookable`: ❌ No funciona

## 🛠️ Recomendaciones

### Inmediatas
1. **Remover de la documentación** los filtros `is_active` e `is_bookable` hasta que se resuelva
2. **Agregar advertencia** en el código indicando que estos filtros no funcionan
3. **Validar en el cliente** los campos `is_active` e `is_bookable` de la respuesta

### A Mediano Plazo
1. **Contactar soporte de TrackHS** para verificar si estos filtros están soportados
2. **Investigar documentación oficial** de la API de TrackHS
3. **Probar con diferentes valores** (true/false, "true"/"false", etc.)

### A Largo Plazo
1. **Implementar filtrado del lado del cliente** si la API no soporta estos filtros
2. **Crear endpoint alternativo** que permita filtrar por estos campos
3. **Actualizar la documentación** una vez resuelto el problema

## 📝 Código Afectado

### Archivos Principales
- `src/trackhs_mcp/services/unit_service.py` - Líneas 34-35, 98-106, 132-135
- `src/trackhs_mcp/schemas.py` - Definiciones de esquemas
- Documentación de la herramienta MCP

### Líneas Específicas
```python
# En unit_service.py
is_active: Optional[str] = None,
is_bookable: Optional[str] = None,

# Validación que no sirve
if is_active is not None:
    params["is_active"] = is_active
if is_bookable is not None:
    params["is_bookable"] = is_bookable
```

## 🎯 Conclusión

Los filtros `is_active` e `is_bookable` en la herramienta `search_units` **NO FUNCIONAN** y deben ser considerados como **no funcionales** hasta que se resuelva el problema con la API de TrackHS.

**Recomendación**: Remover temporalmente estos filtros de la documentación y agregar una nota de que no están soportados por la API actual.
