# Migración FastMCP Completa - TrackHS MCP Connector

## Resumen

Este documento describe la migración completa del proyecto TrackHS MCP Connector a las mejores prácticas de FastMCP 2.12+, incluyendo configuración declarativa, sistema de middleware robusto, validación estricta y testing in-memory.

## Características Implementadas

### 1. Configuración Declarativa (`fastmcp.json`)

**Antes:**
```yaml
# fastmcp.yaml
server:
  name: "TrackHS MCP Server"
  description: "Conector MCP para TrackHS API"
```

**Después:**
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "src/trackhs_mcp/__main__.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.10",
    "requirements": "requirements.txt"
  }
}
```

**Beneficios:**
- Autocompletado en IDE con esquema JSON
- Configuración portable entre ambientes
- Validación automática de configuración

### 2. Sistema de Middleware

#### ErrorHandlingMiddleware
```python
from src.trackhs_mcp.infrastructure.middleware import TrackHSErrorHandlingMiddleware

# Middleware personalizado para TrackHS API
error_middleware = TrackHSErrorHandlingMiddleware(
    include_traceback=False,
    transform_errors=True
)
mcp.add_middleware(error_middleware)
```

**Características:**
- Integración con sistema de logging existente
- Tracking de patrones de error
- Transformación de errores a mensajes amigables
- Estadísticas de errores

#### LoggingMiddleware
```python
from src.trackhs_mcp.infrastructure.middleware import TrackHSLoggingMiddleware

# Middleware de logging estructurado
logging_middleware = TrackHSLoggingMiddleware(
    log_requests=True,
    log_responses=True,
    log_timing=True,
    log_level="INFO"
)
mcp.add_middleware(logging_middleware)
```

**Características:**
- Logging estructurado de requests/responses
- Sanitización automática de parámetros sensibles
- Medición de tiempos de ejecución
- Estadísticas de rendimiento

### 3. Validación Estricta

**Configuración:**
```python
mcp = FastMCP(
    name="TrackHS MCP Server",
    strict_input_validation=True,  # Validación estricta
    mask_error_details=False,      # Mostrar detalles en desarrollo
    include_fastmcp_meta=True      # Metadatos FastMCP
)
```

**Diferencias de comportamiento:**

| Input | `strict_input_validation=False` | `strict_input_validation=True` |
|-------|--------------------------------|--------------------------------|
| `"10"` para `int` | ✅ Coerción a `10` | ❌ Error de validación |
| `"3.14"` para `float` | ✅ Coerción a `3.14` | ❌ Error de validación |
| `"true"` para `bool` | ✅ Coerción a `True` | ❌ Error de validación |

### 4. Manejo de Errores con ToolError

**Antes:**
```python
from ...domain.exceptions.api_exceptions import ValidationError

if not folio_id:
    raise ValidationError("folio_id es requerido", "folio_id")
```

**Después:**
```python
from fastmcp.exceptions import ToolError

if not folio_id:
    raise ToolError("folio_id es requerido")
```

**Beneficios:**
- Mensajes de error más amigables para clientes
- Integración nativa con FastMCP
- Mejor experiencia de usuario

### 5. Testing In-Memory

**Antes (testing con subprocess):**
```python
# Tests lentos, no determinísticos
subprocess.run(["python", "server.py"])
```

**Después (testing in-memory):**
```python
from fastmcp import Client

async with Client(mcp_server) as client:
    result = await client.call_tool("get_folio", {"folio_id": "12345"})
    assert result is not None
```

**Beneficios:**
- Tests rápidos y determinísticos
- Sin dependencias de red
- Mejor debugging

## Variables de Entorno Nuevas

```bash
# Configuración FastMCP
FASTMCP_LOG_LEVEL=INFO                    # Nivel de logging
FASTMCP_INCLUDE_TRACEBACK=false          # Incluir traceback en logs
FASTMCP_MASK_ERROR_DETAILS=false         # Enmascarar detalles de error
FASTMCP_STRICT_INPUT_VALIDATION=true     # Validación estricta
```

## Estructura de Archivos

```
src/trackhs_mcp/
├── infrastructure/
│   ├── middleware/           # Nuevo: Middleware personalizado
│   │   ├── __init__.py
│   │   ├── error_handling.py
│   │   └── logging.py
│   └── mcp/
│       └── get_folio.py     # Actualizado: Usa ToolError
├── __main__.py              # Actualizado: Configuración mejorada
└── ...

tests/
├── unit/
│   ├── test_middleware.py   # Nuevo: Tests de middleware
│   └── test_validation.py   # Nuevo: Tests de validación
└── integration/
    └── test_mcp_server_inmemory.py  # Nuevo: Tests in-memory

fastmcp.json                 # Nuevo: Configuración declarativa
env.example                  # Actualizado: Nuevas variables
```

## Compatibilidad

### Mantenido Durante Migración
- ✅ `schema_hook` existente (como fallback)
- ✅ `fastmcp.yaml` (para referencia)
- ✅ Tests existentes (sin modificaciones)
- ✅ Funcionamiento desde perspectiva del cliente

### Nuevas Características
- ✅ Configuración declarativa con `fastmcp.json`
- ✅ Middleware de logging y manejo de errores
- ✅ Validación estricta de parámetros
- ✅ Testing in-memory determinístico
- ✅ Manejo de errores mejorado con `ToolError`

## Deployment

### FastMCP Cloud
El archivo `fastmcp.json` es compatible con FastMCP Cloud:

```bash
# Deploy automático desde GitHub
fastmcp cloud deploy
```

### Desarrollo Local
```bash
# Usar configuración declarativa
fastmcp run

# O especificar archivo
fastmcp run --config fastmcp.json
```

### Variables de Entorno
```bash
# Copiar y configurar
cp env.example .env

# Editar .env con tus credenciales
# (NO modificar el archivo .env existente con secretos)
```

## Testing

### Ejecutar Tests Existentes
```bash
# Tests actuales (deben seguir pasando)
pytest tests/unit/
pytest tests/integration/
```

### Ejecutar Nuevos Tests
```bash
# Tests de middleware
pytest tests/unit/test_middleware.py

# Tests de validación
pytest tests/unit/test_validation.py

# Tests in-memory
pytest tests/integration/test_mcp_server_inmemory.py
```

### Suite Completa
```bash
# Todos los tests
pytest tests/ -v --cov=src/trackhs_mcp
```

## Monitoreo y Debugging

### Logs Estructurados
```json
{
  "type": "mcp_request",
  "method": "tools/call",
  "request_id": 1,
  "timestamp": 1640995200.0
}
```

### Estadísticas de Middleware
```python
# Obtener estadísticas de logging
stats = logging_middleware.get_stats()
print(f"Requests: {stats['request_count']}")
print(f"Tiempo promedio: {stats['average_time']}s")

# Obtener estadísticas de errores
error_stats = error_middleware.get_error_stats()
print(f"Errores totales: {error_stats['total_errors']}")
```

## Rollback

Si necesitas hacer rollback:

1. **Revertir `__main__.py`** a la versión anterior
2. **Eliminar middleware** del servidor
3. **Restaurar `fastmcp.yaml`** como configuración principal
4. **Mantener `schema_hook`** activo

## Próximos Pasos

1. **Monitorear** logs y estadísticas en producción
2. **Evaluar** rendimiento de validación estricta
3. **Considerar** eliminar `schema_hook` una vez verificado
4. **Expandir** middleware según necesidades específicas

## Referencias

- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Cloud](https://fastmcp.cloud/)
- [TrackHS API Documentation](https://docs.trackhs.com/)
