"""
Tests de integración para get_folio
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase
from src.trackhs_mcp.domain.entities.folios import Folio, GetFolioParams
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestGetFolioIntegration:
    """Tests de integración para get_folio"""

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

    @pytest.mark.asyncio
    async def test_get_folio_api_integration(
        self, api_client, mock_httpx_client, sample_folio_guest
    ):
        """Test integración con API real (mock)"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_guest
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"
        assert result.type == "guest"
        mock_httpx_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_with_auth(
        self, api_client, mock_httpx_client, sample_folio_guest
    ):
        """Test con autenticación"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_guest
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345

        # Verificar que se llamó con headers de autenticación
        call_args = mock_httpx_client.get.call_args
        assert "headers" in call_args.kwargs
        assert "Authorization" in call_args.kwargs["headers"]

    @pytest.mark.asyncio
    async def test_get_folio_complete_flow(
        self, api_client, mock_httpx_client, sample_folio_master
    ):
        """Test flujo completo desde use case hasta API"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_folio_master
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=67890)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 67890
        assert result.status == "closed"
        assert result.type == "master"
        assert result._embedded is not None
        assert result._embedded.company is not None
        assert result._embedded.master_folio_rule is not None

        # Verificar endpoint correcto
        call_args = mock_httpx_client.get.call_args
        assert call_args[0][0] == "https://api-test.trackhs.com/api/pms/folios/67890"

    @pytest.mark.asyncio
    async def test_get_folio_error_handling_401(self, api_client, mock_httpx_client):
        """Test manejo de error 401 en integración"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("Unauthorized")
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(params)

        assert "Unauthorized" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_error_handling_404(self, api_client, mock_httpx_client):
        """Test manejo de error 404 en integración"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not Found")
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=99999)

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(params)

        assert "Not Found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_timeout_handling(self, api_client, mock_httpx_client):
        """Test manejo de timeout en integración"""
        # Arrange
        import httpx

        mock_httpx_client.get.side_effect = httpx.TimeoutException("Request timeout")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(httpx.TimeoutException):
            await use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_folio_network_error(self, api_client, mock_httpx_client):
        """Test manejo de error de red en integración"""
        # Arrange
        import httpx

        mock_httpx_client.get.side_effect = httpx.ConnectError("Connection failed")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(httpx.ConnectError):
            await use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_folio_json_parsing(self, api_client, mock_httpx_client):
        """Test parsing de JSON en integración"""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 12345, "status": "open"}
        mock_httpx_client.get.return_value = mock_response

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"

    @pytest.mark.asyncio
    async def test_get_folio_with_different_folio_types(
        self, api_client, mock_httpx_client
    ):
        """Test con diferentes tipos de folio"""
        # Arrange
        guest_folio = {"id": 12345, "status": "open", "type": "guest"}
        master_folio = {"id": 67890, "status": "closed", "type": "master"}

        mock_response_guest = Mock()
        mock_response_guest.status_code = 200
        mock_response_guest.json.return_value = guest_folio

        mock_response_master = Mock()
        mock_response_master.status_code = 200
        mock_response_master.json.return_value = master_folio

        mock_httpx_client.get.side_effect = [mock_response_guest, mock_response_master]

        use_case = GetFolioUseCase(api_client)

        # Act - Test guest folio
        result_guest = await use_case.execute(GetFolioParams(folio_id=12345))

        # Act - Test master folio
        result_master = await use_case.execute(GetFolioParams(folio_id=67890))

        # Assert
        assert result_guest.type == "guest"
        assert result_guest.status == "open"
        assert result_master.type == "master"
        assert result_master.status == "closed"
