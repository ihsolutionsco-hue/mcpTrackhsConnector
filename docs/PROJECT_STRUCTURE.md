# Estructura del Proyecto - TrackHS MCP Connector

## Estructura Final del Proyecto

```
MCPtrackhsConnector/
 src/
    __init__.py
    trackhs_mcp/                    # Paquete principal Python
        __init__.py
        server.py                   # Servidor FastMCP principal
        resources.py                # Resources MCP (4 resources)
        prompts.py                  # Prompts MCP (5 prompts)
        core/                    # Módulos core
           __init__.py
           api_client.py          # Cliente HTTP con httpx
           auth.py                # Autenticación Basic Auth
           types.py               # Tipos base y configuración
        tools/                   # Herramientas MCP (13 tools)
           __init__.py
           all_tools.py           # Todas las herramientas registradas
           get_reviews.py         # Herramientas individuales
           get_reservation.py
           search_reservations.py
        types/                   # Modelos Pydantic (9 tipos)
            __init__.py
            base.py                # Tipos base
            reviews.py             # Modelos de reseñas
            reservations.py        # Modelos de reservas
            units.py               # Modelos de unidades
            contacts.py            # Modelos de contactos
            folios.py              # Modelos de folios
            ledger_accounts.py     # Modelos de cuentas contables
            reservation_notes.py   # Modelos de notas de reserva
            nodes.py               # Modelos de nodos
            maintenance_work_orders.py # Modelos de órdenes de trabajo
 .github/
    workflows/
        deploy.yml                 # GitHub Actions para deployment
 docs/                           # Documentación
    PYTHON_MIGRATION.md            # Guía de migración
    GITHUB_SETUP.md                # Configuración GitHub
    LOCAL_TESTING.md               # Testing local
    CLEANUP_GUIDE.md               # Guía de limpieza
    PROJECT_STRUCTURE.md           # Este archivo
    MCP_USAGE.md                   # Guía de uso MCP
 pyproject.toml                     # Configuración del proyecto Python
 requirements.txt                   # Dependencias Python
 .env.example                       # Variables de entorno de ejemplo
 test_local.py                      # Script de testing local
 README.md                          # Documentación principal
```

## Organización por Funcionalidad

### 1. Core Modules (`src/trackhs_mcp/core/`)
- **`api_client.py`**: Cliente HTTP asíncrono con httpx
- **`auth.py`**: Autenticación Basic Auth para Track HS
- **`types.py`**: Tipos base, configuración y respuestas genéricas

### 2. MCP Tools (`src/trackhs_mcp/tools/`)
- **`all_tools.py`**: Registro de las 13 herramientas MCP
- **Herramientas individuales**: Archivos separados para cada herramienta
- **13 herramientas disponibles**:
  1. `get_reviews` - Obtener reseñas
  2. `get_reservation` - Obtener reserva específica
  3. `search_reservations` - Buscar reservas
  4. `get_units` - Listar unidades
  5. `get_unit` - Obtener unidad específica
  6. `get_folios_collection` - Obtener folios
  7. `get_contacts` - Listar contactos
  8. `get_ledger_accounts` - Listar cuentas contables
  9. `get_ledger_account` - Obtener cuenta específica
  10. `get_reservation_notes` - Obtener notas de reserva
  11. `get_nodes` - Listar nodos
  12. `get_node` - Obtener nodo específico
  13. `get_maintenance_work_orders` - Órdenes de mantenimiento

### 3. MCP Resources (`src/trackhs_mcp/resources.py`)
- **4 resources disponibles**:
  1. `trackhs://schema/reservations` - Esquema de reservas
  2. `trackhs://schema/units` - Esquema de unidades
  3. `trackhs://status/system` - Estado del sistema
  4. `trackhs://docs/api` - Documentación de la API

### 4. MCP Prompts (`src/trackhs_mcp/prompts.py`)
- **5 prompts disponibles**:
  1. `check-today-reservations` - Revisar reservas de hoy
  2. `unit-availability` - Consultar disponibilidad
  3. `guest-contact-info` - Información de contacto
  4. `maintenance-summary` - Resumen de mantenimiento
  5. `financial-analysis` - Análisis financiero

### 5. Data Models (`src/trackhs_mcp/types/`)
- **9 tipos de datos** con modelos Pydantic:
  1. `reviews.py` - Reseñas
  2. `reservations.py` - Reservas
  3. `units.py` - Unidades
  4. `contacts.py` - Contactos
  5. `folios.py` - Folios
  6. `ledger_accounts.py` - Cuentas contables
  7. `reservation_notes.py` - Notas de reserva
  8. `nodes.py` - Nodos
  9. `maintenance_work_orders.py` - Órdenes de trabajo

## Deployment y CI/CD

### GitHub Actions (`.github/workflows/deploy.yml`)
- **Deployment automático** con FastMCP
- **Trigger**: Push a `main`
- **Secrets requeridos**:
  - `TRACKHS_API_URL`
  - `TRACKHS_USERNAME`
  - `TRACKHS_PASSWORD`

### FastMCP Cloud
- **URL pública** generada automáticamente
- **Gestión de sesiones** mejorada
- **Monitoreo** y métricas

## Documentación

### Archivos Principales
- **`README.md`**: Documentación principal del proyecto
- **`docs/PYTHON_MIGRATION.md`**: Guía completa de migración
- **`docs/MCP_USAGE.md`**: Guía de uso de herramientas MCP
- **`docs/LOCAL_TESTING.md`**: Testing local
- **`docs/GITHUB_SETUP.md`**: Configuración de GitHub
- **`docs/CLEANUP_GUIDE.md`**: Guía de limpieza

## Configuración

### Variables de Entorno (`.env`)
```env
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
```

### Dependencias (`requirements.txt`)
```
fastmcp>=2.0.0
httpx>=0.24.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

## Testing

### Script de Testing (`test_local.py`)
- **Conexión API**: Verificar conectividad con Track HS
- **Herramientas MCP**: Verificar registro de herramientas
- **Resources MCP**: Verificar registro de resources
- **Prompts MCP**: Verificar registro de prompts

### Comandos de Testing
```bash
# Testing automático
python test_local.py

# Servidor local
fastmcp dev

# MCP Inspector
npx @modelcontextprotocol/inspector
```

## Métricas del Proyecto

- **13 Herramientas MCP** funcionales
- **4 Resources MCP** con esquemas
- **5 Prompts MCP** predefinidos
- **9 Tipos de datos** con Pydantic
- **Deployment automático** con GitHub Actions
- **Documentación completa** actualizada

## Próximos Pasos

1. **Configurar variables** de entorno
2. **Ejecutar testing** local
3. **Configurar secrets** en GitHub
4. **Hacer commit** y push
5. **Verificar deployment** automático
6. **Probar URL pública** generada

---

**Estructura Final** - Proyecto migrado exitosamente a Python con FastMCP
