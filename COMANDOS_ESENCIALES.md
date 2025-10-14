# 🛠️ Comandos Esenciales - TrackHS MCP

## 🚀 Comandos de Desarrollo Rápido

### Testing
```bash
# Tests unitarios (rápido)
python -m pytest tests/unit/ -v

# Tests E2E (completo)
python -m pytest tests/e2e/ -v

# Tests específicos
python -m pytest tests/e2e/test_tools_integration.py -v

# Tests con debugging
python -m pytest tests/e2e/test_problema.py -v -s --tb=long

# Tests con pdb
python -m pytest tests/e2e/test_problema.py -v -s --pdb
```

### Formateo y Linting
```bash
# Formatear código
black .

# Ordenar imports
isort .

# Linting
flake8 src/

# Type checking
mypy src/

# Pre-commit hooks
pre-commit run --all-files
```

### Git Workflow
```bash
# Workflow estándar
git add .
git commit -m "DESCRIPCIÓN CLARA"
git push

# Ver estado
git status
git log --oneline -5
```

---

## 🔍 Comandos de Debugging

### Tests Específicos
```bash
# Test individual con detalle
python -m pytest tests/e2e/test_tools_integration.py::TestToolsIntegrationE2E::test_register_both_tools_together -v -s

# Test con logs
python -m pytest tests/e2e/test_problema.py -v -s --log-cli-level=DEBUG

# Test con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Debugging de Mocks
```python
# Inspeccionar mocks en tests
print(f"Call count: {mock_api_client.get.call_count}")
print(f"Call args: {mock_api_client.get.call_args_list}")
print(f"Registered function: {tool_function}")
```

### Validación de Datos
```python
# Validar estructura de datos
def debug_data(data, name="data"):
    print(f"{name} type: {type(data)}")
    if isinstance(data, dict):
        print(f"{name} keys: {list(data.keys())}")
    elif isinstance(data, list):
        print(f"{name} length: {len(data)}")
        if data:
            print(f"{name}[0] type: {type(data[0])}")
```

---

## 🧪 Scripts de Testing

### Test Individual
```bash
# Test específico
python -m pytest tests/e2e/test_search_units_e2e.py::TestSearchUnitsE2E::test_e2e_basic_search -v

# Test con más detalle
python -m pytest tests/e2e/test_search_units_e2e.py::TestSearchUnitsE2E::test_e2e_basic_search -v -s --tb=long
```

### Test de Integración
```bash
# Tests de integración
python -m pytest tests/integration/ -v

# Test específico de integración
python -m pytest tests/integration/test_search_units.py -v
```

### Test de Regresión
```bash
# Tests de regresión
python -m pytest tests/e2e/test_regression_post_fix.py -v

# Test específico de regresión
python -m pytest tests/e2e/test_regression_post_fix.py::TestRegressionPostFix::test_phase_2_search_units_fixed -v
```

---

## 🔧 Comandos de Desarrollo

### Setup del Proyecto
```bash
# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Validación Pre-commit
```bash
# Ejecutar todos los hooks
pre-commit run --all-files

# Hook específico
pre-commit run black
pre-commit run isort
pre-commit run flake8
```

### Coverage
```bash
# Coverage completo
python -m pytest tests/ --cov=src --cov-report=html

# Coverage específico
python -m pytest tests/unit/ --cov=src --cov-report=html

# Ver reporte
# Abrir htmlcov/index.html en navegador
```

---

## 🚨 Comandos de Troubleshooting

### Problemas Comunes
```bash
# IndexError en tests
python -m pytest tests/e2e/test_problema.py -v -s --tb=long

# ValidationError en E2E
python -m pytest tests/e2e/test_problema.py -v -s --log-cli-level=DEBUG

# TypeError con tipos
python -m pytest tests/unit/mcp/test_search_units_tool.py -v -s

# ModuleNotFoundError
python -m pytest tests/ -v --tb=short | grep -i "module"
```

### Debugging de Imports
```bash
# Verificar imports
python -c "from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units; print('OK')"

# Verificar estructura
python -c "import src.trackhs_mcp; print('OK')"
```

### Debugging de Mocks
```python
# En tests, agregar:
import pdb; pdb.set_trace()

# O usar print statements:
print(f"Mock calls: {mock_api_client.get.call_args_list}")
print(f"Mock call count: {mock_api_client.get.call_count}")
```

---

## 📊 Comandos de Análisis

### Performance
```bash
# Tests con timing
python -m pytest tests/ --durations=10

# Tests más lentos
python -m pytest tests/ --durations=0
```

### Coverage Detallado
```bash
# Coverage por archivo
python -m pytest tests/ --cov=src --cov-report=term-missing

# Coverage específico
python -m pytest tests/unit/mcp/ --cov=src.trackhs_mcp.infrastructure.mcp --cov-report=term-missing
```

### Análisis de Código
```bash
# Complejidad
flake8 --max-complexity=10 src/

# Imports no utilizados
flake8 --select=F401 src/

# Variables no utilizadas
flake8 --select=F841 src/
```

---

## 🎯 Scripts de Automatización

### Test Suite Completo
```bash
#!/bin/bash
# test_suite.sh
echo "🧪 Ejecutando test suite completo..."

echo "📋 Tests unitarios..."
python -m pytest tests/unit/ -v

echo "🔗 Tests de integración..."
python -m pytest tests/integration/ -v

echo "🌐 Tests E2E..."
python -m pytest tests/e2e/ -v

echo "✅ Test suite completado"
```

### Pre-deploy Check
```bash
#!/bin/bash
# pre_deploy_check.sh
echo "🚀 Verificando pre-deploy..."

echo "📋 Formateando código..."
black .
isort .

echo "🧪 Ejecutando tests..."
python -m pytest tests/ -v

echo "🔍 Verificando linting..."
flake8 src/

echo "✅ Pre-deploy check completado"
```

### Debugging Script
```bash
#!/bin/bash
# debug_tests.sh
echo "🔍 Debugging tests..."

echo "📋 Tests unitarios..."
python -m pytest tests/unit/ -v --tb=short

echo "🔗 Tests de integración..."
python -m pytest tests/integration/ -v --tb=short

echo "🌐 Tests E2E..."
python -m pytest tests/e2e/ -v --tb=short

echo "📊 Resumen de fallos..."
python -m pytest tests/ --tb=no -q
```

---

## 🎨 Comandos de Formateo

### Formateo Completo
```bash
# Formatear todo
black .
isort .

# Verificar sin cambiar
black --check .
isort --check-only .
```

### Formateo Específico
```bash
# Archivo específico
black src/trackhs_mcp/infrastructure/mcp/search_units.py
isort src/trackhs_mcp/infrastructure/mcp/search_units.py

# Directorio específico
black tests/e2e/
isort tests/e2e/
```

---

## 🔄 Comandos de Git

### Workflow Estándar
```bash
# Ver estado
git status

# Agregar cambios
git add .

# Commit descriptivo
git commit -m "FEATURE: Descripción clara del cambio

✅ IMPLEMENTADO:
- Lista de cambios específicos
- Problemas resueltos
- Tests agregados

✅ IMPACTO:
- Funcionalidad mejorada
- Performance optimizada
- Bugs corregidos"

# Push
git push
```

### Debugging Git
```bash
# Ver commits recientes
git log --oneline -10

# Ver cambios en archivo
git diff src/trackhs_mcp/infrastructure/mcp/search_units.py

# Ver historial de archivo
git log --follow src/trackhs_mcp/infrastructure/mcp/search_units.py
```

---

## 🎯 Comandos de Validación

### Validación Completa
```bash
# Suite completa
python -m pytest tests/ -v --tb=short

# Con coverage
python -m pytest tests/ --cov=src --cov-report=html

# Con linting
flake8 src/
mypy src/
```

### Validación Rápida
```bash
# Solo tests críticos
python -m pytest tests/unit/mcp/ tests/e2e/test_search_units_e2e.py -v

# Tests específicos
python -m pytest tests/e2e/test_tools_integration.py -v
```

---

## 📝 Notas Importantes

### Orden de Ejecución Recomendado
1. **Desarrollo**: Tests unitarios primero
2. **Integración**: Tests de integración después
3. **E2E**: Tests E2E al final
4. **Validación**: Suite completa antes de commit

### Comandos de Emergencia
```bash
# Reset completo de tests
rm -rf .pytest_cache/
python -m pytest tests/ -v

# Limpiar imports
isort . --diff
black . --diff

# Verificar estructura
python -c "import src.trackhs_mcp; print('✅ Estructura OK')"
```

### Debugging Avanzado
```bash
# Test con profiling
python -m pytest tests/e2e/test_problema.py --profile

# Test con memory profiling
python -m pytest tests/e2e/test_problema.py --memray

# Test con coverage específico
python -m pytest tests/e2e/test_problema.py --cov=src.trackhs_mcp.infrastructure.mcp --cov-report=html
```

---

## 🎉 Conclusión

Estos comandos cubren el 90% de las necesidades de desarrollo del proyecto. Mantenerlos actualizados y documentados acelera significativamente el desarrollo.

**Regla de Oro**: Siempre ejecutar tests después de cambios significativos y usar `--tb=short` para output limpio.
