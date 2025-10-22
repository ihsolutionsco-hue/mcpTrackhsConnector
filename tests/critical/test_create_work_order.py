"""
Tests críticos para la herramienta MCP create_maintenance_work_order
"""

from unittest.mock import Mock

import pytest


class TestCreateWorkOrderCritical:
    """Tests críticos para funcionalidad esencial de create_work_order"""

    def test_create_work_order_tool_imports(self):
        """Test: La herramienta create_work_order se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order import (
            register_create_maintenance_work_order,
        )

        assert register_create_maintenance_work_order is not None

    def test_create_work_order_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.mcp.create_maintenance_work_order import (
            register_create_maintenance_work_order,
        )

        register_create_maintenance_work_order(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_create_work_order_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.create_work_order import (
            CreateWorkOrderUseCase,
        )

        assert CreateWorkOrderUseCase is not None

    def test_create_work_order_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.work_orders import WorkOrder

        assert WorkOrder is not None

    def test_create_work_order_validation(self):
        """Test: Validación de parámetros funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.work_orders import CreateWorkOrderParams

        # Act & Assert
        # Parámetros válidos con todos los campos requeridos
        valid_params = CreateWorkOrderParams(
            summary="Reparar aire acondicionado",
            description="El aire acondicionado no funciona",
            priority=5,
            unit_id=123,
            date_received="2024-01-15",
            status="open",
            estimated_cost=150.00,
            estimated_time=120,
        )
        assert valid_params.summary == "Reparar aire acondicionado"
        assert valid_params.priority == 5

    def test_create_work_order_missing_required_fields(self):
        """Test: Campos requeridos faltantes son rechazados"""
        # Arrange
        from src.trackhs_mcp.domain.entities.work_orders import CreateWorkOrderParams

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            CreateWorkOrderParams(
                # summary faltante - campo requerido
                description="Test description",
                priority=3,
            )

    def test_create_work_order_invalid_priority(self):
        """Test: Prioridad inválida es rechazada"""
        # Arrange
        from src.trackhs_mcp.domain.entities.work_orders import CreateWorkOrderParams

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            CreateWorkOrderParams(
                summary="Test work order",
                description="Test description",
                priority=10,  # Prioridad fuera del rango válido (1-5)
            )
