# TrackHS MCP Server

Servidor MCP (Model Context Protocol) para integración con la API de TrackHS, refactorizado siguiendo las mejores prácticas de FastMCP.

## 🏗️ Estructura del Proyecto

```
src/
├── server.py                 # Servidor principal
├── server_logic.py          # Lógica del servidor
├── config.py                # Configuración
├── schemas/                 # Schemas Pydantic
│   ├── base.py
│   ├── reservation.py
│   ├── unit.py
│   ├── amenity.py
│   ├── work_order.py
│   └── folio.py
├── utils/                   # Utilidades
│   ├── logger.py
│   ├── api_client.py
│   ├── exceptions.py
│   └── validators.py
└── tools/                   # Herramientas MCP
    ├── base.py
    ├── search_reservations.py
    ├── get_reservation.py
    ├── search_units.py
    ├── search_amenities.py
    ├── get_folio.py
    ├── create_maintenance_work_order.py
    └── create_housekeeping_work_order.py

tests/
└── unit/                    # Tests unitarios
    ├── test_server_refactored.py
    └── test_simple_refactored.py
```

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd MCPtrackhsConnector
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
# Crear archivo .env
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_password
TRACKHS_API_URL=https://ihmvacations.trackhs.com
```

## 🎯 Uso

### Ejecutar el servidor localmente:
```bash
python src/server.py
```

### Ejecutar con configuración declarativa:
```bash
# Usar fastmcp.json (recomendado)
fastmcp run

# O especificar archivo de configuración
fastmcp run fastmcp.json
```

### Ejecutar tests:
```bash
python tests/unit/test_simple_refactored.py
```

## 🔧 Herramientas Disponibles

- **search_reservations** - Buscar reservas con filtros avanzados
- **get_reservation** - Obtener detalles de una reserva específica
- **search_units** - Buscar unidades de alojamiento
- **search_amenities** - Buscar amenidades/servicios
- **get_folio** - Obtener folio financiero de una reserva
- **create_maintenance_work_order** - Crear orden de mantenimiento
- **create_housekeeping_work_order** - Crear orden de limpieza

## 📋 Características

- ✅ **Arquitectura escalable** con separación de responsabilidades
- ✅ **Schemas Pydantic** para validación robusta
- ✅ **Logging estructurado** para debugging y monitoreo
- ✅ **Timing Middleware** para monitoreo de rendimiento automático
- ✅ **Configuración declarativa** con fastmcp.json
- ✅ **Tests unitarios** para verificación de funcionalidad
- ✅ **Manejo de errores** robusto con excepciones específicas
- ✅ **Documentación completa** con type hints

## 📊 Monitoreo y Rendimiento

### Timing Middleware
El servidor incluye **Timing Middleware** que registra automáticamente el tiempo de ejecución de cada herramienta:

```bash
# Los logs mostrarán información de rendimiento como:
[INFO] search_reservations completed in 2.341s
[INFO] get_reservation completed in 0.823s
[WARN] create_maintenance_work_order completed in 8.912s
```

### Configuración Declarativa
El archivo `fastmcp.json` define toda la configuración del servidor:

```json
{
  "source": {
    "path": "src/__main__.py"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.11",
    "dependencies": [
      "fastmcp>=2.13.0",
      "httpx>=0.27.0",
      "pydantic>=2.12.3"
    ]
  },
  "secrets": {
    "required": [
      "TRACKHS_API_URL",
      "TRACKHS_USERNAME",
      "TRACKHS_PASSWORD"
    ]
  }
}
```

**Beneficios:**
- ✅ **Deployment reproducible** sin warnings de seguridad
- ✅ **Configuración versionada** y portable
- ✅ **Detección automática** de dependencias
- ✅ **Integración perfecta** con FastMCP Cloud

## 🧪 Testing

```bash
# Ejecutar tests unitarios
python tests/unit/test_simple_refactored.py

# Ejecutar tests específicos
python tests/unit/test_server_refactored.py
```

## 📚 Documentación

- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- [REFACTORING_FINAL_SUMMARY.md](REFACTORING_FINAL_SUMMARY.md) - Resumen de refactorización

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.