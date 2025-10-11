"""
Tests de integración para prompts MCP
"""

# datetime imports removed - not used
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

        # Verificar que se registraron múltiples prompts
        assert mock_mcp.prompt.call_count >= 5  # Al menos 5 prompts esperados

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_check_today_reservations_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de verificación de reservas del día"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener la función registrada
        prompt_func = registered_functions["check-today-reservations"]

        result = await prompt_func()

        assert "messages" in result
        assert len(result["messages"]) == 1

        message = result["messages"][0]
        assert message["role"] == "user"
        assert "content" in message
        assert "type" in message["content"]
        assert message["content"]["type"] == "text"
        assert "text" in message["content"]

        text_content = message["content"]["text"]
        assert "reservas" in text_content.lower()
        assert "fecha" in text_content.lower()
        assert "search_reservations" in text_content
        assert "arrivalStart" in text_content
        assert "arrivalEnd" in text_content
        assert "departureStart" in text_content
        assert "departureEnd" in text_content
        assert "inHouseToday" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_check_today_reservations_prompt_with_date(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de verificación de reservas con fecha específica"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        prompt_func = registered_functions["check-today-reservations"]

        result = await prompt_func(date="2024-01-15")

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "2024-01-15" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_unit_availability_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de disponibilidad de unidades"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener la función registrada
        prompt_func = registered_functions["unit-availability"]

        result = await prompt_func(check_in="2024-01-15", check_out="2024-01-20")

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "disponibilidad" in text_content.lower()
        assert "unidades" in text_content.lower()
        assert "search_reservations" in text_content
        assert "unitId" in text_content
        assert "arrivalStart" in text_content
        assert "arrivalEnd" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_unit_availability_prompt_with_parameters(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de disponibilidad con parámetros específicos"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener la función registrada
        prompt_func = registered_functions["unit-availability"]

        result = await prompt_func(
            start_date="2024-01-15", end_date="2024-01-20", unit_type="apartment"
        )

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "2024-01-15" in text_content
        assert "2024-01-20" in text_content
        assert "apartment" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_guest_contact_info_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de información de contacto de huéspedes"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener la función registrada
        prompt_func = registered_functions["guest-contact-info"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "contacto" in text_content.lower()
        assert "huésped" in text_content.lower()
        assert "search_reservations" in text_content
        assert "contactId" in text_content
        assert "información" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_guest_contact_info_prompt_with_contact_id(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de información de contacto con ID específico"""
        registered_functions = self.setup_prompt_mock(mock_mcp)
        register_all_prompts(mock_mcp, mock_api_client)

        # Obtener la función registrada
        prompt_func = registered_functions["guest-contact-info"]

        result = await prompt_func(contact_id=123)

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "123" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_maintenance_summary_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de resumen de mantenimiento"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["maintenance-summary"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "mantenimiento" in text_content.lower()
        assert "resumen" in text_content.lower()
        assert "search_reservations" in text_content
        assert "unidades" in text_content.lower()
        assert "estado" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_maintenance_summary_prompt_with_date_range(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de resumen de mantenimiento con rango de fechas"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["maintenance-summary"]

        result = await prompt_func(start_date="2024-01-01", end_date="2024-01-31")

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "2024-01-01" in text_content
        assert "2024-01-31" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_financial_analysis_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de análisis financiero"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["financial-analysis"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "análisis" in text_content.lower()
        assert "financiero" in text_content.lower()
        assert "search_reservations" in text_content
        assert "ingresos" in text_content.lower()
        assert "reservas" in text_content.lower()
        assert "rentabilidad" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_financial_analysis_prompt_with_period(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de análisis financiero con período específico"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["financial-analysis"]

        result = await prompt_func(
            start_date="2024-01-01", end_date="2024-03-31", analysis_type="quarterly"
        )

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "2024-01-01" in text_content
        assert "2024-03-31" in text_content
        assert "quarterly" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_advanced_reservation_search_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de búsqueda avanzada de reservas"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["advanced-reservation-search"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "búsqueda" in text_content.lower()
        assert "avanzada" in text_content.lower()
        assert "reservas" in text_content.lower()
        assert "search_reservations" in text_content
        assert "filtros" in text_content.lower()
        assert "parámetros" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_advanced_reservation_search_prompt_with_criteria(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de búsqueda avanzada con criterios específicos"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["advanced-reservation-search"]

        result = await prompt_func(
            search_criteria={
                "status": ["Confirmed", "Hold"],
                "unit_type": "apartment",
                "date_range": "2024-01-01 to 2024-12-31",
            }
        )

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "Confirmed" in text_content
        assert "Hold" in text_content
        assert "apartment" in text_content.lower()
        assert "2024-01-01" in text_content
        assert "2024-12-31" in text_content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_reservation_analytics_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de análisis de reservas"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["reservation-analytics"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "análisis" in text_content.lower()
        assert "reservas" in text_content.lower()
        assert "métricas" in text_content.lower()
        assert "search_reservations" in text_content
        assert "tendencias" in text_content.lower()
        assert "estadísticas" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_reservation_analytics_prompt_with_metrics(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de análisis con métricas específicas"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["reservation-analytics"]

        result = await prompt_func(
            metrics=["occupancy_rate", "revenue", "cancellation_rate"], period="monthly"
        )

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "occupancy_rate" in text_content
        assert "revenue" in text_content
        assert "cancellation_rate" in text_content
        assert "monthly" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_guest_experience_analysis_prompt(self, mock_mcp, mock_api_client):
        """Test prompt de análisis de experiencia del huésped"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["guest-experience-analysis"]

        result = await prompt_func()

        assert "messages" in result
        message = result["messages"][0]
        assert message["role"] == "user"

        text_content = message["content"]["text"]
        assert "experiencia" in text_content.lower()
        assert "huésped" in text_content.lower()
        assert "análisis" in text_content.lower()
        assert "search_reservations" in text_content
        assert "satisfacción" in text_content.lower()
        assert "comentarios" in text_content.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_guest_experience_analysis_prompt_with_focus(
        self, mock_mcp, mock_api_client
    ):
        """Test prompt de análisis de experiencia con enfoque específico"""
        registered_functions = self.setup_prompt_mock(mock_mcp)

        register_all_prompts(mock_mcp, mock_api_client)



        # Obtener la función registrada

        prompt_func = registered_functions["guest-experience-analysis"]

        result = await prompt_func(
            focus_area="check_in_process", time_period="last_30_days"
        )

        assert "messages" in result
        message = result["messages"][0]
        text_content = message["content"]["text"]
        assert "check_in_process" in text_content
        assert "last_30_days" in text_content

    @pytest.mark.integration
    def test_prompt_registration_count(self, mock_mcp, mock_api_client):
        """Test que se registran todos los prompts esperados"""
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron al menos 8 prompts
        assert mock_mcp.prompt.call_count >= 8

        # Verificar que cada prompt tiene un nombre único
        prompt_names = [call[0][0] for call in mock_mcp.prompt.call_args_list]
        assert len(set(prompt_names)) == len(
            prompt_names
        ), "Prompt names should be unique"

    @pytest.mark.integration
    def test_prompt_names(self, mock_mcp, mock_api_client):
        """Test nombres de prompts"""
        register_all_prompts(mock_mcp, mock_api_client)

        prompt_names = [call[0][0] for call in mock_mcp.prompt.call_args_list]

        expected_names = [
            "check-today-reservations",
            "unit-availability",
            "guest-contact-info",
            "maintenance-summary",
            "financial-analysis",
            "advanced-reservation-search",
            "reservation-analytics",
            "guest-experience-analysis",
        ]

        for expected_name in expected_names:
            assert (
                expected_name in prompt_names
            ), f"Prompt {expected_name} should be registered"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_prompts_with_api_client_calls(self, mock_mcp, mock_api_client):
        """Test prompts que pueden hacer llamadas al API client"""
        # Configurar mock para llamadas específicas
        mock_api_client.get.return_value = {"data": "test_response"}

        mock_mcp.prompt = Mock()
        register_all_prompts(mock_mcp, mock_api_client)

        # Test que los prompts se pueden ejecutar sin errores
        for call in mock_mcp.prompt.call_args_list:
            prompt_func = call[0][1]
            result = await prompt_func()

            assert "messages" in result
            assert len(result["messages"]) > 0
            assert result["messages"][0]["role"] == "user"
