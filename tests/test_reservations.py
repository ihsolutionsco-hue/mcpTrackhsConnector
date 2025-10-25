import pytest

async def test_search_reservations(mcp_client):
    """Test búsqueda de reservas"""
    result = await mcp_client.call_tool("search_reservations", {
        "page": 0,
        "size": 3,
        "status": "Confirmed"
    })
    assert result is not None
    assert "data" in result or "_embedded" in result

async def test_get_reservation(mcp_client):
    """Test obtener reserva por ID"""
    result = await mcp_client.call_tool("get_reservation", {
        "reservation_id": "12345"
    })
    assert result is not None
