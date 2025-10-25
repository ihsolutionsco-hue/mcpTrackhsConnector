"""
Tests del protocolo MCP para TrackHS Server
"""

import sys
from pathlib import Path

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# Agregar src al path para importaciones
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


class TestMCPProtocol:
    """Tests del protocolo MCP"""

    @pytest.mark.asyncio
    async def test_mcp_protocol_compliance(self):
        """Test de cumplimiento del protocolo MCP"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de herramientas
            tools = await client.list_tools()
            assert len(tools) > 0, "El servidor debe tener al menos una herramienta"

            # Test de listado de recursos
            resources = await client.list_resources()
            assert len(resources) >= 0, "El servidor debe poder listar recursos"

            # Test de ping (reemplaza initialize en FastMCP 2.0)
            try:
                ping_result = await client.ping()
                assert ping_result is True, "El ping debe ser exitoso"
            except AttributeError:
                # Si no hay método ping, validamos que list_tools funciona
                tools = await client.list_tools()
                assert len(tools) > 0, "El servidor debe tener herramientas"

    @pytest.mark.asyncio
    async def test_server_capabilities(self):
        """Test de capacidades del servidor"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Verificar que el servidor tiene las herramientas esperadas
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]

            expected_tools = [
                "search_reservations",
                "get_reservation",
                "search_units",
                "search_amenities",
                "get_folio",
                "create_maintenance_work_order",
                "create_housekeeping_work_order",
            ]

            for expected_tool in expected_tools:
                assert (
                    expected_tool in tool_names
                ), f"Herramienta {expected_tool} no encontrada"

    @pytest.mark.asyncio
    async def test_health_check_resource(self):
        """Test del recurso de health check"""
        from trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            resources = await client.list_resources()
            resource_uris = [resource.uri for resource in resources]

            # Verificar que el health check está disponible
            health_check_uri = "https://trackhs-mcp.local/health"
            # Convertir AnyUrl a string para comparación
            resource_uri_strings = [str(uri) for uri in resource_uris]
            assert (
                health_check_uri in resource_uri_strings
            ), f"Health check {health_check_uri} no encontrado en {resource_uri_strings}"
