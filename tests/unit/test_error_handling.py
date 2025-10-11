"""
Tests unitarios para manejo de errores
"""

from unittest.mock import Mock, patch

import pytest

from src.trackhs_mcp.core.error_handling import (
    ApiError,
    AuthenticationError,
    ErrorHandler,
    ErrorSeverity,
    NetworkError,
    TimeoutError,
    TrackHSError,
    ValidationError,
    error_handler,
    get_error_stats,
    validate_param_types,
    validate_required_params,
)


class TestTrackHSError:
    """Tests para TrackHSError"""

    @pytest.mark.unit
    def test_trackhs_error_creation(self):
        """Test creación de TrackHSError"""
        error = TrackHSError("Test error", ErrorSeverity.HIGH, {"key": "value"})

        assert error.message == "Test error"
        assert error.severity == ErrorSeverity.HIGH
        assert error.context == {"key": "value"}
        assert str(error) == "Test error"

    @pytest.mark.unit
    def test_trackhs_error_with_defaults(self):
        """Test TrackHSError con valores por defecto"""
        error = TrackHSError("Test error")

        assert error.message == "Test error"
        assert error.severity == ErrorSeverity.MEDIUM
        assert error.context == {}

    @pytest.mark.unit
    def test_trackhs_error_inheritance(self):
        """Test que TrackHSError hereda de Exception"""
        error = TrackHSError("Test error")
        assert isinstance(error, Exception)


class TestApiError:
    """Tests para ApiError"""

    @pytest.mark.unit
    def test_api_error_creation(self):
        """Test creación de ApiError"""
        error = ApiError("API error", 404, "/test")

        assert error.message == "API error"
        assert error.severity == ErrorSeverity.HIGH
        assert error.context["status_code"] == 404
        assert error.context["endpoint"] == "/test"

    @pytest.mark.unit
    def test_api_error_without_context(self):
        """Test ApiError sin contexto adicional"""
        error = ApiError("API error")

        assert error.message == "API error"
        assert error.severity == ErrorSeverity.HIGH
        assert error.context == {}


class TestAuthenticationError:
    """Tests para AuthenticationError"""

    @pytest.mark.unit
    def test_authentication_error_creation(self):
        """Test creación de AuthenticationError"""
        error = AuthenticationError("Auth failed")

        assert error.message == "Auth failed"
        assert error.severity == ErrorSeverity.CRITICAL

    @pytest.mark.unit
    def test_authentication_error_default_message(self):
        """Test AuthenticationError con mensaje por defecto"""
        error = AuthenticationError()

        assert error.message == "Authentication failed"
        assert error.severity == ErrorSeverity.CRITICAL


class TestValidationError:
    """Tests para ValidationError"""

    @pytest.mark.unit
    def test_validation_error_creation(self):
        """Test creación de ValidationError"""
        error = ValidationError("Invalid field", "field_name")

        assert error.message == "Invalid field"
        assert error.severity == ErrorSeverity.MEDIUM
        assert error.context["field"] == "field_name"

    @pytest.mark.unit
    def test_validation_error_without_field(self):
        """Test ValidationError sin campo específico"""
        error = ValidationError("Invalid data")

        assert error.message == "Invalid data"
        assert error.severity == ErrorSeverity.MEDIUM
        assert "field" not in error.context


class TestNetworkError:
    """Tests para NetworkError"""

    @pytest.mark.unit
    def test_network_error_creation(self):
        """Test creación de NetworkError"""
        error = NetworkError("Network failed")

        assert error.message == "Network failed"
        assert error.severity == ErrorSeverity.HIGH


class TestTimeoutError:
    """Tests para TimeoutError"""

    @pytest.mark.unit
    def test_timeout_error_creation(self):
        """Test creación de TimeoutError"""
        error = TimeoutError("Request timeout", 30.0)

        assert error.message == "Request timeout"
        assert error.severity == ErrorSeverity.MEDIUM
        assert error.context["timeout_seconds"] == 30.0

    @pytest.mark.unit
    def test_timeout_error_without_timeout(self):
        """Test TimeoutError sin tiempo específico"""
        error = TimeoutError("Request timeout")

        assert error.message == "Request timeout"
        assert error.severity == ErrorSeverity.MEDIUM
        assert "timeout_seconds" not in error.context


class TestErrorHandler:
    """Tests para ErrorHandler"""

    @pytest.fixture
    def error_handler(self):
        """Crear ErrorHandler para testing"""
        return ErrorHandler()

    @pytest.mark.unit
    def test_error_handler_init(self, error_handler):
        """Test inicialización de ErrorHandler"""
        assert error_handler._error_counts == {}
        assert error_handler.logger is not None

    @pytest.mark.unit
    def test_handle_error(self, error_handler):
        """Test manejo de errores"""
        error = TrackHSError("Test error", ErrorSeverity.MEDIUM)

        with patch.object(error_handler.logger, "log") as mock_log:
            error_handler.handle_error(error, "test_operation")

            mock_log.assert_called_once()
            assert error_handler._error_counts["test_operation_medium"] == 1

    @pytest.mark.unit
    def test_handle_critical_error(self, error_handler):
        """Test manejo de errores críticos"""
        error = TrackHSError("Critical error", ErrorSeverity.CRITICAL)

        with patch.object(error_handler.logger, "log") as mock_log, patch.object(
            error_handler.logger, "critical"
        ) as mock_critical:
            error_handler.handle_error(error, "critical_operation")

            mock_log.assert_called_once()
            mock_critical.assert_called_once()

    @pytest.mark.unit
    def test_get_error_stats(self, error_handler):
        """Test obtención de estadísticas de errores"""
        error1 = TrackHSError("Error 1", ErrorSeverity.LOW)
        error2 = TrackHSError("Error 2", ErrorSeverity.HIGH)

        with patch.object(error_handler.logger, "log"):
            error_handler.handle_error(error1, "op1")
            error_handler.handle_error(error2, "op2")

        stats = error_handler.get_error_stats()

        assert stats["total_errors"] == 2
        assert stats["error_counts"]["op1_low"] == 1
        assert stats["error_counts"]["op2_high"] == 1
        assert "timestamp" in stats


class TestErrorHandlerDecorator:
    """Tests para decorador error_handler"""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_handler_async_success(self):
        """Test decorador con función async exitosa"""

        @error_handler("test_operation")
        async def test_func():
            return "success"

        result = await test_func()
        assert result == "success"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_handler_async_with_trackhs_error(self):
        """Test decorador con TrackHSError en función async"""

        @error_handler("test_operation", reraise=True)
        async def test_func():
            raise ValidationError("Invalid input")

        with pytest.raises(ValidationError):
            await test_func()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_handler_async_with_generic_error(self):
        """Test decorador con error genérico en función async"""

        @error_handler("test_operation", reraise=True)
        async def test_func():
            raise ValueError("Generic error")

        with pytest.raises(TrackHSError):
            await test_func()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_handler_async_with_return_default(self):
        """Test decorador con return_default en función async"""

        @error_handler("test_operation", reraise=False, return_default="default")
        async def test_func():
            raise ValueError("Generic error")

        result = await test_func()
        assert result == "default"

    @pytest.mark.unit
    def test_error_handler_sync_success(self):
        """Test decorador con función sync exitosa"""

        @error_handler("test_operation")
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    @pytest.mark.unit
    def test_error_handler_sync_with_error(self):
        """Test decorador con error en función sync"""

        @error_handler("test_operation", reraise=True)
        def test_func():
            raise ValueError("Generic error")

        with pytest.raises(TrackHSError):
            test_func()


class TestValidationFunctions:
    """Tests para funciones de validación"""

    @pytest.mark.unit
    def test_validate_required_params_success(self):
        """Test validación exitosa de parámetros requeridos"""
        params = {"param1": "value1", "param2": "value2"}
        required = ["param1", "param2"]

        # No debe lanzar excepción
        validate_required_params(params, required)

    @pytest.mark.unit
    def test_validate_required_params_missing(self):
        """Test validación con parámetros faltantes"""
        params = {"param1": "value1"}
        required = ["param1", "param2"]

        with pytest.raises(ValidationError, match="Missing required parameters"):
            validate_required_params(params, required)

    @pytest.mark.unit
    def test_validate_required_params_none_value(self):
        """Test validación con valores None"""
        params = {"param1": "value1", "param2": None}
        required = ["param1", "param2"]

        with pytest.raises(ValidationError, match="Missing required parameters"):
            validate_required_params(params, required)

    @pytest.mark.unit
    def test_validate_param_types_success(self):
        """Test validación exitosa de tipos"""
        params = {"param1": "string", "param2": 123}
        type_mapping = {"param1": str, "param2": int}

        # No debe lanzar excepción
        validate_param_types(params, type_mapping)

    @pytest.mark.unit
    def test_validate_param_types_invalid(self):
        """Test validación con tipos inválidos"""
        params = {"param1": "string", "param2": "not_int"}
        type_mapping = {"param1": str, "param2": int}

        with pytest.raises(ValidationError, match="must be of type int"):
            validate_param_types(params, type_mapping)

    @pytest.mark.unit
    def test_validate_param_types_missing_param(self):
        """Test validación con parámetro faltante"""
        params = {"param1": "string"}
        type_mapping = {"param1": str, "param2": int}

        # No debe lanzar excepción si el parámetro no está presente
        validate_param_types(params, type_mapping)

    @pytest.mark.unit
    def test_validate_param_types_none_value(self):
        """Test validación con valor None"""
        params = {"param1": "string", "param2": None}
        type_mapping = {"param1": str, "param2": int}

        # No debe lanzar excepción si el valor es None
        validate_param_types(params, type_mapping)


class TestErrorStats:
    """Tests para estadísticas de errores"""

    @pytest.mark.unit
    def test_get_error_stats(self):
        """Test obtención de estadísticas globales"""
        stats = get_error_stats()

        assert "error_counts" in stats
        assert "total_errors" in stats
        assert "timestamp" in stats
        assert isinstance(stats["error_counts"], dict)
        assert isinstance(stats["total_errors"], int)
