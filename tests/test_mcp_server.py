"""
Tests del servidor MCP para TrackHS
"""

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport


class TestMCPServer:
    """Tests del servidor MCP"""

    @pytest.mark.asyncio
    async def test_server_startup(self):
        """Test de inicio del servidor"""
        from src.trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de inicialización
            initialize_result = await client.initialize()
            assert initialize_result is not None, "La inicialización debe ser exitosa"

    @pytest.mark.asyncio
    async def test_server_tools(self):
        """Test de herramientas del servidor"""
        from src.trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de herramientas
            tools = await client.list_tools()
            assert len(tools) > 0, "El servidor debe tener herramientas"

    @pytest.mark.asyncio
    async def test_server_resources(self):
        """Test de recursos del servidor"""
        from src.trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de recursos
            resources = await client.list_resources()
            assert len(resources) >= 0, "El servidor debe poder listar recursos"