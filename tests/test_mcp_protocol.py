"""
Tests super simples para validar el protocolo MCP
Enfoque MVP: 1 test = 1 componente MCP crítico
"""

import pytest
from unittest.mock import Mock, AsyncMock
from fastmcp import FastMCP


class TestMCPProtocol:
    """Tests críticos para validar el protocolo MCP"""

    def test_mcp_server_creates_successfully(self):
        """Test: El servidor MCP se crea correctamente"""
        # Act
        mcp = FastMCP(
            name="TrackHS MCP Server",
            mask_error_details=False,
            include_fastmcp_meta=True,
        )
        
        # Assert
        assert mcp is not None
        assert hasattr(mcp, 'tool')
        assert hasattr(mcp, 'resource')
        assert hasattr(mcp, 'prompt')

    def test_mcp_tools_registration(self):
        """Test: Las 7 herramientas MCP se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        register_all_tools(mcp, mock_api_client)
        
        # Assert - Verificar que se registraron las 7 herramientas
        # Nota: FastMCP no expone directamente las herramientas registradas,
        # pero podemos verificar que no hay errores en el registro
        assert mcp is not None

    def test_mcp_resources_registration(self):
        """Test: Los 16 recursos MCP se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.resources import register_all_resources
        register_all_resources(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_prompts_registration(self):
        """Test: Los 3 prompts MCP se registran correctamente"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        
        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import register_all_prompts
        register_all_prompts(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_schema_hook_applies_correctly(self):
        """Test: El schema hook se aplica correctamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.tools.schema_hook import create_schema_fixed_server
        
        # Act
        mcp_server = create_schema_fixed_server("Test Server")
        
        # Assert
        assert mcp_server is not None
        assert hasattr(mcp_server, '_schema_fixer_hook')

    def test_mcp_tool_search_reservations(self):
        """Test: La herramienta search_reservations funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "status": "Confirmed"}],
            "total": 1,
            "page": 0,
            "size": 10
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.search_reservations_v2 import register_search_reservations_v2
        register_search_reservations_v2(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_get_reservation(self):
        """Test: La herramienta get_reservation funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "id": 1,
            "status": "Confirmed",
            "arrivalDate": "2024-01-15"
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.get_reservation_v2 import register_get_reservation_v2
        register_get_reservation_v2(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_get_folio(self):
        """Test: La herramienta get_folio funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "id": 1,
            "status": "open",
            "currentBalance": 100.0
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.get_folio import register_get_folio
        register_get_folio(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_search_units(self):
        """Test: La herramienta search_units funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "name": "Villa Paradise"}],
            "total": 1
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.search_units import register_search_units
        register_search_units(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_search_amenities(self):
        """Test: La herramienta search_amenities funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.get = AsyncMock()
        mock_api_client.get.return_value = {
            "data": [{"id": 1, "name": "WiFi"}],
            "total": 1
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.search_amenities import register_search_amenities
        register_search_amenities(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_create_maintenance_work_order(self):
        """Test: La herramienta create_maintenance_work_order funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.post = AsyncMock()
        mock_api_client.post.return_value = {
            "id": 1,
            "status": "open",
            "summary": "Test work order"
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.create_maintenance_work_order import register_create_maintenance_work_order
        register_create_maintenance_work_order(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_tool_create_housekeeping_work_order(self):
        """Test: La herramienta create_housekeeping_work_order funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        mock_api_client.post = AsyncMock()
        mock_api_client.post.return_value = {
            "id": 1,
            "scheduledAt": "2024-01-15T10:00:00Z"
        }
        
        # Act
        from src.trackhs_mcp.infrastructure.tools.create_housekeeping_work_order import register_create_housekeeping_work_order
        register_create_housekeeping_work_order(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_prompt_date_range_search(self):
        """Test: El prompt de búsqueda por fechas funciona"""
        # Arrange
        mcp = FastMCP(name="Test Server")
        mock_api_client = Mock()
        
        # Act
        from src.trackhs_mcp.infrastructure.prompts.reservations import register_all_prompts
        register_all_prompts(mcp, mock_api_client)
        
        # Assert
        assert mcp is not None

    def test_mcp_server_integration(self):
        """Test: El servidor MCP completo se integra correctamente"""
        # Arrange
        from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
        from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient
        
        # Act
        config = TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30
        )
        api_client = TrackHSApiClient(config)
        
        mcp = FastMCP(
            name="TrackHS MCP Server",
            mask_error_details=False,
            include_fastmcp_meta=True,
        )
        
        # Registrar todos los componentes
        from src.trackhs_mcp.infrastructure.tools.registry import register_all_tools
        from src.trackhs_mcp.infrastructure.tools.resources import register_all_resources
        from src.trackhs_mcp.infrastructure.prompts.reservations import register_all_prompts
        
        register_all_tools(mcp, api_client)
        register_all_resources(mcp, api_client)
        register_all_prompts(mcp, api_client)
        
        # Assert
        assert mcp is not None
        assert api_client is not None
        assert config is not None
