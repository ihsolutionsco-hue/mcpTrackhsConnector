"""
Tests críticos para la herramienta MCP search_reservations
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
)


class TestSearchReservationsCritical:
    """Tests críticos para funcionalidad esencial de search_reservations"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.fixture
    def setup_tool(self, mock_mcp, mock_api_client):
        """Configuración de la herramienta"""
        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        # Registrar la función
        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        return registered_function

    @pytest.mark.asyncio
    async def test_search_reservations_basic_success(
        self, setup_tool, mock_api_client, sample_reservation_data
    ):
        """Test: Búsqueda básica de reservas exitosa"""
        # Arrange
        expected_response = {
            "_embedded": {"reservations": [sample_reservation_data]},
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {
                "self": {
                    "href": "https://api-test.trackhs.com/api/v2/pms/reservations?page=0"
                },
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=0, size=25)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 0,
                "size": 25,
                "sortColumn": "arrivalDate",
                "sortDirection": "desc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_reservations_with_filters(
        self, setup_tool, mock_api_client, sample_reservation_data
    ):
        """Test: Búsqueda con filtros específicos"""
        # Arrange
        expected_response = {
            "_embedded": {"reservations": [sample_reservation_data]},
            "page": 0,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(
            page=0,
            size=10,
            arrival_date="2024-01-15",
            departure_date="2024-01-20",
            status="Confirmed",
            currency="USD",
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 0,
                "size": 10,
                "sortColumn": "arrivalDate",
                "sortDirection": "desc",
                "arrivalDate": "2024-01-15",
                "departureDate": "2024-01-20",
                "status": "Confirmed",
                "currency": "USD",
            },
        )

    @pytest.mark.asyncio
    async def test_search_reservations_pagination(self, setup_tool, mock_api_client):
        """Test: Paginación funciona correctamente"""
        # Arrange
        expected_response = {
            "_embedded": {"reservations": []},
            "page": 2,
            "page_count": 3,
            "page_size": 25,
            "total_items": 50,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=2, size=25)

        # Assert
        assert result["page"] == 2
        assert result["page_count"] == 3
        assert result["total_items"] == 50
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 2,
                "size": 25,
                "sortColumn": "arrivalDate",
                "sortDirection": "desc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_reservations_invalid_date_format(self, setup_tool):
        """Test: Validación de formato de fecha inválido"""
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            await setup_tool(page=0, size=25, arrival_date="invalid-date-format")

    @pytest.mark.asyncio
    async def test_search_reservations_api_error_handling(
        self, setup_tool, mock_api_client
    ):
        """Test: Manejo de errores de API"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_api_client.get.side_effect = HTTPStatusError(
            "Internal Server Error", request=Mock(), response=mock_response
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError):
            await setup_tool(page=0, size=25)

    @pytest.mark.asyncio
    async def test_search_reservations_empty_results(self, setup_tool, mock_api_client):
        """Test: Resultados vacíos manejados correctamente"""
        # Arrange
        expected_response = {
            "_embedded": {"reservations": []},
            "page": 0,
            "page_count": 0,
            "page_size": 25,
            "total_items": 0,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=0, size=25)

        # Assert
        assert result["total_items"] == 0
        assert len(result["_embedded"]["reservations"]) == 0
        assert result["page_count"] == 0

    @pytest.mark.asyncio
    async def test_search_reservations_sorting_options(
        self, setup_tool, mock_api_client
    ):
        """Test: Opciones de ordenamiento funcionan"""
        # Arrange
        expected_response = {
            "_embedded": {"reservations": []},
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        await setup_tool(
            page=0, size=25, sort_column="departureDate", sort_direction="asc"
        )

        # Assert
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 0,
                "size": 25,
                "sortColumn": "departureDate",
                "sortDirection": "asc",
            },
        )
