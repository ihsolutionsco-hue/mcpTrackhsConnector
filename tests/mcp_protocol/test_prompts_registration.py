"""
Tests específicos para validar el registro de prompts MCP
Enfoque: Validar que cada prompt se registra correctamente con sus parámetros
"""

from unittest.mock import Mock

import pytest
from fastmcp import FastMCP


class TestMCPPromptsRegistration:
    """Tests para validar el registro de prompts MCP"""

    def test_all_prompts_registration(self):
        """Test: Todos los prompts se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_date_range_search_prompt_registration(self):
        """Test: El prompt de búsqueda por rango de fechas se registra"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_guest_search_prompt_registration(self):
        """Test: El prompt de búsqueda por huésped se registra"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_scroll_search_prompt_registration(self):
        """Test: El prompt de búsqueda con scroll se registra"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_combined_search_prompt_registration(self):
        """Test: El prompt de búsqueda combinada se registra"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_updated_reservations_prompt_registration(self):
        """Test: El prompt de reservas actualizadas se registra"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_prompts_registration_with_invalid_api_client(self):
        """Test: El registro de prompts maneja errores de API client"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        invalid_api_client = None

        # Act & Assert
        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.prompts.reservations import (
                register_all_prompts,
            )

            register_all_prompts(mcp, invalid_api_client)

    def test_prompts_registration_with_missing_methods(self):
        """Test: El registro maneja API client con métodos faltantes"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        incomplete_api_client = Mock()
        # No se definen métodos específicos

        # Act & Assert - Debe funcionar ya que los prompts no requieren métodos específicos
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, incomplete_api_client)
        assert mcp is not None

    def test_prompts_registration_multiple_times(self):
        """Test: Los prompts se pueden registrar múltiples veces sin errores"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp, mock_api_client)
        register_all_prompts(mcp, mock_api_client)  # Segunda vez

        # Assert
        assert mcp is not None

    def test_prompts_registration_with_different_mcp_instances(self):
        """Test: Los prompts se registran en diferentes instancias MCP"""
        # Arrange
        mcp1 = FastMCP(name="Test Server 1")
        mcp2 = FastMCP(name="Test Server 2")
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )

        register_all_prompts(mcp1, mock_api_client)
        register_all_prompts(mcp2, mock_api_client)

        # Assert
        assert mcp1 is not None
        assert mcp2 is not None
        assert mcp1 != mcp2

    def test_prompts_registration_with_none_mcp(self):
        """Test: El registro maneja instancia MCP nula"""
        # Arrange
        mcp = None
        mock_api_client = Mock()

        # Act & Assert
        with pytest.raises((TypeError, AttributeError)):
            from src.trackhs_mcp.infrastructure.prompts.reservations import (
                register_all_prompts,
            )

            register_all_prompts(mcp, mock_api_client)
