# Reporte Final: Pruebas MCP search_units

## Resumen Ejecutivo

**Fecha:** 2025-10-22
**Tester:** AI MCP Testing Agent
**Herramienta:** mcp_ihmTrackhs_search_units
**Estado:** 🔴 PROBLEMA PERSISTENTE - REQUIERE SOLUCIÓN ALTERNATIVA

## Problema Identificado

### Causa Raíz Confirmada

El problema **NO está en la función interna** sino en **cómo FastMCP genera y valida el esquema MCP**.

**Flujo del problema:**
1. Cliente MCP envía: `{"bedrooms": "3"}` (string)
2. FastMCP valida contra esquema generado: `bedrooms: integer`
3. FastMCP **rechaza inmediatamente** porque "3" (string) ≠ `integer`
4. **Nunca llega a la función** donde están las correcciones

### Evidencia del Problema

**Pruebas realizadas:**
- ✅ Funcionalidad básica: Operativa (paginación, fechas)
- ❌ Parámetros numéricos: Siguen fallando con el mismo error
- ❌ Parámetros booleanos: Siguen fallando con el mismo error

**Error persistente:**
```
Parameter 'bedrooms' must be one of types [integer, null], got string
```

## Correcciones Implementadas

### 1. Modificación de Tipos en Función

**Archivo:** `src/trackhs_mcp/infrastructure/mcp/search_units.py`

**Cambios realizados:**
```python
# ANTES:
bedrooms: Optional[Union[int, float, str]] = Field(...)

# DESPUÉS:
bedrooms: Optional[str] = Field(...)
```

**Parámetros modificados:**
- `calendar_id`, `role_id`
- `bedrooms`, `min_bedrooms`, `max_bedrooms`
- `bathrooms`, `min_bathrooms`, `max_bathrooms`
- `pets_friendly`, `allow_unit_rates`, `computed`, `inherited`
- `limited`, `is_bookable`, `include_descriptions`, `is_active`
- `events_allowed`, `smoking_allowed`, `children_allowed`, `is_accessible`

### 2. Hook de Corrección de Esquemas

**Archivo:** `src/trackhs_mcp/infrastructure/mcp/schema_hook.py`

El servidor está configurado para usar un hook que corrige esquemas, pero **no está funcionando** para este problema específico.

## Análisis Técnico

### Por Qué No Funciona

1. **FastMCP genera esquemas automáticamente** desde type hints Python
2. **La validación ocurre ANTES** de que llegue a la función
3. **El hook de corrección** no está interceptando correctamente este caso
4. **El cliente MCP envía strings** pero el esquema espera integers

### Soluciones Alternativas Consideradas

#### Opción 1: Modificar FastMCP (No viable)
- Requeriría cambios en la librería FastMCP
- No es práctico para este proyecto

#### Opción 2: Hook más agresivo (Complejo)
- Interceptar la validación de parámetros
- Requeriría monkey patching profundo

#### Opción 3: Conversión en el adaptador (Recomendada)
- Interceptar parámetros antes de la validación
- Convertir strings a números automáticamente

## Recomendación Inmediata

### Solución Propuesta: Adaptador de Conversión

Crear un adaptador que intercepte los parámetros antes de la validación FastMCP:

```python
def convert_mcp_params(params: dict) -> dict:
    """Convierte parámetros MCP de string a tipos esperados"""
    integer_params = {
        'bedrooms', 'min_bedrooms', 'max_bedrooms', 'bathrooms',
        'min_bathrooms', 'max_bathrooms', 'calendar_id', 'role_id'
    }

    boolean_params = {
        'pets_friendly', 'allow_unit_rates', 'computed', 'inherited',
        'limited', 'is_bookable', 'include_descriptions', 'is_active',
        'events_allowed', 'smoking_allowed', 'children_allowed', 'is_accessible'
    }

    for param in integer_params:
        if param in params and isinstance(params[param], str):
            try:
                params[param] = int(params[param])
            except ValueError:
                pass  # Mantener como string si no es convertible

    for param in boolean_params:
        if param in params and isinstance(params[param], str):
            if params[param] in ['1', 'true', 'True']:
                params[param] = 1
            elif params[param] in ['0', 'false', 'False']:
                params[param] = 0

    return params
```

## Estado Actual

- ✅ **Problema identificado:** Esquema MCP vs validación FastMCP
- ✅ **Correcciones implementadas:** Tipos en función cambiados
- ❌ **Problema persiste:** Validación ocurre antes de la función
- 🔄 **Próximo paso:** Implementar adaptador de conversión

## Impacto en Usuarios

**CRÍTICO:** Los usuarios no pueden usar filtros importantes:
- Filtros por número de habitaciones/baños
- Filtros por características de propiedad
- Filtros booleanos (activo, bookable, etc.)

**Funcionalidad afectada:** ~15 de 30+ parámetros disponibles

---

**Recomendación:** Implementar adaptador de conversión de parámetros antes de la validación FastMCP para resolver definitivamente el problema de compatibilidad.
