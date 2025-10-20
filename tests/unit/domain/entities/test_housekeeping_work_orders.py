"""
Tests unitarios para entidades de housekeeping work orders.
"""

import pytest
from pydantic import ValidationError

from trackhs_mcp.domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrder,
    HousekeepingWorkOrderResponse,
    HousekeepingWorkOrderStatus,
)


class TestHousekeepingWorkOrderStatus:
    """Tests para el enum HousekeepingWorkOrderStatus."""

    def test_valid_statuses(self):
        """Test que todos los estados válidos están definidos."""
        valid_statuses = [
            "pending",
            "not-started",
            "in-progress",
            "completed",
            "processed",
            "cancelled",
            "exception",
        ]

        for status in valid_statuses:
            assert HousekeepingWorkOrderStatus(status) is not None

    def test_invalid_status(self):
        """Test que estados inválidos lanzan error."""
        with pytest.raises(ValueError):
            HousekeepingWorkOrderStatus("invalid-status")


class TestCreateHousekeepingWorkOrderParams:
    """Tests para CreateHousekeepingWorkOrderParams."""

    def test_valid_params_with_unit_id_and_inspection(self):
        """Test parámetros válidos con unit_id e is_inspection."""
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
        )

        assert params.scheduled_at == "2024-01-15T10:00:00Z"
        assert params.status == HousekeepingWorkOrderStatus.PENDING
        assert params.unit_id == 123
        assert params.is_inspection is True

    def test_valid_params_with_unit_block_id_and_clean_type(self):
        """Test parámetros válidos con unit_block_id y clean_type_id."""
        params = CreateHousekeepingWorkOrderParams(
            scheduled_at="2024-01-15",
            status=HousekeepingWorkOrderStatus.NOT_STARTED,
            unit_block_id=456,
            clean_type_id=5,
        )

        assert params.scheduled_at == "2024-01-15"
        assert params.status == HousekeepingWorkOrderStatus.NOT_STARTED
        assert params.unit_block_id == 456
        assert params.clean_type_id == 5

    def test_missing_unit_fields(self):
        """Test que falta unit_id y unit_block_id lanza error."""
        with pytest.raises(ValidationError) as exc_info:
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                is_inspection=True,
            )

        assert "Se requiere exactamente uno de unit_id o unit_block_id" in str(
            exc_info.value
        )

    def test_both_unit_fields(self):
        """Test que ambos unit_id y unit_block_id lanza error."""
        with pytest.raises(ValidationError) as exc_info:
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                unit_block_id=456,
                is_inspection=True,
            )

        assert "No se pueden especificar ambos unit_id y unit_block_id" in str(
            exc_info.value
        )

    def test_missing_task_type_fields(self):
        """Test que falta is_inspection y clean_type_id lanza error."""
        with pytest.raises(ValidationError) as exc_info:
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
            )

        assert "Se requiere exactamente uno de is_inspection o clean_type_id" in str(
            exc_info.value
        )

    def test_both_task_type_fields(self):
        """Test que ambos is_inspection y clean_type_id lanza error."""
        with pytest.raises(ValidationError) as exc_info:
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
                clean_type_id=5,
            )

        assert "No se pueden especificar ambos is_inspection y clean_type_id" in str(
            exc_info.value
        )

    def test_invalid_date_format(self):
        """Test que formato de fecha inválido lanza error."""
        with pytest.raises(ValidationError) as exc_info:
            CreateHousekeepingWorkOrderParams(
                scheduled_at="invalid-date",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
            )

        assert "scheduled_at debe estar en formato ISO 8601" in str(exc_info.value)

    def test_negative_time_estimate(self):
        """Test que time_estimate negativo lanza error."""
        with pytest.raises(ValidationError):
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
                time_estimate=-10,
            )

    def test_negative_cost(self):
        """Test que cost negativo lanza error."""
        with pytest.raises(ValidationError):
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
                cost=-50.0,
            )

    def test_zero_user_id(self):
        """Test que user_id cero lanza error."""
        with pytest.raises(ValidationError):
            CreateHousekeepingWorkOrderParams(
                scheduled_at="2024-01-15T10:00:00Z",
                status=HousekeepingWorkOrderStatus.PENDING,
                unit_id=123,
                is_inspection=True,
                user_id=0,
            )

    def test_all_optional_fields(self):
        """Test que todos los campos opcionales se pueden especificar."""
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
            comments="Limpieza profunda requerida",
            cost=100.0,
        )

        assert params.time_estimate == 60.0
        assert params.actual_time == 45.0
        assert params.user_id == 789
        assert params.vendor_id == 101
        assert params.reservation_id == 202
        assert params.is_turn is True
        assert params.is_manual is False
        assert params.charge_owner is True
        assert params.comments == "Limpieza profunda requerida"
        assert params.cost == 100.0


class TestHousekeepingWorkOrder:
    """Tests para HousekeepingWorkOrder."""

    def test_create_work_order(self):
        """Test crear una orden de trabajo."""
        work_order = HousekeepingWorkOrder(
            id=1,
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
            time_estimate=60.0,
            created_at="2024-01-15T09:00:00Z",
        )

        assert work_order.id == 1
        assert work_order.scheduled_at == "2024-01-15T10:00:00Z"
        assert work_order.status == HousekeepingWorkOrderStatus.PENDING
        assert work_order.unit_id == 123
        assert work_order.is_inspection is True
        assert work_order.time_estimate == 60.0
        assert work_order.created_at == "2024-01-15T09:00:00Z"


class TestHousekeepingWorkOrderResponse:
    """Tests para HousekeepingWorkOrderResponse."""

    def test_success_response(self):
        """Test respuesta de éxito."""
        work_order = HousekeepingWorkOrder(
            id=1,
            scheduled_at="2024-01-15T10:00:00Z",
            status=HousekeepingWorkOrderStatus.PENDING,
            unit_id=123,
            is_inspection=True,
        )

        response = HousekeepingWorkOrderResponse.success_response(work_order)

        assert response.success is True
        assert response.data == work_order
        assert (
            response.message == "Orden de trabajo de housekeeping creada exitosamente"
        )
        assert response.errors is None

    def test_error_response(self):
        """Test respuesta de error."""
        errors = ["Error de validación", "Campo requerido faltante"]
        response = HousekeepingWorkOrderResponse.error_response(
            "Error al crear orden", errors
        )

        assert response.success is False
        assert response.data is None
        assert response.message == "Error al crear orden"
        assert response.errors == errors

    def test_error_response_without_errors(self):
        """Test respuesta de error sin lista de errores."""
        response = HousekeepingWorkOrderResponse.error_response("Error simple")

        assert response.success is False
        assert response.data is None
        assert response.message == "Error simple"
        assert response.errors == []
