"""
Tests básicos para verificar que las mejoras de FastMCP están funcionando
"""

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware


class TestBasicFunctionality:
    """Tests básicos para verificar funcionalidad core"""

    @pytest.fixture
    def mcp_server(self):
        """Servidor MCP básico para testing"""
        mcp = FastMCP("Test Server")
        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )
        return mcp

    @pytest.mark.asyncio
    async def test_server_creation(self, mcp_server):
        """Test básico de creación de servidor"""
        assert mcp_server is not None
        assert mcp_server.name == "Test Server"

    @pytest.mark.asyncio
    async def test_simple_tool(self, mcp_server):
        """Test de herramienta simple"""

        @mcp_server.tool
        def simple_tool() -> dict:
            return {"message": "Hello", "status": "success"}

        async with Client(mcp_server) as client:
            result = await client.call_tool("simple_tool", {})
            assert not result.is_error
            assert result.data["message"] == "Hello"
            assert result.data["status"] == "success"

    @pytest.mark.asyncio
    async def test_tool_with_parameters(self, mcp_server):
        """Test de herramienta con parámetros"""

        @mcp_server.tool
        def parameter_tool(name: str, count: int) -> dict:
            return {"greeting": f"Hello {name}", "count": count}

        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "parameter_tool", {"name": "World", "count": 5}
            )
            assert not result.is_error
            assert result.data["greeting"] == "Hello World"
            assert result.data["count"] == 5

    @pytest.mark.asyncio
    async def test_error_handling(self, mcp_server):
        """Test de manejo de errores"""

        @mcp_server.tool
        def error_tool() -> str:
            raise Exception("Test error")

        async with Client(mcp_server) as client:
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("error_tool", {})
            assert "Test error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_tool_error(self, mcp_server):
        """Test de ToolError"""

        @mcp_server.tool
        def tool_error() -> str:
            raise ToolError("Custom error")

        async with Client(mcp_server) as client:
            with pytest.raises(ToolError) as excinfo:
                await client.call_tool("tool_error", {})
            assert "Custom error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_parameter_validation(self, mcp_server):
        """Test de validación de parámetros"""
        from pydantic import Field

        @mcp_server.tool
        def validation_tool(value: int = Field(ge=1, le=100)) -> dict:
            return {"value": value}

        async with Client(mcp_server) as client:
            # Test válido
            result = await client.call_tool("validation_tool", {"value": 50})
            assert not result.is_error
            assert result.data["value"] == 50

            # Test inválido
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("validation_tool", {"value": 150})
            assert (
                "validation error" in str(excinfo.value).lower()
                or "maximum" in str(excinfo.value).lower()
            )
