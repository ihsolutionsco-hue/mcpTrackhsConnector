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
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el segundo recurso registrado (units_schema)
        resource_func = mock_mcp.resource.call_args_list[1][0][1]

        result = await resource_func()

        assert "schema" in result
        assert "definitions" in result
        assert "description" in result
        assert "version" in result
        assert "api_endpoint" in result
        assert "supported_operations" in result

        # Verificar estructura del esquema de unidades
        schema = result["schema"]
        assert "id" in schema
        assert "name" in schema
        assert "unitCode" in schema
        assert "nodeId" in schema
        assert "unitType" in schema
        assert "maxOccupancy" in schema
        assert "bedrooms" in schema
        assert "bathrooms" in schema

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_system_status_resource(self, mock_mcp, mock_api_client):
        """Test recurso de estado del sistema"""
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el tercer recurso registrado (system_status)
        resource_func = mock_mcp.resource.call_args_list[2][0][1]

        result = await resource_func()

        assert "status" in result
        assert "timestamp" in result
        assert "version" in result
        assert "uptime" in result
        assert "components" in result

        # Verificar componentes del sistema
        components = result["components"]
        assert "api" in components
        assert "database" in components
        assert "authentication" in components
        assert "logging" in components

        # Verificar que cada componente tiene status
        for component_name, component_data in components.items():
            assert "status" in component_data
            assert "last_check" in component_data

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_documentation_resource(self, mock_mcp, mock_api_client):
        """Test recurso de documentación de API"""
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el cuarto recurso registrado (api_documentation)
        resource_func = mock_mcp.resource.call_args_list[3][0][1]

        result = await resource_func()

        assert "title" in result
        assert "version" in result
        assert "description" in result
        assert "base_url" in result
        assert "authentication" in result
        assert "endpoints" in result
        assert "examples" in result
        assert "rate_limits" in result
        assert "error_codes" in result

        # Verificar endpoints
        endpoints = result["endpoints"]
        assert "search_reservations" in endpoints

        search_endpoint = endpoints["search_reservations"]
        assert "method" in search_endpoint
        assert "path" in search_endpoint
        assert "description" in search_endpoint
        assert "parameters" in search_endpoint
        assert "responses" in search_endpoint

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_endpoints_resource(self, mock_mcp, mock_api_client):
        """Test recurso de endpoints API V2"""
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el quinto recurso registrado (api_v2_endpoints)
        resource_func = mock_mcp.resource.call_args_list[4][0][1]

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
        assert "get" in reservations_endpoint
        assert "create" in reservations_endpoint
        assert "update" in reservations_endpoint
        assert "delete" in reservations_endpoint

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_parameters_resource(self, mock_mcp, mock_api_client):
        """Test recurso de parámetros API V2"""
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el sexto recurso registrado (api_v2_parameters)
        resource_func = mock_mcp.resource.call_args_list[5][0][1]

        result = await resource_func()

        assert "parameters" in result
        assert "categories" in result
        assert "validation_rules" in result
        assert "examples" in result

        # Verificar categorías de parámetros
        categories = result["categories"]
        assert "pagination" in categories
        assert "filtering" in categories
        assert "sorting" in categories
        assert "search" in categories
        assert "date_range" in categories
        assert "special" in categories

        # Verificar parámetros de paginación
        pagination_params = categories["pagination"]
        assert "page" in pagination_params
        assert "size" in pagination_params

        # Verificar parámetros de filtrado
        filtering_params = categories["filtering"]
        assert "node_id" in filtering_params
        assert "unit_id" in filtering_params
        assert "status" in filtering_params

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_examples_resource(self, mock_mcp, mock_api_client):
        """Test recurso de ejemplos API V2"""
        mock_mcp.resource = Mock()
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener el séptimo recurso registrado (api_v2_examples)
        resource_func = mock_mcp.resource.call_args_list[6][0][1]

        result = await resource_func()

        assert "examples" in result
        assert "categories" in result
        assert "use_cases" in result

        # Verificar categorías de ejemplos
        categories = result["categories"]
        assert "basic_search" in categories
        assert "advanced_filtering" in categories
        assert "date_range_queries" in categories
        assert "pagination_examples" in categories
        assert "error_handling" in categories

        # Verificar ejemplos básicos
        basic_examples = categories["basic_search"]
        assert len(basic_examples) > 0

        for example in basic_examples:
            assert "description" in example
            assert "parameters" in example
            assert "expected_response" in example

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
