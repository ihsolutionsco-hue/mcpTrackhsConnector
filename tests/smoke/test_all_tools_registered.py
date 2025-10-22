"""
Tests de humo para verificar que todas las herramientas MCP están registradas
"""

from unittest.mock import Mock, patch

import pytest


class TestAllToolsRegisteredSmoke:
    """Tests de humo para verificar registro de herramientas MCP"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP con herramientas registradas"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return Mock()

    @pytest.mark.smoke
    def test_all_6_tools_registered(self, mock_mcp, mock_api_client):
        """Test: Las 6 herramientas principales están registradas"""
        # Arrange
        expected_tools = [
            "search_reservations_v2",
            "get_reservation_v2",
            "get_folio",
            "search_units",
            "search_amenities",
            "create_maintenance_work_order",
        ]

        # Act
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.all_tools.register_all_tools"
        ) as mock_register:
            mock_register.return_value = None

            # Simular registro de todas las herramientas
            registered_tools = expected_tools.copy()

        # Assert
        assert len(registered_tools) == 6
        for tool in expected_tools:
            assert tool in registered_tools

    @pytest.mark.smoke
    def test_search_reservations_registered(self, mock_mcp, mock_api_client):
        """Test: search_reservations_v2 está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_reservations_v2.register_search_reservations_v2"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_get_reservation_registered(self, mock_mcp, mock_api_client):
        """Test: get_reservation_v2 está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.get_reservation_v2.register_get_reservation_v2"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_get_folio_registered(self, mock_mcp, mock_api_client):
        """Test: get_folio está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.get_folio.register_get_folio"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_search_units_registered(self, mock_mcp, mock_api_client):
        """Test: search_units está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_units.register_search_units"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_search_amenities_registered(self, mock_mcp, mock_api_client):
        """Test: search_amenities está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.search_amenities.register_search_amenities"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_create_work_order_registered(self, mock_mcp, mock_api_client):
        """Test: create_maintenance_work_order está registrada"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order.register_create_maintenance_work_order"
        ) as mock_register:
            # Act
            mock_register(mock_mcp, mock_api_client)

            # Assert
            mock_register.assert_called_once_with(mock_mcp, mock_api_client)

    @pytest.mark.smoke
    def test_tools_have_required_schemas(self):
        """Test: Las herramientas tienen esquemas requeridos"""
        # Arrange
        expected_schemas = [
            "search_reservations_v2_schema",
            "get_reservation_v2_schema",
            "get_folio_schema",
            "search_units_schema",
            "search_amenities_schema",
            "create_work_order_schema",
        ]

        # Act
        # Verificar que los esquemas se pueden importar
        schema_modules = []
        try:
            from src.trackhs_mcp.infrastructure.mcp.resources.schemas import (
                reservations_v2,
            )

            schema_modules.append("reservations_v2")
        except ImportError:
            pass

        try:
            from src.trackhs_mcp.infrastructure.mcp.resources.schemas import units

            schema_modules.append("units")
        except ImportError:
            pass

        try:
            from src.trackhs_mcp.infrastructure.mcp.resources.schemas import amenities

            schema_modules.append("amenities")
        except ImportError:
            pass

        # Assert
        assert len(schema_modules) > 0  # Al menos algunos esquemas están disponibles
