"""
Tests para la función de sanitización de logs.
Fase 2 - Seguridad: Sanitización de datos sensibles.
"""

import pytest


def test_sanitize_for_log_exists():
    """Verifica que la función exists"""
    from src.trackhs_mcp.server import sanitize_for_log

    assert sanitize_for_log is not None
    assert callable(sanitize_for_log)


def test_sanitize_simple_dict():
    """Test sanitización de diccionario simple"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {"name": "John", "email": "john@example.com", "age": 30}

    result = sanitize_for_log(data)

    assert result["name"] == "John"  # No sensible
    assert result["email"] == "***REDACTED***"  # Sensible
    assert result["age"] == 30  # No sensible


def test_sanitize_phone_numbers():
    """Test sanitización de números de teléfono"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {"phone": "1234567890", "mobile": "0987654321", "name": "John"}

    result = sanitize_for_log(data)

    assert result["phone"] == "***REDACTED***"
    assert result["mobile"] == "***REDACTED***"
    assert result["name"] == "John"


def test_sanitize_nested_dict():
    """Test sanitización de diccionarios anidados"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {
        "user": {"name": "John", "email": "john@example.com"},
        "reservation": {"id": 123, "status": "confirmed"},
    }

    result = sanitize_for_log(data)

    assert result["user"]["name"] == "John"
    assert result["user"]["email"] == "***REDACTED***"
    assert result["reservation"]["id"] == 123
    assert result["reservation"]["status"] == "confirmed"


def test_sanitize_list():
    """Test sanitización de listas"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = [
        {"name": "John", "email": "john@example.com"},
        {"name": "Jane", "email": "jane@example.com"},
    ]

    result = sanitize_for_log(data)

    assert result[0]["name"] == "John"
    assert result[0]["email"] == "***REDACTED***"
    assert result[1]["name"] == "Jane"
    assert result[1]["email"] == "***REDACTED***"


def test_sanitize_password_fields():
    """Test sanitización de contraseñas"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {"username": "admin", "password": "secret123", "pwd": "pass456"}

    result = sanitize_for_log(data)

    assert result["username"] == "admin"
    assert result["password"] == "***REDACTED***"
    assert result["pwd"] == "***REDACTED***"


def test_sanitize_address_fields():
    """Test sanitización de direcciones"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {
        "name": "John",
        "street": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
    }

    result = sanitize_for_log(data)

    assert result["name"] == "John"
    assert result["street"] == "***REDACTED***"
    assert result["city"] == "New York"  # No sensible
    assert result["postal_code"] == "***REDACTED***"


def test_sanitize_payment_fields():
    """Test sanitización de información de pago"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {
        "amount": 100.50,
        "card_number": "4111111111111111",
        "credit_card": "1234",
        "payment_method": "visa",
    }

    result = sanitize_for_log(data)

    assert result["amount"] == 100.50
    assert result["card_number"] == "***REDACTED***"
    assert result["credit_card"] == "***REDACTED***"
    assert result["payment_method"] == "***REDACTED***"


def test_sanitize_email_strings():
    """Test sanitización de strings que parecen emails"""
    from src.trackhs_mcp.server import sanitize_for_log

    # Email directo como string
    email = "john@example.com"
    result = sanitize_for_log(email)

    assert result == "***EMAIL_REDACTED***"


def test_sanitize_none_values():
    """Test sanitización de valores None"""
    from src.trackhs_mcp.server import sanitize_for_log

    assert sanitize_for_log(None) is None


def test_sanitize_primitives():
    """Test sanitización de valores primitivos"""
    from src.trackhs_mcp.server import sanitize_for_log

    assert sanitize_for_log(123) == 123
    assert sanitize_for_log(45.67) == 45.67
    assert sanitize_for_log(True) is True
    assert sanitize_for_log("normal string") == "normal string"


def test_sanitize_max_depth():
    """Test protección contra recursión infinita"""
    from src.trackhs_mcp.server import sanitize_for_log

    # Crear estructura muy anidada
    deep_data = {"level1": {"level2": {"level3": {"level4": {"level5": "value"}}}}}

    result = sanitize_for_log(deep_data, max_depth=3)

    # Debe truncarse en profundidad 3
    assert "***MAX_DEPTH***" in str(result)


def test_sanitize_mixed_case_keys():
    """Test sanitización con claves en mayúsculas/minúsculas"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {"Email": "john@example.com", "PHONE": "123", "PhOnE": "456"}

    result = sanitize_for_log(data)

    # Debe detectar palabras sensibles sin importar mayúsculas
    assert result["Email"] == "***REDACTED***"
    assert result["PHONE"] == "***REDACTED***"
    assert result["PhOnE"] == "***REDACTED***"


def test_sanitize_partial_matches():
    """Test sanitización con palabras sensibles como subcadena"""
    from src.trackhs_mcp.server import sanitize_for_log

    data = {
        "user_email": "john@example.com",
        "contact_phone": "123",
        "billing_address": "123 Main St",
    }

    result = sanitize_for_log(data)

    # Debe detectar 'email', 'phone', 'address' en las claves
    assert result["user_email"] == "***REDACTED***"
    assert result["contact_phone"] == "***REDACTED***"
    assert result["billing_address"] == "***REDACTED***"


if __name__ == "__main__":
    print("🧪 Ejecutando tests de sanitización...")

    try:
        test_sanitize_for_log_exists()
        print("✅ Test 1: Función existe")

        test_sanitize_simple_dict()
        print("✅ Test 2: Dict simple")

        test_sanitize_phone_numbers()
        print("✅ Test 3: Teléfonos")

        test_sanitize_nested_dict()
        print("✅ Test 4: Dict anidado")

        test_sanitize_password_fields()
        print("✅ Test 5: Contraseñas")

        test_sanitize_email_strings()
        print("✅ Test 6: Emails")

        print("\n🎉 Tests unitarios pasaron!")

    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
