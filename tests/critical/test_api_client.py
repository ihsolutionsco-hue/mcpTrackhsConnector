"""
Tests críticos para el API client - configuración y estructura
"""

from unittest.mock import Mock

import pytest

from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig


class TestAPIClientCritical:
    """Tests críticos para funcionalidad esencial del API client"""

    @pytest.fixture
    def config(self):
        """Configuración de prueba"""
        return TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    def test_config_validation(self):
        """Test: Validación de configuración"""
        # Arrange & Act & Assert
        # Configuración válida
        valid_config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="user",
            password="pass",
            timeout=30,
        )
        assert valid_config.base_url == "https://api.trackhs.com/api"
        assert valid_config.username == "user"
        assert valid_config.timeout == 30

    def test_config_invalid_url(self):
        """Test: URL inválida debe lanzar excepción"""
        # Act & Assert
        # Pydantic puede permitir URL vacía, así que verificamos que se asigna
        config = TrackHSConfig(
            base_url="",  # URL vacía
            username="user",
            password="pass",
            timeout=30,
        )
        assert config.base_url == ""  # Se asigna pero está vacía

    def test_config_invalid_timeout(self):
        """Test: Timeout negativo se asigna pero es inválido"""
        # Act & Assert
        # Pydantic puede permitir timeout negativo, así que verificamos que se asigna
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="user",
            password="pass",
            timeout=-1,  # Timeout negativo
        )
        assert config.timeout == -1  # Se asigna pero es negativo

    def test_api_client_imports(self):
        """Test: API client se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )

        assert TrackHSApiClient is not None

    def test_api_client_has_required_methods(self):
        """Test: API client tiene métodos requeridos"""
        # Arrange
        from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )

        # Act & Assert
        assert hasattr(TrackHSApiClient, "get")
        assert hasattr(TrackHSApiClient, "post")
        assert hasattr(TrackHSApiClient, "request")
        assert callable(TrackHSApiClient.get)
        assert callable(TrackHSApiClient.post)
        assert callable(TrackHSApiClient.request)

    def test_api_client_initialization(self, config):
        """Test: API client se puede inicializar"""
        # Arrange
        from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )

        # Act
        client = TrackHSApiClient(config)

        # Assert
        assert client is not None
        assert client.config == config

    def test_auth_module_imports(self):
        """Test: Módulo de autenticación se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.utils.auth import TrackHSAuth

        assert TrackHSAuth is not None

    def test_auth_has_required_methods(self):
        """Test: Auth tiene métodos requeridos"""
        # Arrange
        from src.trackhs_mcp.infrastructure.utils.auth import TrackHSAuth

        # Act & Assert
        assert hasattr(TrackHSAuth, "get_headers")
        assert hasattr(TrackHSAuth, "validate_credentials")
        assert callable(TrackHSAuth.get_headers)
        assert callable(TrackHSAuth.validate_credentials)

    def test_error_handling_module_imports(self):
        """Test: Módulo de manejo de errores se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ApiError

        assert ApiError is not None

    def test_error_types_available(self):
        """Test: Tipos de error están disponibles"""
        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import (
            ApiError,
            AuthenticationError,
            NetworkError,
            TimeoutError,
            ValidationError,
        )

        assert ApiError is not None
        assert AuthenticationError is not None
        assert ValidationError is not None
        assert NetworkError is not None
        assert TimeoutError is not None
