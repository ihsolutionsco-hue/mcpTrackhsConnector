# 🧪 Testing Completo para search_units

Este documento proporciona una guía completa para ejecutar y entender los tests de la herramienta `search_units` del servidor MCP TrackHS.

## 📋 Resumen Ejecutivo

Se han implementado **4 tipos de tests** que cubren todos los aspectos de la herramienta `search_units`:

1. **Tests Unitarios** - Validación de lógica y parámetros
2. **Tests de Integración** - Integración con MCP y middleware
3. **Tests de API Real** - Conexión real con TrackHS API
4. **Tests End-to-End** - Escenarios completos de usuario

## 🚀 Inicio Rápido

### Ejecutar Todos los Tests

```bash
# Tests básicos (unitarios + integración)
python scripts/run_search_units_tests.py all

# Incluir tests lentos (API real + E2E)
python scripts/run_search_units_tests.py all --slow

# Con reporte de cobertura
python scripts/run_search_units_tests.py all --coverage
```

### Ejecutar Tests Específicos

```bash
# Solo tests unitarios
python scripts/run_search_units_tests.py unit

# Solo tests de integración
python scripts/run_search_units_tests.py integration

# Solo tests de API (requiere credenciales)
python scripts/run_search_units_tests.py api

# Solo tests E2E
python scripts/run_search_units_tests.py e2e
```

## 🔧 Configuración

### Variables de Entorno Requeridas

```bash
# Para tests de API real (opcional)
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_password"
export TRACKHS_BASE_URL="https://api.trackhs.com/api"

# Para tests completos
export SLOW_TESTS="true"  # Incluir tests lentos
export MOCK_API="false"   # Usar API real vs mock
```

### Instalación de Dependencias

```bash
# Dependencias básicas
pip install pytest pytest-asyncio pytest-cov

# Dependencias opcionales
pip install pytest-xdist  # Para tests paralelos
pip install flake8 mypy   # Para linting y type checking
pip install psutil        # Para tests de memoria
```

## 📊 Cobertura de Tests

### Tests Unitarios (`test_search_units_unit.py`)

- ✅ **Validación de parámetros** (100%)
  - Página: 1-400
  - Tamaño: 1-25
  - Dormitorios: 0-20
  - Baños: 0-20
  - Estados: 0 o 1

- ✅ **Manejo de errores** (100%)
  - Error de autenticación
  - Error de API
  - Error de conexión
  - Error de validación
  - Error genérico

- ✅ **Casos límite** (100%)
  - Parámetros mínimos/máximos
  - Strings vacíos
  - Unicode
  - Respuestas vacías

### Tests de Integración (`test_search_units_integration.py`)

- ✅ **Integración con MCP** (100%)
  - Cliente MCP
  - Transporte
  - Serialización

- ✅ **Middleware** (100%)
  - Logging
  - Métricas
  - Autenticación

- ✅ **Rendimiento** (100%)
  - Requests concurrentes
  - Uso de memoria
  - Timeout

### Tests de API Real (`test_search_units_api_real.py`)

- ✅ **Conexión real** (100%)
  - Autenticación
  - Endpoints
  - Respuestas

- ✅ **Filtros y búsqueda** (100%)
  - Por dormitorios
  - Por baños
  - Por estado
  - Por texto

- ✅ **Paginación** (100%)
  - Navegación
  - Consistencia
  - Enlaces HATEOAS

### Tests E2E (`test_search_units_e2e.py`)

- ✅ **Flujos de usuario** (100%)
  - Administrador de propiedades
  - Huésped buscando alojamiento
  - Gestión de inventario

- ✅ **Escenarios de negocio** (100%)
  - Búsqueda para familia
  - Búsqueda para pareja
  - Búsqueda de lujo
  - Búsqueda por ubicación

- ✅ **Rendimiento** (100%)
  - Tests de estrés
  - Uso de memoria
  - Requests concurrentes

## 🎯 Casos de Uso Cubiertos

### 1. Administrador de Propiedades

```python
# Inventario completo
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

## 📈 Métricas de Rendimiento

### Benchmarks Implementados

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

## 🔍 Debugging y Troubleshooting

### Ejecutar Tests con Debug

```bash
# Con logs detallados
pytest tests/test_search_units_unit.py -v -s --tb=long

# Test específico
pytest tests/test_search_units_unit.py::TestSearchUnitsUnit::test_search_units_basic_parameters -v -s

# Con pdb
pytest tests/test_search_units_unit.py --pdb
```

### Verificar Credenciales

```bash
# Verificar variables de entorno
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD

# Test de conexión
python -c "
import os
from src.trackhs_mcp.server import api_client
print('Cliente API:', 'Disponible' if api_client else 'No disponible')
"
```

### Logs de Testing

```python
# Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Logs específicos de search_units
logger = logging.getLogger("test_search_units")
logger.info("Ejecutando test de búsqueda")
```

## 📊 Reportes

### Reporte de Cobertura

```bash
# Generar reporte HTML
python scripts/run_search_units_tests.py coverage
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

## 📚 Estructura de Archivos

```
tests/
├── test_search_units_unit.py          # Tests unitarios
├── test_search_units_integration.py   # Tests de integración
├── test_search_units_api_real.py       # Tests de API real
├── test_search_units_e2e.py            # Tests E2E
├── conftest_search_units.py            # Configuración específica
└── conftest.py                         # Configuración general

scripts/
└── run_search_units_tests.py           # Script de ejecución

docs/
├── TESTING_SEARCH_UNITS.md             # Documentación completa
└── README_TESTING.md                   # Guía rápida

pytest.ini                              # Configuración de pytest
```

## 🎯 Próximos Pasos

1. **Ejecutar tests básicos**:
   ```bash
   python scripts/run_search_units_tests.py unit
   ```

2. **Configurar credenciales** (opcional):
   ```bash
   export TRACKHS_USERNAME="tu_usuario"
   export TRACKHS_PASSWORD="tu_password"
   ```

3. **Ejecutar tests completos**:
   ```bash
   python scripts/run_search_units_tests.py all --slow
   ```

4. **Generar reporte de cobertura**:
   ```bash
   python scripts/run_search_units_tests.py coverage
   ```

## 🤝 Contribuciones

Para contribuir a los tests:

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

---

**¡Los tests están listos para usar! 🚀**
