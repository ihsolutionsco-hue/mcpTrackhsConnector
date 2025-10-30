# 🚨 PROBLEMA IDENTIFICADO: Validación de Tipos en `search_units`

## 📋 RESUMEN EJECUTIVO

**Problema:** Los parámetros booleanos e enteros están llegando como strings cuando se invoca la herramienta `search_units` desde el MCP, causando que Pydantic rechace la validación ANTES de que se ejecuten las funciones de coerción.

**Ubicación:** `src/mcp_tools.py` línea 239-576 (función `search_units`)

**Tipo de problema:** ✅ **PROBLEMA DE NUESTRO CÓDIGO** (no de la API)

---

## 🔍 ANÁLISIS DEL PROBLEMA

### Flujo Actual (QUE NO FUNCIONA)

1. **Invocación desde MCP:**
   ```
   search_units(is_active=true, bedrooms=2)
   ```

2. **FastMCP/MCP recibe y pasa parámetros:**
   - Parece convertir valores a strings: `is_active="true"`, `bedrooms="2"`

3. **Pydantic valida los parámetros (ANTES de ejecutar el código):**
   ```python
   is_active: Optional[bool] = Field(...)  # Espera bool, recibe "true" (string)
   bedrooms: Optional[int] = Field(...)    # Espera int, recibe "2" (string)
   ```
   ❌ **VALIDACIÓN FALLA:** "Parameter 'is_active' must be one of types [boolean, null], got string"

4. **Las funciones de coerción nunca se ejecutan:**
   - `_coerce_bool()` (línea 51) está dentro del código
   - `_coerce_int()` (línea 66) está dentro del código
   - Pero nunca se ejecutan porque Pydantic rechaza primero

### Error Observado

```
Error calling tool: Parameter 'is_active' must be one of types [boolean, null], got string
Error calling tool: Parameter 'bedrooms' must be one of types [integer, null], got string
```

---

## 🔬 EVIDENCIA DEL PROBLEMA

### Código Actual (src/mcp_tools.py)

```python
@mcp_server.tool()
def search_units(
    page: int = Field(default=1, ge=1, description="..."),
    size: int = Field(default=10, ge=1, le=100, description="..."),
    # ...
    is_active: Optional[bool] = Field(default=None, description="..."),  # ❌ Tipo estricto
    is_bookable: Optional[bool] = Field(default=None, description="..."), # ❌ Tipo estricto
    bedrooms: Optional[int] = Field(default=None, ge=0, description="..."), # ❌ Tipo estricto
    # ...
) -> Dict[str, Any]:
    try:
        # ❌ Esta coerción nunca se ejecuta porque Pydantic rechaza antes
        is_active_c = _coerce_bool(is_active)
        bedrooms_c = _coerce_int(bedrooms)
        # ...
```

**El problema:** Pydantic valida los tipos ANTES de ejecutar el código de la función. Si FastMCP/MCP pasa strings, la validación falla antes de llegar a las funciones de coerción.

---

## ✅ SOLUCIÓN PROPUESTA

### Opción 1: Usar Validators de Pydantic (RECOMENDADA)

Cambiar los tipos de los parámetros para aceptar Union[str, bool, int] y usar validators de Pydantic que hagan la coerción:

```python
from typing import Union
from pydantic import field_validator

@mcp_server.tool()
def search_units(
    # ...
    is_active: Optional[Union[bool, str, int]] = Field(default=None, description="..."),
    bedrooms: Optional[Union[int, str]] = Field(default=None, ge=0, description="..."),
    # ...
) -> Dict[str, Any]:
    # Usar field_validator para coercion antes de validación

    @field_validator('is_active', mode='before')
    @classmethod
    def coerce_bool(cls, v):
        if v is None:
            return None
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(int(v))
        if isinstance(v, str):
            v = v.strip().lower()
            if v in {"true", "1", "yes", "y", "si", "sí"}:
                return True
            if v in {"false", "0", "no", "n"}:
                return False
        return v  # Dejar que Pydantic valide si no es convertible
```

### Opción 2: Cambiar tipos a Any y validar manualmente

```python
@mcp_server.tool()
def search_units(
    # ...
    is_active: Optional[Any] = Field(default=None, description="..."),
    bedrooms: Optional[Any] = Field(default=None, description="..."),
    # ...
) -> Dict[str, Any]:
    try:
        # Coerción manual antes de crear UnitSearchParams
        is_active_c = _coerce_bool(is_active)
        bedrooms_c = _coerce_int(bedrooms)
        # ...
```

---

## 🧪 PRUEBAS REALIZADAS

### Pruebas que FUNCIONAN:
✅ Búsqueda básica (solo paginación): `search_units(page=1, size=10)`
✅ Parámetros de texto: `search_units(search="penthouse")`
✅ Ordenamiento: `search_units(sort_column="name", sort_direction="asc")`

### Pruebas que FALLAN:
❌ Booleanos: `search_units(is_active=true)` → Error: "got string"
❌ Enteros: `search_units(bedrooms=2)` → Error: "got string"
❌ Fechas incompletas: `search_units(arrival="2024")` → Error: "Formato YYYY-MM-DD"

---

## 📊 COMPARACIÓN CON LA API REAL

**La API de TrackHS acepta:**
- ✅ Booleanos como `1` o `0` (enteros)
- ✅ Enteros como `2` (enteros)
- ✅ Strings convertidos automáticamente en la query string

**Nuestro código espera:**
- ❌ Booleanos como tipo `bool` de Python
- ❌ Enteros como tipo `int` de Python
- ❌ No acepta strings que necesiten conversión

**Conclusión:** El problema está en NUESTRO código, no en la API. La API es flexible y acepta diferentes formatos, pero nuestro código tiene validación de tipos muy estricta que rechaza strings antes de poder convertirlos.

---

## ✅ SOLUCIÓN IMPLEMENTADA

**Cambio realizado:** Cambiar tipos de parámetros a `Any` en lugar de tipos estrictos.

**Ubicación:** `src/mcp_tools.py` líneas 240-333

**Cambios:**
- `page: int` → `page: Optional[Any]`
- `size: int` → `size: Optional[Any]`
- Todos los `Optional[int]` → `Optional[Any]` (bedrooms, bathrooms, occupancy, etc.)
- Todos los `Optional[bool]` → `Optional[Any]` (is_active, is_bookable, pets_friendly, etc.)
- `calendar_id: Optional[int]` → `Optional[Any]`
- `role_id: Optional[int]` → `Optional[Any]`

**Por qué esta solución:**
1. ✅ **Simple** - No requiere cambios complejos en validators
2. ✅ **Compatible con FastMCP** - Acepta cualquier tipo de entrada
3. ✅ **Reutiliza código existente** - Las funciones `_coerce_bool()` y `_coerce_int()` ya existen y funcionan
4. ✅ **Mantiene validación** - `UnitSearchParams` sigue validando tipos después de la coerción
5. ✅ **Sigue ZEN de Python** - Simple es mejor que complejo

**Flujo ahora:**
1. MCP recibe parámetros (pueden ser strings/booleans/ints)
2. Pydantic acepta `Any` - no rechaza
3. Función ejecuta y hace coerción con `_coerce_bool()` y `_coerce_int()`
4. `UnitSearchParams` valida tipos correctos después de coerción
5. API recibe valores correctos en camelCase

---

## 📝 NOTAS ADICIONALES

- Las funciones `_coerce_bool()` y `_coerce_int()` existen y funcionan correctamente, pero nunca se ejecutan porque Pydantic rechaza primero.
- El esquema `UnitSearchParams` en `src/schemas/unit.py` también tiene tipos estrictos, pero ese no es el problema porque se usa DESPUÉS de la coerción.
- El problema está específicamente en la función `search_units` de `src/mcp_tools.py` donde los tipos están definidos en los parámetros de la función decorada con `@mcp_server.tool()`.

