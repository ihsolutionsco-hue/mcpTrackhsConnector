# Guía del Schema Fixer para MCP

## Descripción

El Schema Fixer es un módulo que corrige automáticamente los esquemas JSON generados por FastMCP Cloud, resolviendo el problema donde los valores numéricos se serializan como strings en lugar de tipos nativos.

## Problema Resuelto

### Antes (Problemático)
```json
{
  "in_house_today": {
    "anyOf": [
      {
        "type": "integer",
        "minimum": "0",    // ❌ String en lugar de número
        "maximum": "1"      // ❌ String en lugar de número
      },
      {
        "type": "null"
      }
    ],
    "default": "null"      // ❌ String en lugar de null
  }
}
```

### Después (Corregido)
```json
{
  "in_house_today": {
    "anyOf": [
      {
        "type": "integer",
        "minimum": 0,      // ✅ Número nativo
        "maximum": 1        // ✅ Número nativo
      },
      {
        "type": "null"
      }
    ],
    "default": null         // ✅ null nativo
  }
}
```

## Componentes

### 1. `schema_fixer.py`
Módulo principal con funciones de corrección:

- `fix_json_schema_types()`: Corrige esquemas recursivamente
- `validate_json_schema()`: Valida esquemas contra JSON Schema Draft 7
- `compare_schemas()`: Compara esquemas antes/después

### 2. `schema_hook.py`
Hook que intercepta FastMCP:

- `SchemaFixerHook`: Clase que aplica monkey-patch
- `create_schema_fixed_server()`: Crea servidor con hook aplicado
- Intercepta `list_tools()` y `get_tool()`

### 3. Integración en `server.py`
El servidor principal usa automáticamente el hook:

```python
from trackhs_mcp.infrastructure.mcp.schema_hook import create_schema_fixed_server

# Crear servidor con corrección automática
mcp = create_schema_fixed_server("TrackHS MCP Server")
```

## Uso

### Automático (Recomendado)
El hook se aplica automáticamente al crear el servidor:

```python
from trackhs_mcp.infrastructure.mcp.schema_hook import create_schema_fixed_server

mcp = create_schema_fixed_server("Mi Servidor MCP")
# El hook ya está aplicado
```

### Manual
Si necesitas control manual:

```python
from fastmcp import FastMCP
from trackhs_mcp.infrastructure.mcp.schema_hook import apply_schema_fixer_hook

mcp = FastMCP("Mi Servidor MCP")
hook = apply_schema_fixer_hook(mcp)
# Hook aplicado manualmente
```

## Scripts de Prueba

### 1. Prueba Básica
```bash
python scripts/test_schema_fixer.py
```
Prueba la funcionalidad básica del schema fixer.

### 2. Inspección de Esquemas
```bash
python scripts/inspect_schemas_with_fix.py
```
Inspecciona esquemas con corrección aplicada.

### 3. Comparación Antes/Después
```bash
python scripts/compare_schemas_before_after.py
```
Compara esquemas antes y después de la corrección.

## Campos Corregidos

El schema fixer convierte automáticamente estos campos de string a número:

- `minimum` → número
- `maximum` → número
- `minLength` → número
- `maxLength` → número
- `minItems` → número
- `maxItems` → número
- `minProperties` → número
- `maxProperties` → número
- `default` → número (cuando es numérico)

## Casos Edge Manejados

### 1. Strings Legítimos
No convierte strings que no son números:
```python
{
  "pattern": "^\\d{4}-\\d{2}-\\d{2}$",  # ✅ Se mantiene como string
  "description": "Date format"            # ✅ Se mantiene como string
}
```

### 2. Objetos Anidados
Corrige recursivamente:
```python
{
  "properties": {
    "nested": {
      "minimum": "0"  # ✅ Se convierte a 0
    }
  }
}
```

### 3. Arrays con Objetos
Corrige en arrays:
```python
{
  "anyOf": [
    {
      "minimum": "1"  # ✅ Se convierte a 1
    }
  ]
}
```

## Validación

### Validación de Esquemas
```python
from trackhs_mcp.infrastructure.utils.schema_fixer import validate_json_schema

is_valid = validate_json_schema(schema)
```

### Comparación de Cambios
```python
from trackhs_mcp.infrastructure.utils.schema_fixer import compare_schemas

differences = compare_schemas(original, fixed)
print(f"Cambios: {differences['total_changes']}")
```

## Logging

El schema fixer incluye logging detallado:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Verás logs como:
# INFO - Fixed schema for tool 'search_reservations': 5 changes
# DEBUG - Converted minimum: '0' -> 0
```

## Compatibilidad

### Clientes MCP Soportados
- ✅ ElevenLabs
- ✅ Claude Desktop
- ✅ MCP Inspector
- ✅ Cualquier cliente que espere JSON Schema válido

### FastMCP Versiones
- ✅ FastMCP 0.1.x
- ✅ FastMCP Cloud
- ✅ FastMCP Local

## Troubleshooting

### Hook No Se Aplica
```python
# Verificar que el hook esté aplicado
if hasattr(mcp, '_schema_fixer_hook'):
    print("Hook aplicado correctamente")
else:
    print("Hook no aplicado")
```

### Esquemas Aún Tienen Strings
1. Verificar que el hook esté aplicado
2. Revisar logs para errores
3. Probar con script de comparación

### Errores de Validación
```python
# Validar esquema manualmente
from trackhs_mcp.infrastructure.utils.schema_fixer import validate_json_schema

if not validate_json_schema(schema):
    print("Esquema inválido")
```

## Mejores Prácticas

### 1. Usar el Hook Automático
```python
# ✅ Recomendado
mcp = create_schema_fixed_server("Mi Servidor")

# ❌ Evitar
mcp = FastMCP("Mi Servidor")
# Aplicar hook manualmente después
```

### 2. Validar en Desarrollo
```bash
# Ejecutar antes de desplegar
python scripts/test_schema_fixer.py
python scripts/inspect_schemas_with_fix.py
```

### 3. Monitorear en Producción
```python
# El hook incluye logging automático
# Revisar logs para confirmar que funciona
```

## Resultados Esperados

Después de aplicar el schema fixer:

1. **ElevenLabs** podrá interpretar correctamente las herramientas
2. **Los esquemas** tendrán valores numéricos nativos
3. **La compatibilidad** con clientes MCP mejorará
4. **Los errores** de "out of date" desaparecerán

## Referencias

- [JSON Schema Draft 7](https://json-schema.org/draft-07/json-schema-release-notes.html)
- [MCP Specification](https://modelcontextprotocol.io/docs/specification)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
