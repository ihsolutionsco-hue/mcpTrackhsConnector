"""
Tests E2E para el servidor MCP completo
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.server import main, register_all_components


class TestServerE2E:
    """Tests E2E para el servidor completo"""

    @pytest.fixture
    def mock_config(self):
        """Configuración mock para testing"""
        return TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    @pytest.fixture
    def mock_api_client(self, mock_config):
        """API client mock"""
        with patch("src.trackhs_mcp.core.api_client.TrackHSAuth") as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {
                "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            return TrackHSApiClient(mock_config)

    @pytest.fixture
    def mock_mcp(self):
        """Servidor MCP mock"""
        mcp = Mock()
        mcp.tool = Mock()
        mcp.resource = Mock()
        mcp.prompt = Mock()
        mcp.run = Mock()
        return mcp

    @pytest.mark.e2e
    def test_server_initialization(self, mock_config):
        """Test inicialización del servidor"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
            patch("src.trackhs_mcp.server.FastMCP") as mock_fastmcp_class,
        ):

            mock_config_class.return_value = mock_config
            mock_client_class.return_value = Mock()
            mock_fastmcp_class.return_value = Mock()

            # Importar y ejecutar la inicialización
            from src.trackhs_mcp.server import api_client, config, mcp

            assert config == mock_config
            assert api_client is not None
            assert mcp is not None

    @pytest.mark.e2e
    def test_register_all_components(self, mock_mcp, mock_api_client):
        """Test registro de todos los componentes"""
        with patch("src.trackhs_mcp.server.register_all_components") as mock_register:
            register_all_components()

            # Verificar que se llamó la función de registro
            mock_register.assert_called_once()

    @pytest.mark.e2e
    def test_register_all_components_integration(self, mock_mcp, mock_api_client):
        """Test integración de registro de componentes"""
        # Importar las funciones de registro
        from src.trackhs_mcp.prompts import register_all_prompts
        from src.trackhs_mcp.resources import register_all_resources
        from src.trackhs_mcp.tools import register_all_tools

        # Registrar todos los componentes
        register_all_tools(mock_mcp, mock_api_client)
        register_all_resources(mock_mcp, mock_api_client)
        register_all_prompts(mock_mcp, mock_api_client)

        # Verificar que se registraron herramientas
        assert mock_mcp.tool.call_count >= 1  # Al menos search_reservations

        # Verificar que se registraron recursos
        assert mock_mcp.resource.call_count >= 7  # Al menos 7 recursos

        # Verificar que se registraron prompts
        assert mock_mcp.prompt.call_count >= 8  # Al menos 8 prompts

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_server_with_real_components(self, mock_config):
        """Test servidor con componentes reales"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
            patch("src.trackhs_mcp.server.FastMCP") as mock_fastmcp_class,
        ):

            mock_config_class.return_value = mock_config
            mock_client_class.return_value = Mock()
            mock_mcp = Mock()
            mock_mcp.tool = Mock()
            mock_mcp.resource = Mock()
            mock_mcp.prompt = Mock()
            mock_mcp.run = Mock()
            mock_fastmcp_class.return_value = mock_mcp

            # Importar y ejecutar la inicialización
            from src.trackhs_mcp.server import register_all_components

            # Ejecutar registro de componentes
            register_all_components()

            # Verificar que se registraron componentes
            assert mock_mcp.tool.call_count >= 1
            assert mock_mcp.resource.call_count >= 7
            assert mock_mcp.prompt.call_count >= 8

    @pytest.mark.e2e
    def test_main_function(self):
        """Test función main"""
        with patch("src.trackhs_mcp.server.mcp") as mock_mcp:
            mock_mcp.run = Mock()

            # Ejecutar main
            main()

            # Verificar que se llamó run
            mock_mcp.run.assert_called_once()

    @pytest.mark.e2e
    def test_server_with_environment_variables(self):
        """Test servidor con variables de entorno"""
        with patch.dict(
            "os.environ",
            {
                "TRACKHS_API_URL": "https://api-test.trackhs.com/api",
                "TRACKHS_USERNAME": "test_user",
                "TRACKHS_PASSWORD": "test_password",
                "TRACKHS_TIMEOUT": "30",
            },
        ):
            with (
                patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
                patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
                patch("src.trackhs_mcp.server.FastMCP") as mock_fastmcp_class,
            ):

                mock_config_class.return_value = Mock()
                mock_client_class.return_value = Mock()
                mock_fastmcp_class.return_value = Mock()

                # Importar y verificar que se usan las variables de entorno
                from src.trackhs_mcp.server import config

                # Verificar que se creó la configuración
                mock_config_class.assert_called_once()
                call_args = mock_config_class.call_args
                assert call_args[1]["base_url"] == "https://api-test.trackhs.com/api"
                assert call_args[1]["username"] == "test_user"
                assert call_args[1]["password"] == "test_password"
                assert call_args[1]["timeout"] == 30

    @pytest.mark.e2e
    def test_server_error_handling(self):
        """Test manejo de errores en el servidor"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
        ):

            # Simular error en la configuración
            mock_config_class.side_effect = Exception("Configuration error")

            with pytest.raises(Exception, match="Configuration error"):
                from src.trackhs_mcp.server import config

    @pytest.mark.e2e
    def test_server_import_structure(self):
        """Test estructura de imports del servidor"""
        # Verificar que todos los imports necesarios están disponibles
        try:
            from src.trackhs_mcp.server import (
                FastMCP,
                Path,
                TrackHSApiClient,
                TrackHSConfig,
                load_dotenv,
                main,
                os,
                register_all_components,
                sys,
            )

            assert True  # Si llegamos aquí, todos los imports funcionan
        except ImportError as e:
            pytest.fail(f"Import error: {e}")

    @pytest.mark.e2e
    def test_server_path_manipulation(self):
        """Test manipulación de paths en el servidor"""
        with (
            patch("src.trackhs_mcp.server.sys") as mock_sys,
            patch("src.trackhs_mcp.server.Path") as mock_path,
        ):

            mock_path.return_value.parent.parent = Mock()
            mock_path.return_value.parent.parent.__str__ = Mock(
                return_value="/test/path"
            )

            # Importar el servidor
            from src.trackhs_mcp.server import sys

            # Verificar que se manipuló el path
            mock_sys.path.insert.assert_called_once()

    @pytest.mark.e2e
    def test_server_dotenv_loading(self):
        """Test carga de variables de entorno"""
        with patch("src.trackhs_mcp.server.load_dotenv") as mock_load_dotenv:
            # Importar el servidor
            from src.trackhs_mcp.server import load_dotenv

            # Verificar que se llamó load_dotenv
            mock_load_dotenv.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_server_component_registration_flow(self, mock_config):
        """Test flujo completo de registro de componentes"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
            patch("src.trackhs_mcp.server.FastMCP") as mock_fastmcp_class,
        ):

            mock_config_class.return_value = mock_config
            mock_client_class.return_value = Mock()
            mock_mcp = Mock()
            mock_mcp.tool = Mock()
            mock_mcp.resource = Mock()
            mock_mcp.prompt = Mock()
            mock_fastmcp_class.return_value = mock_mcp

            # Simular el flujo completo
            from src.trackhs_mcp.server import register_all_components

            # Ejecutar registro
            register_all_components()

            # Verificar que se registraron todos los tipos de componentes
            assert mock_mcp.tool.call_count > 0, "No tools registered"
            assert mock_mcp.resource.call_count > 0, "No resources registered"
            assert mock_mcp.prompt.call_count > 0, "No prompts registered"

            # Verificar que se registraron componentes específicos
            tool_calls = [call[0][0] for call in mock_mcp.tool.call_args_list]
            resource_calls = [call[0][0] for call in mock_mcp.resource.call_args_list]
            prompt_calls = [call[0][0] for call in mock_mcp.prompt.call_args_list]

            # Verificar herramientas específicas
            assert any(
                "search_reservations" in str(call) for call in tool_calls
            ), "search_reservations not registered"

            # Verificar recursos específicos
            assert any(
                "reservations" in str(call) for call in resource_calls
            ), "reservations resource not registered"
            assert any(
                "units" in str(call) for call in resource_calls
            ), "units resource not registered"
            assert any(
                "status" in str(call) for call in resource_calls
            ), "status resource not registered"

            # Verificar prompts específicos
            assert any(
                "check-today" in str(call) for call in prompt_calls
            ), "check-today prompt not registered"
            assert any(
                "unit-availability" in str(call) for call in prompt_calls
            ), "unit-availability prompt not registered"

    @pytest.mark.e2e
    def test_server_configuration_validation(self, mock_config):
        """Test validación de configuración del servidor"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
        ):

            mock_config_class.return_value = mock_config
            mock_client_class.return_value = Mock()

            # Importar y verificar configuración
            from src.trackhs_mcp.server import config

            # Verificar que se creó la configuración con los valores correctos
            mock_config_class.assert_called_once()
            call_args = mock_config_class.call_args[1]

            assert "base_url" in call_args
            assert "username" in call_args
            assert "password" in call_args
            assert "timeout" in call_args

    @pytest.mark.e2e
    def test_server_api_client_initialization(self, mock_config):
        """Test inicialización del API client"""
        with (
            patch("src.trackhs_mcp.server.TrackHSConfig") as mock_config_class,
            patch("src.trackhs_mcp.server.TrackHSApiClient") as mock_client_class,
        ):

            mock_config_class.return_value = mock_config
            mock_client_class.return_value = Mock()

            # Importar y verificar API client
            from src.trackhs_mcp.server import api_client

            # Verificar que se creó el API client
            mock_client_class.assert_called_once_with(mock_config)

    @pytest.mark.e2e
    def test_server_fastmcp_initialization(self):
        """Test inicialización de FastMCP"""
        with patch("src.trackhs_mcp.server.FastMCP") as mock_fastmcp_class:
            mock_fastmcp_class.return_value = Mock()

            # Importar y verificar FastMCP
            from src.trackhs_mcp.server import mcp

            # Verificar que se creó FastMCP
            mock_fastmcp_class.assert_called_once_with("TrackHS MCP Server")
