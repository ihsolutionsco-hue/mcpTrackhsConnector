"""
Entry point único para FastMCP Cloud y ejecución local
Sigue las mejores prácticas de FastMCP: un solo entry point
"""

import sys

# Importar clase desde módulo compartido
from _server import TrackHSServer
from server_logic import create_api_client, create_mcp_server, register_tools
from utils.logger import get_logger

# Crear instancia del servidor para FastMCP Cloud
# FastMCP Cloud espera una variable 'server' en el módulo
api_client = create_api_client()
mcp_server = create_mcp_server()

# Configurar herramientas si hay cliente API
if api_client:
    register_tools(mcp_server, api_client)
else:
    logger = get_logger(__name__)
    logger.warning("Cliente API no disponible - herramientas no configuradas")

# Exponer el objeto servidor para FastMCP Cloud
server = mcp_server


def main():
    """Función principal para ejecutar el servidor localmente"""
    try:
        with TrackHSServer() as server_instance:
            server_instance.run()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as main_error:
        logger = get_logger(__name__)
        logger.error(
            "Error ejecutando servidor",
            extra={
                "error_type": type(main_error).__name__,
                "error_message": str(main_error),
            },
        )
        print(f"Error ejecutando servidor: {main_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
