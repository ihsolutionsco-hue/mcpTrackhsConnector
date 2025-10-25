<!-- 51b01f74-be21-496f-9d4f-6ba933663a12 9c191fce-9c86-4406-8e0f-1d698a73a407 -->
# Plan de Refactorización: TrackHS MCP Connector

## Objetivo

Simplificar el código eliminando Clean Architecture y aprovechar las características nativas de FastMCP 2.13+, incluyendo middleware nativo, testing con FastMCP Client, y configuración declarativa.

## Estrategia: Refactorización Completa

Refactorización completa de una vez, eliminando toda la arquitectura antigua y reemplazándola con la nueva estructura simplificada basada en FastMCP nativo.

---

## Fase 1: Preparación y Configuración Base

### 1.1 Actualizar Dependencias

**Archivo**: `requirements.txt`

- Actualizar FastMCP a versión 2.13+
- Agregar `inline-snapshot>=0.10.0` para testing
- Agregar `dirty-equals>=0.7.0` para assertions flexibles

**Archivo**: `pyproject.toml`

- Actualizar `dev` dependencies con librerías de testing FastMCP

### 1.2 Crear Configuración Declarativa

**Archivo nuevo**: `fastmcp.json`

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "src/trackhs_mcp/__main__.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.11",
    "requirements": "requirements.txt"
  },
  "transport": {
    "type": "http",
    "port": 8080,
    "host": "0.0.0.0"
  },
  "server": {
    "name": "TrackHS MCP Server",
    "description": "Conector MCP para TrackHS API - IHVM Vacations",
    "version": "2.0.0"
  },
  "logging": {
    "level": "INFO",
    "format": "structured"
  },
  "environment_variables": {
    "required": ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"],
    "optional": ["TRACKHS_API_URL", "TRACKHS_TIMEOUT"]
  }
}
```

### 1.3 Crear Estructura de Directorios Nueva

Crear nueva estructura en `src/trackhs_mcp/`:

```
src/trackhs_mcp/
├── config.py          # Configuración con Pydantic
├── client.py          # Cliente HTTP TrackHS simplificado
├── schemas/           # Schemas Pydantic por tool
│   ├── common.py
│   ├── reservations.py
│   ├── units.py
│   ├── amenities.py
│   ├── folios.py
│   └── work_orders.py
├── tools/             # Tools refactorizados
└── resources/         # Resources simplificados
```

---

## Fase 2: Implementar Configuración y Cliente Base

### 2.1 Crear Configuración Pydantic

**Archivo nuevo**: `src/trackhs_mcp/config.py`

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class TrackHSConfig(BaseSettings):
    username: str = Field(..., description="Usuario TrackHS")
    password: str = Field(..., description="Contraseña TrackHS")
    api_url: str = Field(
        default="https://api.trackhs.com",
        description="URL base de TrackHS API"
    )
    timeout: int = Field(default=30, ge=1, le=300)

    class Config:
        env_prefix = "TRACKHS_"
        case_sensitive = False
```

### 2.2 Crear Cliente HTTP Simplificado

**Archivo nuevo**: `src/trackhs_mcp/client.py`

Consolidar funcionalidad de `infrastructure/adapters/trackhs_api_client.py` en un cliente más simple:

```python
import httpx
from typing import Dict, Any
from .config import TrackHSConfig

class TrackHSClient:
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.api_url,
            auth=(config.username, config.password),
            timeout=config.timeout
        )

    async def get(self, endpoint: str, **params) -> Dict[str, Any]:
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, **json_data) -> Dict[str, Any]:
        response = await self.client.post(endpoint, json=json_data)
        response.raise_for_status()
        return response.json()
```

---

## Fase 3: Crear Schemas Pydantic por Tool

### 3.1 Schemas Comunes

**Archivo nuevo**: `src/trackhs_mcp/schemas/common.py`

Extraer tipos comunes de `domain/entities/base.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional

class PaginationParams(BaseModel):
    page: int = Field(default=0, ge=0, description="Página (0-based)")
    size: int = Field(default=3, ge=1, le=100, description="Resultados por página")

class DateRange(BaseModel):
    start: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    end: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
```

### 3.2 Schema Search Reservations

**Archivo nuevo**: `src/trackhs_mcp/schemas/reservations.py`

Migrar de `domain/entities/reservations.py` pero simplificado:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from .common import PaginationParams

class SearchReservationsRequest(PaginationParams):
    sort_column: Literal["name", "status", "checkin", "checkout"] = "name"
    sort_direction: Literal["asc", "desc"] = "asc"
    status: Optional[str] = None
    arrival_start: Optional[str] = None
    arrival_end: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v:
            valid = ['Hold', 'Confirmed', 'Cancelled', 'Checked In', 'Checked Out']
            statuses = [s.strip() for s in v.split(',')]
            invalid = [s for s in statuses if s not in valid]
            if invalid:
                raise ValueError(f'Invalid statuses: {invalid}')
        return v
```

Repetir patrón similar para:

- `schemas/units.py` (migrar de `domain/entities/units.py`)
- `schemas/amenities.py` (migrar de `domain/entities/amenities.py`)
- `schemas/folios.py` (migrar de `domain/entities/folios.py`)
- `schemas/work_orders.py` (migrar de `domain/entities/work_orders.py`)

---

## Fase 4: Refactorizar Tools con FastMCP Nativo

### 4.1 Tool Search Reservations

**Archivo**: `src/trackhs_mcp/tools/search_reservations.py`

Simplificar eliminando use cases y usar schema directamente:

```python
from fastmcp import FastMCP
from ..schemas.reservations import SearchReservationsRequest
from ..client import TrackHSClient

def register_search_reservations(mcp: FastMCP, client: TrackHSClient):
    @mcp.tool(name="search_reservations")
    async def search_reservations(request: SearchReservationsRequest):
        """Busca reservas en TrackHS API con filtros avanzados."""
        params = request.model_dump(exclude_none=True)
        result = await client.get("/api/v2/pms/reservations", **params)
        return result
```

Aplicar mismo patrón a otros 6 tools:

- `tools/get_reservation.py`
- `tools/search_units.py`
- `tools/search_amenities.py`
- `tools/get_folio.py`
- `tools/create_maintenance_wo.py`
- `tools/create_housekeeping_wo.py`

### 4.2 Registry de Tools Simplificado

**Archivo**: `src/trackhs_mcp/tools/__init__.py`

```python
def register_all_tools(mcp, client):
    from .search_reservations import register_search_reservations
    from .get_reservation import register_get_reservation
    # ... importar otros

    register_search_reservations(mcp, client)
    register_get_reservation(mcp, client)
    # ... registrar otros
```

---

## Fase 5: Implementar Middleware FastMCP Nativo

### 5.1 Actualizar Server Principal

**Archivo**: `src/trackhs_mcp/__main__.py`

Reemplazar middleware personalizado con FastMCP nativo:

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from .config import TrackHSConfig
from .client import TrackHSClient
from .tools import register_all_tools
from .resources import register_all_resources

def create_server() -> FastMCP:
    config = TrackHSConfig()
    client = TrackHSClient(config)

    mcp = FastMCP(
        name="TrackHS MCP Server",
        version="2.0.0",
        strict_input_validation=False  # Pydantic flexible
    )

    # Middleware nativo FastMCP
    mcp.add_middleware(LoggingMiddleware(include_payloads=True))
    mcp.add_middleware(TimingMiddleware())
    mcp.add_middleware(ErrorHandlingMiddleware(transform_errors=True))
    mcp.add_middleware(ResponseCachingMiddleware(ttl=300))

    # Registrar componentes
    register_all_tools(mcp, client)
    register_all_resources(mcp, client)

    return mcp

mcp = create_server()

if __name__ == "__main__":
    mcp.run(transport="http")
```

---

## Fase 6: Simplificar Resources

### 6.1 Resources Esenciales

**Archivo**: `src/trackhs_mcp/resources/__init__.py`

Mantener solo resources de documentación esencial:

```python
def register_all_resources(mcp, client):
    @mcp.resource("trackhs://docs/api")
    def api_documentation():
        return {
            "title": "TrackHS API Documentation",
            "endpoints": [
                {"name": "search_reservations", "url": "/api/v2/pms/reservations"},
                {"name": "search_units", "url": "/api/pms/units"}
            ]
        }

    @mcp.resource("trackhs://examples/reservations")
    def reservation_examples():
        return {
            "search_by_status": {
                "status": "Confirmed",
                "page": 0,
                "size": 5
            }
        }
```

---

## Fase 7: Testing con FastMCP Client

### 7.1 Configurar Testing Framework

**Archivo**: `tests/conftest.py`

Crear fixtures con FastMCP Client:

```python
import pytest
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

@pytest.fixture
async def mcp_client():
    from src.trackhs_mcp.__main__ import mcp
    async with Client(transport=mcp) as client:
        yield client

@pytest.fixture
async def mock_api_client():
    # Mock para tests sin API real
    pass
```

### 7.2 Tests con Inline Snapshots

**Archivo nuevo**: `tests/test_tools.py`

```python
from inline_snapshot import snapshot
import pytest

async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert len(tools) == 7
    assert tools[0].name == "search_reservations"

async def test_search_reservations(mcp_client):
    result = await mcp_client.call_tool(
        "search_reservations",
        {"page": 0, "size": 3, "status": "Confirmed"}
    )
    assert result == snapshot()  # Auto-genera snapshot
```

---

## Fase 8: Limpieza y Eliminación

### 8.1 Eliminar Arquitectura Antigua

Eliminar directorios completos:

- `src/trackhs_mcp/domain/` (completo)
- `src/trackhs_mcp/application/` (completo)
- `src/trackhs_mcp/infrastructure/adapters/` (excepto los migrados)
- `src/trackhs_mcp/infrastructure/utils/` (consolidar en schemas)
- `src/trackhs_mcp/infrastructure/validation/` (migrado a validators Pydantic)
- `src/trackhs_mcp/infrastructure/middleware/` (reemplazado por FastMCP nativo)
- `src/trackhs_mcp/infrastructure/prompts/` (eliminado según requerimientos)

### 8.2 Eliminar Archivos Legacy

Eliminar archivos obsoletos:

- `src/trackhs_mcp/server.py` (reemplazado por `__main__.py`)
- `src/trackhs_mcp/infrastructure/tools/schema_hook.py`
- `src/trackhs_mcp/infrastructure/tools/observability.py`
- Todos los archivos en `infrastructure/tools/resources/prompts/`

---

## Fase 9: Actualizar Documentación

### 9.1 Actualizar README

**Archivo**: `Readme.md`

- Documentar nueva arquitectura simplificada
- Actualizar ejemplos de uso
- Documentar uso de `fastmcp.json`

### 9.2 Crear Guía de Migración

**Archivo nuevo**: `MIGRATION_GUIDE.md`

- Documentar cambios de API
- Explicar nueva estructura
- Guía de actualización para usuarios

---

## Fase 10: Validación Final

### 10.1 Ejecutar Tests

```bash
pytest tests/ --inline-snapshot=create
pytest tests/ --cov=src/trackhs_mcp
```

### 10.2 Validar con FastMCP CLI

```bash
fastmcp inspect src/trackhs_mcp/__main__.py
fastmcp run fastmcp.json
```

### 10.3 Verificar Linting

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

---

## Archivos Clave a Modificar

### Crear Nuevos (16 archivos):

1. `fastmcp.json`
2. `src/trackhs_mcp/config.py`
3. `src/trackhs_mcp/client.py`
4. `src/trackhs_mcp/schemas/common.py`
5. `src/trackhs_mcp/schemas/reservations.py`
6. `src/trackhs_mcp/schemas/units.py`
7. `src/trackhs_mcp/schemas/amenities.py`
8. `src/trackhs_mcp/schemas/folios.py`
9. `src/trackhs_mcp/schemas/work_orders.py`
10. `src/trackhs_mcp/tools/search_reservations.py` (refactorizado)
11. `src/trackhs_mcp/tools/get_reservation.py` (refactorizado)
12. `src/trackhs_mcp/tools/search_units.py` (refactorizado)
13. `src/trackhs_mcp/tools/search_amenities.py` (refactorizado)
14. `src/trackhs_mcp/tools/get_folio.py` (refactorizado)
15. `tests/conftest.py` (refactorizado)
16. `tests/test_tools.py`

### Modificar Existentes (4 archivos):

1. `src/trackhs_mcp/__main__.py` (simplificar con middleware nativo)
2. `requirements.txt` (actualizar FastMCP)
3. `pyproject.toml` (agregar deps testing)
4. `Readme.md` (actualizar documentación)

### Eliminar (50+ archivos en directorios):

- Todo `src/trackhs_mcp/domain/`
- Todo `src/trackhs_mcp/application/`
- La mayoría de `src/trackhs_mcp/infrastructure/`

---

## Orden de Ejecución Recomendado

1. Fase 1: Preparación (actualizar deps, crear `fastmcp.json`)
2. Fase 2: Config y Cliente (crear `config.py`, `client.py`)
3. Fase 3: Schemas (crear todos los schemas en `schemas/`)
4. Fase 4: Tools (refactorizar tools uno por uno)
5. Fase 5: Middleware (actualizar `__main__.py`)
6. Fase 6: Resources (simplificar resources)
7. Fase 7: Testing (crear tests con FastMCP Client)
8. Fase 8: Limpieza (eliminar código legacy)
9. Fase 9: Documentación (actualizar docs)
10. Fase 10: Validación (tests, linting, verificación)

---

## Estimación

- Tiempo estimado: 8-12 horas
- Archivos nuevos: ~16
- Archivos modificados: ~4
- Archivos eliminados: ~50+
- Reducción de código: ~40-50%
- Reducción de complejidad: ~60-70%

### To-dos

- [ ] Fase 1: Actualizar dependencias y crear fastmcp.json
- [ ] Fase 2: Crear config.py y client.py simplificados
- [ ] Fase 3: Crear schemas Pydantic para todos los tools
- [ ] Fase 4: Refactorizar 7 tools con FastMCP nativo
- [ ] Fase 5: Implementar middleware FastMCP nativo en __main__.py
- [ ] Fase 6: Simplificar resources a lo esencial
- [ ] Fase 7: Configurar testing con FastMCP Client e inline-snapshot
- [ ] Fase 8: Eliminar domain/, application/, y código legacy
- [ ] Fase 9: Actualizar README y crear guía de migración
- [ ] Fase 10: Ejecutar tests, linting y validación final