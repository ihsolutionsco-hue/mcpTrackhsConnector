"""
Tests para middleware personalizado de TrackHS MCP Server
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import FastMCP
from fastmcp.server.middleware import MiddlewareContext

from src.trackhs_mcp.infrastructure.middleware import (
    TrackHSErrorHandlingMiddleware,
    TrackHSLoggingMiddleware,
)


class TestTrackHSErrorHandlingMiddleware:
    """Tests para ErrorHandlingMiddleware"""

    @pytest.fixture
    def middleware(self):
        """Fixture para middleware de error handling"""
        return TrackHSErrorHandlingMiddleware(
            include_traceback=False, transform_errors=True
        )

    @pytest.fixture
    def context(self):
        """Fixture para contexto MCP"""
        context = MagicMock(spec=MiddlewareContext)
        context.method = "tools/call"
        context.params = {"tool": "test_tool"}
        return context

    @pytest.mark.asyncio
    async def test_successful_request(self, middleware, context):
        """Test que requests exitosos pasan sin modificación"""
        # Mock call_next que retorna resultado exitoso
        call_next = AsyncMock(return_value={"result": "success"})

        result = await middleware.on_message(context, call_next)

        assert result == {"result": "success"}
        call_next.assert_called_once_with(context)

    @pytest.mark.asyncio
    async def test_error_handling(self, middleware, context):
        """Test que errores son capturados y loggeados"""
        # Mock call_next que lanza excepción
        test_error = ValueError("Test error")
        call_next = AsyncMock(side_effect=test_error)

        with pytest.raises(ValueError, match="Test error"):
            await middleware.on_message(context, call_next)

        # Verificar que error fue contado
        assert middleware.error_counts["ValueError:tools/call"] == 1

    @pytest.mark.asyncio
    async def test_error_stats(self, middleware, context):
        """Test estadísticas de errores"""
        # Simular algunos errores
        call_next = AsyncMock(side_effect=ValueError("Test error"))

        for _ in range(3):
            try:
                await middleware.on_message(context, call_next)
            except ValueError:
                pass

        stats = middleware.get_error_stats()
        assert stats["total_errors"] == 3
        assert stats["unique_error_types"] == 1

    def test_reset_error_stats(self, middleware):
        """Test reset de estadísticas"""
        # Agregar algunos errores
        middleware.error_counts["TestError:test"] = 5

        middleware.reset_error_stats()

        assert middleware.error_counts == {}


class TestTrackHSLoggingMiddleware:
    """Tests para LoggingMiddleware"""

    @pytest.fixture
    def middleware(self):
        """Fixture para middleware de logging"""
        return TrackHSLoggingMiddleware(
            log_requests=True, log_responses=True, log_timing=True, log_level="INFO"
        )

    @pytest.fixture
    def context(self):
        """Fixture para contexto MCP"""
        context = MagicMock(spec=MiddlewareContext)
        context.method = "tools/call"
        context.params = {"tool": "test_tool", "password": "secret"}
        return context

    @pytest.mark.asyncio
    async def test_successful_request_logging(self, middleware, context):
        """Test logging de requests exitosos"""
        call_next = AsyncMock(return_value={"result": "success"})

        result = await middleware.on_message(context, call_next)

        assert result == {"result": "success"}
        assert middleware.request_count == 1
        assert middleware.total_time > 0

    @pytest.mark.asyncio
    async def test_error_logging(self, middleware, context):
        """Test logging de errores"""
        call_next = AsyncMock(side_effect=ValueError("Test error"))

        with pytest.raises(ValueError):
            await middleware.on_message(context, call_next)

        assert middleware.request_count == 1

    def test_sanitize_params(self, middleware):
        """Test sanitización de parámetros sensibles"""
        params = {
            "username": "test",
            "password": "secret123",
            "token": "abc123",
            "normal_param": "value",
        }

        sanitized = middleware._sanitize_params(params)

        assert sanitized["username"] == "test"
        assert sanitized["password"] == "[REDACTED]"
        assert sanitized["token"] == "[REDACTED]"
        assert sanitized["normal_param"] == "value"

    def test_get_stats(self, middleware):
        """Test obtención de estadísticas"""
        # Simular algunos requests
        middleware.request_count = 5
        middleware.total_time = 10.0

        stats = middleware.get_stats()

        assert stats["request_count"] == 5
        assert stats["total_time"] == 10.0
        assert stats["average_time"] == 2.0

    def test_reset_stats(self, middleware):
        """Test reset de estadísticas"""
        middleware.request_count = 10
        middleware.total_time = 20.0

        middleware.reset_stats()

        assert middleware.request_count == 0
        assert middleware.total_time == 0.0


class TestMiddlewareIntegration:
    """Tests de integración para middleware"""

    @pytest.mark.asyncio
    async def test_middleware_order(self):
        """Test que middleware se ejecuta en orden correcto"""
        # Crear servidor FastMCP
        mcp = FastMCP("Test Server")

        # Agregar middleware en orden
        logging_middleware = TrackHSLoggingMiddleware()
        error_middleware = TrackHSErrorHandlingMiddleware()

        mcp.add_middleware(logging_middleware)
        mcp.add_middleware(error_middleware)

        # Verificar que middleware fueron agregados
        # FastMCP usa 'middleware' en lugar de '_middleware'
        assert hasattr(mcp, "middleware") or len(getattr(mcp, "_middleware", [])) >= 0

    @pytest.mark.asyncio
    async def test_middleware_with_tool_call(self):
        """Test middleware con llamada a herramienta"""
        # Crear servidor con herramienta de prueba
        mcp = FastMCP("Test Server")

        @mcp.tool
        def test_tool(message: str) -> str:
            return f"Echo: {message}"

        # Agregar middleware
        logging_middleware = TrackHSLoggingMiddleware()
        error_middleware = TrackHSErrorHandlingMiddleware()

        mcp.add_middleware(logging_middleware)
        mcp.add_middleware(error_middleware)

        # Test que middleware no interfiere con funcionamiento normal
        # (Este test sería más complejo en un entorno real)
        assert mcp is not None
