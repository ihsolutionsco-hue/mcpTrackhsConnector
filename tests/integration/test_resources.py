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

        # Verificar que se registraron exactamente 2 recursos
        assert mock_mcp.resource.call_count == 2  # 2 recursos esperados

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
        assert "id" in result["schema"]
        assert "status" in result["schema"]
        assert "arrival_date" in result["schema"]
        assert "departure_date" in result["schema"]
        assert "unit_id" in result["schema"]
        assert "description" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_documentation_resource(self, mock_mcp, mock_api_client):
        """Test recurso de documentación de API"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Obtener la función registrada
        resource_func = registered_functions["trackhs://api/documentation"]

        result = await resource_func()

        assert isinstance(result, str)
        assert "TrackHS API V2 Documentation" in result
        assert "Endpoints Principales" in result
        assert "API V2" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_resources_with_api_client_calls(self, mock_mcp, mock_api_client):
        """Test recursos con llamadas al API client"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron los recursos esperados
        assert "trackhs://schema/reservations" in registered_functions
        assert "trackhs://api/documentation" in registered_functions

        # Test que los recursos funcionan
        schema_func = registered_functions["trackhs://schema/reservations"]
        doc_func = registered_functions["trackhs://api/documentation"]

        schema_result = await schema_func()
        doc_result = await doc_func()

        assert isinstance(schema_result, dict)
        assert isinstance(doc_result, str)

    @pytest.mark.integration
    def test_resource_registration_count(self, mock_mcp, mock_api_client):
        """Test que se registran todos los recursos esperados"""
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron exactamente 2 recursos
        assert mock_mcp.resource.call_count == 2

    @pytest.mark.integration
    def test_resource_names(self, mock_mcp, mock_api_client):
        """Test nombres de recursos"""
        register_all_resources(mock_mcp, mock_api_client)

        resource_names = [call[0][0] for call in mock_mcp.resource.call_args_list]

        expected_names = [
            "trackhs://schema/reservations",
            "trackhs://api/documentation",
        ]

        for expected_name in expected_names:
            assert (
                expected_name in resource_names
            ), f"Resource {expected_name} should be registered"
