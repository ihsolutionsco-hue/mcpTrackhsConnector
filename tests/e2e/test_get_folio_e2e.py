"""
Tests end-to-end para get_folio
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestGetFolioE2E:
    """Tests end-to-end para get_folio"""

    @pytest.fixture
    def mock_httpx_client(self):
        """Mock del cliente HTTPX"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def api_client(self, mock_httpx_client):
        """Cliente API con mock HTTPX"""
        with patch(
            "src.trackhs_mcp.infrastructure.adapters.trackhs_api_client.httpx.AsyncClient"
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value = mock_httpx_client
            config = Mock()
            config.base_url = "https://api-test.trackhs.com/api"
            config.timeout = 30
            return TrackHSApiClient(config)

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def tool_function(self, mock_mcp, api_client):
        """Función de la herramienta registrada"""
        register_get_folio(mock_mcp, api_client)
        return mock_mcp.tool.call_args[0][0]  # Obtener la función decorada

    @pytest.mark.asyncio
    async def test_get_folio_e2e_success(
        self, tool_function, mock_httpx_client, sample_folio_guest
    ):
        """Test flujo completo exitoso"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_guest
        mock_httpx_client.get.return_value = mock_response

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
        self, tool_function, mock_httpx_client, sample_folio_guest, sample_folio_master
    ):
        """Test folios tipo guest y master"""
        # Arrange
        mock_response_guest = Mock()
        mock_response_guest.status_code = 200
        mock_response_guest.json.return_value = sample_folio_guest

        mock_response_master = Mock()
        mock_response_master.status_code = 200
        mock_response_master.json.return_value = sample_folio_master

        mock_httpx_client.get.side_effect = [mock_response_guest, mock_response_master]

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
        self, tool_function, mock_httpx_client, sample_folio_master
    ):
        """Test folios con excepciones"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_master
        mock_httpx_client.get.return_value = mock_response

        # Act
        result = await tool_function(folio_id="67890")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 67890
        assert result["hasException"] is True
        assert result["exceptionMessage"] == "Payment processing delay"
        assert result["status"] == "closed"

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_401(
        self, tool_function, mock_httpx_client
    ):
        """Test escenarios de error completos - 401"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("Unauthorized")
        mock_httpx_client.get.return_value = mock_response

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "No autorizado" in str(exc_info.value)
        assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_403(
        self, tool_function, mock_httpx_client
    ):
        """Test escenarios de error completos - 403"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = Exception("Forbidden")
        mock_httpx_client.get.return_value = mock_response

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Prohibido" in str(exc_info.value)
        assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_404(
        self, tool_function, mock_httpx_client
    ):
        """Test escenarios de error completos - 404"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not Found")
        mock_httpx_client.get.return_value = mock_response

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="99999")

        assert "Folio no encontrado" in str(exc_info.value)
        assert "99999" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_error_scenarios_500(
        self, tool_function, mock_httpx_client
    ):
        """Test escenarios de error completos - 500"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Internal Server Error")
        mock_httpx_client.get.return_value = mock_response

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
        assert "folio_id es requerido y no puede estar vacío" in str(exc_info.value)

        # Test ID negativo
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="-1")
        assert "folio_id debe ser un número entero positivo válido" in str(
            exc_info.value
        )

        # Test ID inválido
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="abc")
        assert "folio_id debe ser un número entero positivo válido" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_get_folio_e2e_with_embedded_data(
        self, tool_function, mock_httpx_client, sample_folio_guest
    ):
        """Test con datos embebidos completos"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_guest
        mock_httpx_client.get.return_value = mock_response

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
        self, tool_function, mock_httpx_client, sample_folio_master
    ):
        """Test con regla de folio maestro"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_master
        mock_httpx_client.get.return_value = mock_response

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
        self, tool_function, mock_httpx_client, sample_folio_minimal
    ):
        """Test con folio mínimo"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_minimal
        mock_httpx_client.get.return_value = mock_response

        # Act
        result = await tool_function(folio_id="11111")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 11111
        assert result["status"] == "open"
        # Campos opcionales pueden estar ausentes
        assert "type" not in result or result["type"] is None

    @pytest.mark.asyncio
    async def test_get_folio_e2e_network_timeout(
        self, tool_function, mock_httpx_client
    ):
        """Test timeout de red en E2E"""
        # Arrange
        import httpx

        mock_httpx_client.get.side_effect = httpx.TimeoutException("Request timeout")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error al obtener el folio" in str(exc_info.value)
        assert "Request timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_e2e_network_connection_error(
        self, tool_function, mock_httpx_client
    ):
        """Test error de conexión en E2E"""
        # Arrange
        import httpx

        mock_httpx_client.get.side_effect = httpx.ConnectError("Connection failed")

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error al obtener el folio" in str(exc_info.value)
        assert "Connection failed" in str(exc_info.value)
