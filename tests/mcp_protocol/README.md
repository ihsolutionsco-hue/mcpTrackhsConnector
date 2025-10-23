# 🧪 Tests de Protocolo MCP - TrackHS MCP Connector

## 📋 **Descripción**

Tests específicos para validar el cumplimiento del protocolo MCP (Model Context Protocol) en el TrackHS MCP Connector. Estos tests se enfocan en validar que todos los componentes MCP (herramientas, recursos, prompts) se registran y funcionan correctamente.

## 🎯 **Objetivos**

- ✅ **Validar registro de herramientas MCP** (7 herramientas)
- ✅ **Validar registro de recursos MCP** (16 recursos)
- ✅ **Validar registro de prompts MCP** (3 prompts)
- ✅ **Validar schema hook** (corrección automática de esquemas)
- ✅ **Validar integración completa** (todos los componentes juntos)

## 📁 **Estructura de Tests**

```
tests/mcp_protocol/
├── test_tools_registration.py      # Tests de registro de herramientas
├── test_resources_registration.py # Tests de registro de recursos
├── test_prompts_registration.py   # Tests de registro de prompts
├── test_schema_validation.py      # Tests de schema hook
├── test_complete_integration.py   # Tests de integración completa
├── conftest.py                    # Fixtures compartidas
├── run_tests.py                   # Script de ejecución
├── pytest.ini                     # Configuración pytest
└── README.md                       # Esta documentación
```

## 🚀 **Ejecución Rápida**

### **Ejecutar Todos los Tests**
```bash
# Desde el directorio raíz del proyecto
python -m pytest tests/mcp_protocol/ -v

# O usar el script específico
python tests/mcp_protocol/run_tests.py all
```

### **Ejecutar Tests Específicos**
```bash
# Solo tests de herramientas
python -m pytest tests/mcp_protocol/test_tools_registration.py -v

# Solo tests de recursos
python -m pytest tests/mcp_protocol/test_resources_registration.py -v

# Solo tests de prompts
python -m pytest tests/mcp_protocol/test_prompts_registration.py -v

# Solo tests de schema hook
python -m pytest tests/mcp_protocol/test_schema_validation.py -v

# Solo tests de integración
python -m pytest tests/mcp_protocol/test_complete_integration.py -v
```

### **Ejecutar con Cobertura**
```bash
# Con reporte de cobertura
python -m pytest tests/mcp_protocol/ -v --cov=src/trackhs_mcp --cov-report=html

# O usar el script
python tests/mcp_protocol/run_tests.py coverage
```

## 📊 **Tests por Categoría**

### **1. Tests de Herramientas MCP (`test_tools_registration.py`)**

| Test | Descripción | Herramienta |
|------|-------------|-------------|
| `test_search_reservations_tool_registration` | Registro de búsqueda de reservas | `search_reservations` |
| `test_get_reservation_tool_registration` | Registro de obtención de reserva | `get_reservation` |
| `test_get_folio_tool_registration` | Registro de obtención de folio | `get_folio` |
| `test_search_units_tool_registration` | Registro de búsqueda de unidades | `search_units` |
| `test_search_amenities_tool_registration` | Registro de búsqueda de amenidades | `search_amenities` |
| `test_create_maintenance_work_order_tool_registration` | Registro de creación de orden de mantenimiento | `create_maintenance_work_order` |
| `test_create_housekeeping_work_order_tool_registration` | Registro de creación de orden de housekeeping | `create_housekeeping_work_order` |
| `test_all_tools_registration_together` | Registro de todas las herramientas juntas | Todas |
| `test_tool_registration_with_invalid_api_client` | Manejo de errores de API client | Todas |
| `test_tool_registration_with_missing_methods` | Manejo de métodos faltantes | Todas |

### **2. Tests de Recursos MCP (`test_resources_registration.py`)**

| Test | Descripción | Categoría |
|------|-------------|-----------|
| `test_schema_resources_registration` | Registro de recursos de esquemas | Schemas |
| `test_documentation_resources_registration` | Registro de recursos de documentación | Documentation |
| `test_reference_resources_registration` | Registro de recursos de referencia | References |
| `test_example_resources_registration` | Registro de recursos de ejemplos | Examples |
| `test_all_resources_registration_together` | Registro de todos los recursos | Todas |
| `test_specific_schema_resources` | Registro de esquemas específicos | Schemas |
| `test_specific_documentation_resources` | Registro de documentación específica | Documentation |
| `test_specific_reference_resources` | Registro de referencias específicas | References |
| `test_specific_example_resources` | Registro de ejemplos específicos | Examples |

### **3. Tests de Prompts MCP (`test_prompts_registration.py`)**

| Test | Descripción | Prompt |
|------|-------------|--------|
| `test_all_prompts_registration` | Registro de todos los prompts | Todos |
| `test_date_range_search_prompt_registration` | Registro de prompt de búsqueda por fechas | `create_date_range_search_prompt` |
| `test_guest_search_prompt_registration` | Registro de prompt de búsqueda por huésped | `create_guest_search_prompt` |
| `test_scroll_search_prompt_registration` | Registro de prompt de búsqueda con scroll | `create_scroll_search_prompt` |
| `test_combined_search_prompt_registration` | Registro de prompt de búsqueda combinada | `create_combined_search_prompt` |
| `test_updated_reservations_prompt_registration` | Registro de prompt de reservas actualizadas | `create_updated_reservations_prompt` |

### **4. Tests de Schema Hook (`test_schema_validation.py`)**

| Test | Descripción | Funcionalidad |
|------|-------------|---------------|
| `test_schema_hook_creation` | Creación del schema hook | Hook básico |
| `test_schema_hook_has_correct_attributes` | Atributos del schema hook | Hook básico |
| `test_schema_hook_with_different_names` | Schema hook con diferentes nombres | Hook básico |
| `test_schema_hook_with_none_name` | Manejo de nombre nulo | Error handling |
| `test_schema_hook_with_empty_name` | Manejo de nombre vacío | Error handling |
| `test_schema_hook_multiple_instances` | Múltiples instancias del hook | Hook básico |
| `test_schema_hook_with_mock_fastmcp` | Hook con FastMCP mockeado | Hook básico |
| `test_schema_hook_import_structure` | Estructura de imports | Hook básico |
| `test_schema_hook_with_invalid_parameters` | Parámetros inválidos | Error handling |
| `test_schema_hook_consistency` | Consistencia del hook | Hook básico |
| `test_schema_hook_with_special_characters` | Caracteres especiales | Hook básico |

### **5. Tests de Integración Completa (`test_complete_integration.py`)**

| Test | Descripción | Integración |
|------|-------------|-------------|
| `test_complete_mcp_server_integration` | Integración completa del servidor MCP | Completa |
| `test_mcp_server_with_mock_api_client` | Servidor MCP con API client mockeado | Completa |
| `test_mcp_server_with_schema_hook` | Servidor MCP con schema hook | Completa |
| `test_mcp_server_error_handling` | Manejo de errores del servidor MCP | Error handling |
| `test_mcp_server_with_none_components` | Manejo de componentes nulos | Error handling |
| `test_mcp_server_with_incomplete_api_client` | API client incompleto | Error handling |
| `test_mcp_server_multiple_registrations` | Múltiples registros | Completa |
| `test_mcp_server_with_different_configurations` | Diferentes configuraciones | Completa |
| `test_mcp_server_consistency` | Consistencia entre instancias | Completa |

## 🔧 **Fixtures Disponibles**

### **Fixtures de API Client**
- `mock_api_client`: API client básico mockeado
- `mock_api_client_with_data`: API client con datos específicos
- `trackhs_api_client`: Cliente API real de TrackHS

### **Fixtures de Servidor MCP**
- `mcp_server`: Servidor MCP básico
- `mcp_server_with_schema_hook`: Servidor MCP con schema hook
- `complete_mcp_server`: Servidor MCP completo con todos los componentes

### **Fixtures de Configuración**
- `trackhs_config`: Configuración de TrackHS
- `trackhs_api_client`: Cliente API de TrackHS

## 📈 **Métricas de Éxito**

### **Cobertura Objetivo**
- **Tests de Herramientas**: 100% de herramientas registradas
- **Tests de Recursos**: 100% de recursos registrados
- **Tests de Prompts**: 100% de prompts registrados
- **Tests de Schema Hook**: 100% de funcionalidades del hook
- **Tests de Integración**: 100% de flujos de integración

### **Tiempos Objetivo**
- **Tests de Herramientas**: <30 segundos
- **Tests de Recursos**: <20 segundos
- **Tests de Prompts**: <15 segundos
- **Tests de Schema Hook**: <10 segundos
- **Tests de Integración**: <60 segundos
- **Total**: <2 minutos

### **Calidad Objetivo**
- **0 tests flaky** (inconsistentes)
- **0 tests lentos** (>5 segundos por test)
- **100% tests pasando** en CI/CD
- **0 warnings** en pytest

## 🐛 **Troubleshooting**

### **Tests Muy Lentos**
```bash
# Verificar que pytest-xdist esté instalado
pip install pytest-xdist

# Ejecutar en paralelo
python -m pytest tests/mcp_protocol/ -n auto
```

### **Tests Fallan**
```bash
# Ver detalles del error
python -m pytest tests/mcp_protocol/ -v --tb=long

# Solo el test que falla
python -m pytest tests/mcp_protocol/test_tools_registration.py::TestMCPToolsRegistration::test_search_reservations_tool_registration -v
```

### **Cobertura Baja**
```bash
# Ver qué no está cubierto
python -m pytest tests/mcp_protocol/ --cov=src/trackhs_mcp --cov-report=term-missing

# Generar reporte HTML
python -m pytest tests/mcp_protocol/ --cov=src/trackhs_mcp --cov-report=html
# Abrir htmlcov_mcp_protocol/index.html
```

## 🔄 **CI/CD Integration**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/mcp_protocol_tests.yml
name: MCP Protocol Tests

on: [push, pull_request]

jobs:
  mcp-protocol-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run MCP Protocol Tests
        run: python -m pytest tests/mcp_protocol/ -v --cov=src/trackhs_mcp --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml
```

## 📚 **Referencias**

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [MCP Protocol](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://fastmcp.dev/)
- [TrackHS API Documentation](https://api.trackhs.com/docs)

## 🎯 **Próximos Pasos**

1. **Ejecutar tests de protocolo MCP** para validar implementación actual
2. **Implementar tests unitarios** para cada herramienta individual
3. **Implementar tests de integración** para flujos completos
4. **Implementar tests de API real** para validación end-to-end
5. **Configurar CI/CD** para automatización completa
