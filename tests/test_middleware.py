"""
Tests para middleware de TrackHS MCP Server
Prueba funcionalidad de middleware nativo FastMCP
"""

import pytest
import time
from unittest.mock import Mock, patch, AsyncMock

from src.trackhs_mcp.middleware_native import (
    TrackHSLoggingMiddleware,
    TrackHSAuthMiddleware,
    TrackHSMetricsMiddleware,
    TrackHSRateLimitMiddleware,
)
from src.trackhs_mcp.exceptions import AuthenticationError


class TestTrackHSLoggingMiddleware:
    """Tests para TrackHSLoggingMiddleware"""

    @pytest.fixture
    def middleware(self):
        """Instancia de middleware para testing"""
        return TrackHSLoggingMiddleware()

    @pytest.fixture
    def mock_context(self):
        """Mock del contexto MCP"""
        context = Mock()
        context.method = "test_method"
        return context

    @pytest.fixture
    def mock_call_next(self):
        """Mock de la función call_next"""
        return AsyncMock(return_value={"result": "success"})

    @pytest.mark.asyncio
    async def test_successful_request(self, middleware, mock_context, mock_call_next):
        """Test request exitoso"""
        # Act
        result = await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert result == {"result": "success"}
        assert middleware.request_count == 1
        mock_call_next.assert_called_once_with(mock_context)

    @pytest.mark.asyncio
    async def test_failed_request(self, middleware, mock_context):
        """Test request fallido"""
        # Arrange
        mock_call_next = AsyncMock(side_effect=Exception("Test error"))

        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            await middleware.on_message(mock_context, mock_call_next)

        assert middleware.request_count == 1

    @pytest.mark.asyncio
    async def test_request_counting(self, middleware, mock_context, mock_call_next):
        """Test conteo de requests"""
        # Act - Múltiples requests
        await middleware.on_message(mock_context, mock_call_next)
        await middleware.on_message(mock_context, mock_call_next)
        await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert middleware.request_count == 3


class TestTrackHSAuthMiddleware:
    """Tests para TrackHSAuthMiddleware"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client

    @pytest.fixture
    def middleware(self, mock_api_client):
        """Instancia de middleware para testing"""
        return TrackHSAuthMiddleware(mock_api_client)

    @pytest.fixture
    def mock_context(self):
        """Mock del contexto MCP"""
        context = Mock()
        context.method = "test_method"
        return context

    @pytest.fixture
    def mock_call_next(self):
        """Mock de la función call_next"""
        return AsyncMock(return_value={"result": "success"})

    def test_check_authentication_success(self, middleware, mock_api_client):
        """Test verificación de autenticación exitosa"""
        # Arrange
        mock_api_client.get.return_value = {"status": "ok"}

        # Act
        result = middleware._check_authentication()

        # Assert
        assert result is True
        assert middleware.is_authenticated is True
        mock_api_client.get.assert_called_once_with("pms/units/amenities", {"page": 1, "size": 1})

    def test_check_authentication_failure(self, middleware, mock_api_client):
        """Test verificación de autenticación fallida"""
        # Arrange
        mock_api_client.get.side_effect = Exception("Auth failed")

        # Act & Assert
        with pytest.raises(AuthenticationError):
            middleware._check_authentication()

        assert middleware.is_authenticated is False

    def test_check_authentication_no_client(self):
        """Test verificación sin cliente API"""
        # Arrange
        middleware = TrackHSAuthMiddleware(None)

        # Act & Assert
        with pytest.raises(AuthenticationError):
            middleware._check_authentication()

    @patch.dict('os.environ', {'TESTING': '1'})
    def test_check_authentication_testing_mode(self):
        """Test verificación en modo testing"""
        # Arrange
        middleware = TrackHSAuthMiddleware(None)

        # Act
        result = middleware._check_authentication()

        # Assert
        assert result is False
        assert middleware.is_authenticated is False

    @pytest.mark.asyncio
    async def test_no_auth_methods(self, middleware, mock_context, mock_call_next):
        """Test métodos que no requieren autenticación"""
        # Arrange
        no_auth_methods = [
            "initialize", "ping", "tools/list",
            "resources/list", "resources/templates/list", "prompts/list"
        ]

        for method in no_auth_methods:
            mock_context.method = method

            # Act
            result = await middleware.on_message(mock_context, mock_call_next)

            # Assert
            assert result == {"result": "success"}

    @pytest.mark.asyncio
    async def test_auth_required_methods(self, middleware, mock_api_client, mock_context, mock_call_next):
        """Test métodos que requieren autenticación"""
        # Arrange
        mock_context.method = "call"  # Requiere autenticación
        mock_api_client.get.return_value = {"status": "ok"}

        # Act
        result = await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert result == {"result": "success"}
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_auth_failure_blocks_request(self, middleware, mock_api_client, mock_context, mock_call_next):
        """Test que fallo de autenticación bloquea request"""
        # Arrange
        mock_context.method = "call"  # Requiere autenticación
        mock_api_client.get.side_effect = Exception("Auth failed")

        # Act & Assert
        with pytest.raises(AuthenticationError):
            await middleware.on_message(mock_context, mock_call_next)

        mock_call_next.assert_not_called()


class TestTrackHSMetricsMiddleware:
    """Tests para TrackHSMetricsMiddleware"""

    @pytest.fixture
    def middleware(self):
        """Instancia de middleware para testing"""
        return TrackHSMetricsMiddleware()

    @pytest.fixture
    def mock_context(self):
        """Mock del contexto MCP"""
        context = Mock()
        context.method = "test_method"
        return context

    @pytest.fixture
    def mock_call_next(self):
        """Mock de la función call_next"""
        return AsyncMock(return_value={"result": "success"})

    @pytest.mark.asyncio
    async def test_successful_request_metrics(self, middleware, mock_context, mock_call_next):
        """Test métricas de request exitoso"""
        # Act
        result = await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert result == {"result": "success"}
        assert middleware.metrics["total_requests"] == 1
        assert middleware.metrics["successful_requests"] == 1
        assert middleware.metrics["failed_requests"] == 0
        assert len(middleware.response_times) == 1

    @pytest.mark.asyncio
    async def test_failed_request_metrics(self, middleware, mock_context):
        """Test métricas de request fallido"""
        # Arrange
        mock_call_next = AsyncMock(side_effect=Exception("Test error"))

        # Act & Assert
        with pytest.raises(Exception):
            await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert middleware.metrics["total_requests"] == 1
        assert middleware.metrics["successful_requests"] == 0
        assert middleware.metrics["failed_requests"] == 1
        assert len(middleware.response_times) == 1

    def test_get_metrics(self, middleware):
        """Test obtener métricas"""
        # Arrange
        middleware.metrics["total_requests"] = 10
        middleware.metrics["successful_requests"] = 8
        middleware.metrics["failed_requests"] = 2
        middleware.response_times = [1.0, 2.0, 3.0, 4.0, 5.0]

        # Act
        metrics = middleware.get_metrics()

        # Assert
        assert metrics["total_requests"] == 10
        assert metrics["successful_requests"] == 8
        assert metrics["failed_requests"] == 2
        assert metrics["average_response_time_seconds"] == 3.0
        assert metrics["error_rate_percentage"] == 20.0
        assert metrics["total_response_times_recorded"] == 5

    def test_reset_metrics(self, middleware):
        """Test resetear métricas"""
        # Arrange
        middleware.metrics["total_requests"] = 10
        middleware.response_times = [1.0, 2.0, 3.0]

        # Act
        middleware.reset_metrics()

        # Assert
        assert middleware.metrics["total_requests"] == 0
        assert middleware.metrics["successful_requests"] == 0
        assert middleware.metrics["failed_requests"] == 0
        assert len(middleware.response_times) == 0


class TestTrackHSRateLimitMiddleware:
    """Tests para TrackHSRateLimitMiddleware"""

    @pytest.fixture
    def middleware(self):
        """Instancia de middleware para testing"""
        return TrackHSRateLimitMiddleware(requests_per_minute=2, burst_size=1)

    @pytest.fixture
    def mock_context(self):
        """Mock del contexto MCP"""
        context = Mock()
        context.method = "test_method"
        context.client_id = "test_client"
        return context

    @pytest.fixture
    def mock_call_next(self):
        """Mock de la función call_next"""
        return AsyncMock(return_value={"result": "success"})

    def test_is_rate_limited_false(self, middleware):
        """Test que no está rate limited"""
        # Act
        result = middleware._is_rate_limited("client1")

        # Assert
        assert result is False

    def test_is_rate_limited_true(self, middleware):
        """Test que está rate limited"""
        # Arrange - Simular requests en el último minuto
        current_time = time.time()
        middleware.request_counts["client1"] = [
            current_time - 30,  # 30 segundos atrás
            current_time - 20,  # 20 segundos atrás
            current_time - 10,  # 10 segundos atrás
        ]

        # Act
        result = middleware._is_rate_limited("client1")

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_rate_limit_allows_request(self, middleware, mock_context, mock_call_next):
        """Test que rate limit permite request"""
        # Act
        result = await middleware.on_message(mock_context, mock_call_next)

        # Assert
        assert result == {"result": "success"}
        assert "test_client" in middleware.request_counts
        assert len(middleware.request_counts["test_client"]) == 1

    @pytest.mark.asyncio
    async def test_rate_limit_blocks_request(self, middleware, mock_context, mock_call_next):
        """Test que rate limit bloquea request"""
        # Arrange - Simular que ya se alcanzó el límite
        current_time = time.time()
        middleware.request_counts["test_client"] = [
            current_time - 30,
            current_time - 20,
            current_time - 10,
        ]

        # Act & Assert
        from fastmcp.exceptions import ToolError
        with pytest.raises(ToolError, match="Rate limit exceeded"):
            await middleware.on_message(mock_context, mock_call_next)

    def test_rate_limit_cleanup(self, middleware):
        """Test limpieza de requests antiguos"""
        # Arrange - Simular requests antiguos y recientes
        current_time = time.time()
        middleware.request_counts["client1"] = [
            current_time - 70,  # 70 segundos atrás (debería limpiarse)
            current_time - 30,  # 30 segundos atrás (debería mantenerse)
            current_time - 10,  # 10 segundos atrás (debería mantenerse)
        ]

        # Act
        result = middleware._is_rate_limited("client1")

        # Assert
        assert result is False  # No debería estar rate limited
        assert len(middleware.request_counts["client1"]) == 2  # Solo los recientes


class TestMiddlewareIntegration:
    """Tests de integración entre middleware"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        client.get.return_value = {"status": "ok"}
        return client

    @pytest.fixture
    def middleware_chain(self, mock_api_client):
        """Cadena de middleware para testing"""
        return [
            TrackHSLoggingMiddleware(),
            TrackHSAuthMiddleware(mock_api_client),
            TrackHSMetricsMiddleware(),
            TrackHSRateLimitMiddleware(requests_per_minute=10, burst_size=5)
        ]

    @pytest.fixture
    def mock_context(self):
        """Mock del contexto MCP"""
        context = Mock()
        context.method = "tools/list"  # No requiere autenticación
        context.client_id = "test_client"
        return context

    @pytest.fixture
    def mock_call_next(self):
        """Mock de la función call_next"""
        return AsyncMock(return_value={"result": "success"})

    @pytest.mark.asyncio
    async def test_middleware_chain_execution(self, middleware_chain, mock_context, mock_call_next):
        """Test ejecución de cadena de middleware"""
        # Arrange
        call_next = mock_call_next

        # Act - Ejecutar middleware en orden
        for middleware in middleware_chain:
            call_next = lambda ctx, next_call: middleware.on_message(ctx, next_call)

        result = await call_next(mock_context, mock_call_next)

        # Assert
        assert result == {"result": "success"}
        mock_call_next.assert_called_once_with(mock_context)

    @pytest.mark.asyncio
    async def test_middleware_error_propagation(self, middleware_chain, mock_context):
        """Test propagación de errores en cadena de middleware"""
        # Arrange
        mock_call_next = AsyncMock(side_effect=Exception("Test error"))
        call_next = mock_call_next

        # Act - Ejecutar middleware en orden
        for middleware in middleware_chain:
            call_next = lambda ctx, next_call: middleware.on_message(ctx, next_call)

        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            await call_next(mock_context, mock_call_next)

    def test_middleware_metrics_aggregation(self, middleware_chain):
        """Test agregación de métricas de middleware"""
        # Arrange
        metrics_middleware = middleware_chain[2]  # TrackHSMetricsMiddleware

        # Act - Simular múltiples requests
        for i in range(5):
            metrics_middleware.metrics["total_requests"] += 1
            metrics_middleware.metrics["successful_requests"] += 1
            metrics_middleware.response_times.append(1.0 + i * 0.1)

        # Act
        metrics = metrics_middleware.get_metrics()

        # Assert
        assert metrics["total_requests"] == 5
        assert metrics["successful_requests"] == 5
        assert metrics["average_response_time_seconds"] == 1.2
        assert metrics["error_rate_percentage"] == 0.0
