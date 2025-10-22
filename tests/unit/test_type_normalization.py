"""
Tests unitarios para type_normalization.py
"""

import pytest
from unittest.mock import Mock

from src.trackhs_mcp.infrastructure.utils.type_normalization import (
    _is_field_info,
    normalize_int,
    normalize_binary_int,
    normalize_bool,
    normalize_float,
    normalize_positive_int,
    normalize_string_to_int,
    normalize_string_to_float,
    normalize_string_to_bool,
)
from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


class TestIsFieldInfo:
    """Tests para _is_field_info"""

    def test_field_info_detection(self):
        """Probar detección de FieldInfo objects"""
        # Mock FieldInfo object
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        assert _is_field_info(field_info) is True

    def test_non_field_info(self):
        """Probar que valores normales no son FieldInfo"""
        assert _is_field_info(42) is False
        assert _is_field_info("test") is False
        assert _is_field_info(None) is False
        assert _is_field_info(True) is False


class TestNormalizeInt:
    """Tests para normalize_int"""

    def test_int_values(self):
        """Probar valores int directos"""
        assert normalize_int(42, "test") == 42
        assert normalize_int(0, "test") == 0
        assert normalize_int(-5, "test") == -5

    def test_float_values(self):
        """Probar valores float que se pueden convertir a int"""
        assert normalize_int(42.0, "test") == 42
        assert normalize_int(0.0, "test") == 0

    def test_float_with_decimals(self):
        """Probar que float con decimales falla"""
        with pytest.raises(ValidationError, match="must be an integer"):
            normalize_int(42.5, "test")

    def test_string_values(self):
        """Probar valores string que se pueden convertir a int"""
        assert normalize_int("42", "test") == 42
        assert normalize_int("0", "test") == 0
        assert normalize_int("-5", "test") == -5

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValidationError, match="must be a valid integer string"):
            normalize_int("abc", "test")

        with pytest.raises(ValidationError, match="must be a valid integer string"):
            normalize_int("42.5", "test")

    def test_empty_string(self):
        """Probar string vacío"""
        with pytest.raises(ValidationError, match="cannot be empty string"):
            normalize_int("", "test")

    def test_none_value(self):
        """Probar valor None"""
        assert normalize_int(None, "test") is None

    def test_field_info(self):
        """Probar FieldInfo object"""
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        assert normalize_int(field_info, "test") is None


class TestNormalizeBinaryInt:
    """Tests para normalize_binary_int"""

    def test_int_values(self):
        """Probar valores int válidos"""
        assert normalize_binary_int(1, "test") == 1
        assert normalize_binary_int(0, "test") == 0

    def test_boolean_values(self):
        """Probar valores booleanos"""
        assert normalize_binary_int(True, "test") == 1
        assert normalize_binary_int(False, "test") == 0

    def test_string_values(self):
        """Probar valores string válidos"""
        assert normalize_binary_int("1", "test") == 1
        assert normalize_binary_int("0", "test") == 0

    def test_float_values(self):
        """Probar valores float válidos"""
        assert normalize_binary_int(1.0, "test") == 1
        assert normalize_binary_int(0.0, "test") == 0

    def test_invalid_values(self):
        """Probar valores inválidos"""
        with pytest.raises(ValidationError, match="must be 0 or 1"):
            normalize_binary_int(2, "test")

        with pytest.raises(ValidationError, match="must be 0 or 1"):
            normalize_binary_int(-1, "test")

    def test_none_value(self):
        """Probar valor None"""
        assert normalize_binary_int(None, "test") is None

    def test_field_info(self):
        """Probar FieldInfo object"""
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        assert normalize_binary_int(field_info, "test") is None


class TestNormalizeBool:
    """Tests para normalize_bool"""

    def test_bool_values(self):
        """Probar valores bool directos"""
        assert normalize_bool(True, "test") is True
        assert normalize_bool(False, "test") is False

    def test_int_values(self):
        """Probar valores int"""
        assert normalize_bool(1, "test") is True
        assert normalize_bool(0, "test") is False
        assert normalize_bool(42, "test") is True

    def test_float_values(self):
        """Probar valores float"""
        assert normalize_bool(1.0, "test") is True
        assert normalize_bool(0.0, "test") is False
        assert normalize_bool(42.5, "test") is True

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_bool("true", "test") is True
        assert normalize_bool("false", "test") is False
        assert normalize_bool("1", "test") is True
        assert normalize_bool("0", "test") is False

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValidationError, match="must be a valid boolean string"):
            normalize_bool("invalid", "test")

    def test_none_value(self):
        """Probar valor None"""
        assert normalize_bool(None, "test") is None

    def test_field_info(self):
        """Probar FieldInfo object"""
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        assert normalize_bool(field_info, "test") is None


class TestNormalizeFloat:
    """Tests para normalize_float"""

    def test_float_values(self):
        """Probar valores float directos"""
        assert normalize_float(42.5, "test") == 42.5
        assert normalize_float(0.0, "test") == 0.0

    def test_int_values(self):
        """Probar valores int"""
        assert normalize_float(42, "test") == 42.0
        assert normalize_float(0, "test") == 0.0

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_float("42.5", "test") == 42.5
        assert normalize_float("0", "test") == 0.0

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValidationError, match="must be a valid float string"):
            normalize_float("invalid", "test")

    def test_none_value(self):
        """Probar valor None"""
        assert normalize_float(None, "test") is None

    def test_field_info(self):
        """Probar FieldInfo object"""
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        assert normalize_float(field_info, "test") is None


class TestNormalizePositiveInt:
    """Tests para normalize_positive_int"""

    def test_positive_int_values(self):
        """Probar valores int positivos"""
        assert normalize_positive_int(42, "test") == 42
        assert normalize_positive_int(1, "test") == 1

    def test_zero_value(self):
        """Probar valor cero"""
        assert normalize_positive_int(0, "test") == 0

    def test_negative_values(self):
        """Probar valores negativos"""
        with pytest.raises(ValidationError, match="must be >= 0"):
            normalize_positive_int(-1, "test")

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_positive_int("42", "test") == 42
        assert normalize_positive_int("0", "test") == 0

    def test_none_value(self):
        """Probar valor None"""
        assert normalize_positive_int(None, "test") is None


class TestNormalizeStringToInt:
    """Tests para normalize_string_to_int"""

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_string_to_int("42") == 42
        assert normalize_string_to_int("0") == 0

    def test_int_values(self):
        """Probar valores int"""
        assert normalize_string_to_int(42) == 42
        assert normalize_string_to_int(0) == 0

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValueError):
            normalize_string_to_int("invalid")


class TestNormalizeStringToFloat:
    """Tests para normalize_string_to_float"""

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_string_to_float("42.5") == 42.5
        assert normalize_string_to_float("0.0") == 0.0

    def test_float_values(self):
        """Probar valores float"""
        assert normalize_string_to_float(42.5) == 42.5
        assert normalize_string_to_float(0.0) == 0.0

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValueError):
            normalize_string_to_float("invalid")


class TestNormalizeStringToBool:
    """Tests para normalize_string_to_bool"""

    def test_string_values(self):
        """Probar valores string"""
        assert normalize_string_to_bool("true") is True
        assert normalize_string_to_bool("false") is False
        assert normalize_string_to_bool("1") is True
        assert normalize_string_to_bool("0") is False

    def test_bool_values(self):
        """Probar valores bool"""
        assert normalize_string_to_bool(True) is True
        assert normalize_string_to_bool(False) is False

    def test_invalid_strings(self):
        """Probar strings inválidos"""
        with pytest.raises(ValueError):
            normalize_string_to_bool("invalid")
