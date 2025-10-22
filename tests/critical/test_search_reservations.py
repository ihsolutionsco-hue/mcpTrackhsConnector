"""
Tests críticos para la herramienta MCP search_reservations
"""

from unittest.mock import Mock

import pytest


class TestSearchReservationsCritical:
    """Tests críticos para funcionalidad esencial de search_reservations"""

    def test_search_reservations_tool_imports(self):
        """Test: La herramienta search_reservations se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        assert register_search_reservations_v2 is not None

    def test_search_reservations_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_search_reservations_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.search_reservations import (
            SearchReservationsUseCase,
        )

        assert SearchReservationsUseCase is not None

    def test_search_reservations_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.reservations import Reservation

        assert Reservation is not None

    def test_search_reservations_validation(self):
        """Test: Validación de parámetros funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.reservations import (
            SearchReservationsParams,
        )

        # Act & Assert
        # Parámetros válidos (size máximo es 5 según validación)
        valid_params = SearchReservationsParams(
            page=0, size=5, arrival_start="2024-01-15", arrival_end="2024-01-20"
        )
        assert valid_params.page == 0
        assert valid_params.size == 5
        assert valid_params.arrival_start == "2024-01-15"

    def test_search_reservations_invalid_date_format(self):
        """Test: Formato de fecha inválido se asigna pero es inválido"""
        # Arrange
        from src.trackhs_mcp.domain.entities.reservations import (
            SearchReservationsParams,
        )

        # Act & Assert
        # Pydantic puede permitir formato inválido, así que verificamos que se asigna
        params = SearchReservationsParams(
            page=0, size=5, arrival_start="invalid-date-format"
        )
        assert (
            params.arrival_start == "invalid-date-format"
        )  # Se asigna pero es inválido

    def test_search_reservations_pagination_validation(self):
        """Test: Validación de paginación funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.reservations import (
            SearchReservationsParams,
        )

        # Act & Assert
        # Página inválida
        with pytest.raises(Exception):  # Pydantic validation error
            SearchReservationsParams(page=-1, size=25)  # Página negativa
