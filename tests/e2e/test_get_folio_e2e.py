"""
Tests end-to-end para get_folio
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio


class TestGetFolioE2E:
    """Tests end-to-end para get_folio"""

    @pytest.fixture
    def api_client(self):
        """Cliente API mock - CORREGIDO sin patching de httpx"""
        # Crear mock directo del TrackHSApiClient siguiendo patrón de tests unitarios
        client = Mock(spec=TrackHSApiClient)
        client.get = AsyncMock()
        client.post = AsyncMock()
        client.request = AsyncMock()
        client.close = AsyncMock()

        # Context manager async support
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=None)

        # Configurar config mock
        client.config = Mock()
        client.config.base_url = "https://api-test.trackhs.com/api"
        client.config.timeout = 30

        return client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def tool_function(self, mock_mcp, api_client):
        """Función de la herramienta registrada"""
        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_get_folio(mock_mcp, api_client)
        return registered_function

    @pytest.mark.asyncio
    async def test_get_folio_e2e_success(
        self, tool_function, api_client, sample_folio_guest
    ):
        """Test flujo completo exitoso"""
        # Arrange
        api_client.get.return_value = sample_folio_guest

        # Act
        result = await tool_function(folio_id="12345")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 12345
        assert result["status"] == "open"
        assert result["type"] == "guest"
        assert result["currentBalance"] == 150.00
        assert result["realizedBalance"] == 100.00
        assert "_embedded" in result
        assert "_links" in result

    @pytest.mark.asyncio
    async def test_get_folio_e2e_different_types(
        self, tool_function, api_client, sample_folio_guest, sample_folio_master
    ):
        """Test folios tipo guest y master"""
        # Arrange
        api_client.get.side_effect = [sample_folio_guest, sample_folio_master]

        # Act - Test guest folio
        result_guest = await tool_function(folio_id="12345")

        # Act - Test master folio
        result_master = await tool_function(folio_id="67890")

        # Assert
        assert result_guest["type"] == "guest"
        assert result_guest["status"] == "open"
        assert result_guest["currentBalance"] == 150.00

        assert result_master["type"] == "master"
        assert result_master["status"] == "closed"
        assert result_master["realizedBalance"] == 2500.00
        assert result_master["hasException"] is True

    @pytest.mark.asyncio
    async def test_get_folio_e2e_with_exceptions(
        self, tool_function, api_client, sample_folio_master
    ):
        """Test folios con excepciones"""
        # Arrange
        api_client.get.return_value = sample_folio_master

        # Act
        result = await tool_function(folio_id="67890")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 67890
        assert result["hasException"] is True
        assert result["exceptionMessage"] == "Payment processing delay"
        assert result["status"] == "closed"

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_401(self, tool_function, api_client):
        """Test escenarios de error completos - 401"""

        # Arrange
        class UnauthorizedError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 401

        api_client.get.side_effect = UnauthorizedError("Unauthorized")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "No autorizado" in str(exc_info.value)
        assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_403(self, tool_function, api_client):
        """Test escenarios de error completos - 403"""

        # Arrange
        class ForbiddenError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 403

        api_client.get.side_effect = ForbiddenError("Forbidden")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Prohibido" in str(exc_info.value)
        assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_404(self, tool_function, api_client):
        """Test escenarios de error completos - 404"""

        # Arrange
        class NotFoundError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 404

        api_client.get.side_effect = NotFoundError("Not Found")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="99999")

        assert "Folio no encontrado" in str(exc_info.value)
        assert "99999" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_500(self, tool_function, api_client):
        """Test escenarios de error completos - 500"""

        # Arrange
        class InternalServerError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 500

        api_client.get.side_effect = InternalServerError("Internal Server Error")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error interno del servidor" in str(exc_info.value)
        assert "temporalmente no disponible" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_validation_errors(self, tool_function):
        """Test errores de validación en E2E"""
        # Test ID vacío
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="")
        assert "Parámetro 'folio_id' es requerido" in str(exc_info.value)

        # Test ID negativo
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="-1")
        assert "Valor inválido para 'folio_id'" in str(exc_info.value)

        # Test ID inválido
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="abc")
        assert "Valor inválido para 'folio_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_with_embedded_data(
        self, tool_function, api_client, sample_folio_guest
    ):
        """Test con datos embebidos completos"""
        # Arrange
        api_client.get.return_value = sample_folio_guest

        # Act
        result = await tool_function(folio_id="12345")

        # Assert
        assert isinstance(result, dict)
        assert "_embedded" in result
        assert "contact" in result["_embedded"]
        assert "travelAgent" in result["_embedded"]
        assert "company" in result["_embedded"]

        # Verificar datos del contacto
        contact = result["_embedded"]["contact"]
        assert contact["id"] == 1
        assert contact["firstName"] == "John"
        assert contact["lastName"] == "Doe"
        assert contact["primaryEmail"] == "john@example.com"

    @pytest.mark.asyncio
    async def test_get_folio_e2e_with_master_folio_rule(
        self, tool_function, api_client, sample_folio_master
    ):
        """Test con regla de folio maestro"""
        # Arrange
        api_client.get.return_value = sample_folio_master

        # Act
        result = await tool_function(folio_id="67890")

        # Assert
        assert isinstance(result, dict)
        assert "_embedded" in result
        assert "masterFolioRule" in result["_embedded"]

        master_rule = result["_embedded"]["masterFolioRule"]
        assert master_rule["id"] == 1
        assert master_rule["ruleId"] == 1
        assert "rule" in master_rule
        assert master_rule["rule"]["name"] == "Monthly Master Rule"

    @pytest.mark.asyncio
    async def test_get_folio_e2e_minimal_folio(
        self, tool_function, api_client, sample_folio_minimal
    ):
        """Test con folio mínimo"""
        # Arrange
        api_client.get.return_value = sample_folio_minimal

        # Act
        result = await tool_function(folio_id="11111")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 11111
        assert result["status"] == "open"
        # Campos opcionales pueden estar ausentes
        assert "type" not in result or result["type"] is None

    @pytest.mark.asyncio
    async def test_get_folio_e2e_network_timeout(self, tool_function, api_client):
        """Test timeout de red en E2E"""
        # Arrange
        import httpx

        api_client.get.side_effect = httpx.TimeoutException("Request timeout")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error al obtener el folio" in str(exc_info.value)
        assert "Request timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_network_connection_error(
        self, tool_function, api_client
    ):
        """Test error de conexión en E2E"""
        # Arrange
        import httpx

        api_client.get.side_effect = httpx.ConnectError("Connection failed")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error al obtener el folio" in str(exc_info.value)
        assert "Connection failed" in str(exc_info.value)
