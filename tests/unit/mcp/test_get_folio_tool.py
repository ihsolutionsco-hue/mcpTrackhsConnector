"""
Tests unitarios para la herramienta MCP get_folio
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio


class TestGetFolioTool:
    """Tests para la herramienta MCP get_folio"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def tool_function(self, mock_mcp, mock_api_client):
        """Función de la herramienta registrada"""
        register_get_folio(mock_mcp, mock_api_client)
        return mock_mcp.tool.call_args[0][0]  # Obtener la función decorada

    @pytest.mark.asyncio
    async def test_get_folio_tool_success(
        self, tool_function, mock_api_client, sample_folio_guest
    ):
        """Test tool funciona correctamente"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_guest

        # Act
        result = await tool_function(folio_id="12345")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 12345
        assert result["status"] == "open"
        assert result["type"] == "guest"
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_tool_validation_empty_id(self, tool_function):
        """Test validación de parámetros - ID vacío"""
        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await tool_function(folio_id="")

        assert "Parámetro 'folio_id' es requerido" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_validation_none_id(self, tool_function):
        """Test validación de parámetros - ID None"""
        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await tool_function(folio_id=None)

        assert "Parámetro 'folio_id' es requerido" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_validation_negative_id(self, tool_function):
        """Test validación de parámetros - ID negativo"""
        # Act & Assert
        from src.trackhs_mcp.domain.exceptions.api_exceptions import TrackHSError

        with pytest.raises(TrackHSError) as exc_info:
            await tool_function(folio_id="-1")

        assert "Valor inválido para 'folio_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_validation_zero_id(self, tool_function):
        """Test validación de parámetros - ID cero"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="0")

        assert "Valor inválido para 'folio_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_validation_invalid_id(self, tool_function):
        """Test validación de parámetros - ID inválido"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="abc")

        assert "Valor inválido para 'folio_id'" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_error_handling_401(
        self, tool_function, mock_api_client
    ):
        """Test manejo de errores - 401 Unauthorized"""
        # Arrange
        error = Exception("Unauthorized")
        error.status_code = 401
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "No autorizado" in str(exc_info.value)
        assert "Credenciales de autenticación inválidas" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_error_handling_403(
        self, tool_function, mock_api_client
    ):
        """Test manejo de errores - 403 Forbidden"""
        # Arrange
        error = Exception("Forbidden")
        error.status_code = 403
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Prohibido" in str(exc_info.value)
        assert "Permisos insuficientes" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_error_handling_404(
        self, tool_function, mock_api_client
    ):
        """Test manejo de errores - 404 Not Found"""
        # Arrange
        error = Exception("Not Found")
        error.status_code = 404
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="99999")

        assert "Folio no encontrado" in str(exc_info.value)
        assert "99999" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_error_handling_500(
        self, tool_function, mock_api_client
    ):
        """Test manejo de errores - 500 Internal Server Error"""
        # Arrange
        error = Exception("Internal Server Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error interno del servidor" in str(exc_info.value)
        assert "temporalmente no disponible" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_folio_tool_response_format(
        self, tool_function, mock_api_client, sample_folio_guest
    ):
        """Test formato de respuesta"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_guest

        # Act
        result = await tool_function(folio_id="12345")

        # Assert
        assert isinstance(result, dict)
        assert "id" in result
        assert "status" in result
        assert "type" in result
        assert "currentBalance" in result
        assert "realizedBalance" in result
        assert "_embedded" in result
        assert "_links" in result

    @pytest.mark.asyncio
    async def test_get_folio_tool_with_master_folio(
        self, tool_function, mock_api_client, sample_folio_master
    ):
        """Test con folio maestro"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_master

        # Act
        result = await tool_function(folio_id="67890")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 67890
        assert result["status"] == "closed"
        assert result["type"] == "master"
        assert result["hasException"] is True
        assert "masterFolioRule" in result["_embedded"]

    @pytest.mark.asyncio
    async def test_get_folio_tool_with_minimal_folio(
        self, tool_function, mock_api_client, sample_folio_minimal
    ):
        """Test con folio mínimo"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_minimal

        # Act
        result = await tool_function(folio_id="11111")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 11111
        assert result["status"] == "open"
        # Campos opcionales pueden estar ausentes
        assert "type" not in result or result["type"] is None

    @pytest.mark.asyncio
    async def test_get_folio_tool_string_id_conversion(
        self, tool_function, mock_api_client, sample_folio_guest
    ):
        """Test conversión de ID string"""
        # Arrange
        mock_api_client.get.return_value = sample_folio_guest

        # Act
        result = await tool_function(folio_id="12345")

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 12345

    @pytest.mark.asyncio
    async def test_get_folio_tool_generic_error(self, tool_function, mock_api_client):
        """Test error genérico sin status_code"""
        # Arrange
        error = Exception("Generic error")
        mock_api_client.get.side_effect = error

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            await tool_function(folio_id="12345")

        assert "Error al obtener el folio" in str(exc_info.value)
        assert "Generic error" in str(exc_info.value)
