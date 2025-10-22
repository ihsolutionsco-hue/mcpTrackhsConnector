"""
Tests críticos para la herramienta MCP search_amenities
"""

from unittest.mock import Mock

import pytest


class TestSearchAmenitiesCritical:
    """Tests críticos para funcionalidad esencial de search_amenities"""

    def test_search_amenities_tool_imports(self):
        """Test: La herramienta search_amenities se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
            register_search_amenities,
        )

        assert register_search_amenities is not None

    def test_search_amenities_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
            register_search_amenities,
        )

        register_search_amenities(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_search_amenities_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.search_amenities import (
            SearchAmenitiesUseCase,
        )

        assert SearchAmenitiesUseCase is not None

    def test_search_amenities_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.amenities import UnitAmenity

        assert UnitAmenity is not None

    def test_search_amenities_validation(self):
        """Test: Validación de parámetros funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.amenities import SearchAmenitiesParams

        # Act & Assert
        # Parámetros válidos (size máximo es 5 según validación)
        valid_params = SearchAmenitiesParams(
            page=0, size=5, search="wifi", category="Internet"
        )
        assert valid_params.page == 0
        assert valid_params.size == 5
        assert valid_params.search == "wifi"

    def test_search_amenities_invalid_page(self):
        """Test: Página inválida es rechazada"""
        # Arrange
        from src.trackhs_mcp.domain.entities.amenities import SearchAmenitiesParams

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            SearchAmenitiesParams(page=-1, size=25)  # Página negativa
