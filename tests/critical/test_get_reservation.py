"""
Tests críticos para la herramienta MCP get_reservation_v2
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
    register_get_reservation_v2,
)


class TestGetReservationCritical:
    """Tests críticos para funcionalidad esencial de get_reservation"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.fixture
    def setup_tool(self, mock_mcp, mock_api_client):
        """Configuración de la herramienta"""
        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        # Registrar la función
        register_get_reservation_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        return registered_function

    @pytest.mark.asyncio
    async def test_get_reservation_by_id_success(
        self, setup_tool, mock_api_client, sample_reservation_data
    ):
        """Test: Obtener reserva por ID exitosa"""
        # Arrange
        reservation_id = 37165851
        mock_api_client.get.return_value = sample_reservation_data

        # Act
        result = await setup_tool(reservation_id=reservation_id)

        # Assert
        assert result == sample_reservation_data
        assert result["id"] == reservation_id
        mock_api_client.get.assert_called_once_with(
            f"/v2/pms/reservations/{reservation_id}"
        )

    @pytest.mark.asyncio
    async def test_get_reservation_invalid_id(self, setup_tool):
        """Test: ID de reserva inválido"""
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            await setup_tool(reservation_id="invalid-id")

    @pytest.mark.asyncio
    async def test_get_reservation_not_found(self, setup_tool, mock_api_client):
        """Test: Reserva no encontrada (404)"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 404
        mock_api_client.get.side_effect = HTTPStatusError(
            "Not Found", request=Mock(), response=mock_response
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError) as exc_info:
            await setup_tool(reservation_id=999999)

        assert exc_info.value.response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_reservation_api_error(self, setup_tool, mock_api_client):
        """Test: Error de API (500)"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_api_client.get.side_effect = HTTPStatusError(
            "Internal Server Error", request=Mock(), response=mock_response
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError) as exc_info:
            await setup_tool(reservation_id=37165851)

        assert exc_info.value.response.status_code == 500

    @pytest.mark.asyncio
    async def test_get_reservation_unauthorized(self, setup_tool, mock_api_client):
        """Test: Error de autorización (401)"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 401
        mock_api_client.get.side_effect = HTTPStatusError(
            "Unauthorized", request=Mock(), response=mock_response
        )

        # Act & Assert
        with pytest.raises(HTTPStatusError) as exc_info:
            await setup_tool(reservation_id=37165851)

        assert exc_info.value.response.status_code == 401
