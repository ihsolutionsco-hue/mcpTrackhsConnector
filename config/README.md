# Configuración del Proyecto

Esta carpeta contiene todos los archivos de configuración del proyecto MCP TrackHS Connector.

## Archivos de Configuración

### `fastmcp.json`
Configuración principal de FastMCP con parámetros de conexión y configuración del servidor.

### `pyrightconfig.json`
Configuración de Pyright (type checker de Python) para el proyecto.

### `pytest.ini`
Configuración de pytest para la ejecución de pruebas unitarias.

### `production_test_report.json`
Reporte de pruebas de producción con resultados y métricas.

## Uso

Estos archivos de configuración son utilizados automáticamente por las herramientas correspondientes:

- **FastMCP**: Lee `fastmcp.json` para la configuración del servidor
- **Pyright**: Usa `pyrightconfig.json` para el análisis de tipos
- **Pytest**: Utiliza `pytest.ini` para la configuración de pruebas
- **Reportes**: `production_test_report.json` contiene métricas de pruebas

## Modificación

⚠️ **Importante**: Modificar estos archivos puede afectar el comportamiento del proyecto. Asegúrate de entender los cambios antes de modificarlos.
