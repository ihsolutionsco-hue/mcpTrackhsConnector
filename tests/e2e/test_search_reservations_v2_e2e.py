"""
Tests E2E para search_reservations_v2
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig


class TestSearchReservationsV2E2E:
    """Tests E2E para search_reservations_v2"""

    @pytest.fixture
    def mock_config(self):
        """Configuración mock para testing"""
        return TrackHSConfig(
            base_url="https://api-test.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

    @pytest.fixture
    def mock_api_client(self):
        """API client mock con respuestas realistas"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def mock_mcp(self):
        """Servidor MCP mock"""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def sample_reservations_response_v2(self):
        """Respuesta de ejemplo para API V2"""
        return {
            "data": [
                {
                    "id": 12345,
                    "status": "Confirmed",
                    "arrival_date": "2024-01-15T15:00:00",
                    "departure_date": "2024-01-20T11:00:00",
                    "guest": {
                        "id": 67890,
                        "name": "Juan Pérez",
                        "email": "juan@example.com",
                    },
                    "unit": {
                        "id": 11111,
                        "name": "Suite 101",
                        "unit_type": "Suite",
                    },
                    "policies": {
                        "cancellation_policy": "Flexible",
                        "deposit_required": True,
                    },
                }
            ],
            "pagination": {
                "total": 1,
                "page": 1,
                "size": 10,
                "total_pages": 1,
            },
        }

    @pytest.mark.asyncio
    async def test_search_reservations_v2_basic_search(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para búsqueda básica con search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Mock de respuesta exitosa
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Act
        result = await tool_func(
            page=1,
            size=10,
            sort_column="name",
            sort_direction="asc",
        )

        # Assert
        assert result is not None
        assert "data" in result
        assert "pagination" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == 12345
        assert result["pagination"]["total"] == 1

        # Verificar que se llamó a la API
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_reservations_v2_with_filters(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para búsqueda con filtros en search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Mock de respuesta exitosa
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Act
        result = await tool_func(
            page=1,
            size=10,
            search="Juan",
            status=["Confirmed"],
            node_id="1,2",
            arrival_start="2025-01-01",
            arrival_end="2025-01-31",
        )

        # Assert
        assert result is not None
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == 12345

        # Verificar que se llamó a la API con los parámetros correctos
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_reservations_v2_validation_errors(
        self, mock_mcp, mock_api_client
    ):
        """Test E2E para validación de errores en search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Act & Assert - Fecha inválida
        with pytest.raises(ValidationError, match="Formato de fecha inválido"):
            await tool_func(
                page=1,
                arrival_start="fecha-invalida",
            )

        # Act & Assert - Página negativa
        with pytest.raises(ValidationError, match="Page must be >= 0"):
            await tool_func(
                page=-1,
            )

        # Act & Assert - Tamaño inválido
        with pytest.raises(ValidationError, match="Size must be >= 1"):
            await tool_func(
                page=1,
                size=0,
            )

    @pytest.mark.asyncio
    async def test_search_reservations_v2_api_errors(self, mock_mcp, mock_api_client):
        """Test E2E para manejo de errores de API en search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Test 401 - Unauthorized
        mock_api_client.get.side_effect = Exception("401 Unauthorized")
        with pytest.raises(Exception, match="401 Unauthorized"):
            await tool_func(page=1)

        # Test 403 - Forbidden
        mock_api_client.get.side_effect = Exception("403 Forbidden")
        with pytest.raises(Exception, match="403 Forbidden"):
            await tool_func(page=1)

        # Test 500 - Server Error
        mock_api_client.get.side_effect = Exception("500 Internal Server Error")
        with pytest.raises(Exception, match="500 Internal Server Error"):
            await tool_func(page=1)

    @pytest.mark.asyncio
    async def test_search_reservations_v2_date_formats(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para diferentes formatos de fecha en search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Mock de respuesta exitosa
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Test diferentes formatos de fecha válidos
        test_cases = [
            ("2025-01-01", "2025-01-31"),  # Formato básico
            ("2025-01-01T00:00:00Z", "2025-01-31T23:59:59Z"),  # Formato ISO completo
        ]

        for arrival_start, arrival_end in test_cases:
            # Act
            result = await tool_func(
                page=1,
                arrival_start=arrival_start,
                arrival_end=arrival_end,
            )

            # Assert
            assert result is not None
            assert "data" in result

        # Verificar que se llamó a la API
        assert mock_api_client.get.call_count == len(test_cases)

    @pytest.mark.asyncio
    async def test_search_reservations_v2_comprehensive_workflow(
        self, mock_mcp, mock_api_client, sample_reservations_response_v2
    ):
        """Test E2E para flujo completo de búsqueda en search_reservations_v2"""
        # Arrange
        from src.trackhs_mcp.infrastructure.mcp.search_reservations_v2 import (
            register_search_reservations_v2,
        )

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        register_search_reservations_v2(mock_mcp, mock_api_client)

        # Obtener la función registrada
        tool_func = registered_function

        # Mock de respuesta exitosa
        mock_api_client.get.return_value = sample_reservations_response_v2

        # Act - Búsqueda completa con todos los parámetros
        result = await tool_func(
            page=1,
            size=10,
            search="Juan",
            status=["Confirmed", "Checked In"],
            node_id="1,2,3",
            unit_id="10,20",
            contact_id="100,200",
            arrival_start="2025-01-01",
            arrival_end="2025-01-31",
            departure_start="2025-01-01",
            departure_end="2025-01-31",
            sort_column="name",
            sort_direction="asc",
        )

        # Assert
        assert result is not None
        assert "data" in result
        assert "pagination" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == 12345
        assert result["pagination"]["total"] == 1

        # Verificar que se llamó a la API
        mock_api_client.get.assert_called_once()
