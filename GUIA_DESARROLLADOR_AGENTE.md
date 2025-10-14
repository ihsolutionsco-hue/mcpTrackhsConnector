# 🤖 Guía Fundamental para Desarrolladores Agentes - TrackHS MCP

## 📋 Índice
1. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
2. [Patrones de Desarrollo](#patrones-de-desarrollo)
3. [Testing Estratégico](#testing-estratégico)
4. [Errores Comunes y Soluciones](#errores-comunes-y-soluciones)
5. [Flujo de Trabajo Recomendado](#flujo-de-trabajo-recomendado)
6. [Comandos Esenciales](#comandos-esenciales)

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Capas
```
src/trackhs_mcp/
├── domain/           # Entidades de negocio y reglas
├── application/      # Casos de uso y lógica de aplicación
├── infrastructure/  # Adaptadores y herramientas MCP
└── main.py         # Punto de entrada
```

### Principios Clave
- **Clean Architecture**: Separación clara de responsabilidades
- **FastMCP**: Framework para herramientas MCP
- **Pydantic**: Validación de tipos y datos
- **Async/Await**: Programación asíncrona

---

## 🔧 Patrones de Desarrollo

### 1. **Creación de Herramientas MCP**

```python
# ✅ PATRÓN CORRECTO
@mcp.tool
async def mi_herramienta(
    param1: int,                    # Tipo específico
    param2: Optional[str] = None,   # Opcional con tipo claro
    param3: List[int] = []          # Lista con tipo específico
) -> dict:
    """Descripción clara de la herramienta"""
    try:
        # Lógica de negocio
        result = await use_case.execute(params)
        return result
    except Exception as e:
        # Manejo de errores con mensajes amigables
        raise TrackHSError(f"Error descriptivo: {str(e)}")
```

### 2. **Validación de Tipos**
```python
# ❌ EVITAR - Union types problemáticos
param: Union[int, str]

# ✅ USAR - Tipos específicos con coerción de Pydantic
param: int  # Pydantic convierte strings a int automáticamente
```

### 3. **Manejo de Errores**
```python
# ✅ PATRÓN RECOMENDADO
from src.trackhs_mcp.infrastructure.utils.user_friendly_messages import (
    format_date_error,
    format_type_error,
    format_required_error
)

try:
    # Lógica
    pass
except ValidationError as e:
    if "date" in str(e):
        raise TrackHSError(format_date_error("param_name"))
    elif "type" in str(e):
        raise TrackHSError(format_type_error("param_name", "int", value))
```

---

## 🧪 Testing Estratégico

### Jerarquía de Tests
1. **Unit Tests** - Componentes individuales
2. **Integration Tests** - Interacción entre capas
3. **E2E Tests** - Flujo completo del sistema

### Patrones de Testing

#### 1. **Mock Decorator Pattern** (CRÍTICO)
```python
# ✅ PATRÓN CORRECTO para capturar funciones registradas
@pytest.fixture
def tool_function(self, mock_mcp, api_client):
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

#### 2. **Mock Data Completo**
```python
# ✅ PROPORCIONAR DATOS COMPLETOS
def mock_get_side_effect(endpoint, **kwargs):
    if "reservations" in endpoint:
        return {
            "_embedded": {"reservations": [complete_reservation_data]},
            "page": 1, "total_items": 1
        }
    elif "folio" in endpoint:
        return complete_folio_data  # Objeto individual, no lista
```

#### 3. **Assertions Específicas**
```python
# ✅ ASERCIONES QUE MATCHEAN EL COMPORTAMIENTO REAL
assert mock_api_client.get.call_count == 2  # No 1 si se llama dos veces
assert result["status"] == "Confirmed,Checked In"  # Formato real
assert formatted_date == "2024-01-01T00:00:00Z"  # Formato real con timezone
```

---

## ⚠️ Errores Comunes y Soluciones

### 1. **IndexError: tuple index out of range**
```python
# ❌ PROBLEMA
tool_func = mock_mcp.tool.call_args[0][0]

# ✅ SOLUCIÓN
# Usar mock decorator pattern para capturar función directamente
```

### 2. **TypeError: '>' not supported between instances of 'str' and 'int'**
```python
# ❌ PROBLEMA
if page > 0:  # page puede ser string

# ✅ SOLUCIÓN
page_int = int(page) if isinstance(page, str) else page
if page_int > 0:
```

### 3. **ValidationError en tests E2E**
```python
# ❌ PROBLEMA
# Mock retorna lista cuando se espera objeto individual

# ✅ SOLUCIÓN
def mock_get_side_effect(endpoint, **kwargs):
    if "individual" in endpoint:
        return individual_object  # Objeto único
    else:
        return paginated_response  # Lista paginada
```

### 4. **ModuleNotFoundError**
```python
# ❌ PROBLEMA
# Importar módulos que ya no existen

# ✅ SOLUCIÓN
# Verificar que todos los imports sean válidos
# Eliminar referencias a módulos eliminados
```

---

## 🔄 Flujo de Trabajo Recomendado

### 1. **Antes de Empezar**
```bash
# Verificar estado del proyecto
python -m pytest tests/unit/ -v
python -m pytest tests/e2e/ -v
```

### 2. **Durante el Desarrollo**
```bash
# Tests específicos mientras desarrollas
python -m pytest tests/unit/mcp/test_mi_herramienta.py -v
python -m pytest tests/e2e/test_mi_herramienta_e2e.py -v
```

### 3. **Antes de Commit**
```bash
# Ejecutar todos los tests
python -m pytest tests/ -v --tb=short

# Verificar formato
black .
isort .
```

### 4. **Debugging de Tests**
```bash
# Tests con más detalle
python -m pytest tests/e2e/test_problema.py -v -s --tb=long

# Tests específicos
python -m pytest tests/e2e/test_tools_integration.py::TestToolsIntegrationE2E::test_register_both_tools_together -v
```

---

## 🛠️ Comandos Esenciales

### Testing
```bash
# Tests unitarios
python -m pytest tests/unit/ -v

# Tests E2E
python -m pytest tests/e2e/ -v

# Tests específicos
python -m pytest tests/e2e/test_tools_integration.py -v

# Tests con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Desarrollo
```bash
# Formatear código
black .
isort .

# Linting
flake8 src/
mypy src/

# Pre-commit hooks
pre-commit run --all-files
```

### Git
```bash
# Workflow estándar
git add .
git commit -m "DESCRIPCIÓN CLARA DE CAMBIOS"
git push
```

---

## 🎯 Mejores Prácticas

### 1. **Nomenclatura**
- Tests: `test_accion_condicion_resultado`
- Herramientas: `search_units`, `get_reservation_v2`
- Variables: `mock_api_client`, `registered_function`

### 2. **Documentación**
- Docstrings claros en herramientas MCP
- Comentarios en tests complejos
- README actualizado

### 3. **Manejo de Errores**
- Mensajes en español para usuarios
- Logging detallado para debugging
- Validación temprana de parámetros

### 4. **Performance**
- Tests rápidos (< 1 segundo por test)
- Mocks eficientes
- Datos de prueba realistas pero mínimos

---

## 🚨 Señales de Alerta

### En Tests
- `IndexError: tuple index out of range` → Usar mock decorator pattern
- `ValidationError` en E2E → Verificar mock data completo
- `TypeError` con comparaciones → Convertir tipos explícitamente
- `ModuleNotFoundError` → Verificar imports

### En Código
- `Union[int, str]` → Usar tipos específicos
- Mocks incompletos → Proporcionar datos realistas
- Tests lentos → Optimizar mocks y datos

---

## 📚 Recursos Adicionales

### Archivos Clave
- `src/trackhs_mcp/infrastructure/utils/user_friendly_messages.py` - Mensajes de error
- `tests/e2e/test_tools_integration.py` - Ejemplo de testing complejo
- `pytest.ini` - Configuración de tests

### Comandos de Debugging
```bash
# Ver logs detallados
python -m pytest tests/e2e/ -v -s --log-cli-level=DEBUG

# Tests con pdb
python -m pytest tests/e2e/test_problema.py -v -s --pdb
```

---

## 🎉 Conclusión

Esta guía cubre los patrones más importantes identificados durante el desarrollo del proyecto. Los desarrolladores agentes que sigan estos patrones podrán:

1. **Evitar errores comunes** ya identificados
2. **Escribir tests efectivos** desde el primer intento
3. **Debuggear problemas** rápidamente
4. **Mantener la calidad** del código

**Recuerda**: Siempre ejecutar tests después de cambios significativos y usar el mock decorator pattern para tests E2E.
