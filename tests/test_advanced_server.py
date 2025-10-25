"""
Tests avanzados para el servidor TrackHS MCP usando mejores prácticas de FastMCP
"""

from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsDict, IsInt, IsList, IsStr
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from inline_snapshot import snapshot


class TestAdvancedServer:
    """Tests avanzados usando mejores prácticas de FastMCP"""

    @pytest.mark.asyncio
    async def test_list_tools_with_snapshot(self, mcp_client: Client[FastMCPTransport]):
        """Test de listado de herramientas con snapshot para validación de estructura"""
        tools = await mcp_client.list_tools()

        # Usar snapshot para validar la estructura completa
        assert tools == snapshot(
            [
                snapshot(
                    {
                        "name": "search_reservations",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "get_reservation",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "search_units",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "search_amenities",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "get_folio",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "create_maintenance_work_order",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
                snapshot(
                    {
                        "name": "create_housekeeping_work_order",
                        "description": IsStr(),
                        "inputSchema": IsDict(),
                    }
                ),
            ]
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "page,size,expected_valid",
        [
            (0, 10, True),
            (1, 25, True),
            (-1, 10, False),  # página negativa
            (0, 0, False),  # tamaño cero
            (0, 101, False),  # tamaño excesivo
        ],
    )
    async def test_search_reservations_parametrized(
        self,
        mcp_client: Client[FastMCPTransport],
        mock_api_response,
        page,
        size,
        expected_valid,
    ):
        """Test parametrizado de búsqueda de reservas con diferentes parámetros"""
        with patch("trackhs_mcp.server.api_client.get", return_value=mock_api_response):
            if expected_valid:
                result = await mcp_client.call_tool(
                    "search_reservations", {"page": page, "size": size}
                )
                assert result.content[0].text is not None
            else:
                with pytest.raises(Exception):
                    await mcp_client.call_tool(
                        "search_reservations", {"page": page, "size": size}
                    )

    @pytest.mark.asyncio
    async def test_search_reservations_with_dynamic_validation(
        self, mcp_client: Client[FastMCPTransport], mock_api_response
    ):
        """Test con validación dinámica usando dirty-equals"""
        with patch("trackhs_mcp.server.api_client.get", return_value=mock_api_response):
            result = await mcp_client.call_tool(
                "search_reservations", {"page": 0, "size": 10}
            )

            # Validar estructura de respuesta con dirty-equals
            response_text = result.content[0].text
            assert response_text == IsStr()  # Debe ser string
            assert "reservations" in response_text or "page" in response_text

    @pytest.mark.asyncio
    async def test_get_reservation_with_snapshot(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de obtención de reserva con snapshot de respuesta"""
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

        with patch("trackhs_mcp.server.api_client.get", return_value=mock_reservation):
            result = await mcp_client.call_tool(
                "get_reservation", {"reservation_id": 12345}
            )

            # Validar que la respuesta contiene la estructura esperada
            response_text = result.content[0].text
            assert response_text == IsStr()
            assert "12345" in response_text  # ID debe estar en la respuesta

    @pytest.mark.asyncio
    async def test_error_handling_with_dynamic_values(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de manejo de errores con validación de valores dinámicos"""
        with patch(
            "trackhs_mcp.server.api_client.get", side_effect=Exception("API Error")
        ):
            with pytest.raises(Exception) as exc_info:
                await mcp_client.call_tool(
                    "search_reservations", {"page": 0, "size": 10}
                )

            # Validar que el error contiene información relevante
            assert "API Error" in str(exc_info.value) or "Error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_work_order_creation_with_snapshot(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de creación de orden de trabajo con snapshot"""
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

        with patch("trackhs_mcp.server.api_client.post", return_value=mock_work_order):
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

            # Validar respuesta con dirty-equals
            response_text = result.content[0].text
            assert response_text == IsStr()
            assert "1001" in response_text or "pending" in response_text

    @pytest.mark.asyncio
    async def test_server_health_with_dynamic_validation(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de health check con validación dinámica"""
        # Simular ping al servidor
        try:
            # El cliente MCP debería tener un método ping
            # Si no existe, validamos que el servidor responde
            tools = await mcp_client.list_tools()
            assert len(tools) == IsInt(ge=7)  # Al menos 7 herramientas
        except AttributeError:
            # Si no hay método ping, validamos que list_tools funciona
            tools = await mcp_client.list_tools()
            assert tools == IsList(length=7)  # Exactamente 7 herramientas
