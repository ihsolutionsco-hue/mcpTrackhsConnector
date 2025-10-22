"""
Tests críticos para la herramienta MCP search_units
"""

from unittest.mock import Mock

import pytest


class TestSearchUnitsCritical:
    """Tests críticos para funcionalidad esencial de search_units"""

    def test_search_units_tool_imports(self):
        """Test: La herramienta search_units se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.mcp.search_units import (
            register_search_units,
        )

        assert register_search_units is not None

    def test_search_units_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.mcp.search_units import (
            register_search_units,
        )

        register_search_units(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_search_units_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.search_units import (
            SearchUnitsUseCase,
        )

        assert SearchUnitsUseCase is not None

    def test_search_units_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.units import Unit

        assert Unit is not None

    def test_search_units_validation(self):
        """Test: Validación de parámetros funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.units import SearchUnitsParams

        # Act & Assert
        # Parámetros válidos (size máximo es 5 según validación)
        valid_params = SearchUnitsParams(page=0, size=5, bedrooms=2, bathrooms=2)
        assert valid_params.page == 0
        assert valid_params.size == 5
        assert valid_params.bedrooms == 2

    def test_search_units_invalid_page(self):
        """Test: Página negativa es rechazada por validación"""
        # Arrange
        from src.trackhs_mcp.domain.entities.units import SearchUnitsParams

        # Act & Assert
        # Pydantic rechaza página negativa
        with pytest.raises(Exception):  # Pydantic validation error
            SearchUnitsParams(page=-1, size=5)  # Página negativa

    def test_search_units_boolean_validation(self):
        """Test: Validación de booleanos funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.units import SearchUnitsParams

        # Act & Assert
        # Parámetros booleanos válidos
        valid_params = SearchUnitsParams(page=0, size=5, pets_friendly=1, is_active=1)
        assert valid_params.pets_friendly == 1
        assert valid_params.is_active == 1
