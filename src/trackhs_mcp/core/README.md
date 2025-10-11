# Utilidades de Soporte - Track HS MCP Connector

Este directorio contiene las utilidades de soporte para el Track HS MCP Connector, incluyendo paginación, logging, completion y manejo de errores.

## Estructura de Archivos

### Utilidades Principales

1. **`pagination.py`** - Utilidad de paginación robusta
2. **`logging.py`** - Sistema de logging avanzado
3. **`completion.py`** - Utilidad de completion inteligente
4. **`error_handling.py`** - Manejo robusto de errores

### Archivos de Soporte

- **`api_client.py`** - Cliente HTTP para la API de Track HS
- **`auth.py`** - Autenticación Basic Auth
- **`types.py`** - Tipos base y configuración

## Utilidades de Soporte

### 1. Paginación (`pagination.py`)

**Descripción:** Utilidad robusta para manejar paginación estándar y scroll de Elasticsearch.

**Características:**
- Soporte para paginación estándar y scroll
- Manejo de grandes conjuntos de datos (hasta 10k resultados)
- Configuración flexible de límites y timeouts
- Iteradores asíncronos para procesamiento eficiente
- Cache de scroll con TTL
- Validación de parámetros de paginación

**Clases Principales:**
- `PaginationUtility` - Utilidad principal de paginación
- `PaginationConfig` - Configuración de paginación
- `PageInfo` - Información de página
- `PaginationResult` - Resultado de paginación

**Ejemplo de Uso:**
```python
from trackhs_mcp.core.pagination import PaginationUtility, PaginationConfig, PaginationMode

# Configurar paginación
config = PaginationConfig(
    mode=PaginationMode.SCROLL,
    max_page_size=1000,
    max_total_results=10000
)

# Usar utilidad
pagination = PaginationUtility(config)

# Paginar resultados
async for result in pagination.paginate_async(api_client, "/v2/pms/reservations", params):
    # Procesar resultados
    pass
```

### 2. Logging (`logging.py`)

**Descripción:** Sistema de logging avanzado con contexto, métricas e integración MCP.

**Características:**
- Niveles de logging personalizados (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Categorías de logs (API_REQUEST, MCP_TOOL, AUTHENTICATION, etc.)
- Contexto de logging con request_id, user_id, session_id
- Métricas de rendimiento integradas
- Integración con MCP para envío de logs
- Context managers para tracking automático
- Logging estructurado con JSON

**Clases Principales:**
- `TrackHSLogger` - Logger principal con contexto
- `RequestContext` - Context manager para tracking
- `PerformanceTimer` - Medición de rendimiento
- `LogContext` - Contexto de logging
- `LogMetric` - Métrica de logging

**Ejemplo de Uso:**
```python
from trackhs_mcp.core.logging import get_logger, RequestContext, PerformanceTimer

# Obtener logger
logger = get_logger(__name__)

# Usar contexto de request
with RequestContext(request_id="123", user_id="user456"):
    logger.log_api_request("GET", "/v2/pms/reservations", params)

# Medir rendimiento
with PerformanceTimer(logger, "search_reservations"):
    result = await search_reservations(...)
```

### 3. Completion (`completion.py`)

**Descripción:** Utilidad de completion inteligente para sugerencias y autocompletado.

**Características:**
- Sugerencias de parámetros para la API V2
- Autocompletado de valores (estados, fechas, IDs)
- Cache inteligente con TTL
- Sugerencias dinámicas desde la API
- Filtrado y ordenamiento de sugerencias
- Soporte para múltiples tipos de completion

**Clases Principales:**
- `TrackHSCompletion` - Sistema de completion principal
- `CompletionSuggestion` - Sugerencia de completion
- `CompletionContext` - Contexto para completion
- `CompletionType` - Tipos de completion

**Ejemplo de Uso:**
```python
from trackhs_mcp.core.completion import TrackHSCompletion, CompletionContext

# Crear sistema de completion
completion = TrackHSCompletion(api_client)

# Obtener sugerencias
context = CompletionContext(
    current_input="conf",
    parameter_name="status"
)
suggestions = await completion.get_completions(context)
```

### 4. Manejo de Errores (`error_handling.py`)

**Descripción:** Manejo robusto de errores según especificación RFC 7807.

**Características:**
- Manejo de errores según especificación RFC 7807
- Tipos de error específicos (API, autenticación, validación, red, etc.)
- Estrategias de reintento configurables
- Severidad de errores (LOW, MEDIUM, HIGH, CRITICAL)
- Logging automático de errores
- Respuestas estructuradas para MCP
- Decoradores para manejo automático

**Clases Principales:**
- `TrackHSError` - Error personalizado
- `TrackHSErrorHandler` - Manejador principal
- `APIErrorResponse` - Respuesta de error de API
- `ErrorType` - Tipos de error
- `ErrorSeverity` - Severidad de errores

**Ejemplo de Uso:**
```python
from trackhs_mcp.core.error_handling import error_handler, TrackHSErrorHandler

# Usar decorador para manejo automático
@error_handler("search_reservations")
async def search_reservations_safe():
    # Código que puede fallar
    pass

# Manejo manual de errores
handler = TrackHSErrorHandler()
try:
    result = await api_call()
except Exception as e:
    error = handler.handle_network_error(e)
    return handler.format_error_response(error)
```

## Funciones de Conveniencia

### Paginación
```python
from trackhs_mcp.core.pagination import paginate_reservations, get_paginated_summary

# Paginar reservaciones
all_reservations = await paginate_reservations(api_client, params)

# Obtener resumen
summary = await get_paginated_summary(api_client, params)
```

### Logging
```python
from trackhs_mcp.core.logging import log_api_call, log_tool_call

# Log de API call
log_api_call(logger, "GET", "/v2/pms/reservations", params)

# Log de tool call
log_tool_call(logger, "search_reservations", params, duration_ms, success)
```

### Completion
```python
from trackhs_mcp.core.completion import get_parameter_completions, get_endpoint_completions

# Obtener completions de parámetros
suggestions = await get_parameter_completions(api_client, "status", "conf")

# Obtener completions de endpoints
endpoints = await get_endpoint_completions("/v2/pms/")
```

### Manejo de Errores
```python
from trackhs_mcp.core.error_handling import handle_api_error, format_error_for_mcp

# Manejar error de API
error = handle_api_error(response_data, status_code)

# Formatear error para MCP
mcp_response = format_error_for_mcp(error)
```

## Configuración Recomendada

### 1. Paginación
```python
# Para conjuntos pequeños
config = PaginationConfig(
    mode=PaginationMode.STANDARD,
    max_page_size=100,
    max_total_results=1000
)

# Para conjuntos grandes
config = PaginationConfig(
    mode=PaginationMode.SCROLL,
    max_page_size=1000,
    max_total_results=10000,
    scroll_timeout="2m"
)
```

### 2. Logging
```python
# Configurar logger con contexto
logger = get_logger("trackhs_mcp", mcp_client)

# Usar context managers
with RequestContext(request_id="123", user_id="user456"):
    logger.info("Processing request")
```

### 3. Completion
```python
# Configurar completion con cache
completion = TrackHSCompletion(api_client)
completion._cache_duration = timedelta(hours=2)  # Cache por 2 horas
```

### 4. Manejo de Errores
```python
# Configurar estrategias de reintento
handler = TrackHSErrorHandler()
handler.retry_strategies[ErrorType.NETWORK_ERROR] = {
    "max_retries": 5,
    "backoff_factor": 2
}
```

## Mejores Prácticas

1. **Usar context managers** para logging y tracking
2. **Implementar manejo de errores** en todas las operaciones
3. **Configurar paginación** según el tamaño de datos esperado
4. **Usar completion** para mejorar experiencia de usuario
5. **Monitorear métricas** de rendimiento y errores

## Troubleshooting

### Problemas de Paginación
- **Error de límite:** Reducir `max_total_results` o usar scroll
- **Timeout de scroll:** Reducir `scroll_timeout` o procesar más rápido

### Problemas de Logging
- **Logs duplicados:** Verificar configuración de handlers
- **Falta de contexto:** Usar `RequestContext` correctamente

### Problemas de Completion
- **Sugerencias lentas:** Verificar cache y TTL
- **Sugerencias incorrectas:** Verificar configuración de API

### Problemas de Errores
- **Errores no manejados:** Verificar decoradores y try/catch
- **Reintentos excesivos:** Ajustar estrategias de reintento
