"""
Tests para el módulo de normalización de tipos.

Este módulo prueba las funciones de normalización de tipos
que resuelven la incompatibilidad entre JSON-RPC y Python type hints.

Autor: Track HS MCP Team
Fecha: Octubre 2025
"""

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_binary_int,
    normalize_bool,
    normalize_float,
    normalize_int,
    normalize_positive_int,
)


class TestNormalizeInt:
    """Tests para normalize_int()"""

    def test_int_passthrough(self):
        """int → int (sin conversión)"""
        assert normalize_int(42, "test") == 42
        assert normalize_int(0, "test") == 0
        assert normalize_int(-10, "test") == -10

    def test_float_to_int(self):
        """float sin decimales → int"""
        assert normalize_int(42.0, "test") == 42
        assert normalize_int(0.0, "test") == 0
        assert normalize_int(-10.0, "test") == -10

    def test_float_with_decimals_raises(self):
        """float con decimales → ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_int(42.5, "test")
        assert "test" in str(exc_info.value)
        assert "decimals" in str(exc_info.value)

    def test_string_to_int(self):
        """string numérico → int"""
        assert normalize_int("42", "test") == 42
        assert normalize_int("0", "test") == 0
        assert normalize_int("-10", "test") == -10
        assert normalize_int("  42  ", "test") == 42  # Con espacios

    def test_invalid_string_raises(self):
        """string no numérico → ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_int("not_a_number", "test")
        assert "test" in str(exc_info.value)

        with pytest.raises(ValidationError):
            normalize_int("42.5", "test")  # Decimal como string

        with pytest.raises(ValidationError):
            normalize_int("", "test")  # String vacío

        with pytest.raises(ValidationError):
            normalize_int("   ", "test")  # Solo espacios

    def test_none_returns_none(self):
        """None → None (para parámetros opcionales)"""
        assert normalize_int(None, "test") is None

    def test_invalid_type_raises(self):
        """Tipo inválido → ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_int([1, 2, 3], "test")
        assert "test" in str(exc_info.value)

        with pytest.raises(ValidationError):
            normalize_int({"key": "value"}, "test")


class TestNormalizeBinaryInt:
    """Tests para normalize_binary_int()"""

    def test_zero_and_one(self):
        """0 y 1 válidos"""
        assert normalize_binary_int(0, "test") == 0
        assert normalize_binary_int(1, "test") == 1

    def test_zero_and_one_as_float(self):
        """0.0 y 1.0 como float"""
        assert normalize_binary_int(0.0, "test") == 0
        assert normalize_binary_int(1.0, "test") == 1

    def test_zero_and_one_as_string(self):
        """'0' y '1' como string"""
        assert normalize_binary_int("0", "test") == 0
        assert normalize_binary_int("1", "test") == 1

    def test_invalid_values_raise(self):
        """Valores fuera de [0, 1] → ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_binary_int(2, "test")
        assert "0 or 1" in str(exc_info.value)

        with pytest.raises(ValidationError):
            normalize_binary_int(-1, "test")

        with pytest.raises(ValidationError):
            normalize_binary_int(42, "test")

    def test_none_returns_none(self):
        """None → None"""
        assert normalize_binary_int(None, "test") is None

    def test_invalid_string_raises(self):
        """String inválido → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_binary_int("2", "test")

        with pytest.raises(ValidationError):
            normalize_binary_int("true", "test")


class TestNormalizeBool:
    """Tests para normalize_bool()"""

    def test_bool_passthrough(self):
        """bool → bool"""
        assert normalize_bool(True, "test") is True
        assert normalize_bool(False, "test") is False

    def test_int_to_bool(self):
        """int → bool (0=False, cualquier otro=True)"""
        assert normalize_bool(0, "test") is False
        assert normalize_bool(1, "test") is True
        assert normalize_bool(42, "test") is True
        assert normalize_bool(-1, "test") is True

    def test_float_to_bool(self):
        """float → bool (0.0=False, cualquier otro=True)"""
        assert normalize_bool(0.0, "test") is False
        assert normalize_bool(1.0, "test") is True
        assert normalize_bool(42.5, "test") is True
        assert normalize_bool(-1.5, "test") is True

    def test_string_to_bool(self):
        """string → bool"""
        # True values
        assert normalize_bool("true", "test") is True
        assert normalize_bool("TRUE", "test") is True
        assert normalize_bool("True", "test") is True
        assert normalize_bool("1", "test") is True
        assert normalize_bool("yes", "test") is True
        assert normalize_bool("YES", "test") is True
        assert normalize_bool("y", "test") is True
        assert normalize_bool("t", "test") is True

        # False values
        assert normalize_bool("false", "test") is False
        assert normalize_bool("FALSE", "test") is False
        assert normalize_bool("False", "test") is False
        assert normalize_bool("0", "test") is False
        assert normalize_bool("no", "test") is False
        assert normalize_bool("NO", "test") is False
        assert normalize_bool("n", "test") is False
        assert normalize_bool("f", "test") is False

    def test_string_with_spaces(self):
        """string con espacios"""
        assert normalize_bool("  true  ", "test") is True
        assert normalize_bool("  false  ", "test") is False

    def test_invalid_string_raises(self):
        """string inválido → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_bool("maybe", "test")

        with pytest.raises(ValidationError):
            normalize_bool("2", "test")

        with pytest.raises(ValidationError):
            normalize_bool("", "test")

    def test_none_returns_none(self):
        """None → None"""
        assert normalize_bool(None, "test") is None

    def test_invalid_type_raises(self):
        """Tipo inválido → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_bool([True], "test")


class TestNormalizeFloat:
    """Tests para normalize_float()"""

    def test_float_passthrough(self):
        """float → float"""
        assert normalize_float(42.5, "test") == 42.5
        assert normalize_float(0.0, "test") == 0.0
        assert normalize_float(-10.5, "test") == -10.5

    def test_int_to_float(self):
        """int → float"""
        assert normalize_float(42, "test") == 42.0
        assert normalize_float(0, "test") == 0.0
        assert normalize_float(-10, "test") == -10.0

    def test_string_to_float(self):
        """string → float"""
        assert normalize_float("42.5", "test") == 42.5
        assert normalize_float("0.0", "test") == 0.0
        assert normalize_float("-10.5", "test") == -10.5
        assert normalize_float("  42.5  ", "test") == 42.5  # Con espacios

    def test_invalid_string_raises(self):
        """string inválido → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_float("not_a_number", "test")

        with pytest.raises(ValidationError):
            normalize_float("", "test")

    def test_none_returns_none(self):
        """None → None"""
        assert normalize_float(None, "test") is None

    def test_invalid_type_raises(self):
        """Tipo inválido → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_float([42.5], "test")


class TestNormalizePositiveInt:
    """Tests para normalize_positive_int()"""

    def test_positive_int(self):
        """int positivo → int"""
        assert normalize_positive_int(0, "test") == 0
        assert normalize_positive_int(1, "test") == 1
        assert normalize_positive_int(42, "test") == 42

    def test_negative_int_raises(self):
        """int negativo → ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_positive_int(-1, "test")
        assert ">= 0" in str(exc_info.value)

        with pytest.raises(ValidationError):
            normalize_positive_int(-10, "test")

    def test_positive_float_to_int(self):
        """float positivo sin decimales → int"""
        assert normalize_positive_int(42.0, "test") == 42
        assert normalize_positive_int(0.0, "test") == 0

    def test_positive_string_to_int(self):
        """string positivo → int"""
        assert normalize_positive_int("42", "test") == 42
        assert normalize_positive_int("0", "test") == 0

    def test_negative_string_raises(self):
        """string negativo → ValidationError"""
        with pytest.raises(ValidationError):
            normalize_positive_int("-1", "test")

    def test_none_returns_none(self):
        """None → None"""
        assert normalize_positive_int(None, "test") is None


class TestEdgeCases:
    """Tests de casos límite"""

    def test_very_large_numbers(self):
        """Números muy grandes"""
        large = 999999999999
        assert normalize_int(large, "test") == large
        assert normalize_int(str(large), "test") == large

    def test_scientific_notation(self):
        """Notación científica"""
        # float en notación científica funciona
        assert normalize_float(1e10, "test") == 1e10

        # int en notación científica funciona si no tiene decimales
        assert normalize_int(1e2, "test") == 100

        # string en notación científica NO funciona (por diseño)
        with pytest.raises(ValidationError):
            normalize_int("1e2", "test")


class TestParameterNames:
    """Tests que verifican que el nombre del parámetro aparece en errores"""

    def test_parameter_name_in_error_message(self):
        """El nombre del parámetro debe aparecer en el mensaje de error"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_int("invalid", "my_custom_param")
        assert "my_custom_param" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            normalize_binary_int(5, "another_param")
        assert "another_param" in str(exc_info.value)


class TestRealWorldScenarios:
    """Tests con escenarios del mundo real (MCP/JSON-RPC)"""

    def test_mcp_page_parameter(self):
        """Simula parámetro 'page' desde MCP"""
        # Cliente puede enviar cualquiera de estos:
        assert normalize_int(1, "page") == 1  # int directo
        assert normalize_int(1.0, "page") == 1  # JSON number como float
        assert normalize_int("1", "page") == 1  # string

    def test_mcp_in_house_today_parameter(self):
        """Simula parámetro 'in_house_today' desde MCP (Issue #2)"""
        # Cliente puede enviar cualquiera de estos:
        assert normalize_binary_int(0, "in_house_today") == 0
        assert normalize_binary_int(1, "in_house_today") == 1
        assert normalize_binary_int(1.0, "in_house_today") == 1  # JSON number
        assert normalize_binary_int("1", "in_house_today") == 1  # string
        assert normalize_binary_int(None, "in_house_today") is None  # opcional

    def test_mcp_pets_friendly_parameter(self):
        """Simula parámetro 'pets_friendly' desde MCP (Issue #1)"""
        assert normalize_binary_int(0, "pets_friendly") == 0
        assert normalize_binary_int(1, "pets_friendly") == 1
        assert normalize_binary_int(1.0, "pets_friendly") == 1
        assert normalize_binary_int("0", "pets_friendly") == 0
        assert normalize_binary_int(None, "pets_friendly") is None

    def test_mcp_bedrooms_parameter(self):
        """Simula parámetro 'bedrooms' desde MCP"""
        assert normalize_int(2, "bedrooms") == 2
        assert normalize_int(2.0, "bedrooms") == 2
        assert normalize_int("2", "bedrooms") == 2
        assert normalize_int(None, "bedrooms") is None


# Marks para pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.asyncio,
]
