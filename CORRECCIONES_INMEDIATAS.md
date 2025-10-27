# 🔧 Correcciones Inmediatas - TrackHS MCP Server

## Prioridad 🔴 CRÍTICA - Implementar HOY

### 1. Habilitar Middleware (⚠️ CRÍTICO)

**Problema:** El middleware está definido pero no se está usando.

**Ubicación:** `src/trackhs_mcp/server.py`

**Corrección:**

```python
# ANTES (línea 198-218):
mcp = FastMCP(
    name="TrackHS API",
    instructions="""...""",
)

# Inicializar middleware
logging_middleware = LoggingMiddleware()
auth_middleware = AuthenticationMiddleware(api_client)
metrics_middleware = MetricsMiddleware()

# Nota: FastMCP 2.13 no soporta middleware decorators como FastAPI
# El middleware se implementa a nivel de aplicación en las funciones de herramientas

# DESPUÉS:
mcp = FastMCP(
    name="TrackHS API",
    instructions="""...""",
)

# Inicializar middleware
logging_middleware = LoggingMiddleware()
auth_middleware = AuthenticationMiddleware(api_client)
metrics_middleware = MetricsMiddleware()

# 🔧 AGREGAR: Registrar middleware en el servidor
mcp.add_middleware(logging_middleware)
mcp.add_middleware(auth_middleware)
mcp.add_middleware(metrics_middleware)
```

**Después de esta corrección, ELIMINAR el código manual de middleware en todas las herramientas:**

```python
# ELIMINAR estas líneas en search_reservations (líneas ~286-334):
# Aplicar middleware de logging
logging_middleware.request_count += 1
start_time = time.time()

# ... código ...

# Aplicar middleware de métricas
duration = time.time() - start_time
metrics_middleware.metrics["successful_requests"] += 1
# ... etc
```

El middleware ahora se ejecutará automáticamente para todas las herramientas.

---

### 2. Sanitizar Logs de Datos Sensibles (🔴 SEGURIDAD)

**Problema:** Los logs pueden exponer información personal de huéspedes (emails, teléfonos, etc.)

**Ubicación:** `src/trackhs_mcp/server.py`

**Corrección:**

```python
# AGREGAR al inicio del archivo, después de los imports (línea ~60):

# Lista de claves sensibles a ocultar en logs
SENSITIVE_KEYS = {
    'email', 'phone', 'password', 'card', 'ssn', 'creditCard',
    'cvv', 'cardNumber', 'phoneNumber', 'mobilePhone',
    'address', 'zipCode', 'postalCode'
}

def sanitize_for_log(data: Any, max_depth: int = 5) -> Any:
    """
    Oculta datos sensibles para logging seguro.

    Args:
        data: Datos a sanitizar
        max_depth: Profundidad máxima para prevenir recursión infinita

    Returns:
        Datos con información sensible oculta
    """
    if max_depth <= 0:
        return "..."

    if isinstance(data, dict):
        return {
            k: '***REDACTED***' if any(sk in k.lower() for sk in SENSITIVE_KEYS)
            else sanitize_for_log(v, max_depth - 1)
            for k, v in data.items()
        }
    elif isinstance(data, (list, tuple)):
        return [sanitize_for_log(item, max_depth - 1) for item in data]
    elif isinstance(data, str) and len(data) > 500:
        return data[:500] + "... (truncated)"
    return data


# MODIFICAR todas las líneas de logging que imprimen datos:

# ANTES (línea 73):
logger.info(f"GET request to {full_url} with params: {params}")

# DESPUÉS:
logger.info(f"GET request to {full_url} with params: {sanitize_for_log(params)}")

# ANTES (línea 84):
logger.info(f"Response preview (first 500 chars): {response_text[:500]}")

# DESPUÉS:
logger.info(f"Response preview (sanitized): {sanitize_for_log(response_text[:500])}")

# ANTES (línea 127):
logger.info(f"POST request to {full_url} with data: {data}")

# DESPUÉS:
logger.info(f"POST request to {full_url} with data: {sanitize_for_log(data)}")

# Aplicar lo mismo en TODAS las líneas que usan logger.info/debug/error con datos
```

---

## Prioridad 🟡 ALTA - Implementar Esta Semana

### 3. Agregar Validación Estricta de Entrada

**Problema:** La validación de entrada no es estricta, permite coerción de tipos.

**Ubicación:** `src/trackhs_mcp/server.py` línea 198

**Corrección:**

```python
# ANTES:
mcp = FastMCP(
    name="TrackHS API",
    instructions="""Servidor MCP para interactuar con la API de TrackHS...""",
)

# DESPUÉS:
mcp = FastMCP(
    name="TrackHS API",
    instructions="""Servidor MCP para interactuar con la API de TrackHS...""",
    strict_input_validation=True,  # 🔧 Agregar validación estricta
)
```

**Impacto:** Rechazará entradas con tipos incorrectos (ej: `"10"` en lugar de `10`)

---

### 4. Agregar Reintentos HTTP

**Problema:** El cliente HTTP no reintenta en caso de fallos transitorios.

**Ubicación:** `src/trackhs_mcp/server.py`

**Paso 1: Agregar dependencia**

Agregar en `requirements.txt`:
```
tenacity>=8.2.3
```

**Paso 2: Modificar TrackHSClient**

```python
# AGREGAR import al inicio:
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# MODIFICAR clase TrackHSClient:

class TrackHSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)

        # 🔧 Configuración mejorada del cliente
        self.client = httpx.Client(
            auth=self.auth,
            timeout=httpx.Timeout(
                timeout=30.0,
                connect=10.0,
                read=25.0
            ),
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10
            ),
        )
        logger.info(f"TrackHSClient inicializado para {base_url}")

    # 🔧 Agregar decorador de reintentos a get()
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Reintentando request (intento {retry_state.attempt_number}/3)..."
        )
    )
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        # ... código existente sin cambios

    # 🔧 Agregar decorador de reintentos a post()
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Reintentando request (intento {retry_state.attempt_number}/3)..."
        )
    )
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        # ... código existente sin cambios
```

---

## Prioridad 🔵 MEDIA - Implementar Este Mes

### 5. Validación de Respuestas de la API

**Problema:** Las respuestas de la API TrackHS no se validan contra un schema.

**Ubicación:** `src/trackhs_mcp/schemas.py` y `src/trackhs_mcp/server.py`

**Paso 1: Crear modelos Pydantic para respuestas**

Agregar en `src/trackhs_mcp/schemas.py`:

```python
# 🔧 AGREGAR modelos de respuesta validados

from pydantic import BaseModel, Field, validator
from typing import Any, Dict, List, Optional

class ReservationItem(BaseModel):
    """Item individual de reserva"""
    id: int
    confirmationNumber: Optional[str] = Field(None, alias="confirmationNumber")
    status: str
    arrivalDate: Optional[str] = Field(None, alias="arrivalDate")
    departureDate: Optional[str] = Field(None, alias="departureDate")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ReservationSearchResponse(BaseModel):
    """Respuesta validada de búsqueda de reservas"""
    page: int
    page_count: int = Field(alias="page_count")
    page_size: int = Field(alias="page_size")
    total_items: int = Field(alias="total_items")
    _embedded: Dict[str, List[Dict[str, Any]]]
    _links: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True

class UnitSearchResponse(BaseModel):
    """Respuesta validada de búsqueda de unidades"""
    page: int
    page_count: int = Field(alias="page_count")
    page_size: int = Field(alias="page_size")
    total_items: int = Field(alias="total_items")
    _embedded: Dict[str, List[Dict[str, Any]]]
    _links: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True

# Exportar para uso en server.py
__all__ = [
    # ... exportaciones existentes ...
    'ReservationSearchResponse',
    'UnitSearchResponse',
]
```

**Paso 2: Usar modelos en herramientas**

```python
# En server.py, modificar search_reservations:

# IMPORTAR modelos:
from .schemas import (
    # ... imports existentes ...
    ReservationSearchResponse,
    UnitSearchResponse,
)

# ANTES:
def search_reservations(...) -> Dict[str, Any]:
    # ...
    result = api_client.get("pms/reservations", params)
    return result

# DESPUÉS:
def search_reservations(...) -> Dict[str, Any]:
    # ...
    result = api_client.get("pms/reservations", params)

    # 🔧 Validar respuesta
    try:
        validated = ReservationSearchResponse(**result)
        return validated.dict(by_alias=True)
    except Exception as e:
        logger.error(f"Error validando respuesta de API: {e}")
        # Retornar respuesta sin validar como fallback
        return result
```

---

### 6. Agregar Más Tests

**Problema:** Cobertura de tests insuficiente (~40%).

**Ubicación:** Crear nuevos archivos en `tests/`

**Crear:** `tests/test_tools.py`

```python
"""Tests de herramientas individuales del servidor TrackHS MCP"""

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
import sys
from pathlib import Path

src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


class TestTools:
    """Tests de herramientas MCP"""

    @pytest.mark.asyncio
    async def test_search_reservations_schema(self):
        """Test del schema de search_reservations"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            tools = await client.list_tools()
            search_res_tool = next(t for t in tools if t.name == "search_reservations")

            # Verificar que tiene schema de entrada
            assert search_res_tool.inputSchema is not None

            # Verificar parámetros esperados
            properties = search_res_tool.inputSchema.get("properties", {})
            assert "page" in properties
            assert "size" in properties
            assert "search" in properties

    @pytest.mark.asyncio
    async def test_all_tools_have_descriptions(self):
        """Verificar que todas las herramientas tienen descripción"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            tools = await client.list_tools()

            for tool in tools:
                assert tool.description, f"Tool {tool.name} sin descripción"
                assert len(tool.description) > 20, f"Descripción muy corta: {tool.name}"

    @pytest.mark.asyncio
    async def test_tools_have_output_schemas(self):
        """Verificar que las herramientas críticas tienen output schema"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            tools = await client.list_tools()

            # Herramientas que deben tener output schema
            critical_tools = [
                "search_reservations",
                "get_reservation",
                "search_units",
                "search_amenities",
            ]

            for tool_name in critical_tools:
                tool = next(t for t in tools if t.name == tool_name)
                # En MCP, output schemas están en annotations
                assert hasattr(tool, 'annotations') or hasattr(tool, 'outputSchema')
```

**Crear:** `tests/test_error_handling.py`

```python
"""Tests de manejo de errores"""

import pytest
from trackhs_mcp.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError,
)
import sys
from pathlib import Path

src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


class TestErrorHandling:
    """Tests de manejo de errores"""

    def test_authentication_error_hierarchy(self):
        """Verificar jerarquía de excepciones"""
        from trackhs_mcp.exceptions import TrackHSError

        err = AuthenticationError("test")
        assert isinstance(err, TrackHSError)
        assert isinstance(err, Exception)

    def test_all_custom_exceptions_exist(self):
        """Verificar que todas las excepciones personalizadas están definidas"""
        from trackhs_mcp import exceptions

        required_exceptions = [
            'TrackHSError',
            'AuthenticationError',
            'APIError',
            'ValidationError',
            'ConnectionError',
            'NotFoundError',
            'RateLimitError',
        ]

        for exc_name in required_exceptions:
            assert hasattr(exceptions, exc_name), f"Falta excepción: {exc_name}"
```

---

## Prioridad 🟢 BAJA - Mejoras Opcionales

### 7. Agregar Prompts

**Ubicación:** `src/trackhs_mcp/server.py`

**Agregar al final del archivo (antes de health_check):**

```python
# 🔧 AGREGAR Prompts para casos de uso comunes

@mcp.prompt
def search_reservations_by_status(
    status: Annotated[str, Field(description="Estado de reserva")] = "confirmed"
):
    """
    Plantilla para buscar reservas por estado.

    Genera una solicitud para buscar todas las reservas con un estado específico.
    Estados comunes: confirmed, cancelled, checked-in, checked-out, pending
    """
    return f"""Busca todas las reservas con estado '{status}' en el sistema TrackHS.

Usa la herramienta search_reservations con los siguientes parámetros:
- status: {status}
- size: 50 (para obtener más resultados)

Después de obtener los resultados, proporciona un resumen con:
1. Número total de reservas encontradas
2. Lista de las primeras 10 reservas con nombre de huésped y unidad
3. Cualquier patrón observable en las reservas
"""


@mcp.prompt
def upcoming_checkins(
    days: Annotated[int, Field(ge=1, le=90, description="Días hacia adelante")] = 7
):
    """
    Plantilla para ver check-ins próximos.

    Genera una solicitud para ver todas las reservas con check-in en los próximos N días.
    """
    from datetime import datetime, timedelta

    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    return f"""Busca todas las reservas con llegada entre {start_date} y {end_date}.

Usa la herramienta search_reservations con:
- arrival_start: {start_date}
- arrival_end: {end_date}
- status: confirmed
- size: 100

Proporciona un resumen con:
1. Total de llegadas esperadas
2. Llegadas por día
3. Unidades que necesitan preparación
4. Cualquier conflicto o problema potencial
"""


@mcp.prompt
def available_units_summary(
    bedrooms: Annotated[Optional[int], Field(ge=0, le=10)] = None
):
    """
    Plantilla para obtener resumen de unidades disponibles.

    Genera una solicitud para ver todas las unidades disponibles para reservar.
    """
    bedroom_filter = f" con {bedrooms} dormitorios" if bedrooms else ""

    return f"""Obtén un resumen de todas las unidades disponibles para reservar{bedroom_filter}.

Usa la herramienta search_units con:
- is_active: 1
- is_bookable: 1
{f"- bedrooms: {bedrooms}" if bedrooms else ""}
- size: 100

Proporciona un resumen con:
1. Total de unidades disponibles
2. Desglose por tipo (número de dormitorios)
3. Capacidad total disponible
4. Cualquier unidad con características especiales
"""
```

---

### 8. Agregar Recursos Adicionales

**Ubicación:** `src/trackhs_mcp/server.py`

**Agregar después del health_check:**

```python
# 🔧 AGREGAR Recursos informativos

@mcp.resource("trackhs://server/metrics")
def server_metrics():
    """
    Métricas en tiempo real del servidor MCP.

    Proporciona estadísticas de uso y rendimiento del servidor.
    """
    if metrics_middleware is None:
        return {"error": "Metrics middleware not initialized"}

    return {
        "total_requests": metrics_middleware.metrics.get("total_requests", 0),
        "successful_requests": metrics_middleware.metrics.get("successful_requests", 0),
        "failed_requests": metrics_middleware.metrics.get("failed_requests", 0),
        "success_rate": round(
            (metrics_middleware.metrics.get("successful_requests", 0) /
             max(metrics_middleware.metrics.get("total_requests", 1), 1)) * 100,
            2
        ),
        "average_response_time_ms": round(
            metrics_middleware.metrics.get("average_response_time", 0) * 1000,
            2
        ),
        "uptime_seconds": round(
            time.time() - metrics_middleware.metrics.get("start_time", time.time()),
            2
        ),
    }


@mcp.resource("trackhs://api/info")
def api_information():
    """
    Información de la API TrackHS configurada.

    Retorna información sobre la conexión a TrackHS sin exponer credenciales.
    """
    return {
        "base_url": API_BASE_URL,
        "authenticated": api_client is not None,
        "username_configured": API_USERNAME is not None,
        "available_endpoints": [
            "pms/reservations - Búsqueda y gestión de reservas",
            "pms/units - Gestión de unidades de alojamiento",
            "pms/units/amenities - Catálogo de amenidades",
            "pms/maintenance/work-orders - Órdenes de mantenimiento",
            "pms/housekeeping/work-orders - Órdenes de limpieza",
        ],
        "tools_available": 7,
        "version": "2.0.0",
    }


@mcp.resource("trackhs://docs/quick-start")
def quick_start_guide():
    """
    Guía rápida de uso del servidor MCP TrackHS.

    Retorna información de cómo empezar a usar el servidor.
    """
    return """
# Guía Rápida - TrackHS MCP Server

## Herramientas Disponibles

### Búsqueda de Reservas
```
search_reservations(
    page=0,
    size=10,
    search="john@email.com",  # Buscar por email, nombre o confirmación
    arrival_start="2024-01-15",  # Filtrar por fecha de llegada
    status="confirmed"  # Filtrar por estado
)
```

### Obtener Detalles de Reserva
```
get_reservation(reservation_id=12345)
```

### Buscar Unidades
```
search_units(
    page=1,
    size=10,
    bedrooms=2,  # Filtrar por dormitorios
    bathrooms=1,  # Filtrar por baños
    is_bookable=1  # Solo unidades disponibles
)
```

### Buscar Amenidades
```
search_amenities(search="wifi")
```

### Obtener Folio Financiero
```
get_folio(reservation_id=12345)
```

### Crear Orden de Mantenimiento
```
create_maintenance_work_order(
    unit_id=123,
    summary="Grifo con fuga",
    description="El grifo del baño principal gotea",
    priority=3  # 1=Baja, 3=Media, 5=Alta
)
```

### Crear Orden de Limpieza
```
create_housekeeping_work_order(
    unit_id=123,
    scheduled_at="2024-01-15",
    is_inspection=False,
    clean_type_id=1
)
```

## Recursos Disponibles

- `https://trackhs-mcp.local/health` - Estado del servidor
- `trackhs://server/metrics` - Métricas de rendimiento
- `trackhs://api/info` - Información de la API
- `trackhs://docs/quick-start` - Esta guía

## Prompts Útiles

- `search_reservations_by_status` - Buscar por estado
- `upcoming_checkins` - Ver próximas llegadas
- `available_units_summary` - Resumen de disponibilidad

Para más información, consulta la documentación completa.
"""
```

---

## 📋 Checklist de Implementación

### Crítico (HOY)
- [ ] Habilitar middleware con `mcp.add_middleware()`
- [ ] Eliminar código manual de middleware en herramientas
- [ ] Implementar sanitización de logs
- [ ] Aplicar sanitización en todos los logger.info/debug/error

### Alta (Esta Semana)
- [ ] Agregar `strict_input_validation=True`
- [ ] Instalar `tenacity` en requirements.txt
- [ ] Agregar decoradores `@retry` a métodos get() y post()
- [ ] Probar reintentos con conexión intermitente

### Media (Este Mes)
- [ ] Crear modelos Pydantic en schemas.py
- [ ] Implementar validación de respuestas en herramientas
- [ ] Crear test_tools.py
- [ ] Crear test_error_handling.py
- [ ] Ejecutar tests y verificar cobertura

### Baja (Cuando tengas tiempo)
- [ ] Agregar prompts para casos de uso comunes
- [ ] Agregar recursos informativos adicionales
- [ ] Documentar nuevas funcionalidades
- [ ] Actualizar README con ejemplos de prompts

---

## 🧪 Cómo Probar las Correcciones

### 1. Probar Middleware
```bash
# Ejecutar servidor y hacer request
python -m src.trackhs_mcp

# En otra terminal, verificar que los logs muestran:
# - "Middleware: logging_middleware ejecutado"
# - "Middleware: auth_middleware ejecutado"
# - "Middleware: metrics_middleware ejecutado"
```

### 2. Probar Sanitización
```python
# Test manual
from trackhs_mcp.server import sanitize_for_log

test_data = {
    "name": "John Doe",
    "email": "john@example.com",  # Debe ocultarse
    "phone": "555-1234",  # Debe ocultarse
    "reservation_id": 123
}

print(sanitize_for_log(test_data))
# Debe mostrar: {'name': 'John Doe', 'email': '***REDACTED***', 'phone': '***REDACTED***', 'reservation_id': 123}
```

### 3. Probar Reintentos
```python
# Simular fallo de red temporal
# Los reintentos deberían aparecer en logs:
# WARNING - Reintentando request (intento 1/3)...
# WARNING - Reintentando request (intento 2/3)...
```

### 4. Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=src/trackhs_mcp --cov-report=html

# Ver cobertura en navegador
open htmlcov/index.html
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué debo sanitizar los logs?
Los logs pueden contener información personal de huéspedes (emails, teléfonos, direcciones) que no deben estar en archivos de log por regulaciones de privacidad (GDPR, CCPA, etc.).

### ¿Qué pasa si no agrego el middleware?
El servidor funciona, pero:
- Pierdes logging automático
- Pierdes métricas de rendimiento
- Tienes código duplicado en cada herramienta
- Es más difícil mantener

### ¿strict_input_validation rompe algo?
Puede requerir que los clientes envíen tipos exactos en lugar de strings que se convierten. Es más estricto pero más seguro.

### ¿Los reintentos hacen las requests más lentas?
Solo si fallan. En caso de éxito, no hay diferencia. En caso de fallo transitorio, evita reportar error al usuario y puede recuperarse automáticamente.

---

**Fin de Correcciones**

Para dudas o problemas durante la implementación, consulta la auditoría completa en `AUDITORIA_MCP_PROTOCOLO.md`.



