"""
Tests para el protocolo MCP
"""

import pytest
from fastmcp import FastMCP


def test_mcp_server_initialization():
    """Test que el servidor MCP se inicializa correctamente"""
    # Importar el servidor desde el módulo principal
    import sys

    sys.path.append("src")
    from trackhs_mcp.server import mcp

    assert mcp is not None
    assert isinstance(mcp, FastMCP)


def test_mcp_tools_registration():
    """Test que las herramientas MCP están registradas"""
    import sys

    sys.path.append("src")
    from trackhs_mcp.server import mcp

    # Verificar que hay herramientas registradas
    tools = getattr(mcp, "tools", [])
    assert len(tools) > 0

    # Verificar que search_amenities está registrada
    tool_names = [getattr(tool, "name", "") for tool in tools]
    assert "search_amenities" in tool_names


def test_mcp_server_configuration():
    """Test que el servidor MCP está configurado correctamente"""
    import sys

    sys.path.append("src")
    from trackhs_mcp.server import mcp

    # Verificar configuración básica
    assert mcp.strict_input_validation is False
    assert mcp.mask_error_details is True


if __name__ == "__main__":
    pytest.main([__file__])
