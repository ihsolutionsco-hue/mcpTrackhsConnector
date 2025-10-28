# TrackHS MCP Connector v2.0.0

**Arquitectura FastMCP Simplificada** - Un conector MCP (Model Context Protocol) para interactuar con la API de TrackHS siguiendo las mejores prácticas de FastMCP.

## 🚀 Características

- **Arquitectura Simplificada**: Código limpio y minimalista siguiendo patrones FastMCP
- **7 Herramientas MCP**: Búsqueda de reservas, unidades, amenidades y gestión de órdenes de trabajo
- **Validación Robusta**: Type safety completo con Pydantic
- **Manejo de Errores**: ToolError consistente para todos los casos de error
- **Configuración Centralizada**: Variables de entorno con validación
- **Logging Estructurado**: Logs informativos y debugging
- **Health Check**: Endpoint de monitoreo integrado

## 📁 Estructura del Proyecto

```
src/trackhs_mcp/
├── server.py          # Servidor principal + todas las tools (400 líneas)
├── client.py          # TrackHSClient simple con httpx (150 líneas)
├── config.py          # Configuración Pydantic centralizada
├── schemas.py         # Output schemas para validación (simplificado)
├── middleware.py      # Middleware esencial (auth + logging)
├── utils.py           # Funciones helper (limpieza de datos)
├── __init__.py        # Exports del paquete
└── __main__.py        # Entry point para FastMCP Cloud
```

## 🛠️ Herramientas Disponibles

### 1. **search_reservations**
Buscar reservas con filtros avanzados (fecha, estado, texto)
```python
search_reservations(
    page=1,
    size=10,
    arrival_start="2024-01-15",
    status="confirmed"
)
```

### 2. **get_reservation**
Obtener detalles completos de una reserva específica
```python
get_reservation(reservation_id=12345)
```

### 3. **search_units**
Buscar unidades de alojamiento con filtros (dormitorios, baños, amenidades)
```python
search_units(
    bedrooms=2,
    bathrooms=1,
    pets_friendly=1,
    is_active=1
)
```

### 4. **search_amenities**
Consultar amenidades disponibles en el sistema
```python
search_amenities(search="wifi", size=50)
```

### 5. **get_folio**
Obtener información financiera completa de una reserva
```python
get_folio(reservation_id=12345)
```

### 6. **create_maintenance_work_order**
Crear órdenes de trabajo de mantenimiento
```python
create_maintenance_work_order(
    unit_id=123,
    summary="Fuga en grifo",
    description="Grifo del baño principal gotea",
    priority=3
)
```

### 7. **create_housekeeping_work_order**
Crear órdenes de trabajo de housekeeping
```python
create_housekeeping_work_order(
    unit_id=123,
    scheduled_at="2024-01-15",
    is_inspection=False,
    clean_type_id=4
)
```

## ⚙️ Instalación

### Requisitos
- Python 3.11+
- Credenciales de TrackHS API

### Instalación desde PyPI
```bash
pip install trackhs-mcp
```

### Instalación desde código fuente
```bash
git clone https://github.com/tu-usuario/trackhs-mcp-connector.git
cd trackhs-mcp-connector
pip install -e .
```

## 🔧 Configuración

### Variables de Entorno
Crear archivo `.env` en el directorio raíz:

```env
# Credenciales TrackHS (requeridas)
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña

# URL de la API (opcional)
TRACKHS_API_URL=https://ihmvacations.trackhs.com

# Configuración de logging (opcional)
LOG_LEVEL=INFO
STRICT_VALIDATION=false

# Configuración de requests (opcional)
MAX_RETRIES=3
REQUEST_TIMEOUT=30.0
```

### Validación de Configuración
El servidor valida automáticamente las credenciales al iniciar:
- ✅ Verifica que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` estén configurados
- ✅ Prueba la conectividad con la API TrackHS
- ✅ Muestra estado de configuración en los logs

## 🚀 Uso

### Ejecutar Servidor Local
```bash
python -m trackhs_mcp
```

### Ejecutar con FastMCP Cloud
```bash
# El servidor está optimizado para FastMCP Cloud
# Solo requiere las variables de entorno configuradas
```

### Usar como Cliente MCP
```python
from fastmcp.client import Client
from trackhs_mcp import mcp

async with Client(mcp) as client:
    # Buscar reservas
    reservations = await client.call_tool(
        "search_reservations",
        arguments={"page": 1, "size": 10}
    )

    # Obtener detalles de reserva
    reservation = await client.call_tool(
        "get_reservation",
        arguments={"reservation_id": 12345}
    )
```

## 🏗️ Arquitectura

### Principios de Diseño
- **Simplicidad**: Código directo sin abstracciones innecesarias
- **FastMCP Idiomático**: Siguiendo patrones recomendados por FastMCP
- **Type Safety**: Validación completa con Pydantic
- **Error Handling**: Manejo consistente de errores con ToolError
- **Logging**: Logs estructurados para debugging y monitoreo

### Flujo de Datos
```
Cliente MCP → FastMCP Server → TrackHSClient → TrackHS API
     ↓              ↓              ↓
Validación → Logging → HTTP Request → Response
     ↓              ↓              ↓
ToolError ← Sanitización ← Data Cleaning ← JSON
```

### Componentes Principales

#### **TrackHSClient** (`client.py`)
- Cliente HTTP simple con httpx
- Autenticación HTTP Basic
- Manejo de errores HTTP → ToolError
- Timeout y retry configurables

#### **Schemas** (`schemas.py`)
- Output schemas para validación de respuestas
- Aliases para campos con underscore
- Documentación completa para LLMs

#### **Utils** (`utils.py`)
- Limpieza de datos problemáticos (campo `area`)
- Sanitización para logging seguro
- Normalización de tipos de datos

#### **Middleware** (`middleware.py`)
- AuthMiddleware: Verificación de credenciales
- LoggingMiddleware: Logs estructurados
- Métricas básicas (opcional)

## 📊 Métricas de Simplificación

### Antes (v1.0.0) vs Después (v2.0.0)
- **Líneas de código**: ~3000 → ~800 (73% reducción)
- **Archivos**: 25+ → 7 archivos (72% reducción)
- **Capas de abstracción**: 4 → 1 (75% reducción)
- **Tiempo de comprensión**: Días → Horas

### Archivos Eliminados
- ❌ `services/` (3 archivos) → Lógica inline en tools
- ❌ `repositories/` (4 archivos) → TrackHSClient directo
- ❌ `models/` (múltiples) → Schemas simplificados
- ❌ `middleware_native.py` → Middleware esencial
- ❌ `cache.py` → httpx cache built-in
- ❌ `metrics.py` → Logging FastMCP
- ❌ `validators.py` → Pydantic automático
- ❌ `exceptions.py` → ToolError FastMCP

## 🧪 Testing

### Ejecutar Tests
```bash
# Test básico de migración
python test_fastmcp_migration.py

# Tests con pytest (si están configurados)
pytest tests/
```

### Validación Manual
```bash
# Usar MCP Inspector para probar herramientas
# 1. Iniciar servidor: python -m trackhs_mcp
# 2. Conectar con MCP Inspector
# 3. Probar cada herramienta individualmente
```

## 🔍 Health Check

El servidor incluye un endpoint de health check:

```python
# Verificar estado del servidor
GET https://trackhs-mcp.local/health

# Respuesta ejemplo:
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "2.0.0",
    "dependencies": {
        "trackhs_api": {
            "status": "healthy",
            "response_time_ms": 245.67,
            "base_url": "https://ihmvacations.trackhs.com",
            "credentials_configured": true
        }
    }
}
```

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. **Error de Credenciales**
```
ToolError: Cliente API no disponible. Verifique las credenciales.
```
**Solución**: Verificar que `TRACKHS_USERNAME` y `TRACKHS_PASSWORD` estén configurados.

#### 2. **Error de Conectividad**
```
ToolError: Error de conexión con TrackHS: ...
```
**Solución**: Verificar conectividad de red y URL de API.

#### 3. **Error de Validación**
```
ValidationError: ...
```
**Solución**: Verificar que los parámetros cumplan con las restricciones (fechas YYYY-MM-DD, etc.).

### Logs de Debug
```bash
# Habilitar logs detallados
export LOG_LEVEL=DEBUG
python -m trackhs_mcp
```

## 🤝 Contribución

### Desarrollo Local
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/trackhs-mcp-connector.git
cd trackhs-mcp-connector

# Instalar en modo desarrollo
pip install -e .

# Ejecutar tests
python test_fastmcp_migration.py
```

### Estructura de Commits
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **FastMCP Team** por el framework excelente
- **TrackHS** por la API robusta
- **Pydantic** por la validación de tipos
- **httpx** por el cliente HTTP asíncrono

## 📞 Soporte

- **Email**: support@trackhs.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/trackhs-mcp-connector/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/tu-usuario/trackhs-mcp-connector/wiki)

---

**TrackHS MCP Connector v2.0.0** - Arquitectura FastMCP Simplificada 🚀
