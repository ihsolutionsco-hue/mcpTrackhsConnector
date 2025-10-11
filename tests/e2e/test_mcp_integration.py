"""
Tests E2E para integración MCP completa
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig


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
        with patch("src.trackhs_mcp.core.api_client.TrackHSAuth") as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {
                "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            return TrackHSApiClient(mock_config)

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
        from src.trackhs_mcp.prompts import register_all_prompts
        from src.trackhs_mcp.resources import register_all_resources
        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)
        register_all_resources(mock_mcp, mock_api_client)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron componentes
        assert mock_mcp.tool.call_count >= 1
        assert mock_mcp.resource.call_count >= 7
        assert mock_mcp.prompt.call_count >= 8

        # Simular uso de herramienta
        tool_func = mock_mcp.tool.call_args_list[0][0][1]
        result = await tool_func(page=1, size=10)

        assert result == sample_search_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_tool_execution_with_error_handling(self, mock_mcp, mock_api_client):
        """Test ejecución de herramienta con manejo de errores"""
        # Configurar error en API
        mock_api_client.get.side_effect = Exception("API Error")

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # La herramienta debe manejar el error
        with pytest.raises(Exception):
            await tool_func(page=1, size=10)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_resource_access(self, mock_mcp, mock_api_client):
        """Test acceso a recursos"""
        mcp = Mock()
        mock_mcp.resource = Mock()

        from src.trackhs_mcp.resources import register_all_resources

        register_all_resources(mock_mcp, mock_api_client)

        # Obtener función de recurso
        resource_func = mock_mcp.resource.call_args_list[0][0][1]

        # Ejecutar recurso
        result = await resource_func()

        assert "schema" in result or "status" in result or "endpoints" in result

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_prompt_usage(self, mock_mcp, mock_api_client):
        """Test uso de prompts"""
        mcp = Mock()
        mock_mcp.prompt = Mock()

        from src.trackhs_mcp.prompts import register_all_prompts

        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener función de prompt
        prompt_func = mock_mcp.prompt.call_args_list[0][0][1]

        # Ejecutar prompt
        result = await prompt_func()

        assert "messages" in result
        assert len(result["messages"]) > 0
        assert result["messages"][0]["role"] == "user"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_search_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo completo de búsqueda"""
        mock_api_client.get.return_value = sample_search_response

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Ejecutar búsqueda con parámetros completos
        result = await tool_func(
            page=1,
            size=10,
            search="test",
            node_id=1,
            status="Confirmed",
            arrival_start="2024-01-01T00:00:00Z",
            arrival_end="2024-01-31T23:59:59Z",
        )

        assert result == sample_search_response
        assert len(result["_embedded"]["reservations"]) == 1
        assert result["total_items"] == 1

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

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Ejecutar primera página
        result1 = await tool_func(page=1, size=1)
        assert result1["page"] == 1
        assert len(result1["_embedded"]["reservations"]) == 1

        # Ejecutar segunda página
        result2 = await tool_func(page=2, size=1)
        assert result2["page"] == 2
        assert len(result2["_embedded"]["reservations"]) == 1

        # Verificar que se hicieron 2 llamadas
        assert mock_api_client.get.call_count == 2

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

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Primera llamada debe fallar
        with pytest.raises(Exception):
            await tool_func(page=1, size=10)

        # Segunda llamada debe tener éxito
        result = await tool_func(page=1, size=10)
        assert result["total_items"] == 0

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_concurrent_requests(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test requests concurrentes"""
        mock_api_client.get.return_value = sample_search_response

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Ejecutar múltiples requests concurrentes
        tasks = [tool_func(page=1, size=10, search=f"search_{i}") for i in range(5)]

        results = await asyncio.gather(*tasks)

        # Verificar que todos los requests fueron exitosos
        assert len(results) == 5
        for result in results:
            assert result == sample_search_response

        # Verificar que se hicieron 5 llamadas al API
        assert mock_api_client.get.call_count == 5

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_mcp_ecosystem(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test ecosistema MCP completo"""
        mock_api_client.get.return_value = sample_search_response

        # Crear servidor MCP completo
        mcp = Mock()
        mock_mcp.tool = Mock()
        mock_mcp.resource = Mock()
        mock_mcp.prompt = Mock()

        # Registrar todos los componentes
        from src.trackhs_mcp.prompts import register_all_prompts
        from src.trackhs_mcp.resources import register_all_resources
        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)
        register_all_resources(mock_mcp, mock_api_client)
        register_all_prompts(mock_mcp, mock_api_client)

        # Simular flujo completo de trabajo
        # 1. Usar herramienta de búsqueda
        tool_func = mock_mcp.tool.call_args_list[0][0][1]
        search_result = await tool_func(page=1, size=10)
        assert search_result == sample_search_response

        # 2. Acceder a recursos
        resource_func = mock_mcp.resource.call_args_list[0][0][1]
        resource_result = await resource_func()
        assert "schema" in resource_result or "status" in resource_result

        # 3. Usar prompts
        prompt_func = mock_mcp.prompt.call_args_list[0][0][1]
        prompt_result = await prompt_func()
        assert "messages" in prompt_result

        # Verificar que se registraron todos los componentes
        assert mock_mcp.tool.call_count >= 1
        assert mock_mcp.resource.call_count >= 7
        assert mock_mcp.prompt.call_count >= 8

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_validation_workflow(self, mock_mcp, mock_api_client):
        """Test flujo de validación"""
        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Test validaciones
        with pytest.raises(Exception):  # ValidationError
            await tool_func(page=0, size=10)  # Página inválida

        with pytest.raises(Exception):  # ValidationError
            await tool_func(page=1, size=0)  # Tamaño inválido

        with pytest.raises(Exception):  # ValidationError
            await tool_func(
                page=1, size=10, arrival_start="invalid-date"
            )  # Fecha inválida

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_performance_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo de rendimiento"""
        import time

        mock_api_client.get.return_value = sample_search_response

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Medir tiempo de ejecución
        start_time = time.time()
        result = await tool_func(page=1, size=10)
        end_time = time.time()

        execution_time = end_time - start_time

        # Verificar que la ejecución fue rápida (menos de 1 segundo)
        assert execution_time < 1.0
        assert result == sample_search_response

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_memory_usage_workflow(
        self, mock_mcp, mock_api_client, sample_search_response
    ):
        """Test flujo de uso de memoria"""
        import os

        import psutil

        # Obtener uso de memoria inicial
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        mock_api_client.get.return_value = sample_search_response

        mcp = Mock()
        mock_mcp.tool = Mock()

        from src.trackhs_mcp.tools import register_all_tools

        register_all_tools(mock_mcp, mock_api_client)

        tool_func = mock_mcp.tool.call_args_list[0][0][1]

        # Ejecutar múltiples operaciones
        for i in range(100):
            result = await tool_func(page=1, size=10, search=f"test_{i}")
            assert result == sample_search_response

        # Verificar que no hay fuga de memoria significativa
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # El aumento de memoria debe ser razonable (menos de 10MB)
        assert memory_increase < 10 * 1024 * 1024
