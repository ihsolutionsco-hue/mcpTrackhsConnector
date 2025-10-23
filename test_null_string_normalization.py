"""
Test para verificar que la normalización de strings "null" funciona correctamente.

Este test valida que cuando un LLM envía el string literal "null" en lugar
de omitir el parámetro, el sistema lo convierte automáticamente a None.
"""

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_optional_string,
)


class TestNormalizeOptionalString:
    """Tests para la función normalize_optional_string"""

    def test_normalize_null_string(self):
        """Debe convertir el string 'null' a None"""
        result = normalize_optional_string("null", "test_param")
        assert result is None

    def test_normalize_none_string(self):
        """Debe convertir el string 'None' a None"""
        result = normalize_optional_string("None", "test_param")
        assert result is None

    def test_normalize_empty_string(self):
        """Debe convertir string vacío a None"""
        result = normalize_optional_string("", "test_param")
        assert result is None

    def test_normalize_whitespace_string(self):
        """Debe convertir string solo con espacios a None"""
        result = normalize_optional_string("   ", "test_param")
        assert result is None

    def test_normalize_none_value(self):
        """Debe retornar None cuando recibe None"""
        result = normalize_optional_string(None, "test_param")
        assert result is None

    def test_normalize_valid_string(self):
        """Debe retornar el string limpio cuando es válido"""
        result = normalize_optional_string("2024-01-15", "test_param")
        assert result == "2024-01-15"

    def test_normalize_string_with_whitespace(self):
        """Debe limpiar espacios pero mantener el valor"""
        result = normalize_optional_string("  2024-01-15  ", "test_param")
        assert result == "2024-01-15"

    def test_normalize_case_insensitive_null(self):
        """Debe convertir 'NULL', 'Null', etc. a None"""
        assert normalize_optional_string("NULL", "test_param") is None
        assert normalize_optional_string("Null", "test_param") is None
        assert normalize_optional_string("nULl", "test_param") is None

    def test_normalize_case_insensitive_none(self):
        """Debe convertir 'NONE', 'NoNe', etc. a None"""
        assert normalize_optional_string("NONE", "test_param") is None
        assert normalize_optional_string("NoNe", "test_param") is None

    def test_normalize_invalid_type(self):
        """Debe lanzar error cuando el valor no es string ni None"""
        with pytest.raises(ValidationError) as exc_info:
            normalize_optional_string(123, "test_param")

        assert "must be a string or None" in str(exc_info.value)


class TestSearchReservationsWithNullStrings:
    """Tests de integración para search_reservations con strings 'null'"""

    @pytest.mark.asyncio
    async def test_search_with_null_string_dates(self, mock_api_client):
        """
        Simula el caso real: LLM envía "null" en lugar de omitir el parámetro.

        Esto debe funcionar sin error y convertir "null" a None automáticamente.
        """
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            search_reservations_v2,
        )

        # Simular que el LLM envía "null" como string
        result = await search_reservations_v2(
            mock_api_client,
            page=0,
            size=2,
            arrival_start="null",  # ❌ LLM envía string "null"
            arrival_end="null",  # ❌ LLM envía string "null"
        )

        # ✅ Debe funcionar sin error (no lanzar ValidationError)
        # Esto demuestra que "null" fue convertido a None automáticamente
        assert result is not None
        assert "data" in result or "error" not in str(result)

    @pytest.mark.asyncio
    async def test_search_with_mixed_valid_and_null_params(self, mock_api_client):
        """
        Caso mixto: algunos parámetros válidos, otros "null".
        """
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            search_reservations_v2,
        )

        result = await search_reservations_v2(
            mock_api_client,
            page=0,
            size=10,
            arrival_start="2024-01-15",  # ✅ Válido
            arrival_end="null",  # ❌ String "null"
            search="John Smith",  # ✅ Válido
            status="null",  # ❌ String "null"
        )

        assert result is not None


@pytest.fixture
def mock_api_client():
    """Mock del cliente API para tests"""
    from unittest.mock import AsyncMock, MagicMock

    client = MagicMock()

    # Mock del método search_request (el que realmente se llama)
    async def mock_search_request(*args, **kwargs):
        return {
            "data": [],
            "meta": {"total": 0, "page": 0, "size": 10},
        }

    client.search_request = mock_search_request
    return client


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
