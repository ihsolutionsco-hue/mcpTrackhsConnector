# Testing Guide - TrackHS MCP Connector

Esta guía explica cómo ejecutar y agregar tests para el TrackHS MCP Connector.

## 📋 Índice

- [Configuración de Testing](#configuración-de-testing)
- [Ejecutar Tests](#ejecutar-tests)
- [Estructura de Tests](#estructura-de-tests)
- [Agregar Nuevos Tests](#agregar-nuevos-tests)
- [Cobertura de Código](#cobertura-de-código)
- [Testing Local](#testing-local)
- [CI/CD Testing](#cicd-testing)

## 🔧 Configuración de Testing

### Prerrequisitos

```bash
# Instalar dependencias de testing
pip install -r requirements-dev.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales
```

### Estructura de Testing

```
tests/
├── __init__.py
├── unit/                    # Tests unitarios
│   ├── test_api_client.py
│   ├── test_auth.py
│   ├── test_types.py
│   ├── test_error_handling.py
│   ├── test_pagination.py
│   ├── test_logging.py
│   └── test_completion.py
├── integration/            # Tests de integración
│   ├── test_search_reservations.py
│   ├── test_resources.py
│   └── test_prompts.py
└── e2e/                   # Tests end-to-end
    ├── test_server.py
    └── test_mcp_integration.py
```

## 🚀 Ejecutar Tests

### Tests Unitarios

```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/ -v

# Ejecutar test específico
pytest tests/unit/test_api_client.py -v

# Ejecutar con cobertura
pytest tests/unit/ -v --cov=src --cov-report=html
```

### Tests de Integración

```bash
# Ejecutar todos los tests de integración
pytest tests/integration/ -v

# Ejecutar test específico
pytest tests/integration/test_search_reservations.py -v
```

### Tests E2E

```bash
# Ejecutar todos los tests E2E
pytest tests/e2e/ -v

# Ejecutar test específico
pytest tests/e2e/test_server.py -v
```

### Todos los Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con marcadores específicos
pytest -m "unit" -v
pytest -m "integration" -v
pytest -m "e2e" -v
```

## 📊 Cobertura de Código

### Generar Reporte de Cobertura

```bash
# Generar reporte HTML
pytest tests/ --cov=src --cov-report=html

# Generar reporte XML
pytest tests/ --cov=src --cov-report=xml

# Ver cobertura en terminal
pytest tests/ --cov=src --cov-report=term-missing
```

### Verificar Cobertura Mínima

```bash
# Requerir 80% de cobertura
pytest tests/ --cov=src --cov-fail-under=80
```

## 🧪 Testing Local

### Script de Testing Local

```bash
# Ejecutar script de testing local
python test_local.py
```

Este script verifica:
- ✅ Configuración de variables de entorno
- ✅ Inicialización del API client
- ✅ Registro de herramientas MCP
- ✅ Registro de recursos MCP
- ✅ Registro de prompts MCP
- ✅ Sistema de manejo de errores

### Testing Manual

```bash
# Ejecutar servidor en modo desarrollo
python src/trackhs_mcp/server.py

# En otra terminal, probar conexión
curl http://localhost:8000/health
```

## 🔄 CI/CD Testing

### GitHub Actions

Los tests se ejecutan automáticamente en:
- **Push a main**: Tests completos + deployment
- **Pull Request**: Tests completos + linting
- **Manual**: Tests completos + security scan

### Configuración de Secrets

```bash
# Configurar secrets en GitHub
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
TRACKHS_TIMEOUT=30
FASTMCP_API_KEY=your_api_key
```

## 📝 Agregar Nuevos Tests

### Test Unitario

```python
# tests/unit/test_new_feature.py
import pytest
from src.trackhs_mcp.new_feature import NewFeature

class TestNewFeature:
    @pytest.mark.unit
    def test_new_feature_basic(self):
        feature = NewFeature()
        result = feature.process("input")
        assert result == "expected_output"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_new_feature_async(self):
        feature = NewFeature()
        result = await feature.process_async("input")
        assert result == "expected_output"
```

### Test de Integración

```python
# tests/integration/test_new_integration.py
import pytest
from unittest.mock import Mock, AsyncMock

class TestNewIntegration:
    @pytest.fixture
    def mock_api_client(self):
        client = Mock()
        client.get = AsyncMock()
        return client
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_new_integration(self, mock_api_client):
        mock_api_client.get.return_value = {"data": "test"}
        
        # Test integration logic
        result = await some_integration_function(mock_api_client)
        assert result["data"] == "test"
```

### Test E2E

```python
# tests/e2e/test_new_e2e.py
import pytest
from unittest.mock import Mock, AsyncMock

class TestNewE2E:
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        # Test complete end-to-end workflow
        result = await complete_workflow()
        assert result["status"] == "success"
```

## 🏷️ Marcadores de Tests

### Marcadores Disponibles

```python
@pytest.mark.unit          # Tests unitarios
@pytest.mark.integration   # Tests de integración
@pytest.mark.e2e          # Tests end-to-end
@pytest.mark.slow         # Tests lentos
@pytest.mark.api          # Tests que requieren API
@pytest.mark.auth         # Tests de autenticación
@pytest.mark.network      # Tests que requieren red
```

### Ejecutar por Marcador

```bash
# Solo tests unitarios
pytest -m "unit" -v

# Solo tests de integración
pytest -m "integration" -v

# Excluir tests lentos
pytest -m "not slow" -v

# Solo tests que requieren API
pytest -m "api" -v
```

## 🔍 Debugging Tests

### Ejecutar con Debug

```bash
# Ejecutar con output detallado
pytest tests/ -v -s

# Ejecutar con pdb
pytest tests/ --pdb

# Ejecutar test específico con debug
pytest tests/unit/test_api_client.py::TestTrackHSApiClient::test_request_success -v -s --pdb
```

### Logging en Tests

```python
import logging

def test_with_logging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.debug("Test starting")
    # Test logic
    logger.debug("Test completed")
```

## 📈 Performance Testing

### Tests de Rendimiento

```bash
# Ejecutar tests de rendimiento
pytest tests/ -k "performance" --benchmark-only

# Generar reporte de rendimiento
pytest tests/ --benchmark-only --benchmark-save=performance-report
```

### Memory Testing

```bash
# Ejecutar tests de memoria
pytest tests/e2e/test_mcp_integration.py::TestMCPIntegrationE2E::test_memory_usage_workflow -v
```

## 🛡️ Security Testing

### Tests de Seguridad

```bash
# Ejecutar bandit (security linter)
bandit -r src/

# Ejecutar safety (vulnerability check)
safety check

# Ejecutar semgrep (security scanner)
semgrep --config=auto src/
```

## 📋 Checklist de Testing

### Antes de Commit

- [ ] Tests unitarios pasan
- [ ] Tests de integración pasan
- [ ] Tests E2E pasan
- [ ] Cobertura >= 80%
- [ ] Linting pasa
- [ ] Security scan pasa

### Antes de Deploy

- [ ] Todos los tests pasan
- [ ] Performance tests pasan
- [ ] Security tests pasan
- [ ] Documentation actualizada
- [ ] Secrets configurados

## 🚨 Troubleshooting

### Problemas Comunes

1. **ImportError**: Verificar que `src/` está en el PYTHONPATH
2. **AsyncIO errors**: Usar `pytest-asyncio` y `@pytest.mark.asyncio`
3. **Mock errors**: Verificar que los mocks están configurados correctamente
4. **Timeout errors**: Aumentar timeout en configuración

### Soluciones

```bash
# Verificar imports
python -c "from src.trackhs_mcp.server import main"

# Verificar async
pytest tests/ --asyncio-mode=auto

# Verificar mocks
pytest tests/ -v -s --tb=short
```

## 📚 Recursos Adicionales

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [FastMCP Testing Guide](https://fastmcp.dev/testing)
- [Python Testing Best Practices](https://docs.python.org/3/library/unittest.html)
