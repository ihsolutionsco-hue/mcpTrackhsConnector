"""
Tests unitarios para GetReservationUseCase
"""

from unittest.mock import AsyncMock, Mock

import pytest

from trackhs_mcp.application.use_cases.get_reservation import GetReservationUseCase
from trackhs_mcp.domain.entities.reservations import GetReservationParams
from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from trackhs_mcp.infrastructure.utils.error_handling import TrackHSError


class TestGetReservationUseCase:
    """Tests para GetReservationUseCase"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del use case con mock"""
        return GetReservationUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_api_client):
        """Test ejecución exitosa"""
        # Arrange
        reservation_id = 12345
        mock_response = {
            "id": reservation_id,
            "status": "Confirmed",
            "arrival_date": "2024-01-15",
            "departure_date": "2024-01-20",
            "nights": 5,
            "currency": "USD",
            "unit_id": 789,
            "contact_id": 456,
            "unit_type_id": 1,
            "is_unit_locked": False,
            "is_unit_assigned": True,
            "is_unit_type_locked": False,
            "early_arrival": False,
            "late_departure": False,
            "arrival_time": "2024-01-15T15:00:00Z",
            "departure_time": "2024-01-20T11:00:00Z",
            "occupants": [
                {
                    "type_id": 1,
                    "name": "Adult",
                    "handle": "adult",
                    "quantity": 2,
                    "included": True,
                    "extra_quantity": 0,
                    "rate_per_person_per_stay": "0.00",
                    "rate_per_stay": "0.00",
                }
            ],
            "security_deposit": {"required": "200.00", "remaining": 200.0},
            "updated_at": "2024-01-10T10:00:00Z",
            "created_at": "2024-01-10T10:00:00Z",
            "booked_at": "2024-01-10T10:00:00Z",
            "guest_breakdown": {
                "gross_rent": "1000.00",
                "guest_gross_display_rent": "1000.00",
                "discount": "0.00",
                "promo_value": "0.00",
                "discount_total": 0,
                "net_rent": "950.00",
                "guest_net_display_rent": "950.00",
                "actual_adr": "190.00",
                "guest_adr": "190.00",
                "total_guest_fees": "50.00",
                "total_rent_fees": "0.00",
                "total_itemized_fees": "0.00",
                "total_tax_fees": "0.00",
                "total_service_fees": "0.00",
                "folio_charges": "0.00",
                "subtotal": "1000.00",
                "guest_subtotal": "1000.00",
                "total_taxes": "0.00",
                "total_guest_taxes": "0.00",
                "total": "1000.00",
                "grand_total": "1000.00",
                "net_payments": "1000.00",
                "payments": "1000.00",
                "refunds": "0.00",
                "net_transfers": "0.00",
                "balance": "0.00",
                "rates": [],
                "guest_fees": [],
                "taxes": [],
            },
            "owner_breakdown": {
                "gross_rent": "1000.00",
                "fee_revenue": "0.00",
                "gross_revenue": "1000.00",
                "manager_commission": "100.00",
                "agent_commission": "0.00",
                "net_revenue": "900.00",
                "owner_fees": [],
            },
            "channel_id": 1,
            "folio_id": 1,
            "user_id": 1,
            "type_id": 1,
            "rate_type_id": 1,
            "is_taxable": True,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "source": "direct",
            "is_channel_locked": False,
            "agreement_status": "not-needed",
            "automate_payment": False,
            "revenue_realized_method": "nightly",
            "updated_by": "admin",
            "created_by": "admin",
            "payment_plan": [],
            "travel_insurance_products": [],
            "_embedded": {
                "unit": {"id": 789, "name": "Casa de Playa"},
                "contact": {"id": 456, "name": "Juan Pérez"},
            },
            "_links": {},
        }
        mock_api_client.get.return_value = mock_response

        params = GetReservationParams(reservation_id=reservation_id)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result.id == reservation_id
        assert result.status == "Confirmed"
        assert result.arrival_date == "2024-01-15"
        assert result.departure_date == "2024-01-20"
        assert result.nights == 5
        mock_api_client.get.assert_called_once_with(
            f"/v2/pms/reservations/{reservation_id}"
        )

    @pytest.mark.asyncio
    async def test_execute_invalid_id_zero(self, use_case):
        """Test con ID inválido (cero)"""
        # Arrange
        params = GetReservationParams(reservation_id=0)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "reservation_id debe ser un entero positivo mayor que 0" in str(
            exc_info.value
        )
        assert exc_info.value.field == "reservation_id"

    @pytest.mark.asyncio
    async def test_execute_invalid_id_negative(self, use_case):
        """Test con ID inválido (negativo)"""
        # Arrange
        params = GetReservationParams(reservation_id=-1)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "reservation_id debe ser un entero positivo mayor que 0" in str(
            exc_info.value
        )
        assert exc_info.value.field == "reservation_id"

    @pytest.mark.asyncio
    async def test_execute_empty_response(self, use_case, mock_api_client):
        """Test con respuesta vacía"""
        # Arrange
        reservation_id = 12345
        mock_api_client.get.return_value = None

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert f"No se encontraron datos para la reserva ID {reservation_id}" in str(
            exc_info.value
        )
        assert exc_info.value.field == "reservation_id"

    @pytest.mark.asyncio
    async def test_execute_api_error_401(self, use_case, mock_api_client):
        """Test error 401 (no autorizado)"""
        # Arrange
        reservation_id = 12345
        error = Exception("401 Unauthorized")
        error.status_code = 401
        mock_api_client.get.side_effect = error

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "No autorizado" in str(exc_info.value)
        assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_api_error_403(self, use_case, mock_api_client):
        """Test error 403 (prohibido)"""
        # Arrange
        reservation_id = 12345
        error = Exception("403 Forbidden")
        error.status_code = 403
        mock_api_client.get.side_effect = error

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Prohibido" in str(exc_info.value)
        assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_api_error_404(self, use_case, mock_api_client):
        """Test error 404 (no encontrado)"""
        # Arrange
        reservation_id = 12345
        error = Exception("404 Not Found")
        error.status_code = 404
        mock_api_client.get.side_effect = error

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Reserva no encontrada" in str(exc_info.value)
        assert f"No existe una reserva con ID {reservation_id}" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_api_error_500(self, use_case, mock_api_client):
        """Test error 500 (error interno)"""
        # Arrange
        reservation_id = 12345
        error = Exception("500 Internal Server Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Error interno del servidor" in str(exc_info.value)
        assert "API está temporalmente no disponible" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_generic_error(self, use_case, mock_api_client):
        """Test error genérico"""
        # Arrange
        reservation_id = 12345
        mock_api_client.get.side_effect = Exception("Error de conexión")

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(params)

        assert "Error de conexión" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_validation_error_propagation(
        self, use_case, mock_api_client
    ):
        """Test que ValidationError se propaga correctamente"""
        # Arrange
        reservation_id = 12345
        validation_error = ValidationError("Error de validación", "field")
        mock_api_client.get.side_effect = validation_error

        params = GetReservationParams(reservation_id=reservation_id)

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Error de validación" in str(exc_info.value)
        assert exc_info.value.field == "field"

    @pytest.mark.asyncio
    async def test_execute_with_embedded_data(self, use_case, mock_api_client):
        """Test con datos embebidos completos"""
        # Arrange
        reservation_id = 12345
        mock_response = {
            "id": reservation_id,
            "status": "Confirmed",
            "arrival_date": "2024-01-15",
            "departure_date": "2024-01-20",
            "nights": 5,
            "currency": "USD",
            "unit_id": 789,
            "contact_id": 456,
            "unit_type_id": 1,
            "is_unit_locked": False,
            "is_unit_assigned": True,
            "is_unit_type_locked": False,
            "early_arrival": False,
            "late_departure": False,
            "arrival_time": "2024-01-15T15:00:00Z",
            "departure_time": "2024-01-20T11:00:00Z",
            "occupants": [
                {
                    "type_id": 1,
                    "name": "Adult",
                    "handle": "adult",
                    "quantity": 2,
                    "included": True,
                    "extra_quantity": 0,
                    "rate_per_person_per_stay": "0.00",
                    "rate_per_stay": "0.00",
                }
            ],
            "security_deposit": {"required": "200.00", "remaining": 200.0},
            "updated_at": "2024-01-10T10:00:00Z",
            "created_at": "2024-01-10T10:00:00Z",
            "booked_at": "2024-01-10T10:00:00Z",
            "guest_breakdown": {
                "gross_rent": "1000.00",
                "guest_gross_display_rent": "1000.00",
                "discount": "0.00",
                "promo_value": "0.00",
                "discount_total": 0,
                "net_rent": "950.00",
                "guest_net_display_rent": "950.00",
                "actual_adr": "190.00",
                "guest_adr": "190.00",
                "total_guest_fees": "50.00",
                "total_rent_fees": "0.00",
                "total_itemized_fees": "0.00",
                "total_tax_fees": "0.00",
                "total_service_fees": "0.00",
                "folio_charges": "0.00",
                "subtotal": "1000.00",
                "guest_subtotal": "1000.00",
                "total_taxes": "0.00",
                "total_guest_taxes": "0.00",
                "total": "1000.00",
                "grand_total": "1000.00",
                "net_payments": "1000.00",
                "payments": "1000.00",
                "refunds": "0.00",
                "net_transfers": "0.00",
                "balance": "0.00",
                "rates": [],
                "guest_fees": [],
                "taxes": [],
            },
            "owner_breakdown": {
                "gross_rent": "1000.00",
                "fee_revenue": "0.00",
                "gross_revenue": "1000.00",
                "manager_commission": "100.00",
                "agent_commission": "0.00",
                "net_revenue": "900.00",
                "owner_fees": [],
            },
            "channel_id": 1,
            "folio_id": 1,
            "user_id": 1,
            "type_id": 1,
            "rate_type_id": 1,
            "is_taxable": True,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "source": "direct",
            "is_channel_locked": False,
            "agreement_status": "not-needed",
            "automate_payment": False,
            "revenue_realized_method": "nightly",
            "updated_by": "admin",
            "created_by": "admin",
            "payment_plan": [],
            "travel_insurance_products": [],
            "_embedded": {
                "unit": {
                    "id": 789,
                    "name": "Casa de Playa",
                    "street_address": "123 Ocean Drive",
                    "max_occupancy": 8,
                    "bedrooms": 3,
                    "full_bathrooms": 2,
                },
                "contact": {
                    "id": 456,
                    "name": "Juan Pérez",
                    "primary_email": "juan@email.com",
                    "cell_phone": "+1234567890",
                },
                "guarantee_policy": {
                    "id": 1,
                    "name": "Política Estándar",
                    "type": "Guarantee",
                },
                "cancellation_policy": {
                    "id": 2,
                    "name": "Cancelación Flexible",
                    "charge_as": "fee",
                },
            },
            "_links": {},
        }
        mock_api_client.get.return_value = mock_response

        params = GetReservationParams(reservation_id=reservation_id)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert result.id == reservation_id
        assert result.status == "Confirmed"
        assert result.arrival_date == "2024-01-15"
        assert result.departure_date == "2024-01-20"
        assert result.nights == 5
        assert result.currency == "USD"
        assert result.unit_id == 789
        assert result.contact_id == 456

        # Verificar datos embebidos
        assert result.embedded is not None
        assert "unit" in result.embedded
        assert "contact" in result.embedded
        assert "guarantee_policy" in result.embedded
        assert "cancellation_policy" in result.embedded
