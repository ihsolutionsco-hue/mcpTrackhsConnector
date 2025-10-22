"""
Tests críticos para la herramienta MCP create_maintenance_work_order
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order import (
    register_create_maintenance_work_order,
)


class TestCreateWorkOrderCritical:
    """Tests críticos para funcionalidad esencial de create_work_order"""

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
        register_create_maintenance_work_order(mock_mcp, mock_api_client)

        # Obtener la función registrada
        return registered_function

    @pytest.mark.asyncio
    async def test_create_work_order_success(
        self, setup_tool, mock_api_client, sample_work_order_data
    ):
        """Test: Creación de orden de trabajo exitosa"""
        # Arrange
        work_order_data = {
            "summary": "Reparar aire acondicionado en unidad 101",
            "description": "El aire acondicionado de la unidad 101 no está funcionando correctamente",
            "priority": 5,
            "unitId": 123,
            "reservationId": 37165851,
            "source": "Guest Request",
            "sourceName": "Juan Pérez",
            "sourcePhone": "+1234567890",
        }
        mock_api_client.post.return_value = sample_work_order_data

        # Act
        result = await setup_tool(**work_order_data)

        # Assert
        assert result == sample_work_order_data
        assert result["id"] == 12345
        mock_api_client.post.assert_called_once_with(
            "/pms/maintenance/work-orders", json=work_order_data
        )

    @pytest.mark.asyncio
    async def test_create_work_order_missing_required_fields(self, setup_tool):
        """Test: Campos requeridos faltantes"""
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            await setup_tool(
                # summary faltante - campo requerido
                description="Test description",
                priority=3,
            )

    @pytest.mark.asyncio
    async def test_create_work_order_invalid_priority(self, setup_tool):
        """Test: Prioridad inválida"""
        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            await setup_tool(
                summary="Test work order",
                description="Test description",
                priority=10,  # Prioridad fuera del rango válido (1-5)
            )

    @pytest.mark.asyncio
    async def test_create_work_order_api_error(self, setup_tool, mock_api_client):
        """Test: Error de API (500)"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_api_client.post.side_effect = HTTPStatusError(
            "Internal Server Error", request=Mock(), response=mock_response
        )

        work_order_data = {
            "summary": "Test work order",
            "description": "Test description",
            "priority": 3,
        }

        # Act & Assert
        with pytest.raises(HTTPStatusError) as exc_info:
            await setup_tool(**work_order_data)

        assert exc_info.value.response.status_code == 500

    @pytest.mark.asyncio
    async def test_create_work_order_unauthorized(self, setup_tool, mock_api_client):
        """Test: Error de autorización (401)"""
        # Arrange
        from httpx import HTTPStatusError

        mock_response = Mock()
        mock_response.status_code = 401
        mock_api_client.post.side_effect = HTTPStatusError(
            "Unauthorized", request=Mock(), response=mock_response
        )

        work_order_data = {
            "summary": "Test work order",
            "description": "Test description",
            "priority": 3,
        }

        # Act & Assert
        with pytest.raises(HTTPStatusError) as exc_info:
            await setup_tool(**work_order_data)

        assert exc_info.value.response.status_code == 401
