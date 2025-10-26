"""
Tests para validadores de reglas de negocio.
Fase 3 - Validación: Reglas de negocio.
"""

import pytest

from src.trackhs_mcp.validators import (
    BusinessValidationError,
    validate_cost,
    validate_date_format,
    validate_date_range,
    validate_integer_range,
    validate_positive_number,
    validate_priority,
    validate_reservation_dates,
    validate_string_length,
    validate_string_not_empty,
    validate_unit_capacity,
    validate_work_order_description,
    validate_work_order_summary,
)


def test_validate_date_format_valid():
    """Test validación de fecha válida"""
    assert validate_date_format("2024-01-15") is True
    assert validate_date_format("2024-12-31") is True


def test_validate_date_format_invalid():
    """Test validación de fecha inválida"""
    with pytest.raises(BusinessValidationError):
        validate_date_format("2024-13-01")  # Mes inválido

    with pytest.raises(BusinessValidationError):
        validate_date_format("2024-02-30")  # Día inválido

    with pytest.raises(BusinessValidationError):
        validate_date_format("01-15-2024")  # Formato incorrecto


def test_validate_date_range_valid():
    """Test validación de rango de fechas válido"""
    assert validate_date_range("2024-01-01", "2024-01-10") is True
    assert validate_date_range("2024-01-15", "2024-02-15") is True


def test_validate_date_range_invalid():
    """Test validación de rango de fechas inválido"""
    with pytest.raises(BusinessValidationError):
        validate_date_range("2024-01-10", "2024-01-05")  # End antes de start

    with pytest.raises(BusinessValidationError):
        validate_date_range("2024-01-15", "2024-01-15")  # Misma fecha


def test_validate_positive_number_valid():
    """Test validación de número positivo válido"""
    assert validate_positive_number(100.5) is True
    assert validate_positive_number(1) is True
    assert validate_positive_number(0.01) is True


def test_validate_positive_number_invalid():
    """Test validación de número positivo inválido"""
    with pytest.raises(BusinessValidationError):
        validate_positive_number(-1)

    with pytest.raises(BusinessValidationError):
        validate_positive_number(0)  # No allow_zero por defecto


def test_validate_positive_number_with_zero():
    """Test validación permitiendo cero"""
    assert validate_positive_number(0, allow_zero=True) is True
    assert validate_positive_number(100, allow_zero=True) is True


def test_validate_integer_range_valid():
    """Test validación de rango de enteros válido"""
    assert validate_integer_range(5, 1, 10) is True
    assert validate_integer_range(1, 1, 10) is True  # En límite inferior
    assert validate_integer_range(10, 1, 10) is True  # En límite superior


def test_validate_integer_range_invalid():
    """Test validación de rango de enteros inválido"""
    with pytest.raises(BusinessValidationError):
        validate_integer_range(0, 1, 10)  # Menor que mínimo

    with pytest.raises(BusinessValidationError):
        validate_integer_range(11, 1, 10)  # Mayor que máximo


def test_validate_string_not_empty_valid():
    """Test validación de string no vacío válido"""
    assert validate_string_not_empty("Hello") is True
    assert validate_string_not_empty("A") is True


def test_validate_string_not_empty_invalid():
    """Test validación de string vacío"""
    with pytest.raises(BusinessValidationError):
        validate_string_not_empty("")

    with pytest.raises(BusinessValidationError):
        validate_string_not_empty("   ")  # Solo espacios


def test_validate_string_length_valid():
    """Test validación de longitud de string válida"""
    assert validate_string_length("Hello", min_length=3, max_length=10) is True
    assert validate_string_length("Hi", min_length=2) is True
    assert validate_string_length("Test", max_length=10) is True


def test_validate_string_length_invalid():
    """Test validación de longitud de string inválida"""
    with pytest.raises(BusinessValidationError):
        validate_string_length("Hi", min_length=5)  # Muy corto

    with pytest.raises(BusinessValidationError):
        validate_string_length("Hello World!", max_length=5)  # Muy largo


def test_validate_priority_valid():
    """Test validación de prioridad válida"""
    assert validate_priority(1) is True
    assert validate_priority(3) is True
    assert validate_priority(5) is True


def test_validate_priority_invalid():
    """Test validación de prioridad inválida"""
    with pytest.raises(BusinessValidationError):
        validate_priority(0)

    with pytest.raises(BusinessValidationError):
        validate_priority(2)

    with pytest.raises(BusinessValidationError):
        validate_priority(4)


def test_validate_reservation_dates_valid():
    """Test validación de fechas de reserva válidas"""
    assert validate_reservation_dates("2024-01-15", "2024-01-20") is True


def test_validate_reservation_dates_invalid():
    """Test validación de fechas de reserva inválidas"""
    with pytest.raises(BusinessValidationError):
        validate_reservation_dates("2024-01-20", "2024-01-15")  # Orden incorrecto


def test_validate_unit_capacity_valid():
    """Test validación de capacidad de unidad válida"""
    assert validate_unit_capacity(bedrooms=3, bathrooms=2) is True
    assert validate_unit_capacity(bedrooms=0) is True  # Studio
    assert validate_unit_capacity(bathrooms=1) is True


def test_validate_unit_capacity_invalid():
    """Test validación de capacidad de unidad inválida"""
    with pytest.raises(BusinessValidationError):
        validate_unit_capacity(bedrooms=25)  # Más de 20

    with pytest.raises(BusinessValidationError):
        validate_unit_capacity(bedrooms=-1)  # Negativo


def test_validate_cost_valid():
    """Test validación de costo válido"""
    assert validate_cost(100.50) is True
    assert validate_cost(0) is True  # Cero es válido
    assert validate_cost(1000000.99) is True


def test_validate_cost_invalid():
    """Test validación de costo inválido"""
    with pytest.raises(BusinessValidationError):
        validate_cost(-10.50)  # Negativo


def test_validate_work_order_summary_valid():
    """Test validación de resumen de work order válido"""
    assert validate_work_order_summary("Fuga en grifo") is True
    assert validate_work_order_summary("A" * 500) is True  # Máximo 500


def test_validate_work_order_summary_invalid():
    """Test validación de resumen de work order inválido"""
    with pytest.raises(BusinessValidationError):
        validate_work_order_summary("")  # Vacío

    with pytest.raises(BusinessValidationError):
        validate_work_order_summary("Hi")  # Muy corto (< 5)

    with pytest.raises(BusinessValidationError):
        validate_work_order_summary("A" * 501)  # Muy largo (> 500)


def test_validate_work_order_description_valid():
    """Test validación de descripción de work order válida"""
    assert (
        validate_work_order_description("Grifo del baño principal gotea constantemente")
        is True
    )
    assert validate_work_order_description("A" * 5000) is True  # Máximo 5000


def test_validate_work_order_description_invalid():
    """Test validación de descripción de work order inválida"""
    with pytest.raises(BusinessValidationError):
        validate_work_order_description("")  # Vacío

    with pytest.raises(BusinessValidationError):
        validate_work_order_description("Short")  # Muy corto (< 10)

    with pytest.raises(BusinessValidationError):
        validate_work_order_description("A" * 5001)  # Muy largo (> 5000)


def test_business_validation_error_is_exception():
    """Test que BusinessValidationError es una excepción"""
    assert issubclass(BusinessValidationError, Exception)


def test_error_messages_are_descriptive():
    """Test que mensajes de error son descriptivos"""
    try:
        validate_date_format("invalid", "test_field")
    except BusinessValidationError as e:
        assert "test_field" in str(e)
        assert "YYYY-MM-DD" in str(e)

    try:
        validate_priority(2)
    except BusinessValidationError as e:
        assert "1" in str(e) and "3" in str(e) and "5" in str(e)


if __name__ == "__main__":
    print("🧪 Ejecutando tests de validadores de negocio...")

    try:
        test_validate_date_format_valid()
        print("✅ Test 1: Formato de fecha válido")

        test_validate_date_range_valid()
        print("✅ Test 2: Rango de fechas válido")

        test_validate_positive_number_valid()
        print("✅ Test 3: Número positivo válido")

        test_validate_priority_valid()
        print("✅ Test 4: Prioridad válida")

        test_validate_work_order_summary_valid()
        print("✅ Test 5: Resumen de work order válido")

        print("\n🎉 Tests básicos pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
