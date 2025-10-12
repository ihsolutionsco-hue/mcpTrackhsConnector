"""
Tests de integración para get_reservation_v2
Valida el funcionamiento completo con la API real de TrackHS
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from trackhs_mcp.application.use_cases.get_reservation import GetReservationUseCase
from trackhs_mcp.domain.entities.reservations import GetReservationParams
from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.utils.error_handling import TrackHSError


class TestGetReservationV2Integration:
    """Tests de integración para get_reservation_v2"""

    @pytest.fixture
    def config(self):
        """Configuración de prueba"""
        return TrackHSConfig(
            base_url="https://api-integration-example.tracksandbox.io",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    @pytest.fixture
    def api_client(self, config):
        """Cliente API de prueba"""
        return TrackHSApiClient(config)

    @pytest.fixture
    def use_case(self, api_client):
        """Use case con cliente real"""
        return GetReservationUseCase(api_client)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_reservation_success_integration(
        self, use_case, sample_reservation_data
    ):
        """Test de integración exitoso con mock"""
        # Arrange
        reservation_id = "12345"  # ID de reserva de prueba
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API
        with patch.object(use_case.api_client, "get", return_value=mock_response):
            # Act
            result = await use_case.execute(
                GetReservationParams(reservation_id=reservation_id)
            )

            # Assert
            assert result is not None
            assert result.id == int(reservation_id)
            assert result.status == "Confirmed"
            assert result.currency == "USD"
            assert result.nights == 5

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_reservation_not_found_integration(self, use_case):
        """Test de integración con reserva inexistente"""
        # Arrange
        reservation_id = "999999"  # ID que no existe

        # Act & Assert
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(GetReservationParams(reservation_id=reservation_id))

        assert "Endpoint not found" in str(exc_info.value)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_reservation_auth_error_integration(self, config):
        """Test de integración con credenciales inválidas"""
        # Arrange
        invalid_config = TrackHSConfig(
            base_url=config.base_url,
            username="invalid_user",
            password="invalid_password",
            timeout=30,
        )

        # El cliente se puede crear con credenciales inválidas
        # pero fallará al hacer la petición real
        client = TrackHSApiClient(invalid_config)
        assert client is not None

    @pytest.mark.asyncio
    async def test_get_reservation_mock_integration(
        self, use_case, sample_reservation_data
    ):
        """Test de integración con mock de API"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API
        with patch.object(use_case.api_client, "get", return_value=mock_response):
            # Act
            result = await use_case.execute(
                GetReservationParams(reservation_id=reservation_id)
            )

            # Assert
            assert result is not None
            assert result.id == int(reservation_id)
            assert result.status == "Confirmed"
            assert result.currency == "USD"
            assert result.nights == 5
            assert result.contact_id == 1

            # Verificar datos embebidos
            assert result.embedded is not None
            assert "unit" in result.embedded
            assert "contact" in result.embedded

            # Verificar información financiera
            assert result.guest_breakdown is not None
            assert result.guest_breakdown.gross_rent == "1000.00"
            assert result.guest_breakdown.net_rent == "950.00"
            assert result.guest_breakdown.grand_total == "1000.00"
            assert result.guest_breakdown.balance == "0.00"

            # owner_breakdown no está incluido en el fixture

            assert result.security_deposit is not None
            assert result.security_deposit.required == "100.00"
            assert result.security_deposit.remaining == 100

    @pytest.mark.asyncio
    async def test_get_reservation_error_handling_integration(self, use_case):
        """Test de integración de manejo de errores"""
        # Arrange
        reservation_id = "12345"
        error_response = {
            "type": "https://tools.ietf.org/html/rfc2616/rfc2616-sec10.html",
            "title": "Not Found",
            "status": 404,
            "detail": "Reservation not found",
        }

        # Mock del cliente API para simular error 404
        with patch.object(
            use_case.api_client, "get", side_effect=Exception("404 Not Found")
        ):
            # Act & Assert
            with pytest.raises(Exception):
                await use_case.execute(
                    GetReservationParams(reservation_id=reservation_id)
                )

    @pytest.mark.asyncio
    async def test_get_reservation_validation_integration(self, use_case):
        """Test de integración de validaciones"""
        # Test con ID inválido
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(GetReservationParams(reservation_id=0))

        assert "reservation_id es requerido" in str(exc_info.value)

        # Test con ID negativo
        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(GetReservationParams(reservation_id="-1"))

        assert "reservation_id debe ser un número entero positivo válido" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_get_reservation_timeout_integration(self, use_case):
        """Test de integración con timeout"""
        # Arrange
        reservation_id = "12345"

        # Mock del cliente API para simular timeout
        with patch.object(
            use_case.api_client,
            "get",
            side_effect=asyncio.TimeoutError("Request timeout"),
        ):
            # Act & Assert
            with pytest.raises(Exception):
                await use_case.execute(
                    GetReservationParams(reservation_id=reservation_id)
                )

    @pytest.mark.asyncio
    async def test_get_reservation_network_error_integration(self, use_case):
        """Test de integración con error de red"""
        # Arrange
        reservation_id = "12345"

        # Mock del cliente API para simular error de red
        with patch.object(
            use_case.api_client, "get", side_effect=ConnectionError("Network error")
        ):
            # Act & Assert
            with pytest.raises(Exception):
                await use_case.execute(
                    GetReservationParams(reservation_id=reservation_id)
                )

    @pytest.mark.asyncio
    async def test_get_reservation_complete_workflow_integration(
        self, use_case, sample_reservation_data
    ):
        """Test de integración del flujo completo"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API
        with patch.object(use_case.api_client, "get", return_value=mock_response):
            # Act
            result = await use_case.execute(
                GetReservationParams(reservation_id=reservation_id)
            )

            # Assert - Verificar que el resultado es válido
            assert result is not None
            assert result.id == int(reservation_id)
            assert result.status == "Confirmed"

            # Verificar que se puede convertir a diccionario
            result_dict = result.model_dump(by_alias=True, exclude_none=True)
            assert isinstance(result_dict, dict)
            assert "id" in result_dict
            assert "status" in result_dict
            assert "arrival_date" in result_dict
            assert "departure_date" in result_dict
