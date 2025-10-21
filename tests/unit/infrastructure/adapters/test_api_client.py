"""
Tests unitarios para TrackHSApiClient
"""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from src.trackhs_mcp.domain.value_objects.request import RequestOptions
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from src.trackhs_mcp.infrastructure.utils.error_handling import (
    ApiError,
    AuthenticationError,
    NetworkError,
    TimeoutError,
)


class TestTrackHSApiClient:
    """Tests para TrackHSApiClient"""

    @pytest.fixture
    def api_client(self, mock_trackhs_config):
        """Crear instancia de API client para testing"""
        with patch(
            "src.trackhs_mcp.infrastructure.utils.auth.TrackHSAuth"
        ) as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {
                "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            return TrackHSApiClient(mock_trackhs_config)

    @pytest.mark.unit
    def test_init_success(self, mock_trackhs_config):
        """Test inicialización exitosa del cliente"""
        with patch(
            "src.trackhs_mcp.infrastructure.utils.auth.TrackHSAuth"
        ) as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            client = TrackHSApiClient(mock_trackhs_config)
            assert client.config == mock_trackhs_config
            assert client.auth is not None

    @pytest.mark.unit
    def test_init_invalid_credentials(self, mock_trackhs_config):
        """Test inicialización con credenciales inválidas"""
        with patch(
            "src.trackhs_mcp.infrastructure.adapters.trackhs_api_client.TrackHSAuth"
        ) as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = False
            with pytest.raises(
                ValueError,
                match="Credenciales de Track HS no configuradas correctamente",
            ):
                TrackHSApiClient(mock_trackhs_config)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_success(self, api_client):
        """Test petición exitosa"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"data": "test"}

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            result = await api_client.request("/test")
            assert result == {"data": "test"}
            mock_request.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_params(self, api_client):
        """Test petición con parámetros de consulta"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"data": "test"}

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            params = {"arrivalStart": "2025-01-01T00:00:00Z", "status": "Confirmed"}
            result = await api_client.request("/test", params=params)
            assert result == {"data": "test"}

            # Verificar que se llamó con los parámetros correctos
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"  # method
            assert call_args[0][1] == "/test"  # endpoint
            assert "params" in call_args[1]
            assert call_args[1]["params"] == params

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_authentication_error(self, api_client):
        """Test error de autenticación"""
        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 401
        mock_response.reason_phrase = "Unauthorized"

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(AuthenticationError, match="Invalid credentials"):
                await api_client.request("/test")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_forbidden_error(self, api_client):
        """Test error de acceso prohibido"""
        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 403
        mock_response.reason_phrase = "Forbidden"

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(AuthenticationError, match="Access forbidden"):
                await api_client.request("/test")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_not_found_error(self, api_client):
        """Test error de endpoint no encontrado"""
        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 404
        mock_response.reason_phrase = "Not Found"

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            with pytest.raises(ApiError, match="Endpoint not found"):
                await api_client.request("/test")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_server_error_with_retry(self, api_client):
        """Test error del servidor con reintentos"""
        mock_response = Mock()
        mock_response.is_success = False
        mock_response.status_code = 500
        mock_response.reason_phrase = "Internal Server Error"

        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(ApiError, match="Server error"):
                    await api_client.request("/test", max_retries=1)

                # Debe haber intentado 2 veces (1 + 1 retry)
                assert mock_request.call_count == 2
                assert mock_sleep.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_timeout_error(self, api_client):
        """Test error de timeout"""
        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Request timeout")

            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(TimeoutError, match="Request timeout"):
                    await api_client.request("/test", max_retries=1)

                # Debe haber intentado 2 veces
                assert mock_request.call_count == 2
                assert mock_sleep.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_connection_error(self, api_client):
        """Test error de conexión"""
        with patch.object(
            api_client.client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")

            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(NetworkError, match="Connection error"):
                    await api_client.request("/test", max_retries=1)

                # Debe haber intentado 2 veces
                assert mock_request.call_count == 2
                assert mock_sleep.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_method(self, api_client):
        """Test método GET"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"data": "test"}

        with patch.object(
            api_client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {"data": "test"}

            result = await api_client.get("/test")
            assert result == {"data": "test"}
            expected_options = RequestOptions(method="GET")
            mock_request.assert_called_once_with("/test", expected_options, params=None)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_method_with_params(self, api_client):
        """Test método GET con parámetros"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"data": "test"}

        with patch.object(
            api_client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {"data": "test"}

            params = {"arrivalStart": "2025-01-01T00:00:00Z", "status": "Confirmed"}
            result = await api_client.get("/test", params=params)
            assert result == {"data": "test"}
            # Verificar que se llamó con los argumentos correctos
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "/test"  # endpoint
            assert call_args[1]["params"] == params  # params

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_post_method(self, api_client):
        """Test método POST"""
        data = {"key": "value"}

        with patch.object(
            api_client, "request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {"data": "test"}

            result = await api_client.post("/test", data=data)
            assert result == {"data": "test"}
            # Verificar que se llamó con los argumentos correctos
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "/test"  # endpoint
            # Verificar que options tiene el body correcto
            options = call_args[0][1]
            assert options.method == "POST"
            assert options.body == '{"key": "value"}'

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_close(self, api_client):
        """Test cierre del cliente"""
        with patch.object(
            api_client.client, "aclose", new_callable=AsyncMock
        ) as mock_close:
            await api_client.close()
            mock_close.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_trackhs_config):
        """Test uso como context manager"""
        with patch(
            "src.trackhs_mcp.infrastructure.utils.auth.TrackHSAuth"
        ) as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {}

            with patch.object(
                TrackHSApiClient, "close", new_callable=AsyncMock
            ) as mock_close:
                async with TrackHSApiClient(mock_trackhs_config) as client:
                    assert client is not None

                mock_close.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_custom_headers(self, api_client):
        """Test request con headers personalizados"""
        # Arrange
        custom_headers = {"X-Custom-Header": "test-value"}
        options = RequestOptions(headers=custom_headers)

        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/json"}
            mock_response.json.return_value = {"data": "test"}
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test", options=options)

            # Assert
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert "headers" in call_args[1]
            headers = call_args[1]["headers"]
            assert "X-Custom-Header" in headers
            assert headers["X-Custom-Header"] == "test-value"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_body(self, api_client):
        """Test request con body"""
        # Arrange
        body_data = '{"key": "value"}'
        options = RequestOptions(method="POST", body=body_data)

        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/json"}
            mock_response.json.return_value = {"data": "test"}
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test", options=options)

            # Assert
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert "data" in call_args[1]
            assert call_args[1]["data"] == body_data

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_400_bad_request(self, api_client):
        """Test manejo de error 400 Bad Request"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 400
            mock_response.text = "Bad Request Error"
            mock_response.headers = {"content-type": "text/plain"}
            mock_request.return_value = mock_response

            # Act & Assert
            with pytest.raises(ApiError) as exc_info:
                await api_client.request("/test")

            assert "Bad Request" in str(exc_info.value)
            assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_400_with_json_error(self, api_client):
        """Test manejo de error 400 con JSON de error"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 400
            mock_response.text = '{"error": "validation failed"}'
            mock_response.headers = {"content-type": "application/json"}
            mock_response.json.return_value = {"error": "validation failed"}
            mock_request.return_value = mock_response

            # Act & Assert
            with pytest.raises(ApiError) as exc_info:
                await api_client.request("/test")

            assert "Bad Request" in str(exc_info.value)
            assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_400_with_invalid_json(self, api_client):
        """Test manejo de error 400 con JSON inválido"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 400
            mock_response.text = "Invalid JSON response"
            mock_response.headers = {"content-type": "text/plain"}
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_request.return_value = mock_response

            # Act & Assert
            with pytest.raises(ApiError) as exc_info:
                await api_client.request("/test")

            assert "Bad Request" in str(exc_info.value)
            assert exc_info.value.status_code == 400

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_retry_on_server_error(self, api_client):
        """Test reintentos en errores del servidor"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            # Primera llamada falla con 500, segunda es exitosa
            mock_response_500 = MagicMock()
            mock_response_500.is_success = False
            mock_response_500.status_code = 500
            mock_response_500.reason_phrase = "Internal Server Error"

            mock_response_200 = MagicMock()
            mock_response_200.is_success = True
            mock_response_200.status_code = 200
            mock_response_200.headers = {"content-type": "application/json"}
            mock_response_200.json.return_value = {"data": "success"}

            # Configurar side_effect para devolver las respuestas directamente
            mock_request.side_effect = [mock_response_500, mock_response_200]

            # Act
            result = await api_client.request("/test")

            # Assert
            assert result == {"data": "success"}
            assert mock_request.call_count == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_max_retries_exceeded(self, api_client):
        """Test cuando se exceden los reintentos máximos"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 500
            mock_response.reason_phrase = "Internal Server Error"
            mock_request.return_value = mock_response

            # Act & Assert
            with pytest.raises(ApiError) as exc_info:
                await api_client.request("/test", max_retries=2)

            assert "Server error" in str(exc_info.value)
            assert exc_info.value.status_code == 500

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_text_response(self, api_client):
        """Test manejo de respuesta de texto"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "text/plain"}
            mock_response.text = "Plain text response"
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test")

            # Assert
            assert result == "Plain text response"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_xml_response(self, api_client):
        """Test manejo de respuesta XML"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/xml"}
            mock_response.text = "<xml>data</xml>"
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test")

            # Assert
            assert result == "<xml>data</xml>"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_unknown_content_type(self, api_client):
        """Test manejo de tipo de contenido desconocido"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/octet-stream"}
            mock_response.text = "Binary data"
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test")

            # Assert
            assert result == "Binary data"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_awaitable_response(self, api_client):
        """Test manejo de respuesta que es awaitable"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            # Crear un mock que simula una respuesta awaitable
            mock_response = MagicMock()
            mock_response.is_success = True
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/json"}
            mock_response.json.return_value = {"data": "test"}

            # Simular que la respuesta es awaitable
            mock_request.return_value = mock_response

            # Act
            result = await api_client.request("/test")

            # Assert
            assert result == {"data": "test"}

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_debug_logging(self, api_client):
        """Test logging de debug cuando DEBUG=true"""
        # Arrange
        import os

        with patch.dict(os.environ, {"DEBUG": "true"}):
            with patch.object(api_client.client, "request") as mock_request:
                with patch("logging.getLogger") as mock_logger:
                    mock_response = MagicMock()
                    mock_response.is_success = True
                    mock_response.status_code = 200
                    mock_response.headers = {"content-type": "application/json"}
                    mock_response.json.return_value = {"data": "test"}
                    mock_request.return_value = mock_response

                    # Act
                    result = await api_client.request("/test", params={"key": "value"})

                    # Assert
                    assert result == {"data": "test"}
                    # Verificar que se llamó al logger de debug
                    mock_logger.assert_called()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_with_other_status_codes(self, api_client):
        """Test manejo de otros códigos de estado"""
        # Arrange
        with patch.object(api_client.client, "request") as mock_request:
            mock_response = AsyncMock()
            mock_response.is_success = False
            mock_response.status_code = 418  # I'm a teapot
            mock_response.reason_phrase = "I'm a teapot"
            mock_request.return_value = mock_response

            # Act & Assert
            with pytest.raises(ApiError) as exc_info:
                await api_client.request("/test")

            assert "API Error" in str(exc_info.value)
            assert exc_info.value.status_code == 418
