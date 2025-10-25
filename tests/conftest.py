import pytest
from fastmcp.client import Client

@pytest.fixture
async def mcp_client():
    """Cliente FastMCP para tests"""
    async with Client("src/trackhs_mcp/__main__.py") as client:
        yield client