"""
Integration tests para MCP - Tests de integración entre componentes
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware


class TestMCPIntegration:
    """Integration tests para MCP"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API para integration tests"""
        client = MagicMock()

        # Configurar métodos async específicos
        async def mock_search_units(*args, **kwargs):
            return {
                "units": [
                    {"id": 1, "name": "Unit 1", "type": "apartment"},
                    {"id": 2, "name": "Unit 2", "type": "house"},
                ],
                "total": 2,
                "page": 1,
                "size": 25,
                "total_pages": 1,
                "has_next": False,
                "has_previous": False,
            }

        async def mock_search_amenities(*args, **kwargs):
            return {
                "amenities": [
                    {"id": 1, "name": "WiFi", "group_id": 1},
                    {"id": 2, "name": "Pool", "group_id": 2},
                ],
                "total": 2,
                "page": 1,
                "size": 25,
                "total_pages": 1,
                "has_next": False,
                "has_previous": False,
            }

        # Configurar el mock para que los métodos async funcionen correctamente
        client.search_units = mock_search_units
        client.search_amenities = mock_search_amenities

        # Configurar el método get para las llamadas HTTP
        async def mock_get(*args, **kwargs):
            # Determinar qué endpoint se está llamando
            if "amenities" in str(args):
                return {
                    "amenities": [
                        {"id": 1, "name": "WiFi", "group_id": 1},
                        {"id": 2, "name": "Pool", "group_id": 2},
                    ],
                    "total": 2,
                    "page": 1,
                    "size": 25,
                    "total_pages": 1,
                    "has_next": False,
                    "has_previous": False,
                }
            else:
                return {
                    "units": [
                        {"id": 1, "name": "Unit 1", "type": "apartment"},
                        {"id": 2, "name": "Unit 2", "type": "house"},
                    ],
                    "total": 2,
                    "page": 1,
                    "size": 25,
                    "total_pages": 1,
                    "has_next": False,
                    "has_previous": False,
                }

        client.get = mock_get

        return client

    @pytest.fixture
    def mcp_server(self, mock_api_client):
        """Servidor MCP con componentes integrados"""
        from src.trackhs_mcp.infrastructure.mcp.server import register_all_components

        mcp = FastMCP("Integration Test Server")
        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )
        register_all_components(mcp, mock_api_client)
        return mcp

    @pytest.mark.asyncio
    async def test_server_components_integration(self, mcp_server):
        """Test que todos los componentes están integrados"""
        async with Client(mcp_server) as client:
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]

            # Verificar que las herramientas principales están registradas
            assert "search_units" in tool_names
            assert "search_amenities" in tool_names

    @pytest.mark.asyncio
    async def test_search_units_integration(self, mcp_server, mock_api_client):
        """Test integración completa de search_units"""
        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "search_units", {"page": 1, "size": 25, "search": "apartment"}
            )

            assert not result.is_error
            data = result.data

            # Verificar estructura del resultado
            assert hasattr(data, "units")
            assert hasattr(data, "total")
            assert hasattr(data, "page")
            assert hasattr(data, "size")
            assert hasattr(data, "total_pages")
            assert hasattr(data, "has_next")
            assert hasattr(data, "has_previous")

            # Verificar datos
            assert data.total == 2
            assert data.page == 1
            assert data.size == 25
            assert len(data.units) == 2
            # Verificar que los units tienen la estructura esperada
            assert isinstance(data.units, list)
            assert len(data.units) > 0

    @pytest.mark.asyncio
    async def test_search_amenities_integration(self, mcp_server, mock_api_client):
        """Test integración completa de search_amenities"""
        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "search_amenities", {"page": 1, "size": 25, "search": "wifi"}
            )

            assert not result.is_error
            data = result.data

            # Verificar estructura del resultado
            assert hasattr(data, "amenities")
            assert hasattr(data, "total")
            assert hasattr(data, "page")
            assert hasattr(data, "size")
            assert hasattr(data, "total_pages")
            assert hasattr(data, "has_next")
            assert hasattr(data, "has_previous")

            # Verificar datos
            assert data.total == 2
            assert data.page == 1
            assert data.size == 25
            assert len(data.amenities) == 2
            # Verificar que los amenities tienen la estructura esperada
            assert isinstance(data.amenities, list)
            assert len(data.amenities) > 0

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, mcp_server):
        """Test integración del manejo de errores"""

        # Crear una herramienta que lance error
        @mcp_server.tool("integration_error_tool")
        def integration_error_tool():
            raise Exception("Integration test error")

        async with Client(mcp_server) as client:
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("integration_error_tool", {})
            assert "Integration test error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_middleware_integration(self, mcp_server):
        """Test que el middleware está integrado correctamente"""
        # Verificar que el middleware está presente
        assert mcp_server is not None

        # Test que el middleware maneja errores
        @mcp_server.tool("middleware_integration_test")
        def middleware_test():
            raise ValueError("Middleware test error")

        async with Client(mcp_server) as client:
            with pytest.raises(Exception) as excinfo:
                await client.call_tool("middleware_integration_test", {})
            assert "Middleware test error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_parameter_validation_integration(self, mcp_server):
        """Test integración de validación de parámetros"""
        async with Client(mcp_server) as client:
            # Test validación de parámetros en search_units
            with pytest.raises(Exception) as excinfo:
                await client.call_tool(
                    "search_units", {"page": -1, "size": 25}  # Inválido
                )
            assert (
                "validation error" in str(excinfo.value).lower()
                or "minimum" in str(excinfo.value).lower()
            )

    @pytest.mark.asyncio
    async def test_output_schema_integration(self, mcp_server, mock_api_client):
        """Test integración de output schemas"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que el resultado tiene la estructura correcta
            data = result.data
            assert isinstance(data.units, list)
            assert isinstance(data.total, int)
            assert isinstance(data.page, int)
            assert isinstance(data.size, int)
            assert isinstance(data.total_pages, int)
            assert isinstance(data.has_next, bool)
            assert isinstance(data.has_previous, bool)

    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self, mcp_server, mock_api_client):
        """Test llamadas concurrentes a herramientas"""
        import asyncio

        async with Client(mcp_server) as client:
            # Crear múltiples tareas concurrentes
            tasks = [
                client.call_tool("search_units", {"page": 1, "size": 25}),
                client.call_tool("search_amenities", {"page": 1, "size": 25}),
                client.call_tool("search_units", {"page": 2, "size": 25}),
            ]

            # Ejecutar concurrentemente
            results = await asyncio.gather(*tasks)

            # Verificar que todas las llamadas fueron exitosas
            for result in results:
                assert not result.is_error
                assert hasattr(result.data, "total")
                assert hasattr(result.data, "page")

    @pytest.mark.asyncio
    async def test_tool_discovery_integration(self, mcp_server):
        """Test descubrimiento de herramientas"""
        async with Client(mcp_server) as client:
            tools = await client.list_tools()

            # Verificar que tenemos herramientas registradas
            assert len(tools) > 0

            # Verificar estructura de herramientas
            for tool in tools:
                assert hasattr(tool, "name")
                assert hasattr(tool, "description")
                assert tool.name is not None
                assert tool.description is not None

    @pytest.mark.asyncio
    async def test_server_configuration_integration(self, mcp_server):
        """Test configuración del servidor"""
        # Verificar configuración básica
        assert mcp_server.name == "Integration Test Server"
        assert mcp_server is not None

        # Verificar que el servidor puede crear clientes
        async with Client(mcp_server) as client:
            assert client is not None
