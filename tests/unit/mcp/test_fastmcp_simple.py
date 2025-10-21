"""
Tests simples para verificar las mejoras de FastMCP
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Client, FastMCP

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestFastMCPSimple:
    """Tests simples para verificar mejoras de FastMCP"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = MagicMock(spec=TrackHSApiClient)
        return client

    @pytest.fixture
    def mcp_server(self, mock_api_client):
        """Servidor MCP básico para testing"""
        mcp = FastMCP("Test Server")

        # Agregar middleware de error handling
        from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )

        return mcp

    @pytest.mark.asyncio
    async def test_fastmcp_server_creation(self, mcp_server):
        """Test de que el servidor FastMCP se crea correctamente"""
        assert mcp_server is not None
        assert mcp_server.name == "Test Server"

    @pytest.mark.asyncio
    async def test_middleware_configured(self, mcp_server):
        """Test de que el middleware está configurado"""
        # Verificar que el servidor tiene middleware
        assert hasattr(mcp_server, "_middleware")
        assert len(mcp_server._middleware) > 0

    @pytest.mark.asyncio
    async def test_error_handling_middleware(self, mcp_server):
        """Test de que el middleware maneja errores"""

        # Agregar una herramienta que lance error
        @mcp_server.tool
        def test_error_tool() -> str:
            raise Exception("Test error")

        async with Client(mcp_server) as client:
            result = await client.call_tool("test_error_tool", {})

            # Verificar que el error es manejado
            assert result.is_error
            assert "error" in str(result.content).lower()

    @pytest.mark.asyncio
    async def test_tool_with_output_schema(self, mcp_server):
        """Test de herramienta con output schema"""
        from dataclasses import dataclass

        @dataclass
        class TestResult:
            message: str
            success: bool

        @mcp_server.tool
        def test_tool() -> TestResult:
            return TestResult(message="Test successful", success=True)

        async with Client(mcp_server) as client:
            result = await client.call_tool("test_tool", {})

            # Verificar que la respuesta es exitosa
            assert not result.is_error
            data = result.data
            assert data["message"] == "Test successful"
            assert data["success"] is True

    @pytest.mark.asyncio
    async def test_tool_error_handling(self, mcp_server):
        """Test de manejo de ToolError"""
        from fastmcp.exceptions import ToolError

        @mcp_server.tool
        def test_tool_error() -> str:
            raise ToolError("Custom tool error")

        async with Client(mcp_server) as client:
            result = await client.call_tool("test_tool_error", {})

            # Verificar que ToolError se maneja correctamente
            assert result.is_error
            assert "Custom tool error" in str(result.content)

    @pytest.mark.asyncio
    async def test_parameter_validation(self, mcp_server):
        """Test de validación de parámetros"""
        from pydantic import Field

        @mcp_server.tool
        def test_validation_tool(
            page: int = Field(ge=1, le=100), name: str = Field(min_length=1)
        ) -> dict:
            return {"page": page, "name": name}

        async with Client(mcp_server) as client:
            # Test con parámetros válidos
            result = await client.call_tool(
                "test_validation_tool", {"page": 5, "name": "test"}
            )

            assert not result.is_error
            data = result.data
            assert data["page"] == 5
            assert data["name"] == "test"

            # Test con parámetros inválidos
            result = await client.call_tool(
                "test_validation_tool", {"page": -1, "name": "test"}  # Inválido
            )

            assert result.is_error
            assert "validation error" in str(result.content).lower()
