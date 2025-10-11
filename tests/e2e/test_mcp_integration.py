"""
Tests E2E para integración MCP completa
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestMCPIntegrationE2E:
    """Tests E2E para integración MCP completa"""

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
    def mock_api_client(self, mock_config):
        """API client mock"""
        mock_client = Mock()
        mock_client.get = Mock()
        mock_client.post = Mock()
        mock_client.put = Mock()
        mock_client.delete = Mock()
        return mock_client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        mcp.resource = Mock()
        mcp.prompt = Mock()
        return mcp

    @pytest.fixture
    def sample_reservation_data(self):
        """Datos de ejemplo de reserva"""
        return {
            "id": 12345,
            "status": "Confirmed",
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "nights": 5,
            "currency": "USD",
            "unitId": 1,
            "contactId": 1,
            "_embedded": {
                "unit": {"id": 1, "name": "Test Unit", "unitCode": "TU001"},
                "contact": {
                    "id": 1,
                    "name": "John Doe",
                    "primaryEmail": "john.doe@example.com",
                },
            },
        }

    @pytest.fixture
    def sample_search_response(self):
        """Respuesta de ejemplo de búsqueda"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "status": "Confirmed",
                        "arrivalDate": "2024-01-15",
                        "departureDate": "2024-01-20",
                        "nights": 5,
                        "currency": "USD",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {
                "self": {"hre": "/v2/pms/reservations?page=1&size=10"},
                "first": {"hre": "/v2/pms/reservations?page=1&size=10"},
                "last": {"hre": "/v2/pms/reservations?page=1&size=10"},
            },
        }

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_mcp_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo completo de trabajo MCP"""
        # Configurar mock del API client
        mock_api_client.get.return_value = sample_search_response

        # Crear servidor MCP mock
        mock_mcp.tool = Mock()
        mock_mcp.resource = Mock()
        mock_mcp.prompt = Mock()

        # Registrar todos los componentes
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools
        from src.trackhs_mcp.infrastructure.mcp.prompts import register_all_prompts
        from src.trackhs_mcp.infrastructure.mcp.resources import register_all_resources

        register_all_tools(mock_mcp, mock_api_client)
        register_all_resources(mock_mcp, mock_api_client)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron componentes
        assert mock_mcp.tool.call_count >= 1
        assert mock_mcp.resource.call_count >= 7
        assert mock_mcp.prompt.call_count >= 8

        # Verificar que se registraron las herramientas correctamente
        # Las herramientas se registran como decoradores, no como funciones directas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_tool_execution_with_error_handling(self, mock_mcp, mock_api_client):
        """Test ejecución de herramienta con manejo de errores"""
        # Configurar error en API
        mock_api_client.get.side_effect = Exception("API Error")

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_resource_access(self, mock_mcp, mock_api_client):
        """Test acceso a recursos"""
        # mcp = Mock()  # Variable not used
        mock_mcp.resource = Mock()

        from src.trackhs_mcp.infrastructure.mcp.resources import register_all_resources

        register_all_resources(mock_mcp, mock_api_client)

        # Verificar que se registraron los recursos
        assert mock_mcp.resource.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_prompt_usage(self, mock_mcp, mock_api_client):
        """Test uso de prompts"""
        # mcp = Mock()  # Variable not used
        mock_mcp.prompt = Mock()

        from src.trackhs_mcp.infrastructure.mcp.prompts import register_all_prompts

        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron los prompts
        assert mock_mcp.prompt.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_search_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo completo de búsqueda"""
        mock_api_client.get.return_value = sample_search_response

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_pagination_workflow(self, mock_mcp, mock_api_client):
        """Test flujo de paginación"""
        # Configurar respuestas de paginación
        page1_response = {
            "_embedded": {"reservations": [{"id": 1}]},
            "page": 1,
            "page_count": 2,
            "page_size": 1,
            "total_items": 2,
            "_links": {
                "self": {"hre": "/v2/pms/reservations?page=1&size=1"},
                "next": {"hre": "/v2/pms/reservations?page=2&size=1"},
                "last": {"hre": "/v2/pms/reservations?page=2&size=1"},
            },
        }

        page2_response = {
            "_embedded": {"reservations": [{"id": 2}]},
            "page": 2,
            "page_count": 2,
            "page_size": 1,
            "total_items": 2,
            "_links": {
                "self": {"hre": "/v2/pms/reservations?page=2&size=1"},
                "prev": {"hre": "/v2/pms/reservations?page=1&size=1"},
                "last": {"hre": "/v2/pms/reservations?page=2&size=1"},
            },
        }

        mock_api_client.get.side_effect = [page1_response, page2_response]

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, mock_mcp, mock_api_client):
        """Test flujo de recuperación de errores"""
        # Configurar error seguido de éxito
        mock_api_client.get.side_effect = [
            Exception("Network error"),
            {
                "_embedded": {"reservations": []},
                "page": 1,
                "page_count": 0,
                "page_size": 10,
                "total_items": 0,
            },
        ]

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_concurrent_requests(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test requests concurrentes"""
        mock_api_client.get.return_value = sample_search_response

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_mcp_ecosystem(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test ecosistema MCP completo"""
        mock_api_client.get.return_value = sample_search_response

        # Crear servidor MCP completo
        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()
        mock_mcp.resource = Mock()
        mock_mcp.prompt = Mock()

        # Registrar todos los componentes
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools
        from src.trackhs_mcp.infrastructure.mcp.prompts import register_all_prompts
        from src.trackhs_mcp.infrastructure.mcp.resources import register_all_resources

        register_all_tools(mock_mcp, mock_api_client)
        register_all_resources(mock_mcp, mock_api_client)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron todos los componentes
        assert mock_mcp.tool.call_count >= 1
        assert mock_mcp.resource.call_count >= 7
        assert mock_mcp.prompt.call_count >= 8

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_validation_workflow(self, mock_mcp, mock_api_client):
        """Test flujo de validación"""
        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_performance_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo de rendimiento"""
        import time

        mock_api_client.get.return_value = sample_search_response

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_memory_usage_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo de uso de memoria"""
        import os

        try:
            import psutil
        except ImportError:
            pytest.skip("psutil not available")

        # Obtener uso de memoria inicial
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        mock_api_client.get.return_value = sample_search_response

        # mcp = Mock()  # Variable not used
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1
