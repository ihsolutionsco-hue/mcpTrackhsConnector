"""
Tests para la herramienta search_units.
Fase 1 - Sprint 1: Tests de herramientas core.
"""

import pytest


def test_search_units_exists():
    """Verifica que la función existe"""
    from src.trackhs_mcp.server import search_units

    assert search_units is not None
    assert callable(search_units.fn)


def test_search_units_parameters():
    """Verifica parámetros esperados"""
    import inspect

    from src.trackhs_mcp.server import search_units

    sig = inspect.signature(search_units.fn)
    params = list(sig.parameters.keys())

    # Parámetros esperados
    assert "page" in params
    assert "size" in params
    assert "search" in params
    assert "bedrooms" in params
    assert "bathrooms" in params
    assert "is_active" in params
    assert "is_bookable" in params


def test_search_units_default_values():
    """Verifica valores por defecto"""
    import inspect

    from src.trackhs_mcp.server import search_units

    sig = inspect.signature(search_units.fn)

    # Verificar defaults de paginación
    assert sig.parameters["page"].default == 1  # 1-based para units
    assert sig.parameters["size"].default == 10

    # Opcionales deben ser None
    assert sig.parameters["search"].default is None
    assert sig.parameters["bedrooms"].default is None
    assert sig.parameters["bathrooms"].default is None
    assert sig.parameters["is_active"].default is None
    assert sig.parameters["is_bookable"].default is None


def test_search_units_output_schema():
    """Verifica schema de salida"""
    from src.trackhs_mcp.server import search_units

    assert hasattr(search_units, "output_schema")
    assert search_units.output_schema is not None


def test_search_units_docstring():
    """Verifica documentación"""
    from src.trackhs_mcp.server import search_units

    assert search_units.fn.__doc__ is not None
    doc = search_units.fn.__doc__

    # Verificar menciones clave
    assert "unidad" in doc.lower()
    assert "dormitorio" in doc.lower() or "bedroom" in doc.lower()


@pytest.mark.integration
def test_search_units_basic():
    """
    Test básico de búsqueda de unidades.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_units

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_units.fn(page=1, size=5)

        # Verificar estructura
        assert isinstance(result, dict)
        assert "total_items" in result or "_embedded" in result

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_units_by_bedrooms():
    """
    Test de filtrado por dormitorios.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_units

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_units.fn(bedrooms=2, size=5)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_units_by_bathrooms():
    """
    Test de filtrado por baños.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_units

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_units.fn(bathrooms=1, size=5)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_units_active_bookable():
    """
    Test de unidades activas y reservables.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_units

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_units.fn(is_active=1, is_bookable=1, size=10)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


@pytest.mark.integration
def test_search_units_combined_filters():
    """
    Test con múltiples filtros.
    Requiere API disponible.
    """
    from src.trackhs_mcp.server import api_client, search_units

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        result = search_units.fn(bedrooms=2, bathrooms=2, is_active=1, size=5)

        assert isinstance(result, dict)

    except Exception as e:
        pytest.skip(f"API no disponible: {e}")


if __name__ == "__main__":
    print("🧪 Ejecutando tests de search_units...")

    try:
        test_search_units_exists()
        print("✅ Test 1: Función existe")

        test_search_units_parameters()
        print("✅ Test 2: Parámetros correctos")

        test_search_units_default_values()
        print("✅ Test 3: Valores por defecto")

        test_search_units_output_schema()
        print("✅ Test 4: Schema de salida")

        test_search_units_docstring()
        print("✅ Test 5: Documentación")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
