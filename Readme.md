# TrackHS MCP Connector

Conector MCP (Model Context Protocol) para la API de TrackHS, diseñado para integrar servicios de gestión hotelera con sistemas de IA.

## 🚀 Características

- **Integración completa** con la API de TrackHS
- **Herramientas MCP** para búsqueda de unidades, reservas, amenidades y más
- **Autenticación segura** con múltiples métodos soportados
- **Arquitectura robusta** con servicios, repositorios y middleware
- **Validación Pydantic** para datos de entrada y salida
- **Manejo de errores** avanzado con reintentos automáticos
- **Logging estructurado** para debugging y monitoreo
- **Configuración flexible** para diferentes entornos

## 📁 Estructura del Proyecto

```
├── src/                    # Código fuente del conector
│   └── trackhs_mcp/       # Módulo principal
│       ├── server.py      # Servidor MCP principal
│       ├── config.py      # Configuración centralizada
│       ├── exceptions.py  # Excepciones personalizadas
│       ├── schemas.py     # Esquemas Pydantic
│       ├── services/      # Lógica de negocio
│       │   ├── reservation_service.py
│       │   ├── unit_service.py
│       │   └── work_order_service.py
│       ├── repositories/  # Acceso a datos
│       │   ├── base.py
│       │   ├── reservation_repository.py
│       │   ├── unit_repository.py
│       │   └── work_order_repository.py
│       └── middleware_native.py  # Middleware personalizado
├── tests/                 # Tests unitarios e integración
├── config/                # Archivos de configuración
├── pyproject.toml         # Configuración del proyecto
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🛠️ Instalación

### Requisitos

- Python 3.11+
- Credenciales de TrackHS

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/ihsolutionsco-hue/mcpTrackhsConnector.git
cd mcpTrackhsConnector

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

### Variables de Entorno

```bash
export TRACKHS_USERNAME='tu_usuario'
export TRACKHS_PASSWORD='tu_password'
export TRACKHS_API_URL='https://ihmvacations.trackhs.com'  # Opcional
export LOG_LEVEL='INFO'  # Opcional
export STRICT_VALIDATION='false'  # Opcional
```

## 🚀 Uso Rápido

### Ejecutar el Servidor MCP

```bash
python -m trackhs_mcp
```

### Herramientas MCP Disponibles

El conector proporciona las siguientes herramientas MCP:

#### 🔍 Búsqueda de Reservas
- `search_reservations` - Buscar reservas con filtros avanzados
- `get_reservation` - Obtener detalles de una reserva específica
- `get_folio` - Obtener folio financiero de una reserva

#### 🏠 Gestión de Unidades
- `search_units` - Buscar unidades de alojamiento con filtros completos
- `search_amenities` - Buscar amenidades disponibles

#### 🔧 Órdenes de Trabajo
- `create_maintenance_work_order` - Crear orden de mantenimiento
- `create_housekeeping_work_order` - Crear orden de limpieza

### Ejemplos de Uso

```python
# Buscar reservas por fecha
search_reservations(
    arrival_start="2024-01-15",
    arrival_end="2024-01-20",
    status="confirmed"
)

# Buscar unidades disponibles
search_units(
    bedrooms=2,
    bathrooms=1,
    is_active=1,
    is_bookable=1
)

# Crear orden de mantenimiento
create_maintenance_work_order(
    unit_id=123,
    summary="Fuga en grifo",
    description="Grifo del baño principal gotea constantemente",
    priority=3
)
```

## 🏗️ Arquitectura

### Patrón de Servicios

El proyecto sigue una arquitectura de servicios que separa las responsabilidades:

- **Servicios**: Lógica de negocio y validaciones
- **Repositorios**: Acceso a datos y comunicación con API
- **Middleware**: Autenticación, logging, métricas y reintentos
- **Esquemas**: Validación de datos con Pydantic

### Middleware Nativo

- **ErrorHandlingMiddleware**: Manejo centralizado de errores
- **RetryMiddleware**: Reintentos automáticos con backoff exponencial
- **TrackHSAuthMiddleware**: Autenticación y autorización
- **TrackHSLoggingMiddleware**: Logging estructurado
- **TrackHSMetricsMiddleware**: Métricas y monitoreo
- **TrackHSRateLimitMiddleware**: Control de velocidad

### Validación de Datos

- **Pydantic**: Validación robusta de entrada y salida
- **Transformación automática**: Conversión de tipos problemáticos
- **Sanitización**: Limpieza de datos sensibles para logs
- **Validación flexible**: Modo estricto y no estricto

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Default | Requerida |
|----------|-------------|---------|-----------|
| `TRACKHS_USERNAME` | Usuario de TrackHS | - | ✅ |
| `TRACKHS_PASSWORD` | Contraseña de TrackHS | - | ✅ |
| `TRACKHS_API_URL` | URL base de la API | `https://ihmvacations.trackhs.com` | ❌ |
| `LOG_LEVEL` | Nivel de logging | `INFO` | ❌ |
| `STRICT_VALIDATION` | Validación estricta | `false` | ❌ |
| `MAX_RETRIES` | Máximo de reintentos | `3` | ❌ |
| `REQUEST_TIMEOUT` | Timeout de requests | `30.0` | ❌ |

### Configuración Avanzada

```python
# config/fastmcp.json
{
  "name": "TrackHS API",
  "version": "2.0.0",
  "description": "Servidor MCP para TrackHS API",
  "environment": {
    "TRACKHS_USERNAME": "your_username",
    "TRACKHS_PASSWORD": "your_password"
  }
}
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=src/trackhs_mcp

# Tests específicos
pytest tests/test_integration.py

# Tests con verbose
pytest -v
```

## 🚀 Despliegue

### FastMCP Cloud

1. **Configurar variables de entorno** en FastMCP Cloud
2. **Desplegar el servidor** usando la configuración de `config/fastmcp.json`
3. **Probar la conectividad** usando las herramientas MCP

### Docker (Próximamente)

```bash
# Construir imagen
docker build -t trackhs-mcp .

# Ejecutar contenedor
docker run -e TRACKHS_USERNAME=user -e TRACKHS_PASSWORD=pass trackhs-mcp
```

## 📊 Monitoreo

### Health Check

```bash
# Verificar estado del servidor
curl https://your-mcp-server.com/health
```

### Métricas Prometheus

```bash
# Obtener métricas
curl https://your-mcp-server.com/metrics
```

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error de autenticación**: Verificar credenciales y URL base
2. **Recurso no encontrado**: Verificar endpoint y configuración
3. **Timeout**: Verificar conectividad de red
4. **Validación fallida**: Revisar formato de datos de entrada

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/trackhs-mcp.log

# Filtrar por nivel
grep "ERROR" logs/trackhs-mcp.log
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:

1. Revisar la documentación en este README
2. Verificar logs del servidor
3. Crear un issue en GitHub con información detallada

## 🎯 Roadmap

- [ ] Soporte para más endpoints de TrackHS
- [ ] Cache inteligente para mejorar rendimiento
- [ ] Métricas y monitoreo avanzado
- [ ] Soporte para webhooks
- [ ] Integración con más sistemas MCP
- [ ] Dockerización completa
- [ ] Tests de carga y rendimiento

---

**Desarrollado por IHM Solutions** - Soluciones de gestión hotelera inteligente

**Versión**: 2.0.0
**Python**: 3.11+
**FastMCP**: 2.13.0+