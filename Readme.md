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

### Ejecutar el servidor:
```bash
python src/server.py
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
- ✅ **Tests unitarios** para verificación de funcionalidad
- ✅ **Manejo de errores** robusto con excepciones específicas
- ✅ **Documentación completa** con type hints

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