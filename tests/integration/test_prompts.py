"""
Tests de integración para prompts MCP
"""

import pytest

from src.trackhs_mcp.infrastructure.mcp.prompts import create_search_reservations_prompt


class TestPromptsIntegration:
    """Tests de integración para prompts MCP"""

    @pytest.mark.integration
    def test_create_search_reservations_prompt(self):
        """Test creación de prompt de búsqueda de reservas"""
        filters = {"status": "Confirmed", "arrival_start": "2024-01-01"}
        result = create_search_reservations_prompt(filters, include_financials=True)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"

    @pytest.mark.integration
    def test_search_reservations_prompt_with_dates(self):
        """Test prompt de búsqueda con fechas"""
        filters = {
            "arrival_start": "2024-01-01",
            "arrival_end": "2024-01-31",
            "status": "Confirmed",
        }
        result = create_search_reservations_prompt(filters, include_financials=False)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        assert "2024-01-01" in result["messages"][0]["content"]["text"]
        assert "2024-01-31" in result["messages"][0]["content"]["text"]

    @pytest.mark.integration
    def test_search_reservations_prompt_with_guest(self):
        """Test prompt de búsqueda con información de huésped"""
        filters = {
            "guest_name": "John Doe",
            "contact_id": "12345",
            "email": "john@example.com",
        }
        result = create_search_reservations_prompt(filters, include_financials=True)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "John Doe" in text_content
        assert "12345" in text_content
        assert "john@example.com" in text_content

    @pytest.mark.integration
    def test_search_reservations_prompt_advanced(self):
        """Test prompt de búsqueda avanzada"""
        filters = {
            "search_term": "VIP",
            "status": "Confirmed",
            "node_id": "123",
            "include_financials": True,
            "scroll_mode": False,
        }
        result = create_search_reservations_prompt(
            filters, include_financials=True, scroll_mode=True
        )

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "VIP" in text_content
        assert "Confirmed" in text_content

    @pytest.mark.integration
    def test_search_reservations_prompt_scroll_mode(self):
        """Test prompt con modo scroll"""
        filters = {"status": "Confirmed"}
        result = create_search_reservations_prompt(filters, scroll_mode=True)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "scroll" in text_content.lower()

    @pytest.mark.integration
    def test_search_reservations_prompt_financials(self):
        """Test prompt con información financiera"""
        filters = {"status": "Confirmed"}
        result = create_search_reservations_prompt(filters, include_financials=True)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"
        text_content = result["messages"][0]["content"]["text"]
        assert "financial" in text_content.lower() or "revenue" in text_content.lower()
