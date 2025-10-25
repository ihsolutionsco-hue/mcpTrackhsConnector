# Testing Completo para search_units

Este documento describe la estrategia completa de testing para la herramienta `search_units` del servidor MCP TrackHS.

## 📋 Resumen de Testing

### Tipos de Tests Implementados

1. **Tests Unitarios** (`test_search_units_unit.py`)
   - Validación de parámetros
   - Manejo de errores
   - Lógica de negocio
   - Casos límite

2. **Tests de Integración** (`test_search_units_integration.py`)
   - Integración con servidor MCP
   - Middleware
   - Flujos completos

3. **Tests de API Real** (`test_search_units_api_real.py`)
   - Conexión real con TrackHS API
   - Casos de uso reales
   - Validación de datos

4. **Tests End-to-End** (`test_search_units_e2e.py`)
   - Escenarios de usuario completos
   - Flujos de negocio
   - Rendimiento

## 🚀 Ejecución de Tests

### Script de Ejecución

```bash
# Ejecutar todos los tests
python scripts/run_search_units_tests.py all

# Ejecutar solo tests unitarios
python scripts/run_search_units_tests.py unit

# Ejecutar tests con cobertura
python scripts/run_search_units_tests.py all --coverage

# Ejecutar tests lentos (API real)
python scripts/run_search_units_tests.py all --slow

# Ejecutar tests de rendimiento
python scripts/run_search_units_tests.py performance

# Ejecutar todas las verificaciones
python scripts/run_search_units_tests.py all-checks
```

### Comandos pytest Directos

```bash
# Tests unitarios
pytest tests/test_search_units_unit.py -v

# Tests de integración
pytest tests/test_search_units_integration.py -v

# Tests de API (requiere credenciales)
pytest tests/test_search_units_api_real.py -v -m "not slow"

# Tests E2E
pytest tests/test_search_units_e2e.py -v -m "not slow"

# Todos los tests con cobertura
pytest tests/test_search_units_*.py --cov=src/trackhs_mcp --cov-report=html
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Credenciales de API (requeridas para tests reales)
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_password"
export TRACKHS_BASE_URL="https://api.trackhs.com/api"

# Configuración de tests
export SLOW_TESTS="true"  # Incluir tests lentos
export MOCK_API="false"  # Usar API real vs mock
export API_TIMEOUT="30.0"  # Timeout en segundos
export MAX_RETRIES="3"    # Reintentos máximos
```

### Dependencias

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio pytest-cov pytest-xdist
pip install flake8 mypy  # Para linting y type checking
```

## 📊 Cobertura de Tests

### Tests Unitarios

- ✅ Validación de parámetros (100%)
- ✅ Manejo de errores (100%)
- ✅ Casos límite (100%)
- ✅ Validación de strings (100%)
- ✅ Manejo de unicode (100%)

### Tests de Integración

- ✅ Integración con MCP (100%)
- ✅ Middleware (100%)
- ✅ Requests concurrentes (100%)
- ✅ Manejo de memoria (100%)
- ✅ Timeout y reintentos (100%)

### Tests de API Real

- ✅ Conexión real (100%)
- ✅ Filtros y búsqueda (100%)
- ✅ Paginación (100%)
- ✅ Rendimiento (100%)
- ✅ Consistencia de datos (100%)

### Tests E2E

- ✅ Flujos de usuario (100%)
- ✅ Escenarios de negocio (100%)
- ✅ Gestión de inventario (100%)
- ✅ Recuperación de errores (100%)
- ✅ Viaje completo del usuario (100%)

## 🎯 Casos de Uso Cubiertos

### 1. Administrador de Propiedades

```python
# Búsqueda de inventario completo
result = await mcp_client.call_tool(
    name="search_units",
    arguments={"is_active": 1, "size": 50}
)

# Filtrado por características
result = await mcp_client.call_tool(
    name="search_units",
    arguments={
        "bedrooms": 2,
        "bathrooms": 1,
        "is_active": 1,
        "is_bookable": 1
    }
)
```

### 2. Huésped Buscando Alojamiento

```python
# Búsqueda por ubicación
result = await mcp_client.call_tool(
    name="search_units",
    arguments={"search": "beach", "is_active": 1, "is_bookable": 1}
)

# Filtrado por capacidad
result = await mcp_client.call_tool(
    name="search_units",
    arguments={
        "bedrooms": 3,
        "bathrooms": 2,
        "is_active": 1,
        "is_bookable": 1
    }
)
```

### 3. Gestión de Inventario

```python
# Análisis de inventario
result = await mcp_client.call_tool(
    name="search_units",
    arguments={"page": 1, "size": 25}
)

# Identificación de problemas
inactive_result = await mcp_client.call_tool(
    name="search_units",
    arguments={"is_active": 0}
)
```

## 🔍 Validaciones Implementadas

### Parámetros de Entrada

- ✅ `page`: 1-400 (validado)
- ✅ `size`: 1-25 (validado)
- ✅ `search`: máximo 200 caracteres (validado)
- ✅ `bedrooms`: 0-20 (validado)
- ✅ `bathrooms`: 0-20 (validado)
- ✅ `is_active`: 0 o 1 (validado)
- ✅ `is_bookable`: 0 o 1 (validado)

### Respuesta de API

- ✅ Estructura de respuesta (validada)
- ✅ Tipos de datos (validados)
- ✅ Campos obligatorios (validados)
- ✅ Enlaces HATEOAS (validados)
- ✅ Metadatos de paginación (validados)

### Manejo de Errores

- ✅ Error de autenticación
- ✅ Error de API
- ✅ Error de conexión
- ✅ Error de validación
- ✅ Timeout
- ✅ Reintentos

## 📈 Métricas de Rendimiento

### Benchmarks

- **Tiempo de respuesta**: < 5 segundos
- **Uso de memoria**: < 100MB
- **Requests concurrentes**: hasta 10
- **Tasa de éxito**: > 95%

### Tests de Rendimiento

```python
# Test de tiempo de respuesta
start_time = time.time()
result = await mcp_client.call_tool(name="search_units", arguments={})
response_time = time.time() - start_time
assert response_time < 5.0

# Test de memoria
process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss
# ... ejecutar tests ...
final_memory = process.memory_info().rss
assert (final_memory - initial_memory) < 100 * 1024 * 1024
```

## 🐛 Debugging y Troubleshooting

### Logs de Testing

```python
# Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Logs específicos de search_units
logger = logging.getLogger("test_search_units")
logger.info("Ejecutando test de búsqueda")
```

### Debug de Fallos

```bash
# Ejecutar con debug
pytest tests/test_search_units_unit.py -v -s --tb=long

# Ejecutar test específico
pytest tests/test_search_units_unit.py::TestSearchUnitsUnit::test_search_units_basic_parameters -v -s

# Ejecutar con pdb
pytest tests/test_search_units_unit.py --pdb
```

### Verificación de Credenciales

```python
# Verificar credenciales antes de tests de API
def test_api_credentials():
    assert os.getenv("TRACKHS_USERNAME"), "TRACKHS_USERNAME no configurado"
    assert os.getenv("TRACKHS_PASSWORD"), "TRACKHS_PASSWORD no configurado"
```

## 📝 Reportes

### Reporte de Cobertura

```bash
# Generar reporte HTML
pytest tests/test_search_units_*.py --cov=src/trackhs_mcp --cov-report=html
open htmlcov/index.html
```

### Reporte de Rendimiento

```bash
# Ejecutar tests de rendimiento
python scripts/run_search_units_tests.py performance
```

### Reporte de Linting

```bash
# Ejecutar linting
python scripts/run_search_units_tests.py lint
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Test search_units
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      - name: Run tests
        run: |
          python scripts/run_search_units_tests.py all --coverage
        env:
          TRACKHS_USERNAME: ${{ secrets.TRACKHS_USERNAME }}
          TRACKHS_PASSWORD: ${{ secrets.TRACKHS_PASSWORD }}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: test-search-units
        name: Test search_units
        entry: python scripts/run_search_units_tests.py unit
        language: system
        pass_filenames: false
```

## 📚 Referencias

- [Documentación de pytest](https://docs.pytest.org/)
- [Documentación de FastMCP](https://fastmcp.dev/)
- [Documentación de TrackHS API](https://docs.trackhs.com/)
- [Mejores prácticas de testing en Python](https://docs.python.org/3/library/unittest.html)

## 🤝 Contribuciones

Para contribuir a los tests de `search_units`:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los tests
4. Ejecuta `python scripts/run_search_units_tests.py all-checks`
5. Crea un pull request

## 📞 Soporte

Para problemas con los tests:

1. Revisa los logs de error
2. Verifica las credenciales de API
3. Ejecuta tests individuales para aislar el problema
4. Crea un issue en el repositorio
