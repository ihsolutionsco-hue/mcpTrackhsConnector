"""
Tests unitarios para TrackHSAuth
"""

import base64

import pytest

from src.trackhs_mcp.core.auth import TrackHSAuth
from src.trackhs_mcp.core.types import TrackHSConfig


class TestTrackHSAuth:
    """Tests para TrackHSAuth"""

    @pytest.fixture
    def valid_config(self):
        """Configuración válida para testing"""
        return TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    @pytest.fixture
    def invalid_config(self):
        """Configuración inválida para testing"""
        return TrackHSConfig(base_url="", username="", password="", timeout=30)

    @pytest.mark.unit
    def test_init_valid_credentials(self, valid_config):
        """Test inicialización con credenciales válidas"""
        auth = TrackHSAuth(valid_config)
        assert auth.config == valid_config

    @pytest.mark.unit
    def test_init_invalid_credentials(self, invalid_config):
        """Test inicialización con credenciales inválidas"""
        with pytest.raises(ValueError, match="Username y password son requeridos"):
            TrackHSAuth(invalid_config)

    @pytest.mark.unit
    def test_init_missing_base_url(self):
        """Test inicialización sin base URL"""
        config = TrackHSConfig(
            base_url="", username="test_user", password="test_password", timeout=30
        )
        with pytest.raises(ValueError, match="Base URL es requerida"):
            TrackHSAuth(config)

    @pytest.mark.unit
    def test_get_auth_header(self, valid_config):
        """Test generación de header de autenticación"""
        auth = TrackHSAuth(valid_config)
        header = auth.get_auth_header()

        # Decodificar y verificar
        encoded_part = header.split(" ")[1]  # Remover "Basic "
        decoded = base64.b64decode(encoded_part).decode("utf-8")
        assert decoded == "test_user:test_password"
        assert header.startswith("Basic ")

    @pytest.mark.unit
    def test_get_headers(self, valid_config):
        """Test generación de headers completos"""
        auth = TrackHSAuth(valid_config)
        headers = auth.get_headers()

        expected_headers = {
            "Authorization": "Basic "
            + base64.b64encode("test_user:test_password".encode("utf-8")).decode(
                "utf-8"
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        assert headers == expected_headers
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert "Accept" in headers

    @pytest.mark.unit
    def test_validate_credentials_valid(self, valid_config):
        """Test validación de credenciales válidas"""
        auth = TrackHSAuth(valid_config)
        assert auth.validate_credentials() is True

    @pytest.mark.unit
    def test_validate_credentials_invalid(self, invalid_config):
        """Test validación de credenciales inválidas"""
        # Crear auth sin validar en init
        auth = TrackHSAuth.__new__(TrackHSAuth)
        auth.config = invalid_config
        assert auth.validate_credentials() is False

    @pytest.mark.unit
    def test_validate_credentials_missing_username(self):
        """Test validación con username faltante"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="",
            password="test_password",
            timeout=30,
        )
        auth = TrackHSAuth.__new__(TrackHSAuth)
        auth.config = config
        assert auth.validate_credentials() is False

    @pytest.mark.unit
    def test_validate_credentials_missing_password(self):
        """Test validación con password faltante"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="test_user",
            password="",
            timeout=30,
        )
        auth = TrackHSAuth.__new__(TrackHSAuth)
        auth.config = config
        assert auth.validate_credentials() is False

    @pytest.mark.unit
    def test_validate_credentials_missing_base_url(self):
        """Test validación con base URL faltante"""
        config = TrackHSConfig(
            base_url="", username="test_user", password="test_password", timeout=30
        )
        auth = TrackHSAuth.__new__(TrackHSAuth)
        auth.config = config
        assert auth.validate_credentials() is False

    @pytest.mark.unit
    def test_auth_header_encoding(self, valid_config):
        """Test que el encoding del header sea correcto"""
        auth = TrackHSAuth(valid_config)
        header = auth.get_auth_header()

        # Verificar que es base64 válido
        encoded_part = header.split(" ")[1]
        try:
            decoded = base64.b64decode(encoded_part).decode("utf-8")
            assert decoded == "test_user:test_password"
        except Exception:
            pytest.fail("Header de autenticación no es base64 válido")

    @pytest.mark.unit
    def test_headers_consistency(self, valid_config):
        """Test que los headers sean consistentes entre llamadas"""
        auth = TrackHSAuth(valid_config)
        headers1 = auth.get_headers()
        headers2 = auth.get_headers()

        assert headers1 == headers2
        assert headers1["Authorization"] == headers2["Authorization"]

    @pytest.mark.unit
    def test_special_characters_in_credentials(self):
        """Test credenciales con caracteres especiales"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="user@domain.com",
            password="pass:word@123",
            timeout=30,
        )
        auth = TrackHSAuth(config)
        header = auth.get_auth_header()

        # Decodificar y verificar
        encoded_part = header.split(" ")[1]
        decoded = base64.b64decode(encoded_part).decode("utf-8")
        assert decoded == "user@domain.com:pass:word@123"

    @pytest.mark.unit
    def test_unicode_credentials(self):
        """Test credenciales con caracteres unicode"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="usuario_ñ",
            password="contraseña_123",
            timeout=30,
        )
        auth = TrackHSAuth(config)
        header = auth.get_auth_header()

        # Decodificar y verificar
        encoded_part = header.split(" ")[1]
        decoded = base64.b64decode(encoded_part).decode("utf-8")
        assert decoded == "usuario_ñ:contraseña_123"
