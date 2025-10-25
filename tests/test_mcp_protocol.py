"""
Tests del protocolo MCP para TrackHS Server
"""

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport


class TestMCPProtocol:
    """Tests del protocolo MCP"""

    @pytest.mark.asyncio
    async def test_mcp_protocol_compliance(self):
        """Test de cumplimiento del protocolo MCP"""
        from src.trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            # Test de listado de herramientas
            tools = await client.list_tools()
            assert len(tools) > 0, "El servidor debe tener al menos una herramienta"

            # Test de listado de recursos
            resources = await client.list_resources()
            assert len(resources) >= 0, "El servidor debe poder listar recursos"

            # Test de inicialización
            initialize_result = await client.initialize()
            assert initialize_result is not None, "La inicialización debe ser exitosa"

    @pytest.mark.asyncio
    async def test_server_capabilities(self):
        """Test de capacidades del servidor"""
        from src.trackhs_mcp.server import mcp

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
        from src.trackhs_mcp.server import mcp

        async with Client(transport=FastMCPTransport(mcp)) as client:
            resources = await client.list_resources()
            resource_uris = [resource.uri for resource in resources]

            # Verificar que el health check está disponible
            health_check_uri = "https://trackhs-mcp.local/health"
            assert (
                health_check_uri in resource_uris
            ), f"Health check {health_check_uri} no encontrado"
