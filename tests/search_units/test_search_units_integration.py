"""
Tests de integración para search_units
Prueba la integración completa con el servidor MCP y middleware
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Agregar src al path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

from trackhs_mcp.exceptions import APIError, AuthenticationError, ConnectionError
from trackhs_mcp.server import mcp


class TestSearchUnitsIntegration:
    """Tests de integración para search_units"""

    @pytest.fixture
    async def mcp_client(self):
        """Cliente MCP para tests de integración"""
        transport = FastMCPTransport(mcp)
        client = Client(transport=transport)
        await client.__aenter__()
        try:
            yield client
        finally:
            await client.__aexit__(None, None, None)

    @pytest.fixture
    def mock_api_response(self):
        """Respuesta mock de la API para tests"""
        return {
            "page": 1,
            "page_count": 2,
            "page_size": 10,
            "total_items": 15,
            "_embedded": {
                "units": [
                    {
                        "id": 100,
                        "name": "Casa de Playa",
                        "code": "CP001",
                        "bedrooms": 3,
                        "bathrooms": 2,
                        "max_occupancy": 6,
                        "area": 120.5,
                        "address": "123 Beach St, Miami, FL",
                        "amenities": ["WiFi", "Pool", "Parking", "AC"],
                        "is_active": True,
                        "is_bookable": True,
                        "description": "Hermosa casa frente al mar",
                        "rules": {
                            "check_in_time": "15:00",
                            "check_out_time": "11:00",
                            "minimum_nights": 2,
                        },
                    },
                    {
                        "id": 101,
                        "name": "Penthouse Suite",
                        "code": "PS002",
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "max_occupancy": 4,
                        "area": 95.0,
                        "address": "456 Downtown Ave, Miami, FL",
                        "amenities": ["WiFi", "Gym", "Concierge", "Valet"],
                        "is_active": True,
                        "is_bookable": True,
                        "description": "Lujoso penthouse en el centro",
                        "rules": {
                            "check_in_time": "16:00",
                            "check_out_time": "12:00",
                            "minimum_nights": 1,
                        },
                    },
                ]
            },
            "_links": {
                "self": {"href": "/pms/units?page=1&size=10"},
                "first": {"href": "/pms/units?page=1&size=10"},
                "last": {"href": "/pms/units?page=2&size=10"},
                "next": {"href": "/pms/units?page=2&size=10"},
            },
        }

    @pytest.mark.asyncio
    async def test_search_units_basic_integration(self, mcp_client, mock_api_response):
        """Test de integración básica de search_units"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_api_response

            # Llamar a la herramienta a través del cliente MCP
            result = await mcp_client.call_tool(name="search_units", arguments={})

            # Verificar que se llamó al cliente API
            mock_client.get.assert_called_once_with(
                "pms/units", {"page": 1, "size": 10}
            )

            # Verificar respuesta
            assert result.data is not None
            assert result.data["page"] == 1
            assert result.data["total_items"] == 15
            assert len(result.data["_embedded"]["units"]) == 2

    @pytest.mark.asyncio
    async def test_search_units_with_filters_integration(
        self, mcp_client, mock_api_response
    ):
        """Test de integración con filtros"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_api_response

            result = await mcp_client.call_tool(
                name="search_units",
                arguments={
                    "page": 2,
                    "size": 5,
                    "search": "penthouse",
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "is_active": 1,
                    "is_bookable": 1,
                },
            )

            # Verificar parámetros enviados
            expected_params = {
                "page": 2,
                "size": 5,
                "search": "penthouse",
                "bedrooms": 2,
                "bathrooms": 2,
                "is_active": 1,
                "is_bookable": 1,
            }
            mock_client.get.assert_called_once_with("pms/units", expected_params)

            assert result.data is not None
            assert result.data["page"] == 1  # Respuesta mock

    @pytest.mark.asyncio
    async def test_search_units_error_handling_integration(self, mcp_client):
        """Test de manejo de errores en integración"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.side_effect = AuthenticationError("Credenciales inválidas")

            with pytest.raises(Exception):  # FastMCP convierte excepciones
                await mcp_client.call_tool(name="search_units", arguments={})

    @pytest.mark.asyncio
    async def test_search_units_middleware_integration(
        self, mcp_client, mock_api_response
    ):
        """Test de integración con middleware"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_api_response

            # El middleware debería procesar este request
            result = await mcp_client.call_tool(
                name="search_units", arguments={"search": "beach"}
            )

            assert result.data is not None
            # El middleware debería haber registrado métricas y logs

    @pytest.mark.asyncio
    async def test_search_units_parameter_validation_integration(self, mcp_client):
        """Test de validación de parámetros en integración"""
        # Test con parámetros inválidos
        with pytest.raises(Exception):  # FastMCP maneja ValidationError
            await mcp_client.call_tool(
                name="search_units",
                arguments={
                    "page": 0,  # Inválido: debe ser >= 1
                    "size": 30,  # Inválido: debe ser <= 25
                },
            )

    @pytest.mark.asyncio
    async def test_search_units_empty_response_integration(self, mcp_client):
        """Test de respuesta vacía en integración"""
        empty_response = {
            "page": 1,
            "page_count": 0,
            "page_size": 10,
            "total_items": 0,
            "_embedded": {"units": []},
            "_links": {"self": {"href": "/pms/units?page=1&size=10"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = empty_response

            result = await mcp_client.call_tool(name="search_units", arguments={})

            assert result.data is not None
            assert result.data["total_items"] == 0
            assert len(result.data["_embedded"]["units"]) == 0

    @pytest.mark.asyncio
    async def test_search_units_pagination_integration(self, mcp_client):
        """Test de paginación en integración"""
        page1_response = {
            "page": 1,
            "page_count": 3,
            "page_size": 10,
            "total_items": 25,
            "_embedded": {"units": [{"id": i} for i in range(1, 11)]},
            "_links": {
                "self": {"href": "/pms/units?page=1"},
                "next": {"href": "/pms/units?page=2"},
                "last": {"href": "/pms/units?page=3"},
            },
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = page1_response

            result = await mcp_client.call_tool(
                name="search_units", arguments={"page": 1, "size": 10}
            )

            assert result.data["page"] == 1
            assert result.data["page_count"] == 3
            assert result.data["total_items"] == 25
            assert len(result.data["_embedded"]["units"]) == 10

    @pytest.mark.asyncio
    async def test_search_units_concurrent_requests_integration(
        self, mcp_client, mock_api_response
    ):
        """Test de requests concurrentes en integración"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_api_response

            # Ejecutar múltiples requests concurrentes
            tasks = [
                mcp_client.call_tool(
                    name="search_units", arguments={"search": f"test{i}"}
                )
                for i in range(5)
            ]

            results = await asyncio.gather(*tasks)

            # Verificar que todos los requests se completaron
            assert len(results) == 5
            for result in results:
                assert result.data is not None
                assert result.data["total_items"] == 15

    @pytest.mark.asyncio
    async def test_search_units_large_response_integration(self, mcp_client):
        """Test de respuesta grande en integración"""
        large_response = {
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 25,
            "_embedded": {
                "units": [
                    {
                        "id": i,
                        "name": f"Unit {i}",
                        "code": f"U{i:03d}",
                        "bedrooms": 1,
                        "bathrooms": 1,
                        "max_occupancy": 2,
                        "area": 50.0,
                        "address": f"{i} Test St",
                        "amenities": ["WiFi"],
                        "is_active": True,
                        "is_bookable": True,
                    }
                    for i in range(1, 26)
                ]
            },
            "_links": {"self": {"href": "/pms/units?page=1&size=25"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = large_response

            result = await mcp_client.call_tool(
                name="search_units", arguments={"size": 25}
            )

            assert result.data["total_items"] == 25
            assert len(result.data["_embedded"]["units"]) == 25

    @pytest.mark.asyncio
    async def test_search_units_unicode_integration(self, mcp_client):
        """Test de caracteres unicode en integración"""
        unicode_response = {
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_embedded": {
                "units": [
                    {
                        "id": 1,
                        "name": "Casa de Playa 🏖️",
                        "code": "CP001",
                        "bedrooms": 3,
                        "bathrooms": 2,
                        "max_occupancy": 6,
                        "area": 120.5,
                        "address": "123 Playa del Sol, Cancún, México",
                        "amenities": ["WiFi", "Piscina", "Aire Acondicionado"],
                        "is_active": True,
                        "is_bookable": True,
                    }
                ]
            },
            "_links": {"self": {"href": "/pms/units?page=1"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = unicode_response

            result = await mcp_client.call_tool(
                name="search_units", arguments={"search": "playa"}
            )

            unit = result.data["_embedded"]["units"][0]
            assert "🏖️" in unit["name"]
            assert "México" in unit["address"]

    @pytest.mark.asyncio
    async def test_search_units_middleware_metrics_integration(
        self, mcp_client, mock_api_response
    ):
        """Test de métricas del middleware en integración"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_api_response

            # Hacer múltiples requests para probar métricas
            for i in range(3):
                await mcp_client.call_tool(
                    name="search_units", arguments={"search": f"test{i}"}
                )

            # Verificar que el middleware registró las métricas
            # (esto se puede verificar a través de los logs o métricas expuestas)

    @pytest.mark.asyncio
    async def test_search_units_timeout_integration(self, mcp_client):
        """Test de timeout en integración"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            # Simular timeout
            import httpx

            mock_client.get.side_effect = httpx.TimeoutException("Request timeout")

            with pytest.raises(Exception):
                await mcp_client.call_tool(name="search_units", arguments={})

    @pytest.mark.asyncio
    async def test_search_units_retry_logic_integration(
        self, mcp_client, mock_api_response
    ):
        """Test de lógica de reintentos en integración"""
        with patch("trackhs_mcp.server.api_client") as mock_client:
            # Simular fallo y luego éxito
            mock_client.get.side_effect = [
                ConnectionError("Connection failed"),
                mock_api_response,
            ]

            # El primer intento debería fallar
            with pytest.raises(Exception):
                await mcp_client.call_tool(name="search_units", arguments={})

    @pytest.mark.asyncio
    async def test_search_units_memory_usage_integration(self, mcp_client):
        """Test de uso de memoria en integración"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        with patch("trackhs_mcp.server.api_client") as mock_client:
            # Respuesta con muchos datos
            large_response = {
                "page": 1,
                "page_count": 1,
                "page_size": 25,
                "total_items": 25,
                "_embedded": {
                    "units": [
                        {
                            "id": i,
                            "name": f"Unit {i}",
                            "code": f"U{i:03d}",
                            "bedrooms": 1,
                            "bathrooms": 1,
                            "max_occupancy": 2,
                            "area": 50.0,
                            "address": f"{i} Test St",
                            "amenities": ["WiFi", "Pool", "AC", "Parking", "Gym"],
                            "is_active": True,
                            "is_bookable": True,
                            "description": "A" * 1000,  # Descripción larga
                        }
                        for i in range(1, 26)
                    ]
                },
                "_links": {"self": {"href": "/pms/units?page=1&size=25"}},
            }

            mock_client.get.return_value = large_response

            # Hacer múltiples requests
            for i in range(10):
                await mcp_client.call_tool(name="search_units", arguments={"size": 25})

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Verificar que el uso de memoria no es excesivo (menos de 50MB)
        assert (
            memory_increase < 50 * 1024 * 1024
        ), f"Uso de memoria excesivo: {memory_increase / 1024 / 1024:.2f}MB"
