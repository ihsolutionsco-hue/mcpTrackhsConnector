"""
Tests unitarios para el servidor TrackHS MCP
"""

from unittest.mock import Mock, patch

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport


class TestTrackHSServer:
    """Tests para el servidor TrackHS MCP"""

    @pytest.mark.asyncio
    async def test_list_tools(self, mcp_client: Client[FastMCPTransport]):
        """Test que el servidor expone las herramientas correctas"""
        tools = await mcp_client.list_tools()

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
            assert expected_tool in tool_names, f"Tool {expected_tool} not found"

    @pytest.mark.asyncio
    async def test_search_reservations_basic(
        self, mcp_client: Client[FastMCPTransport], mock_api_response
    ):
        """Test básico de búsqueda de reservas"""
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_api_response
        ):
            result = await mcp_client.call_tool(
                "search_reservations", {"page": 0, "size": 10}
            )

            assert result.content[0].text is not None
            # Verificar que la respuesta contiene datos esperados
            response_data = result.content[0].text
            assert "reservations" in response_data or "page" in response_data

    @pytest.mark.asyncio
    async def test_search_reservations_with_filters(
        self, mcp_client: Client[FastMCPTransport], mock_api_response
    ):
        """Test de búsqueda de reservas con filtros"""
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_api_response
        ):
            result = await mcp_client.call_tool(
                "search_reservations",
                {
                    "page": 0,
                    "size": 5,
                    "search": "john@example.com",
                    "arrival_start": "2024-01-15",
                    "arrival_end": "2024-01-20",
                    "status": "confirmed",
                },
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_get_reservation(self, mcp_client: Client[FastMCPTransport]):
        """Test de obtención de reserva específica"""
        mock_reservation = {
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

        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_reservation
        ):
            result = await mcp_client.call_tool(
                "get_reservation", {"reservation_id": 12345}
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_search_units(
        self, mcp_client: Client[FastMCPTransport], mock_unit_response
    ):
        """Test de búsqueda de unidades"""
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_unit_response
        ):
            result = await mcp_client.call_tool("search_units", {"page": 1, "size": 10})

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_search_units_with_filters(
        self, mcp_client: Client[FastMCPTransport], mock_unit_response
    ):
        """Test de búsqueda de unidades con filtros"""
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_unit_response
        ):
            result = await mcp_client.call_tool(
                "search_units",
                {
                    "page": 1,
                    "size": 5,
                    "search": "beach",
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "is_active": 1,
                    "is_bookable": 1,
                },
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_search_amenities(self, mcp_client: Client[FastMCPTransport]):
        """Test de búsqueda de amenidades"""
        mock_amenities = {
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 3,
            "_embedded": {
                "amenities": [
                    {"id": 1, "name": "WiFi", "group": {"id": 1, "name": "Internet"}},
                    {"id": 2, "name": "Pool", "group": {"id": 2, "name": "Recreation"}},
                    {
                        "id": 3,
                        "name": "Parking",
                        "group": {"id": 3, "name": "Transportation"},
                    },
                ]
            },
            "_links": {"self": {"href": "https://api-test.trackhs.com/api/amenities"}},
        }

        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_amenities
        ):
            result = await mcp_client.call_tool(
                "search_amenities", {"page": 1, "size": 10}
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_get_folio(self, mcp_client: Client[FastMCPTransport]):
        """Test de obtención de folio"""
        mock_folio = {
            "id": 12345,
            "reservation_id": 12345,
            "total_charges": 500.0,
            "total_payments": 500.0,
            "balance": 0.0,
            "charges": [
                {"description": "Room rate", "amount": 400.0},
                {"description": "Taxes", "amount": 100.0},
            ],
            "payments": [
                {"description": "Deposit", "amount": 250.0},
                {"description": "Final payment", "amount": 250.0},
            ],
        }

        with patch("src.trackhs_mcp.server.api_client.get", return_value=mock_folio):
            result = await mcp_client.call_tool("get_folio", {"reservation_id": 12345})

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_create_maintenance_work_order(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de creación de orden de mantenimiento"""
        mock_work_order = {
            "id": 1001,
            "status": "pending",
            "priority": 3,
            "summary": "Fuga en grifo",
            "description": "Grifo del baño principal gotea constantemente",
            "unit_id": 100,
            "estimated_cost": 150.0,
            "estimated_time": 60,
            "date_received": "2024-01-15",
        }

        with patch(
            "src.trackhs_mcp.server.api_client.post", return_value=mock_work_order
        ):
            result = await mcp_client.call_tool(
                "create_maintenance_work_order",
                {
                    "unit_id": 100,
                    "summary": "Fuga en grifo",
                    "description": "Grifo del baño principal gotea constantemente",
                    "priority": 3,
                    "estimated_cost": 150.0,
                    "estimated_time": 60,
                },
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_create_housekeeping_work_order(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de creación de orden de housekeeping"""
        mock_work_order = {
            "id": 1002,
            "status": "pending",
            "unit_id": 100,
            "scheduled_at": "2024-01-16",
            "is_inspection": False,
            "clean_type_id": 1,
            "comments": "Limpieza post-evento",
            "cost": 75.0,
        }

        with patch(
            "src.trackhs_mcp.server.api_client.post", return_value=mock_work_order
        ):
            result = await mcp_client.call_tool(
                "create_housekeeping_work_order",
                {
                    "unit_id": 100,
                    "scheduled_at": "2024-01-16",
                    "is_inspection": False,
                    "clean_type_id": 1,
                    "comments": "Limpieza post-evento",
                    "cost": 75.0,
                },
            )

            assert result.content[0].text is not None

    @pytest.mark.asyncio
    async def test_validation_errors(self, mcp_client: Client[FastMCPTransport]):
        """Test de validación de parámetros"""
        # Test con parámetros inválidos
        with pytest.raises(Exception):  # FastMCP debería validar los parámetros
            await mcp_client.call_tool(
                "search_reservations", {"page": -1, "size": 0}  # Parámetros inválidos
            )

    @pytest.mark.asyncio
    async def test_api_error_handling(self, mcp_client: Client[FastMCPTransport]):
        """Test de manejo de errores de API"""
        with patch(
            "src.trackhs_mcp.server.api_client.get", side_effect=Exception("API Error")
        ):
            with pytest.raises(Exception):
                await mcp_client.call_tool(
                    "search_reservations", {"page": 0, "size": 10}
                )
