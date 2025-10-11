"""
Tests unitarios para TrackHSApiClient
"""

import pytest
import httpx
from unittest.mock import Mock, AsyncMock, patch
from src.trackhs_mcp.core.api_client import TrackHSApiClient
from src.trackhs_mcp.core.types import TrackHSConfig, RequestOptions
from src.trackhs_mcp.core.error_handling import ApiError, AuthenticationError, NetworkError, TimeoutError


class TestTrackHSApiClient:
    """Tests para TrackHSApiClient"""
    
    @pytest.fixture
    def api_client(self, mock_trackhs_config):
        """Crear instancia de API client para testing"""
        with patch('src.trackhs_mcp.core.api_client.TrackHSAuth') as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {
                "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            return TrackHSApiClient(mock_trackhs_config)
    
    @pytest.mark.unit
    def test_init_success(self, mock_trackhs_config):
        """Test inicialización exitosa del cliente"""
        with patch('src.trackhs_mcp.core.api_client.TrackHSAuth') as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            client = TrackHSApiClient(mock_trackhs_config)
            assert client.config == mock_trackhs_config
            assert client.auth is not None
    
    @pytest.mark.unit
    def test_init_invalid_credentials(self, mock_trackhs_config):
        """Test inicialización con credenciales inválidas"""
        with patch('src.trackhs_mcp.core.api_client.TrackHSAuth') as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = False
            with pytest.raises(ValueError, match="Credenciales de Track HS no configuradas correctamente"):
                TrackHSApiClient(mock_trackhs_config)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_success(self, api_client):
        """Test petición exitosa"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
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
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
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
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
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
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
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
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
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
        
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(ApiError, match="Server error"):
                    await api_client.request("/test", max_retries=1)
                
                # Debe haber intentado 2 veces (1 + 1 retry)
                assert mock_request.call_count == 2
                assert mock_sleep.call_count == 1
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_timeout_error(self, api_client):
        """Test error de timeout"""
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Request timeout")
            
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                with pytest.raises(TimeoutError, match="Request timeout"):
                    await api_client.request("/test", max_retries=1)
                
                # Debe haber intentado 2 veces
                assert mock_request.call_count == 2
                assert mock_sleep.call_count == 1
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_connection_error(self, api_client):
        """Test error de conexión"""
        with patch.object(api_client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")
            
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
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
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        
        with patch.object(api_client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": "test"}
            
            result = await api_client.get("/test")
            assert result == {"data": "test"}
            mock_request.assert_called_once_with("/test", None, params=None)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_method_with_params(self, api_client):
        """Test método GET con parámetros"""
        mock_response = Mock()
        mock_response.is_success = True
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"data": "test"}
        
        with patch.object(api_client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": "test"}
            
            params = {"arrivalStart": "2025-01-01T00:00:00Z", "status": "Confirmed"}
            result = await api_client.get("/test", params=params)
            assert result == {"data": "test"}
            mock_request.assert_called_once_with("/test", None, params=params)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_post_method(self, api_client):
        """Test método POST"""
        options = RequestOptions(method="POST", body={"key": "value"})
        
        with patch.object(api_client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": "test"}
            
            result = await api_client.post("/test", options)
            assert result == {"data": "test"}
            mock_request.assert_called_once_with("/test", options)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_close(self, api_client):
        """Test cierre del cliente"""
        with patch.object(api_client.client, 'aclose', new_callable=AsyncMock) as mock_close:
            await api_client.close()
            mock_close.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_trackhs_config):
        """Test uso como context manager"""
        with patch('src.trackhs_mcp.core.api_client.TrackHSAuth') as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {}
            
            with patch.object(TrackHSApiClient, 'close', new_callable=AsyncMock) as mock_close:
                async with TrackHSApiClient(mock_trackhs_config) as client:
                    assert client is not None
                
                mock_close.assert_called_once()
