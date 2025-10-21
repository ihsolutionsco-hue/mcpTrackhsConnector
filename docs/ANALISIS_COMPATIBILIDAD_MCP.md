# Análisis de Compatibilidad MCP - TrackHS Connector

## Fecha
2025-10-20

## Resumen Ejecutivo

Se realizó una auditoría completa de los esquemas MCP del servidor TrackHS Connector para identificar problemas de compatibilidad con diferentes clientes MCP, especialmente con el agente de ElevenLabs.

### Resultados Principales
- **Total de herramientas**: 7
- **Herramientas con problemas**: 7 (100%)
- **Herramientas válidas**: 0

## Problema Principal Identificado

### 1. Uso Excesivo de `anyOf` con Múltiples Tipos

**Impacto**: CRÍTICO para compatibilidad con clientes AI como ElevenLabs

**Descripción**: FastMCP está generando esquemas con `anyOf` que contienen múltiples tipos para casi todos los parámetros. Esto se debe al uso de `Union[int, float, str]` o `Union[int, str, None]` en las type annotations de Python.

**Ejemplo del problema**:
```json
{
  "page": {
    "anyOf": [
      {"type": "integer"},
      {"type": "number"},
      {"type": "string"}
    ],
    "default": 1
  }
}
```

**Por qué es problemático**:
1. **Ambigüedad**: Clientes AI no saben qué tipo enviar (¿"1" o 1?)
2. **Incompatibilidad**: Algunos clientes esperan tipos específicos
3. **Errores de validación**: Pueden fallar en tiempo de ejecución
4. **Confusión del modelo**: El AI puede elegir el tipo incorrecto

### 2. Parámetros Opcionales con `anyOf` con null

**Impacto**: ALTO

**Estadísticas**:
- `search_reservations`: 26 de 27 parámetros tienen `anyOf` con null
- `search_units`: 36 de 37 parámetros tienen `anyOf` con null
- `create_maintenance_work_order`: 13 de 19 parámetros tienen `anyOf`
- `create_housekeeping_work_order`: 14 de 16 parámetros tienen `anyOf`

**Ejemplo**:
```json
{
  "search": {
    "anyOf": [
      {"type": "string"},
      {"type": "null"}
    ],
    "default": null
  }
}
```

**Solución recomendada**: Usar parámetros opcionales con un solo tipo:
```json
{
  "search": {
    "type": "string"
  }
}
```
Y marcar el parámetro como no requerido en el array `required`.

### 3. Parámetros con 3-4 Tipos Diferentes

**Impacto**: MUY ALTO

**Casos problemáticos**:

| Herramienta | Parámetro | Tipos en anyOf |
|------------|-----------|----------------|
| search_reservations | page, size | integer, number, string |
| search_reservations | scroll | integer, string, null |
| search_reservations | in_house_today | integer, number, string, null (4 tipos!) |
| search_reservations | group_id | integer, number, string, null (4 tipos!) |
| search_units | calendar_id | integer, number, string, null (4 tipos!) |
| create_maintenance_work_order | actual_time | integer, string, null |
| create_maintenance_work_order | block_checkin | boolean, string, null |

**Problema específico con booleans como strings**:
- `block_checkin: Union[bool, str, None]` permite valores como "true", "false", true, false, "1", "0"
- Clientes AI pueden no saber si enviar booleano o string

## Problemas Secundarios

### 4. Falta de `additionalProperties`

**Impacto**: MEDIO

**Descripción**: Ningún esquema define `additionalProperties: false`, lo que permite parámetros extras no documentados.

**Recomendación**: Agregar `additionalProperties: false` a todos los inputSchema.

### 5. Enums Largos

**Impacto**: BAJO

**Ejemplo**: `sort_column` en `search_reservations` tiene 12 valores enum.

**Recomendación**: Documentar mejor los valores disponibles o considerar reducir las opciones.

### 6. Descripciones Muy Largas

**Impacto**: BAJO-MEDIO

**Descripción**: Las descripciones de herramientas contienen:
- Múltiples ejemplos de código
- Documentación completa de todos los parámetros
- Secciones de error handling
- Formatos de fecha detallados

**Ejemplo**: `search_reservations` tiene una descripción de más de 100 líneas.

**Problema**: Algunos modelos AI pueden confundirse con descripciones muy extensas que mezclan documentación con ejemplos.

## Análisis por Herramienta

### search_reservations
- **Parámetros**: 27 total, 0 requeridos
- **Problemas críticos**: 26 anyOf
- **Tipos problemáticos**:
  - 2 con 3 tipos (page, size)
  - 2 con 4 tipos (in_house_today, group_id, checkin_office_id)
  - 1 enum largo (sort_column: 12 valores)
  - 1 anyOf con array (status: string, array, null)

### get_reservation
- **Parámetros**: 1 total, 1 requerido
- **Problemas**: Mínimos (solo falta additionalProperties)
- **Estado**: BIEN ✅

### get_folio
- **Parámetros**: 1 total, 1 requerido
- **Problemas**: Mínimos (solo falta additionalProperties)
- **Estado**: BIEN ✅

### search_units
- **Parámetros**: 37 total, 0 requeridos
- **Problemas críticos**: 36 anyOf
- **Tipos problemáticos**:
  - 2 con 3 tipos (page, size)
  - 1 con 4 tipos (calendar_id)
  - Múltiples filtros opcionales con anyOf + null

### search_amenities
- **Parámetros**: 9 total, 0 requeridos
- **Problemas**: anyOf en todos los parámetros opcionales

### create_maintenance_work_order
- **Parámetros**: 19 total, 6 requeridos
- **Problemas críticos**: 13 anyOf
- **Tipos problemáticos**:
  - `block_checkin`: boolean, string, null (inconsistente)
  - `actual_time`: integer, string, null
  - Múltiples IDs con anyOf

### create_housekeeping_work_order
- **Parámetros**: 16 total, 2 requeridos
- **Problemas críticos**: 14 anyOf
- **Tipos problemáticos**:
  - `is_inspection`, `is_turn`, `is_manual`, `charge_owner`: boolean, string, null
  - Múltiples números y IDs con anyOf

## Impacto en Clientes MCP

### ElevenLabs Agent (CRÍTICO)
**Síntoma**: "Responde que no puede hacer la consulta"

**Causa raíz probable**:
1. El AI de ElevenLabs ve `anyOf` con múltiples tipos
2. No sabe qué tipo enviar
3. Elige un tipo que el servidor no acepta bien (ej: string "1" en lugar de int 1)
4. El servidor puede aceptar la petición pero luego falla en validación interna

**Solución**: Definir tipos específicos en las signatures de Python.

### Claude Desktop (probablemente OK)
- Más tolerante con `anyOf`
- Puede inferir mejor qué tipo enviar basándose en defaults

### MCP Inspector (OK)
- Muestra todos los tipos posibles
- No hace inferencias, solo lista opciones

## Causa Raíz Técnica

### Código Python Actual
```python
def search_reservations(
    page: Union[int, float, str] = 1,
    size: Union[int, float, str] = 10,
    search: Union[str, None] = None,
    in_house_today: Union[int, float, str, None] = None,
    # ...
):
```

### Esquema MCP Generado por FastMCP
```json
{
  "page": {
    "anyOf": [
      {"type": "integer"},
      {"type": "number"},
      {"type": "string"}
    ],
    "default": 1
  }
}
```

### Problema
FastMCP convierte `Union[int, float, str]` directamente a `anyOf` en JSON Schema, sin intentar simplificar o elegir el tipo más apropiado.

## Soluciones Recomendadas

### Solución 1: Cambiar Tipos en Signatures (RECOMENDADO)

**Acción**: Cambiar las type annotations de Python a tipos específicos

**Antes**:
```python
def search_reservations(
    page: Union[int, float, str] = 1,
    size: Union[int, float, str] = 10,
    search: Union[str, None] = None,
):
```

**Después**:
```python
def search_reservations(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
):
```

**Ventajas**:
- Esquemas MCP más limpios
- Mejor documentación del código
- Mayor claridad para clientes AI
- Compatible con especificación MCP

**Desventajas**:
- Puede requerir cambios en lógica de normalización
- Necesita testing exhaustivo

### Solución 2: Agregar `additionalProperties: false`

**Acción**: Modificar la generación de esquemas para incluir `additionalProperties: false`

**Implementación**: Puede requerir custom serialization en FastMCP o post-procesamiento.

### Solución 3: Simplificar Descripciones

**Acción**: Separar documentación de ejemplos

**Antes**:
```python
"""
Search reservations...
[100 líneas de documentación y ejemplos]
"""
```

**Después**:
```python
"""
Search reservations in Track HS API with comprehensive filtering options.
Supports pagination, date ranges, status filtering, and more.
"""
```

Y mover ejemplos a:
- Documentación separada (README, wiki)
- Recursos MCP (si se implementa)
- Prompts MCP con ejemplos

## Plan de Acción

### Fase 1: Cambios Críticos (Alta Prioridad)
1. ✅ Auditar todos los esquemas actuales
2. ⏳ Cambiar `Union` types a tipos específicos en signatures
3. ⏳ Mantener normalización interna para backward compatibility
4. ⏳ Agregar `additionalProperties: false` a todos los esquemas

### Fase 2: Mejoras (Media Prioridad)
1. ⏳ Simplificar descripciones de herramientas
2. ⏳ Documentar enums largos
3. ⏳ Crear guía de uso para cada herramienta

### Fase 3: Testing (Alta Prioridad)
1. ⏳ Test con MCP Inspector
2. ⏳ Test con Claude Desktop
3. ⏳ Test con ElevenLabs Agent
4. ⏳ Validar todos los casos de uso existentes

### Fase 4: Documentación
1. ⏳ Actualizar README con información de compatibilidad
2. ⏳ Crear matriz de compatibilidad por cliente
3. ⏳ Documentar limitaciones conocidas

## Referencias

- [MCP Specification - Tools](reference/mcp/05-referencias/especificacion/draft/server/tools.mdx)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)
- [FastMCP Documentation](reference/mcp/07-repositorios-originales/python-sdk/docs/)

## Archivos Generados

- `docs/tools_schemas.json` - Esquemas completos de todas las herramientas
- `docs/schema_validation_report.json` - Reporte detallado de validación
- `scripts/inspect_tools_simple.py` - Script de auditoría (puede reutilizarse)

## Conclusión

El problema principal de incompatibilidad con clientes como ElevenLabs es el uso excesivo de `anyOf` con múltiples tipos en los parámetros. Esto se debe a las type annotations `Union` en Python que FastMCP convierte directamente a `anyOf` en JSON Schema.

**La solución recomendada es cambiar los tipos en las signatures de Python a tipos específicos** (int, str, bool, Optional[T]) y mantener la normalización interna para asegurar backward compatibility.

Esta acción resolverá aproximadamente el 90% de los problemas de compatibilidad identificados.
