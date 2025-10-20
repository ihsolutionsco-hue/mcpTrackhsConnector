"""
Tests unitarios para CreateHousekeepingWorkOrderUseCase.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from trackhs_mcp.application.use_cases.create_housekeeping_work_order import (
    CreateHousekeepingWorkOrderUseCase,
)
from trackhs_mcp.domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrder,
    HousekeepingWorkOrderResponse,
    HousekeepingWorkOrderStatus,
)


class TestCreateHousekeepingWorkOrderUseCase:
    """Tests para CreateHousekeepingWorkOrderUseCase."""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del use case con mock."""
        return CreateHousekeepingWorkOrderUseCase(mock_api_client)

    @pytest.fixture
    def valid_params(self):
        """Parámetros válidos para testing."""
        return CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
        )

    @pytest.fixture
    def api_response(self):
        """Respuesta mock de la API."""
        return {
            "id": 1,
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitId": 123,
            "isInspection": True,
            "timeEstimate": 60.0,
            "createdAt": "2024-01-15T09:00:00Z",
        }

    @pytest.mark.asyncio
    async def test_execute_success(
        self, use_case, mock_api_client, valid_params, api_response
    ):
        """Test ejecución exitosa del use case."""
        # Configurar mock
        mock_api_client.create_housekeeping_work_order.return_value = api_response

        # Ejecutar
        result = await use_case.execute(valid_params)

        # Verificar
        assert result.success is True
        assert result.data is not None
        assert result.data.id == 1
        assert result.data.scheduled_at == "2024-01-15T10:00:00Z"
        assert result.data.status == HousekeepingWorkOrderStatus.PENDING
        assert result.data.unit_id == 123
        assert result.data.is_inspection is True
        assert result.message == "Orden de trabajo de housekeeping creada exitosamente"

        # Verificar que se llamó al API client
        mock_api_client.create_housekeeping_work_order.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_api_error(self, use_case, mock_api_client, valid_params):
        """Test manejo de error de API."""
        # Configurar mock para lanzar excepción
        mock_api_client.create_housekeeping_work_order.side_effect = Exception(
            "API Error"
        )

        # Ejecutar
        result = await use_case.execute(valid_params)

        # Verificar
        assert result.success is False
        assert result.data is None
        assert "Error al crear orden de trabajo" in result.message
        assert "API Error" in result.message

    @pytest.mark.asyncio
    async def test_prepare_request_data_with_unit_id(self, use_case, valid_params):
        """Test preparación de datos con unit_id."""
        request_data = use_case._prepare_request_data(valid_params)

        expected_data = {
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitId": 123,
            "isInspection": True,
        }

        assert request_data == expected_data

    @pytest.mark.asyncio
    async def test_prepare_request_data_with_unit_block_id(self, use_case):
        """Test preparación de datos con unit_block_id."""
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_block_id=456,
            clean_type_id=5,
        )

        request_data = use_case._prepare_request_data(params)

        expected_data = {
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitBlockId": 456,
            "cleanTypeId": 5,
        }

        assert request_data == expected_data

    @pytest.mark.asyncio
    async def test_prepare_request_data_with_all_optional_fields(self, use_case):
        """Test preparación de datos con todos los campos opcionales."""
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
            time_estimate=60.0,
            actual_time=45.0,
            user_id=789,
            vendor_id=101,
            reservation_id=202,
            is_turn=True,
            is_manual=False,
            charge_owner=True,
            comments="Limpieza profunda",
            cost=100.0,
        )

        request_data = use_case._prepare_request_data(params)

        expected_data = {
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitId": 123,
            "isInspection": True,
            "timeEstimate": 60.0,
            "actualTime": 45.0,
            "userId": 789,
            "vendorId": 101,
            "reservationId": 202,
            "isTurn": True,
            "isManual": False,
            "chargeOwner": True,
            "comments": "Limpieza profunda",
            "cost": 100.0,
        }

        assert request_data == expected_data

    @pytest.mark.asyncio
    async def test_prepare_request_data_ignores_none_values(self, use_case):
        """Test que los valores None no se incluyen en la petición."""
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
            # Todos los campos opcionales son None por defecto
        )

        request_data = use_case._prepare_request_data(params)

        # Solo deben estar los campos requeridos
        expected_keys = {"scheduledAt", "status", "unitId", "isInspection"}
        assert set(request_data.keys()) == expected_keys

    @pytest.mark.asyncio
    async def test_transform_response(self, use_case, api_response):
        """Test transformación de respuesta de API."""
        work_order = use_case._transform_response(api_response)

        assert isinstance(work_order, HousekeepingWorkOrder)
        assert work_order.id == 1
        assert work_order.scheduled_at == "2024-01-15T10:00:00Z"
        assert work_order.status == HousekeepingWorkOrderStatus.PENDING
        assert work_order.unit_id == 123
        assert work_order.is_inspection is True
        assert work_order.time_estimate == 60.0
        assert work_order.created_at == "2024-01-15T09:00:00Z"

    @pytest.mark.asyncio
    async def test_transform_response_with_none_values(self, use_case):
        """Test transformación con valores None en la respuesta."""
        api_response = {
            "id": 1,
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitId": 123,
            "isInspection": True,
            # Otros campos son None
        }

        work_order = use_case._transform_response(api_response)

        assert work_order.id == 1
        assert work_order.unit_id == 123
        assert work_order.is_inspection is True
        assert work_order.time_estimate is None
        assert work_order.user_id is None
        assert work_order.comments is None
