# TrackHS MCP Connector - Clean Architecture

Servidor MCP (Model Context Protocol) para Track HS API V2 implementado con **Clean Architecture** en Python.

## 🏗️ Arquitectura

Este proyecto sigue los principios de **Clean Architecture** con separación clara de responsabilidades:

```
src/trackhs_mcp/
├── domain/                    # Capa de Dominio
│   ├── entities/             # Entidades de negocio
│   ├── value_objects/        # Value Objects
│   └── exceptions/           # Excepciones de dominio
├── application/              # Capa de Aplicación
│   ├── use_cases/           # Casos de uso
│   └── ports/               # Interfaces (puertos)
└── infrastructure/           # Capa de Infraestructura
    ├── adapters/            # Adaptadores (API, MCP)
    ├── mcp/                 # Adaptador MCP
    └── utils/               # Utilidades
```

## 🚀 Características

- **✅ Clean Architecture** - Separación clara de responsabilidades
- **✅ API V2 Completa** - Soporte completo para Search Reservations V2
- **✅ Protocolo MCP** - Integración nativa con el ecosistema MCP
- **✅ Inyección de Dependencias** - Fácil testing y mantenimiento
- **✅ Testing Robusto** - Tests unitarios, integración y E2E
- **✅ Documentación Completa** - Organizada por temas

## 📋 Herramienta Principal

### Search Reservations V2
- **`search_reservations`** - ⭐ **HERRAMIENTA PRINCIPAL** - Búsqueda avanzada de reservas
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
# Ejecutar servidor con Clean Architecture
python -m src.trackhs_mcp

# O ejecutar directamente
python -m src.trackhs_mcp.__main__

# Con variables de entorno específicas
TRACKHS_USERNAME=usuario TRACKHS_PASSWORD=contraseña python -m src.trackhs_mcp
```

### Configuración en Claude Desktop

1. Crear archivo de configuración `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "src.trackhs_mcp"],
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

### Estructura del Proyecto (Clean Architecture)

```
src/trackhs_mcp/
├── domain/                    # Capa de Dominio
│   ├── entities/             # Entidades de negocio
│   │   ├── reservation.py
│   │   ├── contact.py
│   │   ├── unit.py
│   │   └── ...
│   ├── value_objects/        # Value Objects
│   │   ├── config.py
│   │   └── request.py
│   └── exceptions/           # Excepciones de dominio
│       └── api_exceptions.py
├── application/              # Capa de Aplicación
│   ├── use_cases/           # Casos de uso
│   │   └── search_reservations.py
│   └── ports/               # Interfaces (puertos)
│       └── api_client_port.py
├── infrastructure/           # Capa de Infraestructura
│   ├── adapters/            # Adaptadores
│   │   ├── trackhs_api_client.py
│   │   └── config.py
│   ├── mcp/                 # Adaptador MCP
│   │   ├── tools.py
│   │   ├── resources.py
│   │   ├── prompts.py
│   │   └── server.py
│   └── utils/               # Utilidades
│       ├── auth.py
│       ├── error_handling.py
│       ├── logging.py
│       ├── pagination.py
│       └── completion.py
└── __main__.py              # Entry point con inyección de dependencias
```

### Principios de Clean Architecture

1. **Independencia de Frameworks** - El código de negocio no depende de frameworks
2. **Testabilidad** - Fácil testing con inyección de dependencias
3. **Independencia de UI** - La lógica de negocio no depende de la interfaz
4. **Independencia de Base de Datos** - El dominio no depende de la persistencia
5. **Independencia de Agentes Externos** - El dominio no depende de servicios externos

### Agregar Nueva Herramienta

1. Crear caso de uso en `application/use_cases/`
2. Crear puerto (interfaz) en `application/ports/`
3. Implementar adaptador en `infrastructure/adapters/`
4. Registrar en `infrastructure/mcp/`

### Comandos de Desarrollo

```bash
# Ejecutar servidor con Clean Architecture
python -m src.trackhs_mcp

# Verificar estructura del proyecto
python -c "from src.trackhs_mcp.__main__ import main; print('Estructura OK')"

# Instalar en modo desarrollo
pip install -e .
```

## 🧪 Testing

### Estructura de Tests (Clean Architecture)

```
tests/
├── unit/                    # Tests unitarios por capa
│   ├── domain/
│   │   ├── entities/
│   │   └── value_objects/
│   ├── application/
│   │   └── use_cases/
│   └── infrastructure/
│       ├── adapters/
│       └── utils/
├── integration/             # Tests de integración
└── e2e/                     # Tests end-to-end
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=src/trackhs_mcp --cov-report=html

# Tests específicos por capa
pytest tests/unit/domain/ -v          # Tests de dominio
pytest tests/unit/application/ -v     # Tests de aplicación
pytest tests/unit/infrastructure/ -v   # Tests de infraestructura
pytest tests/integration/ -v           # Tests de integración
pytest tests/e2e/ -v                   # Tests E2E
```

## 📦 Deployment

### Deployment con Clean Architecture

```bash
# Verificar que el servidor funciona
python -m src.trackhs_mcp

# Probar con variables de entorno
TRACKHS_USERNAME=test TRACKHS_PASSWORD=test python -m src.trackhs_mcp
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

## 📚 Documentación Adicional

- [Documentación Completa](docs/README.md) - Guía completa organizada por temas
- [Arquitectura](docs/architecture/) - Detalles de Clean Architecture
- [API](docs/api/) - Documentación de la API V2
- [MCP](docs/mcp/) - Protocolo MCP y mejores prácticas
- [Desarrollo](docs/development/) - Guías de desarrollo
- [Deployment](docs/deployment/) - Guías de deployment

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

- ✅ **Clean Architecture**: Implementada completamente
- ✅ **Servidor MCP**: Completamente funcional
- ✅ **API V2**: Soporte completo con todos los parámetros
- ✅ **Inyección de Dependencias**: Implementada
- ✅ **Testing**: Tests organizados por capas
- ✅ **Documentación**: Organizada por temas
- ✅ **Deployment**: Configurado para producción

---

**TrackHS MCP Connector** - Conectando Track HS con el ecosistema MCP usando Clean Architecture 🚀

*Última actualización: 2025-01-27*
