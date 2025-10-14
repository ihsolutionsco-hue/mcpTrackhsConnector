# 🧪 Patrones de Testing Críticos - TrackHS MCP

## 🎯 Patrones Identificados Durante el Desarrollo

### 1. **Mock Decorator Pattern** (MÁS CRÍTICO)

**Problema**: `IndexError: tuple index out of range` al acceder a `mock_mcp.tool.call_args[0][0]`

**Causa**: El decorador `@mcp.tool` pasa argumentos por nombre, no por posición

**Solución**:
```python
@pytest.fixture
def tool_function(self, mock_mcp, api_client):
    """Captura la función registrada correctamente"""
    registered_function = None

    def mock_tool_decorator(name=None):
        def decorator(func):
            nonlocal registered_function
            registered_function = func
            return func
        return decorator

    mock_mcp.tool = mock_tool_decorator
    register_my_tool(mock_mcp, api_client)
    return registered_function
```

**Aplicación**: Usar en TODOS los tests E2E que registran herramientas MCP

---

### 2. **Mock Data Completo Pattern**

**Problema**: `ValidationError` en tests E2E por datos incompletos

**Causa**: Mocks retornan listas cuando se esperan objetos individuales

**Solución**:
```python
def mock_get_side_effect(endpoint, **kwargs):
    """Retorna datos apropiados según el endpoint"""
    if "reservations" in endpoint:
        return {
            "_embedded": {"reservations": [complete_reservation_data]},
            "page": 1, "total_items": 1
        }
    elif "folio" in endpoint:
        return complete_folio_data  # Objeto individual
    elif "reservation" in endpoint and "individual" in endpoint:
        return individual_reservation_data  # Objeto individual
```

**Aplicación**:
- Endpoints de búsqueda → Datos paginados
- Endpoints individuales → Objetos únicos

---

### 3. **Type Conversion Pattern**

**Problema**: `TypeError: '>' not supported between instances of 'str' and 'int'`

**Causa**: Parámetros pueden llegar como string pero se comparan como int

**Solución**:
```python
# En herramientas MCP
page_int = int(page) if isinstance(page, str) else page
if page_int > 0:
    adjusted_page = max(0, page_int - 1)

# En casos de uso
if params.page:
    page_int = int(params.page) if isinstance(params.page, str) else params.page
    adjusted_page = max(0, page_int - 1) if page_int > 0 else 0
```

**Aplicación**: Siempre convertir tipos antes de comparaciones

---

### 4. **Call Count Assertion Pattern**

**Problema**: `AssertionError: assert 2 == 1` en call_count

**Causa**: Tests llaman la misma herramienta múltiples veces

**Solución**:
```python
# ✅ CORRECTO - Verificar el número real de llamadas
assert mock_api_client.get.call_count == 2  # Si se llama 2 veces

# ❌ INCORRECTO - Asumir número incorrecto
assert mock_api_client.get.call_count == 1  # Si realmente se llama 2 veces
```

**Aplicación**: Contar las llamadas reales, no asumir

---

### 5. **Date Format Assertion Pattern**

**Problema**: `AssertionError: assert '2024-01-01' == '2024-01-01T00:00:00Z'`

**Causa**: Formatos de fecha reales incluyen timezone

**Solución**:
```python
# ✅ CORRECTO - Usar formato real
assert formatted_date == "2024-01-01T00:00:00Z"

# ❌ INCORRECTO - Asumir formato simplificado
assert formatted_date == "2024-01-01"
```

**Aplicación**: Verificar formatos reales, no asumir formatos simplificados

---

### 6. **Variable Reference Pattern**

**Problema**: `NameError: name 'v2_call' is not defined`

**Causa**: Variables no definidas en tests complejos

**Solución**:
```python
# ✅ CORRECTO - Definir todas las variables
v2_call_1 = mock_api_client.get.call_args_list[0]
v2_call_2 = mock_api_client.get.call_args_list[1]

# Usar variables definidas
v1_params = v2_call_1[1]["params"]
v2_params = v2_call_2[1]["params"]

# ❌ INCORRECTO - Usar variables no definidas
v1_params = v2_call[1]["params"]  # v2_call no existe
```

**Aplicación**: Definir todas las variables antes de usarlas

---

### 7. **Error Message Pattern**

**Problema**: `AssertionError: Regex pattern did not match`

**Causa**: Patrones regex no coinciden con mensajes reales

**Solución**:
```python
# ✅ CORRECTO - Usar mensajes reales
with pytest.raises(TrackHSError, match="Size must be >= 1"):

# ❌ INCORRECTO - Usar mensajes asumidos
with pytest.raises(TrackHSError, match="Size debe estar entre 1 y 100"):
```

**Aplicación**: Verificar mensajes reales, no asumir

---

### 8. **Import Cleanup Pattern**

**Problema**: `ModuleNotFoundError: No module named 'search_reservations_v1'`

**Causa**: Imports de módulos eliminados

**Solución**:
```python
# ✅ CORRECTO - Verificar imports válidos
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import register_search_reservations_v2

# ❌ INCORRECTO - Importar módulos eliminados
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import register_search_reservations_v1
```

**Aplicación**: Limpiar imports después de eliminar módulos

---

## 🔧 Herramientas de Debugging

### 1. **Test Debugging Commands**
```bash
# Test específico con detalle
python -m pytest tests/e2e/test_problema.py::TestClass::test_method -v -s --tb=long

# Test con pdb
python -m pytest tests/e2e/test_problema.py -v -s --pdb

# Test con logs
python -m pytest tests/e2e/test_problema.py -v -s --log-cli-level=DEBUG
```

### 2. **Mock Inspection**
```python
# Inspeccionar llamadas a mocks
print(f"Call count: {mock_api_client.get.call_count}")
print(f"Call args: {mock_api_client.get.call_args_list}")

# Verificar función registrada
print(f"Registered function: {tool_function}")
print(f"Function name: {tool_function.__name__}")
```

### 3. **Data Validation**
```python
# Validar datos de mock
def validate_mock_data(data):
    if isinstance(data, list):
        print("❌ Data is list, expected object")
    elif isinstance(data, dict):
        print("✅ Data is object")
        print(f"Keys: {list(data.keys())}")
```

---

## 📋 Checklist de Testing

### Antes de Escribir Tests
- [ ] ¿Entiendo qué hace la herramienta?
- [ ] ¿Tengo datos de mock realistas?
- [ ] ¿Sé qué formato de respuesta esperar?

### Durante el Desarrollo
- [ ] ¿Uso mock decorator pattern?
- [ ] ¿Los datos de mock son completos?
- [ ] ¿Las aserciones matchean el comportamiento real?
- [ ] ¿Manejo todos los casos de error?

### Antes de Commit
- [ ] ¿Todos los tests pasan?
- [ ] ¿No hay imports rotos?
- [ ] ¿Los mensajes de error son claros?
- [ ] ¿El código está formateado?

---

## 🎯 Patrones por Tipo de Test

### Unit Tests
- Mock dependencies
- Test individual components
- Fast execution
- Clear assertions

### Integration Tests
- Test layer interactions
- Real data flow
- Error propagation
- Type consistency

### E2E Tests
- Full workflow
- Mock decorator pattern
- Complete mock data
- Real user scenarios

---

## 🚨 Red Flags

### En Tests
- `IndexError` → Mock decorator pattern
- `ValidationError` → Mock data completo
- `TypeError` → Type conversion
- `NameError` → Variable definition
- `ModuleNotFoundError` → Import cleanup

### En Código
- `Union[int, str]` → Use specific types
- Complex mock setup → Simplify
- Slow tests → Optimize mocks
- Flaky tests → Stable data

---

## 🎉 Conclusión

Estos patrones fueron identificados durante la resolución de problemas reales en el proyecto. Seguir estos patrones evitará los errores más comunes y acelerará el desarrollo.

**Regla de Oro**: Siempre usar mock decorator pattern para tests E2E y proporcionar datos de mock completos y realistas.
