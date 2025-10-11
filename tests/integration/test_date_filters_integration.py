"""
Tests de integración para validar que los filtros de fecha funcionan end-to-end
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.trackhs_mcp.core.api_client import TrackHSApiClient
from src.trackhs_mcp.core.types import TrackHSConfig
from src.trackhs_mcp.tools.search_reservations import register_search_reservations


class TestDateFiltersIntegration:
    """Tests de integración para filtros de fecha"""
    
    @pytest.fixture
    def mock_config(self):
        """Configuración mock para tests"""
        return TrackHSConfig(
            base_url="https://ihmvacations.trackhs.com/api",
            username="test_user",
            password="test_pass"
        )
    
    @pytest.fixture
    def mock_api_client(self, mock_config):
        """Cliente API mock para tests"""
        with patch('src.trackhs_mcp.core.api_client.TrackHSAuth') as mock_auth:
            mock_auth.return_value.validate_credentials.return_value = True
            mock_auth.return_value.get_headers.return_value = {"Authorization": "Bearer token"}
            
            client = TrackHSApiClient(mock_config)
            client.client = AsyncMock()
            return client
    
    @pytest.mark.asyncio
    async def test_search_reservations_with_date_filters_params_transformation(self, mock_mcp, mock_api_client):
        """Test que valida que los parámetros de fecha se transforman correctamente"""
        
        # Mock de la respuesta del API
        mock_response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 5,
            "total_items": 0,
            "_links": {"self": {"href": "https://ihmvacations.trackhs.com/api/v2/pms/reservations/?page=1&size=5&sortColumn=name&sortDirection=asc&status=Confirmed&arrivalStart=2025-01-01T00:00:00Z&arrivalEnd=2025-01-31T23:59:59Z"}}
        }
        
        mock_api_client.client.request.return_value = AsyncMock()
        mock_api_client.client.request.return_value.is_success = True
        mock_api_client.client.request.return_value.json.return_value = mock_response
        mock_api_client.client.request.return_value.headers = {"content-type": "application/json"}
        
        # Capturar los parámetros pasados al request
        captured_params = {}
        
        async def capture_request(method, endpoint, **kwargs):
            if 'params' in kwargs:
                captured_params.update(kwargs['params'])
            return mock_api_client.client.request.return_value
        
        mock_api_client.client.request.side_effect = capture_request
        
        # Crear mock del servidor MCP
        mock_mcp = MagicMock()
        
        # Registrar la herramienta
        register_search_reservations(mock_mcp, mock_api_client)
        
        # Obtener la función registrada
        search_func = mock_mcp.tool.call_args[0][0]
        
        # Ejecutar búsqueda con filtros de fecha
        result = await search_func(
            arrival_start="2025-01-01",
            arrival_end="2025-01-31T23:59:59Z",
            status="Confirmed",
            size=5
        )
        
        # Validar que los parámetros se transformaron correctamente
        assert "arrivalStart" in captured_params
        assert "arrivalEnd" in captured_params
        assert captured_params["arrivalStart"] == "2025-01-01T00:00:00Z"
        assert captured_params["arrivalEnd"] == "2025-01-31T23:59:59Z"
        assert captured_params["status"] == "Confirmed"
        assert captured_params["size"] == 5
        
        # Validar que se llamó al endpoint correcto
        mock_api_client.client.request.assert_called_once()
        call_args = mock_api_client.client.request.call_args
        assert call_args[0][0] == "GET"  # method
        assert call_args[0][1] == "/v2/pms/reservations"  # endpoint
    
    @pytest.mark.asyncio
    async def test_date_normalization_formats(self, mock_mcp, mock_api_client):
        """Test que valida la normalización de diferentes formatos de fecha"""
        
        test_cases = [
            ("2025-01-01", "2025-01-01T00:00:00Z"),
            ("2025-01-31T23:59:59", "2025-01-31T23:59:59Z"),
            ("2025-01-31T23:59:59Z", "2025-01-31T23:59:59Z"),
        ]
        
        for input_date, expected_output in test_cases:
            # Resetear mock
            mock_api_client.client.request.reset_mock()
            
            # Mock de respuesta
            mock_response = {
                "_embedded": {"reservations": []},
                "page": 1,
                "page_count": 0,
                "page_size": 5,
                "total_items": 0,
                "_links": {"self": {"href": "test"}}
            }
            
            mock_api_client.client.request.return_value = AsyncMock()
            mock_api_client.client.request.return_value.is_success = True
            mock_api_client.client.request.return_value.json.return_value = mock_response
            mock_api_client.client.request.return_value.headers = {"content-type": "application/json"}
            
            # Capturar parámetros
            captured_params = {}
            
            async def capture_request(method, endpoint, **kwargs):
                if 'params' in kwargs:
                    captured_params.update(kwargs['params'])
                return mock_api_client.client.request.return_value
            
            mock_api_client.client.request.side_effect = capture_request
            
            # Crear mock del servidor MCP
            mock_mcp = MagicMock()
            register_search_reservations(mock_mcp, mock_api_client)
            search_func = mock_mcp.tool.call_args[0][0]
            
            # Ejecutar búsqueda
            await search_func(
                arrival_start=input_date,
                status="Confirmed"
            )
            
            # Validar normalización
            assert captured_params["arrivalStart"] == expected_output, f"Failed for input: {input_date}"
    
    @pytest.mark.asyncio
    async def test_all_date_parameters_included(self, mock_mcp, mock_api_client):
        """Test que valida que todos los parámetros de fecha se incluyen correctamente"""
        
        # Mock de respuesta
        mock_response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 5,
            "total_items": 0,
            "_links": {"self": {"href": "test"}}
        }
        
        mock_api_client.client.request.return_value = AsyncMock()
        mock_api_client.client.request.return_value.is_success = True
        mock_api_client.client.request.return_value.json.return_value = mock_response
        mock_api_client.client.request.return_value.headers = {"content-type": "application/json"}
        
        # Capturar parámetros
        captured_params = {}
        
        async def capture_request(method, endpoint, **kwargs):
            if 'params' in kwargs:
                captured_params.update(kwargs['params'])
            return mock_api_client.client.request.return_value
        
        mock_api_client.client.request.side_effect = capture_request
        
        # Crear mock del servidor MCP
        mock_mcp = MagicMock()
        register_search_reservations(mock_mcp, mock_api_client)
        search_func = mock_mcp.tool.call_args[0][0]
        
        # Ejecutar búsqueda con todos los parámetros de fecha
        await search_func(
            arrival_start="2025-01-01",
            arrival_end="2025-01-31",
            departure_start="2025-02-01",
            departure_end="2025-02-28",
            booked_start="2024-12-01",
            booked_end="2024-12-31",
            updated_since="2024-12-01T00:00:00Z",
            status="Confirmed"
        )
        
        # Validar que todos los parámetros de fecha están presentes
        expected_date_params = {
            "arrivalStart": "2025-01-01T00:00:00Z",
            "arrivalEnd": "2025-01-31T00:00:00Z",
            "departureStart": "2025-02-01T00:00:00Z",
            "departureEnd": "2025-02-28T00:00:00Z",
            "bookedStart": "2024-12-01T00:00:00Z",
            "bookedEnd": "2024-12-31T00:00:00Z",
            "updatedSince": "2024-12-01T00:00:00Z"
        }
        
        for param_name, expected_value in expected_date_params.items():
            assert param_name in captured_params, f"Missing parameter: {param_name}"
            assert captured_params[param_name] == expected_value, f"Wrong value for {param_name}: {captured_params[param_name]} != {expected_value}"
    
    @pytest.mark.asyncio
    async def test_url_construction_with_date_filters(self, mock_mcp, mock_api_client):
        """Test que valida que el URL se construye correctamente con filtros de fecha"""
        
        # Mock de respuesta
        mock_response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 5,
            "total_items": 0,
            "_links": {"self": {"href": "test"}}
        }
        
        mock_api_client.client.request.return_value = AsyncMock()
        mock_api_client.client.request.return_value.is_success = True
        mock_api_client.client.request.return_value.json.return_value = mock_response
        mock_api_client.client.request.return_value.headers = {"content-type": "application/json"}
        
        # Crear mock del servidor MCP
        mock_mcp = MagicMock()
        register_search_reservations(mock_mcp, mock_api_client)
        search_func = mock_mcp.tool.call_args[0][0]
        
        # Ejecutar búsqueda
        await search_func(
            arrival_start="2025-01-01",
            arrival_end="2025-01-31T23:59:59Z",
            status="Confirmed",
            size=5
        )
        
        # Validar que se llamó con el endpoint correcto
        mock_api_client.client.request.assert_called_once()
        call_args = mock_api_client.client.request.call_args
        
        # Verificar método y endpoint
        assert call_args[0][0] == "GET"
        assert call_args[0][1] == "/v2/pms/reservations"
        
        # Verificar que params está en kwargs
        assert "params" in call_args[1]
        params = call_args[1]["params"]
        
        # Verificar parámetros específicos
        assert params["arrivalStart"] == "2025-01-01T00:00:00Z"
        assert params["arrivalEnd"] == "2025-01-31T23:59:59Z"
        assert params["status"] == "Confirmed"
        assert params["size"] == 5


if __name__ == "__main__":
    pytest.main([__file__])
