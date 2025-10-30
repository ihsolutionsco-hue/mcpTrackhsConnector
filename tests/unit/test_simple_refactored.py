"""
Test simple para verificar la refactorización
"""

import os
import sys
from unittest.mock import Mock, patch

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))


def test_server_creation():
    """Test básico de creación del servidor"""
    print("Test: Creacion del servidor")

    try:
        from _server import TrackHSServer

        # Crear servidor (sin credenciales)
        server = TrackHSServer()

        # Verificar que se creó
        assert server is not None
        assert hasattr(server, "api_client")
        assert hasattr(server, "mcp_server")
        assert hasattr(server, "tools")

        print("OK Servidor se crea correctamente")
        return True

    except Exception as error:
        print(f"ERROR Error creando servidor: {error}")
        return False


def test_server_logic_functions():
    """Test de las funciones de lógica del servidor"""
    print("Test: Funciones de logica")

    try:
        from server_logic import create_api_client, create_mcp_server, register_tools

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

        print("OK Funciones de logica funcionan correctamente")
        return True

    except Exception as error:
        print(f"ERROR Error en funciones de logica: {error}")
        return False


def test_server_structure():
    """Test de la estructura del servidor"""
    print("Test: Estructura del servidor")

    try:
        from _server import TrackHSServer

        # Crear servidor
        server = TrackHSServer()

        # Verificar métodos principales
        assert hasattr(server, "run")
        assert hasattr(server, "close")
        assert hasattr(server, "__enter__")
        assert hasattr(server, "__exit__")

        print("OK Estructura del servidor es correcta")
        return True

    except Exception as error:
        print(f"ERROR Error en estructura: {error}")
        return False


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=== Ejecutando tests simples del servidor refactorizado ===\n")

    tests = [test_server_creation, test_server_logic_functions, test_server_structure]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"=== Resultados: {passed}/{total} tests pasaron ===")

    if passed == total:
        print("TODOS LOS TESTS PASARON EXITOSAMENTE")
        return True
    else:
        print("ALGUNOS TESTS FALLARON")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
