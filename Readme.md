# TrackHS MCP Connector - API V2

Servidor MCP (Model Context Protocol) para Track HS API V2 implementado con FastMCP en Python.

## 🚀 Características

- **1 Herramienta Principal** - `search_reservations` con capacidades completas de API V2
- **4 Resources** con esquemas y documentación actualizados
- **5 Prompts** predefinidos para casos de uso comunes
- **Autenticación Basic Auth** integrada
- **Validación de tipos** con Pydantic V2
- **Cliente HTTP** robusto con manejo de errores
- **Utilidades de soporte** (paginación, logging, completion, errores)
- **Testing Completo** - Tests unitarios, integración y E2E
- **Deployment Automático** - CI/CD con GitHub Actions y FastMCP Cloud

## 📋 Herramienta Principal

### Search Reservations V2
- **`search_reservations`** - ⭐ **HERRAMIENTA PRINCIPAL** - Búsqueda avanzada de reservas con todos los parámetros de la API V2
  - Filtros de fecha completos (booked, arrival, departure)
  - Filtros por ID múltiples (node, unit, contact, etc.)
  - Paginación estándar y scroll de Elasticsearch
  - Ordenamiento avanzado
  - Búsqueda de texto
  - Filtros especiales (inHouseToday, status, tags, etc.)

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- FastMCP 2.0+
- Credenciales de Track HS API

### Instalación Local

```bash
# Clonar el repositorio
git clone <repository-url>
cd MCPtrackhsConnector

# Instalar dependencias
pip install -r requirements.txt

# O usar uv (recomendado)
uv pip install -r requirements.txt
```

### Configuración

1. Crear archivo `.env` en la raíz del proyecto:
```bash
touch .env
```

2. Configurar las variables de entorno en `.env`:
```env
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
TRACKHS_TIMEOUT=30
```

## 🚀 Uso

### Desarrollo Local

```bash
# Ejecutar servidor en modo desarrollo
fastmcp dev

# O ejecutar directamente
python -m src.trackhs_mcp.server

# Con variables de entorno específicas
TRACKHS_USERNAME=usuario TRACKHS_PASSWORD=contraseña python -m src.trackhs_mcp.server
```

### Configuración en Claude Desktop

1. Crear archivo de configuración `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "src.trackhs_mcp.server"],
      "cwd": "/ruta/al/proyecto",
      "env": {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

2. Reiniciar Claude Desktop

## 📚 Recursos MCP

- `trackhs://schema/reservations` - Esquema completo de reservas V2
- `trackhs://api/v2/endpoints` - Endpoints disponibles en API V2
- `trackhs://api/v2/parameters` - Parámetros de la API V2
- `trackhs://api/v2/examples` - Ejemplos de uso de la API V2
- `trackhs://status/system` - Estado del sistema y conectividad
- `trackhs://docs/api` - Documentación completa de la API V2

## 🎯 Prompts Predefinidos

- `check-today-reservations` - Revisar reservas de hoy usando API V2
- `advanced-reservation-search` - Búsqueda avanzada con filtros V2
- `reservation-analytics` - Análisis con métricas y KPIs
- `guest-experience-analysis` - Análisis de experiencia del huésped
- `financial-analysis` - Análisis financiero básico

## 🔧 Desarrollo

### Estructura del Proyecto

```
src/trackhs_mcp/
├── __init__.py
├── server.py              # Servidor FastMCP principal
├── core/
│   ├── __init__.py
│   ├── api_client.py      # Cliente HTTP con autenticación
│   ├── auth.py           # Manejo de autenticación Basic Auth
│   ├── types.py          # Tipos base y configuración
│   ├── pagination.py      # Utilidad de paginación robusta
│   ├── logging.py         # Sistema de logging avanzado
│   ├── completion.py     # Utilidad de completion inteligente
│   └── error_handling.py # Manejo robusto de errores
├── tools/
│   ├── __init__.py
│   ├── all_tools.py      # Registrador de la herramienta principal
│   ├── search_reservations.py # ⭐ HERRAMIENTA PRINCIPAL V2
│   ├── README.md         # Documentación de herramientas
│   └── SEARCH_RESERVATIONS_V2.md # Documentación detallada
├── types/
│   ├── __init__.py
│   ├── base.py           # Tipos base
│   ├── contacts.py       # Modelos de contactos
│   ├── folios.py         # Modelos de folios
│   ├── ledger_accounts.py # Modelos de cuentas contables
│   ├── maintenance_work_orders.py # Modelos de mantenimiento
│   ├── nodes.py          # Modelos de nodos
│   ├── reservation_notes.py # Modelos de notas
│   ├── reservations.py   # Modelos de reservas
│   ├── reviews.py        # Modelos de reseñas
│   └── units.py          # Modelos de unidades
├── resources.py          # Resources MCP
└── prompts.py           # Prompts MCP
```

### Agregar Nueva Herramienta

1. Crear archivo `src/trackhs_mcp/tools/nueva_herramienta.py`:

```python
from ..core.api_client import TrackHSApiClient

def register_nueva_herramienta(mcp, api_client: TrackHSApiClient):
    """Registra la nueva herramienta MCP"""
    
    @mcp.tool()
    async def nueva_herramienta(param1: str, param2: int = 10):
        """Descripción de la nueva herramienta"""
        try:
            result = await api_client.get(f"/endpoint/{param1}")
            return result
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
```

2. Importar y registrar en `src/trackhs_mcp/tools/all_tools.py`:

```python
from .nueva_herramienta import register_nueva_herramienta

def register_all_tools(mcp, api_client: TrackHSApiClient):
    # ... otras herramientas ...
    register_nueva_herramienta(mcp, api_client)
```

### Agregar Nuevo Resource

1. Agregar en `src/trackhs_mcp/resources.py`:

```python
@mcp.resource("trackhs://nuevo-resource")
async def nuevo_resource():
    """Descripción del resource"""
    return {"data": "valor"}
```

### Agregar Nuevo Prompt

1. Agregar en `src/trackhs_mcp/prompts.py`:

```python
@mcp.prompt("nuevo-prompt")
async def nuevo_prompt(param1: str):
    """Descripción del prompt"""
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Prompt con {param1}"
                }
            }
        ]
    }
```

### Comandos de Desarrollo

```bash
# Ejecutar servidor en modo desarrollo
python -m src.trackhs_mcp.server

# Verificar estructura del proyecto
python -c "from src.trackhs_mcp.server import main; print('Estructura OK')"

# Instalar en modo desarrollo
pip install -e .
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=src/trackhs_mcp

# Verificar conectividad con Track HS
python -c "from src.trackhs_mcp.core.api_client import TrackHSApiClient; print('API Client OK')"
```

## 📦 Deployment

### Configuración Local

```bash
# Verificar que el servidor funciona
python -m src.trackhs_mcp.server

# Probar con variables de entorno
TRACKHS_USERNAME=test TRACKHS_PASSWORD=test python -m src.trackhs_mcp.server
```

### Deployment con FastMCP

```bash
# Deploy manual
fastmcp deploy

# Verificar deployment
fastmcp status

# Ver logs
fastmcp logs
```

### Variables de Entorno para Producción

```env
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=usuario_produccion
TRACKHS_PASSWORD=contraseña_produccion
TRACKHS_TIMEOUT=30
```

## 🔍 Troubleshooting

### Error de Autenticación

```bash
# Verificar variables de entorno
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD

# Verificar archivo .env
cat .env
```

### Error de Conexión

```bash
# Verificar URL de API
curl -u $TRACKHS_USERNAME:$TRACKHS_PASSWORD $TRACKHS_API_URL/health

# Probar conectividad
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'URL: {os.getenv(\"TRACKHS_API_URL\")}')
print(f'User: {os.getenv(\"TRACKHS_USERNAME\")}')
"
```

### FastMCP no encontrado

```bash
# Instalar FastMCP
pip install fastmcp

# O con uv
uv pip install fastmcp

# Verificar instalación
fastmcp --version
```

### Problemas con Claude Desktop

```bash
# Verificar configuración
cat claude_desktop_config.json

# Verificar que Python está en PATH
which python

# Probar ejecución directa
python -m src.trackhs_mcp.server
```

## 🧪 Testing

### Tests Automáticos

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/ -v          # Tests unitarios
pytest tests/integration/ -v   # Tests de integración
pytest tests/e2e/ -v           # Tests E2E
```

### Test Local

```bash
# Ejecutar test local completo
python test_local.py
```

### CI/CD Testing

Los tests se ejecutan automáticamente en:
- ✅ **Push a main**: Tests completos + deployment
- ✅ **Pull Request**: Tests completos + linting
- ✅ **Manual**: Tests completos + security scan

## 🚀 Deployment

### Deployment Automático

El deployment se ejecuta automáticamente cuando se hace push a `main`:

1. **Tests**: Se ejecutan todos los tests
2. **Build**: Se construye el paquete Python
3. **Deploy**: Se despliega a FastMCP Cloud
4. **Verify**: Se verifica que el deployment fue exitoso

### Configuración de Secrets

Configura los siguientes secrets en GitHub:

```
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
TRACKHS_TIMEOUT=30
FASTMCP_API_KEY=your_api_key
```

### Deployment Manual

```bash
# Construir paquete
python -m build

# Desplegar a FastMCP Cloud
fastmcp deploy

# Verificar deployment
fastmcp status
```

## 📊 Monitoreo

### Health Check

```bash
# Verificar salud del servidor
curl https://trackhs-mcp.fastmcp.cloud/health
```

### Logs y Métricas

```bash
# Ver logs en tiempo real
fastmcp logs --follow

# Ver métricas
fastmcp metrics

# Ver dashboard
fastmcp dashboard
```

## 📚 Documentación Adicional

- [Testing](docs/TESTING.md) - Guía completa de testing
- [Deployment](docs/DEPLOYMENT.md) - Guía de deployment
- [Estructura del Proyecto](docs/PROJECT_STRUCTURE.md) - Arquitectura del proyecto

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📞 Soporte

- **Documentación**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/trackhs/mcp-connector/issues)
- **Email**: team@trackhs.com

## 📋 Estado del Proyecto

- ✅ **Servidor MCP**: Completamente funcional
- ✅ **13 Herramientas**: Todas implementadas y probadas
- ✅ **4 Resources**: Esquemas y documentación disponibles
- ✅ **5 Prompts**: Casos de uso predefinidos
- ✅ **Autenticación**: Basic Auth integrada
- ✅ **Validación**: Tipos Pydantic implementados
- ✅ **Estructura**: Modular y mantenible

---

**TrackHS MCP Connector** - Conectando Track HS con el ecosistema MCP 🚀

*Última actualización: 2025-01-27*