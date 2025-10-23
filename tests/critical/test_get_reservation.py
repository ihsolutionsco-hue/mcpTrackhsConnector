"""
Tests críticos para la herramienta MCP get_reservation_v2
"""

from unittest.mock import Mock

import pytest


class TestGetReservationCritical:
    """Tests críticos para funcionalidad esencial de get_reservation"""

    def test_get_reservation_tool_imports(self):
        """Test: La herramienta get_reservation se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.tools.get_reservation_v2 import (
            register_get_reservation_v2,
        )

        assert register_get_reservation_v2 is not None

    def test_get_reservation_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.tools.get_reservation_v2 import (
            register_get_reservation_v2,
        )

        register_get_reservation_v2(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_get_reservation_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.get_reservation import (
            GetReservationUseCase,
        )

        assert GetReservationUseCase is not None

    def test_get_reservation_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.reservations import Reservation

        assert Reservation is not None

    def test_get_reservation_validation(self):
        """Test: Validación de ID funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.reservations import GetReservationParams

        # Act & Assert
        # ID válido
        valid_params = GetReservationParams(reservation_id=37165851)
        assert valid_params.reservation_id == 37165851

    def test_get_reservation_invalid_id(self):
        """Test: ID inválido es rechazado"""
        # Arrange
        from src.trackhs_mcp.domain.entities.reservations import GetReservationParams

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            GetReservationParams(reservation_id="invalid-id")
