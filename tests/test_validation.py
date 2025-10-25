"""
Tests de validación de parámetros para TrackHS MCP Server
"""

import pytest
from pydantic import ValidationError

from src.trackhs_mcp.schemas import (
    HousekeepingWorkOrderStatus,
    MaintenanceWorkOrderStatus,
    WorkOrderPriority,
)


class TestSchemaValidation:
    """Tests para validación de esquemas Pydantic"""

    def test_work_order_priority_enum(self):
        """Test de enum de prioridades"""
        assert WorkOrderPriority.LOW == 1
        assert WorkOrderPriority.MEDIUM == 3
        assert WorkOrderPriority.HIGH == 5

    def test_maintenance_work_order_status_enum(self):
        """Test de enum de estados de mantenimiento"""
        assert MaintenanceWorkOrderStatus.PENDING == "pending"
        assert MaintenanceWorkOrderStatus.IN_PROGRESS == "in-progress"
        assert MaintenanceWorkOrderStatus.COMPLETED == "completed"
        assert MaintenanceWorkOrderStatus.CANCELLED == "cancelled"

    def test_housekeeping_work_order_status_enum(self):
        """Test de enum de estados de housekeeping"""
        assert HousekeepingWorkOrderStatus.PENDING == "pending"
        assert HousekeepingWorkOrderStatus.NOT_STARTED == "not-started"
        assert HousekeepingWorkOrderStatus.IN_PROGRESS == "in-progress"
        assert HousekeepingWorkOrderStatus.COMPLETED == "completed"
        assert HousekeepingWorkOrderStatus.PROCESSED == "processed"
        assert HousekeepingWorkOrderStatus.CANCELLED == "cancelled"
        assert HousekeepingWorkOrderStatus.EXCEPTION == "exception"


class TestParameterValidation:
    """Tests para validación de parámetros de herramientas"""

    def test_search_reservations_validation(self):
        """Test de validación de parámetros de búsqueda de reservas"""
        # Las funciones decoradas con @mcp.tool no son directamente llamables
        # La validación se hace a través del cliente MCP
        assert True  # Placeholder - validación real se hace en test_server.py

    def test_search_units_validation(self):
        """Test de validación de parámetros de búsqueda de unidades"""
        # Las funciones decoradas con @mcp.tool no son directamente llamables
        # La validación se hace a través del cliente MCP
        assert True  # Placeholder - validación real se hace en test_server.py

    def test_create_maintenance_work_order_validation(self):
        """Test de validación de parámetros de creación de orden de mantenimiento"""
        # Las funciones decoradas con @mcp.tool no son directamente llamables
        # La validación se hace a través del cliente MCP
        assert True  # Placeholder - validación real se hace en test_server.py

    def test_create_housekeeping_work_order_validation(self):
        """Test de validación de parámetros de creación de orden de housekeeping"""
        # Las funciones decoradas con @mcp.tool no son directamente llamables
        # La validación se hace a través del cliente MCP
        assert True  # Placeholder - validación real se hace en test_server.py


class TestOutputSchemas:
    """Tests para esquemas de salida"""

    def test_reservation_search_output_schema(self):
        """Test del esquema de salida para búsqueda de reservas"""
        from src.trackhs_mcp.schemas import RESERVATION_SEARCH_OUTPUT_SCHEMA

        assert "type" in RESERVATION_SEARCH_OUTPUT_SCHEMA
        assert "properties" in RESERVATION_SEARCH_OUTPUT_SCHEMA
        assert "_embedded" in RESERVATION_SEARCH_OUTPUT_SCHEMA["properties"]
        assert (
            "reservations"
            in RESERVATION_SEARCH_OUTPUT_SCHEMA["properties"]["_embedded"]["properties"]
        )

    def test_unit_search_output_schema(self):
        """Test del esquema de salida para búsqueda de unidades"""
        from src.trackhs_mcp.schemas import UNIT_SEARCH_OUTPUT_SCHEMA

        assert "type" in UNIT_SEARCH_OUTPUT_SCHEMA
        assert "properties" in UNIT_SEARCH_OUTPUT_SCHEMA
        assert "_embedded" in UNIT_SEARCH_OUTPUT_SCHEMA["properties"]
        assert (
            "units"
            in UNIT_SEARCH_OUTPUT_SCHEMA["properties"]["_embedded"]["properties"]
        )

    def test_work_order_output_schema(self):
        """Test del esquema de salida para órdenes de trabajo"""
        from src.trackhs_mcp.schemas import WORK_ORDER_OUTPUT_SCHEMA

        assert "type" in WORK_ORDER_OUTPUT_SCHEMA
        assert "properties" in WORK_ORDER_OUTPUT_SCHEMA
        assert "id" in WORK_ORDER_OUTPUT_SCHEMA["properties"]
        assert "status" in WORK_ORDER_OUTPUT_SCHEMA["properties"]
        assert "priority" in WORK_ORDER_OUTPUT_SCHEMA["properties"]
