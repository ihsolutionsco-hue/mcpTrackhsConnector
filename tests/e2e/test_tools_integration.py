"""
Tests E2E para integración completa de ambos tools
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig


class TestToolsIntegrationE2E:
    """Tests E2E para integración completa de ambos tools"""

    @pytest.fixture
    def mock_config(self):
        """Configuración mock para testing"""
        return TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    @pytest.fixture
    def mock_api_client(self):
        """API client mock con respuestas realistas"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Servidor MCP mock"""
        mcp = Mock()
        mcp.tool = Mock()
        mcp.resource = Mock()
        mcp.prompt = Mock()
        return mcp

    @pytest.fixture
    def sample_reservations_response_v1(self):
        """Respuesta de ejemplo para API V1"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "status": "Confirmed",
                        "arrival_date": "2024-01-15T15:00:00",
                        "departure_date": "2024-01-20T11:00:00",
                        "nights": 5,
                        "guest": {
                            "id": 1,
                            "name": "Juan Pérez",
                            "email": "juan@example.com",
                        },
                        "unit": {"id": 101, "name": "Apartamento 101"},
                        "total": "500.00",
                        "currency": "USD",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {
                "self": {"href": "/pms/reservations?page=1&size=10"},
                "next": {"href": "/pms/reservations?page=2&size=10"},
            },
        }

    @pytest.fixture
    def sample_reservations_response_v2(self):
        """Respuesta de ejemplo para API V2"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "status": "Confirmed",
                        "arrival_date": "2024-01-15T15:00:00",
                        "departure_date": "2024-01-20T11:00:00",
                        "nights": 5.0,
                        "occupants": [
                            {
                                "type_id": 1,
                                "name": "Adult",
                                "handle": "adult",
                                "quantity": 2.0,
                                "included": True,
                                "extra_quantity": 0.0,
                                "rate_per_person_per_stay": "0.00",
                                "rate_per_stay": "0.00",
                            }
                        ],
                        "security_deposit": {"required": "100.00", "remaining": 100.0},
                        "guest_breakdown": {
                            "gross_rent": "500.00",
                            "net_rent": "500.00",
                            "total": "500.00",
                            "balance": "500.00",
                        },
                        "embedded": {
                            "unit": {
                                "id": 101,
                                "name": "Apartamento 101",
                                "unit_code": "APT101",
                            },
                            "contact": {
                                "id": 1,
                                "first_name": "Juan",
                                "last_name": "Pérez",
                                "primary_email": "juan@example.com",
                            },
                        },
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {
                "self": {"href": "/v2/pms/reservations?page=1&size=10"},
                "next": {"href": "/v2/pms/reservations?page=2&size=10"},
            },
        }

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_register_both_tools_together(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para registro de ambos tools juntos"""

        # Configurar mocks para diferentes endpoints
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron ambos tools
        assert mock_mcp.tool.call_count == 2

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test V1 tool
        result_v1 = await v1_tool(page=1, size=10)
        assert result_v1 == sample_reservations_response_v1

        # Test V2 tool
        result_v2 = await v2_tool(page=1, size=10)
        assert result_v2 == sample_reservations_response_v2

        # Verificar que se llamaron ambos endpoints
        assert mock_api_client.get.call_count == 2

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_with_same_parameters(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para ambos tools con los mismos parámetros"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Parámetros comunes
        common_params = {
            "page": 1,
            "size": 10,
            "status": ["Confirmed", "Checked In"],
            "arrival_start": "2024-01-01",
            "arrival_end": "2024-01-31",
            "node_id": "1,2,3",
            "unit_id": "101,102",
            "search": "Juan Pérez",
        }

        # Ejecutar ambos tools con los mismos parámetros
        result_v1 = await v1_tool(**common_params)
        result_v2 = await v2_tool(**common_params)

        # Verificar resultados
        assert result_v1 == sample_reservations_response_v1
        assert result_v2 == sample_reservations_response_v2

        # Verificar que se llamaron ambos endpoints
        assert mock_api_client.get.call_count == 2

        # Verificar parámetros enviados a cada endpoint
        v1_call = mock_api_client.get.call_args_list[0]
        v2_call = mock_api_client.get.call_args_list[1]

        assert v1_call[0][0] == "/pms/reservations"
        assert v2_call[0][0] == "/v2/pms/reservations"

        # Verificar que los parámetros son consistentes
        v1_params = v1_call[1]["params"]
        v2_params = v2_call[1]["params"]

        # Parámetros que deben ser iguales
        assert v1_params["page"] == v2_params["page"]
        assert v1_params["size"] == v2_params["size"]
        assert v1_params["status"] == v2_params["status"]
        assert v1_params["nodeId"] == v2_params["nodeId"]
        assert v1_params["unitId"] == v2_params["unitId"]
        assert v1_params["search"] == v2_params["search"]

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_error_handling(self, mock_mcp, mock_api_client):
        """Test E2E para manejo de errores en ambos tools"""
        # Configurar mock para simular errores
        mock_error = Mock()
        mock_error.status_code = 401
        mock_api_client.get.side_effect = mock_error

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test error en V1
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(
            ValidationError, match="Unauthorized.*Invalid authentication"
        ):
            await v1_tool()

        # Test error en V2
        with pytest.raises(
            ValidationError, match="Unauthorized.*Invalid authentication"
        ):
            await v2_tool()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_validation_errors(self, mock_mcp, mock_api_client):
        """Test E2E para validación de errores en ambos tools"""
        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test errores de validación en ambos tools
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        # Test error de página negativa
        with pytest.raises(ValidationError, match="Page must be >= 0"):
            await v1_tool(page=-1)

        with pytest.raises(ValidationError, match="Page must be >= 0"):
            await v2_tool(page=-1)

        # Test error de tamaño inválido
        with pytest.raises(ValidationError, match="Size must be >= 1"):
            await v1_tool(size=0)

        with pytest.raises(ValidationError, match="Size must be >= 1"):
            await v2_tool(size=0)

        # Test error de formato de fecha
        with pytest.raises(ValidationError, match="Invalid date format"):
            await v1_tool(arrival_start="invalid-date")

        with pytest.raises(ValidationError, match="Invalid date format"):
            await v2_tool(arrival_start="invalid-date")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_date_format_consistency(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para consistencia de formato de fechas en ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test diferentes formatos de fecha en ambos tools
        test_dates = [
            "2024-01-01",
            "2024-01-01T00:00:00",
            "2024-01-01T00:00:00Z",
            "2024-01-01T00:00:00+00:00",
            "2024-01-01T00:00:00-05:00",
        ]

        for test_date in test_dates:
            # Reset mock calls
            mock_api_client.get.reset_mock()
            mock_api_client.get.side_effect = mock_get_side_effect

            # Test V1
            await v1_tool(arrival_start=test_date)
            v1_call = mock_api_client.get.call_args
            v1_params = v1_call[1]["params"]
            v1_formatted_date = v1_params["arrivalStart"]

            # Test V2
            await v2_tool(arrival_start=test_date)
            v2_call = mock_api_client.get.call_args
            v2_params = v2_call[1]["params"]
            v2_formatted_date = v2_params["arrivalStart"]

            # Verificar que ambos tools formatean las fechas de la misma manera
            assert v1_formatted_date == v2_formatted_date

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_id_parsing_consistency(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para consistencia de parsing de IDs en ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test diferentes formatos de ID en ambos tools
        test_ids = [
            ("1", 1),
            ("1,2,3", [1, 2, 3]),
            ("[1,2,3]", [1, 2, 3]),
            (1, 1),
        ]

        for input_id, expected_id in test_ids:
            # Reset mock calls
            mock_api_client.get.reset_mock()
            mock_api_client.get.side_effect = mock_get_side_effect

            # Test V1
            await v1_tool(node_id=input_id)
            v1_call = mock_api_client.get.call_args
            v1_params = v1_call[1]["params"]
            v1_parsed_id = v1_params["nodeId"]

            # Test V2
            await v2_tool(node_id=input_id)
            v2_call = mock_api_client.get.call_args
            v2_params = v2_call[1]["params"]
            v2_parsed_id = v2_params["nodeId"]

            # Verificar que ambos tools parsean los IDs de la misma manera
            assert v1_parsed_id == v2_parsed_id == expected_id

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_status_parsing_consistency(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para consistencia de parsing de status en ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test diferentes formatos de status en ambos tools
        test_statuses = [
            ("Confirmed", "Confirmed"),
            (["Confirmed", "Checked In"], ["Confirmed", "Checked In"]),
            ('["Confirmed", "Checked In"]', ["Confirmed", "Checked In"]),
            ("Confirmed,Checked In", ["Confirmed", "Checked In"]),
        ]

        for input_status, expected_status in test_statuses:
            # Reset mock calls
            mock_api_client.get.reset_mock()
            mock_api_client.get.side_effect = mock_get_side_effect

            # Test V1
            await v1_tool(status=input_status)
            v1_call = mock_api_client.get.call_args
            v1_params = v1_call[1]["params"]
            v1_parsed_status = v1_params["status"]

            # Test V2
            await v2_tool(status=input_status)
            v2_call = mock_api_client.get.call_args
            v2_params = v2_call[1]["params"]
            v2_parsed_status = v2_params["status"]

            # Verificar que ambos tools parsean los status de la misma manera
            assert v1_parsed_status == v2_parsed_status == expected_status

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_scroll_consistency(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para consistencia de scroll en ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Test scroll en ambos tools
        # Reset mock calls
        mock_api_client.get.reset_mock()
        mock_api_client.get.side_effect = mock_get_side_effect

        # Test V1 con scroll
        await v1_tool(scroll=1, size=1000)
        v1_call = mock_api_client.get.call_args
        v1_params = v1_call[1]["params"]
        v1_scroll = v1_params["scroll"]
        v1_size = v1_params["size"]
        v1_sort_column = v1_params["sortColumn"]
        v1_sort_direction = v1_params["sortDirection"]

        # Test V2 con scroll
        await v2_tool(scroll=1, size=1000)
        v2_call = mock_api_client.get.call_args
        v2_params = v2_call[1]["params"]
        v2_scroll = v2_params["scroll"]
        v2_size = v2_params["size"]
        v2_sort_column = v2_params["sortColumn"]
        v2_sort_direction = v2_params["sortDirection"]

        # Verificar que ambos tools manejan scroll de la misma manera
        assert v1_scroll == v2_scroll == 1
        assert v1_size == v2_size == 1000
        assert v1_sort_column == v2_sort_column == "name"
        assert v1_sort_direction == v2_sort_direction == "asc"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_comprehensive_workflow(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para flujo completo de ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Parámetros completos para ambos tools
        comprehensive_params = {
            "page": 1,
            "size": 50,
            "sort_column": "checkin",
            "sort_direction": "desc",
            "search": "Juan Pérez",
            "tags": "vip",
            "node_id": "1,2,3",
            "unit_id": "101,102,103",
            "contact_id": "1001,1002",
            "travel_agent_id": "2001",
            "campaign_id": "3001",
            "user_id": "4001",
            "unit_type_id": "5001",
            "rate_type_id": "6001",
            "reservation_type_id": "7001",
            "booked_start": "2024-01-01",
            "booked_end": "2024-01-31",
            "arrival_start": "2024-02-01",
            "arrival_end": "2024-02-29",
            "departure_start": "2024-03-01",
            "departure_end": "2024-03-31",
            "updated_since": "2024-01-01",
            "status": ["Confirmed", "Checked In"],
            "group_id": 100,
            "checkin_office_id": 200,
            "in_house_today": 1,
        }

        # Ejecutar ambos tools con parámetros completos
        result_v1 = await v1_tool(**comprehensive_params)
        result_v2 = await v2_tool(**comprehensive_params)

        # Verificar resultados
        assert result_v1 == sample_reservations_response_v1
        assert result_v2 == sample_reservations_response_v2

        # Verificar que se llamaron ambos endpoints
        assert mock_api_client.get.call_count == 2

        # Verificar parámetros enviados a cada endpoint
        v1_call = mock_api_client.get.call_args_list[0]
        v2_call = mock_api_client.get.call_args_list[1]

        assert v1_call[0][0] == "/pms/reservations"
        assert v2_call[0][0] == "/v2/pms/reservations"

        # Verificar que los parámetros son consistentes entre ambos tools
        v1_params = v1_call[1]["params"]
        v2_params = v2_call[1]["params"]

        # Parámetros que deben ser iguales
        assert v1_params["page"] == v2_params["page"]
        assert v1_params["size"] == v2_params["size"]
        assert v1_params["sortColumn"] == v2_params["sortColumn"]
        assert v1_params["sortDirection"] == v2_params["sortDirection"]
        assert v1_params["search"] == v2_params["search"]
        assert v1_params["tags"] == v2_params["tags"]
        assert v1_params["nodeId"] == v2_params["nodeId"]
        assert v1_params["unitId"] == v2_params["unitId"]
        assert v1_params["contactId"] == v2_params["contactId"]
        assert v1_params["travelAgentId"] == v2_params["travelAgentId"]
        assert v1_params["campaignId"] == v2_params["campaignId"]
        assert v1_params["userId"] == v2_params["userId"]
        assert v1_params["unitTypeId"] == v2_params["unitTypeId"]
        assert v1_params["rateTypeId"] == v2_params["rateTypeId"]
        assert v1_params["reservationTypeId"] == v2_params["reservationTypeId"]
        assert v1_params["status"] == v2_params["status"]
        assert v1_params["groupId"] == v2_params["groupId"]
        assert v1_params["checkinOfficeId"] == v2_params["checkinOfficeId"]
        assert v1_params["inHouseToday"] == v2_params["inHouseToday"]

        # Verificar fechas (pueden tener diferencias menores en formato)
        assert v1_params["bookedStart"] == v2_params["bookedStart"]
        assert v1_params["bookedEnd"] == v2_params["bookedEnd"]
        assert v1_params["arrivalStart"] == v2_params["arrivalStart"]
        assert v1_params["arrivalEnd"] == v2_params["arrivalEnd"]
        assert v1_params["departureStart"] == v2_params["departureStart"]
        assert v1_params["departureEnd"] == v2_params["departureEnd"]
        assert v1_params["updatedSince"] == v2_params["updatedSince"]

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_performance_comparison(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para comparación de rendimiento entre ambos tools"""
        import time

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Parámetros de prueba
        test_params = {
            "page": 1,
            "size": 10,
            "status": ["Confirmed"],
            "arrival_start": "2024-01-01",
            "arrival_end": "2024-01-31",
        }

        # Medir tiempo de ejecución para V1
        start_time_v1 = time.time()
        result_v1 = await v1_tool(**test_params)
        end_time_v1 = time.time()
        execution_time_v1 = end_time_v1 - start_time_v1

        # Medir tiempo de ejecución para V2
        start_time_v2 = time.time()
        result_v2 = await v2_tool(**test_params)
        end_time_v2 = time.time()
        execution_time_v2 = end_time_v2 - start_time_v2

        # Verificar que ambos tools completaron exitosamente
        assert result_v1 == sample_reservations_response_v1
        assert result_v2 == sample_reservations_response_v2

        # Verificar que ambos tools tienen tiempos de ejecución razonables
        # (en un entorno real, estos tiempos serían más significativos)
        assert execution_time_v1 < 1.0  # Menos de 1 segundo
        assert execution_time_v2 < 1.0  # Menos de 1 segundo

        # Verificar que se llamaron ambos endpoints
        assert mock_api_client.get.call_count == 2

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_both_tools_concurrent_execution(
        self,
        mock_mcp,
        mock_api_client,
        sample_reservations_response_v1,
        sample_reservations_response_v2,
    ):
        """Test E2E para ejecución concurrente de ambos tools"""

        # Configurar mocks
        def mock_get_side_effect(endpoint, **kwargs):
            if endpoint == "/pms/reservations":
                return sample_reservations_response_v1
            elif endpoint == "/v2/pms/reservations":
                return sample_reservations_response_v2
            else:
                raise ValueError(f"Unexpected endpoint: {endpoint}")

        mock_api_client.get.side_effect = mock_get_side_effect

        # Registrar ambos tools
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Obtener las funciones registradas
        tool_calls = mock_mcp.tool.call_args_list
        v1_tool = tool_calls[0][0][0]
        v2_tool = tool_calls[1][0][0]

        # Parámetros de prueba
        test_params = {
            "page": 1,
            "size": 10,
            "status": ["Confirmed"],
            "arrival_start": "2024-01-01",
            "arrival_end": "2024-01-31",
        }

        # Ejecutar ambos tools concurrentemente
        results = await asyncio.gather(v1_tool(**test_params), v2_tool(**test_params))

        # Verificar resultados
        assert results[0] == sample_reservations_response_v1
        assert results[1] == sample_reservations_response_v2

        # Verificar que se llamaron ambos endpoints
        assert mock_api_client.get.call_count == 2
