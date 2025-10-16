"""
Tests unitarios para CreateWorkOrderUseCase - Versión corregida.

Este módulo contiene tests que se enfocan en la funcionalidad real del use case,
no en las validaciones de Pydantic que ya funcionan correctamente.
"""

from unittest.mock import Mock

import pytest

from trackhs_mcp.application.use_cases.create_work_order import CreateWorkOrderUseCase
from trackhs_mcp.domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrderResponse,
    WorkOrderStatus,
)
from trackhs_mcp.domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ServerError,
    ValidationError,
)


class TestCreateWorkOrderUseCase:
    """Tests para CreateWorkOrderUseCase."""

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Caso de uso para testing."""
        return CreateWorkOrderUseCase(mock_api_client)

    def test_successful_execution(
        self, use_case, mock_api_client, sample_work_order_minimal
    ):
        """Test ejecución exitosa del caso de uso."""
        # Configurar mock para devolver datos síncronos
        from unittest.mock import Mock

        mock_api_client.post = Mock(return_value=sample_work_order_minimal)

        # Ejecutar caso de uso
        result = use_case.execute(
            CreateWorkOrderParams(
                dateReceived="2024-01-15",
                priority=3,
                status=WorkOrderStatus.NOT_STARTED,
                summary="Test",
                estimatedCost=75.50,
                estimatedTime=60,
            )
        )

        # Verificar resultado
        assert isinstance(result, WorkOrderResponse)
        assert result.success is True
        assert result.work_order.id == 67890
        assert result.work_order.summary == "Mantenimiento preventivo"
        assert result.work_order.priority == 3
        assert result.work_order.status == WorkOrderStatus.NOT_STARTED
        assert result.work_order.estimated_cost == 75.5
        assert result.work_order.estimated_time == 60

        # Verificar llamada a API
        mock_api_client.post.assert_called_once()
        call_args = mock_api_client.post.call_args
        assert call_args[0][0] == "/pms/maintenance/work-orders"
        assert call_args[1]["data"]["dateReceived"] == "2024-01-15"
        assert call_args[1]["data"]["priority"] == 3
        assert call_args[1]["data"]["status"] == "not-started"

    def test_payload_construction_minimal(
        self, use_case, mock_api_client, sample_work_order_minimal
    ):
        """Test construcción de payload con campos mínimos."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(return_value=sample_work_order_minimal)

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        result = use_case.execute(params)

        # Verificar que se llamó a la API
        mock_api_client.post.assert_called_once()
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]

        # Verificar campos requeridos
        assert payload["dateReceived"] == "2024-01-15"
        assert payload["priority"] == 3
        assert payload["status"] == "not-started"
        assert payload["summary"] == "Test"
        assert payload["estimatedCost"] == 75.50
        assert payload["estimatedTime"] == 60

    def test_payload_construction_complete(
        self, use_case, mock_api_client, sample_work_order_response
    ):
        """Test construcción de payload con todos los campos."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(return_value=sample_work_order_response)

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=5,
            status=WorkOrderStatus.OPEN,
            summary="Test completo",
            estimatedCost=150.00,
            estimatedTime=120,
            dateScheduled="2024-01-16T09:00:00Z",
            userId=1,
            vendorId=456,
            unitId=123,
            reservationId=37165851,
            referenceNumber="WO-2024-001",
            description="Descripción detallada",
            workPerformed="Trabajo realizado",
            source="Guest Request",
            sourceName="Juan Pérez",
            sourcePhone="+1234567890",
            actualTime=90,
            blockCheckin=True,
        )

        result = use_case.execute(params)

        # Verificar que se llamó a la API
        mock_api_client.post.assert_called_once()
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]

        # Verificar todos los campos
        assert payload["dateReceived"] == "2024-01-15"
        assert payload["priority"] == 5
        assert payload["status"] == "open"
        assert payload["summary"] == "Test completo"
        assert payload["estimatedCost"] == 150.00
        assert payload["estimatedTime"] == 120
        assert payload["dateScheduled"] == "2024-01-16T09:00:00Z"
        assert payload["userId"] == 1
        assert payload["vendorId"] == 456
        assert payload["unitId"] == 123
        assert payload["reservationId"] == 37165851
        assert payload["referenceNumber"] == "WO-2024-001"
        assert payload["description"] == "Descripción detallada"
        assert payload["workPerformed"] == "Trabajo realizado"
        assert payload["source"] == "Guest Request"
        assert payload["sourceName"] == "Juan Pérez"
        assert payload["sourcePhone"] == "+1234567890"
        assert payload["actualTime"] == 90
        assert payload["blockCheckin"] is True

    def test_api_error_401_handling(self, use_case, mock_api_client):
        """Test manejo de error 401 de API."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(side_effect=ApiError("Unauthorized", 401))

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        with pytest.raises(AuthenticationError) as exc_info:
            use_case.execute(params)

        assert "No autorizado" in str(exc_info.value)

    def test_api_error_403_handling(self, use_case, mock_api_client):
        """Test manejo de error 403 de API."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(side_effect=ApiError("Forbidden", 403))

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        with pytest.raises(AuthorizationError) as exc_info:
            use_case.execute(params)

        assert "Prohibido" in str(exc_info.value)

    def test_api_error_422_handling(self, use_case, mock_api_client):
        """Test manejo de error 422 de API."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(side_effect=ApiError("Validation failed", 422))

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        with pytest.raises(ValidationError) as exc_info:
            use_case.execute(params)

        assert "Datos inválidos" in str(exc_info.value)

    def test_api_error_500_handling(self, use_case, mock_api_client):
        """Test manejo de error 500 de API."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(side_effect=ApiError("Internal Server Error", 500))

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        with pytest.raises(ServerError) as exc_info:
            use_case.execute(params)

        assert "Error interno del servidor" in str(exc_info.value)

    def test_unexpected_error_handling(self, use_case, mock_api_client):
        """Test manejo de error inesperado."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(side_effect=Exception("Unexpected error"))

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=3,
            status=WorkOrderStatus.NOT_STARTED,
            summary="Test",
            estimatedCost=75.50,
            estimatedTime=60,
        )

        with pytest.raises(ApiError) as exc_info:
            use_case.execute(params)

        assert "Error inesperado" in str(exc_info.value)

    def test_work_order_response_creation(
        self, use_case, mock_api_client, sample_work_order_response
    ):
        """Test creación de respuesta WorkOrderResponse."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(return_value=sample_work_order_response)

        params = CreateWorkOrderParams(
            dateReceived="2024-01-15",
            priority=5,
            status=WorkOrderStatus.OPEN,
            summary="Reparar aire acondicionado en unidad 101",
            estimatedCost=150.00,
            estimatedTime=120,
        )

        result = use_case.execute(params)

        # Verificar estructura de respuesta
        assert result.success is True
        assert result.work_order.id == 12345
        assert result.work_order.summary == "Reparar aire acondicionado en unidad 101"
        assert result.work_order.priority == 5
        assert result.work_order.status == WorkOrderStatus.OPEN
        assert result.work_order.estimated_cost == 150.00
        assert result.work_order.estimated_time == 120

    def test_iso8601_date_validation_valid_dates(
        self, use_case, mock_api_client, sample_work_order_minimal
    ):
        """Test validación de fechas ISO 8601 válidas."""
        from unittest.mock import Mock

        mock_api_client.post = Mock(return_value=sample_work_order_minimal)

        valid_dates = [
            "2024-01-15",
            "2024-01-15T10:30:00Z",
            "2024-01-15T10:30:00+00:00",
            "2024-01-15T10:30:00-05:00",
        ]

        for date_str in valid_dates:
            params = CreateWorkOrderParams(
                dateReceived=date_str,
                priority=3,
                status=WorkOrderStatus.NOT_STARTED,
                summary="Test",
                estimatedCost=75.50,
                estimatedTime=60,
            )

            result = use_case.execute(params)
            assert result.success is True
            # Verificar que el payload se construyó correctamente con la fecha
            call_args = mock_api_client.post.call_args
            assert call_args[1]["data"]["dateReceived"] == date_str
