# MCP TrackHS Connector

Conector MCP (Model Context Protocol) para la API de TrackHS, diseñado para integrar servicios de gestión hotelera con sistemas de IA.

## 🚀 Características

- **Integración completa** con la API de TrackHS
- **Herramientas MCP** para búsqueda de unidades, reservas, amenidades y más
- **Autenticación segura** con múltiples métodos soportados
- **Documentación completa** con ejemplos de uso
- **Scripts de diagnóstico** para troubleshooting
- **Configuración flexible** para diferentes entornos

## 📁 Estructura del Proyecto

```
├── src/                    # Código fuente del conector
│   └── trackhs_mcp/       # Módulo principal
├── docs/                  # Documentación del proyecto
├── examples/              # Ejemplos de uso
├── scripts/               # Scripts de utilidad y diagnóstico
├── tests/                 # Tests unitarios e integración
├── config/                # Archivos de configuración
├── temp_tests/            # Tests temporales (ignorados por git)
├── reports/               # Reportes de pruebas (ignorados por git)
├── pyproject.toml         # Configuración del proyecto
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🛠️ Instalación

### Requisitos

- Python 3.8+
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
export TRACKHS_API_URL='https://ihmvacations.trackhs.com/api'  # Opcional
```

## 🚀 Uso Rápido

### Ejecutar el Servidor MCP

```bash
python -m trackhs_mcp
```

### Usar las Herramientas MCP

El conector proporciona las siguientes herramientas MCP:

- `search_units` - Buscar unidades de alojamiento
- `search_reservations` - Buscar reservas
- `get_reservation` - Obtener detalles de una reserva
- `get_folio` - Obtener folio financiero de una reserva
- `search_amenities` - Buscar amenidades disponibles
- `create_maintenance_work_order` - Crear orden de mantenimiento
- `create_housekeeping_work_order` - Crear orden de limpieza

## 📚 Documentación

La documentación completa está disponible en la carpeta `docs/`:

- [Búsqueda de Unidades](docs/unit_collection.md)
- [Gestión de Reservas](docs/reservation_collection.md)
- [Amenidades](docs/get_amenities.md)
- [Folios Financieros](docs/get_folio.md)
- [Órdenes de Mantenimiento](docs/wo_maintenance.md)
- [Órdenes de Limpieza](docs/wo_housekeeping.md)

## 🔧 Scripts de Diagnóstico

Para diagnosticar problemas de conectividad o configuración:

```bash
# Prueba rápida
python scripts/run_quick_test.py

# Diagnóstico completo
python scripts/run_final_diagnosis.py

# Verificar configuración
python scripts/verify_server_config.py
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=src/trackhs_mcp

# Tests específicos
pytest tests/test_integration.py
```

## 🚀 Despliegue en FastMCP Cloud

1. **Configurar variables de entorno** en FastMCP Cloud:
   ```
   TRACKHS_USERNAME=tu_usuario
   TRACKHS_PASSWORD=tu_password
   TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
   ```

2. **Desplegar el servidor** usando la configuración de `config/fastmcp.json`

3. **Probar la conectividad** usando los scripts de diagnóstico

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error de autenticación**: Verificar credenciales y URL base
2. **Recurso no encontrado**: Verificar endpoint y configuración
3. **Timeout**: Verificar conectividad de red

### Scripts de Diagnóstico

```bash
# Diagnóstico completo
python scripts/run_final_diagnosis.py

# Verificar configuración específica
python scripts/test_current_config.py

# Probar conectividad
python scripts/test_basic_connectivity.py
```

## 📄 Reportes

Los scripts de diagnóstico generan reportes en la carpeta `reports/`:

- `final_diagnosis_report_*.json` - Diagnóstico completo
- `connectivity_test_results.json` - Resultados de conectividad
- `local_tests_report_*.json` - Tests locales

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

1. Revisar la documentación en `docs/`
2. Ejecutar los scripts de diagnóstico
3. Crear un issue en GitHub con los reportes generados

## 🎯 Roadmap

- [ ] Soporte para más endpoints de TrackHS
- [ ] Cache inteligente para mejorar rendimiento
- [ ] Métricas y monitoreo avanzado
- [ ] Soporte para webhooks
- [ ] Integración con más sistemas MCP

---

**Desarrollado por IHM Solutions** - Soluciones de gestión hotelera inteligente