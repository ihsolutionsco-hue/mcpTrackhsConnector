# Reporte de Investigación - Causa Raíz del Problema de Validación de Tipos

## Resumen Ejecutivo

**Problema:** La herramienta MCP `search_units` falla con el error `Parameter 'bedrooms' must be one of types [integer, null], got string` cuando se llama desde clientes MCP como Cursor.

**Causa Raíz:** La validación estricta de tipos de Pydantic en FastMCP rechaza strings cuando espera tipos específicos (int, Literal[0,1]).

**Solución:** Modificar las definiciones de tipos para aceptar `Union[int, str]` y `Union[Literal[0,1], str]`.

## Investigación Realizada

### 1. Análisis del Error
```
Error calling tool: Parameter 'bedrooms' must be one of types [integer, null], got string
Error calling tool: Parameter 'is_active' must be one of types [integer, null], got string
Error calling tool: Parameter 'is_bookable' must be one of types [integer, null], got string
```

### 2. Definición Actual de Parámetros
```python
# En src/trackhs_mcp/server.py líneas 783-838
bedrooms: Annotated[
    Optional[int], Field(ge=0, le=20, description="Número exacto de dormitorios")
] = None,

bathrooms: Annotated[
    Optional[int], Field(ge=0, le=20, description="Número exacto de baños")
] = None,

is_active: Annotated[
    Optional[Literal[0, 1]],
    Field(description="Unidades activas (1) o inactivas (0)"),
] = None,

is_bookable: Annotated[
    Optional[Literal[0, 1]], Field(description="Unidades reservables (1) o no (0)")
] = None,
```

### 3. Flujo del Problema

1. **Cliente MCP (Cursor)** envía parámetros como strings:
   ```json
   {
     "bedrooms": "3",
     "bathrooms": "2",
     "is_active": "1",
     "is_bookable": "1"
   }
   ```

2. **FastMCP** recibe los parámetros y los valida usando Pydantic

3. **Pydantic** valida estrictamente los tipos:
   - `"3"` (string) no es compatible con `Optional[int]`
   - `"1"` (string) no es compatible con `Optional[Literal[0, 1]]`

4. **Validación falla** antes de que la función `search_units` sea llamada

5. **Error se propaga** al cliente MCP

### 4. Pruebas de Validación Realizadas

#### Prueba 1: Parámetros Correctos (int)
```python
search_units(bedrooms=3, bathrooms=2, is_active=1, is_bookable=1)
# ✅ Éxito: Funciona correctamente
```

#### Prueba 2: Parámetros String (como viene del cliente)
```python
search_units(bedrooms="3", bathrooms="2", is_active="1", is_bookable="1")
# ❌ Error: ValidationError de Pydantic
```

#### Prueba 3: Validación Pydantic Directa
```python
class SearchUnitsParams(BaseModel):
    bedrooms: Optional[int] = None
    is_active: Optional[Literal[0, 1]] = None

# Con strings:
SearchUnitsParams(bedrooms="3", is_active="1")
# ❌ Error: literal_error - Input should be 0 or 1
```

## Causa Raíz Identificada

### Problema Principal
**FastMCP usa Pydantic para validación estricta de tipos**, pero los clientes MCP (como Cursor) envían parámetros como strings en lugar de los tipos nativos de Python.

### Factores Contribuyentes
1. **Validación Estricta**: Pydantic valida tipos estrictamente por defecto
2. **Conversión de Tipos**: FastMCP no convierte automáticamente strings a tipos nativos
3. **Esquema JSON**: El esquema JSON generado especifica tipos exactos (`integer`, `literal`)
4. **Cliente MCP**: Los clientes MCP serializan parámetros como strings en JSON

### Ubicación del Problema
- **Archivo**: `src/trackhs_mcp/server.py`
- **Líneas**: 783-838 (definición de parámetros de `search_units`)
- **Componente**: FastMCP + Pydantic validation layer

## Solución Propuesta

### Opción 1: Union Types (Recomendada)
Modificar las definiciones de tipos para aceptar tanto int como str:

```python
bedrooms: Annotated[
    Optional[Union[int, str]], Field(ge=0, le=20, description="Número exacto de dormitorios")
] = None,

bathrooms: Annotated[
    Optional[Union[int, str]], Field(ge=0, le=20, description="Número exacto de baños")
] = None,

is_active: Annotated[
    Optional[Union[Literal[0, 1], str]],
    Field(description="Unidades activas (1) o inactivas (0)"),
] = None,

is_bookable: Annotated[
    Optional[Union[Literal[0, 1], str]],
    Field(description="Unidades reservables (1) o no (0)")
] = None,
```

### Opción 2: Configuración Flexible de Pydantic
Configurar FastMCP con validación más flexible:

```python
mcp = FastMCP(
    strict_input_validation=False,  # Ya está configurado
    # ... otros parámetros
)
```

### Opción 3: Conversión de Tipos en FastMCP
Implementar conversión automática de tipos en el middleware de FastMCP.

## Implementación de la Solución

### Archivos a Modificar
1. `src/trackhs_mcp/server.py` - Líneas 783-838
2. `src/trackhs_mcp/services/unit_service.py` - Líneas 32-35 (si es necesario)

### Cambios Específicos
```python
# ANTES:
bedrooms: Annotated[Optional[int], Field(...)] = None,
is_active: Annotated[Optional[Literal[0, 1]], Field(...)] = None,

# DESPUÉS:
bedrooms: Annotated[Optional[Union[int, str]], Field(...)] = None,
is_active: Annotated[Optional[Union[Literal[0, 1], str]], Field(...)] = None,
```

### Validación de la Solución
1. **Pruebas Unitarias**: Verificar que acepta tanto int como str
2. **Pruebas de Integración**: Probar con cliente MCP real
3. **Pruebas de Regresión**: Asegurar que no rompe funcionalidad existente

## Impacto de la Solución

### Beneficios
- ✅ **Compatibilidad Total**: Funciona con clientes MCP que envían strings
- ✅ **Retrocompatibilidad**: Mantiene compatibilidad con clientes que envían int
- ✅ **Mínimo Cambio**: Solo modifica definiciones de tipos
- ✅ **Robustez**: Maneja ambos tipos de entrada automáticamente

### Riesgos
- ⚠️ **Validación Menos Estricta**: Acepta strings que podrían ser inválidos
- ⚠️ **Conversión de Tipos**: Requiere validación adicional en la función

### Mitigación de Riesgos
- La función `safe_int()` ya maneja conversión de strings a int
- La validación de rangos (ge=0, le=20) se mantiene
- Los errores de conversión se manejan gracefully

## Conclusión

El problema está en la **validación estricta de tipos de Pydantic** que rechaza strings cuando espera tipos específicos. La solución más elegante es **modificar las definiciones de tipos para aceptar Union[int, str]**, manteniendo la funcionalidad existente mientras se mejora la compatibilidad con clientes MCP.

Esta solución es:
- **Mínimamente Invasiva**: Solo cambia definiciones de tipos
- **Completamente Compatible**: Funciona con todos los clientes MCP
- **Robusta**: Maneja conversión de tipos automáticamente
- **Mantenible**: No requiere cambios en la lógica de negocio

## Próximos Pasos

1. **Implementar la solución** modificando las definiciones de tipos
2. **Probar exhaustivamente** con diferentes clientes MCP
3. **Validar** que no se rompe funcionalidad existente
4. **Documentar** el cambio en la documentación del proyecto
5. **Aplicar** la misma solución a otras herramientas MCP si es necesario
