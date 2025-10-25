# 🧪 Guía de Testing - TrackHS MCP Server

## 📋 **Resumen de Estrategia de Testing**

Esta guía documenta la estrategia de testing mejorada para el servidor TrackHS MCP, implementando las mejores prácticas de FastMCP 2.0.

## 🎯 **Objetivos de Testing**

1. **Validación Completa**: Asegurar que todas las herramientas MCP funcionen correctamente
2. **Testing Determinístico**: Tests rápidos y confiables usando transporte in-memory
3. **Validación de Red**: Tests de transportes HTTP/SSE para despliegue
4. **Integración End-to-End**: Flujos completos de trabajo
5. **Performance**: Validación bajo carga y concurrencia

## 🏗️ **Arquitectura de Testing**

### **Niveles de Testing**

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING PYRAMID                         │
├─────────────────────────────────────────────────────────────┤
│  Integration Tests (test_integration.py)                   │
│  ├─ Full workflows                                         │
│  ├─ Error recovery                                         │
│  └─ Performance under load                                 │
├─────────────────────────────────────────────────────────────┤
│  Network Tests (test_network_transports.py)                │
│  ├─ HTTP transport validation                              │
│  ├─ SSE transport validation                               │
│  └─ Concurrent requests                                    │
├─────────────────────────────────────────────────────────────┤
│  Advanced Tests (test_advanced_server.py)                  │
│  ├─ Inline snapshots                                       │
│  ├─ Dirty equals validation                                │
│  └─ Parametrized tests                                     │
├─────────────────────────────────────────────────────────────┤
│  Unit Tests (test_server.py, test_validation.py)          │
│  ├─ Individual tool testing                                │
│  ├─ Schema validation                                      │
│  └─ Error handling                                         │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ **Herramientas y Dependencias**

### **Dependencias Principales**
```txt
fastmcp>=2.0.0              # Framework MCP
pytest>=7.0.0               # Framework de testing
pytest-asyncio>=0.21.0      # Soporte async
inline-snapshot>=0.4.0      # Snapshots para validación
dirty-equals>=0.5.0         # Validación flexible
anyio>=4.0.0                # Task groups para tests de red
```

### **Marcadores de pytest**
```ini
markers =
    asyncio: marks tests as async
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    network: marks tests that require network access
    slow: marks tests that take longer to run
    client_process: marks tests that spawn subprocesses
```

## 🧪 **Tipos de Tests**

### **1. Tests In-Memory (Recomendado)**

**Archivo**: `tests/test_advanced_server.py`

**Características**:
- ✅ Rápidos (milisegundos)
- ✅ Determinísticos
- ✅ Sin dependencias de red
- ✅ Soporte completo de debugger

**Ejemplo**:
```python
@pytest.mark.asyncio
async def test_list_tools_with_snapshot(self, mcp_client: Client[FastMCPTransport]):
    """Test con snapshot para validación de estructura"""
    tools = await mcp_client.list_tools()

    # Usar snapshot para validar estructura completa
    assert tools == snapshot([
        snapshot({
            "name": "search_reservations",
            "description": IsStr(),
            "inputSchema": IsDict()
        }),
        # ... más herramientas
    ])
```

### **2. Tests de Red**

**Archivo**: `tests/test_network_transports.py`

**Características**:
- 🌐 Validación de transportes HTTP/SSE
- 🔄 Tests de concurrencia
- ⚡ Tests de performance
- 🏷️ Marcador `@pytest.mark.network`

**Ejemplo**:
```python
@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_basic(http_server: str):
    """Test básico de transporte HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        result = await client.ping()
        assert result is True
```

### **3. Tests de Integración**

**Archivo**: `tests/test_integration.py`

**Características**:
- 🔄 Flujos completos de trabajo
- 🚨 Recuperación de errores
- 📊 Performance bajo carga
- 🏷️ Marcador `@pytest.mark.integration`

**Ejemplo**:
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_reservation_workflow(self, mcp_client):
    """Test de flujo completo de reserva"""
    # 1. Buscar reservas
    # 2. Obtener reserva específica
    # 3. Obtener folio
    # Validar flujo completo
```

## 🚀 **Comandos de Testing**

### **Ejecutar Todos los Tests**
```bash
# Tests completos con cobertura
pytest tests/ -v --cov=src --cov-report=html

# Solo tests unitarios (rápidos)
pytest tests/test_server.py tests/test_validation.py -v

# Solo tests de red
pytest tests/test_network_transports.py -v -m network

# Solo tests de integración
pytest tests/test_integration.py -v -m integration
```

### **Tests Específicos**
```bash
# Tests con snapshots (actualizar snapshots)
pytest tests/test_advanced_server.py --inline-snapshot=fix

# Tests de performance
pytest tests/test_integration.py -v -m slow

# Tests concurrentes
pytest tests/test_network_transports.py -v -k concurrent
```

### **Validación para FastMCP Cloud**
```bash
# Test de validación para despliegue
python test_fastmcp_cloud.py

# Test simple del servidor
python scripts/test_server_simple.py
```

## 📊 **Métricas de Testing**

### **Cobertura de Código**
```bash
# Generar reporte de cobertura
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Ver reporte en navegador
open htmlcov/index.html
```

### **Performance**
```bash
# Tests de performance
pytest tests/test_integration.py -v -m slow --durations=10

# Tests de red
pytest tests/test_network_transports.py -v -m network --durations=5
```

## 🔧 **Configuración Avanzada**

### **Variables de Entorno**
```bash
# Para tests locales
export TRACKHS_USERNAME="test_user"
export TRACKHS_PASSWORD="test_password"
export TRACKHS_BASE_URL="https://api-test.trackhs.com/api"

# Para tests de integración
export TRACKHS_TEST_MODE="integration"
```

### **Fixtures Personalizadas**
```python
@pytest.fixture
async def mcp_client():
    """Cliente MCP para tests in-memory"""
    from trackhs_mcp.server import mcp
    async with Client(transport=FastMCPTransport(mcp)) as client:
        yield client

@pytest.fixture
async def http_server_fixture(task_group: TaskGroup):
    """Servidor HTTP para tests de red"""
    from fastmcp.utilities.tests import run_server_async
    url = await run_server_async(task_group, mcp, transport="http")
    yield url
```

## 🎯 **Mejores Prácticas**

### **1. Usar Inline Snapshots**
```python
# ✅ Bueno: Validación de estructura completa
assert tools == snapshot([...])

# ❌ Malo: Validación manual
assert len(tools) == 7
assert tools[0].name == "search_reservations"
```

### **2. Usar Dirty Equals para Valores Dinámicos**
```python
# ✅ Bueno: Validación flexible
assert response == IsStr()
assert timestamp == IsInt(ge=0)

# ❌ Malo: Validación exacta
assert response == "specific_string"
assert timestamp == 1234567890
```

### **3. Tests Parametrizados**
```python
# ✅ Bueno: Múltiples escenarios
@pytest.mark.parametrize("page,size,expected_valid", [
    (0, 10, True),
    (1, 25, True),
    (-1, 10, False),
    (0, 0, False),
])
async def test_search_reservations_parametrized(page, size, expected_valid):
    # Test logic
```

### **4. Marcadores Apropiados**
```python
# ✅ Bueno: Marcadores específicos
@pytest.mark.network
@pytest.mark.slow
@pytest.mark.asyncio
async def test_performance():
    # Test logic
```

## 🚨 **Troubleshooting**

### **Problemas Comunes**

1. **Tests de Red Fallan**
   ```bash
   # Verificar que el servidor esté corriendo
   pytest tests/test_network_transports.py -v -s
   ```

2. **Snapshots Desactualizados**
   ```bash
   # Actualizar snapshots
   pytest tests/test_advanced_server.py --inline-snapshot=fix
   ```

3. **Tests Lentos**
   ```bash
   # Ejecutar solo tests rápidos
   pytest tests/ -v -m "not slow"
   ```

### **Debug de Tests**
```python
# Agregar prints para debug
@pytest.mark.asyncio
async def test_debug():
    result = await mcp_client.call_tool("search_reservations", {"page": 0, "size": 10})
    print(f"Result: {result.content[0].text}")
    assert result.content[0].text is not None
```

## 📈 **Métricas de Éxito**

### **Objetivos de Testing**
- ✅ **Cobertura**: >90% de código cubierto
- ⚡ **Velocidad**: Tests unitarios <1s, integración <30s
- 🔄 **Confiabilidad**: 0% de flaky tests
- 📊 **Performance**: <5s para tests de red

### **Reportes**
```bash
# Reporte completo
pytest tests/ --cov=src --cov-report=html --junitxml=test-results.xml

# Métricas de performance
pytest tests/ --durations=10 --tb=short
```

## 🎉 **Conclusión**

Esta estrategia de testing implementa las mejores prácticas de FastMCP 2.0:

- ✅ **Testing In-Memory**: Rápido y determinístico
- ✅ **Inline Snapshots**: Validación de estructuras complejas
- ✅ **Dirty Equals**: Validación flexible de valores dinámicos
- ✅ **Tests de Red**: Validación de transportes HTTP/SSE
- ✅ **Integración**: Flujos completos de trabajo
- ✅ **Performance**: Validación bajo carga

**El servidor TrackHS MCP está completamente preparado para testing robusto y despliegue en producción** 🚀
