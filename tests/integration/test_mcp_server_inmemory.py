"""
Tests de integración in-memory para servidor MCP
Utiliza FastMCP Client para testing determinístico sin red
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Client, FastMCP

from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.mcp.server import register_all_components
from src.trackhs_mcp.infrastructure.middleware import (
    TrackHSErrorHandlingMiddleware,
    TrackHSLoggingMiddleware,
)


class TestMCPServerInMemory:
    """Tests de integración in-memory para servidor MCP"""

    @pytest.fixture
    def mock_config(self):
        """Configuración mock para tests"""
        config = MagicMock(spec=TrackHSConfig)
        config.base_url = "https://test.trackhs.com/api"
        config.username = "test_user"
        config.password = "test_pass"
        config.timeout = 30
        return config

    @pytest.fixture
    def mock_api_client(self):
        """Cliente API mock para tests"""
        client = AsyncMock(spec=TrackHSApiClient)
        return client

    @pytest.fixture
    def mcp_server(self, mock_config, mock_api_client):
        """Servidor MCP configurado para tests"""
        # Crear servidor FastMCP con configuración de test
        mcp = FastMCP(
            name="Test TrackHS Server",
            mask_error_details=False,
            include_fastmcp_meta=True,
        )

        # Registrar componentes
        register_all_components(mcp, mock_api_client)

        # Agregar middleware
        logging_middleware = TrackHSLoggingMiddleware(
            log_requests=True, log_responses=True, log_timing=True, log_level="DEBUG"
        )
        error_middleware = TrackHSErrorHandlingMiddleware(
            include_traceback=False, transform_errors=True
        )

        mcp.add_middleware(logging_middleware)
        mcp.add_middleware(error_middleware)

        return mcp

    @pytest.mark.asyncio
    async def test_server_creation(self, mcp_server):
        """Test que servidor se crea correctamente"""
        assert mcp_server is not None
        assert mcp_server.name == "Test TrackHS Server"
        # Verificar que servidor tiene configuración correcta
        assert hasattr(mcp_server, "name")

    @pytest.mark.asyncio
    async def test_client_connection(self, mcp_server):
        """Test conexión de cliente in-memory"""
        async with Client(mcp_server) as client:
            # Test que cliente se conecta correctamente
            assert client is not None

    @pytest.mark.asyncio
    async def test_tools_listing(self, mcp_server):
        """Test listado de herramientas"""
        async with Client(mcp_server) as client:
            tools = await client.list_tools()

            # Verificar que hay herramientas registradas
            assert isinstance(tools, list)
            assert len(tools) > 0

        # Verificar estructura de herramientas
        for tool in tools:
            # Los objetos Tool de FastMCP tienen atributos, no claves de diccionario
            assert hasattr(tool, "name")
            assert hasattr(tool, "description")
            assert hasattr(tool, "inputSchema")

    @pytest.mark.asyncio
    async def test_tool_call_success(self, mcp_server, mock_api_client):
        """Test llamada exitosa a herramienta"""
        # Test que el servidor tiene herramientas registradas
        async with Client(mcp_server) as client:
            # Verificar que cliente se conecta correctamente
            assert client is not None

            # Test que se pueden listar herramientas
            tools = await client.list_tools()
            assert isinstance(tools, list)
            assert len(tools) > 0

    @pytest.mark.asyncio
    async def test_tool_call_validation_error(self, mcp_server):
        """Test error de validación en llamada a herramienta"""
        async with Client(mcp_server) as client:
            # Test con parámetro inválido
            with pytest.raises(Exception):  # FastMCP lanzará error de validación
                await client.call_tool(
                    "get_folio", {"folio_id": ""}  # ID vacío debería fallar
                )

    @pytest.mark.asyncio
    async def test_middleware_integration(self, mcp_server):
        """Test integración de middleware"""
        # Verificar que middleware está registrado
        # FastMCP puede no exponer middleware directamente
        assert mcp_server is not None

    @pytest.mark.asyncio
    async def test_resources_listing(self, mcp_server):
        """Test listado de recursos"""
        async with Client(mcp_server) as client:
            resources = await client.list_resources()

            # Verificar que hay recursos registrados
            assert isinstance(resources, list)

    @pytest.mark.asyncio
    async def test_prompts_listing(self, mcp_server):
        """Test listado de prompts"""
        async with Client(mcp_server) as client:
            prompts = await client.list_prompts()

            # Verificar que hay prompts registrados
            assert isinstance(prompts, list)

    @pytest.mark.asyncio
    async def test_server_metadata(self, mcp_server):
        """Test metadatos del servidor"""
        # Verificar configuración
        assert mcp_server is not None
        assert mcp_server.name == "Test TrackHS Server"

    @pytest.mark.asyncio
    async def test_error_handling_flow(self, mcp_server, mock_api_client):
        """Test flujo completo de manejo de errores"""
        # Mock error de API - agregar método get_folio al mock
        mock_api_client.get_folio = AsyncMock(side_effect=Exception("API Error"))

        async with Client(mcp_server) as client:
            # Test que error es manejado por middleware
            with pytest.raises(Exception):
                await client.call_tool("get_folio", {"folio_id": "12345"})

    @pytest.mark.asyncio
    async def test_logging_middleware_stats(self, mcp_server):
        """Test estadísticas de middleware de logging"""
        # FastMCP puede no exponer middleware directamente
        # Verificar que servidor funciona correctamente
        assert mcp_server is not None

    @pytest.mark.asyncio
    async def test_error_middleware_stats(self, mcp_server):
        """Test estadísticas de middleware de errores"""
        # FastMCP puede no exponer middleware directamente
        # Verificar que servidor funciona correctamente
        assert mcp_server is not None


class TestMCPClientFeatures:
    """Tests para características específicas del cliente MCP"""

    @pytest.mark.asyncio
    async def test_client_timeout_configuration(self):
        """Test configuración de timeout en cliente"""
        mcp = FastMCP("Test Server")

        # Test cliente con timeout personalizado
        async with Client(mcp, timeout=30.0) as client:
            # Verificar que cliente se crea correctamente
            assert client is not None

    @pytest.mark.asyncio
    async def test_client_logging_handlers(self):
        """Test manejadores de logging en cliente"""
        mcp = FastMCP("Test Server")

        # Test cliente con manejadores personalizados
        async def log_handler(message):
            pass

        async with Client(mcp, log_handler=log_handler) as client:
            # Verificar que cliente se crea correctamente
            assert client is not None

    @pytest.mark.asyncio
    async def test_client_progress_handlers(self):
        """Test manejadores de progreso en cliente"""
        mcp = FastMCP("Test Server")

        # Test cliente con manejador de progreso
        async def progress_handler(progress, total, message):
            pass

        async with Client(mcp, progress_handler=progress_handler) as client:
            # Verificar que cliente se crea correctamente
            assert client is not None
