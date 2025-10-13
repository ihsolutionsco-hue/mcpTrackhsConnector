"""
Tests unitarios para SearchUnitsUseCase
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.application.use_cases.search_units import SearchUnitsUseCase
from src.trackhs_mcp.domain.entities.units import SearchUnitsParams
from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


class TestSearchUnitsUseCase:
    """Tests para SearchUnitsUseCase"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del caso de uso"""
        return SearchUnitsUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_execute_basic_search(self, use_case, mock_api_client):
        """Test de búsqueda básica"""
        # Arrange
        params = SearchUnitsParams(page=0, size=25)
        expected_response = {
            "_embedded": {"units": []},
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units", params={"page": 0, "size": 25}
        )

    @pytest.mark.asyncio
    async def test_execute_with_filters(self, use_case, mock_api_client):
        """Test de búsqueda con filtros"""
        # Arrange
        params = SearchUnitsParams(
            page=0,
            size=10,
            bedrooms=2,
            bathrooms=2,
            pets_friendly=1,
            is_active=1,
            node_id=1,
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
                "page": 0,
                "size": 10,
                "nodeId": 1,
                "bedrooms": 2,
                "bathrooms": 2,
                "petsFriendly": 1,
                "isActive": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_execute_with_date_filters(self, use_case, mock_api_client):
        """Test de búsqueda con filtros de fecha"""
        # Arrange
        params = SearchUnitsParams(
            arrival="2024-01-01",
            departure="2024-01-07",
            content_updated_since="2024-01-01T00:00:00Z",
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
                "arrival": "2024-01-01",
                "departure": "2024-01-07",
                "contentUpdatedSince": "2024-01-01T00:00:00Z",
            },
        )

    @pytest.mark.asyncio
    async def test_execute_with_multiple_ids(self, use_case, mock_api_client):
        """Test de búsqueda con múltiples IDs"""
        # Arrange
        params = SearchUnitsParams(
            node_id=[1, 2, 3], amenity_id=[4, 5, 6], unit_type_id=7
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
                "nodeId": [1, 2, 3],
                "amenityId": [4, 5, 6],
                "unitTypeId": 7,
            },
        )

    def test_validate_params_page_negative(self, use_case):
        """Test de validación de página negativa"""
        # Arrange & Act & Assert
        # Pydantic valida automáticamente, no necesitamos validación personalizada
        with pytest.raises(Exception):  # Pydantic validation error
            SearchUnitsParams(page=-1)

    def test_validate_params_size_invalid(self, use_case):
        """Test de validación de tamaño inválido"""
        # Arrange & Act & Assert
        # Pydantic valida automáticamente, no necesitamos validación personalizada
        with pytest.raises(Exception):  # Pydantic validation error
            SearchUnitsParams(size=0)

        # Test tamaño máximo
        with pytest.raises(Exception):  # Pydantic validation error
            SearchUnitsParams(size=1001)

    def test_validate_params_total_results_limit(self, use_case):
        """Test de validación de límite total de resultados"""
        # Arrange
        params = SearchUnitsParams(
            page=101, size=100
        )  # 10,100 resultados (excede límite)

        # Act & Assert
        # Esta validación se hace en el caso de uso, no en Pydantic
        with pytest.raises(
            ValidationError, match="Total results \\(page \\* size\\) must be <= 10,000"
        ):
            use_case._validate_params(params)

    def test_validate_params_date_range_invalid(self, use_case):
        """Test de validación de rango de fechas inválido"""
        # Arrange
        params = SearchUnitsParams(
            arrival="2024-01-07",
            departure="2024-01-01",  # Fecha de salida antes de llegada
        )

        # Act & Assert
        with pytest.raises(
            ValidationError, match="arrival debe ser anterior a departure"
        ):
            use_case._validate_params(params)

    def test_validate_params_bedroom_range_invalid(self, use_case):
        """Test de validación de rango de habitaciones inválido"""
        # Arrange
        params = SearchUnitsParams(
            min_bedrooms=3, max_bedrooms=1  # Mínimo mayor que máximo
        )

        # Act & Assert
        with pytest.raises(
            ValidationError, match="min_bedrooms debe ser menor o igual a max_bedrooms"
        ):
            use_case._validate_params(params)

    def test_validate_params_bathroom_range_invalid(self, use_case):
        """Test de validación de rango de baños inválido"""
        # Arrange
        params = SearchUnitsParams(
            min_bathrooms=3, max_bathrooms=1  # Mínimo mayor que máximo
        )

        # Act & Assert
        with pytest.raises(
            ValidationError,
            match="min_bathrooms debe ser menor o igual a max_bathrooms",
        ):
            use_case._validate_params(params)

    def test_build_request_params_comprehensive(self, use_case):
        """Test de construcción de parámetros comprehensiva"""
        # Arrange
        params = SearchUnitsParams(
            page=1,
            size=50,
            sort_column="name",
            sort_direction="desc",
            search="villa",
            term="luxury",
            unit_code="V001",
            short_name="VIL",
            node_id=[1, 2],
            amenity_id=3,
            unit_type_id=[4, 5],
            id=[6, 7, 8],
            calendar_id=9,
            role_id=10,
            bedrooms=2,
            min_bedrooms=1,
            max_bedrooms=3,
            bathrooms=2,
            min_bathrooms=1,
            max_bathrooms=3,
            pets_friendly=1,
            allow_unit_rates=0,
            computed=1,
            inherited=0,
            limited=1,
            is_bookable=1,
            include_descriptions=0,
            is_active=1,
            arrival="2024-01-01",
            departure="2024-01-07",
            content_updated_since="2024-01-01T00:00:00Z",
            updated_since="2024-01-01",
            unit_status="clean",
        )

        # Act
        result = use_case._build_request_params(params)

        # Assert
        expected = {
            "page": 1,
            "size": 50,
            "sortColumn": "name",
            "sortDirection": "desc",
            "search": "villa",
            "term": "luxury",
            "unitCode": "V001",
            "shortName": "VIL",
            "nodeId": [1, 2],
            "amenityId": 3,
            "unitTypeId": [4, 5],
            "id": [6, 7, 8],
            "calendarId": 9,
            "roleId": 10,
            "bedrooms": 2,
            "minBedrooms": 1,
            "maxBedrooms": 3,
            "bathrooms": 2,
            "minBathrooms": 1,
            "maxBathrooms": 3,
            "petsFriendly": 1,
            "allowUnitRates": 0,
            "computed": 1,
            "inherited": 0,
            "limited": 1,
            "isBookable": 1,
            "includeDescriptions": 0,
            "isActive": 1,
            "arrival": "2024-01-01",
            "departure": "2024-01-07",
            "contentUpdatedSince": "2024-01-01T00:00:00Z",
            "updatedSince": "2024-01-01",
            "unitStatus": "clean",
        }
        assert result == expected

    def test_format_id_list_single_int(self, use_case):
        """Test de formateo de ID único"""
        # Act
        result = use_case._format_id_list(1)

        # Assert
        assert result == 1

    def test_format_id_list_list(self, use_case):
        """Test de formateo de lista de IDs"""
        # Act
        result = use_case._format_id_list([1, 2, 3])

        # Assert
        assert result == [1, 2, 3]

    def test_format_id_list_single_item_list(self, use_case):
        """Test de formateo de lista con un elemento"""
        # Act
        result = use_case._format_id_list([1])

        # Assert
        assert result == 1

    def test_process_response(self, use_case):
        """Test de procesamiento de respuesta"""
        # Arrange
        response = {"_embedded": {"units": []}, "page": 0}

        # Act
        result = use_case._process_response(response)

        # Assert
        assert result == response
