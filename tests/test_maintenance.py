import pytest
from pydantic import ValidationError
from datetime import date, timedelta

async def test_create_maintenance_work_order(mcp_client):
    """Test creación de orden de trabajo de mantenimiento"""
    result = await mcp_client.call_tool("create_maintenance_work_order", {
        "summary": "AC not working in bedroom",
        "status": "open",
        "date_received": "2024-01-15",
        "priority": "high",
        "estimated_cost": 150.0,
        "estimated_time": 120,
        "unit_id": 1
    })
    assert result is not None

async def test_create_housekeeping_work_order(mcp_client):
    """Test creación de orden de trabajo de housekeeping"""
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    result = await mcp_client.call_tool("create_housekeeping_work_order", {
        "scheduled_at": tomorrow,
        "status": "pending",
        "unit_id": 1,
        "is_inspection": False
    })
    assert result is not None

async def test_maintenance_work_order_validation():
    """Test validación de parámetros de mantenimiento"""
    from src.trackhs_mcp.tools.maintenance import CreateMaintenanceWORequest
    
    # Test fecha futura
    with pytest.raises(ValidationError) as exc_info:
        CreateMaintenanceWORequest(
            summary="Test issue",
            status="open",
            date_received="2030-01-01",  # Fecha futura
            priority="high",
            estimated_cost=100.0,
            estimated_time=60
        )
    assert "Fecha de recepción no puede ser futura" in str(exc_info.value)
    
    # Test costo demasiado alto
    with pytest.raises(ValidationError) as exc_info:
        CreateMaintenanceWORequest(
            summary="Test issue",
            status="open",
            date_received="2024-01-15",
            priority="high",
            estimated_cost=200000.0,  # Demasiado alto
            estimated_time=60
        )
    assert "Costo estimado demasiado alto" in str(exc_info.value)
    
    # Test tiempo estimado demasiado alto
    with pytest.raises(ValidationError) as exc_info:
        CreateMaintenanceWORequest(
            summary="Test issue",
            status="open",
            date_received="2024-01-15",
            priority="high",
            estimated_cost=100.0,
            estimated_time=2000  # Más de 24 horas
        )
    assert "Tiempo estimado demasiado alto" in str(exc_info.value)

async def test_housekeeping_work_order_validation():
    """Test validación de parámetros de housekeeping"""
    from src.trackhs_mcp.tools.maintenance import CreateHousekeepingWORequest
    
    # Test fecha pasada
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(ValidationError) as exc_info:
        CreateHousekeepingWORequest(
            scheduled_at=yesterday,  # Fecha pasada
            status="pending",
            unit_id=1
        )
    assert "Fecha programada no puede ser pasada" in str(exc_info.value)
    
    # Test fecha demasiado futura
    future_date = (date.today() + timedelta(days=35)).strftime("%Y-%m-%d")
    with pytest.raises(ValidationError) as exc_info:
        CreateHousekeepingWORequest(
            scheduled_at=future_date,  # Más de 30 días
            status="pending",
            unit_id=1
        )
    assert "Fecha programada no puede ser mayor a 30 días" in str(exc_info.value)
    
    # Test ID de unidad demasiado alto
    with pytest.raises(ValidationError) as exc_info:
        CreateHousekeepingWORequest(
            scheduled_at="2024-01-20",
            status="pending",
            unit_id=50000  # Demasiado alto
        )
    assert "ID de unidad demasiado alto" in str(exc_info.value)

async def test_maintenance_error_handling(mcp_client):
    """Test manejo de errores en creación de órdenes de trabajo"""
    # Test con parámetros inválidos
    with pytest.raises(Exception):  # Puede ser ValidationError o API error
        await mcp_client.call_tool("create_maintenance_work_order", {
            "summary": "",  # Resumen vacío
            "status": "invalid_status",  # Status inválido
            "date_received": "invalid_date",  # Fecha inválida
            "priority": "invalid_priority",  # Prioridad inválida
            "estimated_cost": -100,  # Costo negativo
            "estimated_time": 0  # Tiempo inválido
        })

async def test_housekeeping_error_handling(mcp_client):
    """Test manejo de errores en creación de órdenes de housekeeping"""
    # Test con parámetros inválidos
    with pytest.raises(Exception):  # Puede ser ValidationError o API error
        await mcp_client.call_tool("create_housekeeping_work_order", {
            "scheduled_at": "invalid_date",  # Fecha inválida
            "status": "invalid_status",  # Status inválido
            "unit_id": 0,  # ID inválido
            "clean_type_id": 50  # ID de tipo inválido
        })