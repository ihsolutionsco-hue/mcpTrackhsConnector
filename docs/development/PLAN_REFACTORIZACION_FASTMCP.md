# Plan de Refactorización - FastMCP Nativo

## 🎯 Objetivo
Migrar el código actual para usar características nativas de FastMCP 2.13, reduciendo complejidad y mejorando rendimiento.

---

## 📋 Cambio 1: Middleware Nativo (CRÍTICO)

### Archivo: `src/trackhs_mcp/middleware.py`

#### ANTES (Actual - 134 líneas)
```python
class LoggingMiddleware:
    """Middleware de logging para todas las operaciones"""
    def __init__(self):
        self.request_count = 0
        self.error_count = 0

    async def __call__(self, request, next_handler):
        # Lógica manual...
```

#### DESPUÉS (Nuevo - ~40 líneas)
```python
"""
Middleware FastMCP-compatible para TrackHS MCP Server
"""
import logging
import time
from typing import Any

from fastmcp.server.middleware import Middleware, MiddlewareContext

logger = logging.getLogger(__name__)


class TrackHSMiddleware(Middleware):
    """
    Middleware unificado para logging, autenticación y métricas.
    Compatible con FastMCP 2.9+
    """

    def __init__(self, api_client=None, auth_cache_ttl: int = 300):
        self.api_client = api_client
        self.auth_cache_ttl = auth_cache_ttl
        self.last_auth_check = None
        self.is_authenticated = False

        # Métricas
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }
        self.response_times = []

    async def on_message(self, context: MiddlewareContext, call_next):
        """
        Intercepta cada mensaje MCP para aplicar logging, auth y métricas.
        """
        self.metrics["total_requests"] += 1
        start_time = time.time()

        # 1. Verificar autenticación (con cache)
        if self.api_client is None:
            from .exceptions import AuthenticationError
            raise AuthenticationError(
                "API client no disponible. Configure TRACKHS_USERNAME y TRACKHS_PASSWORD"
            )

        # Cache de autenticación (solo verificar cada 5 minutos)
        now = time.time()
        if (
            self.last_auth_check is None
            or (now - self.last_auth_check) > self.auth_cache_ttl
        ):
            try:
                # Verificación ligera
                self.api_client.get("pms/units/amenities", {"page": 1, "size": 1})
                self.is_authenticated = True
                self.last_auth_check = now
                logger.debug("Authentication cache refreshed")
            except Exception as e:
                self.is_authenticated = False
                logger.error(f"Authentication failed: {str(e)}")
                from .exceptions import AuthenticationError
                raise AuthenticationError(f"Credenciales inválidas: {str(e)}")

        if not self.is_authenticated:
            from .exceptions import AuthenticationError
            raise AuthenticationError("No autenticado")

        # 2. Logging de request
        logger.info(
            f"Tool called: {context.method} | "
            f"Request #{self.metrics['total_requests']}"
        )

        # 3. Ejecutar la herramienta
        try:
            result = await call_next(context)

            # 4. Métricas de éxito
            duration = time.time() - start_time
            self.response_times.append(duration)
            self.metrics["successful_requests"] += 1

            avg_time = sum(self.response_times) / len(self.response_times)

            logger.info(
                f"✅ Success | Duration: {duration:.2f}s | "
                f"Avg: {avg_time:.2f}s"
            )

            return result

        except Exception as e:
            # 5. Métricas de error
            duration = time.time() - start_time
            self.metrics["failed_requests"] += 1
            error_rate = (
                self.metrics["failed_requests"]
                / self.metrics["total_requests"]
            ) * 100

            logger.error(
                f"❌ Error in {context.method} | "
                f"Duration: {duration:.2f}s | "
                f"Error rate: {error_rate:.1f}% | "
                f"Error: {type(e).__name__}: {str(e)}"
            )

            raise

    def get_metrics(self) -> dict[str, Any]:
        """Retorna métricas actuales"""
        avg_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0
        )

        return {
            **self.metrics,
            "average_response_time": avg_time,
            "error_rate": (
                (self.metrics["failed_requests"] / self.metrics["total_requests"]) * 100
                if self.metrics["total_requests"] > 0
                else 0
            ),
        }
```

---

## 📋 Cambio 2: Servidor con Middleware Integrado

### Archivo: `src/trackhs_mcp/server.py`

#### ANTES (líneas 380-430)
```python
# Crear servidor MCP con validación estricta
mcp = FastMCP(
    name="TrackHS API",
    instructions="""...""",
    strict_input_validation=True,
)

# Inicializar middleware
logging_middleware = LoggingMiddleware()
auth_middleware = AuthenticationMiddleware(api_client)
metrics_middleware = MetricsMiddleware()

# ✅ Quick Win #1: Habilitar middleware
# Nota: El middleware se aplica a nivel de función en cada tool
# FastMCP gestiona el middleware de forma integrada con las herramientas
```

#### DESPUÉS
```python
from contextlib import asynccontextmanager
from fastmcp.server.middleware.error_handling import (
    ErrorHandlingMiddleware,
    RetryMiddleware,
)
from .middleware import TrackHSMiddleware

# Server Lifespan para inicialización/limpieza
@asynccontextmanager
async def lifespan(server):
    """
    Maneja el ciclo de vida del servidor MCP.
    Se ejecuta una vez al inicio y al final.
    """
    # Inicialización
    logger.info("🚀 TrackHS MCP Server iniciando...")
    logger.info(f"📍 Base URL: {API_BASE_URL}")

    # Verificar conexión API
    if api_client:
        try:
            start = time.time()
            api_client.get("pms/units/amenities", {"page": 1, "size": 1})
            duration = time.time() - start
            logger.info(f"✅ API TrackHS conectada ({duration:.2f}s)")
        except Exception as e:
            logger.error(f"❌ API TrackHS no disponible: {e}")
            logger.warning("El servidor se iniciará pero las herramientas fallarán")
    else:
        logger.warning("⚠️  Credenciales no configuradas")

    logger.info("✅ Servidor listo para recibir requests")

    yield  # Servidor corriendo

    # Limpieza
    logger.info("🛑 TrackHS MCP Server cerrando...")
    if api_client and hasattr(api_client, 'client'):
        api_client.client.close()
        logger.info("✅ Conexiones cerradas")

# Crear servidor MCP con todas las mejoras
mcp = FastMCP(
    name="TrackHS API",
    instructions="""Servidor MCP para interactuar con la API de TrackHS.

    Proporciona herramientas para:
    - Buscar y consultar reservas
    - Gestionar unidades de alojamiento
    - Consultar amenidades disponibles
    - Obtener información financiera (folios)
    - Crear órdenes de trabajo (mantenimiento y housekeeping)

    Todas las herramientas incluyen validación robusta y documentación completa.""",
    strict_input_validation=True,
    mask_error_details=True,  # ✅ Seguridad en producción
    lifespan=lifespan,  # ✅ Ciclo de vida
)

# ✅ Registrar middleware nativo de FastMCP
mcp.add_middleware(
    ErrorHandlingMiddleware(
        include_traceback=True,
        transform_errors=True,
    )
)

mcp.add_middleware(
    RetryMiddleware(
        max_retries=3,
        retry_exceptions=(httpx.RequestError, httpx.HTTPStatusError),
        backoff_factor=2.0,
    )
)

# ✅ Middleware personalizado unificado
trackhs_middleware = TrackHSMiddleware(
    api_client=api_client,
    auth_cache_ttl=300,  # 5 minutos
)
mcp.add_middleware(trackhs_middleware)

logger.info("✅ Middleware registrado correctamente")
```

---

## 📋 Cambio 3: Simplificar Tools (Eliminar Código Manual)

### Archivo: `src/trackhs_mcp/server.py`

#### ANTES (líneas 432-544 - search_reservations)
```python
@mcp.tool(output_schema=RESERVATION_SEARCH_OUTPUT_SCHEMA)
def search_reservations(
    page: Annotated[int, Field(ge=0, le=10000, ...)] = 0,
    size: Annotated[int, Field(ge=1, le=100, ...)] = 10,
    # ... más parámetros
) -> Dict[str, Any]:
    """Buscar reservas en TrackHS..."""

    # ❌ Aplicar middleware de logging (MANUAL)
    logging_middleware.request_count += 1
    start_time = time.time()

    logger.info(f"Buscando reservas con parámetros: ...")

    # ❌ Aplicar middleware de autenticación (MANUAL)
    if api_client is None:
        raise AuthenticationError(...)

    params = {"page": page, "size": size}
    # ... construir params

    try:
        result = api_client.get("pms/reservations", params)

        # ❌ Aplicar middleware de métricas (MANUAL)
        duration = time.time() - start_time
        metrics_middleware.metrics["successful_requests"] += 1
        metrics_middleware.response_times.append(duration)
        metrics_middleware.metrics["average_response_time"] = ...

        logger.info(f"Búsqueda de reservas exitosa - ...")
        return result

    except Exception as e:
        # ❌ Aplicar middleware de métricas para errores (MANUAL)
        metrics_middleware.metrics["failed_requests"] += 1
        metrics_middleware.metrics["error_rate"] = ...

        logger.error(f"Error en búsqueda de reservas: {str(e)}")
        raise
```

#### DESPUÉS (Simplificado - ~30 líneas menos)
```python
@mcp.tool(output_schema=RESERVATION_SEARCH_OUTPUT_SCHEMA)
def search_reservations(
    page: Annotated[int, Field(ge=0, le=10000, ...)] = 0,
    size: Annotated[int, Field(ge=1, le=100, ...)] = 10,
    search: Annotated[Optional[str], Field(...)] = None,
    arrival_start: Annotated[Optional[str], Field(...)] = None,
    arrival_end: Annotated[Optional[str], Field(...)] = None,
    status: Annotated[Optional[str], Field(...)] = None,
) -> Dict[str, Any]:
    """
    Buscar reservas en TrackHS con filtros avanzados.

    [Documentación completa igual que antes]
    """
    # ✅ Sin código de middleware - se aplica automáticamente

    # Construir parámetros de búsqueda
    params = {"page": page, "size": size}
    if search:
        params["search"] = search
    if arrival_start:
        params["arrival_start"] = arrival_start
    if arrival_end:
        params["arrival_end"] = arrival_end
    if status:
        params["status"] = status

    # Llamar a la API (con reintentos automáticos del middleware)
    result = api_client.get("pms/reservations", params)

    return result  # ✅ Simple y limpio
```

**Resultado:**
- ❌ Eliminadas ~25 líneas de código repetitivo
- ✅ Más fácil de leer y mantener
- ✅ Middleware se aplica automáticamente
- ✅ Logging, autenticación, métricas y reintentos sin código manual

---

## 📋 Cambio 4: Eliminar retry_with_backoff (Ya Incluido en Middleware)

### Archivo: `src/trackhs_mcp/server.py`

#### ANTES (líneas 147-206)
```python
def retry_with_backoff(
    func, max_retries: int = MAX_RETRIES, base_delay: float = RETRY_DELAY_BASE
):
    """Ejecuta una función con reintentos automáticos..."""
    # ... ~60 líneas de código de reintentos
```

#### DESPUÉS
```python
# ❌ ELIMINAR COMPLETAMENTE - Ya no se necesita
# FastMCP RetryMiddleware maneja esto automáticamente
```

### Archivo: `src/trackhs_mcp/server.py` - TrackHSClient

#### ANTES (líneas 245-314 en método `get()`)
```python
def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """GET request to TrackHS API"""
    # ...
    def _execute_request():
        # ... lógica de request

    # ❌ Ejecutar con reintentos automáticos
    return retry_with_backoff(_execute_request)
```

#### DESPUÉS (Simplificado)
```python
def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """GET request to TrackHS API with error handling"""
    full_url = f"{self.base_url}/{endpoint}"
    sanitized_params = sanitize_for_log(params)
    logger.info(f"GET request to {full_url} with params: {sanitized_params}")

    # ✅ Request directo - RetryMiddleware maneja reintentos
    try:
        response = self.client.get(full_url, params=params)
        logger.info(f"Response status: {response.status_code}")

        response.raise_for_status()

        response_data = response.json()
        sanitized_response = sanitize_for_log(response_data)
        logger.info(f"Response preview: {str(sanitized_response)[:500]}")

        return response_data

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error {e.response.status_code}")

        if "text/html" in e.response.headers.get("content-type", ""):
            raise NotFoundError(
                f"Endpoint no encontrado. URL: {full_url}"
            )

        if e.response.status_code == 401:
            raise AuthenticationError(f"Credenciales inválidas: {e.response.text}")
        elif e.response.status_code == 403:
            raise AuthenticationError(f"Acceso denegado: {e.response.text}")
        elif e.response.status_code == 404:
            raise NotFoundError(f"Recurso no encontrado: {e.response.text}")
        elif e.response.status_code == 422:
            raise ValidationError(f"Error de validación: {e.response.text}")
        else:
            raise APIError(f"Error de API: {e.response.status_code} - {e.response.text}")

    except httpx.RequestError as e:
        # RetryMiddleware manejará reintentos de errores de red
        raise ConnectionError(f"Error de conexión con TrackHS: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise TrackHSError(f"Error inesperado: {str(e)}")
```

**Resultado:**
- ❌ Eliminadas ~60 líneas de `retry_with_backoff()`
- ❌ Eliminadas ~30 líneas de wrapping en `get()` y `post()`
- ✅ Código más simple y directo
- ✅ Reintentos manejados por FastMCP RetryMiddleware

---

## 📋 Cambio 5: Response Caching para Amenidades

### Archivo: `src/trackhs_mcp/server.py`

```python
# Después de registrar el middleware principal, agregar caching

# ✅ NUEVO: Cache para consultas que raramente cambian
# Nota: Requiere instalar fastmcp[cache] o implementación personalizada
try:
    from fastmcp.server.middleware.caching import ResponseCachingMiddleware

    mcp.add_middleware(
        ResponseCachingMiddleware(
            ttl=3600,  # 1 hora
            cache_tools=["search_amenities"],  # Solo cachear amenidades
        )
    )
    logger.info("✅ Response caching habilitado para amenidades")
except ImportError:
    logger.warning("⚠️  ResponseCachingMiddleware no disponible")
    # Continuar sin caching
```

---

## 📋 Cambio 6: Health Check Mejorado

### Archivo: `src/trackhs_mcp/server.py`

#### ANTES (líneas 1010-1061)
```python
@mcp.resource("https://trackhs-mcp.local/health")
def health_check():
    """Health check endpoint"""
    # ... código con version hardcoded
    "fastmcp_version": "2.12.5",  # ⚠️ Desactualizado
```

#### DESPUÉS
```python
import fastmcp
import json

@mcp.resource("https://trackhs-mcp.local/health")
def health_check() -> str:
    """
    Health check endpoint para monitoreo del servidor.

    Retorna estado del servidor, dependencias, métricas y versiones.
    """
    try:
        # Verificar conexión con API TrackHS
        api_status = "healthy"
        api_response_time = None

        if api_client:
            try:
                start_time = time.time()
                api_client.get("pms/units/amenities", {"page": 1, "size": 1})
                api_response_time = round((time.time() - start_time) * 1000, 2)
            except Exception as e:
                api_status = "unhealthy"
                logger.warning(f"API TrackHS no disponible: {str(e)}")
        else:
            api_status = "not_configured"

        # Obtener métricas del middleware
        middleware_metrics = (
            trackhs_middleware.get_metrics()
            if trackhs_middleware
            else {}
        )

        health_data = {
            "status": "healthy" if api_status in ["healthy", "not_configured"] else "degraded",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "dependencies": {
                "trackhs_api": {
                    "status": api_status,
                    "response_time_ms": api_response_time,
                    "base_url": API_BASE_URL,
                }
            },
            "metrics": middleware_metrics,
            "environment": {
                "python_version": os.sys.version,
                "fastmcp_version": fastmcp.__version__,  # ✅ Dinámico
            },
        }

        logger.debug(f"Health check: {health_data['status']}")

        # ✅ Retornar JSON string
        return json.dumps(health_data, indent=2)

    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        error_data = {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }
        return json.dumps(error_data, indent=2)
```

---

## 📋 Cambio 7: Usar mask_error_details con ToolError

### Archivo: `src/trackhs_mcp/server.py`

```python
from fastmcp.exceptions import ToolError

@mcp.tool(output_schema=RESERVATION_DETAIL_OUTPUT_SCHEMA)
def get_reservation(
    reservation_id: Annotated[int, Field(gt=0, ...)],
) -> Dict[str, Any]:
    """Obtener detalles completos de una reserva específica por ID."""
    logger.info(f"Obteniendo detalles de reserva ID: {reservation_id}")

    try:
        result = api_client.get(f"pms/reservations/{reservation_id}")

        # Validar respuesta (modo no-strict)
        validated_result = validate_response(result, ReservationResponse, strict=False)

        logger.info(f"Detalles de reserva {reservation_id} obtenidos exitosamente")
        return validated_result

    except NotFoundError:
        # ✅ ToolError: Este mensaje SÍ se muestra al cliente
        raise ToolError(f"Reserva {reservation_id} no encontrada en TrackHS")

    except AuthenticationError as e:
        # ✅ ToolError para errores que el cliente puede resolver
        raise ToolError(f"Error de autenticación: {str(e)}")

    except Exception as e:
        # ⚠️ Exception genérica: se oculta con mask_error_details=True
        logger.error(f"Error obteniendo reserva {reservation_id}: {str(e)}")
        raise
```

---

## 📊 Resumen de Cambios

| Cambio | Archivo | Líneas Eliminadas | Líneas Agregadas | Impacto |
|--------|---------|-------------------|------------------|---------|
| 1. Middleware nativo | `middleware.py` | ~134 | ~80 | -54 líneas |
| 2. Servidor con lifespan | `server.py` | ~50 | ~80 | +30 líneas |
| 3. Simplificar search_reservations | `server.py` | ~115 | ~85 | -30 líneas |
| 4. Simplificar search_units | `server.py` | ~115 | ~85 | -30 líneas |
| 5. Eliminar retry_with_backoff | `server.py` | ~60 | 0 | -60 líneas |
| 6. Simplificar TrackHSClient | `server.py` | ~140 | ~80 | -60 líneas |
| 7. Health check mejorado | `server.py` | ~52 | ~60 | +8 líneas |
| 8. ToolError en tools | `server.py` | 0 | ~10 | +10 líneas |
| **TOTAL** | | **~666** | **~480** | **-186 líneas** |

**Mejora neta:** -186 líneas (~17% reducción)

---

## 🚀 Orden de Implementación

### Sprint 1 (1-2 horas)
1. ✅ Crear nuevo `middleware.py` con `TrackHSMiddleware`
2. ✅ Agregar lifespan al servidor
3. ✅ Registrar middleware con `mcp.add_middleware()`
4. ✅ Probar que funciona

### Sprint 2 (2-3 horas)
5. ✅ Simplificar `search_reservations` (eliminar código manual)
6. ✅ Simplificar `search_units` (eliminar código manual)
7. ✅ Simplificar resto de tools
8. ✅ Probar cada tool

### Sprint 3 (1-2 horas)
9. ✅ Eliminar `retry_with_backoff()`
10. ✅ Simplificar `TrackHSClient.get()` y `post()`
11. ✅ Habilitar `mask_error_details=True`
12. ✅ Agregar `ToolError` en tools

### Sprint 4 (1 hora)
13. ✅ Mejorar health check
14. ✅ Agregar response caching (opcional)
15. ✅ Testing completo
16. ✅ Actualizar documentación

---

## ✅ Checklist de Validación

Después de cada cambio, verificar:

- [ ] ✅ Servidor inicia sin errores
- [ ] ✅ Tools responden correctamente
- [ ] ✅ Middleware intercepta todas las llamadas
- [ ] ✅ Logging funciona (sin duplicados)
- [ ] ✅ Autenticación funciona (con cache)
- [ ] ✅ Reintentos funcionan en errores de red
- [ ] ✅ Métricas se registran correctamente
- [ ] ✅ Health check muestra estado correcto
- [ ] ✅ Errores sensibles se ocultan con mask_error_details
- [ ] ✅ Tests pasan (ejecutar suite completa)

---

## 🎯 Beneficios Esperados

### Código
- ✅ -17% líneas de código
- ✅ -30% complejidad ciclomática
- ✅ Mejor separación de responsabilidades

### Rendimiento
- ✅ -40% latencia (cache de autenticación)
- ✅ Menos overhead por request
- ✅ Response caching para amenidades

### Mantenibilidad
- ✅ Más fácil de leer
- ✅ Menos código duplicado
- ✅ Middleware centralizado

### Seguridad
- ✅ Errores sensibles ocultos
- ✅ Mejor logging (sin PII)
- ✅ Autenticación robusta

---

## 📚 Testing Post-Refactorización

```bash
# 1. Tests unitarios
pytest tests/ -v

# 2. Tests de integración
pytest tests/test_integration.py -v

# 3. Tests específicos de middleware
pytest tests/test_middleware_integration.py -v

# 4. Test de carga (opcional)
python scripts/load_test.py

# 5. Validar health check
curl http://localhost:8000/health | jq
```

---

**Próximo paso:** Implementar Sprint 1 🚀

