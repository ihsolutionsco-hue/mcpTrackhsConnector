"""
Tests unitarios para get_reservation_v2 tool MCP
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
    register_get_reservation_v2,
)
from trackhs_mcp.infrastructure.utils.error_handling import TrackHSError


class TestGetReservationV2Tool:
    """Tests para get_reservation_v2 tool MCP"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    def test_register_get_reservation_v2(self, mock_mcp, mock_api_client):
        """Test registro de la herramienta"""
        # Act
        register_get_reservation_v2(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    @pytest.mark.asyncio
    async def test_tool_success(self, mock_api_client, sample_reservation_data):
        """Test ejecución exitosa del tool"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.return_value = Mock(
                model_dump=Mock(return_value=mock_response)
            )
            mock_use_case_class.return_value = mock_use_case

            # Act
            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            # Crear mock MCP que capture la función tool
            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Ejecutar la función tool
            result = await tool_func(reservation_id)

            # Assert
            assert result == mock_response
            mock_use_case.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_tool_invalid_id_zero(self, mock_api_client):
        """Test con ID inválido (cero)"""
        # Arrange
        reservation_id = "0"

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ):
            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Valor inválido para 'reservation_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_tool_invalid_id_negative(self, mock_api_client):
        """Test con ID inválido (negativo)"""
        # Arrange
        reservation_id = "-1"

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ):
            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Valor inválido para 'reservation_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_tool_api_error_401(self, mock_api_client):
        """Test error 401 (no autorizado)"""
        # Arrange
        reservation_id = "12345"
        from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        error = ValidationError("No autorizado", "auth")
        error.status_code = 401

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.side_effect = error
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "No autorizado" in str(exc_info.value)
            assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_tool_api_error_403(self, mock_api_client):
        """Test error 403 (prohibido)"""
        # Arrange
        reservation_id = "12345"
        from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        error = ValidationError("Prohibido", "permissions")
        error.status_code = 403

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.side_effect = error
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Prohibido" in str(exc_info.value)
            assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_tool_api_error_404(self, mock_api_client):
        """Test error 404 (no encontrado)"""
        # Arrange
        reservation_id = "12345"
        from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        error = ValidationError("No encontrado", "reservation_id")
        error.status_code = 404

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.side_effect = error
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Reserva no encontrada" in str(exc_info.value)
            assert f"No existe una reserva con ID {reservation_id}" in str(
                exc_info.value
            )

    @pytest.mark.asyncio
    async def test_tool_api_error_500(self, mock_api_client):
        """Test error 500 (error interno)"""
        # Arrange
        reservation_id = "12345"
        from trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        error = ValidationError("Error interno", "api")
        error.status_code = 500

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.side_effect = error
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Error interno del servidor" in str(exc_info.value)
            assert "API de TrackHS está temporalmente no disponible" in str(
                exc_info.value
            )

    @pytest.mark.asyncio
    async def test_tool_generic_error(self, mock_api_client):
        """Test error genérico"""
        # Arrange
        reservation_id = "12345"

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.side_effect = Exception("Error de conexión")
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act & Assert
            with pytest.raises(TrackHSError) as exc_info:
                await tool_func(reservation_id)

            assert "Error al obtener la reserva" in str(exc_info.value)
            assert "Error de conexión" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_tool_with_complete_data(
        self, mock_api_client, sample_reservation_data
    ):
        """Test con datos completos incluyendo embebidos"""
        # Arrange
        reservation_id = "12345"
        mock_response = sample_reservation_data.copy()
        mock_response["id"] = int(reservation_id)

        with patch(
            "trackhs_mcp.infrastructure.mcp.get_reservation_v2.GetReservationUseCase"
        ) as mock_use_case_class:
            mock_use_case = AsyncMock()
            mock_use_case.execute.return_value = Mock(
                model_dump=Mock(return_value=mock_response)
            )
            mock_use_case_class.return_value = mock_use_case

            from trackhs_mcp.infrastructure.mcp.get_reservation_v2 import (
                register_get_reservation_v2,
            )

            mock_mcp = Mock()
            tool_func = None

            def capture_tool(name=None):
                def decorator(func):
                    nonlocal tool_func
                    tool_func = func
                    return func

                return decorator

            mock_mcp.tool = capture_tool

            register_get_reservation_v2(mock_mcp, mock_api_client)

            # Act
            result = await tool_func(reservation_id)

            # Assert
            assert result == mock_response
            assert result["id"] == int(reservation_id)
            assert result["status"] == "Confirmed"
            assert "_embedded" in result
            assert "unit" in result["_embedded"]
            assert "contact" in result["_embedded"]
            # Verificar que los datos embebidos están presentes
            assert len(result["_embedded"]) >= 2
            mock_use_case.execute.assert_called_once()
