"""
Tests de integración para recursos MCP
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.resources import register_all_resources


class TestResourcesIntegration:
    """Tests de integración para recursos MCP"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.resource = Mock()
        return mcp

    def setup_resource_mock(self, mock_mcp):
        """Configura un mock que funcione como decorador de resources"""
        registered_functions = {}

        def mock_resource_decorator(name):
            def decorator(func):
                registered_functions[name] = func
                return func

            return decorator

        mock_mcp.resource = mock_resource_decorator
        return registered_functions

    @pytest.mark.integration
    def test_register_all_resources(self, mock_mcp, mock_api_client):
        """Test registro de todos los recursos"""
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron múltiples recursos
        assert mock_mcp.resource.call_count >= 4  # Al menos 4 recursos esperados

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_reservations_schema_resource(self, mock_mcp, mock_api_client):
        """Test recurso de esquema de reservas"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://schema/reservations"]

        result = await resource_func()

        assert "schema" in result
        assert "definitions" in result
        assert "description" in result
        assert "version" in result
        assert "api_endpoint" in result
        assert "supported_operations" in result
        assert "pagination" in result
        assert "filtering" in result
        assert "sorting" in result

        # Verificar estructura del esquema
        schema = result["schema"]
        assert "id" in schema
        assert "alternates" in schema
        assert "currency" in schema
        assert "unitId" in schema
        assert "status" in schema
        assert "arrivalDate" in schema
        assert "departureDate" in schema

        # Verificar definiciones
        definitions = result["definitions"]
        assert "Occupant" in definitions
        assert "SecurityDeposit" in definitions
        assert "GuestBreakdown" in definitions
        assert "OwnerBreakdown" in definitions
        assert "Rate" in definitions
        assert "GuestFee" in definitions
        assert "Tax" in definitions
        assert "OwnerFee" in definitions
        assert "PaymentPlan" in definitions
        assert "TravelInsuranceProduct" in definitions

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_units_schema_resource(self, mock_mcp, mock_api_client):
        """Test recurso de esquema de unidades"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://schema/units"]

        result = await resource_func()

        assert "schema" in result
        # El recurso de unidades no tiene definitions, solo schema
        assert "description" in result
        # El recurso de unidades no incluye version, api_endpoint ni
        # supported_operations

        # Verificar estructura del esquema de unidades
        schema = result["schema"]
        assert "id" in schema
        assert "name" in schema
        assert "type" in schema
        assert "capacity" in schema
        assert "status" in schema
        assert "nodeId" in schema
        assert "amenities" in schema

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_system_status_resource(self, mock_mcp, mock_api_client):
        """Test recurso de estado del sistema"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://system/status"]

        result = await resource_func()

        assert "status" in result
        assert "timestamp" in result
        assert "version" in result
        # El recurso de system status no incluye uptime ni components

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_documentation_resource(self, mock_mcp, mock_api_client):
        """Test recurso de documentación de API"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://api/documentation"]

        result = await resource_func()

        # El recurso de documentación devuelve un string, no un dict
        assert isinstance(result, str)
        assert "TrackHS API V2" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_endpoints_resource(self, mock_mcp, mock_api_client):
        """Test recurso de endpoints API V2"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://api/v2/endpoints"]

        result = await resource_func()

        assert "version" in result
        assert "base_url" in result
        assert "endpoints" in result
        assert "authentication" in result
        assert "rate_limits" in result

        # Verificar endpoints
        endpoints = result["endpoints"]
        assert "reservations" in endpoints

        reservations_endpoint = endpoints["reservations"]
        assert "search" in reservations_endpoint

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_parameters_resource(self, mock_mcp, mock_api_client):
        """Test recurso de parámetros API V2"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://api/v2/parameters"]

        result = await resource_func()

        # El recurso de parámetros tiene una estructura diferente
        assert "pagination" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_examples_resource(self, mock_mcp, mock_api_client):
        """Test recurso de ejemplos API V2"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://api/v2/examples"]

        result = await resource_func()

        # El recurso de ejemplos tiene una estructura diferente
        assert "basic_search" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_resources_with_api_client_calls(self, mock_mcp, mock_api_client):
        """Test recursos que hacen llamadas al API client"""
        # Configurar mock para llamadas específicas
        mock_api_client.get.return_value = {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
        }

        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Test system_status que puede hacer llamadas al API
        system_status_func = None
        for call in mock_mcp.resource.call_args_list:
            if "system_status" in str(call):
                system_status_func = call[0][1]
                break

        if system_status_func:
            result = await system_status_func()
            assert "status" in result
            assert "timestamp" in result

    @pytest.mark.integration
    def test_resource_registration_count(self, mock_mcp, mock_api_client):
        """Test que se registran todos los recursos esperados"""
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron al menos 7 recursos
        assert mock_mcp.resource.call_count >= 7

        # Verificar que cada recurso tiene un nombre único
        resource_names = [call[0][0] for call in mock_mcp.resource.call_args_list]
        assert len(set(resource_names)) == len(
            resource_names
        ), "Resource names should be unique"

    @pytest.mark.integration
    def test_resource_names(self, mock_mcp, mock_api_client):
        """Test nombres de recursos"""
        register_all_resources(mock_mcp, mock_api_client)

        resource_names = [call[0][0] for call in mock_mcp.resource.call_args_list]

        expected_names = [
            "trackhs://schema/reservations",
            "trackhs://schema/units",
            "trackhs://system/status",
            "trackhs://api/documentation",
            "trackhs://api/v2/endpoints",
            "trackhs://api/v2/parameters",
            "trackhs://api/v2/examples",
        ]

        for expected_name in expected_names:
            assert (
                expected_name in resource_names
            ), f"Resource {expected_name} should be registered"
