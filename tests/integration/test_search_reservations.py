"""
Tests de integración para search_reservations V1 y V2
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
    _is_valid_date_format as v1_is_valid_date_format,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
    register_search_reservations_v1,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    _is_valid_date_format as v2_is_valid_date_format,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
    register_search_reservations_v2,
)
from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError


class TestSearchReservationsIntegration:
    """Tests de integración para search_reservations V1 y V2"""

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

    @pytest.mark.integration
    def test_register_search_reservations_v1(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v1"""
        register_search_reservations_v1(mock_mcp, mock_api_client)
        assert mock_mcp.tool.called

    @pytest.mark.integration
    def test_register_search_reservations_v2(self, mock_mcp, mock_api_client):
        """Test registro de search_reservations_v2"""
        register_search_reservations_v2(mock_mcp, mock_api_client)
        assert mock_mcp.tool.called

    @pytest.mark.integration
    def test_v1_date_format_validation(self):
        """Test validación de formato de fecha V1"""
        # Formatos válidos
        assert v1_is_valid_date_format("2024-01-01")
        assert v1_is_valid_date_format("2024-01-01T00:00:00Z")
        assert v1_is_valid_date_format("2024-01-01T00:00:00")

        # Formatos inválidos
        assert not v1_is_valid_date_format("01/01/2024")
        assert not v1_is_valid_date_format("invalid-date")
        assert not v1_is_valid_date_format("")

    @pytest.mark.integration
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
