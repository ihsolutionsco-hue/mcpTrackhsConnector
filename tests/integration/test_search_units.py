"""
Tests de integración para search_units
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.application.use_cases.search_units import SearchUnitsUseCase
from src.trackhs_mcp.domain.entities.units import SearchUnitsParams
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestSearchUnitsIntegration:
    """Tests de integración para search_units"""

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
        return SearchUnitsUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_search_units_basic_integration(self, use_case, mock_api_client):
        """Test de integración básica"""
        # Arrange
        params = SearchUnitsParams(page=0, size=3)
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 1,
                        "name": "Test Unit",
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "petsFriendly": True,
                        "isActive": True,
                    }
                ]
            },
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {
                "self": {"href": "https://api.example.com/api/pms/units/?page=0"},
                "first": {"href": "https://api.example.com/api/pms/units/"},
                "last": {"href": "https://api.example.com/api/pms/units/?page=0"},
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 0,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_with_complex_filters(self, use_case, mock_api_client):
        """Test de integración con filtros complejos"""
        # Arrange
        params = SearchUnitsParams(
            page=1,
            size=3,
            sort_column="name",
            sort_direction="desc",
            search="villa",
            node_id=[1, 2, 3],
            amenity_id=[4, 5],
            bedrooms=2,
            min_bedrooms=1,
            max_bedrooms=3,
            pets_friendly=1,
            is_active=1,
            arrival="2024-01-01",
            departure="2024-01-07",
            unit_status="clean",
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 50,
                "sortColumn": "name",
                "sortDirection": "desc",
                "search": "villa",
                "nodeId": [1, 2, 3],
                "amenityId": [4, 5],
                "bedrooms": 2,
                "minBedrooms": 1,
                "maxBedrooms": 3,
                "petsFriendly": 1,
                "isActive": 1,
                "arrival": "2024-01-01",
                "departure": "2024-01-07",
                "unitStatus": "clean",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_boolean_filters(self, use_case, mock_api_client):
        """Test de integración con filtros booleanos"""
        # Arrange
        params = SearchUnitsParams(
            pets_friendly=1,
            events_allowed=0,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
            is_bookable=1,
            is_active=1,
            computed=1,
            inherited=0,
            limited=0,
            include_descriptions=1,
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "petsFriendly": 1,
                "eventsAllowed": 0,
                "smokingAllowed": 0,
                "childrenAllowed": 1,
                "isAccessible": 1,
                "isBookable": 1,
                "isActive": 1,
                "computed": 1,
                "inherited": 0,
                "limited": 0,
                "includeDescriptions": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_date_filters(self, use_case, mock_api_client):
        """Test de integración con filtros de fecha"""
        # Arrange
        params = SearchUnitsParams(
            arrival="2024-01-01",
            departure="2024-01-07",
            content_updated_since="2024-01-01T00:00:00Z",
            updated_since="2024-01-01",
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "arrival": "2024-01-01",
                "departure": "2024-01-07",
                "contentUpdatedSince": "2024-01-01T00:00:00Z",
                "updatedSince": "2024-01-01",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_room_bathroom_filters(self, use_case, mock_api_client):
        """Test de integración con filtros de habitaciones y baños"""
        # Arrange
        params = SearchUnitsParams(
            bedrooms=2,
            min_bedrooms=1,
            max_bedrooms=3,
            bathrooms=2,
            min_bathrooms=1,
            max_bathrooms=3,
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "bedrooms": 2,
                "minBedrooms": 1,
                "maxBedrooms": 3,
                "bathrooms": 2,
                "minBathrooms": 1,
                "maxBathrooms": 3,
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_search_filters(self, use_case, mock_api_client):
        """Test de integración con filtros de búsqueda"""
        # Arrange
        params = SearchUnitsParams(
            search="luxury villa", term="ocean view", unit_code="V001", short_name="VIL"
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "search": "luxury villa",
                "term": "ocean view",
                "unitCode": "V001",
                "shortName": "VIL",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_id_filters(self, use_case, mock_api_client):
        """Test de integración con filtros de ID"""
        # Arrange
        params = SearchUnitsParams(
            node_id=[1, 2, 3],
            amenity_id=4,
            unit_type_id=[5, 6],
            id=[7, 8, 9],
            calendar_id=10,
            role_id=11,
        )
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "nodeId": [1, 2, 3],
                "amenityId": 4,
                "unitTypeId": [5, 6],
                "id": [7, 8, 9],
                "calendarId": 10,
                "roleId": 11,
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_status_filters(self, use_case, mock_api_client):
        """Test de integración con filtros de estado"""
        # Arrange
        params = SearchUnitsParams(is_active=1, is_bookable=1, unit_status="clean")
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "isActive": 1,
                "isBookable": 1,
                "unitStatus": "clean",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_pagination(self, use_case, mock_api_client):
        """Test de integración con paginación"""
        # Arrange
        params = SearchUnitsParams(page=2, size=5)
        expected_response = {
            "_embedded": {"units": []},
            "page": 2,
            "page_count": 10,
            "page_size": 5,
            "total_items": 1000,
            "_links": {
                "self": {"href": "https://api.example.com/api/pms/units/?page=2"},
                "first": {"href": "https://api.example.com/api/pms/units/"},
                "last": {"href": "https://api.example.com/api/pms/units/?page=9"},
                "next": {"href": "https://api.example.com/api/pms/units/?page=3"},
                "prev": {"href": "https://api.example.com/api/pms/units/?page=1"},
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 2,
                "size": 100,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_search_units_sorting(self, use_case, mock_api_client):
        """Test de integración con ordenamiento"""
        # Arrange
        params = SearchUnitsParams(sort_column="name", sort_direction="desc")
        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "desc",
            },
        )
