import pytest

async def test_search_units(mcp_client):
    """Test búsqueda de unidades"""
    result = await mcp_client.call_tool("search_units", {
        "page": 1,
        "size": 2
    })
    assert result is not None
