"""
Tests para el health check endpoint del servidor MCP.
Quick Win #3: Verificación de salud del sistema.
"""

from datetime import datetime

import pytest


def test_health_check_resource_exists():
    """Verifica que el recurso health_check existe"""
    from src.trackhs_mcp.server import health_check

    # Verificar que el recurso está registrado
    assert health_check is not None
    assert hasattr(health_check, "fn")  # FunctionResource tiene función subyacente


def test_health_check_function():
    """Verifica que la función health_check funciona correctamente"""
    from src.trackhs_mcp.server import health_check

    # Llamar a la función subyacente
    response = health_check.fn()

    # Verificar campos requeridos
    assert "status" in response
    assert "timestamp" in response
    assert "version" in response

    # Verificar que status es válido
    assert response["status"] in ["healthy", "degraded", "unhealthy"]


def test_health_check_with_api():
    """Verifica health check incluye información de API"""
    from src.trackhs_mcp.server import health_check

    response = health_check.fn()

    # Debe tener dependencias o error
    assert "dependencies" in response or "error" in response

    # Si hay dependencias, verificar estructura de TrackHS API
    if "dependencies" in response:
        assert "trackhs_api" in response["dependencies"]
        api_status = response["dependencies"]["trackhs_api"]

        assert "status" in api_status
        assert "base_url" in api_status


def test_health_check_version():
    """Verifica que incluye versión correcta"""
    from src.trackhs_mcp.server import health_check

    response = health_check.fn()

    assert "version" in response
    assert isinstance(response["version"], str)
    assert response["version"] == "2.0.0"


def test_health_check_timestamp():
    """Verifica timestamp en formato ISO"""
    from src.trackhs_mcp.server import health_check

    response = health_check.fn()

    assert "timestamp" in response

    # Verificar formato ISO
    try:
        dt = datetime.fromisoformat(response["timestamp"])
        # Debe ser una fecha reciente (último minuto)
        from datetime import timedelta

        assert (datetime.now() - dt) < timedelta(minutes=1)
    except ValueError:
        pytest.fail("Timestamp no es ISO válido")


if __name__ == "__main__":
    # Ejecutar tests básicos
    print("🧪 Ejecutando tests de health check...")

    try:
        test_health_check_structure()
        print("✅ Test 1: Estructura correcta")

        test_health_check_version()
        print("✅ Test 2: Versión incluida")

        test_health_check_timestamp_format()
        print("✅ Test 3: Timestamp válido")

        test_health_check_handles_errors_gracefully()
        print("✅ Test 4: Manejo de errores")

        test_health_check_with_api_available()
        print("✅ Test 5: API disponible")

        print("\n🎉 Todos los tests pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
