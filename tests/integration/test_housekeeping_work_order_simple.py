"""
Test simple de integración para housekeeping work order.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from trackhs_mcp.application.use_cases.create_housekeeping_work_order import (
    CreateHousekeepingWorkOrderUseCase,
)
from trackhs_mcp.domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrderStatus,
)


class TestHousekeepingWorkOrderSimple:
    """Test simple de integración."""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Use case con mock."""
        return CreateHousekeepingWorkOrderUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_create_housekeeping_work_order_success(
        self, use_case, mock_api_client
    ):
        """Test creación exitosa."""
        # Configurar mock
        mock_api_response = {
            "id": 1,
            "scheduledAt": "2024-01-15T10:00:00Z",
            "status": "pending",
            "unitId": 123,
            "isInspection": True,
            "timeEstimate": 60.0,
            "createdAt": "2024-01-15T09:00:00Z",
        }
        mock_api_client.create_housekeeping_work_order.return_value = mock_api_response

        # Crear parámetros
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
        )

        # Ejecutar
        result = await use_case.execute(params)

        # Verificar
        assert result.success is True
        assert result.data is not None
        assert result.data.id == 1
        assert result.data.scheduled_at == "2024-01-15T10:00:00Z"
        assert result.data.status == HousekeepingWorkOrderStatus.PENDING
        assert result.data.unit_id == 123
        assert result.data.is_inspection is True
        assert result.message == "Orden de trabajo de housekeeping creada exitosamente"

    @pytest.mark.asyncio
    async def test_create_housekeeping_work_order_with_unit_block_id(
        self, use_case, mock_api_client
    ):
        """Test con unit_block_id."""
        mock_api_response = {
            "id": 2,
            "scheduledAt": "2024-01-15T14:00:00Z",
            "status": "not-started",
            "unitBlockId": 456,
            "cleanTypeId": 5,
            "timeEstimate": 90.0,
        }
        mock_api_client.create_housekeeping_work_order.return_value = mock_api_response

        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T14:00:00Z",
            status=HousekeepingWorkOrderStatus.NOT_STARTED,
            unit_block_id=456,
            clean_type_id=5,
        )

        result = await use_case.execute(params)

        assert result.success is True
        assert result.data.unit_block_id == 456
        assert result.data.clean_type_id == 5

    @pytest.mark.asyncio
    async def test_create_housekeeping_work_order_with_all_fields(
        self, use_case, mock_api_client
    ):
        """Test con todos los campos."""
        mock_api_response = {
            "id": 3,
            "scheduledAt": "2024-01-15T16:00:00Z",
            "status": "pending",
            "unitId": 789,
            "isInspection": False,
            "cleanTypeId": 3,
            "timeEstimate": 120.0,
            "actualTime": 110.0,
            "userId": 101,
            "vendorId": 202,
            "reservationId": 303,
            "isTurn": True,
            "isManual": False,
            "chargeOwner": True,
            "comments": "Limpieza profunda requerida",
            "cost": 150.0,
        }
        mock_api_client.create_housekeeping_work_order.return_value = mock_api_response

        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T16:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=789,
            is_inspection=False,
            clean_type_id=3,
            time_estimate=120.0,
            actual_time=110.0,
            user_id=101,
            vendor_id=202,
            reservation_id=303,
            is_turn=True,
            is_manual=False,
            charge_owner=True,
            comments="Limpieza profunda requerida",
            cost=150.0,
        )

        result = await use_case.execute(params)

        assert result.success is True
        assert result.data.id == 3
        assert result.data.comments == "Limpieza profunda requerida"
        assert result.data.cost == 150.0

    @pytest.mark.asyncio
    async def test_validation_missing_unit_fields(self, use_case):
        """Test validación de campos de unidad faltantes."""
        with pytest.raises(ValueError) as exc_info:
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                is_inspection=True,
            )

        assert "Se requiere exactamente uno de unit_id o unit_block_id" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_validation_both_unit_fields(self, use_case):
        """Test validación de ambos campos de unidad."""
        with pytest.raises(ValueError) as exc_info:
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                unit_block_id=456,
                is_inspection=True,
            )

        assert "No se pueden especificar ambos unit_id y unit_block_id" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_validation_missing_task_type_fields(self, use_case):
        """Test validación de campos de tipo de tarea faltantes."""
        with pytest.raises(ValueError) as exc_info:
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
            )

        assert "Se requiere exactamente uno de is_inspection o clean_type_id" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_validation_both_task_type_fields(self, use_case):
        """Test validación de ambos campos de tipo de tarea."""
        with pytest.raises(ValueError) as exc_info:
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
                clean_type_id=5,
            )

        assert "No se pueden especificar ambos is_inspection y clean_type_id" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_validation_invalid_date_format(self, use_case):
        """Test validación de formato de fecha inválido."""
        with pytest.raises(ValueError) as exc_info:
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at="invalid-date",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
            )

        assert "scheduled_at debe estar en formato ISO 8601" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_api_error_handling(self, use_case, mock_api_client):
        """Test manejo de errores de API."""
        mock_api_client.create_housekeeping_work_order.side_effect = Exception(
            "API Error"
        )

        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
        )

        result = await use_case.execute(params)

        assert result.success is False
        assert "Error al crear orden de trabajo" in result.message
        assert "API Error" in result.message
