"""
Tests de integración para middleware de FastMCP
Verificando que ErrorHandlingMiddleware funciona correctamente
"""

from unittest.mock import MagicMock

import pytest
from fastmcp import Client, FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestMiddlewareIntegration:
    """Tests de integración para middleware"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = MagicMock(spec=TrackHSApiClient)
        return client

    @pytest.fixture
    def mcp_server_with_middleware(self, mock_api_client):
        """Servidor MCP con middleware para testing"""
        mcp = FastMCP("Test Server", mask_error_details=True)

        # Agregar middleware de manejo de errores
        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )

        # Registrar herramientas
        register_search_units(mcp, mock_api_client)

        return mcp

    @pytest.mark.asyncio
    async def test_error_handling_middleware(
        self, mcp_server_with_middleware, mock_api_client
    ):
        """Test de que el middleware maneja errores correctamente"""
        # Configurar mock para lanzar excepción
        mock_api_client.search_units.side_effect = Exception("Simulated API Error")

        async with Client(mcp_server_with_middleware) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que el middleware captura y transforma el error
            assert result.is_error
            # El middleware debería transformar el error
            assert "error" in str(result.content).lower()

    @pytest.mark.asyncio
    async def test_middleware_preserves_successful_requests(
        self, mcp_server_with_middleware, mock_api_client
    ):
        """Test de que el middleware no interfiere con requests exitosos"""
        # Mock de respuesta exitosa
        mock_response = {
            "units": [{"id": 1, "name": "Test Unit"}],
            "total": 1,
            "page": 1,
            "size": 25,
            "total_pages": 1,
            "has_next": False,
            "has_previous": False,
        }

        mock_api_client.search_units.return_value = mock_response

        async with Client(mcp_server_with_middleware) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que la respuesta exitosa no es afectada por el middleware
            assert not result.is_error
            data = result.data
            assert data["total"] == 1
            assert len(data["units"]) == 1

    @pytest.mark.asyncio
    async def test_middleware_error_transformation(
        self, mcp_server_with_middleware, mock_api_client
    ):
        """Test de que el middleware transforma errores apropiadamente"""
        # Configurar diferentes tipos de errores
        test_cases = [
            (ValueError("Invalid parameter"), "parameter"),
            (ConnectionError("Network error"), "network"),
            (Exception("Generic error"), "error"),
        ]

        for error, expected_keyword in test_cases:
            mock_api_client.search_units.side_effect = error

            async with Client(mcp_server_with_middleware) as client:
                result = await client.call_tool("search_units", {"page": 1, "size": 25})

                # Verificar que el error es transformado
                assert result.is_error
                error_content = str(result.content)
                assert expected_keyword in error_content.lower()

    @pytest.mark.asyncio
    async def test_middleware_with_tool_error(
        self, mcp_server_with_middleware, mock_api_client
    ):
        """Test de que el middleware respeta ToolError"""
        # Configurar mock para lanzar ToolError
        from fastmcp.exceptions import ToolError

        mock_api_client.search_units.side_effect = ToolError(
            "Custom tool error message"
        )

        async with Client(mcp_server_with_middleware) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que ToolError se preserva
            assert result.is_error
            assert "Custom tool error message" in str(result.content)

    @pytest.mark.asyncio
    async def test_middleware_error_masking(
        self, mcp_server_with_middleware, mock_api_client
    ):
        """Test de que el middleware enmascara detalles internos"""
        # Configurar mock para lanzar excepción con detalles internos
        mock_api_client.search_units.side_effect = Exception(
            "Internal database error: connection failed at line 123"
        )

        async with Client(mcp_server_with_middleware) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que los detalles internos están enmascarados
            assert result.is_error
            error_content = str(result.content)
            # No debería contener detalles específicos de implementación
            assert "line 123" not in error_content
            assert "database" not in error_content.lower()
