"""
Tests de validación para search_reservations V1 y V2
Valida las correcciones implementadas según documentación API V1 y V2
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
    register_search_reservations_v1,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
)
from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError


class TestSearchReservationsValidation:
    """Tests de validación para search_reservations V1 y V2"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.mark.unit
    def test_register_search_reservations_v1(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v1"""
        register_search_reservations_v1(mock_mcp, mock_api_client)
        assert mock_mcp.tool.called

    @pytest.mark.unit
    def test_register_search_reservations_v2(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v2"""
        register_search_reservations_v2(mock_mcp, mock_api_client)
        assert mock_mcp.tool.called
