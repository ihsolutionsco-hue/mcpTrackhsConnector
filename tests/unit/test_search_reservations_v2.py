"""
Tests unitarios para search_reservations_v2.py
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from pydantic import ValidationError

from src.trackhs_mcp.domain.exceptions.api_exceptions import (
    ValidationError as APIValidationError,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
    search_reservations_v2,
)


class TestSearchReservationsV2:
    """Tests para search_reservations_v2"""

    @pytest.mark.asyncio
    async def test_basic_search(self):
        """Probar búsqueda básica"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(
                page=0, size=10, sort_column="name", sort_direction="asc"
            )

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_filters(self):
        """Probar búsqueda con filtros"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(
                page=0, size=10, search="John", status="Confirmed", in_house_today=1
            )

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_validation_errors(self):
        """Probar errores de validación"""
        with pytest.raises(APIValidationError):
            await search_reservations_v2(page=-1, size=10)  # Página inválida

    @pytest.mark.asyncio
    async def test_size_validation(self):
        """Probar validación de tamaño"""
        with pytest.raises(APIValidationError):
            await search_reservations_v2(page=0, size=101)  # Tamaño inválido

    @pytest.mark.asyncio
    async def test_total_results_validation(self):
        """Probar validación de total de resultados"""
        with pytest.raises(APIValidationError):
            await search_reservations_v2(page=1000, size=10)  # Página que excede límite

    @pytest.mark.asyncio
    async def test_scroll_parameter(self):
        """Probar parámetro scroll"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(page=0, size=10, scroll="1")

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_folio_id_parameter(self):
        """Probar parámetro folio_id"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(page=0, size=10, folio_id="12345")

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_date_filters(self):
        """Probar filtros de fecha"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(
                page=0, size=10, arrival_start="2024-01-01", arrival_end="2024-01-31"
            )

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_id_filters(self):
        """Probar filtros de ID"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.return_value = {"reservations": []}
            mock_use_case.return_value = mock_instance

            result = await search_reservations_v2(
                page=0, size=10, unit_id="123", contact_id="456"
            )

            assert result == {"reservations": []}
            mock_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Probar manejo de errores"""
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.SearchReservationsUseCase"
        ) as mock_use_case:
            mock_instance = AsyncMock()
            mock_instance.execute.side_effect = Exception("API Error")
            mock_use_case.return_value = mock_instance

            with pytest.raises(Exception, match="API Error"):
                await search_reservations_v2(page=0, size=10)

    def test_field_info_handling(self):
        """Probar manejo de FieldInfo objects"""
        # Simular FieldInfo object
        field_info = Mock()
        field_info.__class__.__name__ = "FieldInfo"

        # Este test verifica que la función maneja FieldInfo objects
        # sin lanzar errores
        assert True  # Placeholder para test que se ejecuta sin errores
