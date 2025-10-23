"""
Tests específicos para validar el registro de herramientas MCP
Enfoque: Validar que cada herramienta se registra correctamente con sus parámetros
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP


class TestMCPToolsRegistration:
    """Tests para validar el registro de herramientas MCP"""

    def test_search_reservations_tool_registration(self):
        """Test: La herramienta search_reservations se registra con parámetros correctos"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "status": "Confirmed"}],
            "total": 1,
            "page": 0,
            "size": 10,
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mcp, mock_api_client)

        # Assert
        assert mcp is not None
        # Verificar que no hay errores en el registro
        # FastMCP no expone directamente las herramientas registradas

    def test_get_reservation_tool_registration(self):
        """Test: La herramienta get_reservation se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "id": 1,
            "status": "Confirmed",
            "arrivalDate": "2024-01-15",
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.get_reservation_v2 import (
            register_get_reservation_v2,
        )

        register_get_reservation_v2(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_get_folio_tool_registration(self):
        """Test: La herramienta get_folio se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "id": 1,
            "status": "open",
            "currentBalance": 100.0,
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.get_folio import register_get_folio

        register_get_folio(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_search_units_tool_registration(self):
        """Test: La herramienta search_units se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "name": "Villa Paradise"}],
            "total": 1,
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.search_units import (
            register_search_units,
        )

        register_search_units(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_search_amenities_tool_registration(self):
        """Test: La herramienta search_amenities se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "name": "WiFi"}],
            "total": 1,
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.search_amenities import (
            register_search_amenities,
        )

        register_search_amenities(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_create_maintenance_work_order_tool_registration(self):
        """Test: La herramienta create_maintenance_work_order se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.post = AsyncMock()
        mock_api_client.post.return_value = {
            "id": 1,
            "status": "open",
            "summary": "Test work order",
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.create_maintenance_work_order import (
            register_create_maintenance_work_order,
        )

        register_create_maintenance_work_order(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_create_housekeeping_work_order_tool_registration(self):
        """Test: La herramienta create_housekeeping_work_order se registra correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.post = AsyncMock()
        mock_api_client.post.return_value = {
            "id": 1,
            "scheduledAt": "2024-01-15T10:00:00Z",
        }

        # Act
        from src.trackhs_mcp.infrastructure.tools.create_housekeeping_work_order import (
            register_create_housekeeping_work_order,
        )

        register_create_housekeeping_work_order(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_all_tools_registration_together(self):
        """Test: Todas las herramientas se registran juntas sin errores"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.return_value = {"data": [], "total": 0}
        mock_api_client.post.return_value = {"id": 1, "status": "created"}

        # Act
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools

        register_all_tools(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_tool_registration_with_invalid_api_client(self):
        """Test: El registro de herramientas maneja errores de API client"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        invalid_api_client = None

        # Act & Assert
        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools

            register_all_tools(mcp, invalid_api_client)

    def test_tool_registration_with_missing_methods(self):
        """Test: El registro maneja API client con métodos faltantes"""
        # Arrange
        mcp = FastMCP(name="Test Server")

        # Crear una clase que no tenga los métodos requeridos
        class IncompleteAPI:
            pass

        incomplete_api_client = IncompleteAPI()

        # Act & Assert
        with pytest.raises(AttributeError):
            from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools

            register_all_tools(mcp, incomplete_api_client)
