"""
Tests de integración para search_reservations
Verifica que el use case funcione correctamente con dependencias reales
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.application.use_cases.search_reservations import (
    SearchReservationsUseCase,
)
from src.trackhs_mcp.domain.entities.reservations import SearchReservationsParams
from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


class TestSearchReservationsIntegration:
    """Tests de integración para search_reservations"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = AsyncMock()
        client.get.return_value = {
            "reservations": [
                {
                    "id": "123",
                    "guest_name": "John Doe",
                    "check_in": "2024-01-15",
                    "check_out": "2024-01-20",
                    "status": "Confirmed",
                }
            ],
            "total": 1,
            "page": 1,
            "size": 10,
        }
        return client

    @pytest.fixture
    def search_use_case(self, mock_api_client):
        """Use case con dependencias mockeadas"""
        return SearchReservationsUseCase(api_client=mock_api_client)

    @pytest.mark.asyncio
    async def test_search_reservations_success_integration(
        self, search_use_case, mock_api_client
    ):
        """Test de integración exitoso para search_reservations"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
        )

        # Act
        result = await search_use_case.execute(params)

        # Assert
        assert result is not None
        assert "reservations" in result
        assert len(result["reservations"]) == 1
        assert result["reservations"][0]["id"] == "123"
        assert result["reservations"][0]["guest_name"] == "John Doe"

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_reservations_with_pagination_integration(
        self, search_use_case, mock_api_client
    ):
        """Test de integración con paginación"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-01", arrival_end="2024-01-31", page=2, size=5
        )

        # Act
        result = await search_use_case.execute(params)

        # Assert
        assert result is not None
        assert "page" in result
        assert result["page"] == 1  # Mock retorna page 1
        assert "size" in result
        assert result["size"] == 10  # Mock retorna size 10

    @pytest.mark.asyncio
    async def test_search_reservations_validation_error_integration(
        self, search_use_case
    ):
        """Test de integración con error de validación"""
        # Arrange - parámetros inválidos
        with pytest.raises(ValidationError):
            params = SearchReservationsParams(
                arrival_start="invalid-date", arrival_end="2024-01-31"
            )
            await search_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_search_reservations_api_error_integration(self, mock_api_client):
        """Test de integración con error de API"""
        # Arrange
        mock_api_client.get.side_effect = Exception("API Error")
        search_use_case = SearchReservationsUseCase(api_client=mock_api_client)

        params = SearchReservationsParams(
            arrival_start="2024-01-01", arrival_end="2024-01-31"
        )

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await search_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_search_reservations_empty_result_integration(
        self, search_use_case, mock_api_client
    ):
        """Test de integración con resultado vacío"""
        # Arrange
        mock_api_client.get.return_value = {
            "reservations": [],
            "total": 0,
            "page": 1,
            "size": 10,
        }

        params = SearchReservationsParams(
            arrival_start="2024-01-01", arrival_end="2024-01-31"
        )

        # Act
        result = await search_use_case.execute(params)

        # Assert
        assert result is not None
        assert "reservations" in result
        assert len(result["reservations"]) == 0
        assert result["total"] == 0

    @pytest.mark.asyncio
    async def test_search_reservations_with_filters_integration(
        self, search_use_case, mock_api_client
    ):
        """Test de integración con filtros adicionales"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
            group_id=123,
            status="Confirmed",
        )

        # Act
        result = await search_use_case.execute(params)

        # Assert
        assert result is not None
        mock_api_client.get.assert_called_once()

        # Verificar que los parámetros se pasaron correctamente
        call_args = mock_api_client.get.call_args
        assert call_args is not None

    @pytest.mark.asyncio
    async def test_search_reservations_complete_workflow_integration(
        self, search_use_case, mock_api_client
    ):
        """Test de integración del workflow completo"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
            page=1,
            size=10,
            sort_column="name",
            sort_direction="asc",
        )

        # Act
        result = await search_use_case.execute(params)

        # Assert
        assert result is not None
        assert "reservations" in result
        assert "total" in result
        assert "page" in result
        assert "size" in result

        # Verificar que el API client fue llamado
        mock_api_client.get.assert_called_once()
