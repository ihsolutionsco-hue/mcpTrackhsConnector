"""
Tests de integración usando Cliente FastMCP in-memory
Siguiendo las mejores prácticas de FastMCP para testing
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Client, FastMCP

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.mcp.search_amenities import (
    register_search_amenities,
)
from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestFastMCPIntegration:
    """Tests de integración usando Cliente FastMCP in-memory"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = MagicMock(spec=TrackHSApiClient)
        # Configurar métodos que serán llamados por los use cases
        client.search_units = AsyncMock()
        client.search_amenities = AsyncMock()
        return client

    @pytest.fixture
    def mcp_server(self, mock_api_client):
        """Servidor MCP para testing in-memory"""
        mcp = FastMCP("Test Server")

        # Registrar herramientas
        register_search_units(mcp, mock_api_client)
        register_search_amenities(mcp, mock_api_client)

        return mcp

    @pytest.mark.asyncio
    async def test_search_units_integration(self, mcp_server, mock_api_client):
        """Test de integración para search_units usando cliente FastMCP"""
        # Mock de respuesta de la API
        mock_response = {
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

        # Configurar mock
        mock_api_client.search_units.return_value = mock_response

        # Test usando cliente FastMCP in-memory
        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "search_units", {"page": 1, "size": 25, "search": "apartment"}
            )

            # Verificar que no hay errores
            assert not result.is_error

            # Verificar estructura de respuesta
            data = result.data
            assert "units" in data
            assert "total" in data
            assert "page" in data
            assert "size" in data
            assert "total_pages" in data
            assert "has_next" in data
            assert "has_previous" in data

            # Verificar datos específicos
            assert data["total"] == 2
            assert data["page"] == 1
            assert len(data["units"]) == 2

    @pytest.mark.asyncio
    async def test_search_amenities_integration(self, mcp_server, mock_api_client):
        """Test de integración para search_amenities usando cliente FastMCP"""
        # Mock de respuesta de la API
        mock_response = {
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

        # Configurar mock
        mock_api_client.search_amenities.return_value = mock_response

        # Test usando cliente FastMCP in-memory
        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "search_amenities", {"page": 1, "size": 25, "is_public": 1}
            )

            # Verificar que no hay errores
            assert not result.is_error

            # Verificar estructura de respuesta
            data = result.data
            assert "amenities" in data
            assert "total" in data
            assert "page" in data
            assert "size" in data
            assert "total_pages" in data
            assert "has_next" in data
            assert "has_previous" in data

            # Verificar datos específicos
            assert data["total"] == 2
            assert data["page"] == 1
            assert len(data["amenities"]) == 2

    @pytest.mark.asyncio
    async def test_tool_error_handling(self, mcp_server, mock_api_client):
        """Test de manejo de errores con ToolError"""
        # Configurar mock para lanzar excepción
        mock_api_client.search_units.side_effect = Exception("API Error")

        async with Client(mcp_server) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que se maneja el error correctamente
            assert result.is_error
            assert "API Error" in str(result.content)

    @pytest.mark.asyncio
    async def test_parameter_validation(self, mcp_server, mock_api_client):
        """Test de validación de parámetros"""
        async with Client(mcp_server) as client:
            # Test con parámetros inválidos
            result = await client.call_tool(
                "search_units", {"page": -1, "size": 25}  # Página inválida
            )

            # Debería manejar el error con ToolError
            assert result.is_error
            assert "Page must be >= 1" in str(result.content)

    @pytest.mark.asyncio
    async def test_output_schema_validation(self, mcp_server, mock_api_client):
        """Test de validación de output schemas"""
        # Mock de respuesta
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

        async with Client(mcp_server) as client:
            result = await client.call_tool("search_units", {"page": 1, "size": 25})

            # Verificar que la respuesta tiene la estructura correcta
            assert not result.is_error
            data = result.data

            # Verificar que todos los campos requeridos están presentes
            required_fields = [
                "units",
                "total",
                "page",
                "size",
                "total_pages",
                "has_next",
                "has_previous",
            ]
            for field in required_fields:
                assert field in data, f"Campo {field} faltante en la respuesta"

            # Verificar tipos de datos
            assert isinstance(data["units"], list)
            assert isinstance(data["total"], int)
            assert isinstance(data["page"], int)
            assert isinstance(data["size"], int)
            assert isinstance(data["total_pages"], int)
            assert isinstance(data["has_next"], bool)
            assert isinstance(data["has_previous"], bool)
