"""
Tests de integración para TrackHS MCP Server
Tests completos con mocks y validación de flujos
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# Agregar src al path para importaciones
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


class TestTrackHSIntegration:
    """Tests de integración para TrackHS MCP Server"""

    @pytest.fixture
    async def mcp_client(self):
        """Fixture para cliente MCP"""
        from trackhs_mcp.server import mcp
        async with Client(transport=FastMCPTransport(mcp)) as client:
            yield client

    @pytest.mark.asyncio
    async def test_search_reservations_integration(self, mcp_client):
        """Test de integración para búsqueda de reservas"""
        # Mock de respuesta de API
        mock_response = {
            "page": 0,
            "page_count": 1,
            "page_size": 10,
            "total_items": 2,
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
                        "total_amount": 500.00,
                        "balance": 0.00,
                    }
                ]
            },
            "_links": {"self": {"href": "/reservations"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_response

            # Test de búsqueda básica
            result = await mcp_client.call_tool(
                name="search_reservations",
                arguments={"page": 0, "size": 10, "status": "confirmed"},
            )

            assert result.data is not None
            assert result.data["total_items"] == 2
            assert len(result.data["_embedded"]["reservations"]) == 1
            assert result.data["_embedded"]["reservations"][0]["id"] == 12345

    @pytest.mark.asyncio
    async def test_get_reservation_integration(self, mcp_client):
        """Test de integración para obtener reserva específica"""
        mock_response = {
            "id": 12345,
            "confirmation_number": "CONF123",
            "guest": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "address": "123 Main St",
            },
            "dates": {
                "arrival": "2024-01-15",
                "departure": "2024-01-20",
                "nights": 5,
            },
            "unit": {
                "id": 100,
                "name": "Luxury Villa",
                "code": "LV001",
                "bedrooms": 3,
                "bathrooms": 2,
            },
            "status": "confirmed",
            "financial": {
                "total_amount": 500.00,
                "balance": 0.00,
                "deposit": 100.00,
            },
            "_links": {"folio": {"href": "/reservations/12345/folio"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_response

            result = await mcp_client.call_tool(
                name="get_reservation", arguments={"reservation_id": 12345}
            )

            assert result.data is not None
            assert result.data["id"] == 12345
            assert result.data["guest"]["name"] == "John Doe"
            assert result.data["unit"]["bedrooms"] == 3

    @pytest.mark.asyncio
    async def test_search_units_integration(self, mcp_client):
        """Test de integración para búsqueda de unidades"""
        mock_response = {
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_embedded": {
                "units": [
                    {
                        "id": 100,
                        "name": "Luxury Villa",
                        "code": "LV001",
                        "bedrooms": 3,
                        "bathrooms": 2,
                        "max_occupancy": 6,
                        "area": 150.5,
                        "address": "123 Resort Way",
                        "amenities": ["WiFi", "Pool", "AC"],
                        "is_active": True,
                        "is_bookable": True,
                    }
                ]
            },
            "_links": {"self": {"href": "/units"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.return_value = mock_response

            result = await mcp_client.call_tool(
                name="search_units",
                arguments={"bedrooms": 3, "bathrooms": 2, "is_active": 1},
            )

            assert result.data is not None
            assert result.data["total_items"] == 1
            unit = result.data["_embedded"]["units"][0]
            assert unit["bedrooms"] == 3
            assert unit["bathrooms"] == 2
            assert "Pool" in unit["amenities"]

    @pytest.mark.asyncio
    async def test_create_maintenance_work_order_integration(self, mcp_client):
        """Test de integración para crear orden de mantenimiento"""
        mock_response = {
            "id": 789,
            "status": "pending",
            "priority": 3,
            "summary": "Reparar aire acondicionado",
            "description": "AC no enfría correctamente",
            "unit_id": 100,
            "estimated_cost": 150.0,
            "estimated_time": 120,
            "date_received": "2024-01-15",
            "assigned_to": None,
            "vendor": None,
            "_links": {"self": {"href": "/maintenance-work-orders/789"}},
        }

        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = mock_response

            result = await mcp_client.call_tool(
                name="create_maintenance_work_order",
                arguments={
                    "unit_id": 100,
                    "summary": "Reparar aire acondicionado",
                    "description": "AC no enfría correctamente",
                    "priority": 3,
                    "estimated_cost": 150.0,
                    "estimated_time": 120,
                },
            )

            assert result.data is not None
            assert result.data["id"] == 789
            assert result.data["status"] == "pending"
            assert result.data["priority"] == 3

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, mcp_client):
        """Test de manejo de errores en integración"""
        from trackhs_mcp.exceptions import AuthenticationError, APIError

        # Test de error de autenticación
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.side_effect = AuthenticationError("Credenciales inválidas")

            with pytest.raises(Exception):  # FastMCP convierte excepciones
                await mcp_client.call_tool(
                    name="search_reservations", arguments={"page": 0, "size": 10}
                )

        # Test de error de API
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_client.get.side_effect = APIError("Error de API: 500")

            with pytest.raises(Exception):
                await mcp_client.call_tool(
                    name="search_reservations", arguments={"page": 0, "size": 10}
                )

    @pytest.mark.asyncio
    async def test_middleware_integration(self, mcp_client):
        """Test de integración del middleware"""
        # Verificar que el middleware está funcionando
        # (esto se puede verificar a través de los logs)
        
        with patch("trackhs_mcp.server.api_client") as mock_client:
            mock_response = {"page": 0, "page_count": 1, "page_size": 10, "total_items": 0, "_embedded": {"reservations": []}, "_links": {}}
            mock_client.get.return_value = mock_response

            # El middleware debería procesar este request
            result = await mcp_client.call_tool(
                name="search_reservations", arguments={"page": 0, "size": 10}
            )

            assert result.data is not None
            # El middleware debería haber registrado métricas y logs

    @pytest.mark.asyncio
    async def test_health_check_integration(self, mcp_client):
        """Test de integración del health check"""
        # Test del recurso de health check
        resources = await mcp_client.list_resources()
        resource_uris = [str(resource.uri) for resource in resources]
        
        assert "https://trackhs-mcp.local/health" in resource_uris

        # Test del contenido del health check
        health_content = await mcp_client.read_resource("https://trackhs-mcp.local/health")
        assert health_content is not None
        assert "status" in health_content
        assert "timestamp" in health_content
