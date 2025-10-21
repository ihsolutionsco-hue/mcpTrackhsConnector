"""
Tests de integración para transporte HTTP
Verifica que el servidor MCP funcione correctamente con transporte HTTP
Nota: FastMCP Cloud maneja automáticamente el transporte HTTP
"""

import asyncio
import json
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestHTTPTransport:
    """Tests para transporte HTTP del servidor MCP"""

    @pytest.fixture
    def mock_config(self):
        """Configuración mock para tests"""
        config = TrackHSConfig(
            api_url="https://api.trackhs.com/api",
            username="test_user",
            password="test_pass",
            timeout=30,
        )
        return config

    @pytest.fixture
    def mock_api_client(self, mock_config):
        """Cliente API mock"""
        with patch(
            "src.trackhs_mcp.infrastructure.adapters.trackhs_api_client.TrackHSApiClient"
        ):
            client = MagicMock()
            client.search_reservations_v2.return_value = {
                "reservations": [],
                "total": 0,
                "page": 1,
                "size": 10,
            }
            return client

    @pytest.fixture
    async def http_client(self):
        """Cliente HTTP para tests"""
        async with httpx.AsyncClient() as client:
            yield client

    @pytest.mark.asyncio
    async def test_health_endpoint(self, http_client):
        """Test que el endpoint de salud responde correctamente"""
        # Este test asume que el servidor está corriendo en localhost:8080
        # En un entorno real, se usaría un servidor de test
        try:
            response = await http_client.get("http://localhost:8080/health")
            assert response.status_code == 200
        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    @pytest.mark.asyncio
    async def test_mcp_tools_list_endpoint(self, http_client):
        """Test que el endpoint MCP responde a tools/list"""
        try:
            payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}

            response = await http_client.post(
                "http://localhost:8080/mcp",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            assert "tools" in data["result"]

            # Verificar que tenemos las 6 tools esperadas
            tools = data["result"]["tools"]
            assert len(tools) == 6

            # Verificar nombres de tools
            tool_names = [tool["name"] for tool in tools]
            expected_tools = [
                "search_reservations_v2",
                "get_reservation_v2",
                "get_folio",
                "search_units",
                "search_amenities",
                "create_maintenance_work_order",
            ]

            for expected_tool in expected_tools:
                assert expected_tool in tool_names

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    @pytest.mark.asyncio
    async def test_mcp_resources_list_endpoint(self, http_client):
        """Test que el endpoint MCP responde a resources/list"""
        try:
            payload = {"jsonrpc": "2.0", "id": 1, "method": "resources/list"}

            response = await http_client.post(
                "http://localhost:8080/mcp",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            assert "resources" in data["result"]

            # Verificar que tenemos los 16 resources esperados
            resources = data["result"]["resources"]
            assert len(resources) == 16

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    @pytest.mark.asyncio
    async def test_mcp_prompts_list_endpoint(self, http_client):
        """Test que el endpoint MCP responde a prompts/list"""
        try:
            payload = {"jsonrpc": "2.0", "id": 1, "method": "prompts/list"}

            response = await http_client.post(
                "http://localhost:8080/mcp",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            assert "prompts" in data["result"]

            # Verificar que tenemos los 3 prompts esperados
            prompts = data["result"]["prompts"]
            assert len(prompts) == 3

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    @pytest.mark.asyncio
    async def test_cors_headers(self, http_client):
        """Test que los headers CORS están configurados correctamente"""
        try:
            # Test OPTIONS request para CORS preflight
            response = await http_client.options(
                "http://localhost:8080/mcp",
                headers={
                    "Origin": "https://elevenlabs.io",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                },
            )

            # Verificar headers CORS
            assert "Access-Control-Allow-Origin" in response.headers
            assert "Access-Control-Allow-Methods" in response.headers
            assert "Access-Control-Allow-Headers" in response.headers

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    @pytest.mark.asyncio
    async def test_invalid_jsonrpc_request(self, http_client):
        """Test manejo de requests JSON-RPC inválidos"""
        try:
            # Request sin method
            payload = {"jsonrpc": "2.0", "id": 1}

            response = await http_client.post(
                "http://localhost:8080/mcp",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            assert response.status_code == 200
            data = response.json()
            assert "error" in data

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")

    def test_http_transport_configuration(self):
        """Test que la configuración HTTP es correcta"""
        # Verificar que el módulo principal puede importarse
        from src.trackhs_mcp.__main__ import main

        # Verificar que main() retorna una instancia de FastMCP
        with (
            patch(
                "src.trackhs_mcp.infrastructure.adapters.config.TrackHSConfig.from_env"
            ) as mock_config,
            patch(
                "src.trackhs_mcp.infrastructure.adapters.trackhs_api_client.TrackHSApiClient"
            ) as mock_client,
        ):

            mock_config.return_value = MagicMock()
            mock_client.return_value = MagicMock()

            mcp = main()
            assert mcp is not None
            assert hasattr(mcp, "run")


@pytest.mark.integration
class TestHTTPTransportIntegration:
    """Tests de integración end-to-end para transporte HTTP"""

    @pytest.mark.asyncio
    async def test_full_mcp_workflow(self):
        """Test workflow completo: listar tools, ejecutar tool, obtener resultado"""
        try:
            async with httpx.AsyncClient() as http_client:
                # 1. Listar tools
                tools_payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}

                tools_response = await http_client.post(
                    "http://localhost:8080/mcp",
                    json=tools_payload,
                    headers={"Content-Type": "application/json"},
                )

                assert tools_response.status_code == 200
                tools_data = tools_response.json()
                assert "result" in tools_data

                # 2. Ejecutar una tool (search_units con parámetros mínimos)
                tool_payload = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "search_units",
                        "arguments": {"page": 1, "size": 5},
                    },
                }

                tool_response = await http_client.post(
                    "http://localhost:8080/mcp",
                    json=tool_payload,
                    headers={"Content-Type": "application/json"},
                )

                assert tool_response.status_code == 200
                tool_data = tool_response.json()

                # Verificar que la respuesta tiene la estructura esperada
                assert "result" in tool_data or "error" in tool_data

        except httpx.ConnectError:
            pytest.skip("Servidor no está corriendo - test de integración")
