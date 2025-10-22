"""
Tests críticos para la herramienta MCP get_folio
"""

from unittest.mock import Mock

import pytest


class TestGetFolioCritical:
    """Tests críticos para funcionalidad esencial de get_folio"""

    def test_get_folio_tool_imports(self):
        """Test: La herramienta get_folio se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        assert register_get_folio is not None

    def test_get_folio_tool_registration(self):
        """Test: La herramienta se puede registrar"""
        # Arrange
        mock_mcp = Mock()
        mock_mcp.tool = Mock()
        mock_api_client = Mock()

        # Act
        from src.trackhs_mcp.infrastructure.mcp.get_folio import register_get_folio

        register_get_folio(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_get_folio_use_case_imports(self):
        """Test: Caso de uso se puede importar"""
        # Act & Assert
        from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase

        assert GetFolioUseCase is not None

    def test_get_folio_entity_imports(self):
        """Test: Entidades se pueden importar"""
        # Act & Assert
        from src.trackhs_mcp.domain.entities.folios import Folio

        assert Folio is not None

    def test_get_folio_validation(self):
        """Test: Validación de ID funciona"""
        # Arrange
        from src.trackhs_mcp.domain.entities.folios import GetFolioParams

        # Act & Assert
        # ID válido
        valid_params = GetFolioParams(folio_id=12345)
        assert valid_params.folio_id == 12345

    def test_get_folio_invalid_id(self):
        """Test: ID inválido es rechazado"""
        # Arrange
        from src.trackhs_mcp.domain.entities.folios import GetFolioParams

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic validation error
            GetFolioParams(folio_id="invalid-id")
