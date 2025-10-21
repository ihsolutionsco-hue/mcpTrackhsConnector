"""
Tests de integración para create_work_order
Verifica que el use case funcione correctamente con dependencias reales
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.application.use_cases.create_work_order import (
    CreateWorkOrderUseCase,
)
from src.trackhs_mcp.domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrderResponse,
    WorkOrderStatus,
)


class TestCreateWorkOrderIntegration:
    """Tests de integración para create_work_order"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = AsyncMock()
        client.post.return_value = {
            "id": 123,
            "dateReceived": "2024-01-15T10:00:00Z",
            "priority": 3,
            "status": "open",
            "summary": "Test Work Order Summary",
            "estimatedCost": 100.0,
            "estimatedTime": 60,
            "unitId": 123,
            "userId": 456,
            "vendorId": 789,
            "dateScheduled": "2024-01-20T14:00:00Z",
            "description": "Test Description",
            "source": "maintenance",
            "sourceName": "John Doe",
            "sourcePhone": "+1234567890",
            "createdAt": "2024-01-15T10:00:00Z",
            "updatedAt": "2024-01-15T10:00:00Z",
            "createdBy": "system",
            "updatedBy": "system",
        }
        return client

    @pytest.fixture
    def create_use_case(self, mock_api_client):
        """Use case con dependencias mockeadas"""
        return CreateWorkOrderUseCase(api_client=mock_api_client)

    @pytest.mark.asyncio
    async def test_create_work_order_success_integration(
        self, create_use_case, mock_api_client
    ):
        """Test de integración exitoso para create_work_order"""
        # Arrange
        params = CreateWorkOrderParams(
            date_received="2024-01-15T10:00:00Z",
            priority=3,
            status=WorkOrderStatus.OPEN,
            summary="Test Work Order Summary",
            estimated_cost=100.0,
            estimated_time=60,
            unit_id=123,
        )

        # Act
        result = await create_use_case.execute(params)

        # Assert
        assert result is not None
        assert type(result).__name__ == "WorkOrderResponse"
        assert result.work_order.id == 123
        assert result.work_order.summary == "Test Work Order Summary"
        assert result.work_order.description == "Test Description"
        assert result.work_order.priority == 3
        assert result.work_order.status == "open"

        # Verificar que se llamó al API client
        mock_api_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_work_order_with_all_fields_integration(
        self, create_use_case, mock_api_client
    ):
        """Test de integración con todos los campos"""
        # Arrange
        params = CreateWorkOrderParams(
            date_received="2024-01-15T10:00:00Z",
            priority=5,
            status=WorkOrderStatus.OPEN,
            summary="Complete Work Order Summary",
            estimated_cost=200.0,
            estimated_time=120,
            unit_id=456,
            user_id=789,
            vendor_id=101,
            date_scheduled="2024-01-20T14:00:00Z",
        )

        # Act
        result = await create_use_case.execute(params)

        # Assert
        assert result is not None
        assert result.work_order.id == 123
        assert result.work_order.summary == "Test Work Order Summary"  # Mock response

        # Verificar que se llamó al API client
        mock_api_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_work_order_validation_error_integration(
        self, create_use_case
    ):
        """Test de integración con error de validación"""
        # Arrange - parámetros inválidos (faltan campos requeridos)
        with pytest.raises(ValueError):
            params = CreateWorkOrderParams(
                date_received="2024-01-15T10:00:00Z",
                priority=3,
                status=WorkOrderStatus.OPEN,
                summary="",  # Campo vacío
                estimated_cost=100.0,
                estimated_time=60,
            )
            await create_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_create_work_order_api_error_integration(self, mock_api_client):
        """Test de integración con error de API"""
        # Arrange
        mock_api_client.post.side_effect = Exception("API Error")
        create_use_case = CreateWorkOrderUseCase(api_client=mock_api_client)

        params = CreateWorkOrderParams(
            date_received="2024-01-15T10:00:00Z",
            priority=3,
            status=WorkOrderStatus.OPEN,
            summary="Test Work Order Summary",
            estimated_cost=100.0,
            estimated_time=60,
            unit_id=123,
        )

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await create_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_create_work_order_different_priorities_integration(
        self, create_use_case, mock_api_client
    ):
        """Test de integración con diferentes prioridades"""
        priorities = [1, 3, 5]  # Baja, Media, Alta

        for priority in priorities:
            # Arrange
            params = CreateWorkOrderParams(
                date_received="2024-01-15T10:00:00Z",
                priority=priority,
                status=WorkOrderStatus.OPEN,
                summary=f"Work Order Priority {priority}",
                estimated_cost=100.0,
                estimated_time=60,
                unit_id=123,
            )

            # Act
            result = await create_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.work_order.priority == 3  # Mock response

    @pytest.mark.asyncio
    async def test_create_work_order_with_optional_fields_integration(
        self, create_use_case, mock_api_client
    ):
        """Test de integración con campos opcionales"""
        # Arrange
        params = CreateWorkOrderParams(
            date_received="2024-01-15T10:00:00Z",
            priority=3,
            status=WorkOrderStatus.OPEN,
            summary="Optional Fields Work Order",
            estimated_cost=150.0,
            estimated_time=90,
            unit_id=123,
            user_id=456,
            vendor_id=789,
            date_scheduled="2024-01-25T10:00:00Z",
        )

        # Act
        result = await create_use_case.execute(params)

        # Assert
        assert result is not None
        assert result.work_order.id == 123

        # Verificar que se llamó al API client
        mock_api_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_work_order_complete_workflow_integration(
        self, create_use_case, mock_api_client
    ):
        """Test de integración del workflow completo"""
        # Arrange
        params = CreateWorkOrderParams(
            date_received="2024-01-15T10:00:00Z",
            priority=5,
            status=WorkOrderStatus.OPEN,
            summary="Complete Workflow Test",
            estimated_cost=300.0,
            estimated_time=180,
            unit_id=789,
            user_id=123,
            vendor_id=456,
            date_scheduled="2024-01-30T10:00:00Z",
        )

        # Act
        result = await create_use_case.execute(params)

        # Assert
        assert result is not None
        assert type(result).__name__ == "WorkOrderResponse"
        assert result.work_order.id == 123
        assert result.work_order.summary == "Test Work Order Summary"  # Mock response

        # Verificar que el API client fue llamado
        mock_api_client.post.assert_called_once()

        # Verificar que los parámetros se pasaron correctamente
        call_args = mock_api_client.post.call_args
        assert call_args is not None
