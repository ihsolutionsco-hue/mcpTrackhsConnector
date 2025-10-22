"""
Tests críticos para la herramienta MCP search_amenities
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
    register_search_amenities,
)


class TestSearchAmenitiesCritical:
    """Tests críticos para funcionalidad esencial de search_amenities"""

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
        register_search_amenities(mock_mcp, mock_api_client)

        # Obtener la función registrada
        return registered_function

    @pytest.mark.asyncio
    async def test_search_amenities_basic_success(
        self, setup_tool, mock_api_client, sample_amenity_data
    ):
        """Test: Búsqueda básica de amenidades exitosa"""
        # Arrange
        expected_response = {
            "_embedded": {"amenities": [sample_amenity_data]},
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {
                "self": {
                    "href": "https://api-test.trackhs.com/api/pms/amenities?page=0"
                },
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=0, size=25)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/amenities",
            params={
                "page": 0,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_with_filters(
        self, setup_tool, mock_api_client, sample_amenity_data
    ):
        """Test: Búsqueda con filtros específicos"""
        # Arrange
        expected_response = {
            "_embedded": {"amenities": [sample_amenity_data]},
            "page": 0,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(
            page=0, size=10, search="wifi", category="Internet", is_active=1
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/amenities",
            params={
                "page": 0,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "search": "wifi",
                "category": "Internet",
                "isActive": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_pagination(self, setup_tool, mock_api_client):
        """Test: Paginación funciona correctamente"""
        # Arrange
        expected_response = {
            "_embedded": {"amenities": []},
            "page": 1,
            "page_count": 2,
            "page_size": 25,
            "total_items": 30,
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=1, size=25)

        # Assert
        assert result["page"] == 1
        assert result["page_count"] == 2
        assert result["total_items"] == 30
        mock_api_client.get.assert_called_once_with(
            "/pms/amenities",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_api_error_handling(
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
    async def test_search_amenities_empty_results(self, setup_tool, mock_api_client):
        """Test: Resultados vacíos manejados correctamente"""
        # Arrange
        expected_response = {
            "_embedded": {"amenities": []},
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
        assert len(result["_embedded"]["amenities"]) == 0
        assert result["page_count"] == 0
