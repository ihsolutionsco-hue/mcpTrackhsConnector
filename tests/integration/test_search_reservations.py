"""
Tests de integración para search_reservations V2
"""

from unittest.mock import AsyncMock, Mock

import pytest

# NOTA: _is_valid_date_format fue eliminada después de la estandarización MCP
# La validación ahora se hace con Pydantic Field() + pattern
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
)


class TestSearchReservationsIntegration:
    """Tests de integración para search_reservations V2"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        return Mock()

    # NOTA: Test comentado - _is_valid_date_format fue eliminada después
    # de la estandarización MCP. Validación ahora automática con Pydantic Field()
    # def test_v2_date_format_validation(self):
    #     """Test validación de formato de fecha V2 - DEPRECATED"""
    #     pass

    def test_register_search_reservations_v2(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v2"""
        # Act
        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()
