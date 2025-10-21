"""
Tests E2E refactorizados para search_units siguiendo mejores prácticas arquitecturales.

Estos tests se enfocan en:
1. Comportamiento del usuario, no implementación interna
2. Contratos de la API, no parámetros específicos
3. Robustez ante cambios en la implementación
4. Separación clara de responsabilidades
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestSearchUnitsE2ERefactored:
    """Tests E2E refactorizados para search_units con mejores prácticas"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API con respuesta estándar"""
        client = AsyncMock()
        client.get.return_value = {
            "_embedded": {
                "units": [
                    {
                        "id": 1,
                        "name": "Test Unit",
                        "unitType": {"name": "Villa"},
                        "node": {"name": "Test Node"},
                    }
                ]
            },
            "page": {"totalElements": 1, "totalPages": 1},
        }
        return client

    @pytest.fixture
    def setup_tool(self, mock_mcp, mock_api_client):
        """Configuración de la herramienta"""
        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator

        # Registrar la función
        register_search_units(mock_mcp, mock_api_client)

        # Obtener la función registrada
        return registered_function

    @pytest.mark.asyncio
    async def test_basic_search_returns_expected_structure(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda básica retorna estructura esperada"""
        # Act
        result = await setup_tool()

        # Assert - Verificar comportamiento, no implementación
        assert result is not None
        assert "_embedded" in result
        assert "units" in result["_embedded"]
        assert isinstance(result["_embedded"]["units"], list)

        # Verificar que se llamó a la API (comportamiento, no parámetros específicos)
        mock_api_client.get.assert_called_once()
        call_args = mock_api_client.get.call_args
        assert call_args[0][0] == "/pms/units"  # Endpoint correcto
        assert "params" in call_args[1]  # Se pasaron parámetros

    @pytest.mark.asyncio
    async def test_search_with_filters_works_correctly(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda con filtros funciona correctamente"""
        # Act
        result = await setup_tool(bedrooms=2, bathrooms=2, pets_friendly=1, is_active=1)

        # Assert - Verificar comportamiento
        assert result is not None
        assert "_embedded" in result

        # Verificar que se llamó a la API con filtros
        mock_api_client.get.assert_called_once()
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]

        # Verificar que los filtros se pasaron correctamente
        assert params["bedrooms"] == 2
        assert params["bathrooms"] == 2
        assert params["petsFriendly"] == 1
        assert params["isActive"] == 1

    @pytest.mark.asyncio
    async def test_search_with_availability_filters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con filtros de disponibilidad"""
        # Act
        result = await setup_tool(
            arrival="2024-01-01", departure="2024-01-07", is_bookable=1
        )

        # Assert
        assert result is not None

        # Verificar parámetros de disponibilidad
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["arrival"] == "2024-01-01"
        assert params["departure"] == "2024-01-07"
        assert params["isBookable"] == 1

    @pytest.mark.asyncio
    async def test_search_with_amenities_and_features(
        self, setup_tool, mock_api_client
    ):
        """Test E2E: Búsqueda con amenidades y características"""
        # Act
        result = await setup_tool(
            amenity_id="1,2,3",
            pets_friendly=1,
            events_allowed=1,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
        )

        # Assert
        assert result is not None

        # Verificar parámetros de amenidades
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["amenityId"] == [1, 2, 3]
        assert params["petsFriendly"] == 1
        assert params["eventsAllowed"] == 1
        assert params["smokingAllowed"] == 0
        assert params["childrenAllowed"] == 1
        assert params["isAccessible"] == 1

    @pytest.mark.asyncio
    async def test_search_with_location_filters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con filtros de ubicación"""
        # Act
        result = await setup_tool(node_id="1,2,3", is_active=1)

        # Assert
        assert result is not None

        # Verificar parámetros de ubicación
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["nodeId"] == [1, 2, 3]
        assert params["isActive"] == 1

    @pytest.mark.asyncio
    async def test_search_with_sorting_options(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con opciones de ordenamiento"""
        # Act
        result = await setup_tool(sort_column="name", sort_direction="desc")

        # Assert
        assert result is not None

        # Verificar parámetros de ordenamiento
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["sortColumn"] == "name"
        assert params["sortDirection"] == "desc"

    @pytest.mark.asyncio
    async def test_search_with_text_filters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con filtros de texto"""
        # Act
        result = await setup_tool(search="luxury villa ocean view")

        # Assert
        assert result is not None

        # Verificar parámetros de texto
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["search"] == "luxury villa ocean view"

    @pytest.mark.asyncio
    async def test_search_with_room_filters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con filtros de habitaciones"""
        # Act
        result = await setup_tool(bedrooms=3, min_bathrooms=2, max_bathrooms=3)

        # Assert
        assert result is not None

        # Verificar parámetros de habitaciones
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["bedrooms"] == 3
        assert params["minBathrooms"] == 2
        assert params["maxBathrooms"] == 3

    @pytest.mark.asyncio
    async def test_search_with_status_filters(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con filtros de estado"""
        # Act
        result = await setup_tool(is_active=1, is_bookable=1, unit_status="clean")

        # Assert
        assert result is not None

        # Verificar parámetros de estado
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["isActive"] == 1
        assert params["isBookable"] == 1
        assert params["unitStatus"] == "clean"

    @pytest.mark.asyncio
    async def test_search_with_pagination(self, setup_tool, mock_api_client):
        """Test E2E: Búsqueda con paginación"""
        # Act
        result = await setup_tool(page=2, size=100)

        # Assert
        assert result is not None

        # Verificar parámetros de paginación
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]
        assert params["page"] == 2  # page=2 (1-based) → page=2 (1-based)
        assert params["size"] == 100

    @pytest.mark.asyncio
    async def test_search_handles_api_errors_gracefully(self):
        """Test E2E: Manejo de errores de API"""
        # Arrange - Mock que simula error de API
        mock_api_client = AsyncMock()
        mock_api_client.get.side_effect = Exception("API Error")

        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp = MagicMock()
        mock_mcp.tool = mock_tool_decorator

        register_search_units(mock_mcp, mock_api_client)
        tool_func = registered_function

        # Act & Assert - Verificar que se maneja el error correctamente
        with pytest.raises(Exception):
            await tool_func()

    @pytest.mark.asyncio
    async def test_search_validation_errors_handled_correctly(self, setup_tool):
        """Test E2E: Manejo de errores de validación"""
        # Act & Assert - Verificar que se manejan errores de validación
        with pytest.raises(Exception, match="Page must be >= 1"):
            await setup_tool(page=-1)  # Página inválida

    @pytest.mark.asyncio
    async def test_search_comprehensive_workflow(self, setup_tool, mock_api_client):
        """Test E2E: Flujo de trabajo completo"""
        # Act - Búsqueda compleja con múltiples filtros
        result = await setup_tool(
            page=1,
            size=25,
            search="luxury",
            bedrooms=2,
            bathrooms=2,
            pets_friendly=1,
            events_allowed=1,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
            is_active=1,
            is_bookable=1,
            node_id="1,2,3",
            amenity_id="4,5,6",
            arrival="2024-01-01",
            departure="2024-01-07",
            sort_column="name",
            sort_direction="asc",
        )

        # Assert - Verificar que funciona correctamente
        assert result is not None
        assert "_embedded" in result

        # Verificar que se llamó a la API
        mock_api_client.get.assert_called_once()

        # Verificar que se pasaron todos los parámetros
        call_args = mock_api_client.get.call_args
        params = call_args[1]["params"]

        # Verificar parámetros principales
        assert params["page"] == 1
        assert params["size"] == 25
        assert params["search"] == "luxury"
        assert params["bedrooms"] == 2
        assert params["bathrooms"] == 2
        assert params["petsFriendly"] == 1
        assert params["eventsAllowed"] == 1
        assert params["smokingAllowed"] == 0
        assert params["childrenAllowed"] == 1
        assert params["isAccessible"] == 1
        assert params["isActive"] == 1
        assert params["isBookable"] == 1
        assert params["nodeId"] == [1, 2, 3]
        assert params["amenityId"] == [4, 5, 6]
        assert params["arrival"] == "2024-01-01"
        assert params["departure"] == "2024-01-07"
        assert params["sortColumn"] == "name"
        assert params["sortDirection"] == "asc"
