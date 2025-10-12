"""
Tests E2E para los dos tools principales: search_reservations_v1 y search_reservations_v2
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig


class TestSearchReservationsToolsE2E:
    """Tests E2E para los tools de búsqueda de reservas V1 y V2"""

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
    async def test_search_reservations_v1_basic_search(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para búsqueda básica con search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        # Verificar que se registró el tool
        assert mock_mcp.tool.called

        # Simular llamada al tool
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(page=1, size=10)

        # Verificar resultado
        assert result == sample_reservations_response_v1
        mock_api_client.get.assert_called_once_with(
            "/pms/reservations",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_with_filters(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para búsqueda con filtros en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        # Simular llamada con filtros
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(
            page=1,
            size=10,
            status=["Confirmed", "Checked In"],
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            node_id="1,2,3",
            unit_id="101,102",
        )

        # Verificar resultado
        assert result == sample_reservations_response_v1

        # Verificar parámetros enviados
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/pms/reservations"
        params = call_args[1]["params"]
        assert params["status"] == ["Confirmed", "Checked In"]
        assert params["arrivalStart"] == "2024-01-01T00:00:00"
        assert params["arrivalEnd"] == "2024-01-31T00:00:00"
        assert params["nodeId"] == [1, 2, 3]
        assert params["unitId"] == [101, 102]

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_scroll(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para búsqueda con scroll en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        # Simular llamada con scroll
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(scroll=1, size=1000)

        # Verificar resultado
        assert result == sample_reservations_response_v1

        # Verificar parámetros de scroll
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["scroll"] == 1
        assert params["size"] == 1000
        assert (
            params["sortColumn"] == "name"
        )  # Debe usar valores por defecto con scroll
        assert params["sortDirection"] == "asc"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_basic_search(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para búsqueda básica con search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Verificar que se registró el tool
        assert mock_mcp.tool.called

        # Simular llamada al tool
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(page=1, size=10)

        # Verificar resultado
        assert result == sample_reservations_response_v2
        mock_api_client.get.assert_called_once_with(
            "/v2/pms/reservations",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_with_filters(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para búsqueda con filtros en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Simular llamada con filtros
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(
            page=1,
            size=10,
            status=["Confirmed", "Checked In"],
            arrival_start="2024-01-01T00:00:00Z",
            arrival_end="2024-01-31T23:59:59Z",
            node_id="1,2,3",
            unit_id="101,102",
            search="Juan Pérez",
        )

        # Verificar resultado
        assert result == sample_reservations_response_v2

        # Verificar parámetros enviados
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/v2/pms/reservations"
        params = call_args[1]["params"]
        assert params["status"] == ["Confirmed", "Checked In"]
        assert params["arrivalStart"] == "2024-01-01T00:00:00"
        assert params["arrivalEnd"] == "2024-01-31T23:59:59"
        assert params["nodeId"] == [1, 2, 3]
        assert params["unitId"] == [101, 102]
        assert params["search"] == "Juan Pérez"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_scroll(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para búsqueda con scroll en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Simular llamada con scroll (usar size=100 que es el máximo permitido en V2)
        tool_func = mock_mcp.tool.call_args[0][0]
        result = await tool_func(scroll=1, size=100)

        # Verificar resultado
        assert result == sample_reservations_response_v2

        # Verificar parámetros de scroll
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["scroll"] == 1
        assert params["size"] == 100
        assert (
            params["sortColumn"] == "name"
        )  # Debe usar valores por defecto con scroll
        assert params["sortDirection"] == "asc"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_validation_errors(
        self, mock_mcp, mock_api_client
    ):
        """Test E2E para validación de errores en search_reservations_v1"""
        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error de página negativa
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="Page must be >= 0"):
            await tool_func(page=-1)

        # Test error de tamaño inválido
        with pytest.raises(TrackHSError, match="Size must be >= 1"):
            await tool_func(size=0)

        # Test error de límite total
        with pytest.raises(TrackHSError, match="Total results.*must be <= 10,000"):
            await tool_func(page=1000, size=11)

        # Test error de scroll inválido
        with pytest.raises(TrackHSError, match="Scroll must start with 1"):
            await tool_func(scroll=2)

        # Test error de formato de fecha
        with pytest.raises(TrackHSError, match="Invalid date format"):
            await tool_func(arrival_start="invalid-date")

        # Test error de status inválido
        with pytest.raises(TrackHSError, match="Invalid status"):
            await tool_func(status="InvalidStatus")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_validation_errors(
        self, mock_mcp, mock_api_client
    ):
        """Test E2E para validación de errores en search_reservations_v2"""
        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error de página negativa
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="Page must be >= 0"):
            await tool_func(page=-1)

        # Test error de tamaño inválido
        with pytest.raises(TrackHSError, match="Size must be >= 1"):
            await tool_func(size=0)

        # Test error de tamaño máximo
        with pytest.raises(TrackHSError, match="Size must be <= 1000"):
            await tool_func(size=1001)

        # Test error de límite total
        with pytest.raises(TrackHSError, match="Total results.*must be <= 10,000"):
            await tool_func(page=1000, size=11)

        # Test error de scroll inválido
        with pytest.raises(TrackHSError, match="Scroll must start with 1"):
            await tool_func(scroll=2)

        # Test error de formato de fecha
        with pytest.raises(TrackHSError, match="Invalid date format"):
            await tool_func(arrival_start="invalid-date")

        # Test error de status inválido
        with pytest.raises(TrackHSError, match="Invalid status"):
            await tool_func(status="InvalidStatus")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_api_errors(self, mock_mcp, mock_api_client):
        """Test E2E para manejo de errores de API en search_reservations_v1"""
        # Configurar mock para simular errores de API
        mock_error = Mock()
        mock_error.status_code = 401
        mock_api_client.get.side_effect = mock_error

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error 401
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="Unauthorized.*Invalid authentication"):
            await tool_func()

        # Test error 403
        mock_error.status_code = 403
        with pytest.raises(TrackHSError, match="Forbidden.*Insufficient permissions"):
            await tool_func()

        # Test error 404
        mock_error.status_code = 404
        with pytest.raises(TrackHSError, match="Endpoint not found"):
            await tool_func()

        # Test error 500
        mock_error.status_code = 500
        with pytest.raises(TrackHSError, match="Internal Server Error"):
            await tool_func()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_api_errors(self, mock_mcp, mock_api_client):
        """Test E2E para manejo de errores de API en search_reservations_v2"""
        # Configurar mock para simular errores de API
        mock_error = Mock()
        mock_error.status_code = 401
        mock_api_client.get.side_effect = mock_error

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error 401
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="Unauthorized.*Invalid authentication"):
            await tool_func()

        # Test error 403
        mock_error.status_code = 403
        with pytest.raises(TrackHSError, match="Forbidden.*Insufficient permissions"):
            await tool_func()

        # Test error 404
        mock_error.status_code = 404
        with pytest.raises(
            TrackHSError, match="Endpoint not found.*/v2/pms/reservations"
        ):
            await tool_func()

        # Test error 500
        mock_error.status_code = 500
        with pytest.raises(TrackHSError, match="Internal Server Error"):
            await tool_func()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_date_formats(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para diferentes formatos de fecha en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de fecha
        test_cases = [
            ("2024-01-01", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00Z", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00+00:00", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00-05:00", "2024-01-01T00:00:00"),
        ]

        for input_date, expected_date in test_cases:
            await tool_func(arrival_start=input_date)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["arrivalStart"] == expected_date

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_date_formats(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para diferentes formatos de fecha en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de fecha
        test_cases = [
            ("2024-01-01", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00Z", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00+00:00", "2024-01-01T00:00:00"),
            ("2024-01-01T00:00:00-05:00", "2024-01-01T00:00:00"),
        ]

        for input_date, expected_date in test_cases:
            await tool_func(arrival_start=input_date)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["arrivalStart"] == expected_date

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_id_parsing(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para parsing de IDs en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de ID
        test_cases = [
            ("1", 1),
            ("1,2,3", [1, 2, 3]),
            ("[1,2,3]", [1, 2, 3]),
            (1, 1),
        ]

        for input_id, expected_id in test_cases:
            await tool_func(node_id=input_id)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["nodeId"] == expected_id

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_id_parsing(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para parsing de IDs en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de ID
        test_cases = [
            ("1", 1),
            ("1,2,3", [1, 2, 3]),
            ("[1,2,3]", [1, 2, 3]),
            (1, 1),
            ([1, 2, 3], [1, 2, 3]),
        ]

        for input_id, expected_id in test_cases:
            await tool_func(node_id=input_id)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["nodeId"] == expected_id

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_status_parsing(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para parsing de status en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de status
        test_cases = [
            ("Confirmed", "Confirmed"),
            (["Confirmed", "Checked In"], ["Confirmed", "Checked In"]),
            ('["Confirmed", "Checked In"]', ["Confirmed", "Checked In"]),
            ("Confirmed,Checked In", ["Confirmed", "Checked In"]),
        ]

        for input_status, expected_status in test_cases:
            await tool_func(status=input_status)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["status"] == expected_status

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_status_parsing(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para parsing de status en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test diferentes formatos de status
        test_cases = [
            ("Confirmed", "Confirmed"),
            (["Confirmed", "Checked In"], ["Confirmed", "Checked In"]),
            ('["Confirmed", "Checked In"]', ["Confirmed", "Checked In"]),
            ("Confirmed,Checked In", ["Confirmed", "Checked In"]),
        ]

        for input_status, expected_status in test_cases:
            await tool_func(status=input_status)
            call_args = mock_api_client.get.call_args
            params = call_args[1]["params"]
            assert params["status"] == expected_status

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_scroll_with_sorting_error(
        self, mock_mcp, mock_api_client
    ):
        """Test E2E para error de sorting con scroll en search_reservations_v1"""
        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error cuando se usa scroll con sorting personalizado
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(
            TrackHSError, match="When using scroll, sorting is disabled"
        ):
            await tool_func(scroll=1, sort_column="status", sort_direction="desc")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_scroll_with_sorting_error(
        self, mock_mcp, mock_api_client
    ):
        """Test E2E para error de sorting con scroll en search_reservations_v2"""
        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test error cuando se usa scroll con sorting personalizado
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(
            TrackHSError, match="When using scroll, sorting is disabled"
        ):
            await tool_func(scroll=1, sort_column="status", sort_direction="desc")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_in_house_today_filter(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para filtro in_house_today en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test in_house_today = 1
        await tool_func(in_house_today=1)
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["inHouseToday"] == 1

        # Test in_house_today = 0
        await tool_func(in_house_today=0)
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["inHouseToday"] == 0

        # Test error con valor inválido
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="in_house_today must be 0 or 1"):
            await tool_func(in_house_today=2)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_in_house_today_filter(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para filtro in_house_today en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Test in_house_today = 1
        await tool_func(in_house_today=1)
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["inHouseToday"] == 1

        # Test in_house_today = 0
        await tool_func(in_house_today=0)
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["inHouseToday"] == 0

        # Test error con valor inválido
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError, match="in_house_today must be 0 or 1"):
            await tool_func(in_house_today=2)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v1_comprehensive_workflow(
        self, mock_mcp, mock_api_client, sample_reservations_response_v1
    ):
        """Test E2E para flujo completo de búsqueda en search_reservations_v1"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v1

        # Registrar tool V1
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v1 import (
            register_search_reservations_v1,
        )

        register_search_reservations_v1(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Simular flujo completo de búsqueda
        result = await tool_func(
            page=1,
            size=50,
            sort_column="checkin",
            sort_direction="desc",
            search="Juan",
            tags="vip",
            node_id="1,2,3",
            unit_id="101,102,103",
            contact_id="1001,1002",
            travel_agent_id="2001",
            campaign_id="3001",
            user_id="4001",
            unit_type_id="5001",
            rate_type_id="6001",
            reservation_type_id="7001",
            booked_start="2024-01-01",
            booked_end="2024-01-31",
            arrival_start="2024-02-01",
            arrival_end="2024-02-29",
            departure_start="2024-03-01",
            departure_end="2024-03-31",
            updated_since="2024-01-01",
            status=["Confirmed", "Checked In"],
            group_id=100,
            checkin_office_id=200,
        )

        # Verificar resultado
        assert result == sample_reservations_response_v1

        # Verificar todos los parámetros
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/pms/reservations"
        params = call_args[1]["params"]

        assert params["page"] == 1
        assert params["size"] == 50
        assert params["sortColumn"] == "checkin"
        assert params["sortDirection"] == "desc"
        assert params["search"] == "Juan"
        assert params["tags"] == "vip"
        assert params["nodeId"] == [1, 2, 3]
        assert params["unitId"] == [101, 102, 103]
        assert params["contactId"] == [1001, 1002]
        assert params["travelAgentId"] == 2001
        assert params["campaignId"] == 3001
        assert params["userId"] == 4001
        assert params["unitTypeId"] == 5001
        assert params["rateTypeId"] == 6001
        assert params["reservationTypeId"] == 7001
        assert params["bookedStart"] == "2024-01-01T00:00:00"
        assert params["bookedEnd"] == "2024-01-31T00:00:00"
        assert params["arrivalStart"] == "2024-02-01T00:00:00"
        assert params["arrivalEnd"] == "2024-02-29T00:00:00"
        assert params["departureStart"] == "2024-03-01T00:00:00"
        assert params["departureEnd"] == "2024-03-31T00:00:00"
        assert params["updatedSince"] == "2024-01-01T00:00:00"
        assert params["status"] == ["Confirmed", "Checked In"]
        assert params["groupId"] == 100
        assert params["checkinOfficeId"] == 200

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_search_reservations_v2_comprehensive_workflow(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para flujo completo de búsqueda en search_reservations_v2"""
        # Configurar mock
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Registrar tool V2
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        register_search_reservations_v2(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args[0][0]

        # Simular flujo completo de búsqueda
        result = await tool_func(
            page=1,
            size=50,
            sort_column="checkin",
            sort_direction="desc",
            search="Juan",
            tags="vip",
            node_id="1,2,3",
            unit_id="101,102,103",
            contact_id="1001,1002",
            travel_agent_id="2001",
            campaign_id="3001",
            user_id="4001",
            unit_type_id="5001",
            rate_type_id="6001",
            reservation_type_id="7001",
            booked_start="2024-01-01T00:00:00Z",
            booked_end="2024-01-31T23:59:59Z",
            arrival_start="2024-02-01T00:00:00Z",
            arrival_end="2024-02-29T23:59:59Z",
            departure_start="2024-03-01T00:00:00Z",
            departure_end="2024-03-31T23:59:59Z",
            updated_since="2024-01-01T00:00:00Z",
            status=["Confirmed", "Checked In"],
            group_id=100,
            checkin_office_id=200,
        )

        # Verificar resultado
        assert result == sample_reservations_response_v2

        # Verificar todos los parámetros
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/v2/pms/reservations"
        params = call_args[1]["params"]

        assert params["page"] == 1
        assert params["size"] == 50
        assert params["sortColumn"] == "checkin"
        assert params["sortDirection"] == "desc"
        assert params["search"] == "Juan"
        assert params["tags"] == "vip"
        assert params["nodeId"] == [1, 2, 3]
        assert params["unitId"] == [101, 102, 103]
        assert params["contactId"] == [1001, 1002]
        assert params["travelAgentId"] == 2001
        assert params["campaignId"] == 3001
        assert params["userId"] == 4001
        assert params["unitTypeId"] == 5001
        assert params["rateTypeId"] == 6001
        assert params["reservationTypeId"] == 7001
        assert params["bookedStart"] == "2024-01-01T00:00:00"
        assert params["bookedEnd"] == "2024-01-31T23:59:59"
        assert params["arrivalStart"] == "2024-02-01T00:00:00"
        assert params["arrivalEnd"] == "2024-02-29T23:59:59"
        assert params["departureStart"] == "2024-03-01T00:00:00"
        assert params["departureEnd"] == "2024-03-31T23:59:59"
        assert params["updatedSince"] == "2024-01-01T00:00:00"
        assert params["status"] == ["Confirmed", "Checked In"]
        assert params["groupId"] == 100
        assert params["checkinOfficeId"] == 200
