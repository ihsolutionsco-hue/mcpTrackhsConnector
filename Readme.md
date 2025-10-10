# TrackHS MCP Connector - Python

Servidor MCP (Model Context Protocol) para Track HS API implementado con FastMCP en Python.

## 🚀 Características

- **13 Herramientas MCP** para interactuar con la API de Track HS
- **4 Resources** con esquemas y documentación
- **5 Prompts** predefinidos para casos de uso comunes
- **Autenticación Basic Auth** integrada
- **Validación de tipos** con Pydantic
- **Deployment automático** con FastMCP

## 📋 Herramientas Disponibles

### Reservas
- `get_reservation` - Obtener reserva específica
- `search_reservations` - Buscar reservas con filtros

### Unidades
- `get_units` - Listar unidades con filtros
- `get_unit` - Obtener unidad específica

### Reseñas
- `get_reviews` - Obtener reseñas paginadas

### Contactos
- `get_contacts` - Listar contactos

### Contabilidad
- `get_ledger_accounts` - Listar cuentas contables
- `get_ledger_account` - Obtener cuenta contable específica
- `get_folios_collection` - Obtener colección de folios

### Mantenimiento
- `get_maintenance_work_orders` - Obtener órdenes de trabajo

### Nodos
- `get_nodes` - Listar nodos
- `get_node` - Obtener nodo específico

### Notas de Reserva
- `get_reservation_notes` - Obtener notas de reserva

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- FastMCP 2.0+

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

1. Copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Configurar las variables de entorno en `.env`:
```env
TRACKHS_API_URL=https://api.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
```

## 🚀 Uso

### Desarrollo Local

```bash
# Ejecutar servidor en modo desarrollo
fastmcp dev

# O ejecutar directamente
python -m src.trackhs_mcp.server
```

### Deployment con FastMCP

```bash
# Deploy a FastMCP
fastmcp deploy

# Verificar deployment
fastmcp status
```

## 📚 Recursos MCP

- `trackhs://schema/reservations` - Esquema de reservas
- `trackhs://schema/units` - Esquema de unidades  
- `trackhs://status/system` - Estado del sistema
- `trackhs://docs/api` - Documentación de la API

## 🎯 Prompts Predefinidos

- `check-today-reservations` - Revisar reservas de hoy
- `unit-availability` - Consultar disponibilidad de unidades
- `guest-contact-info` - Información de contacto de huéspedes
- `maintenance-summary` - Resumen de órdenes de mantenimiento
- `financial-analysis` - Análisis financiero básico

## 🔧 Desarrollo

### Estructura del Proyecto

```
src/trackhs_mcp/
├── __init__.py
├── server.py              # Servidor FastMCP principal
├── core/
│   ├── api_client.py      # Cliente HTTP
│   ├── auth.py           # Autenticación
│   └── types.py          # Tipos base
├── tools/
│   ├── all_tools.py      # Todas las herramientas MCP
│   └── __init__.py
├── types/
│   ├── reviews.py        # Modelos de reseñas
│   ├── reservations.py   # Modelos de reservas
│   ├── units.py         # Modelos de unidades
│   └── ...              # Otros modelos
├── resources.py          # Resources MCP
└── prompts.py           # Prompts MCP
```

### Agregar Nueva Herramienta

1. Agregar la función en `src/trackhs_mcp/tools/all_tools.py`:

```python
@mcp.tool()
async def nueva_herramienta(param1: str, param2: int = 10):
    """Descripción de la nueva herramienta"""
    try:
        result = await api_client.get(f"/endpoint/{param1}")
        return result
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
```

2. La herramienta se registrará automáticamente.

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

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=src/trackhs_mcp
```

## 📦 Deployment

### GitHub Actions (Automático)

El proyecto está configurado para deployment automático con FastMCP:

1. Push a `main` → deployment automático
2. FastMCP genera URL pública
3. Configurar secrets en GitHub:
   - `TRACKHS_API_URL`
   - `TRACKHS_USERNAME` 
   - `TRACKHS_PASSWORD`

### Manual

```bash
# Deploy manual
fastmcp deploy

# Verificar
fastmcp status
```

## 🔍 Troubleshooting

### Error de Autenticación

```bash
# Verificar variables de entorno
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD
```

### Error de Conexión

```bash
# Verificar URL de API
curl -u $TRACKHS_USERNAME:$TRACKHS_PASSWORD $TRACKHS_API_URL/health
```

### FastMCP no encontrado

```bash
# Instalar FastMCP
pip install fastmcp

# O con uv
uv pip install fastmcp
```

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

---

**TrackHS MCP Connector** - Conectando Track HS con el ecosistema MCP 🚀