# TrackHS MCP Connector

Servidor MCP robusto para interactuar con la API de TrackHS, implementando las mejores prácticas de FastMCP con validación Pydantic y documentación completa.

## 🚀 Características

- **Herramientas MCP** para gestión de reservas, unidades, amenidades y órdenes de trabajo
- **Validación robusta** con Pydantic y esquemas de salida
- **Manejo de errores** completo con excepciones personalizadas
- **Middleware** para logging, autenticación y métricas
- **Testing completo** con cobertura exhaustiva
- **Documentación** detallada y ejemplos de uso

## 📋 Herramientas Disponibles

### 🔍 Búsqueda y Consulta
- `search_reservations` - Buscar reservas con filtros avanzados
- `get_reservation` - Obtener detalles de reserva específica
- `search_units` - Buscar unidades de alojamiento
- `search_amenities` - Consultar amenidades disponibles

### 💰 Información Financiera
- `get_folio` - Obtener folio financiero de reserva

### 🔧 Gestión de Operaciones
- `create_maintenance_work_order` - Crear orden de mantenimiento
- `create_housekeeping_work_order` - Crear orden de limpieza

## 🛠️ Instalación

### Requisitos
- Python 3.9+
- Credenciales de TrackHS API

### Instalación
```bash
# Clonar repositorio
git clone <repository-url>
cd MCPtrackhsConnector

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export TRACKHS_USERNAME="tu_usuario"
export TRACKHS_PASSWORD="tu_password"
export TRACKHS_BASE_URL="https://api.trackhs.com/api"
```

## 🚀 Uso

### Ejecutar Servidor MCP
```bash
python -m src.trackhs_mcp
```

### Usar con Cliente MCP
```python
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from trackhs_mcp.server import mcp

async with Client(transport=FastMCPTransport(mcp)) as client:
    # Buscar unidades
    result = await client.call_tool(
        name="search_units",
        arguments={"bedrooms": 2, "bathrooms": 1}
    )
    print(result.data)
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/search_units/ -v

# Tests con cobertura
python -m pytest tests/search_units/ --cov=src/trackhs_mcp --cov-report=html

# Script de testing completo
python scripts/testing/run_search_units_tests.py all
```

### Ejemplos de Uso
```bash
# Ejecutar ejemplos
python scripts/testing/example_search_units_usage.py
```

## 📚 Documentación

- [Documentación Completa](docs/testing/TESTING_SEARCH_UNITS.md)
- [Guía Rápida](docs/testing/README_TESTING.md)
- [Documentación Oficial TrackHS](documentacion%20oficial%20trackhs/)

## 🏗️ Estructura del Proyecto

```
MCPtrackhsConnector/
├── src/trackhs_mcp/          # Código fuente principal
│   ├── server.py             # Servidor MCP
│   ├── schemas.py            # Esquemas Pydantic
│   ├── exceptions.py         # Excepciones personalizadas
│   └── middleware.py         # Middleware
├── tests/                    # Tests
│   ├── search_units/         # Tests específicos de search_units
│   └── conftest.py           # Configuración de tests
├── scripts/testing/          # Scripts de testing
├── docs/testing/             # Documentación de testing
└── requirements.txt          # Dependencias
```

## 🔧 Configuración

### Variables de Entorno
```bash
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_BASE_URL=https://api.trackhs.com/api
```

### Configuración de Tests
```bash
SLOW_TESTS=true              # Incluir tests lentos
MOCK_API=false              # Usar API real vs mock
API_TIMEOUT=30.0            # Timeout en segundos
MAX_RETRIES=3               # Reintentos máximos
```

## 📊 Testing

### Cobertura de Tests
- **Tests Unitarios**: Validación de parámetros, manejo de errores, casos límite
- **Tests de Integración**: Integración con MCP, middleware
- **Tests de API Real**: Conexión real con TrackHS API
- **Tests E2E**: Escenarios completos de usuario

### Métricas de Rendimiento
- Tiempo de respuesta: < 5 segundos
- Uso de memoria: < 100MB
- Requests concurrentes: hasta 10
- Tasa de éxito: > 95%

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Ejecuta los tests: `python scripts/testing/run_search_units_tests.py all-checks`
5. Crea un pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🆘 Soporte

Para problemas o preguntas:
1. Revisa la documentación en `docs/testing/`
2. Ejecuta los tests para verificar la configuración
3. Crea un issue en el repositorio

---

**¡TrackHS MCP Connector - Conectando con Excelencia! 🚀**