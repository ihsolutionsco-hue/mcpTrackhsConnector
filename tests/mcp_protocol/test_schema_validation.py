"""
Tests específicos para validar el schema hook y validaciones MCP
Enfoque: Validar que el schema hook funciona correctamente y corrige esquemas
"""

from unittest.mock import Mock, patch

import pytest
from fastmcp import FastMCP


class TestMCPSchemaValidation:
    """Tests para validar el schema hook y validaciones MCP"""

    def test_schema_hook_creation(self):
        """Test: El schema hook se crea correctamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        mcp_server = create_schema_fixed_server("Test Server")

        # Assert
        assert mcp_server is not None
        assert hasattr(mcp_server, "_schema_fixer_hook")

    def test_schema_hook_has_correct_attributes(self):
        """Test: El schema hook tiene los atributos correctos"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        mcp_server = create_schema_fixed_server("Test Server")

        # Assert
        assert hasattr(mcp_server, "_schema_fixer_hook")
        # El schema hook es una instancia de SchemaFixerHook, no una función callable
        assert hasattr(mcp_server._schema_fixer_hook, "apply_hook")
        assert hasattr(mcp_server._schema_fixer_hook, "mcp_server")

    def test_schema_hook_with_different_names(self):
        """Test: El schema hook funciona con diferentes nombres de servidor"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        server1 = create_schema_fixed_server("Server 1")
        server2 = create_schema_fixed_server("Server 2")
        server3 = create_schema_fixed_server("TrackHS MCP Server")

        # Assert
        assert server1 is not None
        assert server2 is not None
        assert server3 is not None
        assert server1 != server2
        assert server2 != server3

    def test_schema_hook_with_none_name(self):
        """Test: El schema hook maneja nombre nulo"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act & Assert
        with pytest.raises(TypeError):
            create_schema_fixed_server(None)

    def test_schema_hook_with_empty_name(self):
        """Test: El schema hook maneja nombre vacío"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act & Assert
        with pytest.raises(ValueError):
            create_schema_fixed_server("")

    def test_schema_hook_multiple_instances(self):
        """Test: Se pueden crear múltiples instancias del schema hook"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        server1 = create_schema_fixed_server("Server 1")
        server2 = create_schema_fixed_server("Server 2")
        server3 = create_schema_fixed_server("Server 3")

        # Assert
        assert server1 is not None
        assert server2 is not None
        assert server3 is not None
        assert server1 != server2
        assert server2 != server3
        assert server1 != server3

    def test_schema_hook_with_mock_fastmcp(self):
        """Test: El schema hook funciona con FastMCP mockeado"""
        # Arrange
        with patch(
            "src.trackhs_mcp.infrastructure.tools.schema_hook.FastMCP"
        ) as mock_fastmcp:
            mock_instance = Mock()
            mock_fastmcp.return_value = mock_instance

            from src.trackhs_mcp.infrastructure.tools.schema_hook import (
                create_schema_fixed_server,
            )

            # Act
            server = create_schema_fixed_server("Test Server")

            # Assert
            assert server is not None
            mock_fastmcp.assert_called_once()

    def test_schema_hook_import_structure(self):
        """Test: Los imports del schema hook funcionan correctamente"""
        # Act & Assert
        try:
            from src.trackhs_mcp.infrastructure.tools.schema_hook import (
                create_schema_fixed_server,
            )

            assert callable(create_schema_fixed_server)
        except ImportError as e:
            pytest.fail(f"Error importando schema hook: {e}")

    def test_schema_hook_with_invalid_parameters(self):
        """Test: El schema hook maneja parámetros inválidos"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act & Assert
        with pytest.raises(TypeError):
            create_schema_fixed_server(123)  # Número en lugar de string

        with pytest.raises(TypeError):
            create_schema_fixed_server([])  # Lista en lugar de string

        with pytest.raises(TypeError):
            create_schema_fixed_server({})  # Diccionario en lugar de string

    def test_schema_hook_consistency(self):
        """Test: El schema hook es consistente entre llamadas"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        server1 = create_schema_fixed_server("Test Server")
        server2 = create_schema_fixed_server("Test Server")

        # Assert
        assert server1 is not None
        assert server2 is not None
        # Deben ser instancias diferentes pero con la misma funcionalidad
        assert hasattr(server1, "_schema_fixer_hook")
        assert hasattr(server2, "_schema_fixer_hook")

    def test_schema_hook_with_special_characters(self):
        """Test: El schema hook maneja caracteres especiales en el nombre"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import (
            create_schema_fixed_server,
        )

        # Act
        server1 = create_schema_fixed_server("Test-Server_1")
        server2 = create_schema_fixed_server("Test Server 2")
        server3 = create_schema_fixed_server("Test@Server#3")

        # Assert
        assert server1 is not None
        assert server2 is not None
        assert server3 is not None
        assert hasattr(server1, "_schema_fixer_hook")
        assert hasattr(server2, "_schema_fixer_hook")
        assert hasattr(server3, "_schema_fixer_hook")
