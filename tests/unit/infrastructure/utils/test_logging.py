"""
Tests unitarios para sistema de logging
"""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from src.trackhs_mcp.core.logging import (
    LogCategory,
    LogContext,
    LogLevel,
    LogMetric,
    PerformanceTimer,
    RequestContext,
    TrackHSLogger,
    get_logger,
)


class TestLogLevel:
    """Tests para LogLevel"""

    @pytest.mark.unit
    def test_log_level_values(self):
        """Test valores de LogLevel"""
        assert LogLevel.TRACE.value == 5
        assert LogLevel.DEBUG.value == 10
        assert LogLevel.INFO.value == 20
        assert LogLevel.WARNING.value == 30
        assert LogLevel.ERROR.value == 40
        assert LogLevel.CRITICAL.value == 50


class TestLogCategory:
    """Tests para LogCategory"""

    @pytest.mark.unit
    def test_log_category_values(self):
        """Test valores de LogCategory"""
        assert LogCategory.MCP_TOOL.value == "mcp_tool"
        assert LogCategory.API_REQUEST.value == "api_request"
        assert LogCategory.AUTHENTICATION.value == "authentication"
        assert LogCategory.PERFORMANCE.value == "performance"
        assert LogCategory.SECURITY.value == "security"


class TestLogContext:
    """Tests para LogContext"""

    @pytest.mark.unit
    def test_log_context_creation(self):
        """Test creación de LogContext"""
        context = LogContext(
            request_id="req123",
            user_id="user456",
            session_id="session789",
            tool_name="test_tool",
        )

        assert context.request_id == "req123"
        assert context.user_id == "user456"
        assert context.session_id == "session789"
        assert context.tool_name == "test_tool"

    @pytest.mark.unit
    def test_log_context_with_defaults(self):
        """Test LogContext con valores por defecto"""
        context = LogContext()

        assert context.request_id is None
        assert context.user_id is None
        assert context.session_id is None
        assert context.tool_name is None


class TestLogMetric:
    """Tests para LogMetric"""

    @pytest.mark.unit
    def test_log_metric_creation(self):
        """Test creación de LogMetric"""
        metric = LogMetric(
            name="response_time",
            value=1.5,
            unit="seconds",
            timestamp=datetime.now(timezone.utc),
        )

        assert metric.name == "response_time"
        assert metric.value == 1.5
        assert metric.unit == "seconds"
        assert isinstance(metric.timestamp, datetime)


class TestTrackHSLogger:
    """Tests para TrackHSLogger"""

    @pytest.fixture
    def mock_mcp_client(self):
        """Mock del cliente MCP"""
        return Mock()

    @pytest.fixture
    def logger(self, mock_mcp_client):
        """Crear logger para testing"""
        return TrackHSLogger("test_logger", mock_mcp_client)

    @pytest.mark.unit
    def test_logger_init(self, logger, mock_mcp_client):
        """Test inicialización del logger"""
        assert logger.logger is not None
        assert logger.mcp_client == mock_mcp_client
        assert logger._metrics == []

    @pytest.mark.unit
    def test_get_context(self, logger):
        """Test obtención de contexto"""
        context = logger._get_context()

        assert isinstance(context, LogContext)
        # Los valores específicos dependen de las variables de contexto
        # que pueden no estar configuradas en el entorno de testing

    @pytest.mark.unit
    def test_format_message(self, logger):
        """Test formateo de mensaje"""
        message = "Test message"
        context = LogContext(request_id="req123", tool_name="test")

        # Use the private method for testing
        formatted = logger._format_message(
            message, context, LogCategory.API_REQUEST, LogLevel.INFO
        )

        assert "Test message" in formatted["message"]
        assert formatted["context"]["request_id"] == "req123"
        assert formatted["context"]["tool_name"] == "test"

    @pytest.mark.unit
    def test_log_basic(self, logger):
        """Test logging básico"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log(LogLevel.INFO, "Test message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 20  # INFO level
            assert "Test message" in args[1]

    @pytest.mark.unit
    def test_log_with_context(self, logger):
        """Test logging con contexto"""
        context = LogContext(request_id="req123", tool_name="test")

        with patch.object(logger.logger, "log") as mock_log:
            logger.log(LogLevel.INFO, "Test message", LogCategory.MCP_TOOL, context)

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "extra" in kwargs
            assert kwargs["extra"]["request_id"] == "req123"

    @pytest.mark.unit
    def test_log_with_metrics(self, logger):
        """Test logging con métricas"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log(LogLevel.INFO, "Test message", metrics={"response_time": 1.5})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "metrics" in kwargs
            assert kwargs["metrics"]["response_time"] == 1.5

    @pytest.mark.unit
    def test_trace_log(self, logger):
        """Test log de nivel trace"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.trace("Trace message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 5  # TRACE level

    @pytest.mark.unit
    def test_debug_log(self, logger):
        """Test log de nivel debug"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.debug("Debug message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 10  # DEBUG level

    @pytest.mark.unit
    def test_info_log(self, logger):
        """Test log de nivel info"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.info("Info message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 20  # INFO level

    @pytest.mark.unit
    def test_warning_log(self, logger):
        """Test log de nivel warning"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.warning("Warning message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 30  # WARNING level

    @pytest.mark.unit
    def test_error_log(self, logger):
        """Test log de nivel error"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.error("Error message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 40  # ERROR level

    @pytest.mark.unit
    def test_critical_log(self, logger):
        """Test log de nivel critical"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.critical("Critical message")

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert args[0] == 50  # CRITICAL level

    @pytest.mark.unit
    def test_log_api_request(self, logger):
        """Test logging de petición API"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_api_request("GET", "/test", {"param": "value"})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "API Request" in args[1]
            assert "GET" in args[1]
            assert "/test" in args[1]

    @pytest.mark.unit
    def test_log_api_response(self, logger):
        """Test logging de respuesta API"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_api_response("GET", "/test", 200, 1.5)

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "API Response" in args[1]
            assert "200" in args[1]

    @pytest.mark.unit
    def test_log_tool_execution(self, logger):
        """Test logging de ejecución de herramienta"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_tool_execution("search_reservations", {"page": 1}, 1.5, True)

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Tool Execution" in args[1]
            assert "search_reservations" in args[1]

    @pytest.mark.unit
    def test_log_resource_access(self, logger):
        """Test logging de acceso a recurso"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_resource_access("reservations", {"data": "test"})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Resource Access" in args[1]
            assert "reservations" in args[1]

    @pytest.mark.unit
    def test_log_prompt_usage(self, logger):
        """Test logging de uso de prompt"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_prompt_usage("check_reservations", {"date": "2024-01-01"})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Prompt Usage" in args[1]
            assert "check_reservations" in args[1]

    @pytest.mark.unit
    def test_log_authentication(self, logger):
        """Test logging de autenticación"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_authentication("user123", True)

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Authentication" in args[1]
            assert "user123" in args[1]

    @pytest.mark.unit
    def test_log_performance(self, logger):
        """Test logging de rendimiento"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_performance("api_call", 1.5, {"endpoint": "/test"})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Performance" in args[1]
            assert "api_call" in args[1]
            assert "1.5" in args[1]

    @pytest.mark.unit
    def test_log_security(self, logger):
        """Test logging de seguridad"""
        with patch.object(logger.logger, "log") as mock_log:
            logger.log_security("suspicious_activity", {"ip": "192.168.1.1"})

            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert "Security" in args[1]
            assert "suspicious_activity" in args[1]

    @pytest.mark.unit
    def test_add_metric(self, logger):
        """Test agregar métrica"""
        logger.add_metric("response_time", 1.5, "seconds")

        assert len(logger._metrics) == 1
        assert logger._metrics[0].name == "response_time"
        assert logger._metrics[0].value == 1.5
        assert logger._metrics[0].unit == "seconds"

    @pytest.mark.unit
    def test_get_metrics(self, logger):
        """Test obtención de métricas"""
        logger.add_metric("response_time", 1.5, "seconds")
        logger.add_metric("memory_usage", 100, "MB")

        metrics = logger.get_metrics()

        assert len(metrics) == 2
        assert any(m.name == "response_time" for m in metrics)
        assert any(m.name == "memory_usage" for m in metrics)

    @pytest.mark.unit
    def test_clear_metrics(self, logger):
        """Test limpiar métricas"""
        logger.add_metric("response_time", 1.5, "seconds")
        assert len(logger._metrics) == 1

        logger.clear_metrics()
        assert len(logger._metrics) == 0


class TestRequestContext:
    """Tests para RequestContext"""

    @pytest.mark.unit
    def test_request_context_enter_exit(self):
        """Test context manager de RequestContext"""
        with patch("src.trackhs_mcp.core.logging.request_id_var") as mock_var:
            mock_var.set = Mock()
            mock_var.get = Mock(return_value=None)

            with RequestContext("req123"):
                mock_var.set.assert_called_with("req123")

    @pytest.mark.unit
    def test_request_context_with_user_id(self):
        """Test RequestContext con user_id"""
        with (
            patch("src.trackhs_mcp.core.logging.request_id_var") as mock_request_var,
            patch("src.trackhs_mcp.core.logging.user_id_var") as mock_user_var,
        ):
            mock_request_var.set = Mock()
            mock_user_var.set = Mock()

            with RequestContext("req123", "user456"):
                mock_request_var.set.assert_called_with("req123")
                mock_user_var.set.assert_called_with("user456")


class TestPerformanceTimer:
    """Tests para PerformanceTimer"""

    @pytest.mark.unit
    def test_performance_timer_enter_exit(self):
        """Test context manager de PerformanceTimer"""
        logger = TrackHSLogger("test_logger")

        with patch("time.time") as mock_time:
            mock_time.side_effect = [0.0, 1.5]  # start_time, end_time

            with PerformanceTimer(logger, "test_operation") as timer:
                pass

            assert timer.operation == "test_operation"
            assert timer.duration == 1.5

    @pytest.mark.unit
    def test_performance_timer_with_logger(self):
        """Test PerformanceTimer con logger"""
        mock_logger = Mock()

        with patch("time.time") as mock_time:
            mock_time.side_effect = [0.0, 1.5]

            with PerformanceTimer("test_operation", mock_logger) as timer:
                pass

            # Verify timer was used
            assert timer.operation == "test_operation"

            mock_logger.log_performance.assert_called_once_with(
                "test_operation", 1.5, {}
            )


class TestGetLogger:
    """Tests para get_logger"""

    @pytest.mark.unit
    def test_get_logger(self):
        """Test obtención de logger"""
        logger = get_logger("test_module")

        assert isinstance(logger, TrackHSLogger)
        assert logger.logger.name == "test_module"

    @pytest.mark.unit
    def test_get_logger_with_mcp_client(self):
        """Test obtención de logger con cliente MCP"""
        mock_mcp_client = Mock()
        logger = get_logger("test_module", mock_mcp_client)

        assert isinstance(logger, TrackHSLogger)
        assert logger.mcp_client == mock_mcp_client
