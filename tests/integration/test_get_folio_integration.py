"""
Tests de integración para get_folio
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase
from src.trackhs_mcp.domain.entities.folios import Folio, GetFolioParams
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class TestGetFolioIntegration:
    """Tests de integración para get_folio"""

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

    @pytest.mark.asyncio
    async def test_get_folio_api_integration(self, api_client, sample_folio_guest):
        """Test integración con API real (mock)"""
        # Arrange
        api_client.get.return_value = sample_folio_guest

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"
        assert result.type == "guest"
        api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_with_auth(self, api_client, sample_folio_guest):
        """Test con autenticación"""
        # Arrange
        api_client.get.return_value = sample_folio_guest

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345

        # Verificar que se llamó el método get
        api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_complete_flow(self, api_client, sample_folio_master):
        """Test flujo completo desde use case hasta API"""
        # Arrange
        api_client.get.return_value = sample_folio_master

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=67890)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 67890
        assert result.status == "closed"
        assert result.type == "master"
        assert result.embedded is not None
        assert result.embedded.company is not None
        assert result.embedded.master_folio_rule is not None

        # Verificar que se llamó el método get
        api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_error_handling_401(self, api_client):
        """Test manejo de error 401 en integración"""

        # Arrange
        class UnauthorizedError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 401

        api_client.get.side_effect = UnauthorizedError("Unauthorized")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "No autorizado" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_error_handling_404(self, api_client):
        """Test manejo de error 404 en integración"""

        # Arrange
        class NotFoundError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.status_code = 404

        api_client.get.side_effect = NotFoundError("Not Found")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=99999)

        # Act & Assert
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Folio no encontrado" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_timeout_handling(self, api_client):
        """Test manejo de timeout en integración"""
        # Arrange
        import httpx

        api_client.get.side_effect = httpx.TimeoutException("Request timeout")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Request timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_network_error(self, api_client):
        """Test manejo de error de red en integración"""
        # Arrange
        import httpx

        api_client.get.side_effect = httpx.ConnectError("Connection failed")

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        from src.trackhs_mcp.infrastructure.utils.error_handling import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Connection failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_json_parsing(self, api_client):
        """Test parsing de JSON en integración"""
        # Arrange
        api_client.get.return_value = {"id": 12345, "status": "open"}

        use_case = GetFolioUseCase(api_client)
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"

    @pytest.mark.asyncio
    async def test_get_folio_with_different_folio_types(self, api_client):
        """Test con diferentes tipos de folio"""
        # Arrange
        guest_folio = {"id": 12345, "status": "open", "type": "guest"}
        master_folio = {"id": 67890, "status": "closed", "type": "master"}

        api_client.get.side_effect = [guest_folio, master_folio]

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
