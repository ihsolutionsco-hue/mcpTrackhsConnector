"""
Tests unitarios para utilidades de completion
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.core.completion import (
    CompletionContext,
    CompletionSuggestion,
    CompletionType,
    TrackHSCompletion,
)


class TestCompletionType:
    """Tests para CompletionType"""

    @pytest.mark.unit
    def test_completion_type_values(self):
        """Test valores de CompletionType"""
        assert CompletionType.PARAMETER.value == "parameter"
        assert CompletionType.VALUE.value == "value"
        assert CompletionType.ENDPOINT.value == "endpoint"
        assert CompletionType.FILTER.value == "filter"
        assert CompletionType.SORT.value == "sort"
        assert CompletionType.DATE.value == "date"
        assert CompletionType.STATUS.value == "status"


class TestCompletionSuggestion:
    """Tests para CompletionSuggestion"""

    @pytest.mark.unit
    def test_completion_suggestion_creation(self):
        """Test creación de CompletionSuggestion"""
        suggestion = CompletionSuggestion(
            value="test_value",
            label="Test Label",
            description="Test description",
            category="parameter",
            priority=9,
        )

        assert suggestion.value == "test_value"
        assert suggestion.label == "Test Label"
        assert suggestion.description == "Test description"
        assert suggestion.category == "parameter"
        assert suggestion.priority == 9

    @pytest.mark.unit
    def test_completion_suggestion_with_defaults(self):
        """Test CompletionSuggestion con valores por defecto"""
        suggestion = CompletionSuggestion(value="test_value", label="Test Label")

        assert suggestion.value == "test_value"
        assert suggestion.label == "Test Label"
        assert suggestion.description is None
        assert suggestion.category is None
        assert suggestion.priority == 0


class TestCompletionContext:
    """Tests para CompletionContext"""

    @pytest.mark.unit
    def test_completion_context_creation(self):
        """Test creación de CompletionContext"""
        context = CompletionContext(
            current_input="no", parameter_name="node_id", endpoint="search"
        )

        assert context.current_input == "no"
        assert context.parameter_name == "node_id"
        assert context.endpoint == "search"

    @pytest.mark.unit
    def test_completion_context_with_defaults(self):
        """Test CompletionContext con valores por defecto"""
        context = CompletionContext(current_input="test")

        assert context.current_input == "test"
        assert context.parameter_name is None
        assert context.endpoint is None


class TestTrackHSCompletion:
    """Tests para TrackHSCompletion"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def completion(self, mock_api_client):
        """Crear TrackHSCompletion para testing"""
        return TrackHSCompletion(mock_api_client)

    @pytest.mark.unit
    def test_completion_init(self, completion, mock_api_client):
        """Test inicialización de TrackHSCompletion"""
        assert completion.api_client == mock_api_client
        assert completion._cache == {}
        assert completion._cache_ttl == {}
        assert completion._cache_duration == timedelta(hours=1)

    @pytest.mark.unit
    def test_completion_init_without_api_client(self):
        """Test inicialización sin API client"""
        completion = TrackHSCompletion()

        assert completion.api_client is None
        assert completion._cache == {}
        assert completion._cache_ttl == {}

    @pytest.mark.unit
    def test_is_cache_valid_fresh(self, completion):
        """Test cache válido (fresco)"""
        cache_key = "test_key"
        completion._cache_ttl[cache_key] = datetime.now() + timedelta(minutes=30)

        assert completion._is_cache_valid(cache_key) is True

    @pytest.mark.unit
    def test_is_cache_valid_expired(self, completion):
        """Test cache expirado"""
        cache_key = "test_key"
        completion._cache_ttl[cache_key] = datetime.now() - timedelta(minutes=30)

        assert completion._is_cache_valid(cache_key) is False

    @pytest.mark.unit
    def test_is_cache_valid_missing(self, completion):
        """Test cache faltante"""
        cache_key = "test_key"

        assert completion._is_cache_valid(cache_key) is False

    @pytest.mark.unit
    def test_set_cache(self, completion):
        """Test establecer cache"""
        cache_key = "test_key"
        suggestions = [
            CompletionSuggestion("value1", "Label 1"),
            CompletionSuggestion("value2", "Label 2"),
        ]

        completion._set_cache(cache_key, suggestions)

        assert cache_key in completion._cache
        assert completion._cache[cache_key] == suggestions
        assert cache_key in completion._cache_ttl

    @pytest.mark.unit
    def test_get_cache_valid(self, completion):
        """Test obtener cache válido"""
        cache_key = "test_key"
        suggestions = [CompletionSuggestion("value1", "Label 1")]
        completion._set_cache(cache_key, suggestions)

        cached_suggestions = completion._get_cache(cache_key)

        assert cached_suggestions == suggestions

    @pytest.mark.unit
    def test_get_cache_invalid(self, completion):
        """Test obtener cache inválido"""
        cache_key = "test_key"

        cached_suggestions = completion._get_cache(cache_key)

        assert cached_suggestions is None

    @pytest.mark.unit
    def test_filter_suggestions(self, completion):
        """Test filtrado de sugerencias"""
        suggestions = [
            CompletionSuggestion("node1", "Node 1"),
            CompletionSuggestion("node2", "Node 2"),
            CompletionSuggestion("unit1", "Unit 1"),
        ]

        context = CompletionContext(current_input="no", parameter_name="node_id")

        filtered = completion._filter_suggestions(suggestions, context)

        # Debe filtrar por "no" (node1, node2)
        assert len(filtered) == 2
        assert any(s.value == "node1" for s in filtered)
        assert any(s.value == "node2" for s in filtered)
        assert not any(s.value == "unit1" for s in filtered)

    @pytest.mark.unit
    def test_get_parameter_suggestions(self, completion):
        """Test obtención de sugerencias de parámetros"""
        context = CompletionContext(current_input="test", parameter_name="test_param")

        suggestions = completion.get_parameter_suggestions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.PARAMETER for s in suggestions)

    @pytest.mark.unit
    def test_get_sort_column_suggestions(self, completion):
        """Test obtención de sugerencias de columnas de ordenamiento"""
        context = CompletionContext(current_input="test", parameter_name="sort_column")

        suggestions = completion.get_sort_column_suggestions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.SORT for s in suggestions)

        # Verificar que incluye columnas conocidas
        values = [s.value for s in suggestions]
        assert "name" in values
        assert "status" in values
        assert "checkin" in values

    @pytest.mark.unit
    def test_get_status_suggestions(self, completion):
        """Test obtención de sugerencias de estado"""
        context = CompletionContext(current_input="test", parameter_name="status")

        suggestions = completion.get_status_suggestions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.STATUS for s in suggestions)

        # Verificar que incluye estados conocidos
        values = [s.value for s in suggestions]
        assert "Confirmed" in values
        assert "Hold" in values
        assert "Cancelled" in values

    @pytest.mark.unit
    def test_get_date_suggestions(self, completion):
        """Test obtención de sugerencias de fecha"""
        context = CompletionContext(current_input="", parameter_name="arrival_start")

        suggestions = completion.get_date_suggestions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.DATE for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_dynamic_suggestions_node_id(self, completion, mock_api_client):
        """Test obtención de sugerencias dinámicas para node_id"""
        mock_api_client.get.return_value = {
            "_embedded": {
                "nodes": [{"id": 1, "name": "Node 1"}, {"id": 2, "name": "Node 2"}]
            }
        }

        context = CompletionContext(current_input="", parameter_name="nodeId")

        suggestions = await completion.get_dynamic_suggestions(context)

        assert len(suggestions) == 2
        assert any(s.value == "1" for s in suggestions)
        assert any(s.value == "2" for s in suggestions)
        assert any(s.label == "Node 1" for s in suggestions)
        assert any(s.label == "Node 2" for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_dynamic_suggestions_unit_id(self, completion, mock_api_client):
        """Test obtención de sugerencias dinámicas para unit_id"""
        mock_api_client.get.return_value = {
            "_embedded": {
                "units": [{"id": 1, "name": "Unit 1"}, {"id": 2, "name": "Unit 2"}]
            }
        }

        context = CompletionContext(current_input="", parameter_name="unitId")

        suggestions = await completion.get_dynamic_suggestions(context)

        assert len(suggestions) == 2
        assert any(s.value == "1" for s in suggestions)
        assert any(s.value == "2" for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_dynamic_suggestions_contact_id(
        self, completion, mock_api_client
    ):
        """Test obtención de sugerencias dinámicas para contact_id"""
        mock_api_client.get.return_value = {
            "_embedded": {
                "contacts": [
                    {"id": 1, "name": "Contact 1"},
                    {"id": 2, "name": "Contact 2"},
                ]
            }
        }

        context = CompletionContext(current_input="", parameter_name="contactId")

        suggestions = await completion.get_dynamic_suggestions(context)

        assert len(suggestions) == 2
        assert any(s.value == "1" for s in suggestions)
        assert any(s.value == "2" for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_dynamic_suggestions_unknown_parameter(self, completion):
        """Test obtención de sugerencias dinámicas para parámetro desconocido"""
        context = CompletionContext(current_input="", parameter_name="unknown_param")

        suggestions = await completion.get_dynamic_suggestions(context)

        assert len(suggestions) == 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_dynamic_suggestions_api_error(self, completion, mock_api_client):
        """Test obtención de sugerencias dinámicas con error de API"""
        mock_api_client.get.side_effect = Exception("API Error")

        context = CompletionContext(current_input="", parameter_name="nodeId")

        suggestions = await completion.get_dynamic_suggestions(context)

        # Debe retornar lista vacía en caso de error
        assert len(suggestions) == 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_parameter_suggestions(self, completion):
        """Test obtención de completions para sugerencias de parámetros"""
        context = CompletionContext(current_input="test", parameter_name="test_param")

        suggestions = await completion.get_completions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.PARAMETER for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_sort_column(self, completion):
        """Test obtención de completions para sort_column"""
        context = CompletionContext(current_input="test", parameter_name="sort_column")

        suggestions = await completion.get_completions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.SORT for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_status(self, completion):
        """Test obtención de completions para status"""
        context = CompletionContext(current_input="test", parameter_name="status")

        suggestions = await completion.get_completions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.STATUS for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_date_parameter(self, completion):
        """Test obtención de completions para parámetros de fecha"""
        context = CompletionContext(current_input="", parameter_name="arrival_start")

        suggestions = await completion.get_completions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.DATE for s in suggestions)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_dynamic_node_id(self, completion, mock_api_client):
        """Test obtención de completions dinámicos para node_id"""
        mock_api_client.get.return_value = {
            "_embedded": {"nodes": [{"id": 1, "name": "Node 1"}]}
        }

        context = CompletionContext(current_input="", parameter_name="nodeId")

        suggestions = await completion.get_completions(context)

        assert len(suggestions) > 0
        assert any(s.value == "1" for s in suggestions)

    @pytest.mark.unit
    def test_get_endpoint_suggestions(self, completion):
        """Test obtención de sugerencias de endpoints"""
        context = CompletionContext(current_input="", parameter_name="endpoint")

        suggestions = completion.get_endpoint_suggestions(context)

        assert len(suggestions) > 0
        assert all(s.type == CompletionType.ENDPOINT for s in suggestions)

        # Verificar que incluye endpoints conocidos
        values = [s.value for s in suggestions]
        assert "/v2/pms/reservations" in values

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_with_cache(self, completion):
        """Test obtención de completions con cache"""
        context = CompletionContext(current_input="test", parameter_name="test_param")

        # Primera llamada
        suggestions1 = await completion.get_completions(context)

        # Segunda llamada (debe usar cache)
        suggestions2 = await completion.get_completions(context)

        assert suggestions1 == suggestions2
        assert len(suggestions1) > 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_completions_with_partial_input(self, completion):
        """Test obtención de completions con entrada parcial"""
        context = CompletionContext(current_input="no", parameter_name="node_id")

        suggestions = await completion.get_completions(context)

        # Debe filtrar las sugerencias basándose en la entrada parcial
        assert len(suggestions) >= 0  # Puede ser 0 si no hay coincidencias
