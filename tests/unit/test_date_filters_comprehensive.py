"""
Tests comprehensivos para filtros de fecha
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.core.api_client import TrackHSApiClient
from src.trackhs_mcp.tools.search_reservations import (
    _is_valid_date_format,
    _normalize_date_format,
    register_search_reservations,
)


class TestDateFiltersComprehensive:
    """Tests comprehensivos para filtros de fecha"""

    def test_date_normalization_comprehensive(self):
        """Test comprehensivo de normalización de fechas"""

        test_cases = [
            # (input, expected_output, description)
            ("2025-01-01", "2025-01-01T00:00:00Z", "Solo fecha básica"),
            ("2025-01-31", "2025-01-31T00:00:00Z", "Solo fecha fin de mes"),
            (
                "2025-01-01T00:00:00",
                "2025-01-01T00:00:00Z",
                "Fecha con tiempo sin timezone",
            ),
            (
                "2025-01-01T23:59:59",
                "2025-01-01T23:59:59Z",
                "Fecha con tiempo final sin timezone",
            ),
            ("2025-01-01T00:00:00Z", "2025-01-01T00:00:00Z", "Ya normalizada con Z"),
            (
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "Ya normalizada con offset",
            ),
            (
                "2025-01-01T00:00:00.123",
                "2025-01-01T00:00:00.123Z",
                "Con microsegundos sin timezone",
            ),
            (
                "2025-01-01T00:00:00.123Z",
                "2025-01-01T00:00:00.123Z",
                "Con microsegundos y Z",
            ),
        ]

        for input_date, expected, description in test_cases:
            result = _normalize_date_format(input_date)
            assert (
                result == expected
            ), f"Failed for {description}: {input_date} -> {result} != {expected}"

    def test_date_validation_comprehensive(self):
        """Test comprehensivo de validación de fechas"""

        valid_cases = [
            "2025-01-01",
            "2025-01-01T00:00:00",
            "2025-01-01T00:00:00Z",
            "2025-01-01T00:00:00+00:00",
            "2025-01-01T00:00:00-05:00",
            "2025-01-01T00:00:00.123Z",
            "2025-01-01 00:00:00",
        ]

        invalid_cases = [
            "2025/01/01",
            "01-01-2025",
            "2025-1-1",
            "invalid-date",
            "",
            "2025-01-01T",
            "2025-01-01T00:00:00X",
        ]

        for date in valid_cases:
            assert _is_valid_date_format(date), f"Valid date failed: {date}"

        for date in invalid_cases:
            assert not _is_valid_date_format(date), f"Invalid date passed: {date}"

    @pytest.mark.asyncio
    async def test_date_parameters_construction(self):
        """Test que verifica la construcción correcta de parámetros de fecha"""

        # Mock del cliente API
        mock_api_client = MagicMock(spec=TrackHSApiClient)
        mock_api_client.client = AsyncMock()

        # Mock de respuesta
        mock_response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 5,
            "total_items": 0,
            "_links": {"self": {"href": "test"}},
        }

        mock_response_obj = AsyncMock()
        mock_response_obj.is_success = True
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.headers = {"content-type": "application/json"}
        mock_api_client.client.request.return_value = mock_response_obj

        # Capturar parámetros
        captured_params = {}

        async def capture_request(method, endpoint, **kwargs):
            if "params" in kwargs:
                captured_params.update(kwargs["params"])
            return mock_response_obj

        mock_api_client.client.request.side_effect = capture_request

        # Mock MCP
        class MockMCP:
            def __init__(self):
                self.registered_tools = {}

            def tool(self, func):
                self.registered_tools[func.__name__] = func
                return func

        mcp = MockMCP()
        register_search_reservations(mcp, mock_api_client)
        search_func = mcp.registered_tools["search_reservations"]

        # Ejecutar búsqueda con todos los parámetros de fecha
        await search_func(
            arrival_start="2025-01-01",
            arrival_end="2025-01-31",
            departure_start="2025-02-01",
            departure_end="2025-02-28",
            booked_start="2024-12-01",
            booked_end="2024-12-31",
            updated_since="2024-12-01T00:00:00Z",
            status="Confirmed",
        )

        # Verificar que todos los parámetros de fecha están presentes
        expected_date_params = {
            "arrivalStart": "2025-01-01T00:00:00Z",
            "arrivalEnd": "2025-01-31T00:00:00Z",
            "departureStart": "2025-02-01T00:00:00Z",
            "departureEnd": "2025-02-28T00:00:00Z",
            "bookedStart": "2024-12-01T00:00:00Z",
            "bookedEnd": "2024-12-31T00:00:00Z",
            "updatedSince": "2024-12-01T00:00:00Z",
        }

        for param_name, expected_value in expected_date_params.items():
            assert param_name in captured_params, f"Missing parameter: {param_name}"
            actual_value = captured_params[param_name]
            assert actual_value == expected_value, (
                f"Wrong value for {param_name}: {actual_value} != {expected_value}"
            )

    @pytest.mark.asyncio
    async def test_date_parameter_edge_cases(self):
        """Test casos edge de parámetros de fecha"""

        # Mock del cliente API
        mock_api_client = MagicMock(spec=TrackHSApiClient)
        mock_api_client.client = AsyncMock()

        mock_response_obj = AsyncMock()
        mock_response_obj.is_success = True
        mock_response_obj.json.return_value = {"_embedded": {"reservations": []}}
        mock_response_obj.headers = {"content-type": "application/json"}
        mock_api_client.client.request.return_value = mock_response_obj

        # Capturar parámetros
        captured_params = {}

        async def capture_request(method, endpoint, **kwargs):
            if "params" in kwargs:
                captured_params.update(kwargs["params"])
            return mock_response_obj

        mock_api_client.client.request.side_effect = capture_request

        # Mock MCP
        class MockMCP:
            def __init__(self):
                self.registered_tools = {}

            def tool(self, func):
                self.registered_tools[func.__name__] = func
                return func

        mcp = MockMCP()
        register_search_reservations(mcp, mock_api_client)
        search_func = mcp.registered_tools["search_reservations"]

        # Test casos edge
        edge_cases = [
            # (arrival_start, arrival_end, expected_start, expected_end, description)
            (
                "2025-01-01",
                "2025-01-31",
                "2025-01-01T00:00:00Z",
                "2025-01-31T00:00:00Z",
                "Solo fechas",
            ),
            (
                "2025-01-01T00:00:00",
                "2025-01-31T23:59:59",
                "2025-01-01T00:00:00Z",
                "2025-01-31T23:59:59Z",
                "Con tiempo",
            ),
            (
                "2025-01-01T00:00:00Z",
                "2025-01-31T23:59:59Z",
                "2025-01-01T00:00:00Z",
                "2025-01-31T23:59:59Z",
                "Ya normalizadas",
            ),
        ]

        for (
            arrival_start,
            arrival_end,
            expected_start,
            expected_end,
            description,
        ) in edge_cases:
            # Resetear parámetros capturados
            captured_params.clear()

            await search_func(
                arrival_start=arrival_start, arrival_end=arrival_end, status="Confirmed"
            )

            assert (
                captured_params["arrivalStart"] == expected_start
            ), f"Failed for {description}: arrivalStart"
            assert (
                captured_params["arrivalEnd"] == expected_end
            ), f"Failed for {description}: arrivalEnd"

    def test_date_validation_error_cases(self):
        """Test casos de error en validación de fechas"""

        with pytest.raises(Exception):
            # Esto debería fallar si se implementa validación estricta
            _normalize_date_format("invalid-date")

        # Test que fechas inválidas no pasen la validación
        invalid_dates = [
            "2025/01/01",
            "01-01-2025",
            "2025-1-1",
            "invalid-date",
            "",
            "2025-01-01T",
        ]

        for invalid_date in invalid_dates:
            assert not _is_valid_date_format(
                invalid_date
            ), f"Invalid date passed validation: {invalid_date}"

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self):
        """Test combinaciones de parámetros de fecha"""

        # Mock del cliente API
        mock_api_client = MagicMock(spec=TrackHSApiClient)
        mock_api_client.client = AsyncMock()

        mock_response_obj = AsyncMock()
        mock_response_obj.is_success = True
        mock_response_obj.json.return_value = {"_embedded": {"reservations": []}}
        mock_response_obj.headers = {"content-type": "application/json"}
        mock_api_client.client.request.return_value = mock_response_obj

        # Capturar parámetros
        captured_params = {}

        async def capture_request(method, endpoint, **kwargs):
            if "params" in kwargs:
                captured_params.update(kwargs["params"])
            return mock_response_obj

        mock_api_client.client.request.side_effect = capture_request

        # Mock MCP
        class MockMCP:
            def __init__(self):
                self.registered_tools = {}

            def tool(self, func):
                self.registered_tools[func.__name__] = func
                return func

        mcp = MockMCP()
        register_search_reservations(mcp, mock_api_client)
        search_func = mcp.registered_tools["search_reservations"]

        # Test diferentes combinaciones
        combinations = [
            # Solo arrival
            {"arrival_start": "2025-01-01", "arrival_end": "2025-01-31"},
            # Solo departure
            {"departure_start": "2025-02-01", "departure_end": "2025-02-28"},
            # Solo booked
            {"booked_start": "2024-12-01", "booked_end": "2024-12-31"},
            # Combinación completa
            {
                "arrival_start": "2025-01-01",
                "arrival_end": "2025-01-31",
                "departure_start": "2025-02-01",
                "departure_end": "2025-02-28",
                "booked_start": "2024-12-01",
                "booked_end": "2024-12-31",
            },
        ]

        for i, params in enumerate(combinations):
            captured_params.clear()

            await search_func(**params, status="Confirmed")

            # Verificar que los parámetros esperados están presentes
            for param_name, param_value in params.items():
                api_param_name = param_name.replace("_start", "Start").replace(
                    "_end", "End"
                )
                expected_value = _normalize_date_format(param_value)
                assert (
                    captured_params[api_param_name] == expected_value
                ), f"Combination {i+1}: {api_param_name} mismatch"


if __name__ == "__main__":
    pytest.main([__file__])
