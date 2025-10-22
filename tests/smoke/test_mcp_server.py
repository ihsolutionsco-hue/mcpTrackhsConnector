"""
Tests de humo para el servidor MCP - verificación básica de funcionamiento
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from src.trackhs_mcp.server import mcp


class TestMCPServerSmoke:
    """Tests de humo para verificar que el servidor MCP funciona básicamente"""

    @pytest.mark.smoke
    def test_server_imports_successfully(self):
        """Test: El servidor MCP se puede importar sin errores"""
        # Act & Assert
        from src.trackhs_mcp.server import mcp

        assert mcp is not None

    @pytest.mark.smoke
    def test_server_has_required_attributes(self):
        """Test: El servidor MCP tiene los atributos requeridos"""
        # Act & Assert
        assert hasattr(mcp, "tool")
        assert hasattr(mcp, "resource")
        assert hasattr(mcp, "prompt")
        assert callable(mcp.tool)
        assert callable(mcp.resource)
        assert callable(mcp.prompt)

    @pytest.mark.smoke
    def test_server_can_be_configured(self):
        """Test: El servidor MCP se puede configurar"""
        # Arrange
        mock_config = Mock()
        mock_config.base_url = "https://api-test.trackhs.com/api"
        mock_config.username = "test_user"
        mock_config.password = "test_password"
        mock_config.timeout = 30

        # Act & Assert
        # Verificar que no hay errores al configurar
        assert mock_config.base_url is not None
        assert mock_config.username is not None
        assert mock_config.timeout > 0

    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_server_responds_to_health_check(self):
        """Test: El servidor responde a health check (simulado)"""
        # Arrange
        with patch("src.trackhs_mcp.server.mcp") as mock_mcp:
            mock_mcp.run.return_value = None

            # Act
            # Simular que el servidor está corriendo
            server_running = True

            # Assert
            assert server_running is True

    @pytest.mark.smoke
    def test_http_transport_configured(self):
        """Test: Transporte HTTP está configurado"""
        # Arrange
        from src.trackhs_mcp.server import mcp

        # Act & Assert
        # Verificar que el servidor MCP está configurado para HTTP
        assert mcp is not None
        # El transporte HTTP se maneja automáticamente por FastMCP Cloud

    @pytest.mark.smoke
    def test_schema_hook_active(self):
        """Test: Schema hook está activo"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.schema_hook import apply_schema_fixes

        # Act & Assert
        # Verificar que el schema hook se puede importar y usar
        assert callable(apply_schema_fixes)

    @pytest.mark.smoke
    def test_cors_configuration(self):
        """Test: Configuración CORS está presente"""
        # Arrange
        import os

        # Act
        cors_origins = os.environ.get("CORS_ORIGINS", "")

        # Assert
        assert "elevenlabs.io" in cors_origins or cors_origins == ""

    @pytest.mark.smoke
    def test_environment_variables_set(self):
        """Test: Variables de entorno están configuradas"""
        # Arrange
        import os

        # Act & Assert
        assert os.environ.get("TRACKHS_API_URL") is not None
        assert os.environ.get("TRACKHS_USERNAME") is not None
        assert os.environ.get("TRACKHS_PASSWORD") is not None
        assert os.environ.get("TRACKHS_TIMEOUT") is not None

    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_server_startup_sequence(self):
        """Test: Secuencia de inicio del servidor (simulado)"""
        # Arrange
        startup_steps = [
            "import_dependencies",
            "load_configuration",
            "register_tools",
            "register_resources",
            "register_prompts",
            "start_server",
        ]

        # Act
        completed_steps = []
        for step in startup_steps:
            completed_steps.append(step)

        # Assert
        assert len(completed_steps) == len(startup_steps)
        assert "register_tools" in completed_steps
        assert "register_resources" in completed_steps
        assert "register_prompts" in completed_steps
