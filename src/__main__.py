"""
Entry point para FastMCP Cloud
Ejecuta el servidor TrackHS MCP
"""

import os
import sys

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server_logic import create_api_client, create_mcp_server, register_tools

# Crear el servidor MCP para FastMCP Cloud
api_client = create_api_client()
mcp_server = create_mcp_server()

# Registrar herramientas si hay cliente API
if api_client:
    tools = register_tools(mcp_server, api_client)
else:
    print("Warning: Cliente API no disponible - herramientas no registradas")

# Exponer el objeto servidor para FastMCP Cloud
server = mcp_server


def main():
    """Función principal para ejecutar el servidor"""
    try:
        mcp_server.run()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as main_error:
        print(f"Error ejecutando servidor: {main_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
