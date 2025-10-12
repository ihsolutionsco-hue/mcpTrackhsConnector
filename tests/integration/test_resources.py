"""
Tests de integración para recursos MCP V1 y V2
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.resources import register_all_resources


class TestResourcesIntegration:
    """Tests de integración para recursos MCP V1 y V2"""

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

        # Verificar que se registraron exactamente 9 recursos (V1 y V2)
        assert mock_mcp.resource.call_count == 9  # 9 recursos esperados

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_reservations_v1_schema_resource(self, mock_mcp, mock_api_client):
        """Test recurso de esquema de reservas V1"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que el recurso de esquema V1 está registrado
        assert "trackhs://schema/reservations-v1" in registered_functions
        resource_func = registered_functions["trackhs://schema/reservations-v1"]

        # Ejecutar el recurso
        result = await resource_func()

        # Verificar que el resultado contiene el esquema
        assert "schema" in result
        assert "description" in result
        assert "version" in result
        assert "api_endpoint" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_reservations_v2_schema_resource(self, mock_mcp, mock_api_client):
        """Test recurso de esquema de reservas V2"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que el recurso de esquema V2 está registrado
        assert "trackhs://schema/reservations-v2" in registered_functions
        resource_func = registered_functions["trackhs://schema/reservations-v2"]

        # Ejecutar el recurso
        result = await resource_func()

        # Verificar que el resultado contiene el esquema
        assert "schema" in result
        assert "definitions" in result
        assert "description" in result
        assert "version" in result
        assert "api_endpoint" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v1_documentation_resource(self, mock_mcp, mock_api_client):
        """Test recurso de documentación API V1"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que el recurso de documentación V1 está registrado
        assert "trackhs://docs/api-v1" in registered_functions
        resource_func = registered_functions["trackhs://docs/api-v1"]

        # Ejecutar el recurso
        result = await resource_func()

        # Verificar que el resultado contiene documentación
        assert isinstance(result, str)
        assert "TrackHS API V1" in result
        assert "Endpoint Principal" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_api_v2_documentation_resource(self, mock_mcp, mock_api_client):
        """Test recurso de documentación API V2"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que el recurso de documentación V2 está registrado
        assert "trackhs://docs/api-v2" in registered_functions
        resource_func = registered_functions["trackhs://docs/api-v2"]

        # Ejecutar el recurso
        result = await resource_func()

        # Verificar que el resultado contiene documentación
        assert isinstance(result, str)
        assert "TrackHS API V2" in result
        assert "Endpoint Principal" in result

    @pytest.mark.integration
    def test_resource_registration_count(self, mock_mcp, mock_api_client):
        """Test que se registran la cantidad correcta de recursos"""
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron exactamente 9 recursos
        assert mock_mcp.resource.call_count == 9

    @pytest.mark.integration
    def test_resource_names(self, mock_mcp, mock_api_client):
        """Test que los recursos tienen los nombres correctos"""
        registered_functions = self.setup_resource_mock(mock_mcp)
        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que los recursos están registrados con los nombres correctos
        expected_resources = [
            "trackhs://schema/reservations-v1",
            "trackhs://schema/reservations-v2",
            "trackhs://docs/api-v1",
            "trackhs://docs/api-v2",
            "trackhs://docs/migration-guide",
            "trackhs://docs/examples",
            "trackhs://reference/parameters",
            "trackhs://reference/status-values",
            "trackhs://reference/date-formats",
        ]

        for resource_name in expected_resources:
            assert (
                resource_name in registered_functions
            ), f"Resource {resource_name} should be registered"
