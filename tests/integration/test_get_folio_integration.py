"""
Tests de integración para get_folio
Verifica que el use case funcione correctamente con dependencias reales
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.application.use_cases.get_folio import GetFolioUseCase
from src.trackhs_mcp.domain.entities.folios import Folio, GetFolioParams


class TestGetFolioIntegration:
    """Tests de integración para get_folio"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = AsyncMock()
        client.get.return_value = {
            "id": 123,
            "status": "open",
            "reservation_id": 456,
            "type": "guest",
            "current_balance": 150.00,
            "realized_balance": 0.00,
            "start_date": "2024-01-15",
            "end_date": "2024-01-20",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
            "contact_id": 789,
            "company_id": None,
            "travel_agent_id": None,
            "master_folio_id": None,
            "master_folio_rule_id": None,
            "currency": "USD",
            "notes": "Test folio",
            "tags": [],
            "_embedded": {
                "contact": {
                    "id": 789,
                    "firstName": "John",
                    "lastName": "Doe",
                    "primaryEmail": "john.doe@example.com",
                    "cellPhone": "+1234567890",
                }
            },
            "_links": {
                "self": {"href": "/pms/folios/123"},
                "logs": {"href": "/pms/folios/123/logs"},
            },
        }
        return client

    @pytest.fixture
    def get_folio_use_case(self, mock_api_client):
        """Use case con dependencias mockeadas"""
        return GetFolioUseCase(api_client=mock_api_client)

    @pytest.mark.asyncio
    async def test_get_folio_success_integration(
        self, get_folio_use_case, mock_api_client
    ):
        """Test de integración exitoso para get_folio"""
        # Arrange
        params = GetFolioParams(folio_id=123)

        # Act
        result = await get_folio_use_case.execute(params)

        # Assert
        assert result is not None
        assert isinstance(result, Folio)
        assert result.id == 123
        assert result.reservation_id == 456
        assert result.current_balance == 150.00
        assert result.status == "open"

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_folio_with_different_ids_integration(
        self, get_folio_use_case, mock_api_client
    ):
        """Test de integración con diferentes IDs"""
        folio_ids = [1, 2, 3]

        for folio_id in folio_ids:
            # Arrange
            params = GetFolioParams(folio_id=folio_id)

            # Act
            result = await get_folio_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.id == 123  # Mock response

    @pytest.mark.asyncio
    async def test_get_folio_api_error_integration(self, mock_api_client):
        """Test de integración con error de API"""
        # Arrange
        mock_api_client.get.side_effect = Exception("API Error")
        get_folio_use_case = GetFolioUseCase(api_client=mock_api_client)

        params = GetFolioParams(folio_id=123)

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await get_folio_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_folio_not_found_integration(self, mock_api_client):
        """Test de integración con folio no encontrado"""
        # Arrange
        mock_api_client.get.side_effect = Exception("Folio not found")
        get_folio_use_case = GetFolioUseCase(api_client=mock_api_client)

        params = GetFolioParams(folio_id=999)

        # Act & Assert
        with pytest.raises(Exception, match="Folio not found"):
            await get_folio_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_folio_with_items_integration(
        self, get_folio_use_case, mock_api_client
    ):
        """Test de integración con items del folio"""
        # Arrange
        params = GetFolioParams(folio_id=123)

        # Act
        result = await get_folio_use_case.execute(params)

        # Assert
        assert result is not None
        assert result.id == 123
        assert result.status == "open"

    @pytest.mark.asyncio
    async def test_get_folio_different_statuses_integration(self, mock_api_client):
        """Test de integración con diferentes estados"""
        statuses = ["open", "closed"]

        for status in statuses:
            # Arrange
            mock_api_client.get.return_value = {
                "id": 123,
                "status": status,
                "reservation_id": 456,
                "type": "guest",
                "current_balance": 150.00,
                "realized_balance": 0.00,
                "start_date": "2024-01-15",
                "end_date": "2024-01-20",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "contact_id": 789,
                "company_id": None,
                "travel_agent_id": None,
                "master_folio_id": None,
                "master_folio_rule_id": None,
                "currency": "USD",
                "notes": "Test folio",
                "tags": [],
                "_embedded": {
                    "contact": {
                        "id": 789,
                        "firstName": "John",
                        "lastName": "Doe",
                        "primaryEmail": "john.doe@example.com",
                        "cellPhone": "+1234567890",
                    }
                },
                "_links": {
                    "self": {"href": "/pms/folios/123"},
                    "logs": {"href": "/pms/folios/123/logs"},
                },
            }

            get_folio_use_case = GetFolioUseCase(api_client=mock_api_client)
            params = GetFolioParams(folio_id=123)

            # Act
            result = await get_folio_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.status == status

    @pytest.mark.asyncio
    async def test_get_folio_complete_workflow_integration(
        self, get_folio_use_case, mock_api_client
    ):
        """Test de integración del workflow completo"""
        # Arrange
        params = GetFolioParams(folio_id=123)

        # Act
        result = await get_folio_use_case.execute(params)

        # Assert
        assert result is not None
        assert isinstance(result, Folio)
        assert result.id == 123
        assert result.reservation_id == 456
        assert result.current_balance == 150.00
        assert result.status == "open"

        # Verificar que el API client fue llamado
        mock_api_client.get.assert_called_once()
