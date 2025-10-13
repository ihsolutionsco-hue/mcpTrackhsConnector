"""
Tests unitarios para la herramienta MCP search_units
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.trackhs_mcp.domain.exceptions.api_exceptions import ValidationError
from src.trackhs_mcp.infrastructure.mcp.search_units import (
    _is_valid_date_format,
    _parse_id_list,
    _parse_id_string,
    register_search_units,
)


class TestSearchUnitsTool:
    """Tests para la herramienta MCP search_units"""

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

    def test_register_search_units(self, mock_mcp, mock_api_client):
        """Test de registro de la herramienta"""
        # Act
        register_search_units(mock_mcp, mock_api_client)

        # Assert
        mock_mcp.tool.assert_called_once()

    def test_is_valid_date_format_valid_dates(self):
        """Test de validación de formatos de fecha válidos"""
        valid_dates = [
            "2024-01-01",
            "2024-01-01T00:00:00",
            "2024-01-01T00:00:00Z",
            "2024-01-01T00:00:00+00:00",
            "2024-01-01T00:00:00-05:00",
            "2024-01-01 00:00:00",
        ]

        for date_str in valid_dates:
            assert _is_valid_date_format(date_str), f"Date {date_str} should be valid"

    def test_is_valid_date_format_invalid_dates(self):
        """Test de validación de formatos de fecha inválidos"""
        invalid_dates = [
            "01/01/2024",
            "2024-1-1",
            "2024-13-01",
            "2024-01-32",
            "invalid-date",
            "",
            None,
        ]

        for date_str in invalid_dates:
            if date_str is not None:
                assert not _is_valid_date_format(
                    date_str
                ), f"Date {date_str} should be invalid"

    def test_parse_id_string_single_int(self):
        """Test de parsing de ID único como entero"""
        # Act
        result = _parse_id_string("123")

        # Assert
        assert result == 123

    def test_parse_id_string_single_int_already_int(self):
        """Test de parsing de ID único ya como entero"""
        # Act
        result = _parse_id_string(123)

        # Assert
        assert result == 123

    def test_parse_id_string_comma_separated(self):
        """Test de parsing de IDs separados por comas"""
        # Act
        result = _parse_id_string("1,2,3")

        # Assert
        assert result == [1, 2, 3]

    def test_parse_id_string_array_format(self):
        """Test de parsing de formato array"""
        # Act
        result = _parse_id_string("[1,2,3]")

        # Assert
        assert result == [1, 2, 3]

    def test_parse_id_string_single_item_array(self):
        """Test de parsing de array con un elemento"""
        # Act
        result = _parse_id_string("[123]")

        # Assert
        assert result == 123

    def test_parse_id_string_empty(self):
        """Test de parsing de string vacío"""
        # Act & Assert
        with pytest.raises(ValidationError, match="ID string cannot be empty"):
            _parse_id_string("")

    def test_parse_id_string_invalid_format(self):
        """Test de parsing de formato inválido"""
        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid ID format"):
            _parse_id_string("invalid")

    def test_parse_id_string_empty_array(self):
        """Test de parsing de array vacío"""
        # Act & Assert
        with pytest.raises(ValidationError, match="Empty array not allowed"):
            _parse_id_string("[]")

    def test_parse_id_list_comma_separated(self):
        """Test de parsing de lista de IDs separados por comas"""
        # Act
        result = _parse_id_list("1,2,3")

        # Assert
        assert result == [1, 2, 3]

    def test_parse_id_list_array_format(self):
        """Test de parsing de formato array para lista"""
        # Act
        result = _parse_id_list("[1,2,3]")

        # Assert
        assert result == [1, 2, 3]

    def test_parse_id_list_single_id(self):
        """Test de parsing de ID único para lista"""
        # Act
        result = _parse_id_list("123")

        # Assert
        assert result == [123]

    def test_parse_id_list_empty(self):
        """Test de parsing de string vacío para lista"""
        # Act & Assert
        with pytest.raises(ValidationError, match="ID string cannot be empty"):
            _parse_id_list("")

    def test_parse_id_list_invalid_format(self):
        """Test de parsing de formato inválido para lista"""
        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid ID format"):
            _parse_id_list("invalid")

    def test_parse_id_list_empty_array(self):
        """Test de parsing de array vacío para lista"""
        # Act & Assert
        with pytest.raises(ValidationError, match="Empty array not allowed"):
            _parse_id_list("[]")


class TestSearchUnitsToolIntegration:
    """Tests de integración para la herramienta MCP"""

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

    @pytest.mark.asyncio
    async def test_search_units_basic_call(self, mock_mcp, mock_api_client):
        """Test de llamada básica a search_units"""
        # Arrange
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
        tool_func = registered_function

        expected_response = {
            "_embedded": {"units": []},
            "page": 0,
            "page_count": 1,
            "page_size": 25,
            "total_items": 0,
            "_links": {},
        }
        mock_api_client.get.return_value = expected_response

        # Act
        result = await tool_func(page=0, size=25)

        # Assert
        assert result == expected_response

    @pytest.mark.asyncio
    async def test_search_units_with_filters(self, mock_mcp, mock_api_client):
        """Test de llamada con filtros"""
        # Arrange
        register_search_units(mock_mcp, mock_api_client)

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
        tool_func = registered_function

        expected_response = {"_embedded": {"units": []}}
        mock_api_client.get.return_value = expected_response

        # Act
        result = await tool_func(
            page=0,
            size=10,
            bedrooms=2,
            bathrooms=2,
            pets_friendly=1,
            is_active=1,
            node_id="1,2,3",
        )

        # Assert
        assert result == expected_response

    @pytest.mark.asyncio
    async def test_search_units_validation_errors(self, mock_mcp, mock_api_client):
        """Test de errores de validación"""
        # Arrange
        register_search_units(mock_mcp, mock_api_client)

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
        tool_func = registered_function

        # Test página negativa (ahora se convierte automáticamente, pero Pydantic valida)
        with pytest.raises(Exception, match="API request failed"):
            await tool_func(page=-1)

        # Test tamaño inválido (ahora se convierte automáticamente, pero Pydantic valida)
        with pytest.raises(Exception, match="API request failed"):
            await tool_func(size=0)

        # Test límite total de resultados (usar valores que realmente excedan el límite)
        with pytest.raises(
            Exception, match="Total results \\(page \\* size\\) must be <= 10,000"
        ):
            await tool_func(
                page=102, size=100
            )  # adjusted_page = 101, 101 * 100 = 10,100

        # Test formato de fecha inválido
        with pytest.raises(Exception, match="Formato de fecha inválido"):
            await tool_func(arrival="01/01/2024")

        # Test rango de habitaciones inválido
        with pytest.raises(Exception, match="min_bedrooms must be <= max_bedrooms"):
            await tool_func(min_bedrooms=3, max_bedrooms=1)

    @pytest.mark.asyncio
    async def test_search_units_api_errors(self, mock_mcp, mock_api_client):
        """Test de manejo de errores de API"""
        # Arrange
        register_search_units(mock_mcp, mock_api_client)

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
        tool_func = registered_function

        # Test error 401
        error_401 = Exception("Unauthorized")
        error_401.status_code = 401
        mock_api_client.get.side_effect = error_401

        with pytest.raises(
            ValidationError, match="Unauthorized: Invalid authentication credentials"
        ):
            await tool_func()

        # Test error 403
        error_403 = Exception("Forbidden")
        error_403.status_code = 403
        mock_api_client.get.side_effect = error_403

        with pytest.raises(
            ValidationError, match="Forbidden: Insufficient permissions"
        ):
            await tool_func()

        # Test error 404
        error_404 = Exception("Not Found")
        error_404.status_code = 404
        mock_api_client.get.side_effect = error_404

        with pytest.raises(ValidationError, match="Endpoint not found"):
            await tool_func()

        # Test error 500
        error_500 = Exception("Internal Server Error")
        error_500.status_code = 500
        mock_api_client.get.side_effect = error_500

        with pytest.raises(ValidationError, match="Internal Server Error"):
            await tool_func()
