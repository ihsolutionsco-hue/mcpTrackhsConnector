# Guía de Conexión de Clientes - TrackHS MCP

Esta guía explica cómo conectarse al servidor TrackHS MCP usando diferentes transportes y clientes, con especial enfoque en la compatibilidad con FastMCP Cloud y ElevenLabs.

## Visión General de Transportes MCP

El Model Context Protocol (MCP) soporta diferentes tipos de transporte para la comunicación entre clientes y servidores:

### STDIO Transport (Local)
- **Uso**: Desarrollo local, Claude Desktop
- **Características**: Comunicación a través de stdin/stdout
- **Limitaciones**: Un cliente por proceso, no accesible remotamente

### HTTP Streamable Transport (Remoto) ⭐ **Recomendado**
- **Uso**: Servidores remotos, FastMCP Cloud, ElevenLabs
- **Características**: Comunicación bidireccional sobre HTTP
- **Ventajas**: Múltiples clientes, escalable, accesible remotamente

### SSE Transport (Legacy)
- **Uso**: Compatibilidad con clientes antiguos
- **Características**: Solo streaming del servidor al cliente
- **Estado**: No recomendado para nuevos proyectos

## Configuración del Servidor TrackHS

### Estado Actual
El servidor TrackHS MCP está configurado para usar **HTTP Streamable Transport**:

```python
# src/trackhs_mcp/__main__.py
mcp.run(transport="http")  # ✅ HTTP Streamable Transport
```

### Configuración en FastMCP Cloud
El archivo `fastmcp.yaml` ya incluye la configuración necesaria:

```yaml
# fastmcp.yaml
network:
  port: 8080
  host: "0.0.0.0"

cors:
  origins:
    - "https://elevenlabs.io"
    - "https://app.elevenlabs.io"
    - "https://claude.ai"
    - "https://app.claude.ai"
  credentials: true
  methods: ["GET", "POST", "DELETE", "OPTIONS"]
```

## Conexión desde Clientes Python

### Instalación de Dependencias

```bash
pip install fastmcp httpx
```

### Ejemplo Básico

```python
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def connect_to_trackhs():
    # URL proporcionada por FastMCP Cloud
    server_url = "https://tu-servidor.fastmcp.cloud/mcp"

    # Crear transporte HTTP
    transport = StreamableHttpTransport(url=server_url)
    client = Client(transport)

    async with client:
        # Probar conexión
        await client.ping()
        print("✅ Conectado al servidor TrackHS MCP")

        # Listar herramientas disponibles
        tools = await client.list_tools()
        print(f"Herramientas disponibles: {len(tools.tools)}")

        # Usar una herramienta
        result = await client.call_tool(
            "search_reservations_v2",
            {
                "arrival_start": "2024-01-01",
                "arrival_end": "2024-01-31",
                "status": "Confirmed",
                "size": 10
            }
        )
        print(f"Resultado: {result.content}")

# Ejecutar
asyncio.run(connect_to_trackhs())
```

### Conexión con Autenticación

```python
from fastmcp.client.transports import StreamableHttpTransport

# Headers de autenticación (opcional)
headers = {
    "Authorization": "Bearer tu-token-aqui",
    "X-API-Key": "tu-api-key-aqui"
}

transport = StreamableHttpTransport(
    url="https://tu-servidor.fastmcp.cloud/mcp",
    headers=headers
)
```

## Configuración en ElevenLabs

### Paso 1: Obtener URL del Servidor
Después del deployment en FastMCP Cloud, obtienes una URL como:
```
https://tu-servidor.fastmcp.cloud/mcp
```

### Paso 2: Configurar en ElevenLabs
1. Ve a [ElevenLabs MCP Integrations](https://elevenlabs.io/app/agents/integrations)
2. Haz clic en "Add Custom MCP Server"
3. Configura los siguientes campos:

| Campo | Valor |
|-------|-------|
| **Name** | `TrackHS MCP Server` |
| **Description** | `Conector MCP para TrackHS API - Gestión de reservas y unidades` |
| **Server URL** | `https://tu-servidor.fastmcp.cloud/mcp` |
| **Secret Token** | (Opcional) Token de autenticación |
| **HTTP Headers** | (Opcional) Headers adicionales |

### Paso 3: Configurar Aprobación de Herramientas
ElevenLabs ofrece 3 modos de aprobación:

#### Always Ask (Recomendado)
- **Seguridad**: Máxima
- **Uso**: Requiere aprobación para cada herramienta
- **Recomendado para**: Producción, datos sensibles

#### Fine-Grained Tool Approval
- **Seguridad**: Personalizable
- **Uso**: Configurar aprobación por herramienta
- **Recomendado para**: Control granular

#### No Approval
- **Seguridad**: Mínima
- **Uso**: Sin aprobación requerida
- **Recomendado para**: Desarrollo, herramientas de solo lectura

### Herramientas Disponibles en ElevenLabs

El servidor TrackHS MCP expone las siguientes herramientas:

| Herramienta | Descripción | Tipo |
|-------------|-------------|------|
| `search_reservations_v2` | Buscar reservaciones | Lectura |
| `get_reservation_v2` | Obtener reservación específica | Lectura |
| `get_folio` | Obtener folio financiero | Lectura |
| `search_units` | Buscar unidades disponibles | Lectura |
| `search_amenities` | Buscar amenidades | Lectura |
| `create_maintenance_work_order` | Crear orden de mantenimiento | Escritura |
| `create_housekeeping_work_order` | Crear orden de limpieza | Escritura |

## Configuración en Claude Desktop

### Método 1: STDIO (Local)
```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "src.trackhs_mcp"],
      "cwd": "/path/to/MCPtrackhsConnector",
      "env": {
        "TRACKHS_API_URL": "https://api.trackhs.com/api",
        "TRACKHS_USERNAME": "tu_usuario",
        "TRACKHS_PASSWORD": "tu_contraseña"
      }
    }
  }
}
```

### Método 2: HTTP (Remoto)
```json
{
  "mcpServers": {
    "trackhs": {
      "url": "https://tu-servidor.fastmcp.cloud/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer tu-token-opcional"
      }
    }
  }
}
```

## Testing de Conectividad

### Script de Prueba Básico

```python
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def test_connectivity(server_url: str):
    try:
        transport = StreamableHttpTransport(url=server_url)
        client = Client(transport)

        async with client:
            # Test de ping
            await client.ping()
            print("✅ Servidor responde")

            # Listar herramientas
            tools = await client.list_tools()
            print(f"✅ {len(tools.tools)} herramientas disponibles")

            # Listar recursos
            resources = await client.list_resources()
            print(f"✅ {len(resources.resources)} recursos disponibles")

            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Usar
server_url = "https://tu-servidor.fastmcp.cloud/mcp"
asyncio.run(test_connectivity(server_url))
```

### Comandos de Prueba con cURL

```bash
# Health check
curl https://tu-servidor.fastmcp.cloud/health

# Listar herramientas
curl -X POST https://tu-servidor.fastmcp.cloud/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Troubleshooting

### Problemas Comunes

#### "Cannot connect to MCP server"
**Causas**:
- URL incorrecta
- Servidor no desplegado
- CORS mal configurado

**Soluciones**:
1. Verificar URL: `https://tu-servidor.fastmcp.cloud/mcp`
2. Verificar que el servidor esté corriendo
3. Revisar logs en FastMCP Cloud dashboard

#### "Tools not available"
**Causas**:
- Servidor no inicializado
- Variables de entorno faltantes
- Error en la API de TrackHS

**Soluciones**:
1. Verificar variables de entorno en FastMCP Cloud
2. Revisar logs del servidor
3. Probar conexión a TrackHS API

#### "CORS error"
**Causas**:
- Orígenes CORS no configurados
- Headers faltantes

**Soluciones**:
1. Verificar configuración en `fastmcp.yaml`
2. Agregar `https://elevenlabs.io` a orígenes CORS
3. Reiniciar el servidor

### Logs Útiles

```bash
# Verificar deployment en FastMCP Cloud
curl https://tu-servidor.fastmcp.cloud/health

# Verificar herramientas disponibles
curl -X POST https://tu-servidor.fastmcp.cloud/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Mejores Prácticas

### Seguridad
1. **Usar HTTPS**: Siempre usar URLs HTTPS en producción
2. **Configurar CORS**: Limitar orígenes permitidos
3. **Monitorear acceso**: Revisar logs regularmente
4. **Rotar credenciales**: Cambiar contraseñas periódicamente

### Rendimiento
1. **Caché**: Usar caché para consultas frecuentes
2. **Rate limiting**: Configurar límites de requests
3. **Monitoreo**: Usar métricas de FastMCP Cloud
4. **Escalabilidad**: Configurar auto-scaling si es necesario

### Mantenimiento
1. **Actualizaciones**: Mantener dependencias actualizadas
2. **Backups**: Hacer backup de configuraciones
3. **Testing**: Probar integración regularmente
4. **Documentación**: Mantener documentación actualizada

## Recursos Adicionales

- [Documentación FastMCP](https://gofastmcp.com/)
- [Documentación ElevenLabs MCP](https://elevenlabs.io/docs/conversational-ai/customization/mcp)
- [TrackHS API Documentation](https://api.trackhs.com/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io/specification)

## Soporte

Si tienes problemas con la conexión:

1. **Revisar logs** en FastMCP Cloud dashboard
2. **Verificar configuración** de variables de entorno
3. **Probar conectividad** con los scripts de ejemplo
4. **Contactar soporte** de FastMCP Cloud o TrackHS

---

**Última actualización**: 17 de Octubre, 2025
**Versión**: 1.0
**Compatibilidad**: FastMCP Cloud, ElevenLabs, Claude Desktop
