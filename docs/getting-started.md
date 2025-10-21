# Getting Started

This guide will help you get the TrackHS MCP Connector up and running quickly.

## Prerequisites

- Python 3.8 or higher
- pip or uv package manager
- Track HS API credentials
- Basic understanding of MCP (Model Context Protocol)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MCPtrackhsConnector
```

### 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt

# Using uv (recommended)
uv pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Add your Track HS credentials to `.env`:

```env
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password
TRACKHS_TIMEOUT=30
```

### 4. Start the Server

```bash
# Development mode
python -m src.trackhs_mcp

# With specific environment variables
TRACKHS_USERNAME=user TRACKHS_PASSWORD=pass python -m src.trackhs_mcp
```

### 5. Test with MCP Inspector

```bash
# Install MCP Inspector
npx -y @modelcontextprotocol/inspector

# Connect using stdio transport
# The server will be available for MCP connections
```

## Installation Details

### Python Environment

Ensure you have Python 3.8+ installed:

```bash
python --version
# Should show Python 3.8 or higher
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

The project requires these core dependencies:

- **fastmcp**: MCP server framework
- **httpx**: HTTP client for API requests
- **pydantic**: Data validation and settings
- **python-dotenv**: Environment variable management

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRACKHS_API_URL` | Yes | - | Track HS API base URL |
| `TRACKHS_USERNAME` | Yes | - | API username |
| `TRACKHS_PASSWORD` | Yes | - | API password |
| `TRACKHS_TIMEOUT` | No | 30 | Request timeout in seconds |

### Configuration File

Create a `.env` file in the project root:

```env
# Required
TRACKHS_API_URL=https://ihmvacations.trackhs.com/api
TRACKHS_USERNAME=your_username
TRACKHS_PASSWORD=your_password

# Optional
TRACKHS_TIMEOUT=30
DEBUG=false
LOG_LEVEL=INFO
```

## Running the Server

### Development Mode

```bash
# Start with auto-reload
python -m src.trackhs_mcp

# With debug logging
DEBUG=true python -m src.trackhs_mcp
```

### Production Mode

```bash
# Set production environment
export PRODUCTION=true
export DEBUG=false
python -m src.trackhs_mcp
```

### Docker

```bash
# Build image
docker build -t trackhs-mcp-connector .

# Run container
docker run -e TRACKHS_USERNAME=user -e TRACKHS_PASSWORD=pass trackhs-mcp-connector
```

## Testing the Installation

### 1. Verify Server Startup

```bash
python -m src.trackhs_mcp
# Should show: "Starting MCP server 'TrackHS MCP Server'"
```

### 2. Test API Connectivity

```bash
python -c "
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
config = TrackHSConfig.from_env()
client = TrackHSApiClient(config)
print('API connection test:', client.test_connection())
"
```

### 3. Test with MCP Inspector

1. Start the server: `python -m src.trackhs_mcp`
2. Open MCP Inspector: `npx -y @modelcontextprotocol/inspector`
3. Connect using stdio transport
4. Test available tools, resources, and prompts

## First Steps with Claude Desktop

### Método 1: STDIO Transport (Local)

Para desarrollo local, usa STDIO transport:

```json
{
  "mcpServers": {
    "trackhs": {
      "command": "python",
      "args": ["-m", "src.trackhs_mcp"],
      "cwd": "/path/to/MCPtrackhsConnector",
      "env": {
        "TRACKHS_API_URL": "https://ihmvacations.trackhs.com/api",
        "TRACKHS_USERNAME": "your_username",
        "TRACKHS_PASSWORD": "your_password"
      }
    }
  }
}
```

### Método 2: HTTP Transport (Remoto) ⭐ **Recomendado**

Para usar con FastMCP Cloud y ElevenLabs, usa HTTP transport:

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

### 2. Restart Claude Desktop

After configuring, restart Claude Desktop to load the MCP server.

### 3. Test MCP Integration

In Claude Desktop, you can now:

- Use the `search_reservations_v2` tool
- Access Track HS resources and schemas
- Use pre-built prompts for reservation management
- Search units and amenities
- Create work orders

## Conexión HTTP para FastMCP Cloud

### 1. Deploy en FastMCP Cloud

1. Conecta tu repositorio en [FastMCP Cloud](https://fastmcp.cloud)
2. Configura las variables de entorno:
   ```
   TRACKHS_API_URL=https://api.trackhs.com/api
   TRACKHS_USERNAME=tu_usuario
   TRACKHS_PASSWORD=tu_contraseña
   ```
3. Haz push a main para deploy automático

### 2. Obtener URL del Servidor

FastMCP Cloud proporciona automáticamente una URL como:
```
https://tu-servidor.fastmcp.cloud/mcp
```

### 3. Conectar desde Clientes

Usa la URL HTTP para conectar desde:
- **ElevenLabs**: Configuración de servidor MCP personalizado
- **Claude Desktop**: HTTP transport en configuración JSON
- **Clientes Python**: `StreamableHttpTransport`

Ver [Guía de Conexión de Clientes](guides/CLIENT_CONNECTION_GUIDE.md) para ejemplos detallados.

## Common Issues & Solutions

### "Module not found" errors

**Cause**: Missing dependencies or incorrect Python path

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### "Authentication failed"

**Cause**: Invalid credentials or API URL

**Solution**:
```bash
# Verify credentials
echo $TRACKHS_USERNAME
echo $TRACKHS_PASSWORD

# Test API connectivity
curl -u $TRACKHS_USERNAME:$TRACKHS_PASSWORD $TRACKHS_API_URL/health
```

### "Connection timeout"

**Cause**: Network issues or incorrect API URL

**Solution**:
```bash
# Test network connectivity
ping ihmvacations.trackhs.com

# Verify API URL
curl -I https://ihmvacations.trackhs.com/api
```

### "Server not starting"

**Cause**: Port conflicts or configuration issues

**Solution**:
```bash
# Check for port conflicts
lsof -i :8000

# Run with debug logging
DEBUG=true python -m src.trackhs_mcp
```

## Next Steps

Once you have the server running:

1. **Explore Tools**: Try the `search_reservations` tool with different parameters
2. **Use Resources**: Access Track HS schemas and documentation
3. **Try Prompts**: Use pre-built prompts for common tasks
4. **Customize**: See [Customization Guide](customization-guide.md) for extending functionality
5. **Deploy**: See [Deployment Guide](deployment.md) for production deployment

## Getting Help

- **Documentation**: Check the [API Reference](api-reference.md)
- **Architecture**: Learn about [Clean Architecture](architecture.md)
- **Issues**: Report problems on GitHub Issues
- **Support**: Contact the development team

## Examples

See the `examples/` directory for practical usage examples:

- `examples/basic_usage.py`: Basic MCP operations
- `examples/README.md`: Detailed usage instructions
