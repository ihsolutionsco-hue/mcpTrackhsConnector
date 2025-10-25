# Guía de Migración: TrackHS MCP v1 → v2

## 🎯 Resumen de Cambios

La versión 2.0 elimina completamente Clean Architecture y simplifica a FastMCP nativo con schemas integrados.

## 📊 Comparación v1 vs v2

| Aspecto | v1 (Clean Architecture) | v2 (FastMCP Nativo) |
|---------|-------------------------|---------------------|
| **Archivos** | 50+ archivos | ~15 archivos |
| **Líneas de código** | 2000+ líneas | <800 líneas |
| **Capas** | domain/application/infrastructure | tools/ directos |
| **Schemas** | Separados en domain/ | Integrados en tools/ |
| **Cliente HTTP** | Abstracciones complejas | httpx directo |
| **Middleware** | Custom + FastMCP | Solo FastMCP nativo |
| **Testing** | Tests complejos | FastMCP Client |

## 🗂️ Mapeo de Archivos

### Eliminados (v1 → v2)

```
❌ src/trackhs_mcp/domain/          → Eliminado
❌ src/trackhs_mcp/application/     → Eliminado  
❌ src/trackhs_mcp/infrastructure/ → Eliminado
❌ src/trackhs_mcp/server.py       → Eliminado
❌ tests/mcp_protocol/             → Eliminado
❌ tests/middleware/               → Eliminado
❌ tests/performance/              → Eliminado
```

### Nuevos (v2)

```
✅ src/trackhs_mcp/config.py       → Configuración Pydantic
✅ src/trackhs_mcp/client.py       → Cliente HTTP simple
✅ src/trackhs_mcp/tools/          → Tools agrupados por dominio
✅ tests/conftest.py               → Fixtures FastMCP Client
✅ tests/test_*.py                 → Tests simplificados
```

### Modificados

```
🔄 src/trackhs_mcp/__main__.py     → FastMCP nativo
🔄 requirements.txt                → Dependencias actualizadas
🔄 pyproject.toml                  → Configuración simplificada
🔄 README.md                       → Documentación actualizada
```

## 🔄 Mapeo de Tools

### Reservations

**v1**: `infrastructure/tools/search_reservations_v2.py` + `get_reservation_v2.py`
**v2**: `tools/reservations.py` (ambos tools en un archivo)

```python
# v1 (separado)
from trackhs_mcp.infrastructure.tools.search_reservations_v2 import wrapped_search_reservations_v2
from trackhs_mcp.infrastructure.tools.get_reservation_v2 import wrapped_get_reservation_v2

# v2 (integrado)
from trackhs_mcp.tools.reservations import register_reservation_tools
```

### Units

**v1**: `infrastructure/tools/search_units.py`
**v2**: `tools/units.py`

### Amenities

**v1**: `infrastructure/tools/search_amenities.py`
**v2**: `tools/amenities.py`

### Folios

**v1**: `infrastructure/tools/get_folio.py`
**v2**: `tools/folios.py`

### Maintenance

**v1**: `infrastructure/tools/create_maintenance_work_order.py` + `create_housekeeping_work_order.py`
**v2**: `tools/maintenance.py` (ambos tools en un archivo)

## 🏗️ Cambios en Arquitectura

### v1: Clean Architecture

```
┌─────────────────┐
│   Domain Layer  │ ← Entities, Value Objects
├─────────────────┤
│ Application     │ ← Use Cases, Ports
├─────────────────┤
│ Infrastructure  │ ← Adapters, Tools, Config
└─────────────────┘
```

### v2: FastMCP Nativo

```
┌─────────────────┐
│   __main__.py   │ ← FastMCP Server
├─────────────────┤
│   tools/        │ ← Tools + Schemas
├─────────────────┤
│   client.py     │ ← HTTP Client
├─────────────────┤
│   config.py     │ ← Pydantic Settings
└─────────────────┘
```

## 📝 Cambios en Schemas

### v1: Schemas Separados

```python
# domain/entities/reservations.py
class SearchReservationsParams(BaseModel):
    page: int = Field(default=0)
    size: int = Field(default=3)

# infrastructure/tools/search_reservations_v2.py
from trackhs_mcp.domain.entities.reservations import SearchReservationsParams
```

### v2: Schemas Integrados

```python
# tools/reservations.py
class SearchReservationsRequest(BaseModel):
    page: int = Field(default=0, ge=0, description="Página (0-based)")
    size: int = Field(default=3, ge=1, le=100, description="Resultados. Voz: 3-5")
```

## 🔧 Cambios en Cliente HTTP

### v1: Abstracciones Complejas

```python
# infrastructure/adapters/trackhs_api_client.py
class TrackHSApiClient:
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self.session = httpx.AsyncClient()
    
    async def search_reservations(self, params: SearchReservationsParams):
        # Lógica compleja de autenticación y manejo de errores
```

### v2: Cliente Simple

```python
# client.py
class TrackHSClient:
    def __init__(self):
        self.base_url = settings.trackhs_api_url
        self.auth = (settings.trackhs_username, settings.trackhs_password)
    
    async def get(self, endpoint: str, params: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params, auth=self.auth)
            response.raise_for_status()
            return response.json()
```

## 🧪 Cambios en Testing

### v1: Tests Complejos

```python
# tests/mcp_protocol/test_tools.py
class TestMCPTools:
    def setup_method(self):
        self.mcp_server = create_mcp_server()
        self.client = MCPClient(self.mcp_server)
    
    async def test_search_reservations(self):
        # Tests complejos con mocks y fixtures
```

### v2: Tests Simplificados

```python
# tests/test_reservations.py
async def test_search_reservations(mcp_client):
    result = await mcp_client.call_tool("search_reservations", {
        "page": 0, "size": 3, "status": "Confirmed"
    })
    assert result is not None
```

## ⚙️ Cambios en Configuración

### v1: Configuración Compleja

```python
# infrastructure/adapters/config.py
class TrackHSConfig:
    def __init__(self):
        self.api_url = os.getenv("TRACKHS_API_URL")
        self.username = os.getenv("TRACKHS_USERNAME")
        # Validación manual
```

### v2: Pydantic Settings

```python
# config.py
class Settings(BaseSettings):
    trackhs_api_url: str
    trackhs_username: str
    trackhs_password: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

## 🚀 Migración Paso a Paso

### 1. Backup del Proyecto v1

```bash
cp -r trackhs-mcp trackhs-mcp-v1-backup
```

### 2. Actualizar Dependencias

```bash
pip install fastmcp>=0.4.0 pydantic-settings>=2.0.0
```

### 3. Crear Nueva Estructura

```bash
mkdir -p src/trackhs_mcp/tools
mkdir -p tests
```

### 4. Migrar Tools

Para cada tool:
1. Crear archivo en `tools/`
2. Mover schema de `domain/` a `tools/`
3. Simplificar implementación
4. Agregar logging estructurado

### 5. Actualizar Tests

```bash
# Eliminar tests antiguos
rm -rf tests/mcp_protocol/ tests/middleware/ tests/performance/

# Crear tests nuevos
pytest tests/ -v
```

### 6. Verificar Funcionamiento

```bash
python -m src.trackhs_mcp
```

## 🔍 Verificación Post-Migración

### Checklist

- [ ] Servidor inicia sin errores
- [ ] Todos los tools funcionan
- [ ] Tests pasan
- [ ] Logging estructurado funciona
- [ ] Configuración desde .env
- [ ] Cliente HTTP responde
- [ ] Middleware funciona

### Comandos de Verificación

```bash
# 1. Verificar estructura
ls -la src/trackhs_mcp/

# 2. Ejecutar tests
pytest tests/ -v

# 3. Verificar servidor
python -m src.trackhs_mcp

# 4. Verificar logs
tail -f logs/trackhs-mcp.log
```

## 🎯 Beneficios de la Migración

### Reducción de Complejidad

- **Archivos**: 50+ → 15 (-70%)
- **Líneas**: 2000+ → 800 (-60%)
- **Capas**: 3 → 1 (-67%)
- **Dependencias**: 15+ → 5 (-67%)

### Mejoras en Mantenibilidad

- **Código más directo**: Sin abstracciones innecesarias
- **Debugging más fácil**: Logs estructurados
- **Testing más simple**: FastMCP Client
- **Configuración centralizada**: Pydantic Settings

### Performance

- **Menos overhead**: Sin capas de abstracción
- **Startup más rápido**: Menos imports
- **Memoria optimizada**: Menos objetos en memoria

## 🚨 Consideraciones

### Breaking Changes

- **Imports**: Todos los imports de domain/application/infrastructure fallarán
- **Configuración**: Cambiar de TrackHSConfig a Settings
- **Testing**: Cambiar de MCPClient a FastMCP Client
- **Middleware**: Cambiar de custom a FastMCP nativo

### Compatibilidad

- **Python**: Mantiene >=3.8
- **FastMCP**: Actualiza a >=0.4.0
- **Pydantic**: Mantiene >=2.0.0
- **httpx**: Actualiza a >=0.27.0

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisa los logs del servidor
2. Verifica la configuración de .env
3. Ejecuta los tests para identificar errores
4. Consulta la documentación de FastMCP

## 🎉 Conclusión

La migración a v2.0 simplifica significativamente el código manteniendo toda la funcionalidad. El resultado es un servidor MCP más rápido, fácil de mantener y con menos complejidad.
