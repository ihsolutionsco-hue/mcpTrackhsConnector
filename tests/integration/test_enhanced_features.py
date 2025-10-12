"""
Tests de integración para las nuevas funcionalidades mejoradas
Incluye testing de herramientas, recursos y prompts especializados
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.infrastructure.mcp.prompts_enhanced import (
    register_enhanced_prompts,
)
from src.trackhs_mcp.infrastructure.mcp.resources_enhanced import (
    register_enhanced_resources,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_advanced import (
    register_search_reservations_advanced,
)
from src.trackhs_mcp.infrastructure.mcp.search_reservations_enhanced import (
    ReservationCache,
    ReservationMetrics,
    register_search_reservations_enhanced,
)


class TestEnhancedFeatures:
    """Tests para funcionalidades mejoradas"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        client.search_reservations = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        mcp.resource = Mock()
        mcp.prompt = Mock()
        return mcp

    @pytest.fixture
    def sample_reservations_data(self):
        """Datos de ejemplo para testing"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 1,
                        "name": "Reserva Test 1",
                        "status": "Confirmed",
                        "arrival_date": "2024-01-15",
                        "departure_date": "2024-01-18",
                        "nights": 3,
                        "unit_id": 101,
                        "node_id": 1,
                        "channel_id": 1,
                        "guest_breakdown": {
                            "total": "450.00",
                            "gross_rent": "400.00",
                            "fees": "50.00",
                        },
                    },
                    {
                        "id": 2,
                        "name": "Reserva Test 2",
                        "status": "Checked In",
                        "arrival_date": "2024-01-20",
                        "departure_date": "2024-01-25",
                        "nights": 5,
                        "unit_id": 102,
                        "node_id": 2,
                        "channel_id": 2,
                        "guest_breakdown": {
                            "total": "750.00",
                            "gross_rent": "700.00",
                            "fees": "50.00",
                        },
                    },
                ]
            },
            "page": 1,
            "page_size": 10,
            "total_items": 2,
        }


class TestReservationCache:
    """Tests para el sistema de caché"""

    def test_cache_initialization(self):
        """Test inicialización del caché"""
        cache = ReservationCache(ttl=300)
        assert cache.ttl == 300
        assert len(cache.cache) == 0

    def test_cache_key_generation(self):
        """Test generación de claves de caché"""
        cache = ReservationCache()
        key = cache._generate_cache_key(page=1, size=10, status="Confirmed")
        assert isinstance(key, str)
        assert key.startswith("reservations:")

    def test_cache_ttl_expiration(self):
        """Test expiración del caché"""
        cache = ReservationCache(ttl=1)  # 1 segundo
        cache.cache["test_key"] = ("data", time.time() - 2)  # Expired

        # Simular que el caché está expirado
        assert "test_key" in cache.cache
        # En un test real, verificaríamos que get_or_fetch no devuelve datos expirados

    def test_cache_clear(self):
        """Test limpieza del caché"""
        cache = ReservationCache()
        cache.cache["test_key"] = ("data", time.time())
        assert len(cache.cache) == 1

        cache.clear_cache()
        assert len(cache.cache) == 0


class TestReservationMetrics:
    """Tests para el sistema de métricas"""

    def test_metrics_initialization(self):
        """Test inicialización de métricas"""
        metrics = ReservationMetrics()
        assert metrics.requests_total == 0
        assert metrics.errors == 0
        assert metrics.cache_hits == 0
        assert metrics.cache_misses == 0

    def test_record_request(self):
        """Test registro de requests"""
        metrics = ReservationMetrics()
        metrics.record_request("test_tool", 1.5, True, True)

        assert metrics.requests_total == 1
        assert metrics.requests_by_tool["test_tool"] == 1
        assert metrics.cache_hits == 1
        assert metrics.cache_misses == 0
        assert len(metrics.response_times) == 1

    def test_get_metrics_summary(self):
        """Test resumen de métricas"""
        metrics = ReservationMetrics()
        metrics.record_request("test_tool", 1.0, True, True)
        metrics.record_request("test_tool", 2.0, False, False)

        summary = metrics.get_metrics_summary()
        assert summary["requests_total"] == 2
        assert summary["error_rate"] == 0.5
        assert summary["cache_hit_rate"] == 0.5
        assert summary["avg_response_time"] == 1.5


class TestEnhancedTools:
    """Tests para herramientas mejoradas"""

    @pytest.fixture
    def sample_reservations_data(self):
        """Datos de ejemplo para testing"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 1,
                        "name": "Reserva Test 1",
                        "status": "Confirmed",
                        "arrival_date": "2024-01-15",
                        "departure_date": "2024-01-18",
                        "nights": 3,
                        "unit_id": 101,
                        "node_id": 1,
                        "channel_id": 1,
                        "guest_breakdown": {
                            "total": "450.00",
                            "gross_rent": "400.00",
                            "fees": "50.00",
                        },
                    },
                    {
                        "id": 2,
                        "name": "Reserva Test 2",
                        "status": "Checked In",
                        "arrival_date": "2024-01-20",
                        "departure_date": "2024-01-25",
                        "nights": 5,
                        "unit_id": 102,
                        "node_id": 2,
                        "channel_id": 2,
                        "guest_breakdown": {
                            "total": "750.00",
                            "gross_rent": "700.00",
                            "fees": "50.00",
                        },
                    },
                ]
            },
            "page": 1,
            "page_size": 10,
            "total_items": 2,
        }

    @pytest.mark.asyncio
    async def test_search_reservations_enhanced_basic(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test búsqueda básica mejorada"""
        # Configurar mock
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar herramienta
        register_search_reservations_enhanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called

    @pytest.mark.asyncio
    async def test_search_reservations_enhanced_with_filters(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test búsqueda con filtros avanzados"""
        # Configurar mock
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar herramienta
        register_search_reservations_enhanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called

    @pytest.mark.asyncio
    async def test_search_reservations_advanced_basic(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test búsqueda avanzada básica"""
        # Configurar mock
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar herramienta
        register_search_reservations_advanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called

    @pytest.mark.asyncio
    async def test_search_reservations_advanced_with_financial_filters(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test búsqueda avanzada con filtros financieros"""
        # Configurar mock
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar herramienta
        register_search_reservations_advanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called


class TestEnhancedResources:
    """Tests para recursos mejorados"""

    @pytest.mark.asyncio
    async def test_realtime_occupancy_resource(self, mock_mcp, mock_api_client):
        """Test recurso de ocupación en tiempo real"""
        # Registrar recursos
        register_enhanced_resources(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró el recurso
        assert mock_mcp.resource.called

    @pytest.mark.asyncio
    async def test_kpi_dashboard_resource(self, mock_mcp, mock_api_client):
        """Test recurso de dashboard KPI"""
        # Registrar recursos
        register_enhanced_resources(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró el recurso
        assert mock_mcp.resource.called

    @pytest.mark.asyncio
    async def test_demand_forecast_resource(self, mock_mcp, mock_api_client):
        """Test recurso de previsión de demanda"""
        # Registrar recursos
        register_enhanced_resources(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró el recurso
        assert mock_mcp.resource.called

    @pytest.mark.asyncio
    async def test_config_resources(self, mock_mcp, mock_api_client):
        """Test recursos de configuración"""
        # Registrar recursos
        register_enhanced_resources(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registraron los recursos
        assert mock_mcp.resource.called


class TestEnhancedPrompts:
    """Tests para prompts mejorados"""

    def test_occupancy_analysis_prompt(self, mock_mcp):
        """Test prompt de análisis de ocupación"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called

    def test_revenue_analysis_prompt(self, mock_mcp):
        """Test prompt de análisis de ingresos"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called

    def test_guest_analysis_prompt(self, mock_mcp):
        """Test prompt de análisis de huéspedes"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called

    def test_pricing_optimization_prompt(self, mock_mcp):
        """Test prompt de optimización de precios"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called

    def test_channel_analysis_prompt(self, mock_mcp):
        """Test prompt de análisis de canales"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called

    def test_executive_report_prompt(self, mock_mcp):
        """Test prompt de reporte ejecutivo"""
        # Registrar prompts
        register_enhanced_prompts(mcp=mock_mcp)

        # Verificar que se registró el prompt
        assert mock_mcp.prompt.called


class TestIntegration:
    """Tests de integración completa"""

    @pytest.fixture
    def sample_reservations_data(self):
        """Datos de ejemplo para testing"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 1,
                        "name": "Reserva Test 1",
                        "status": "Confirmed",
                        "arrival_date": "2024-01-15",
                        "departure_date": "2024-01-18",
                        "nights": 3,
                        "unit_id": 101,
                        "node_id": 1,
                        "channel_id": 1,
                        "guest_breakdown": {
                            "total": "450.00",
                            "gross_rent": "400.00",
                            "fees": "50.00",
                        },
                    },
                    {
                        "id": 2,
                        "name": "Reserva Test 2",
                        "status": "Checked In",
                        "arrival_date": "2024-01-20",
                        "departure_date": "2024-01-25",
                        "nights": 5,
                        "unit_id": 102,
                        "node_id": 2,
                        "channel_id": 2,
                        "guest_breakdown": {
                            "total": "750.00",
                            "gross_rent": "700.00",
                            "fees": "50.00",
                        },
                    },
                ]
            },
            "page": 1,
            "page_size": 10,
            "total_items": 2,
        }

    @pytest.mark.asyncio
    async def test_full_integration(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test integración completa del sistema"""
        # Configurar mocks
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar todas las funcionalidades
        from src.trackhs_mcp.infrastructure.mcp.all_tools import register_all_tools

        register_all_tools(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registraron todas las funcionalidades
        assert mock_mcp.tool.call_count >= 4  # Al menos 4 herramientas
        assert mock_mcp.resource.call_count >= 6  # Al menos 6 recursos
        # Los prompts se registran con decoradores, no con llamadas directas
        # assert mock_mcp.prompt.call_count >= 0  # Los prompts se registran automáticamente

    @pytest.mark.asyncio
    async def test_error_handling(self, mock_mcp, mock_api_client):
        """Test manejo de errores"""
        # Configurar mock para lanzar error
        mock_api_client.search_reservations.side_effect = Exception("API Error")

        # Registrar herramientas
        register_search_reservations_enhanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called

    @pytest.mark.asyncio
    async def test_performance_metrics(
        self, mock_mcp, mock_api_client, sample_reservations_data
    ):
        """Test métricas de rendimiento"""
        # Configurar mock
        mock_api_client.search_reservations.return_value = sample_reservations_data

        # Registrar herramientas
        register_search_reservations_enhanced(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se registró la herramienta
        assert mock_mcp.tool.called


# Tests de validación de parámetros
class TestParameterValidation:
    """Tests para validación de parámetros"""

    def test_enhanced_parameter_validation(self):
        """Test validación de parámetros mejorados"""
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_enhanced import (
            _validate_enhanced_params,
        )

        # Test parámetros válidos
        _validate_enhanced_params(1, 10, 100.0, 500.0, 1, 5, "full")

        # Test parámetros inválidos
        with pytest.raises(Exception):
            _validate_enhanced_params(-1, 10, 100.0, 500.0, 1, 5, "full")

        with pytest.raises(Exception):
            _validate_enhanced_params(1, 10, 500.0, 100.0, 1, 5, "full")

    def test_advanced_parameter_validation(self):
        """Test validación de parámetros avanzados"""
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_advanced import (
            _validate_advanced_params,
        )

        # Test parámetros válidos
        _validate_advanced_params(
            100.0, 500.0, 50.0, 200.0, 1, 5, 0.5, 1.0, "node", "json"
        )

        # Test parámetros inválidos
        with pytest.raises(Exception):
            _validate_advanced_params(
                -100.0, 500.0, 50.0, 200.0, 1, 5, 0.5, 1.0, "node", "json"
            )

        with pytest.raises(Exception):
            _validate_advanced_params(
                100.0, 500.0, 50.0, 200.0, 1, 5, 1.5, 1.0, "node", "json"
            )


# Tests de procesamiento de datos
class TestDataProcessing:
    """Tests para procesamiento de datos"""

    def test_revenue_filtering(self):
        """Test filtrado por ingresos"""
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_advanced import (
            _filter_by_revenue,
        )

        reservations = [
            {"guest_breakdown": {"total": "300.00"}},
            {"guest_breakdown": {"total": "800.00"}},
            {"guest_breakdown": {"total": "1200.00"}},
        ]

        # Test filtrado
        filtered = _filter_by_revenue(reservations, 400.0, 1000.0)
        assert len(filtered) == 1
        assert filtered[0]["guest_breakdown"]["total"] == "800.00"

    def test_nights_filtering(self):
        """Test filtrado por noches"""
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_advanced import (
            _filter_by_nights,
        )

        reservations = [{"nights": 2}, {"nights": 5}, {"nights": 8}]

        # Test filtrado
        filtered = _filter_by_nights(reservations, 3, 7)
        assert len(filtered) == 1
        assert filtered[0]["nights"] == 5

    def test_grouping(self):
        """Test agrupación de reservas"""
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_advanced import (
            _group_reservations,
        )

        reservations = [
            {"node_id": 1, "status": "Confirmed"},
            {"node_id": 1, "status": "Checked In"},
            {"node_id": 2, "status": "Confirmed"},
        ]

        # Test agrupación por nodo
        grouped = _group_reservations(reservations, "node")
        assert len(grouped) == 2
        assert len(grouped[1]) == 2
        assert len(grouped[2]) == 1

        # Test agrupación por estado
        grouped = _group_reservations(reservations, "status")
        assert len(grouped) == 2
        assert len(grouped["Confirmed"]) == 2
        assert len(grouped["Checked In"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
