import pytest

async def test_create_maintenance_wo(mcp_client):
    """Test crear orden de trabajo de mantenimiento"""
    result = await mcp_client.call_tool("create_maintenance_work_order", {
        "summary": "AC not working",
        "status": "open",
        "date_received": "2024-01-15",
        "priority": "high",
        "estimated_cost": 150.0,
        "estimated_time": 120
    })
    assert result is not None

async def test_create_housekeeping_wo(mcp_client):
    """Test crear orden de trabajo de housekeeping"""
    result = await mcp_client.call_tool("create_housekeeping_work_order", {
        "scheduled_at": "2024-01-15",
        "status": "pending",
        "unit_id": 101
    })
    assert result is not None
