"""
Tests para validación de respuestas de API con Pydantic.
Fase 3 - Validación: Validar respuestas de API.
"""

import pytest

from src.trackhs_mcp.exceptions import ValidationError
from src.trackhs_mcp.schemas import (
    FolioResponse,
    ReservationResponse,
    UnitResponse,
    WorkOrderResponse,
)


def test_validate_response_exists():
    """Verifica que la función de validación existe"""
    from src.trackhs_mcp.server import validate_response

    assert validate_response is not None
    assert callable(validate_response)


def test_validate_reservation_response_valid():
    """Test validación exitosa de respuesta de reserva"""
    from src.trackhs_mcp.server import validate_response

    valid_data = {
        "id": 123,
        "confirmation_number": "ABC123",
        "status": "confirmed",
        "arrival": "2024-01-15",
        "departure": "2024-01-20",
        "guest": {"name": "John Doe"},  # Campo extra permitido
    }

    result = validate_response(valid_data, ReservationResponse, strict=False)

    assert result["id"] == 123
    assert result["confirmation_number"] == "ABC123"
    assert result["status"] == "confirmed"


def test_validate_reservation_response_minimal():
    """Test validación con campos mínimos requeridos"""
    from src.trackhs_mcp.server import validate_response

    minimal_data = {"id": 456}  # Solo ID requerido

    result = validate_response(minimal_data, ReservationResponse, strict=False)

    assert result["id"] == 456


def test_validate_reservation_response_invalid_strict():
    """Test validación estricta con datos inválidos"""
    from src.trackhs_mcp.server import validate_response

    invalid_data = {"no_id": "missing"}  # Falta ID requerido

    with pytest.raises(ValidationError):
        validate_response(invalid_data, ReservationResponse, strict=True)


def test_validate_reservation_response_invalid_non_strict():
    """Test validación no-estricta con datos inválidos retorna datos originales"""
    from src.trackhs_mcp.server import validate_response

    invalid_data = {"no_id": "missing"}

    result = validate_response(invalid_data, ReservationResponse, strict=False)

    # En modo no-strict, retorna datos originales si falla
    assert result == invalid_data


def test_validate_unit_response_valid():
    """Test validación de respuesta de unidad"""
    from src.trackhs_mcp.server import validate_response

    valid_data = {
        "id": 789,
        "name": "Penthouse Suite",
        "code": "PH-01",
        "bedrooms": 3,
        "bathrooms": 2,
    }

    result = validate_response(valid_data, UnitResponse, strict=False)

    assert result["id"] == 789
    assert result["name"] == "Penthouse Suite"
    assert result["bedrooms"] == 3


def test_validate_folio_response_valid():
    """Test validación de respuesta de folio"""
    from src.trackhs_mcp.server import validate_response

    valid_data = {
        "id": 111,
        "reservation_id": 222,
        "balance": 500.50,
        "total": 1500.00,
    }

    result = validate_response(valid_data, FolioResponse, strict=False)

    assert result["id"] == 111
    assert result["reservation_id"] == 222
    assert result["balance"] == 500.50


def test_validate_work_order_response_valid():
    """Test validación de respuesta de work order"""
    from src.trackhs_mcp.server import validate_response

    valid_data = {"id": 333, "status": "pending", "unit_id": 444, "priority": 3}

    result = validate_response(valid_data, WorkOrderResponse, strict=False)

    assert result["id"] == 333
    assert result["status"] == "pending"
    assert result["unit_id"] == 444


def test_validate_response_with_extra_fields():
    """Test que campos extra son permitidos (extra='allow')"""
    from src.trackhs_mcp.server import validate_response

    data_with_extras = {
        "id": 555,
        "extra_field_1": "value1",
        "extra_field_2": 123,
        "nested": {"deep": "value"},
    }

    result = validate_response(data_with_extras, ReservationResponse, strict=False)

    assert result["id"] == 555
    # Campos extra deben estar presentes
    assert "extra_field_1" in result
    assert "extra_field_2" in result


def test_models_have_correct_config():
    """Verifica que los modelos tienen configuración correcta"""
    assert ReservationResponse.model_config["extra"] == "allow"
    assert UnitResponse.model_config["extra"] == "allow"
    assert FolioResponse.model_config["extra"] == "allow"
    assert WorkOrderResponse.model_config["extra"] == "allow"


def test_validate_response_type_coercion():
    """Test que Pydantic hace coerción de tipos cuando es posible"""
    from src.trackhs_mcp.server import validate_response

    data_with_string_id = {
        "id": "123",  # String que puede convertirse a int
        "status": "active",
    }

    result = validate_response(data_with_string_id, ReservationResponse, strict=False)

    # Pydantic debe convertir string a int
    assert result["id"] == 123
    assert isinstance(result["id"], int)


def test_reservation_response_model_directly():
    """Test creación directa del modelo ReservationResponse"""
    reservation = ReservationResponse(
        id=999, confirmation_number="TEST999", status="confirmed"
    )

    assert reservation.id == 999
    assert reservation.confirmation_number == "TEST999"
    assert reservation.status == "confirmed"


def test_unit_response_model_directly():
    """Test creación directa del modelo UnitResponse"""
    unit = UnitResponse(id=888, name="Test Unit", bedrooms=2, bathrooms=1)

    assert unit.id == 888
    assert unit.name == "Test Unit"
    assert unit.bedrooms == 2


def test_folio_response_model_directly():
    """Test creación directa del modelo FolioResponse"""
    folio = FolioResponse(id=777, reservation_id=666, balance=100.0, total=500.0)

    assert folio.id == 777
    assert folio.reservation_id == 666
    assert folio.balance == 100.0


def test_work_order_response_model_directly():
    """Test creación directa del modelo WorkOrderResponse"""
    wo = WorkOrderResponse(id=555, status="in-progress", unit_id=444, priority=5)

    assert wo.id == 555
    assert wo.status == "in-progress"
    assert wo.unit_id == 444
    assert wo.priority == 5


if __name__ == "__main__":
    print("🧪 Ejecutando tests de validación de respuestas...")

    try:
        test_validate_response_exists()
        print("✅ Test 1: Función exists")

        test_validate_reservation_response_valid()
        print("✅ Test 2: Validación reserva válida")

        test_validate_reservation_response_minimal()
        print("✅ Test 3: Validación con campos mínimos")

        test_validate_unit_response_valid()
        print("✅ Test 4: Validación unidad válida")

        test_models_have_correct_config()
        print("✅ Test 5: Configuración de modelos")

        print("\n🎉 Tests básicos pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
