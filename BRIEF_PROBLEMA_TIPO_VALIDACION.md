# Brief: Problema de Validación de Tipos en FastMCP MCP SDK

## Problema Principal

El MCP SDK está validando los parámetros de entrada **ANTES** de que lleguen a FastMCP o Pydantic, rechazando strings cuando el schema MCP espera tipos específicos (boolean, integer, List[int]).

## Error Específico

```
Parameter 'is_active' must be one of types [boolean, null], got string
```

Similar para otros parámetros:
- `bedrooms`: espera `integer`, recibe `string` ("2")
- `node_id`: espera `array[integer]`, recibe `string` ("[3,6]")

## Contexto Técnico

### Arquitectura Actual

1. **Cliente MCP** envía parámetros como strings (ej: `"true"`, `"2"`, `"[3,6]"`)
2. **MCP SDK** valida contra el **schema MCP** generado por FastMCP
3. **FastMCP** genera el schema MCP desde **anotaciones de Python** en `tool_wrapper` (actualmente `Any`)
4. **Pydantic** debería validar y convertir strings a tipos correctos, pero nunca llega ahí

### Cambios Intentados (Sin Éxito)

1. ✅ Cambiar schema Pydantic de `Union[str, bool]` → `str`
   - Schema JSON de Pydantic acepta strings ✅
   - Schema MCP generado por FastMCP **sigue restringido** ❌

2. ✅ Usar `Any` en anotaciones FastMCP
   - No resuelve el problema ❌

3. ✅ Eliminar `field_validator` del schema Pydantic
   - Mover conversión a `build_units_query` ✅
   - Pero el MCP SDK valida ANTES de llegar ahí ❌

4. ✅ Agregar `strict_input_validation=False` al servidor FastMCP
   - No ayuda porque el MCP SDK valida ANTES ❌

## Root Cause

**El MCP SDK está validando contra el schema MCP ANTES de que FastMCP pueda hacer la coerción automática o Pydantic pueda convertir los strings.**

FastMCP genera el schema MCP desde:
- Anotaciones de Python en `tool_wrapper` (actualmente `Any`)
- No está usando el schema JSON de Pydantic directamente

## Archivos Clave

- `src/server_logic.py`: Registro de herramientas (línea ~180-330)
  - Usa `Any` en anotaciones FastMCP
  - Genera `tool_wrapper` con `Parameter(..., annotation=Any)`

- `src/schemas/unit.py`: Schema Pydantic
  - Campos como `is_active: Optional[str]` (acepta strings)
  - Schema JSON de Pydantic acepta strings ✅

- `src/utils/api_client.py`: Construcción de query API
  - Convierte strings a bool/int/List[int] en `build_units_query` ✅

## Pregunta Clave

**¿Cómo hacer que FastMCP genere un schema MCP que acepte strings cuando el schema Pydantic acepta strings?**

O alternativamente:

**¿Cómo hacer que el MCP SDK NO valide tipos antes de que FastMCP/Pydantic puedan hacer la conversión?**

## Estado Actual

- ✅ Schema Pydantic acepta strings
- ✅ Conversión strings → tipos en `build_units_query`
- ✅ Logging mejorado con FastMCP best practices
- ❌ **Schema MCP generado por FastMCP sigue restringido**
- ❌ **MCP SDK valida ANTES de FastMCP/Pydantic**

## Información de FastMCP

- Versión: FastMCP 2.13.0 (según documentación)
- `strict_input_validation=False` configurado
- `LoggingMiddleware` agregado
- `TimingMiddleware` agregado

## Próximos Pasos Sugeridos

1. Investigar cómo FastMCP genera el schema MCP desde Pydantic models
2. Verificar si hay forma de pasar el schema JSON de Pydantic directamente a FastMCP
3. Revisar si el MCP SDK tiene configuración para deshabilitar validación temprana
4. Considerar usar Context en herramientas para logging a clientes MCP

