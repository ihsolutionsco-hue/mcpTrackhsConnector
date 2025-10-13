"""
Tests end-to-end para get_reservation_v2
Valida el funcionamiento completo del sistema MCP
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
    register_get_reservation_v2,
)


class TestGetReservationV2E2E:
    """Tests end-to-end para get_reservation_v2"""

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
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_success(
        self, mock_mcp, api_client, sample_reservation_data
    ):
        """Test E2E exitoso del tool MCP"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API
        with patch.object(api_client, "get", return_value=mock_response):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Verificar que se registró el tool
            mock_mcp.tool.assert_called_once()

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Ejecutar el tool
            result = await tool_func(reservation_id)

            # Assert
            assert result is not None
            assert result["id"] == int(reservation_id)
            assert result["status"] == "Confirmed"
            assert "_embedded" in result
            assert "unit" in result["_embedded"]
            assert "contact" in result["_embedded"]

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_validation_error(self, mock_mcp, api_client):
        """Test E2E con error de validación"""
        # Arrange
        invalid_reservation_id = "0"

        # Act
        register_get_reservation_v2(mock_mcp, api_client)

        # Obtener la función tool registrada
        tool_func = mock_mcp.tool.call_args[0][0]

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await tool_func(invalid_reservation_id)

        assert "Valor inválido para 'reservation_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_api_error(self, mock_mcp, api_client):
        """Test E2E con error de API"""
        # Arrange
        reservation_id = "12345"
        error_response = {
            "type": "https://tools.ietf.org/html/rfc2616/rfc2616-sec10.html",
            "title": "Not Found",
            "status": 404,
            "detail": "Reservation not found",
        }

        # Mock del cliente API para simular error 404
        with patch.object(api_client, "get", side_effect=Exception("404 Not Found")):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Act & Assert
            with pytest.raises(Exception):
                await tool_func(reservation_id)

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_timeout(self, mock_mcp, api_client):
        """Test E2E con timeout"""
        # Arrange
        reservation_id = "12345"

        # Mock del cliente API para simular timeout
        with patch.object(
            api_client, "get", side_effect=asyncio.TimeoutError("Request timeout")
        ):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Act & Assert
            with pytest.raises(Exception):
                await tool_func(reservation_id)

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_network_error(self, mock_mcp, api_client):
        """Test E2E con error de red"""
        # Arrange
        reservation_id = "12345"

        # Mock del cliente API para simular error de red
        with patch.object(
            api_client, "get", side_effect=ConnectionError("Network error")
        ):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Act & Assert
            with pytest.raises(Exception):
                await tool_func(reservation_id)

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_complete_workflow(
        self, mock_mcp, api_client, sample_reservation_data
    ):
        """Test E2E del flujo completo"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API
        with patch.object(api_client, "get", return_value=mock_response):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Verificar que se registró el tool
            mock_mcp.tool.assert_called_once()

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Ejecutar el tool
            result = await tool_func(reservation_id)

            # Assert
            assert result is not None
            assert result["id"] == int(reservation_id)
            assert result["status"] == "Confirmed"
            assert result["arrivalDate"] == "2024-01-15"
            assert result["departureDate"] == "2024-01-20"
            assert result["nights"] == 5
            assert result["currency"] == "USD"
            assert result["unitId"] == 1
            assert result["contactId"] == 1

            # Verificar datos embebidos
            assert "_embedded" in result
            embedded = result["_embedded"]
            assert "unit" in embedded
            assert "contact" in embedded

            # Verificar información financiera
            assert "guestBreakdown" in result
            guest_breakdown = result["guestBreakdown"]
            assert guest_breakdown["grossRent"] == "1000.00"
            assert guest_breakdown["netRent"] == "950.00"
            assert guest_breakdown["grandTotal"] == "1000.00"
            assert guest_breakdown["balance"] == "0.00"

            assert "securityDeposit" in result
            security_deposit = result["securityDeposit"]
            assert security_deposit["required"] == "100.00"
            assert security_deposit["remaining"] == 100

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_error_handling(self, mock_mcp, api_client):
        """Test E2E de manejo de errores"""
        # Arrange
        reservation_id = "12345"

        # Test con diferentes tipos de errores
        error_scenarios = [
            (Exception("API Error"), "Error al obtener la reserva"),
            (ConnectionError("Network Error"), "Error al obtener la reserva"),
            (asyncio.TimeoutError("Timeout"), "Error al obtener la reserva"),
        ]

        for error, expected_message in error_scenarios:
            with patch.object(api_client, "get", side_effect=error):
                # Act
                register_get_reservation_v2(mock_mcp, api_client)

                # Obtener la función tool registrada
                tool_func = mock_mcp.tool.call_args[0][0]

                # Act & Assert
                with pytest.raises(Exception) as exc_info:
                    await tool_func(reservation_id)

                assert expected_message in str(exc_info.value)

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_get_reservation_v2_e2e_performance(
        self, mock_mcp, api_client, sample_reservation_data
    ):
        """Test E2E de rendimiento"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        # Mock del cliente API con delay simulado
        async def mock_get_with_delay(*args, **kwargs):
            await asyncio.sleep(0.1)  # Simular delay de 100ms
            return mock_response

        with patch.object(api_client, "get", side_effect=mock_get_with_delay):
            # Act
            register_get_reservation_v2(mock_mcp, api_client)

            # Obtener la función tool registrada
            tool_func = mock_mcp.tool.call_args[0][0]

            # Medir tiempo de ejecución
            start_time = asyncio.get_event_loop().time()
            result = await tool_func(reservation_id)
            end_time = asyncio.get_event_loop().time()

            execution_time = end_time - start_time

            # Assert
            assert result is not None
            assert execution_time >= 0.1  # Debe tomar al menos 100ms
            assert execution_time < 1.0  # No debe tomar más de 1 segundo
