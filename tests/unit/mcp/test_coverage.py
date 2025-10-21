"""
Test simple para mejorar la cobertura de código
"""

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

# Importar el código principal para mejorar cobertura
from src.trackhs_mcp.__init__ import __author__, __email__, __version__
from src.trackhs_mcp.domain.exceptions.api_exceptions import (
    ApiError,
    AuthenticationError,
    NetworkError,
    TimeoutError,
    TrackHSError,
    ValidationError,
)
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.domain.value_objects.request import RequestOptions
from src.trackhs_mcp.infrastructure.utils.error_handling import ErrorHandler
from src.trackhs_mcp.infrastructure.utils.user_friendly_messages import (
    format_boolean_error,
    format_date_error,
    format_id_list_error,
    format_range_error,
    format_required_error,
    format_type_error,
)


class TestCoverage:
    """Tests para mejorar la cobertura de código"""

    def test_package_imports(self):
        """Test de imports del paquete principal"""
        assert __version__ is not None
        assert __author__ is not None
        assert __email__ is not None

    def test_exceptions(self):
        """Test de excepciones del dominio"""
        # Test TrackHSError
        error = TrackHSError("Test error", severity="high")
        assert str(error) == "Test error"
        assert error.severity == "high"

        # Test ApiError
        api_error = ApiError("API error", status_code=500)
        assert str(api_error) == "API error"
        assert api_error.status_code == 500

        # Test AuthenticationError
        auth_error = AuthenticationError("Auth failed")
        assert str(auth_error) == "Auth failed"

        # Test ValidationError
        validation_error = ValidationError("Invalid input", field="test_field")
        assert str(validation_error) == "Invalid input"
        assert validation_error.field == "test_field"

        # Test NetworkError
        network_error = NetworkError("Network failed")
        assert str(network_error) == "Network failed"

        # Test TimeoutError
        timeout_error = TimeoutError("Request timeout", timeout=30)
        assert str(timeout_error) == "Request timeout"
        assert timeout_error.timeout == 30

    def test_config_objects(self):
        """Test de objetos de configuración"""
        # Test TrackHSConfig
        config = TrackHSConfig(
            base_url="https://api.example.com",
            username="test_user",
            password="test_pass",
        )
        assert config.base_url == "https://api.example.com"
        assert config.username == "test_user"
        assert config.password == "test_pass"

        # Test RequestOptions
        options = RequestOptions(method="GET", timeout=30, retries=3)
        assert options.method == "GET"
        assert options.timeout == 30
        assert options.retries == 3

    def test_error_handler(self):
        """Test del manejador de errores"""
        handler = ErrorHandler()

        # Test manejo de error
        result = handler.handle_error(TrackHSError("Test error"))
        assert result is not None

        # Test estadísticas
        stats = handler.get_error_stats()
        assert isinstance(stats, dict)

    def test_user_friendly_messages(self):
        """Test de mensajes amigables al usuario"""
        # Test format_date_error
        date_msg = format_date_error("Invalid date")
        assert isinstance(date_msg, str)
        assert "fecha" in date_msg.lower()

        # Test format_type_error
        type_msg = format_type_error("Invalid type")
        assert isinstance(type_msg, str)

        # Test format_range_error
        range_msg = format_range_error("Out of range", min_val=1, max_val=10)
        assert isinstance(range_msg, str)

        # Test format_required_error
        required_msg = format_required_error("Missing field")
        assert isinstance(required_msg, str)

        # Test format_boolean_error
        boolean_msg = format_boolean_error("Invalid boolean")
        assert isinstance(boolean_msg, str)

        # Test format_id_list_error
        id_list_msg = format_id_list_error("Invalid ID list")
        assert isinstance(id_list_msg, str)

    def test_fastmcp_basic_functionality(self):
        """Test básico de FastMCP"""
        mcp = FastMCP("Test Server")
        mcp.add_middleware(
            ErrorHandlingMiddleware(include_traceback=False, transform_errors=True)
        )

        @mcp.tool("test_tool")
        def test_tool() -> dict:
            return {"message": "Hello World"}

        assert mcp.name == "Test Server"
        assert len(mcp._middleware) > 0
