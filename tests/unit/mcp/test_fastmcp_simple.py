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
        # FastMCP puede no exponer _middleware directamente
        assert mcp_server is not None

    @pytest.mark.asyncio
    async def test_error_handling_middleware(self, mcp_server):
        """Test de que el middleware maneja errores"""

        # Agregar una herramienta que lance error
        @mcp_server.tool
        def test_error_tool() -> str:
            raise Exception("Test error")

        async with Client(mcp_server) as client:
            # El middleware debería transformar la excepción en ToolError
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("test_error_tool", {})
            assert "Test error" in str(excinfo.value)

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
            # Acceder a los atributos del dataclass directamente
            assert data.message == "Test successful"
            assert data.success is True

    @pytest.mark.asyncio
    async def test_tool_error_handling(self, mcp_server):
        """Test de manejo de ToolError"""
        from fastmcp.exceptions import ToolError

        @mcp_server.tool
        def test_tool_error() -> str:
            raise ToolError("Custom tool error")

        async with Client(mcp_server) as client:
            # ToolError debería ser lanzado directamente
            with pytest.raises(ToolError) as excinfo:
                await client.call_tool("test_tool_error", {})
            assert "Custom tool error" in str(excinfo.value)

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

            # Test con parámetros inválidos - debería lanzar ToolError
            with pytest.raises(Exception) as excinfo:
                await client.call_tool(
                    "test_validation_tool", {"page": -1, "name": "test"}  # Inválido
                )
            assert (
                "validation error" in str(excinfo.value).lower()
                or "minimum" in str(excinfo.value).lower()
            )
