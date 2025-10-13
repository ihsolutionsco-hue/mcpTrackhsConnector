"""
Tests unitarios para GetFolioUseCase
"""

from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError as PydanticValidationError

from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase
from src.trackhs_mcp.domain.entities.folios import Folio, GetFolioParams
from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError


class TestGetFolioUseCase:
    """Tests para GetFolioUseCase"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def use_case(self, mock_api_client):
        """Instancia del use case"""
        return GetFolioUseCase(mock_api_client)

    @pytest.mark.asyncio
    async def test_get_folio_success(
        self, use_case, mock_api_client, sample_folio_guest
    ):
        """Test caso exitoso de obtención de folio"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_guest
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"
        assert result.type == "guest"
        mock_api_client.get.assert_called_once_with("/pms/folios/12345")

    @pytest.mark.asyncio
    async def test_get_folio_invalid_id(self, use_case):
        """Test con ID inválido"""
        # Arrange
        params = GetFolioParams(folio_id=0)

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "folio_id es requerido" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_negative_id(self, use_case):
        """Test con ID negativo"""
        # Arrange
        params = GetFolioParams(folio_id=-1)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "folio_id debe ser un número entero positivo válido" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_get_folio_empty_id(self, use_case):
        """Test con ID vacío"""
        # Arrange - Crear parámetros con string vacío que falle en Pydantic
        with pytest.raises(PydanticValidationError) as exc_info:
            GetFolioParams(folio_id="")

        # Verificar que Pydantic valida correctamente
        assert "unable to parse string as an integer" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_not_found(self, use_case, mock_api_client):
        """Test folio no encontrado (404)"""
        # Arrange
        error = Exception("Not Found")
        error.status_code = 404
        mock_api_client.get.side_effect = error
        params = GetFolioParams(folio_id=99999)

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Folio no encontrado" in str(exc_info.value)
        assert "99999" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_unauthorized(self, use_case, mock_api_client):
        """Test error de autorización (401)"""
        # Arrange
        error = Exception("Unauthorized")
        error.status_code = 401
        mock_api_client.get.side_effect = error
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "No autorizado" in str(exc_info.value)
        assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_forbidden(self, use_case, mock_api_client):
        """Test error de permisos (403)"""
        # Arrange
        error = Exception("Forbidden")
        error.status_code = 403
        mock_api_client.get.side_effect = error
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await use_case.execute(params)

        assert "Prohibido" in str(exc_info.value)
        assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_server_error(self, use_case, mock_api_client):
        """Test error del servidor (500)"""
        # Arrange
        error = Exception("Internal Server Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "Error interno del servidor" in str(exc_info.value)
        assert "temporalmente no disponible" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_json_string_response(
        self, use_case, mock_api_client, sample_folio_guest
    ):
        """Test respuesta como string JSON"""
        # Arrange
        import json

        json_string = json.dumps(sample_folio_guest)
        mock_api_client.get.return_value = json_string
        params = GetFolioParams(folio_id=12345)

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        assert result.status == "open"

    @pytest.mark.asyncio
    async def test_get_folio_with_embedded_data(
        self, use_case, mock_api_client, sample_folio_master
    ):
        """Test folio con datos embebidos completos"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_master
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

    @pytest.mark.asyncio
    async def test_get_folio_empty_response(self, use_case, mock_api_client):
        """Test respuesta vacía de la API"""
        # Arrange
        mock_api_client.get.return_value = None
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "No se encontraron datos para el folio ID 12345" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_invalid_json_response(self, use_case, mock_api_client):
        """Test respuesta JSON inválida"""
        # Arrange
        mock_api_client.get.return_value = "invalid json"
        params = GetFolioParams(folio_id=12345)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await use_case.execute(params)

        assert "Error al parsear respuesta JSON" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_string_id_conversion(
        self, use_case, mock_api_client, sample_folio_guest
    ):
        """Test conversión de ID string a entero"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_guest
        params = GetFolioParams(folio_id="12345")

        # Act
        result = await use_case.execute(params)

        # Assert
        assert isinstance(result, Folio)
        assert result.id == 12345
        mock_api_client.get.assert_called_once_with("/pms/folios/12345")
