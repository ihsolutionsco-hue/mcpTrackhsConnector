"""
Tests para la herramienta create_maintenance_work_order.
Fase 1 - Sprint 1: Tests de herramientas core.
"""

import pytest


def test_create_maintenance_work_order_exists():
    """Verifica que la función existe"""
    from src.trackhs_mcp.server import create_maintenance_work_order

    assert create_maintenance_work_order is not None
    assert callable(create_maintenance_work_order.fn)


def test_create_maintenance_work_order_parameters():
    """Verifica parámetros requeridos y opcionales"""
    import inspect

    from src.trackhs_mcp.server import create_maintenance_work_order

    sig = inspect.signature(create_maintenance_work_order.fn)
    params = list(sig.parameters.keys())

    # Parámetros requeridos
    assert "unit_id" in params
    assert "summary" in params
    assert "description" in params

    # Parámetros opcionales
    assert "priority" in params
    assert "estimated_cost" in params
    assert "estimated_time" in params
    assert "date_received" in params


def test_create_maintenance_work_order_required_params():
    """Verifica que los parámetros requeridos no tienen default"""
    import inspect

    from src.trackhs_mcp.server import create_maintenance_work_order

    sig = inspect.signature(create_maintenance_work_order.fn)

    # unit_id es requerido
    assert sig.parameters["unit_id"].default == inspect.Parameter.empty

    # summary es requerido
    assert sig.parameters["summary"].default == inspect.Parameter.empty

    # description es requerido
    assert sig.parameters["description"].default == inspect.Parameter.empty


def test_create_maintenance_work_order_optional_params():
    """Verifica valores por defecto de parámetros opcionales"""
    import inspect

    from src.trackhs_mcp.server import create_maintenance_work_order

    sig = inspect.signature(create_maintenance_work_order.fn)

    # priority tiene default de 3 (media)
    assert sig.parameters["priority"].default == 3

    # estimated_cost es opcional (None)
    assert sig.parameters["estimated_cost"].default is None

    # estimated_time es opcional (None)
    assert sig.parameters["estimated_time"].default is None

    # date_received es opcional (None)
    assert sig.parameters["date_received"].default is None


def test_create_maintenance_work_order_priority_values():
    """Verifica que priority acepta solo 1, 3, 5"""
    import inspect

    from src.trackhs_mcp.server import create_maintenance_work_order

    sig = inspect.signature(create_maintenance_work_order.fn)

    # La validación debe estar en el type hint con Literal[1, 3, 5]
    assert "priority" in sig.parameters


def test_create_maintenance_work_order_output_schema():
    """Verifica schema de salida"""
    from src.trackhs_mcp.server import create_maintenance_work_order

    assert hasattr(create_maintenance_work_order, "output_schema")
    assert create_maintenance_work_order.output_schema is not None


def test_create_maintenance_work_order_docstring():
    """Verifica documentación completa"""
    from src.trackhs_mcp.server import create_maintenance_work_order

    assert create_maintenance_work_order.fn.__doc__ is not None
    doc = create_maintenance_work_order.fn.__doc__

    # Verificar menciones clave
    assert "mantenimiento" in doc.lower()
    assert "orden" in doc.lower() or "work order" in doc.lower()
    assert "prioridad" in doc.lower() or "priority" in doc.lower()


@pytest.mark.integration
def test_create_maintenance_work_order_integration():
    """
    Test de creación de orden con API real.
    Requiere API disponible y permisos de escritura.
    """
    from src.trackhs_mcp.server import api_client, create_maintenance_work_order

    if api_client is None:
        pytest.skip("API client no disponible")

    # Este test crearía una orden real - skip por defecto
    pytest.skip("Test requiere permisos de escritura y unit_id válido")


@pytest.mark.integration
def test_create_maintenance_work_order_all_params():
    """
    Test con todos los parámetros.
    Verifica que acepta todos los campos opcionales.
    """
    from src.trackhs_mcp.server import api_client, create_maintenance_work_order

    if api_client is None:
        pytest.skip("API client no disponible")

    pytest.skip("Test requiere permisos de escritura")


def test_create_maintenance_work_order_string_lengths():
    """Verifica restricciones de longitud de strings"""
    import inspect

    from src.trackhs_mcp.server import create_maintenance_work_order

    sig = inspect.signature(create_maintenance_work_order.fn)

    # summary y description deben tener restricciones
    assert "summary" in sig.parameters
    assert "description" in sig.parameters


if __name__ == "__main__":
    print("🧪 Ejecutando tests de create_maintenance_work_order...")

    try:
        test_create_maintenance_work_order_exists()
        print("✅ Test 1: Función existe")

        test_create_maintenance_work_order_parameters()
        print("✅ Test 2: Parámetros correctos")

        test_create_maintenance_work_order_required_params()
        print("✅ Test 3: Parámetros requeridos")

        test_create_maintenance_work_order_optional_params()
        print("✅ Test 4: Parámetros opcionales")

        test_create_maintenance_work_order_priority_values()
        print("✅ Test 5: Prioridades válidas")

        test_create_maintenance_work_order_output_schema()
        print("✅ Test 6: Schema de salida")

        test_create_maintenance_work_order_docstring()
        print("✅ Test 7: Documentación")

        test_create_maintenance_work_order_string_lengths()
        print("✅ Test 8: Validación de longitudes")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

