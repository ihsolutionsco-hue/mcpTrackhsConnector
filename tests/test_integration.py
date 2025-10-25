"""
Tests de integración para TrackHS MCP Server
"""

import os
from unittest.mock import patch

import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport


@pytest.mark.integration
class TestTrackHSIntegration:
    """Tests de integración con TrackHS API"""

    @pytest.mark.asyncio
    async def test_full_reservation_workflow(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de flujo completo de reserva"""
        # Mock de datos de reserva
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

        # 1. Buscar reservas
        with patch(
            "src.trackhs_mcp.server.api_client.get",
            return_value={
                "page": 1,
                "total_items": 1,
                "_embedded": {"reservations": [mock_reservation]},
            },
        ):
            search_result = await mcp_client.call_tool(
                "search_reservations",
                {"page": 0, "size": 10, "search": "john@example.com"},
            )
            assert search_result.content[0].text is not None

        # 2. Obtener reserva específica
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_reservation
        ):
            reservation_result = await mcp_client.call_tool(
                "get_reservation", {"reservation_id": 12345}
            )
            assert reservation_result.content[0].text is not None

        # 3. Obtener folio de la reserva
        with patch("src.trackhs_mcp.server.api_client.get", return_value=mock_folio):
            folio_result = await mcp_client.call_tool(
                "get_folio", {"reservation_id": 12345}
            )
            assert folio_result.content[0].text is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_unit_management_workflow(self, mcp_client: Client[FastMCPTransport]):
        """Test de flujo de gestión de unidades"""
        mock_units = {
            "page": 1,
            "total_items": 1,
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
                        "address": "123 Beach St",
                        "amenities": ["WiFi", "Pool", "Parking"],
                        "is_active": True,
                        "is_bookable": True,
                    }
                ]
            },
        }

        mock_amenities = {
            "page": 1,
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
        }

        # 1. Buscar unidades
        with patch("src.trackhs_mcp.server.api_client.get", return_value=mock_units):
            units_result = await mcp_client.call_tool(
                "search_units", {"page": 1, "size": 10, "bedrooms": 3}
            )
            assert units_result.content[0].text is not None

        # 2. Buscar amenidades
        with patch(
            "src.trackhs_mcp.server.api_client.get", return_value=mock_amenities
        ):
            amenities_result = await mcp_client.call_tool(
                "search_amenities", {"page": 1, "size": 10}
            )
            assert amenities_result.content[0].text is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_work_order_management_workflow(
        self, mcp_client: Client[FastMCPTransport]
    ):
        """Test de flujo de gestión de órdenes de trabajo"""
        mock_maintenance_wo = {
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

        mock_housekeeping_wo = {
            "id": 1002,
            "status": "pending",
            "unit_id": 100,
            "scheduled_at": "2024-01-16",
            "is_inspection": False,
            "clean_type_id": 1,
            "comments": "Limpieza post-evento",
            "cost": 75.0,
        }

        # 1. Crear orden de mantenimiento
        with patch(
            "src.trackhs_mcp.server.api_client.post", return_value=mock_maintenance_wo
        ):
            maintenance_result = await mcp_client.call_tool(
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
            assert maintenance_result.content[0].text is not None

        # 2. Crear orden de housekeeping
        with patch(
            "src.trackhs_mcp.server.api_client.post", return_value=mock_housekeeping_wo
        ):
            housekeeping_result = await mcp_client.call_tool(
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
            assert housekeeping_result.content[0].text is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, mcp_client: Client[FastMCPTransport]):
        """Test de recuperación de errores en flujo completo"""
        # Simular error en primera llamada
        with patch(
            "src.trackhs_mcp.server.api_client.get", side_effect=Exception("API Error")
        ):
            with pytest.raises(Exception):
                await mcp_client.call_tool(
                    "search_reservations", {"page": 0, "size": 10}
                )

        # Simular recuperación exitosa
        mock_response = {"page": 1, "total_items": 1, "_embedded": {"reservations": []}}

        with patch("src.trackhs_mcp.server.api_client.get", return_value=mock_response):
            result = await mcp_client.call_tool(
                "search_reservations", {"page": 0, "size": 10}
            )
            assert result.content[0].text is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, mcp_client: Client[FastMCPTransport]):
        """Test de operaciones concurrentes"""
        import asyncio

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

        async def search_reservation():
            with patch(
                "src.trackhs_mcp.server.api_client.get",
                return_value={
                    "page": 1,
                    "total_items": 1,
                    "_embedded": {"reservations": [mock_reservation]},
                },
            ):
                return await mcp_client.call_tool(
                    "search_reservations", {"page": 0, "size": 10}
                )

        async def get_reservation():
            with patch(
                "src.trackhs_mcp.server.api_client.get", return_value=mock_reservation
            ):
                return await mcp_client.call_tool(
                    "get_reservation", {"reservation_id": 12345}
                )

        # Ejecutar operaciones concurrentes
        results = await asyncio.gather(
            search_reservation(),
            get_reservation(),
            search_reservation(),  # Duplicado para test de concurrencia
        )

        # Todas las operaciones deben completarse exitosamente
        assert len(results) == 3
        for result in results:
            assert result.content[0].text is not None

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_performance_under_load(self, mcp_client: Client[FastMCPTransport]):
        """Test de performance bajo carga"""
        import asyncio
        import time

        mock_response = {"page": 1, "total_items": 1, "_embedded": {"reservations": []}}

        async def make_request():
            with patch(
                "src.trackhs_mcp.server.api_client.get", return_value=mock_response
            ):
                return await mcp_client.call_tool(
                    "search_reservations", {"page": 0, "size": 10}
                )

        # Ejecutar 20 requests concurrentes
        start_time = time.time()
        tasks = [make_request() for _ in range(20)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        execution_time = end_time - start_time

        # Debe completarse en menos de 10 segundos
        assert execution_time < 10.0
        assert len(results) == 20

        # Todos los resultados deben ser válidos
        for result in results:
            assert result.content[0].text is not None
