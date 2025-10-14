"""
Tests de integración para search_reservations V2
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    _is_valid_date_format as v2_is_valid_date_format,
)
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

    def test_v2_date_format_validation(self):
        """Test validación de formato de fecha V2"""
        # Formatos válidos
        assert v2_is_valid_date_format("2024-01-01")
        assert v2_is_valid_date_format("2024-01-01T00:00:00Z")
        assert v2_is_valid_date_format("2024-01-01T00:00:00")

        # Formatos inválidos
        assert not v2_is_valid_date_format("01/01/2024")
        assert not v2_is_valid_date_format("invalid-date")
        assert not v2_is_valid_date_format("")

    def test_register_search_reservations_v2(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v2"""
        # Act
        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()
