"""
Tests de integración para search_amenities
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.application.use_cases.search_amenities import (
    SearchAmenitiesUseCase,
)
from src.trackhs_mcp.domain.entities.amenities import SearchAmenitiesParams
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestSearchAmenitiesIntegration:
    """Tests de integración para search_amenities"""

    @pytest.fixture
    def mock_config(self):
        """Mock de configuración"""
        return TrackHSConfig(
            base_url="https://api.example.com",
            username="test_user",
            password="test_pass",
            timeout=30,
        )

    @pytest.fixture
    def mock_api_client(self, mock_config):
        """Mock del cliente API con configuración"""
        client = MagicMock(spec=TrackHSApiClient)
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del caso de uso"""
        return SearchAmenitiesUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_search_amenities_basic_integration(self, use_case, mock_api_client):
        """Test de integración básica"""
        # Arrange
        params = SearchAmenitiesParams(page=1, size=25)
        expected_response = {
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
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "order",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_with_complex_filters(
        self, use_case, mock_api_client
    ):
        """Test de integración con filtros complejos"""
        # Arrange
        params = SearchAmenitiesParams(
            page=2,
            size=50,
            sort_column="id",
            sort_direction="desc",
            search="pool",
            group_id=1,
            is_public=1,
            public_searchable=1,
            is_filterable=1,
        )
        expected_response = {
            "_embedded": {
                "amenities": [
                    {
                        "id": 4,
                        "name": "Pool",
                        "groupId": 2,
                        "groupName": "Pool",
                        "homeawayType": "POOL_SPA_PRIVATE_POOL",
                        "airbnbType": "pool",
                        "tripadvisorType": "UNHEATED_OUTDOOR_POOL_PRIVATE",
                        "updatedAt": "2020-05-12T10:27:41-04:00",
                        "_links": {
                            "self": {
                                "href": "https://api.example.com/api/pms/units/amenities/4/"
                            },
                            "group": {
                                "href": "https://api.example.com/api/pms/units/amenity-groups/2/"
                            },
                        },
                    }
                ]
            },
            "page": 2,
            "page_count": 4,
            "page_size": 50,
            "total_items": 150,
            "_links": {
                "self": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=2"
                },
                "first": {"href": "https://api.example.com/api/pms/units/amenities/"},
                "last": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=4"
                },
                "prev": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=1"
                },
                "next": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=3"
                },
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 2,
                "size": 50,
                "sortColumn": "id",
                "sortDirection": "desc",
                "search": "pool",
                "groupId": 1,
                "isPublic": 1,
                "publicSearchable": 1,
                "isFilterable": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_pagination(self, use_case, mock_api_client):
        """Test de integración con paginación"""
        # Arrange
        params = SearchAmenitiesParams(page=3, size=10)
        expected_response = {
            "_embedded": {
                "amenities": [
                    {
                        "id": 21,
                        "name": "Test Amenity",
                        "groupId": 1,
                        "groupName": "Test Group",
                        "homeawayType": None,
                        "airbnbType": None,
                        "tripadvisorType": None,
                        "updatedAt": "2020-01-01T00:00:00-00:00",
                        "_links": {
                            "self": {
                                "href": "https://api.example.com/api/pms/units/amenities/21/"
                            },
                            "group": {
                                "href": "https://api.example.com/api/pms/units/amenity-groups/1/"
                            },
                        },
                    }
                ]
            },
            "page": 3,
            "page_count": 10,
            "page_size": 10,
            "total_items": 95,
            "_links": {
                "self": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=3"
                },
                "first": {"href": "https://api.example.com/api/pms/units/amenities/"},
                "last": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=10"
                },
                "prev": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=2"
                },
                "next": {
                    "href": "https://api.example.com/api/pms/units/amenities/?page=4"
                },
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 3,
                "size": 10,
                "sortColumn": "order",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_sorting(self, use_case, mock_api_client):
        """Test de integración con ordenamiento"""
        # Arrange
        params = SearchAmenitiesParams(
            sort_column="isPublic",
            sort_direction="desc",
            is_public=1,
        )
        expected_response = {
            "_embedded": {
                "amenities": [
                    {
                        "id": 1,
                        "name": "Public Amenity 1",
                        "groupId": 1,
                        "groupName": "Public Group",
                        "homeawayType": "PUBLIC_TYPE",
                        "airbnbType": "public",
                        "tripadvisorType": "PUBLIC",
                        "updatedAt": "2020-01-01T00:00:00-00:00",
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
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
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
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "isPublic",
                "sortDirection": "desc",
                "isPublic": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_empty_result(self, use_case, mock_api_client):
        """Test de integración con resultado vacío"""
        # Arrange
        params = SearchAmenitiesParams(search="nonexistent")
        expected_response = {
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
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 1,
                "size": 10,
                "search": "nonexistent",
                "sortColumn": "order",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_amenities_api_error_handling(self, use_case, mock_api_client):
        """Test de manejo de errores de la API"""
        # Arrange
        params = SearchAmenitiesParams()

        # Mock API error
        error = Exception("API Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await use_case.execute(params)

    @pytest.mark.asyncio
    async def test_search_amenities_validation_error(self, use_case, mock_api_client):
        """Test de manejo de errores de validación"""
        # Arrange
        params = SearchAmenitiesParams(page=0)  # Invalid page

        # Act & Assert
        with pytest.raises(Exception, match="Page debe ser mayor o igual a 1"):
            await use_case.execute(params)

    @pytest.mark.asyncio
    async def test_search_amenities_json_response_processing(
        self, use_case, mock_api_client
    ):
        """Test de procesamiento de respuesta JSON string"""
        # Arrange
        import json

        params = SearchAmenitiesParams()
        response_data = {
            "_embedded": {"amenities": []},
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
            "_links": {},
        }
        json_response = json.dumps(response_data)
        mock_api_client.get.return_value = json_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == response_data
        mock_api_client.get.assert_called_once_with(
            "/pms/units/amenities",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "order",
                "sortDirection": "asc",
            },
        )
