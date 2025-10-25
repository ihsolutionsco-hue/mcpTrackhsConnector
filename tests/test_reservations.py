import pytest
from pydantic import ValidationError

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

async def test_search_reservations_validation():
    """Test validación de parámetros de búsqueda"""
    from src.trackhs_mcp.tools.reservations import SearchReservationsRequest
    
    # Test validación de fechas
    with pytest.raises(ValidationError) as exc_info:
        SearchReservationsRequest(
            arrival_start="2024-01-15",
            arrival_end="2024-01-10"  # Fecha final antes que inicial
        )
    assert "arrival_end debe ser posterior a arrival_start" in str(exc_info.value)
    
    # Test validación de formato de fecha
    with pytest.raises(ValidationError) as exc_info:
        SearchReservationsRequest(arrival_start="15-01-2024")  # Formato incorrecto
    assert "Formato de fecha inválido" in str(exc_info.value)
    
    # Test validación de status
    with pytest.raises(ValidationError) as exc_info:
        SearchReservationsRequest(status="InvalidStatus")
    assert "Status inválido" in str(exc_info.value)

async def test_get_reservation_validation():
    """Test validación de ID de reserva"""
    from src.trackhs_mcp.tools.reservations import GetReservationRequest
    
    # Test ID no numérico
    with pytest.raises(ValidationError) as exc_info:
        GetReservationRequest(reservation_id="abc123")
    assert "ID de reserva debe ser numérico" in str(exc_info.value)
    
    # Test ID demasiado largo
    with pytest.raises(ValidationError) as exc_info:
        GetReservationRequest(reservation_id="1" * 25)
    assert "ID de reserva demasiado largo" in str(exc_info.value)

async def test_search_reservations_error_handling(mcp_client):
    """Test manejo de errores en búsqueda de reservas"""
    # Test con parámetros inválidos que deberían fallar en validación
    with pytest.raises(Exception):  # Puede ser ValidationError o API error
        await mcp_client.call_tool("search_reservations", {
            "page": -1,  # Página negativa
            "size": 0    # Tamaño inválido
        })

async def test_get_reservation_error_handling(mcp_client):
    """Test manejo de errores al obtener reserva"""
    # Test con ID inválido
    with pytest.raises(Exception):  # Puede ser ValidationError o API error
        await mcp_client.call_tool("get_reservation", {
            "reservation_id": "invalid_id"
        })
