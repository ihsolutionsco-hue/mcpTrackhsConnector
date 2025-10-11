"""
Tests de integración para search_reservations
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.trackhs_mcp.tools.search_reservations import register_search_reservations, _is_valid_date_format
from src.trackhs_mcp.core.error_handling import ValidationError


class TestSearchReservationsIntegration:
    """Tests de integración para search_reservations"""
    
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
    def sample_search_response(self):
        """Respuesta de ejemplo de búsqueda"""
        return {
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "status": "Confirmed",
                        "arrivalDate": "2024-01-15",
                        "departureDate": "2024-01-20",
                        "nights": 5,
                        "currency": "USD",
                        "unitId": 1,
                        "contactId": 1
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {
                "self": {"href": "/v2/pms/reservations?page=1&size=10"},
                "first": {"href": "/v2/pms/reservations?page=1&size=10"},
                "last": {"href": "/v2/pms/reservations?page=1&size=10"}
            }
        }
    
    @pytest.mark.integration
    def test_register_search_reservations(self, mock_mcp, mock_api_client):
        """Test registro de la herramienta search_reservations"""
        register_search_reservations(mock_mcp, mock_api_client)
        
        # Verificar que se registró la herramienta
        mock_mcp.tool.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_basic_success(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda básica exitosa"""
        mock_api_client.get.return_value = sample_search_response
        
        # Registrar la herramienta
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        # Obtener la función registrada
        tool_func = mock_mcp.tool.call_args[0][0]
        
        # Ejecutar la función
        result = await tool_func(
            page=1,
            size=10,
            sort_column="name",
            sort_direction="asc"
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_with_filters(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda con filtros"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(
            page=1,
            size=10,
            search="test",
            node_id=1,
            unit_id=1,
            status="Confirmed"
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_with_date_filters(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda con filtros de fecha"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(
            page=1,
            size=10,
            arrival_start="2024-01-01T00:00:00Z",
            arrival_end="2024-01-31T23:59:59Z",
            departure_start="2024-02-01T00:00:00Z",
            departure_end="2024-02-28T23:59:59Z"
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_with_scroll(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda con scroll"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(
            page=1,
            size=10,
            scroll=1
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_with_multiple_ids(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda con múltiples IDs"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(
            page=1,
            size=10,
            node_id=[1, 2, 3],
            unit_id=[1, 2],
            contact_id=[1, 2, 3, 4]
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_validation_error_invalid_page(self, mock_mcp, mock_api_client):
        """Test error de validación con página inválida"""
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            await tool_func(page=0, size=10)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_validation_error_invalid_size(self, mock_mcp, mock_api_client):
        """Test error de validación con tamaño inválido"""
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        with pytest.raises(ValidationError, match="Size must be between 1 and 1000"):
            await tool_func(page=1, size=0)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_validation_error_size_too_large(self, mock_mcp, mock_api_client):
        """Test error de validación con tamaño demasiado grande"""
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        with pytest.raises(ValidationError, match="Size must be between 1 and 1000"):
            await tool_func(page=1, size=1001)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_validation_error_invalid_date(self, mock_mcp, mock_api_client):
        """Test error de validación con fecha inválida"""
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        with pytest.raises(ValidationError, match="Invalid date format"):
            await tool_func(
                page=1,
                size=10,
                arrival_start="invalid-date"
            )
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_api_error(self, mock_mcp, mock_api_client):
        """Test error de API"""
        mock_api_client.get.side_effect = Exception("API Error")
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        with pytest.raises(Exception, match="API Error"):
            await tool_func(page=1, size=10)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_all_parameters(self, mock_mcp, mock_api_client, sample_search_response):
        """Test búsqueda con todos los parámetros"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(
            page=2,
            size=20,
            sort_column="checkin",
            sort_direction="desc",
            search="test search",
            tags="tag1,tag2",
            node_id=[1, 2],
            unit_id=1,
            reservation_type_id=[1, 2, 3],
            contact_id=1,
            travel_agent_id=1,
            campaign_id=1,
            user_id=1,
            unit_type_id=1,
            rate_type_id=1,
            booked_start="2024-01-01T00:00:00Z",
            booked_end="2024-01-31T23:59:59Z",
            arrival_start="2024-02-01T00:00:00Z",
            arrival_end="2024-02-28T23:59:59Z",
            departure_start="2024-03-01T00:00:00Z",
            departure_end="2024-03-31T23:59:59Z",
            updated_since="2024-01-01T00:00:00Z",
            scroll="scroll123",
            in_house_today=1,
            status=["Confirmed", "Hold"],
            group_id=1,
            checkin_office_id=1
        )
        
        assert result == sample_search_response
        mock_api_client.get.assert_called_once()
    
    @pytest.mark.integration
    def test_is_valid_date_format_valid_dates(self):
        """Test validación de fechas válidas"""
        valid_dates = [
            "2024-01-01T00:00:00Z",
            "2024-01-01T00:00:00+00:00",
            "2024-01-01T00:00:00-05:00",
            "2024-01-01T12:30:45.123Z",
            "2024-12-31T23:59:59Z"
        ]
        
        for date_str in valid_dates:
            assert _is_valid_date_format(date_str), f"Date {date_str} should be valid"
    
    @pytest.mark.integration
    def test_is_valid_date_format_invalid_dates(self):
        """Test validación de fechas inválidas"""
        invalid_dates = [
            "invalid-date",
            "2024-13-01T00:00:00Z",  # Mes inválido
            "2024-01-32T00:00:00Z",   # Día inválido
            "2024-01-01T25:00:00Z",   # Hora inválida
            "2024-01-01T00:60:00Z",   # Minutos inválidos
            "2024-01-01T00:00:60Z",   # Segundos inválidos
            "not-a-date",
            "2024/01/01",             # Formato incorrecto
            "01-01-2024"              # Formato incorrecto
        ]
        
        for date_str in invalid_dates:
            assert not _is_valid_date_format(date_str), f"Date {date_str} should be invalid"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_endpoint_construction(self, mock_mcp, mock_api_client, sample_search_response):
        """Test construcción del endpoint con parámetros"""
        mock_api_client.get.return_value = sample_search_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        await tool_func(
            page=2,
            size=20,
            search="test",
            node_id=1,
            status="Confirmed"
        )
        
        # Verificar que se llamó con el endpoint correcto
        mock_api_client.get.assert_called_once()
        call_args = mock_api_client.get.call_args[0]
        endpoint = call_args[0]
        
        assert endpoint.startswith("/v2/pms/reservations")
        assert "page=2" in endpoint
        assert "size=20" in endpoint
        assert "search=test" in endpoint
        assert "nodeId=1" in endpoint
        assert "status=Confirmed" in endpoint
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_search_reservations_empty_response(self, mock_mcp, mock_api_client):
        """Test respuesta vacía"""
        empty_response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 10,
            "total_items": 0,
            "_links": {
                "self": {"href": "/v2/pms/reservations?page=1&size=10"},
                "first": {"href": "/v2/pms/reservations?page=1&size=10"},
                "last": {"href": "/v2/pms/reservations?page=1&size=10"}
            }
        }
        
        mock_api_client.get.return_value = empty_response
        
        mock_mcp.tool = Mock()
        register_search_reservations(mock_mcp, mock_api_client)
        
        tool_func = mock_mcp.tool.call_args[0][0]
        
        result = await tool_func(page=1, size=10)
        
        assert result == empty_response
        assert len(result["_embedded"]["reservations"]) == 0
        assert result["total_items"] == 0
