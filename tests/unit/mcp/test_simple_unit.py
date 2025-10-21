"""
Unit tests simples que funcionan - Tests de componente individual
"""

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware


class TestSimpleUnit:
    """Unit tests simples que funcionan"""

    @pytest.fixture
    def mcp_server(self):
        """Servidor MCP básico"""
        mcp = FastMCP("Test Server")
        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )
        return mcp

    @pytest.mark.asyncio
    async def test_server_creation(self, mcp_server):
        """Test creación de servidor"""
        assert mcp_server is not None
        assert mcp_server.name == "Test Server"

    @pytest.mark.asyncio
    async def test_tool_registration(self, mcp_server):
        """Test registro de herramientas"""

        @mcp_server.tool
        def test_tool() -> dict:
            return {"message": "Hello"}

        async with Client(mcp_server) as client:
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]
            assert "test_tool" in tool_names

    @pytest.mark.asyncio
    async def test_tool_execution(self, mcp_server):
        """Test ejecución de herramienta"""

        @mcp_server.tool
        def test_tool() -> dict:
            return {"message": "Hello", "status": "success"}

        async with Client(mcp_server) as client:
            result = await client.call_tool("test_tool", {})
            assert not result.is_error
            assert result.data["message"] == "Hello"
            assert result.data["status"] == "success"

    @pytest.mark.asyncio
    async def test_tool_with_parameters(self, mcp_server):
        """Test herramienta con parámetros"""

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
        """Test manejo de errores"""

        @mcp_server.tool
        def error_tool() -> str:
            raise Exception("Test error")

        async with Client(mcp_server) as client:
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("error_tool", {})
            assert "Test error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_tool_error(self, mcp_server):
        """Test ToolError"""

        @mcp_server.tool
        def tool_error() -> str:
            raise ToolError("Custom error")

        async with Client(mcp_server) as client:
            with pytest.raises(ToolError) as excinfo:
                await client.call_tool("tool_error", {})
            assert "Custom error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_parameter_validation(self, mcp_server):
        """Test validación de parámetros"""
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

    @pytest.mark.asyncio
    async def test_output_schema_dataclass(self, mcp_server):
        """Test output schema con dataclass"""
        from dataclasses import dataclass

        @dataclass
        class TestResult:
            message: str
            success: bool

        @mcp_server.tool
        def dataclass_tool() -> TestResult:
            return TestResult(message="Test successful", success=True)

        async with Client(mcp_server) as client:
            result = await client.call_tool("dataclass_tool", {})
            assert not result.is_error
            data = result.data
            assert data.message == "Test successful"
            assert data.success is True

    @pytest.mark.asyncio
    async def test_middleware_error_transformation(self, mcp_server):
        """Test que el middleware transforma errores"""

        @mcp_server.tool
        def middleware_test_tool() -> str:
            raise ValueError("Test value error")

        async with Client(mcp_server) as client:
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("middleware_test_tool", {})
            # El middleware debería transformar el error
            assert "Test value error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_multiple_tools(self, mcp_server):
        """Test múltiples herramientas"""

        @mcp_server.tool
        def tool1() -> dict:
            return {"tool": "1"}

        @mcp_server.tool
        def tool2() -> dict:
            return {"tool": "2"}

        async with Client(mcp_server) as client:
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]
            assert "tool1" in tool_names
            assert "tool2" in tool_names

            # Test ambas herramientas
            result1 = await client.call_tool("tool1", {})
            assert not result1.is_error
            assert result1.data["tool"] == "1"

            result2 = await client.call_tool("tool2", {})
            assert not result2.is_error
            assert result2.data["tool"] == "2"
