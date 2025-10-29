"""
Test unitario para servidor refactorizado
Verifica que la refactorización mantenga la funcionalidad
"""

import os
import sys
from unittest.mock import Mock, patch

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from server import TrackHSServer
from server_logic import create_api_client, create_mcp_server, register_tools


def test_server_initialization():
    """Test que el servidor se inicializa correctamente"""
    print("Test: Inicializacion del servidor")

    # Mock de las dependencias
    with (
        patch("server.create_api_client") as mock_api_client,
        patch("server.create_mcp_server") as mock_mcp_server,
        patch("server.register_tools") as mock_register_tools,
    ):

        # Configurar mocks
        mock_api_client.return_value = Mock()
        mock_mcp_server.return_value = Mock()
        mock_register_tools.return_value = {"test_tool": Mock()}

        # Crear servidor
        server = TrackHSServer()

        # Verificar que se llamaron las funciones
        mock_api_client.assert_called_once()
        mock_mcp_server.assert_called_once()
        mock_register_tools.assert_called_once()

        print("OK Servidor se inicializa correctamente")


def test_server_without_credentials():
    """Test que el servidor maneja correctamente la falta de credenciales"""
    print("Test: Servidor sin credenciales")

    with (
        patch("server.create_api_client") as mock_api_client,
        patch("server.create_mcp_server") as mock_mcp_server,
        patch("server.register_tools") as mock_register_tools,
    ):

        # Configurar mocks - sin credenciales
        mock_api_client.return_value = None
        mock_mcp_server.return_value = Mock()
        mock_register_tools.return_value = {}

        # Crear servidor
        server = TrackHSServer()

        # Verificar que se llamaron las funciones
        mock_api_client.assert_called_once()
        mock_mcp_server.assert_called_once()
        mock_register_tools.assert_not_called()  # No se registran herramientas sin API

        print("OK Servidor maneja correctamente la falta de credenciales")


def test_server_run():
    """Test que el servidor puede ejecutarse"""
    print("Test: Ejecucion del servidor")

    with (
        patch("server.create_api_client") as mock_api_client,
        patch("server.create_mcp_server") as mock_mcp_server,
        patch("server.register_tools") as mock_register_tools,
    ):

        # Configurar mocks
        mock_api_client.return_value = Mock()
        mock_mcp_server.return_value = Mock()
        mock_register_tools.return_value = {"test_tool": Mock()}

        # Crear servidor
        server = TrackHSServer()

        # Mock del método run del servidor MCP
        server.mcp_server.run = Mock()

        # Ejecutar servidor
        server.run(host="localhost", port=8000)

        # Verificar que se llamó run
        server.mcp_server.run.assert_called_once_with(
            transport="http", host="localhost", port=8000
        )

        print("OK Servidor se ejecuta correctamente")


def test_server_close():
    """Test que el servidor se cierra correctamente"""
    print("Test: Cierre del servidor")

    with (
        patch("server.create_api_client") as mock_api_client,
        patch("server.create_mcp_server") as mock_mcp_server,
        patch("server.register_tools") as mock_register_tools,
    ):

        # Configurar mocks
        mock_api_client.return_value = Mock()
        mock_mcp_server.return_value = Mock()
        mock_register_tools.return_value = {"test_tool": Mock()}

        # Crear servidor
        server = TrackHSServer()

        # Mock del método close del cliente API
        server.api_client.close = Mock()

        # Cerrar servidor
        server.close()

        # Verificar que se llamó close
        server.api_client.close.assert_called_once()

        print("OK Servidor se cierra correctamente")


def test_context_manager():
    """Test que el servidor funciona como context manager"""
    print("Test: Context manager")

    with (
        patch("server.create_api_client") as mock_api_client,
        patch("server.create_mcp_server") as mock_mcp_server,
        patch("server.register_tools") as mock_register_tools,
    ):

        # Configurar mocks
        mock_api_client.return_value = Mock()
        mock_mcp_server.return_value = Mock()
        mock_register_tools.return_value = {"test_tool": Mock()}

        # Usar como context manager
        with TrackHSServer() as server:
            assert server is not None
            assert hasattr(server, "api_client")
            assert hasattr(server, "mcp_server")
            assert hasattr(server, "tools")

        print("OK Servidor funciona como context manager")


def test_server_logic_functions():
    """Test que las funciones de lógica del servidor funcionan"""
    print("Test: Funciones de logica del servidor")

    # Test create_api_client sin credenciales
    with patch.dict(os.environ, {}, clear=True):
        api_client = create_api_client()
        assert api_client is None
        print("OK create_api_client maneja falta de credenciales")

    # Test create_mcp_server
    with patch("fastmcp.FastMCP") as mock_fastmcp:
        mock_fastmcp.return_value = Mock()
        mcp_server = create_mcp_server()
        assert mcp_server is not None
        print("OK create_mcp_server funciona correctamente")

    # Test register_tools
    with patch("tools.TOOLS", [Mock]) as mock_tools:
        mock_tool_class = Mock()
        mock_tool_instance = Mock()
        mock_tool_instance.name = "test_tool"
        mock_tool_instance.description = "Test tool"
        mock_tool_class.return_value = mock_tool_instance

        mock_tools[0] = mock_tool_class

        mock_mcp_server = Mock()
        mock_api_client = Mock()

        tools = register_tools(mock_mcp_server, mock_api_client)

        assert "test_tool" in tools
        print("OK register_tools funciona correctamente")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=== Ejecutando tests del servidor refactorizado ===\n")

    try:
        test_server_initialization()
        test_server_without_credentials()
        test_server_run()
        test_server_close()
        test_context_manager()
        test_server_logic_functions()

        print("\n=== Todos los tests pasaron exitosamente ===")
        return True

    except Exception as test_error:
        print(f"\nERROR Error en test: {test_error}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
