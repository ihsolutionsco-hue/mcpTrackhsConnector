"""
Tests unitarios para la herramienta MCP search_amenities
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
    register_search_amenities,
)


class TestSearchAmenitiesTool:
    """Tests para la herramienta MCP search_amenities"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    def test_register_search_amenities(self, mock_mcp, mock_api_client):
        """Test de registro de la herramienta"""
        # Act
        register_search_amenities(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_amenities_basic_parameters(self, mock_mcp, mock_api_client):
        """Test de parámetros básicos"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Mock response
        mock_response = {
            "_embedded": {
                "amenities": [
                    {
                        "id": 1,
                        "name": "Air Conditioning",
                        "groupId": 1,
                        "groupName": "Additional Amenities",
                        "homeawayType": "AMENITIES_AIR_CONDITIONING",
                        "airbnbType": "ac",
                        "tripadvisorType": "AIR_CONDITIONING",
                        "updatedAt": "2020-08-25T12:41:07-04:00",
                        "_links": {
                            "self": {
                                "href": "https://api.example.com/api/pms/units/amenities/1/"
                            },
                            "group": {
                                "href": "https://api.example.com/api/pms/units/amenity-groups/1/"
                            },
                        },
                    }
                ]
            },
            "page": 1,
            "page_count": 8,
            "page_size": 25,
            "total_items": 185,
            "_links": {
                "self": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=1"
                },
                "first": {"href": "https://api.example.com/api/pms/units/amenities/"},
                "last": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=8"
                },
            },
        }
        mock_api_client.get.return_value = mock_response

        # Act
        result = await registered_function(page=1, size=25)

        # Assert
        assert result == mock_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_amenities_with_filters(self, mock_mcp, mock_api_client):
        """Test con filtros específicos"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        mock_response = {
            "_embedded": {"amenities": []},
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
            "_links": {},
        }
        mock_api_client.get.return_value = mock_response

        # Act
        result = await registered_function(
            page=1,
            size=50,
            group_id=1,
            is_public=1,
            public_searchable=1,
            is_filterable=1,
        )

        # Assert
        assert result == mock_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_amenities_with_sorting(self, mock_mcp, mock_api_client):
        """Test con ordenamiento"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        mock_response = {
            "_embedded": {"amenities": []},
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
            "_links": {},
        }
        mock_api_client.get.return_value = mock_response

        # Act
        result = await registered_function(
            sort_column="id",
            sort_direction="desc",
            search="pool",
        )

        # Assert
        assert result == mock_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_page(self, mock_mcp, mock_api_client):
        """Test con página inválida"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert - Usar un valor que falle en la validación de Pydantic
        with pytest.raises(ValidationError, match="API request failed"):
            await registered_function(page=-1)

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_size(self, mock_mcp, mock_api_client):
        """Test con tamaño inválido"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(ValidationError, match="API request failed"):
            await registered_function(size=1001)

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_sort_column(
        self, mock_mcp, mock_api_client
    ):
        """Test con columna de ordenamiento inválida"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(ValidationError, match="API request failed"):
            await registered_function(sort_column="invalid_column")

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_sort_direction(
        self, mock_mcp, mock_api_client
    ):
        """Test con dirección de ordenamiento inválida"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(ValidationError, match="API request failed"):
            await registered_function(sort_direction="invalid")

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_boolean_params(
        self, mock_mcp, mock_api_client
    ):
        """Test con parámetros booleanos inválidos"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(ValidationError, match="is_public must be 0 or 1"):
            await registered_function(is_public=2)

    @pytest.mark.asyncio
    async def test_search_amenities_invalid_group_id(self, mock_mcp, mock_api_client):
        """Test con group_id inválido"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(
            ValidationError, match="group_id debe ser un entero positivo"
        ):
            await registered_function(group_id=0)

    @pytest.mark.asyncio
    async def test_search_amenities_pagination_limit_exceeded(
        self, mock_mcp, mock_api_client
    ):
        """Test con límite de paginación excedido"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Act & Assert
        with pytest.raises(
            ValidationError, match="Total results \\(page \\* size\\) must be <= 10,000"
        ):
            await registered_function(page=500, size=25)  # 500 * 25 = 12500 > 10000

    @pytest.mark.asyncio
    async def test_search_amenities_api_error_401(self, mock_mcp, mock_api_client):
        """Test con error 401 de la API"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Mock API error
        error = Exception("Unauthorized")
        error.status_code = 401
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(
            ValidationError, match="Unauthorized: Invalid authentication credentials"
        ):
            await registered_function()

    @pytest.mark.asyncio
    async def test_search_amenities_api_error_403(self, mock_mcp, mock_api_client):
        """Test con error 403 de la API"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Mock API error
        error = Exception("Forbidden")
        error.status_code = 403
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(
            ValidationError, match="Forbidden: Insufficient permissions"
        ):
            await registered_function()

    @pytest.mark.asyncio
    async def test_search_amenities_api_error_500(self, mock_mcp, mock_api_client):
        """Test con error 500 de la API"""
        # Arrange
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_search_amenities(mock_mcp, mock_api_client)

        # Mock API error
        error = Exception("Internal Server Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(
            ValidationError, match="Internal Server Error: API temporarily unavailable"
        ):
            await registered_function()
