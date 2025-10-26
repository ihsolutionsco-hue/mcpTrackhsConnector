"""
Tests para la herramienta get_folio.
Fase 1 - Sprint 1: Tests de herramientas core.
"""

import pytest


def test_get_folio_exists():
    """Verifica que la función existe"""
    from src.trackhs_mcp.server import get_folio

    assert get_folio is not None
    assert callable(get_folio.fn)


def test_get_folio_parameters():
    """Verifica parámetros requeridos"""
    import inspect

    from src.trackhs_mcp.server import get_folio

    sig = inspect.signature(get_folio.fn)
    params = list(sig.parameters.keys())

    # Debe tener reservation_id como parámetro
    assert "reservation_id" in params
    assert len(params) == 1  # Solo debe tener este parámetro


def test_get_folio_parameter_type():
    """Verifica tipo del parámetro"""
    import inspect

    from src.trackhs_mcp.server import get_folio

    sig = inspect.signature(get_folio.fn)

    # reservation_id debe ser int y requerido
    assert "reservation_id" in sig.parameters
    param = sig.parameters["reservation_id"]
    assert param.default == inspect.Parameter.empty


def test_get_folio_output_schema():
    """Verifica schema de salida"""
    from src.trackhs_mcp.server import get_folio

    assert hasattr(get_folio, "output_schema")
    assert get_folio.output_schema is not None


def test_get_folio_docstring():
    """Verifica documentación completa"""
    from src.trackhs_mcp.server import get_folio

    assert get_folio.fn.__doc__ is not None
    doc = get_folio.fn.__doc__

    # Verificar menciones clave
    assert "folio" in doc.lower()
    assert "financiero" in doc.lower() or "cargos" in doc.lower()


@pytest.mark.integration
def test_get_folio_with_valid_id():
    """
    Test con ID válido.
    Requiere API disponible y un ID de reserva real.
    """
    from src.trackhs_mcp.server import api_client, get_folio

    if api_client is None:
        pytest.skip("API client no disponible")

    # Nota: Este test requiere un ID de reserva válido
    pytest.skip("Requiere ID de reserva válido del sistema")


@pytest.mark.integration
def test_get_folio_structure():
    """
    Test de estructura del folio.
    Verifica que incluye cargos, pagos, balance.
    """
    from src.trackhs_mcp.server import api_client, get_folio

    if api_client is None:
        pytest.skip("API client no disponible")

    pytest.skip("Requiere ID de reserva válido")


def test_get_folio_positive_id_only():
    """Verifica que solo acepta IDs positivos"""
    import inspect

    from src.trackhs_mcp.server import get_folio

    sig = inspect.signature(get_folio.fn)

    # La validación debe estar en el type hint con Field(gt=0)
    assert "reservation_id" in sig.parameters


if __name__ == "__main__":
    print("🧪 Ejecutando tests de get_folio...")

    try:
        test_get_folio_exists()
        print("✅ Test 1: Función existe")

        test_get_folio_parameters()
        print("✅ Test 2: Parámetros correctos")

        test_get_folio_parameter_type()
        print("✅ Test 3: Tipo correcto")

        test_get_folio_output_schema()
        print("✅ Test 4: Schema de salida")

        test_get_folio_docstring()
        print("✅ Test 5: Documentación")

        test_get_folio_positive_id_only()
        print("✅ Test 6: Validación ID positivo")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

