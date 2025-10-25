"""
Tests de red para transportes HTTP/SSE usando mejores prácticas de FastMCP
"""

from unittest.mock import patch

import pytest
from anyio.abc import TaskGroup
from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.utilities.tests import run_server_async


def create_test_server() -> FastMCP:
    """Crear servidor de test para pruebas de red"""
    from trackhs_mcp.server import mcp

    return mcp


@pytest.fixture
async def http_server(task_group: TaskGroup) -> str:
    """Iniciar servidor HTTP en proceso usando task group"""
    server = create_test_server()
    url = await run_server_async(task_group, server, transport="http")
    return url


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_basic(http_server: str):
    """Test básico de transporte HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        # Test ping básico
        try:
            result = await client.ping()
            assert result is True
        except AttributeError:
            # Si no hay método ping, validamos que list_tools funciona
            tools = await client.list_tools()
            assert len(tools) >= 7


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_tools(http_server: str):
    """Test de herramientas a través de transporte HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
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
            assert expected_tool in tool_names


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_tool_execution(http_server: str):
    """Test de ejecución de herramientas a través de HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        # Mock de respuesta de API
        mock_response = {
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "confirmation_number": "CONF123",
                        "guest_name": "John Doe",
                        "guest_email": "john@example.com",
                        "arrival_date": "2024-01-15",
                        "departure_date": "2024-01-20",
                        "status": "confirmed",
                        "unit_id": 100,
                        "total_amount": 500.0,
                        "balance": 0.0,
                    }
                ]
            },
        }

        with patch("src.trackhs_mcp.server.api_client.get", return_value=mock_response):
            result = await client.call_tool(
                "search_reservations", {"page": 0, "size": 10}
            )

            assert result.content[0].text is not None
            response_text = result.content[0].text
            assert "reservations" in response_text or "page" in response_text


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_resources(http_server: str):
    """Test de recursos a través de transporte HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        resources = await client.list_resources()

        # Debe tener al menos el health check
        assert len(resources) >= 1

        # Verificar que el health check está disponible
        resource_uris = [resource.uri for resource in resources]
        assert any("health" in uri for uri in resource_uris)


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_error_handling(http_server: str):
    """Test de manejo de errores a través de HTTP"""
    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        with patch(
            "src.trackhs_mcp.server.api_client.get",
            side_effect=Exception("Network Error"),
        ):
            with pytest.raises(Exception):
                await client.call_tool("search_reservations", {"page": 0, "size": 10})


@pytest.mark.network
@pytest.mark.slow
@pytest.mark.asyncio
async def test_http_transport_performance(http_server: str):
    """Test de performance del transporte HTTP"""
    import time

    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        start_time = time.time()

        # Ejecutar múltiples operaciones
        tools = await client.list_tools()
        resources = await client.list_resources()

        end_time = time.time()
        execution_time = end_time - start_time

        # Debe completarse en menos de 5 segundos
        assert execution_time < 5.0
        assert len(tools) >= 7
        assert len(resources) >= 1


@pytest.mark.network
@pytest.mark.asyncio
async def test_http_transport_concurrent_requests(http_server: str):
    """Test de requests concurrentes a través de HTTP"""
    import asyncio

    async def make_request(client):
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value={"test": "data"}
        ):
            return await client.call_tool("search_reservations", {"page": 0, "size": 1})

    async with Client(transport=StreamableHttpTransport(http_server)) as client:
        # Ejecutar múltiples requests concurrentes
        tasks = [make_request(client) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        # Todos los requests deben completarse exitosamente
        assert len(results) == 5
        for result in results:
            assert result.content[0].text is not None
