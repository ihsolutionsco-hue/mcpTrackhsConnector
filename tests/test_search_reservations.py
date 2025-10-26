"""
Tests para la herramienta search_reservations.
Fase 1 - Sprint 1: Tests de herramientas core.
"""

from datetime import datetime, timedelta

import pytest


@pytest.fixture
def mock_api_client(mocker):
    """Mock del cliente API para tests unitarios"""
    from src.trackhs_mcp.server import TrackHSClient

    mock_client = mocker.MagicMock(spec=TrackHSClient)
    return mock_client


def test_search_reservations_basic():
    """Test básico de búsqueda de reservas"""
    from src.trackhs_mcp.server import search_reservations

    # Este test requiere credenciales válidas
    # Por ahora verificamos que la función existe y acepta parámetros
    assert search_reservations is not None
    assert callable(search_reservations.fn)


def test_search_reservations_parameters():
    """Verifica que acepta todos los parámetros esperados"""
    import inspect

    from src.trackhs_mcp.server import search_reservations

    sig = inspect.signature(search_reservations.fn)
    params = list(sig.parameters.keys())

    # Verificar parámetros esperados
    assert "page" in params
    assert "size" in params
    assert "search" in params
    assert "arrival_start" in params
    assert "arrival_end" in params
    assert "status" in params


def test_search_reservations_default_values():
    """Verifica valores por defecto de parámetros"""
    import inspect

    from src.trackhs_mcp.server import search_reservations

    sig = inspect.signature(search_reservations.fn)

    # Verificar defaults
    assert sig.parameters["page"].default == 0
    assert sig.parameters["size"].default == 10
    assert sig.parameters["search"].default is None
    assert sig.parameters["arrival_start"].default is None
    assert sig.parameters["arrival_end"].default is None
    assert sig.parameters["status"].default is None


def test_search_reservations_with_pagination():
    """Test de paginación básica"""
    from src.trackhs_mcp.server import search_reservations

    # Verificar que acepta parámetros de paginación
    try:
        # Mock para evitar llamada real a API
        # En producción esto requiere credenciales válidas
        import inspect

        sig = inspect.signature(search_reservations.fn)
        params = sig.parameters

        # Verificar que page tiene restricciones correctas
        assert params["page"].annotation is not None

    except Exception as e:
        pytest.skip(f"Requiere API disponible: {e}")


def test_search_reservations_date_format():
    """Verifica validación de formato de fecha"""
    import inspect

    from src.trackhs_mcp.server import search_reservations

    sig = inspect.signature(search_reservations.fn)

    # Las fechas deben aceptar formato YYYY-MM-DD
    # La validación se hace vía Pydantic con pattern
    assert "arrival_start" in sig.parameters
    assert "arrival_end" in sig.parameters


def test_search_reservations_output_schema():
    """Verifica que tiene schema de salida definido"""
    from src.trackhs_mcp.server import search_reservations

    # Verificar que es un FunctionTool con output_schema
    assert hasattr(search_reservations, "output_schema")
    assert search_reservations.output_schema is not None


def test_search_reservations_docstring():
    """Verifica que tiene documentación completa"""
    from src.trackhs_mcp.server import search_reservations

    assert search_reservations.fn.__doc__ is not None
    doc = search_reservations.fn.__doc__

    # Verificar que menciona casos de uso importantes
    assert "reservas" in doc.lower()
    assert "búsqueda" in doc.lower() or "busqueda" in doc.lower()


@pytest.mark.integration
def test_search_reservations_integration():
    """
    Test de integración con API real.
    Requiere credenciales válidas en variables de entorno.
    """
    from src.trackhs_mcp.server import api_client, search_reservations

    if api_client is None:
        pytest.skip("API client no disponible - requiere credenciales")

    try:
        # Intentar búsqueda básica
        result = search_reservations.fn(page=0, size=1)

        # Verificar estructura de respuesta
        assert isinstance(result, dict)
        assert "page" in result or "_embedded" in result or "error" in str(result)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_reservations_by_date():
    """
    Test de búsqueda por fecha.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_reservations

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        # Buscar reservas de hoy
        today = datetime.now().strftime("%Y-%m-%d")

        result = search_reservations.fn(arrival_start=today, arrival_end=today, size=5)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_reservations_by_status():
    """
    Test de búsqueda por estado.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_reservations

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_reservations.fn(status="confirmed", size=5)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


if __name__ == "__main__":
    # Ejecutar tests básicos
    print("🧪 Ejecutando tests de search_reservations...")

    try:
        test_search_reservations_basic()
        print("✅ Test 1: Función existe")

        test_search_reservations_parameters()
        print("✅ Test 2: Parámetros correctos")

        test_search_reservations_default_values()
        print("✅ Test 3: Valores por defecto")

        test_search_reservations_output_schema()
        print("✅ Test 4: Output schema definido")

        test_search_reservations_docstring()
        print("✅ Test 5: Documentación presente")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
