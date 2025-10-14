# 🔬 Análisis Técnico: Causa Raíz y Solución de Validación de Tipos

**Fecha**: 14 de Octubre, 2025
**Analista**: Equipo de Desarrollo
**Basado en**: Informe de Testing Profesional de Usuario

---

## 📋 RESUMEN EJECUTIVO

### Problema Identificado
Dos issues críticos bloqueantes en producción causados por **incompatibilidad sistemática** entre tipos JSON-RPC (protocolo MCP) y type hints estrictos de Python (FastMCP).

### Impacto
- ❌ **1 herramienta completamente bloqueada**: `search_units` (100% inoperativa)
- ⚠️ **1 herramienta parcialmente afectada**: `search_reservations_v2` (parámetro `in_house_today` bloqueado)
- 📊 **20% de funcionalidad core afectada**

### Solución Propuesta
**Normalización de tipos flexible** en la capa de entrada de las herramientas MCP, permitiendo múltiples representaciones de tipos numéricos y booleanos según el estándar JSON-RPC.

---

## 🔍 ANÁLISIS DESDE LOS FUNDAMENTOS

### 1. Arquitectura del Sistema

```
┌─────────────┐         JSON-RPC          ┌──────────────┐
│   Cliente   │◄────────────────────────► │   Servidor   │
│   (Cursor)  │   MCP Protocol (JSON)     │   (FastMCP)  │
└─────────────┘                            └──────────────┘
                                                    │
                                                    ▼
                                           ┌────────────────┐
                                           │  Type Hints    │
                                           │  (Python int)  │
                                           └────────────────┘
                                                    │
                                                    ▼
                                           ┌────────────────┐
                                           │  Validación    │
                                           │  Estricta ❌   │
                                           └────────────────┘
```

**Problema**: La validación ocurre ANTES de que el código pueda normalizar los tipos.

### 2. Tipos JSON vs Python

| Tipo JSON | Tipo Python | FastMCP Espera | Cliente Envía |
|-----------|-------------|----------------|---------------|
| `number`  | `int`       | `int` ✅       | `number` ❌   |
| `number`  | `float`     | `float` ✅     | `number` ❌   |
| `true/false` | `bool`   | `bool` ✅      | `boolean` ❌  |

**Causa Raíz**:
- JSON tiene tipos **genéricos** (`number`)
- Python tiene tipos **específicos** (`int`, `float`)
- FastMCP valida contra **tipos específicos** de Python

### 3. Flujo del Problema

```python
# ❌ ESTADO ACTUAL

# 1. Cliente MCP (Cursor) envía:
{
  "method": "tools/call",
  "params": {
    "name": "search_units",
    "arguments": {
      "page": 1,          # ← Tipo JSON: "number"
      "size": 25          # ← Tipo JSON: "number"
    }
  }
}

# 2. FastMCP recibe y valida contra signature:
@mcp.tool(name="search_units")
async def search_units(
    page: int = 1,        # ← Espera tipo Python: "int"
    size: int = 25        # ← Espera tipo Python: "int"
):
    # Esta función NUNCA se ejecuta si la validación falla
    ...

# 3. FastMCP valida:
#    - Recibido: "number" (JSON)
#    - Esperado: "int" (Python)
#    - Resultado: ❌ "Parameter 'page' must be one of types [integer, string], got number"

# 4. La función search_units() NUNCA se ejecuta
#    - El código de normalización (líneas 166-167) NUNCA se alcanza
#    - La validación de negocio NUNCA se ejecuta
```

### 4. Evidencia del Código

#### Issue #1: `search_units`

**Archivo**: `src/trackhs_mcp/infrastructure/mcp/search_units.py`

```python
# Líneas 25-27: Signature estricta
@mcp.tool(name="search_units")
@error_handler("search_units")
async def search_units(
    page: int = 1,              # ← PROBLEMA: Type hint estricto
    size: int = 25,             # ← PROBLEMA: Type hint estricto
    ...
):
    # Líneas 166-167: Normalización que NUNCA se ejecuta
    page_int = int(page) if isinstance(page, str) else page
    size_int = int(size) if isinstance(size, str) else size
    # ↑ Este código es correcto pero INACCESIBLE
```

**Error resultante**:
```
Parameter 'page' must be one of types [integer, string], got number
```

#### Issue #2: `search_reservations_v2` - Parámetro `in_house_today`

**Archivo**: `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`

```python
# Línea 60: Signature con Literal estricto
@mcp.tool(name="search_reservations")
@error_handler("search_reservations")
async def search_reservations_v2(
    page: int = 1,                           # ← Funciona (FastMCP lo normaliza)
    size: int = 10,                          # ← Funciona (FastMCP lo normaliza)
    ...
    in_house_today: Optional[Literal[0, 1]] = None,  # ← PROBLEMA: Literal estricto
    ...
):
    # La función se ejecuta para page/size pero FALLA para in_house_today
```

**Error resultante**:
```
Parameter 'in_house_today' must be one of types [integer, null], got number
```

### 5. ¿Por Qué Algunos Parámetros Funcionan y Otros No?

**Observación clave del testing**:
- ✅ `search_reservations_v2(page=1, size=10)` → **FUNCIONA**
- ❌ `search_reservations_v2(in_house_today=1)` → **FALLA**
- ❌ `search_units(page=1)` → **FALLA**

**Explicación**:

```python
# FastMCP tiene lógica de normalización INTERNA para tipos básicos
# pero NO para todos los casos

# CASO 1: page/size en search_reservations_v2 ✅
# FastMCP detecta: "Esta herramienta ya funcionó antes"
# FastMCP aplica: Normalización interna automática
# Resultado: FUNCIONA

# CASO 2: in_house_today con Literal[0, 1] ❌
# FastMCP detecta: "Literal estricto"
# FastMCP NO aplica: Normalización automática (requiere valor exacto)
# Resultado: FALLA

# CASO 3: page/size en search_units ❌
# FastMCP detecta: "Primera llamada a esta herramienta"
# FastMCP aplica: Validación estricta inicial
# Resultado: FALLA
```

**Hipótesis**: FastMCP tiene comportamiento inconsistente en la normalización automática dependiendo de:
1. Si la herramienta ha sido llamada antes (caché de normalización)
2. El tipo de annotation (Optional[int] vs Optional[Literal[0, 1]])
3. La versión de FastMCP (>= 2.0.0)

---

## 🛠️ SOLUCIÓN ARQUITECTÓNICA

### Opción 1: Normalización en Type Hints (RECOMENDADA)

**Ventajas**:
- ✅ Solución limpia y declarativa
- ✅ Compatible con FastMCP
- ✅ No requiere middleware adicional
- ✅ Fácil de mantener

**Implementación**:

```python
from typing import Union, Optional

# ANTES ❌
async def search_units(
    page: int = 1,
    size: int = 25,
    pets_friendly: Optional[int] = None,
):
    # Código nunca alcanzado si tipos no coinciden
    page_int = int(page) if isinstance(page, str) else page
    ...

# DESPUÉS ✅
async def search_units(
    page: Union[int, float, str] = 1,           # Acepta múltiples tipos
    size: Union[int, float, str] = 25,          # Acepta múltiples tipos
    pets_friendly: Optional[Union[int, float, str]] = None,  # Acepta múltiples tipos
):
    # Normalización garantizada de ejecutarse
    page_int = _normalize_int(page, "page")     # Helper de normalización
    size_int = _normalize_int(size, "size")     # Helper de normalización
    pets_friendly_int = _normalize_int(pets_friendly, "pets_friendly") if pets_friendly is not None else None
    ...

# Helper de normalización (crear en src/trackhs_mcp/infrastructure/utils/type_normalization.py)
def _normalize_int(value: Union[int, float, str], param_name: str) -> int:
    """
    Normaliza un valor a int desde múltiples representaciones.

    Soporta:
    - int → int (directo)
    - float → int (conversión)
    - str → int (parsing)
    - JSON number → int (desde FastMCP)

    Raises:
        ValidationError: Si el valor no puede convertirse a int
    """
    if isinstance(value, int):
        return value

    if isinstance(value, float):
        # Validar que no tiene decimales significativos
        if value.is_integer():
            return int(value)
        raise ValidationError(f"{param_name} must be an integer, got float with decimals: {value}", param_name)

    if isinstance(value, str):
        try:
            # Intentar parsear como int
            return int(value)
        except ValueError:
            raise ValidationError(f"{param_name} must be a valid integer string, got: {value}", param_name)

    # Tipo no soportado
    raise ValidationError(f"{param_name} must be int, float, or str, got: {type(value).__name__}", param_name)
```

### Opción 2: Decorador de Normalización

**Ventajas**:
- ✅ Centraliza la lógica de normalización
- ✅ Reutilizable en todas las herramientas
- ✅ Separa concerns (normalización vs lógica de negocio)

**Desventajas**:
- ⚠️ Más complejo de implementar
- ⚠️ Puede interferir con decoradores existentes (@mcp.tool, @error_handler)

**Implementación**:

```python
from functools import wraps
from typing import get_type_hints
import inspect

def normalize_mcp_params(func):
    """
    Decorador que normaliza parámetros MCP antes de ejecutar la función.

    Convierte:
    - JSON "number" → Python int/float
    - Strings numéricos → int/float
    - Valida tipos según type hints
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Obtener type hints de la función
        hints = get_type_hints(func)

        # Normalizar cada parámetro
        normalized_kwargs = {}
        for param_name, param_value in kwargs.items():
            if param_name not in hints:
                # Parámetro sin type hint, mantener original
                normalized_kwargs[param_name] = param_value
                continue

            expected_type = hints[param_name]

            # Normalizar según tipo esperado
            if expected_type == int or _is_optional_int(expected_type):
                normalized_kwargs[param_name] = _normalize_int(param_value, param_name)
            elif expected_type == bool or _is_optional_bool(expected_type):
                normalized_kwargs[param_name] = _normalize_bool(param_value, param_name)
            else:
                # Mantener original
                normalized_kwargs[param_name] = param_value

        # Ejecutar función con parámetros normalizados
        return await func(*args, **normalized_kwargs)

    return wrapper

# Uso:
@mcp.tool(name="search_units")
@normalize_mcp_params  # ← Decorador de normalización
@error_handler("search_units")
async def search_units(
    page: int = 1,
    size: int = 25,
    ...
):
    # Aquí page y size YA están normalizados a int
    ...
```

### Opción 3: Middleware Global en FastMCP

**Ventajas**:
- ✅ Solución única para todas las herramientas
- ✅ No requiere cambios en cada herramienta individual
- ✅ Más mantenible a largo plazo

**Desventajas**:
- ⚠️ Requiere modificar el registro de herramientas en `server.py`
- ⚠️ Puede afectar el rendimiento si no se optimiza

**Implementación**:

```python
# src/trackhs_mcp/infrastructure/mcp/server.py

from ..utils.type_normalization import create_normalizing_wrapper

def register_all_components(mcp, api_client: "ApiClientPort"):
    """Registra todos los componentes del servidor MCP con normalización de tipos"""
    from .all_tools import register_all_tools
    from .prompts import register_all_prompts
    from .resources import register_all_resources

    # Wrapper de normalización para todas las herramientas
    original_tool_decorator = mcp.tool

    def normalizing_tool_decorator(*decorator_args, **decorator_kwargs):
        """Decorador que envuelve las herramientas con normalización automática"""
        def decorator(func):
            # Aplicar normalización ANTES del decorador original
            normalized_func = create_normalizing_wrapper(func)
            # Aplicar decorador original de FastMCP
            return original_tool_decorator(*decorator_args, **decorator_kwargs)(normalized_func)
        return decorator

    # Reemplazar mcp.tool con versión normalizada
    mcp.tool = normalizing_tool_decorator

    # Registrar herramientas (ahora con normalización automática)
    register_all_tools(mcp, api_client)

    # Registrar resources y prompts
    register_all_resources(mcp, api_client)
    register_all_prompts(mcp, api_client)
```

---

## 🎯 PLAN DE IMPLEMENTACIÓN RECOMENDADO

### Fase 1: Solución Inmediata (1-2 horas)

**Objetivo**: Desbloquear las herramientas críticas

**Acción**:
1. Modificar type hints de `search_units` para aceptar `Union[int, float, str]`
2. Modificar type hint de `in_house_today` para aceptar `Optional[Union[int, float, str]]`
3. Asegurar que la normalización interna se ejecute correctamente

**Archivos a modificar**:
- `src/trackhs_mcp/infrastructure/mcp/search_units.py`
- `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py`

**Testing inmediato**:
```python
# Casos de prueba críticos
test_search_units(page=1, size=25)              # ← Debe funcionar
test_search_units(page=1.0, size=25.0)          # ← Debe funcionar
test_search_units(page="1", size="25")          # ← Debe funcionar

test_search_reservations_v2(in_house_today=1)   # ← Debe funcionar
test_search_reservations_v2(in_house_today=0)   # ← Debe funcionar
```

### Fase 2: Refactorización (2-3 horas)

**Objetivo**: Crear solución sostenible y reutilizable

**Acción**:
1. Crear módulo `src/trackhs_mcp/infrastructure/utils/type_normalization.py`
2. Implementar helpers de normalización:
   - `_normalize_int(value, param_name)`
   - `_normalize_bool(value, param_name)`
   - `_normalize_float(value, param_name)`
3. Refactorizar todas las herramientas para usar helpers
4. Documentar patrones de uso

**Estructura del módulo**:
```python
# src/trackhs_mcp/infrastructure/utils/type_normalization.py

from typing import Union, Optional
from ...domain.exceptions.api_exceptions import ValidationError

def normalize_int(value: Optional[Union[int, float, str]], param_name: str) -> Optional[int]:
    """Normaliza valor a int, soporta None"""
    if value is None:
        return None
    return _normalize_int_required(value, param_name)

def _normalize_int_required(value: Union[int, float, str], param_name: str) -> int:
    """Normaliza valor a int, NO soporta None"""
    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValidationError(f"{param_name} must be an integer, got float with decimals: {value}", param_name)

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise ValidationError(f"{param_name} must be a valid integer string, got: {value}", param_name)

    raise ValidationError(f"{param_name} must be int, float, or str, got: {type(value).__name__}", param_name)

def normalize_bool(value: Optional[Union[bool, int, str]], param_name: str) -> Optional[bool]:
    """Normaliza valor a bool"""
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value != 0

    if isinstance(value, str):
        lower = value.lower()
        if lower in ('true', '1', 'yes'):
            return True
        if lower in ('false', '0', 'no'):
            return False
        raise ValidationError(f"{param_name} must be a valid boolean string, got: {value}", param_name)

    raise ValidationError(f"{param_name} must be bool, int, or str, got: {type(value).__name__}", param_name)

def normalize_binary_int(value: Optional[Union[int, float, str]], param_name: str) -> Optional[int]:
    """
    Normaliza valor a 0 o 1 (para flags booleanos representados como int).
    Común en APIs que usan 0/1 en lugar de true/false.
    """
    if value is None:
        return None

    # Normalizar a int primero
    int_value = _normalize_int_required(value, param_name)

    # Validar que sea 0 o 1
    if int_value not in [0, 1]:
        raise ValidationError(f"{param_name} must be 0 or 1, got: {int_value}", param_name)

    return int_value
```

### Fase 3: Testing Completo (1-2 horas)

**Objetivo**: Validar que la solución no rompe nada y soluciona los issues

**Acción**:
1. Re-ejecutar testing completo de `search_units` (9 casos planificados)
2. Re-ejecutar testing de `in_house_today` en `search_reservations_v2`
3. Ejecutar tests de regresión en herramientas que funcionan
4. Validar casos edge:
   - Valores negativos
   - Valores muy grandes
   - Strings vacíos
   - Tipos incorrectos (arrays, objetos)

**Suite de tests**:
```python
# tests/test_type_normalization.py

import pytest
from src.trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_int,
    normalize_bool,
    normalize_binary_int
)
from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

class TestNormalizeInt:
    def test_int_passthrough(self):
        assert normalize_int(42, "test") == 42

    def test_float_to_int(self):
        assert normalize_int(42.0, "test") == 42

    def test_float_with_decimals_raises(self):
        with pytest.raises(ValidationError):
            normalize_int(42.5, "test")

    def test_string_to_int(self):
        assert normalize_int("42", "test") == 42

    def test_invalid_string_raises(self):
        with pytest.raises(ValidationError):
            normalize_int("not_a_number", "test")

    def test_none_returns_none(self):
        assert normalize_int(None, "test") is None

class TestNormalizeBinaryInt:
    def test_zero_and_one(self):
        assert normalize_binary_int(0, "test") == 0
        assert normalize_binary_int(1, "test") == 1

    def test_invalid_values_raise(self):
        with pytest.raises(ValidationError):
            normalize_binary_int(2, "test")

        with pytest.raises(ValidationError):
            normalize_binary_int(-1, "test")

    def test_string_conversion(self):
        assert normalize_binary_int("0", "test") == 0
        assert normalize_binary_int("1", "test") == 1
```

### Fase 4: Documentación y Prevención (30 min)

**Objetivo**: Prevenir que el problema se repita

**Acción**:
1. Documentar patrón de normalización en guía de desarrollo
2. Crear plantilla para nuevas herramientas MCP
3. Agregar lint/test que detecte type hints estrictos sin normalización

**Documentación**:
```markdown
# Guía de Desarrollo: Type Hints en Herramientas MCP

## ⚠️ IMPORTANTE: Normalización de Tipos

Las herramientas MCP reciben parámetros vía JSON-RPC, que usa tipos genéricos (number, boolean).
Python usa tipos específicos (int, float, bool).

### ✅ Patrón Correcto

```python
from typing import Union, Optional
from ...infrastructure.utils.type_normalization import normalize_int, normalize_binary_int

@mcp.tool(name="my_tool")
async def my_tool(
    page: Union[int, float, str] = 1,           # ← Acepta múltiples tipos
    size: Union[int, float, str] = 10,          # ← Acepta múltiples tipos
    is_active: Optional[Union[int, float, str]] = None,  # ← Acepta múltiples tipos
):
    # Normalizar INMEDIATAMENTE
    page = normalize_int(page, "page")
    size = normalize_int(size, "size")
    is_active = normalize_binary_int(is_active, "is_active") if is_active is not None else None

    # Ahora usar valores normalizados
    ...
```

### ❌ Antipatrón

```python
# NO HACER ESTO
@mcp.tool(name="my_tool")
async def my_tool(
    page: int = 1,                     # ← Rechazará JSON "number"
    is_active: Optional[Literal[0, 1]] = None,  # ← Rechazará JSON "number"
):
    # Esta función NUNCA se ejecutará si el cliente envía tipos JSON
    ...
```
```

---

## 📊 MÉTRICAS DE ÉXITO

### Pre-Fix
- ❌ `search_units`: 0% funcional
- ⚠️ `search_reservations_v2`: 90% funcional (1 parámetro bloqueado)
- ✅ Otras herramientas: 100% funcionales

### Post-Fix Esperado
- ✅ `search_units`: 100% funcional
- ✅ `search_reservations_v2`: 100% funcional
- ✅ Otras herramientas: 100% funcionales (sin regresión)

### Tests de Validación
```python
# Suite mínima de validación post-fix
def validate_fix():
    # Issue #1: search_units
    assert search_units(page=1, size=25) == SUCCESS
    assert search_units(page=1.0, size=25.0) == SUCCESS
    assert search_units(page="1", size="25") == SUCCESS

    # Issue #2: in_house_today
    assert search_reservations_v2(in_house_today=1) == SUCCESS
    assert search_reservations_v2(in_house_today=0) == SUCCESS

    # Regresión: herramientas que funcionaban
    assert search_reservations_v2(page=1, size=10) == SUCCESS
    assert get_reservation_v2(reservation_id="1") == SUCCESS
    assert get_folio(folio_id="1") == SUCCESS

    print("✅ Todas las validaciones pasaron")
```

---

## 🚦 CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Fix Inmediato
- [ ] Modificar `search_units.py` - cambiar type hints a `Union[int, float, str]`
- [ ] Modificar `search_reservations_v2.py` - cambiar `in_house_today` a `Optional[Union[int, float, str]]`
- [ ] Probar manualmente los 2 casos críticos
- [ ] Commit: "fix: Allow flexible types in search_units and in_house_today"

### Fase 2: Refactorización
- [ ] Crear `type_normalization.py` con helpers
- [ ] Implementar `normalize_int()`
- [ ] Implementar `normalize_bool()`
- [ ] Implementar `normalize_binary_int()`
- [ ] Refactorizar `search_units.py` para usar helpers
- [ ] Refactorizar `search_reservations_v2.py` para usar helpers
- [ ] Commit: "refactor: Add type normalization utilities"

### Fase 3: Testing
- [ ] Crear `tests/test_type_normalization.py`
- [ ] Implementar tests unitarios de normalización
- [ ] Re-ejecutar testing completo de `search_units`
- [ ] Re-ejecutar testing de `in_house_today`
- [ ] Ejecutar tests de regresión
- [ ] Commit: "test: Add comprehensive type normalization tests"

### Fase 4: Documentación
- [ ] Documentar patrón en guía de desarrollo
- [ ] Crear plantilla para nuevas herramientas
- [ ] Actualizar CHANGELOG.md
- [ ] Commit: "docs: Add type normalization guidelines"

---

## 🔬 APRENDIZAJES Y PREVENCIÓN

### Lecciones Aprendidas

1. **Type hints estrictos en contextos JSON-RPC son problemáticos**
   - JSON tiene tipos genéricos
   - Python tiene tipos específicos
   - La conversión NO es automática en FastMCP

2. **La validación de FastMCP ocurre ANTES del código de la función**
   - Los helpers de normalización dentro de la función son inútiles si la validación falla
   - La normalización debe ocurrir en type hints o decoradores

3. **FastMCP tiene comportamiento inconsistente**
   - Algunos parámetros se normalizan automáticamente
   - Otros fallan con error de tipo
   - Literal types son especialmente problemáticos

### Prevención Futura

1. **Code Review Checklist**
   - [ ] ¿La herramienta usa type hints estrictos (`int`, `bool`, `Literal`)?
   - [ ] ¿La herramienta normaliza parámetros antes de usarlos?
   - [ ] ¿Los tests incluyen casos con diferentes tipos de entrada?

2. **Lint Rules**
   ```python
   # Crear regla de lint que detecte:
   # - @mcp.tool con parámetros int sin Union
   # - @mcp.tool con parámetros Literal sin Union
   ```

3. **Template de Herramienta MCP**
   ```python
   # Plantilla estándar para nuevas herramientas
   from typing import Union, Optional
   from ...infrastructure.utils.type_normalization import normalize_int

   @mcp.tool(name="new_tool")
   async def new_tool(
       param1: Union[int, float, str] = DEFAULT,  # ← Siempre Union
       param2: Optional[Union[int, float, str]] = None,  # ← Optional + Union
   ):
       # Normalizar PRIMERO
       param1 = normalize_int(param1, "param1")
       param2 = normalize_int(param2, "param2") if param2 is not None else None

       # Luego validar lógica de negocio
       if param1 < 0:
           raise ValidationError("param1 must be >= 0", "param1")

       # Finalmente ejecutar lógica
       ...
   ```

---

## 📚 REFERENCIAS

### Documentación Técnica
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)

### Archivos Relacionados
- `INFORME_DESARROLLADOR.md` - Informe de testing original
- `CASOS_PRUEBA_EJECUTADOS.md` - Evidencia de los tests
- `src/trackhs_mcp/infrastructure/mcp/search_units.py` - Issue #1
- `src/trackhs_mcp/infrastructure/mcp/search_reservations_v2.py` - Issue #2

---

**Preparado por**: Equipo de Desarrollo
**Aprobado por**: Pendiente
**Fecha de próxima revisión**: Post-implementación de la solución

