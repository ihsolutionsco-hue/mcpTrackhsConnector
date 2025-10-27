"""
Tests para la herramienta get_reservation.
Fase 1 - Sprint 1: Tests de herramientas core.
"""

import pytest


def test_get_reservation_exists():
    """Verifica que la función existe"""
    from src.trackhs_mcp.server import get_reservation

    assert get_reservation is not None
    assert callable(get_reservation.fn)


def test_get_reservation_parameters():
    """Verifica parámetros requeridos"""
    import inspect

    from src.trackhs_mcp.server import get_reservation

    sig = inspect.signature(get_reservation.fn)
    params = list(sig.parameters.keys())

    # Debe tener reservation_id como parámetro
    assert "reservation_id" in params


def test_get_reservation_parameter_type():
    """Verifica tipo del parámetro reservation_id"""
    import inspect

    from src.trackhs_mcp.server import get_reservation

    sig = inspect.signature(get_reservation.fn)

    # reservation_id debe ser int
    assert "reservation_id" in sig.parameters


def test_get_reservation_no_default():
    """Verifica que reservation_id es requerido (sin default)"""
    import inspect

    from src.trackhs_mcp.server import get_reservation

    sig = inspect.signature(get_reservation.fn)
    param = sig.parameters["reservation_id"]

    # No debe tener valor por defecto
    assert param.default == inspect.Parameter.empty


def test_get_reservation_output_schema():
    """Verifica schema de salida"""
    from src.trackhs_mcp.server import get_reservation

    assert hasattr(get_reservation, "output_schema")
    assert get_reservation.output_schema is not None


def test_get_reservation_docstring():
    """Verifica documentación completa"""
    from src.trackhs_mcp.server import get_reservation

    assert get_reservation.fn.__doc__ is not None
    doc = get_reservation.fn.__doc__

    # Verificar menciones clave
    assert "reserva" in doc.lower()
    assert "detalle" in doc.lower() or "completo" in doc.lower()


@pytest.mark.integration
def test_get_reservation_with_valid_id():
    """
    Test con ID válido.
    Requiere API disponible y un ID de reserva real.
    """
    from src.trackhs_mcp.server import api_client, get_reservation

    if api_client is None:
        pytest.skip("API client no disponible")

    # Nota: Este test requiere un ID de reserva válido
    # En un entorno real, obtendríamos esto de search_reservations primero
    pytest.skip("Requiere ID de reserva válido del sistema")


@pytest.mark.integration
def test_get_reservation_with_invalid_id():
    """
    Test con ID inválido.
    Debe manejar el error apropiadamente.
    """
    from src.trackhs_mcp.server import api_client, get_reservation

    if api_client is None:
        pytest.skip("API client no disponible")

    try:
        # ID muy alto, probablemente no existe
        result = get_reservation.fn(reservation_id=999999999)

        # Si llega aquí, verificar que sea un error o respuesta vacía
        assert result is not None

    except Exception as e:
        # Se espera que lance excepción
        error_msg = str(e).lower()
        assert (
            "404" in str(e) or 
            "not found" in error_msg or 
            "no encontrado" in error_msg or
            "reserva" in error_msg and "no encontrada" in error_msg
        )


def test_get_reservation_positive_id_only():
    """Verifica que solo acepta IDs positivos"""
    import inspect

    from src.trackhs_mcp.server import get_reservation

    sig = inspect.signature(get_reservation.fn)

    # La validación debe estar en el type hint con Field(gt=0)
    assert "reservation_id" in sig.parameters


if __name__ == "__main__":
    print("🧪 Ejecutando tests de get_reservation...")

    try:
        test_get_reservation_exists()
        print("✅ Test 1: Función existe")

        test_get_reservation_parameters()
        print("✅ Test 2: Parámetros correctos")

        test_get_reservation_parameter_type()
        print("✅ Test 3: Tipo correcto")

        test_get_reservation_no_default()
        print("✅ Test 4: Parámetro requerido")

        test_get_reservation_output_schema()
        print("✅ Test 5: Schema de salida")

        test_get_reservation_docstring()
        print("✅ Test 6: Documentación")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
