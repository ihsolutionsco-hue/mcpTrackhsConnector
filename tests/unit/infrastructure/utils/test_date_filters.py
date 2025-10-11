"""
Tests consolidados para filtros de fecha
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_reservations import (
    _is_valid_date_format,
    _normalize_date_format,
)


class TestDateFilters:
    """Tests consolidados para filtros de fecha"""

    def test_normalize_date_format_solo_fecha(self):
        """Test normalización de fecha solo (YYYY-MM-DD)"""
        # Solo fecha
        result = _normalize_date_format("2025-01-01")
        assert result == "2025-01-01T00:00:00Z"

        result = _normalize_date_format("2024-12-31")
        assert result == "2024-12-31T00:00:00Z"

    def test_normalize_date_format_con_tiempo_sin_timezone(self):
        """Test normalización de fecha con tiempo sin timezone"""
        # Fecha con tiempo sin timezone
        result = _normalize_date_format("2025-01-01T00:00:00")
        assert result == "2025-01-01T00:00:00Z"

        result = _normalize_date_format("2025-01-01T23:59:59")
        assert result == "2025-01-01T23:59:59Z"

    def test_normalize_date_format_ya_normalizado(self):
        """Test que fechas ya normalizadas no cambien"""
        # Ya tiene timezone Z
        result = _normalize_date_format("2025-01-01T00:00:00Z")
        assert result == "2025-01-01T00:00:00Z"

        # Ya tiene timezone offset
        result = _normalize_date_format("2025-01-01T00:00:00+00:00")
        assert result == "2025-01-01T00:00:00+00:00"

    def test_is_valid_date_format_solo_fecha(self):
        """Test validación de formato solo fecha"""
        # Solo fecha válida
        assert _is_valid_date_format("2025-01-01") == True
        assert _is_valid_date_format("2024-12-31") == True

        # Solo fecha inválida
        assert _is_valid_date_format("2025-13-01") == False
        assert _is_valid_date_format("2025-01-32") == False
        assert _is_valid_date_format("invalid") == False

    def test_is_valid_date_format_con_tiempo(self):
        """Test validación de formato con tiempo"""
        # Con tiempo válido
        assert _is_valid_date_format("2025-01-01T00:00:00") == True
        assert _is_valid_date_format("2025-01-01T23:59:59") == True
        assert _is_valid_date_format("2025-01-01T00:00:00Z") == True
        assert _is_valid_date_format("2025-01-01T00:00:00+00:00") == True

        # Con tiempo inválido
        assert _is_valid_date_format("2025-01-01T25:00:00") == False
        assert _is_valid_date_format("2025-01-01T00:60:00") == False
        assert _is_valid_date_format("2025-01-01T00:00:60") == False

    def test_date_normalization_comprehensive(self):
        """Test comprehensivo de normalización de fechas"""
        test_cases = [
            # (input, expected_output, description)
            ("2025-01-01", "2025-01-01T00:00:00Z", "Solo fecha básica"),
            ("2025-01-31", "2025-01-31T00:00:00Z", "Solo fecha fin de mes"),
            (
                "2025-01-01T00:00:00",
                "2025-01-01T00:00:00Z",
                "Fecha con tiempo sin timezone",
            ),
            (
                "2025-01-01T23:59:59",
                "2025-01-01T23:59:59Z",
                "Fecha con tiempo final sin timezone",
            ),
            ("2025-01-01T00:00:00Z", "2025-01-01T00:00:00Z", "Ya normalizada con Z"),
            (
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "Ya normalizada con offset",
            ),
            (
                "2025-01-01T00:00:00.123",
                "2025-01-01T00:00:00.123Z",
                "Con microsegundos sin timezone",
            ),
            (
                "2025-01-01T00:00:00.123Z",
                "2025-01-01T00:00:00.123Z",
                "Con microsegundos y timezone Z",
            ),
        ]

        for input_date, expected, description in test_cases:
            result = _normalize_date_format(input_date)
            assert (
                result == expected
            ), f"Failed for {description}: {input_date} -> {result}"

    def test_date_validation_comprehensive(self):
        """Test comprehensivo de validación de fechas"""
        valid_cases = [
            "2025-01-01",
            "2025-01-01T00:00:00",
            "2025-01-01T00:00:00Z",
            "2025-01-01T00:00:00+00:00",
            "2025-01-01T00:00:00-05:00",
            "2025-01-01T00:00:00.123Z",
            "2025-01-01T00:00:00.123456Z",
        ]

        invalid_cases = [
            "invalid",
            "2025-13-01",
            "2025-01-32",
            "2025-01-01T25:00:00",
            "2025-01-01T00:60:00",
            "2025-01-01T00:00:60",
            "2025/01/01",
            "01-01-2025",
        ]

        for date_str in valid_cases:
            assert _is_valid_date_format(date_str), f"Should be valid: {date_str}"

        for date_str in invalid_cases:
            assert not _is_valid_date_format(date_str), f"Should be invalid: {date_str}"
