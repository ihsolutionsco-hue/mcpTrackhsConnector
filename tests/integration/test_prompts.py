"""
Tests de integración para prompts MCP V1 y V2
"""

from unittest.mock import Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.prompts import register_all_prompts


class TestPromptsIntegration:
    """Tests de integración para prompts MCP V1 y V2"""

    @pytest.mark.integration
    def test_register_all_prompts(self):
        """Test registro de todos los prompts"""
        # Mock del servidor MCP
        mock_mcp = Mock()
        mock_api_client = Mock()

        # Registrar prompts
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron los prompts
        assert mock_mcp.prompt.called

    @pytest.mark.integration
    def test_prompts_are_registered(self):
        """Test que los prompts están registrados correctamente"""
        # Mock del servidor MCP
        mock_mcp = Mock()
        mock_api_client = Mock()

        # Registrar prompts
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se llamó el decorador @mcp.prompt
        assert mock_mcp.prompt.called
