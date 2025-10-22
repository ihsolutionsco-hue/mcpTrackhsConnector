"""
Tests end-to-end para search_units
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.search_units import register_search_units


class TestSearchUnitsE2E:
    """Tests end-to-end para search_units"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP"""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

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
    async def test_e2e_basic_search(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda básica"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 1,
                        "name": "Villa Paradise",
                        "shortName": "VP001",
                        "unitCode": "VP001",
                        "nodeId": 1,
                        "bedrooms": 3,
                        "fullBathrooms": 2,
                        "maxOccupancy": 6,
                        "petsFriendly": True,
                        "eventsAllowed": False,
                        "smokingAllowed": False,
                        "childrenAllowed": True,
                        "isAccessible": True,
                        "updatedAt": "2024-01-15T10:30:00Z",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {
                "self": {"href": "https://api.example.com/api/pms/units/?page=0"},
                "first": {"href": "https://api.example.com/api/pms/units/"},
                "last": {"href": "https://api.example.com/api/pms/units/?page=0"},
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=1, size=3)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_filters(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con filtros"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 2,
                        "name": "Beach House",
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "petsFriendly": True,
                        "isActive": True,
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(
            page=1, size=3, bedrooms=2, bathrooms=2, pets_friendly=1, is_active=1
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 10,
                "sortColumn": "name",
                "sortDirection": "asc",
                "bedrooms": 2,
                "bathrooms": 2,
                "petsFriendly": 1,
                "isActive": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_by_availability(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda por disponibilidad"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 3,
                        "name": "Mountain Cabin",
                        "isBookable": True,
                        "arrival": "2024-01-01",
                        "departure": "2024-01-07",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(
            arrival="2024-01-01", departure="2024-01-07", is_bookable=1
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "arrival": "2024-01-01",
                "departure": "2024-01-07",
                "isBookable": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_by_amenities(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda por amenidades"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 4,
                        "name": "Luxury Penthouse",
                        "amenities": [
                            {
                                "id": 1,
                                "name": "Pool",
                                "group": {"id": 1, "name": "Outdoor"},
                            },
                            {
                                "id": 2,
                                "name": "Gym",
                                "group": {"id": 2, "name": "Fitness"},
                            },
                        ],
                        "petsFriendly": True,
                        "eventsAllowed": True,
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(amenity_id="1,2,3", pets_friendly=1, events_allowed=1)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "amenityId": [1, 2, 3],
                "petsFriendly": 1,
                "eventsAllowed": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_by_location(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda por ubicación"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 5,
                        "name": "Downtown Apartment",
                        "nodeId": 1,
                        "locality": "Miami",
                        "region": "FL",
                        "country": "US",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(node_id="1,2,3", is_active=1)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "nodeId": [1, 2, 3],
                "isActive": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_sorting(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con ordenamiento"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {"id": 3, "name": "Z Villa"},
                    {"id": 2, "name": "B House"},
                    {"id": 1, "name": "A Apartment"},
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 3,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(sort_column="name", sort_direction="desc", size=3)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "desc",
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_text(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda por texto"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 6,
                        "name": "Luxury Villa with Ocean View",
                        "shortDescription": "Beautiful villa with stunning ocean views",
                        "longDescription": "This luxury villa offers breathtaking ocean views and modern amenities",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(search="luxury villa ocean view")

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "search": "luxury villa ocean view",
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_room_filters(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con filtros de habitaciones"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 7,
                        "name": "Family House",
                        "bedrooms": 3,
                        "fullBathrooms": 2,
                        "halfBathrooms": 1,
                        "maxOccupancy": 8,
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(bedrooms=3, min_bathrooms=2, max_bathrooms=3)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "bedrooms": 3,
                "minBathrooms": 2,
                "maxBathrooms": 3,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_status_filters(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con filtros de estado"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 8,
                        "name": "Clean Unit",
                        "isActive": True,
                        "isBookable": True,
                        "unitStatus": "clean",
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(is_active=1, is_bookable=1, unit_status="clean")

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "isActive": 1,
                "isBookable": 1,
                "unitStatus": "clean",
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_boolean_filters(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con filtros booleanos"""
        # Arrange
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 9,
                        "name": "Pet-Friendly Accessible Unit",
                        "petsFriendly": True,
                        "eventsAllowed": False,
                        "smokingAllowed": False,
                        "childrenAllowed": True,
                        "isAccessible": True,
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(
            pets_friendly=1,
            events_allowed=0,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 1,
                "size": 25,
                "sortColumn": "name",
                "sortDirection": "asc",
                "petsFriendly": 1,
                "eventsAllowed": 0,
                "smokingAllowed": 0,
                "childrenAllowed": 1,
                "isAccessible": 1,
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_with_pagination(self, setup_tool, mock_api_client):
        """Test E2E de búsqueda con paginación"""
        # Arrange
        expected_response = {
            "_embedded": {"units": []},
            "page": 2,
            "page_count": 10,
            "page_size": 100,
            "total_items": 1000,
            "_links": {
                "self": {"href": "https://api.example.com/api/pms/units/?page=2"},
                "first": {"href": "https://api.example.com/api/pms/units/"},
                "last": {"href": "https://api.example.com/api/pms/units/?page=9"},
                "next": {"href": "https://api.example.com/api/pms/units/?page=3"},
                "prev": {"href": "https://api.example.com/api/pms/units/?page=1"},
            },
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await setup_tool(page=2, size=5)

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(
            "/pms/units",
            params={
                "page": 2,  # page=2 (1-based) → page=2 (1-based)
                "size": 100,
                "sortColumn": "name",
                "sortDirection": "asc",
            },
        )

    @pytest.mark.asyncio
    async def test_e2e_search_validation_errors(self, setup_tool):
        """Test E2E de errores de validación"""
        # Test página negativa
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            await setup_tool(page=-1)

        # Test tamaño inválido
        with pytest.raises(ValidationError, match="Size must be >= 1"):
            await setup_tool(size=0)

        # Test límite total de resultados (ahora con page=102 para exceder 10k)
        with pytest.raises(
            Exception, match="Total results \\(page \\* size\\) must be <= 10,000"
        ):
            await setup_tool(page=2001, size=5)

        # Test formato de fecha inválido
        with pytest.raises(Exception, match="Formato de fecha inválido"):
            await setup_tool(arrival="01/01/2024")

        # Test rango de habitaciones inválido
        with pytest.raises(
            Exception, match="min_bedrooms cannot be greater than max_bedrooms"
        ):
            await setup_tool(min_bedrooms=3, max_bedrooms=1)

    @pytest.mark.asyncio
    async def test_e2e_search_api_errors(self, setup_tool, mock_api_client):
        """Test E2E de errores de API"""
        # Test error 401
        error_401 = Exception("Unauthorized")
        error_401.status_code = 401
        mock_api_client.get.side_effect = error_401

        with pytest.raises(
            ValidationError, match="Unauthorized: Invalid authentication credentials"
        ):
            await setup_tool()

        # Reset mock
        mock_api_client.reset_mock()

        # Test error 403
        error_403 = Exception("Forbidden")
        error_403.status_code = 403
        mock_api_client.get.side_effect = error_403

        with pytest.raises(
            ValidationError, match="Forbidden: Insufficient permissions"
        ):
            await setup_tool()

        # Reset mock
        mock_api_client.reset_mock()

        # Test error 404
        error_404 = Exception("Not Found")
        error_404.status_code = 404
        mock_api_client.get.side_effect = error_404

        with pytest.raises(ValidationError, match="Endpoint not found"):
            await setup_tool()

        # Reset mock
        mock_api_client.reset_mock()

        # Test error 500
        error_500 = Exception("Internal Server Error")
        error_500.status_code = 500
        mock_api_client.get.side_effect = error_500

        with pytest.raises(ValidationError, match="Internal Server Error"):
            await setup_tool()

    @pytest.mark.asyncio
    async def test_search_units_with_integer_params_fixed(
        self, setup_tool, mock_api_client
    ):
        """Test con parámetros numéricos como integers (corrección del bloqueador crítico)"""
        # Mock response
        expected_response = {
            "_embedded": {
                "units": [
                    {
                        "id": 1,
                        "name": "Unit 1",
                        "bedrooms": 2,
                        "bathrooms": 1,
                        "isActive": True,
                        "petsFriendly": True,
                    }
                ]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 5,
            "total_items": 1,
        }
        mock_api_client.get.return_value = expected_response

        # Act - Ejecutar con parámetros numéricos como integers (caso que antes fallaba)
        result = await setup_tool(
            page=1,  # int
            size=5,  # int
            bedrooms=2,  # int
            bathrooms=1,  # int
            is_active=1,  # int
            pets_friendly=1,  # int
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_units_with_all_numeric_params(
        self, setup_tool, mock_api_client
    ):
        """Test con todos los parámetros numéricos como integers"""
        # Mock response
        expected_response = {
            "_embedded": {
                "units": [{"id": 1, "name": "Unit 1", "bedrooms": 2, "bathrooms": 1}]
            },
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
        }
        mock_api_client.get.return_value = expected_response

        # Act - Ejecutar con todos los parámetros numéricos
        result = await setup_tool(
            page=1,
            size=3,
            calendar_id=123,
            role_id=456,
            bedrooms=2,
            min_bedrooms=1,
            max_bedrooms=4,
            bathrooms=1,
            min_bathrooms=1,
            max_bathrooms=2,
            pets_friendly=1,
            allow_unit_rates=1,
            computed=1,
            inherited=1,
            limited=1,
            is_bookable=1,
            include_descriptions=1,
            is_active=1,
            events_allowed=1,
            smoking_allowed=0,
            children_allowed=1,
            is_accessible=1,
        )

        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_units_error_messages_are_user_friendly(
        self, setup_tool, mock_api_client
    ):
        """Test que verifica mensajes de error amigables"""
        # Test con fecha inválida para verificar mensaje de error
        with pytest.raises(ValidationError) as exc_info:
            await setup_tool(page=1, size=25, arrival="invalid-date")  # Fecha inválida

        # Verificar que el mensaje de error es amigable
        error_message = str(exc_info.value)
        assert "Formato de fecha inválido" in error_message
        assert "2025-01-01" in error_message  # Debe incluir ejemplo
        assert (
            "arrival='2025-01-15'" in error_message
        )  # Debe incluir ejemplo específico

    @pytest.mark.asyncio
    async def test_search_units_performance_requirements(
        self, setup_tool, mock_api_client
    ):
        """Test de requisitos de performance"""
        import time

        # Mock response
        expected_response = {
            "_embedded": {"units": [{"id": 1, "name": "Unit 1"}]},
            "page": 1,
            "page_count": 1,
            "page_size": 25,
            "total_items": 1,
        }
        mock_api_client.get.return_value = expected_response

        # Medir tiempo de respuesta
        start_time = time.time()
        result = await setup_tool(page=1, size=3, bedrooms=2)
        end_time = time.time()

        response_time = end_time - start_time

        # Verificar que el tiempo de respuesta es < 3 segundos
        assert (
            response_time < 3.0
        ), f"Tiempo de respuesta {response_time:.2f}s debe ser < 3s"

        # Verificar resultado
        assert result == expected_response
