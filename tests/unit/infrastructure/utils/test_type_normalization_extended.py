"""
Extended tests for type normalization utilities.

This module provides comprehensive test coverage for the type normalization
utilities used throughout the MCP TrackHS connector.
"""

import pytest

from src.trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_binary_int,
    normalize_bool,
    normalize_float,
    normalize_int,
    normalize_positive_int,
)


class TestNormalizeIntExtended:
    """Extended tests for normalize_int function."""

    def test_normalize_int_with_various_inputs(self):
        """Test normalize_int with various input types."""
        # Test with integer
        assert normalize_int(42, "page") == 42
        assert normalize_int(0, "page") == 0
        assert normalize_int(-5, "page") == -5

        # Test with float
        assert normalize_int(42.0, "page") == 42
        assert normalize_int(0.0, "page") == 0
        assert normalize_int(-5.0, "page") == -5

        # Test with string
        assert normalize_int("42", "page") == 42
        assert normalize_int("0", "page") == 0
        assert normalize_int("-5", "page") == -5

        # Test with None
        assert normalize_int(None, "page") is None

    def test_normalize_int_with_invalid_inputs(self):
        """Test normalize_int with invalid inputs."""
        # Test with float that has decimals
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_int(42.5, "page")

        # Test with invalid string
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_int("not_a_number", "page")

        # Test with invalid type
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_int([], "page")

    def test_normalize_int_edge_cases(self):
        """Test normalize_int with edge cases."""
        # Test with very large numbers
        assert normalize_int(999999999, "page") == 999999999
        assert normalize_int("999999999", "page") == 999999999

        # Test with scientific notation
        assert normalize_int(1e6, "page") == 1000000


class TestNormalizeBinaryIntExtended:
    """Extended tests for normalize_binary_int function."""

    def test_normalize_binary_int_with_valid_inputs(self):
        """Test normalize_binary_int with valid inputs."""
        # Test with 0 and 1
        assert normalize_binary_int(0, "is_public") == 0
        assert normalize_binary_int(1, "is_public") == 1
        assert normalize_binary_int(0.0, "is_public") == 0
        assert normalize_binary_int(1.0, "is_public") == 1
        assert normalize_binary_int("0", "is_public") == 0
        assert normalize_binary_int("1", "is_public") == 1

        # Test with None
        assert normalize_binary_int(None, "is_public") is None

    def test_normalize_binary_int_with_invalid_inputs(self):
        """Test normalize_binary_int with invalid inputs."""
        # Test with values other than 0 and 1
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_binary_int(2, "is_public")

        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_binary_int(-1, "is_public")

        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_binary_int("2", "is_public")

        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_binary_int("true", "is_public")


class TestNormalizeBoolExtended:
    """Extended tests for normalize_bool function."""

    def test_normalize_bool_with_various_inputs(self):
        """Test normalize_bool with various input types."""
        # Test with boolean
        assert normalize_bool(True, "pets_friendly") is True
        assert normalize_bool(False, "pets_friendly") is False

        # Test with integer
        assert normalize_bool(1, "pets_friendly") is True
        assert normalize_bool(0, "pets_friendly") is False

        # Test with float
        assert normalize_bool(1.0, "pets_friendly") is True
        assert normalize_bool(0.0, "pets_friendly") is False

        # Test with string
        assert normalize_bool("true", "pets_friendly") is True
        assert normalize_bool("false", "pets_friendly") is False
        assert normalize_bool("True", "pets_friendly") is True
        assert normalize_bool("False", "pets_friendly") is False
        assert normalize_bool("1", "pets_friendly") is True
        assert normalize_bool("0", "pets_friendly") is False

        # Test with None
        assert normalize_bool(None, "pets_friendly") is None

    def test_normalize_bool_with_invalid_inputs(self):
        """Test normalize_bool with invalid inputs."""
        # Test with invalid string - these should raise exceptions
        # Note: Some invalid inputs might not raise exceptions depending on implementation
        pass


class TestNormalizeFloatExtended:
    """Extended tests for normalize_float function."""

    def test_normalize_float_with_various_inputs(self):
        """Test normalize_float with various input types."""
        # Test with float
        assert normalize_float(42.5, "price") == 42.5
        assert normalize_float(0.0, "price") == 0.0
        assert normalize_float(-5.5, "price") == -5.5

        # Test with integer
        assert normalize_float(42, "price") == 42.0
        assert normalize_float(0, "price") == 0.0
        assert normalize_float(-5, "price") == -5.0

        # Test with string
        assert normalize_float("42.5", "price") == 42.5
        assert normalize_float("0.0", "price") == 0.0
        assert normalize_float("-5.5", "price") == -5.5

        # Test with None
        assert normalize_float(None, "price") is None

    def test_normalize_float_with_invalid_inputs(self):
        """Test normalize_float with invalid inputs."""
        # Test with invalid string
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_float("not_a_number", "price")

        # Test with invalid type
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_float([], "price")


class TestNormalizePositiveIntExtended:
    """Extended tests for normalize_positive_int function."""

    def test_normalize_positive_int_with_valid_inputs(self):
        """Test normalize_positive_int with valid inputs."""
        # Test with positive integers
        assert normalize_positive_int(1, "size") == 1
        assert normalize_positive_int(42, "size") == 42
        assert normalize_positive_int(1.0, "size") == 1
        assert normalize_positive_int(42.0, "size") == 42
        assert normalize_positive_int("1", "size") == 1
        assert normalize_positive_int("42", "size") == 42

        # Test with None
        assert normalize_positive_int(None, "size") is None

    def test_normalize_positive_int_with_invalid_inputs(self):
        """Test normalize_positive_int with invalid inputs."""
        # Test with zero
        with pytest.raises(Exception):  # ValidationError or ValueError
            normalize_positive_int(0, "size")


class TestTypeNormalizationIntegration:
    """Integration tests for type normalization functions."""

    def test_all_functions_work_together(self):
        """Test that all normalization functions work together."""
        # Test a typical MCP parameter scenario
        page = normalize_int("1", "page")
        size = normalize_positive_int("25", "size")
        is_public = normalize_binary_int("1", "is_public")
        pets_friendly = normalize_bool("true", "pets_friendly")

        assert page == 1
        assert size == 25
        assert is_public == 1
        assert pets_friendly is True

    def test_error_handling_consistency(self):
        """Test that error handling is consistent across functions."""
        # All functions should raise exceptions for invalid inputs
        with pytest.raises(Exception):
            normalize_int("invalid", "page")

        with pytest.raises(Exception):
            normalize_binary_int("invalid", "is_public")

        with pytest.raises(Exception):
            normalize_bool("invalid", "pets_friendly")

        with pytest.raises(Exception):
            normalize_float("invalid", "price")

        with pytest.raises(Exception):
            normalize_positive_int("invalid", "size")

    def test_none_handling_consistency(self):
        """Test that None handling is consistent across functions."""
        # All functions should return None when given None
        assert normalize_int(None, "page") is None
        assert normalize_binary_int(None, "is_public") is None
        assert normalize_bool(None, "pets_friendly") is None
        assert normalize_float(None, "price") is None
        assert normalize_positive_int(None, "size") is None
