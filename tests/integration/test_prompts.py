"""
Tests de integración para prompts MCP
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.mcp.prompts import register_all_prompts


class TestPromptsIntegration:
    """Tests de integración para prompts MCP"""

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
        mcp.prompt = Mock()
        return mcp

    def setup_prompt_mock(self, mock_mcp):
        """Configura un mock que funcione como decorador de prompts"""
        registered_functions = {}

        def mock_prompt_decorator(name):
            def decorator(func):
                registered_functions[name] = func
                return func

            return decorator

        mock_mcp.prompt = mock_prompt_decorator
        return registered_functions

    @pytest.mark.integration
    def test_register_all_prompts(self, mock_mcp, mock_api_client):
        """Test registro de todos los prompts"""
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron exactamente 3 prompts
        assert mock_mcp.prompt.call_count == 3  # 3 prompts esperados

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_by_dates_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de búsqueda por fechas"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que el prompt existe
        assert "search-reservations-by-dates" in registered_functions

        # Test con fechas específicas
        prompt_func = registered_functions["search-reservations-by-dates"]
        result = await prompt_func(
            start_date="2024-01-01", end_date="2024-01-31", date_type="arrival"
        )

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        assert "2024-01-01" in result["messages"][0]["content"]["text"]
        assert "2024-01-31" in result["messages"][0]["content"]["text"]
        assert "arrival" in result["messages"][0]["content"]["text"]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_by_guest_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de búsqueda por huésped"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que el prompt existe
        assert "search-reservations-by-guest" in registered_functions

        # Test con parámetros de huésped
        prompt_func = registered_functions["search-reservations-by-guest"]
        result = await prompt_func(
            guest_name="John Doe", contact_id="12345", email="john@example.com"
        )

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "John Doe" in text_content
        assert "12345" in text_content
        assert "john@example.com" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_advanced_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de búsqueda avanzada"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que el prompt existe
        assert "search-reservations-advanced" in registered_functions

        # Test con filtros avanzados
        prompt_func = registered_functions["search-reservations-advanced"]
        result = await prompt_func(
            search_term="VIP",
            status="Confirmed",
            node_id="123",
            include_financials=True,
            scroll_mode=False,
        )

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "VIP" in text_content
        assert "Confirmed" in text_content
        assert "123" in text_content
        assert "Sí" in text_content  # include_financials=True
        assert "Paginación estándar" in text_content  # scroll_mode=False

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_prompt_content_structure(self, mock_mcp, mock_api_client):
        """Test estructura de contenido de prompts"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Test estructura para search-reservations-by-dates
        prompt_func = registered_functions["search-reservations-by-dates"]
        result = await prompt_func("2024-01-01", "2024-01-31")

        assert "messages" in result
        assert len(result["messages"]) == 1

        message = result["messages"][0]
        assert message["role"] == "user"
        assert "content" in message
        assert "type" in message["content"]
        assert message["content"]["type"] == "text"
        assert "text" in message["content"]

        text_content = message["content"]["text"]
        assert "search_reservations" in text_content
        assert "arrivalStart" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_prompt_parameter_handling(self, mock_mcp, mock_api_client):
        """Test manejo de parámetros en prompts"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Test search-reservations-by-guest con parámetros opcionales
        prompt_func = registered_functions["search-reservations-by-guest"]

        # Test con todos los parámetros
        result = await prompt_func(
            guest_name="Jane Doe",
            contact_id="67890",
            email="jane@example.com",
            phone="555-1234",
        )

        text_content = result["messages"][0]["content"]["text"]
        assert "Jane Doe" in text_content
        assert "67890" in text_content
        assert "jane@example.com" in text_content
        assert "555-1234" in text_content

        # Test con parámetros mínimos
        result = await prompt_func(guest_name="Test Guest")
        text_content = result["messages"][0]["content"]["text"]
        assert "Test Guest" in text_content
        assert "Sin criterios específicos" not in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_prompt_instructions_content(self, mock_mcp, mock_api_client):
        """Test contenido de instrucciones en prompts"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Test search-reservations-advanced
        prompt_func = registered_functions["search-reservations-advanced"]
        result = await prompt_func(
            search_term="test", status="Confirmed", include_financials=True
        )

        text_content = result["messages"][0]["content"]["text"]

        # Verificar que contiene instrucciones específicas
        assert "search_reservations" in text_content
        assert "Instrucciones:" in text_content
        assert "Instrucciones:" in text_content
        assert "Información a Incluir:" in text_content
        assert "Formato de Respuesta:" in text_content
