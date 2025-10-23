"""
Configuración de fixtures para tests de protocolo MCP
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP


@pytest.fixture
def mock_api_client():
    """Fixture para API client mockeado"""
    mock_client = Mock()
    mock_client.get = AsyncMock()
    mock_client.post = AsyncMock()
    mock_client.get.return_value = {"data": [], "total": 0}
    mock_client.post.return_value = {"id": 1, "status": "created"}
    return mock_client


@pytest.fixture
def mock_api_client_with_data():
    """Fixture para API client mockeado con datos específicos"""
    mock_client = Mock()
    mock_client.get = AsyncMock()
    mock_client.post = AsyncMock()
    mock_client.get.return_value = {
        "data": [{"id": 1, "status": "Confirmed"}],
        "total": 1,
        "page": 0,
        "size": 10,
    }
    mock_client.post.return_value = {
        "id": 1,
        "status": "open",
        "summary": "Test work order",
    }
    return mock_client


@pytest.fixture
def mcp_server():
    """Fixture para servidor MCP básico"""
    return FastMCP(name="Test Server")


@pytest.fixture
def mcp_server_with_schema_hook():
    """Fixture para servidor MCP con schema hook"""
    from src.trackhs_mcp.infrastructure.tools.schema_hook import (
        create_schema_fixed_server,
    )

    return create_schema_fixed_server("Test Server")


@pytest.fixture
def trackhs_config():
    """Fixture para configuración de TrackHS"""
    from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig

    return TrackHSConfig(
        base_url="https://api-test.trackhs.com/api",
        username="test_user",
        password="test_password",
        timeout=30,
    )


@pytest.fixture
def trackhs_api_client(trackhs_config):
    """Fixture para cliente API de TrackHS"""
    from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
        TrackHSApiClient,
    )

    return TrackHSApiClient(trackhs_config)


@pytest.fixture
def complete_mcp_server(trackhs_api_client):
    """Fixture para servidor MCP completo con todos los componentes"""
    mcp = FastMCP(
        name="TrackHS MCP Server",
        mask_error_details=False,
        include_fastmcp_meta=True,
    )

    # Registrar todos los componentes
    from src.trackhs_mcp.infrastructure.prompts.reservations import (
        register_all_prompts,
    )
    from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
    from src.trackhs_mcp.infrastructure.tools.resources import (
        register_all_resources,
    )

    register_all_tools(mcp, trackhs_api_client)
    register_all_resources(mcp, trackhs_api_client)
    register_all_prompts(mcp, trackhs_api_client)

    return mcp
