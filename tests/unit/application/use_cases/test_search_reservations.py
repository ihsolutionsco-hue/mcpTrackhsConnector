"""
Tests unitarios para SearchReservationsUseCase
Implementando el patrón oficial de FastMCP para testing
"""

from typing import Any, Dict
from unittest.mock import AsyncMock, Mock

import pytest

from trackhs_mcp.application.use_cases.search_reservations import (
    SearchReservationsUseCase,
)
from trackhs_mcp.domain.entities.reservations import SearchReservationsParams
from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


class TestSearchReservationsUseCase:
    """Tests para SearchReservationsUseCase"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = AsyncMock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del use case con mock"""
        return SearchReservationsUseCase(mock_api_client)

    @pytest.fixture
    def sample_params(self):
        """Parámetros de ejemplo para testing"""
        return SearchReservationsParams(
            page=1,
            size=10,
            search="test search",
            sort_column="name",
            sort_direction="asc",
        )

    @pytest.fixture
    def sample_api_response(self):
        """Respuesta de ejemplo de la API"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "status": "Confirmed",
                        "arrivalDate": "2024-01-15",
                        "departureDate": "2024-01-20",
                        "nights": 5,
                        "currency": "USD",
                        "contact": {
                            "id": 1,
                            "firstName": "John",
                            "lastName": "Doe",
                            "primaryEmail": "john@example.com",
                        },
                        "unit": {"id": 1, "name": "Test Unit", "unitCode": "TU001"},
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {
                "self": {"href": "/api/v2/pms/reservations?page=1"},
                "first": {"href": "/api/v2/pms/reservations?page=1"},
                "last": {"href": "/api/v2/pms/reservations?page=1"},
            },
        }

    @pytest.mark.asyncio
    async def test_execute_success(
        self, use_case, sample_params, sample_api_response, mock_api_client
    ):
        """Test ejecución exitosa del use case"""
        # Arrange
        mock_api_client.get.return_value = sample_api_response

        # Act
        result = await use_case.execute(sample_params)

        # Assert
        assert result == sample_api_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 1,
                "size": 10,
                "search": "test search",
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_execute_with_date_filters(
        self, use_case, mock_api_client, sample_api_response
    ):
        """Test ejecución con filtros de fecha"""
        # Arrange
        params = SearchReservationsParams(
            page=None,  # No incluir parámetros por defecto
            size=None,
            sort_column=None,
            sort_direction=None,
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
        )
        mock_api_client.get.return_value = sample_api_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == sample_api_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "arrivalStart": "2024-01-01",
                "arrivalEnd": "2024-01-31",
                "bookedStart": "2024-01-01",
                "bookedEnd": "2024-01-31",
            },
        )

    @pytest.mark.asyncio
    async def test_execute_with_id_filters(
        self, use_case, mock_api_client, sample_api_response
    ):
        """Test ejecución con filtros de ID"""
        # Arrange
        params = SearchReservationsParams(
            page=None,  # No incluir parámetros por defecto
            size=None,
            sort_column=None,
            sort_direction=None,
            node_id=[1, 2, 3],
            unit_id=123,
            contact_id=[456, 789],
            status=["Confirmed", "Pending"],
        )
        mock_api_client.get.return_value = sample_api_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == sample_api_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "nodeId": "1,2,3",
                "unitId": "123",
                "contactId": "456,789",
                "status": "Confirmed,Pending",
            },
        )

    @pytest.mark.asyncio
    async def test_execute_with_special_params(
        self, use_case, mock_api_client, sample_api_response
    ):
        """Test ejecución con parámetros especiales"""
        # Arrange
        params = SearchReservationsParams(
            page=None,  # No incluir parámetros por defecto
            size=None,
            sort_column=None,
            sort_direction=None,
            scroll=True,
            in_house_today=1,
            group_id=123,  # Cambiar a entero
            checkin_office_id=456,
        )
        mock_api_client.get.return_value = sample_api_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == sample_api_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "scroll": True,
                "inHouseToday": 1,
                "groupId": 123,
                "checkinOfficeId": 456,
            },
        )

    def test_validate_params_valid_values(self, use_case):
        """Test validación de parámetros - valores válidos"""
        # Arrange
        params = SearchReservationsParams(page=1, size=10)

        # Act & Assert - No debe lanzar excepción
        use_case._validate_params(params)  # No debe lanzar excepción

    def test_validate_params_valid_date_range(self, use_case):
        """Test validación de parámetros - rango de fechas válido"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-01", arrival_end="2024-01-31"
        )

        # Act & Assert - No debe lanzar excepción
        use_case._validate_params(params)  # No debe lanzar excepción

    def test_validate_params_invalid_size_too_large(self, use_case):
        """Test validación de parámetros - tamaño demasiado grande"""
        # Arrange
        params = SearchReservationsParams(size=101)

        # Act & Assert
        with pytest.raises(ValidationError, match="Size debe estar entre 1 y 100"):
            use_case._validate_params(params)

    def test_validate_params_invalid_date_range(self, use_case):
        """Test validación de parámetros - rango de fechas inválido"""
        # Arrange
        params = SearchReservationsParams(
            arrival_start="2024-01-31",
            arrival_end="2024-01-01",  # Fecha de fin anterior a inicio
        )

        # Act & Assert
        with pytest.raises(
            ValidationError, match="arrival_start debe ser anterior a arrival_end"
        ):
            use_case._validate_params(params)

    def test_format_id_list_single_id(self, use_case):
        """Test formateo de lista de IDs - ID único"""
        # Act
        result = use_case._format_id_list(123)

        # Assert
        assert result == "123"

    def test_format_id_list_multiple_ids(self, use_case):
        """Test formateo de lista de IDs - múltiples IDs"""
        # Act
        result = use_case._format_id_list([1, 2, 3])

        # Assert
        assert result == "1,2,3"

    def test_format_status_list_single_status(self, use_case):
        """Test formateo de lista de estados - estado único"""
        # Act
        result = use_case._format_status_list("Confirmed")

        # Assert
        assert result == "Confirmed"

    def test_format_status_list_multiple_statuses(self, use_case):
        """Test formateo de lista de estados - múltiples estados"""
        # Act
        result = use_case._format_status_list(["Confirmed", "Pending", "Cancelled"])

        # Assert
        assert result == "Confirmed,Pending,Cancelled"

    def test_build_request_params_minimal(self, use_case):
        """Test construcción de parámetros de petición - mínimos"""
        # Arrange
        params = SearchReservationsParams(
            page=None, size=None, sort_column=None, sort_direction=None
        )

        # Act
        result = use_case._build_request_params(params)

        # Assert
        assert result == {}

    def test_build_request_params_comprehensive(self, use_case):
        """Test construcción de parámetros de petición - completos"""
        # Arrange
        params = SearchReservationsParams(
            page=2,
            size=25,
            search="test",
            sort_column="name",
            sort_direction="desc",
            node_id=[1, 2],
            unit_id=123,
            contact_id=456,
            status=["Confirmed", "Pending"],
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
            travel_agent_id=789,
            campaign_id=101,
            user_id=202,
            unit_type_id=303,
            rate_type_id=404,
            reservation_type_id=505,
            scroll=True,
            in_house_today=1,
            group_id=123,  # Cambiar a entero
            checkin_office_id=606,
            updated_since="2024-01-01T00:00:00Z",
            tags="tag1,tag2",
        )

        # Act
        result = use_case._build_request_params(params)

        # Assert
        expected = {
            "page": 2,
            "size": 25,
            "search": "test",
            "sortColumn": "name",
            "sortDirection": "desc",
            "nodeId": "1,2",
            "unitId": "123",
            "contactId": "456",
            "status": "Confirmed,Pending",
            "arrivalStart": "2024-01-01",
            "arrivalEnd": "2024-01-31",
            "bookedStart": "2024-01-01",
            "bookedEnd": "2024-01-31",
            "travelAgentId": "789",
            "campaignId": "101",
            "userId": "202",
            "unitTypeId": "303",
            "rateTypeId": "404",
            "reservationTypeId": "505",
            "scroll": True,
            "inHouseToday": 1,
            "groupId": 123,
            "checkinOfficeId": 606,
            "updatedSince": "2024-01-01T00:00:00Z",
            "tags": "tag1,tag2",
        }
        assert result == expected

    def test_process_response(self, use_case, sample_api_response):
        """Test procesamiento de respuesta"""
        # Act
        result = use_case._process_response(sample_api_response)

        # Assert
        assert result == sample_api_response

    @pytest.mark.asyncio
    async def test_execute_api_error(self, use_case, sample_params, mock_api_client):
        """Test manejo de error de API"""
        # Arrange
        mock_api_client.get.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await use_case.execute(sample_params)

    @pytest.mark.asyncio
    async def test_execute_success_with_validation(
        self, use_case, mock_api_client, sample_api_response
    ):
        """Test ejecución exitosa con validación"""
        # Arrange
        params = SearchReservationsParams(page=1, size=10)
        mock_api_client.get.return_value = sample_api_response

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result == sample_api_response
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )
