"""
Servidor MCP refactorizado para TrackHS
Estructura escalable siguiendo mejores prácticas de FastMCP
"""

import sys
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from server_logic import create_api_client, create_mcp_server, register_tools
from utils.api_client import TrackHSAPIClient
from utils.logger import get_logger


class TrackHSServer:
    """Servidor MCP para TrackHS con estructura escalable"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.api_client: Optional[TrackHSAPIClient] = None
        self.mcp_server: Optional[FastMCP] = None
        self.tools = {}

        # Configurar servidor
        self._setup_server()

    def _setup_server(self) -> None:
        """Configura el servidor completo"""
        try:
            # Crear cliente API
            self.api_client = create_api_client()

            # Crear servidor MCP
            self.mcp_server = create_mcp_server()

            # Registrar herramientas si hay cliente API
            if self.api_client:
                self.tools = register_tools(self.mcp_server, self.api_client)
            else:
                self.logger.warning(
                    "Cliente API no disponible - herramientas no registradas"
                )

        except Exception as setup_error:
            self.logger.error(
                "Error configurando servidor",
                extra={
                    "error_type": type(setup_error).__name__,
                    "error_message": str(setup_error),
                },
            )
            raise

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """
        Ejecuta el servidor MCP

        Args:
            host: Host del servidor
            port: Puerto del servidor
        """
        if not self.mcp_server:
            self.logger.error("Servidor MCP no configurado")
            raise RuntimeError("Servidor MCP no configurado")

        try:
            self.logger.info(
                "Iniciando servidor TrackHS MCP",
                extra={"host": host, "port": port, "tools_count": len(self.tools)},
            )

            self.mcp_server.run(transport="http", host=host, port=port)

        except Exception as server_error:
            self.logger.error(
                "Error ejecutando servidor MCP",
                extra={
                    "host": host,
                    "port": port,
                    "error_type": type(server_error).__name__,
                    "error_message": str(server_error),
                },
            )
            raise

    def close(self) -> None:
        """Cierra el servidor y libera recursos"""
        if self.api_client:
            self.api_client.close()
            self.logger.info("Cliente API cerrado")

        self.logger.info("Servidor TrackHS MCP cerrado")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Función principal para ejecutar el servidor"""
    try:
        with TrackHSServer() as server:
            server.run()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as main_error:
        print(f"Error ejecutando servidor: {main_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
