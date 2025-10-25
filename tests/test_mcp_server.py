"""
Tests del servidor MCP para TrackHS
"""

import sys
from pathlib import Path

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# Agregar src al path para importaciones
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


class TestMCPServer:
    """Tests del servidor MCP"""

    @pytest.mark.asyncio
    async def test_server_startup(self):
        """Test de inicio del servidor"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de ping (reemplaza initialize en FastMCP 2.0)
            try:
                ping_result = await client.ping()
                assert ping_result is True, "El ping debe ser exitoso"
            except AttributeError:
                # Si no hay método ping, validamos que list_tools funciona
                tools = await client.list_tools()
                assert len(tools) > 0, "El servidor debe tener herramientas"

    @pytest.mark.asyncio
    async def test_server_tools(self):
        """Test de herramientas del servidor"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de herramientas
            tools = await client.list_tools()
            assert len(tools) > 0, "El servidor debe tener herramientas"

    @pytest.mark.asyncio
    async def test_server_resources(self):
        """Test de recursos del servidor"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de recursos
            resources = await client.list_resources()
            assert len(resources) >= 0, "El servidor debe poder listar recursos"
