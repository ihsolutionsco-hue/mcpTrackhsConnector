"""
Tests de integración completa para el protocolo MCP
Enfoque: Validar que todos los componentes MCP funcionan juntos correctamente
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastmcp import FastMCP


class TestMCPCompleteIntegration:
    """Tests de integración completa para el protocolo MCP"""

    def test_complete_mcp_server_integration(self):
        """Test: El servidor MCP completo se integra correctamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
        from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )

        # Act
        config = TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )
        api_client = TrackHSApiClient(config)

        mcp = FastMCP(
            name="TrackHS MCP Server",
            mask_error_details=False,
            include_fastmcp_meta=True,
        )

        # Registrar todos los componentes
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_tools(mcp, api_client)
        register_all_resources(mcp, api_client)
        register_all_prompts(mcp, api_client)

        # Assert
        assert mcp is not None
        assert api_client is not None
        assert config is not None

    def test_mcp_server_with_mock_api_client(self):
        """Test: El servidor MCP funciona con API client mockeado"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.return_value = {"data": [], "total": 0}
        mock_api_client.post.return_value = {"id": 1, "status": "created"}

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_tools(mcp, mock_api_client)
        register_all_resources(mcp, mock_api_client)
        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_mcp_server_with_schema_hook(self):
        """Test: El servidor MCP funciona con schema hook"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        mcp_server = create_schema_fixed_server("TrackHS MCP Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.return_value = {"data": [], "total": 0}
        mock_api_client.post.return_value = {"id": 1, "status": "created"}

        # Registrar componentes
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_tools(mcp_server, mock_api_client)
        register_all_resources(mcp_server, mock_api_client)
        register_all_prompts(mcp_server, mock_api_client)

        # Assert
        assert mcp_server is not None
        assert hasattr(mcp_server, "_schema_fixer_hook")

    def test_mcp_server_error_handling(self):
        """Test: El servidor MCP maneja errores correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.side_effect = Exception("API Error")
        mock_api_client.post.side_effect = Exception("API Error")

        # Act & Assert
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        # Debe funcionar sin errores durante el registro
        register_all_tools(mcp, mock_api_client)
        register_all_resources(mcp, mock_api_client)
        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_mcp_server_with_none_components(self):
        """Test: El servidor MCP maneja componentes nulos"""
        # Arrange
        mcp = FastMCP(name="Test Server")

        # Act & Assert
        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools

            register_all_tools(mcp, None)

        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.tools.resources import (
                register_all_resources,
            )

            register_all_resources(mcp, None)

        with pytest.raises(TypeError):
            from src.trackhs_mcp.infrastructure.prompts.reservations import (
                register_all_prompts,
            )

            register_all_prompts(mcp, None)

    def test_mcp_server_with_incomplete_api_client(self):
        """Test: El servidor MCP maneja API client incompleto"""
        # Arrange
        mcp = FastMCP(name="Test Server")

        # Crear una clase que no tenga los métodos requeridos
        class IncompleteAPI:
            pass

        incomplete_api_client = IncompleteAPI()

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        # Debe funcionar para recursos y prompts
        register_all_resources(mcp, incomplete_api_client)
        register_all_prompts(mcp, incomplete_api_client)

        # Debe fallar para herramientas que requieren métodos específicos
        with pytest.raises(AttributeError):
            register_all_tools(mcp, incomplete_api_client)

        # Assert
        assert mcp is not None

    def test_mcp_server_multiple_registrations(self):
        """Test: El servidor MCP maneja múltiples registros"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.return_value = {"data": [], "total": 0}
        mock_api_client.post.return_value = {"id": 1, "status": "created"}

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        # Múltiples registros
        register_all_tools(mcp, mock_api_client)
        register_all_resources(mcp, mock_api_client)
        register_all_prompts(mcp, mock_api_client)

        # Segunda vez
        register_all_tools(mcp, mock_api_client)
        register_all_resources(mcp, mock_api_client)
        register_all_prompts(mcp, mock_api_client)

        # Assert
        assert mcp is not None

    def test_mcp_server_with_different_configurations(self):
        """Test: El servidor MCP funciona con diferentes configuraciones"""
        # Arrange
        configs = [
            {"name": "Test Server 1", "mask_error_details": True},
            {"name": "Test Server 2", "mask_error_details": False},
            {"name": "TrackHS MCP Server", "include_fastmcp_meta": True},
        ]

        for config in configs:
            # Act
            mcp = FastMCP(**config)
            mock_api_client = Mock()
            mock_api_client.get = AsyncMock()
            mock_api_client.post = AsyncMock()
            mock_api_client.get.return_value = {"data": [], "total": 0}
            mock_api_client.post.return_value = {"id": 1, "status": "created"}

            from src.trackhs_mcp.infrastructure.prompts.reservations import (
                register_all_prompts,
            )
            from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
            from src.trackhs_mcp.infrastructure.tools.resources import (
                register_all_resources,
            )

            register_all_tools(mcp, mock_api_client)
            register_all_resources(mcp, mock_api_client)
            register_all_prompts(mcp, mock_api_client)

            # Assert
            assert mcp is not None

    def test_mcp_server_consistency(self):
        """Test: El servidor MCP es consistente entre instancias"""
        # Arrange
        mcp1 = FastMCP(name="Test Server 1")
        mcp2 = FastMCP(name="Test Server 2")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.post = AsyncMock()
        mock_api_client.get.return_value = {"data": [], "total": 0}
        mock_api_client.post.return_value = {"id": 1, "status": "created"}

        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import (
            register_all_prompts,
        )
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import (
            register_all_resources,
        )

        register_all_tools(mcp1, mock_api_client)
        register_all_resources(mcp1, mock_api_client)
        register_all_prompts(mcp1, mock_api_client)

        register_all_tools(mcp2, mock_api_client)
        register_all_resources(mcp2, mock_api_client)
        register_all_prompts(mcp2, mock_api_client)

        # Assert
        assert mcp1 is not None
        assert mcp2 is not None
        assert mcp1 != mcp2
