"""
Tests E2E para search_amenities siguiendo mejores prácticas arquitecturales.

Estos tests se enfocan en:
1. Comportamiento del usuario, no implementación interna
2. Contratos de la API, no parámetros específicos
3. Robustez ante cambios en la implementación
4. Separación clara de responsabilidades
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
    register_search_amenities,
)


class TestSearchAmenitiesE2E:
    """Tests E2E para search_amenities con mejores prácticas"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API con respuesta estándar"""
        client = AsyncMock()
        client.get.return_value = {
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
                "next": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=2"
                },
            },
        }
        return client

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
    async def test_basic_search_returns_expected_structure(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda básica retorna estructura esperada"""
        # Act
        result = await setup_tool()

        # Assert - Verificar comportamiento, no implementación
        assert result is not None
        assert "_embedded" in result
        assert "amenities" in result["_embedded"]
        assert isinstance(result["_embedded"]["amenities"], list)

        # Verificar que se llamó a la API (comportamiento, no parámetros específicos)
        mock_api_client.get.assert_called_once()
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/pms/units/amenities"  # Endpoint correcto
        assert "params" in call_args[1]  # Se pasaron parámetros

    @pytest.mark.asyncio
    async def test_search_with_filters_works_correctly(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda con filtros funciona correctamente"""
        # Act
        result = await setup_tool(
            group_id=1, is_public=1, public_searchable=1, is_filterable=1
        )

        # Assert - Verificar comportamiento
        assert result is not None
        assert "_embedded" in result

        # Verificar que se llamó a la API con filtros
        mock_api_client.get.assert_called_once()
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]

        # Verificar que los filtros se pasaron correctamente
        assert params["groupId"] == 1
        assert params["isPublic"] == 1
        assert params["publicSearchable"] == 1
        assert params["isFilterable"] == 1

    @pytest.mark.asyncio
    async def test_search_with_sorting(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con ordenamiento"""
        # Act
        result = await setup_tool(
            sort_column="id", sort_direction="desc", search="pool"
        )

        # Assert
        assert result is not None

        # Verificar parámetros de ordenamiento
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["sortColumn"] == "id"
        assert params["sortDirection"] == "desc"
        assert params["search"] == "pool"

    @pytest.mark.asyncio
    async def test_search_with_pagination(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con paginación"""
        # Act
        result = await setup_tool(page=2, size=50)

        # Assert
        assert result is not None

        # Verificar parámetros de paginación
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["page"] == 2
        assert params["size"] == 50

    @pytest.mark.asyncio
    async def test_search_handles_empty_results(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda maneja resultados vacíos"""
        # Arrange - Mock empty response
        mock_api_client.get.return_value = {
            "_embedded": {"amenities": []},
            "page": 1,
            "page_count": 0,
            "page_size": 25,
            "total_items": 0,
            "_links": {
                "self": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=1"
                },
                "first": {"href": "https://api.example.com/api/pms/units/amenities/"},
                "last": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=1"
                },
            },
        }

        # Act
        result = await setup_tool(search="nonexistent")

        # Assert
        assert result is not None
        assert "_embedded" in result
        assert result["_embedded"]["amenities"] == []
        assert result["total_items"] == 0

    @pytest.mark.asyncio
    async def test_search_handles_api_errors(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda maneja errores de la API"""
        # Arrange - Mock API error
        error = Exception("Unauthorized")
        error.status_code = 401
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(
            Exception, match="Unauthorized: Invalid authentication credentials"
        ):
            await setup_tool()

    @pytest.mark.asyncio
    async def test_search_handles_validation_errors(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda maneja errores de validación"""
        # Act & Assert
        with pytest.raises(Exception, match="Page debe ser mayor o igual a 1"):
            await setup_tool(page=0)

    @pytest.mark.asyncio
    async def test_search_handles_invalid_boolean_params(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda maneja parámetros booleanos inválidos"""
        # Act & Assert
        with pytest.raises(Exception, match="is_public must be 0 or 1"):
            await setup_tool(is_public=2)

    @pytest.mark.asyncio
    async def test_search_handles_invalid_sort_column(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda maneja columna de ordenamiento inválida"""
        # Act & Assert
        with pytest.raises(Exception, match="API request failed"):
            await setup_tool(sort_column="invalid_column")

    @pytest.mark.asyncio
    async def test_search_handles_pagination_limit(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda maneja límite de paginación"""
        # Act & Assert
        with pytest.raises(
            Exception, match="Total results \\(page \\* size\\) must be <= 10,000"
        ):
            await setup_tool(page=500, size=25)  # 500 * 25 = 12500 > 10000

    @pytest.mark.asyncio
    async def test_search_with_all_parameters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con todos los parámetros"""
        # Act
        result = await setup_tool(
            page=2,
            size=50,
            sort_column="isPublic",
            sort_direction="desc",
            search="pool",
            group_id=1,
            is_public=1,
            public_searchable=1,
            is_filterable=1,
        )

        # Assert
        assert result is not None

        # Verificar que todos los parámetros se pasaron correctamente
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]

        assert params["page"] == 2
        assert params["size"] == 50
        assert params["sortColumn"] == "isPublic"
        assert params["sortDirection"] == "desc"
        assert params["search"] == "pool"
        assert params["groupId"] == 1
        assert params["isPublic"] == 1
        assert params["publicSearchable"] == 1
        assert params["isFilterable"] == 1

    @pytest.mark.asyncio
    async def test_search_response_structure_validation(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Validación de estructura de respuesta"""
        # Act
        result = await setup_tool()

        # Assert - Verificar estructura completa de respuesta
        assert "_embedded" in result
        assert "amenities" in result["_embedded"]
        assert "page" in result
        assert "page_count" in result
        assert "page_size" in result
        assert "total_items" in result
        assert "_links" in result

        # Verificar estructura de amenidad individual
        if result["_embedded"]["amenities"]:
            amenity = result["_embedded"]["amenities"][0]
            assert "id" in amenity
            assert "name" in amenity
            assert "groupId" in amenity
            assert "groupName" in amenity
            assert "updatedAt" in amenity
            assert "_links" in amenity

    @pytest.mark.asyncio
    async def test_search_parameter_normalization(self, setup_tool, mock_api_client):
        """Test E2E: Normalización de parámetros"""
        # Act - Usar tipos mixtos para probar normalización
        result = await setup_tool(
            page="2",  # String que debe convertirse a int
            size=50.0,  # Float que debe convertirse a int
            group_id="1",  # String que debe convertirse a int
            is_public="1",  # String que debe convertirse a 0/1
            public_searchable=1.0,  # Float que debe convertirse a 0/1
            is_filterable="0",  # String que debe convertirse a 0/1
        )

        # Assert
        assert result is not None

        # Verificar que los parámetros se normalizaron correctamente
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]

        assert params["page"] == 2
        assert params["size"] == 50
        assert params["groupId"] == 1
        assert params["isPublic"] == 1
        assert params["publicSearchable"] == 1
        assert params["isFilterable"] == 0
