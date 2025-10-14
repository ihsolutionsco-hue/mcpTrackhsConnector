# Herramientas de Desarrollo MCP

Esta sección contiene herramientas para desarrollar, probar y depurar servidores y clientes MCP.

## MCP Inspector

**Ubicación**: [inspector/](./inspector/) | [Guía de uso](./guia-inspector.md)

Herramienta interactiva para testing y debugging de servidores MCP.

### Características

- **Testing de servidores**: Prueba servidores MCP locales y remotos
- **Debugging visual**: Interfaz gráfica para inspeccionar herramientas, recursos y prompts
- **Validación de protocolo**: Verifica cumplimiento de la especificación MCP
- **Testing de autenticación**: Prueba flujos OAuth y autenticación

### Instalación y Uso

```bash
# Instalación global
npm install -g @modelcontextprotocol/inspector

# Uso básico
npx @modelcontextprotocol/inspector <comando>

# Ejemplo: Probar servidor local
npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path/to/directory

# Ejemplo: Probar servidor remoto
npx @modelcontextprotocol/inspector https://your-mcp-server.com/mcp
```

### Características Principales

#### 1. Panel de Conexión
- Selección de transporte (stdio, HTTP, SSE)
- Configuración de argumentos de línea de comandos
- Variables de entorno personalizadas

#### 2. Pestaña de Recursos
- Lista todos los recursos disponibles
- Muestra metadatos (tipos MIME, descripciones)
- Permite inspeccionar contenido de recursos
- Soporte para testing de suscripciones

#### 3. Pestaña de Prompts
- Muestra plantillas de prompts disponibles
- Argumentos y descripciones de prompts
- Testing de prompts con argumentos personalizados
- Vista previa de mensajes generados

#### 4. Pestaña de Herramientas
- Lista herramientas disponibles
- Esquemas y descripciones de herramientas
- Testing de herramientas con entradas personalizadas
- Visualización de resultados de ejecución

#### 5. Panel de Notificaciones
- Registro de todos los logs del servidor
- Notificaciones recibidas del servidor
- Debugging de flujos de comunicación

### Flujo de Trabajo de Desarrollo

#### 1. Inicio del Desarrollo
```bash
# Lanzar Inspector con tu servidor
npx @modelcontextprotocol/inspector node path/to/your/server.js

# Verificar conectividad básica
# Revisar negociación de capacidades
```

#### 2. Testing Iterativo
```bash
# Hacer cambios en el servidor
# Reconstruir el servidor
# Reconectar el Inspector
# Probar características afectadas
# Monitorear mensajes
```

#### 3. Testing de Casos Edge
- Entradas inválidas
- Argumentos de prompt faltantes
- Operaciones concurrentes
- Verificar manejo de errores

### Configuración Avanzada

#### Variables de Entorno
```bash
# Configurar variables para el servidor
npx @modelcontextprotocol/inspector \
  --env API_KEY=your-api-key \
  --env DEBUG=true \
  node your-server.js
```

#### Servidores con Dependencias
```bash
# Servidor Python con dependencias
npx @modelcontextprotocol/inspector \
  uv --directory path/to/server run package-name args...

# Servidor Node.js con dependencias
npx @modelcontextprotocol/inspector \
  npm run start -- --arg value
```

### Debugging de Servidores Remotos

#### Configuración de Autenticación
```bash
# Servidor con autenticación OAuth
npx @modelcontextprotocol/inspector \
  --auth-type oauth \
  --auth-url https://auth-server.com/oauth/authorize \
  --client-id your-client-id \
  https://your-mcp-server.com/mcp
```

#### Testing de CORS
```bash
# Verificar configuración CORS
npx @modelcontextprotocol/inspector \
  --cors-origin https://claude.ai \
  https://your-mcp-server.com/mcp
```

## Otras Herramientas

### CLI de MCP (Python)
```bash
# Instalación
pip install mcp[cli]

# Comandos disponibles
mcp --help
mcp dev server.py          # Modo desarrollo
mcp install server.py      # Instalar en Claude Desktop
mcp run server.py          # Ejecutar servidor
```

### Testing Automatizado

#### Jest para Node.js
```javascript
// test/mcp-server.test.js
const { MCPClient } = require('@modelcontextprotocol/client');

describe('MCP Server', () => {
  test('should list tools', async () => {
    const client = new MCPClient('stdio', ['node', 'server.js']);
    await client.connect();

    const tools = await client.listTools();
    expect(tools).toHaveLength(1);
    expect(tools[0].name).toBe('test_tool');
  });
});
```

#### Pytest para Python
```python
# test_server.py
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_server_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert len(tools.tools) == 1
            assert tools.tools[0].name == "test_tool"
```

## Mejores Prácticas

### 1. Desarrollo Local
- Usa el Inspector para testing interactivo
- Implementa tests automatizados
- Valida con múltiples clientes

### 2. Testing de Producción
- Prueba con datos reales
- Valida rendimiento bajo carga
- Verifica manejo de errores

### 3. Debugging
- Usa logs estructurados
- Implementa métricas de rendimiento
- Monitorea uso de recursos

## Recursos Adicionales

- **Guía completa del Inspector**: [guia-inspector.md](./guia-inspector.md)
- **Ejemplos de testing**: [04-ejemplos/](../04-ejemplos/)
- **Mejores prácticas**: [02-servidores-remotos/mejores-practicas.md](../02-servidores-remotos/mejores-practicas.md)
- **Referencias técnicas**: [05-referencias/](../05-referencias/)
