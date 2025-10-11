"""
Tests de validación para search_reservations.py
Valida las correcciones implementadas según documentación API V2
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.trackhs_mcp.core.error_handling import ValidationError
from src.trackhs_mcp.tools.search_reservations import register_search_reservations


class TestSearchReservationsValidation:
    """Tests de validación para search_reservations"""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del objeto MCP"""
        return AsyncMock()

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        return AsyncMock()

    @pytest.fixture
    def search_tool(self, mock_mcp, mock_api_client):
        """Herramienta de búsqueda registrada"""
        register_search_reservations(mock_mcp, mock_api_client)
        return mock_mcp.tool.call_args[0][0]

    @pytest.mark.asyncio
    async def test_page_validation_zero_allowed(self, search_tool):
        """Test que página 0 es válida según documentación API V2"""
        # Página 0 debe ser válida
        await search_tool(page=0, size=10)
        # No debe lanzar excepción

    @pytest.mark.asyncio
    async def test_page_validation_negative_invalid(self, search_tool):
        """Test que página negativa es inválida"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(page=-1, size=10)
        assert "Page must be >= 0" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_size_validation_minimum(self, search_tool):
            """Test validación de tamaño mínimo"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(page=1, size=0)
        assert "Size must be >= 1" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_total_results_limit(self, search_tool):
            """Test límite de 10k resultados totales"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(page=1000, size=10)
        assert "Total results (page * size) must be <= 10,000" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_scroll_validation_start_with_one(self, search_tool):
            """Test que scroll debe empezar con 1"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(scroll=2)
        assert "Scroll must start with 1" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_scroll_validation_empty_string(self, search_tool):
            """Test que scroll string no puede estar vacío"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(scroll="")
        assert "Scroll string cannot be empty" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_scroll_disables_sorting(self, search_tool):
            """Test que scroll deshabilita sorting"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(scroll=1, sort_column="status")
        assert "When using scroll, sorting is disabled" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_scroll_disables_sorting_direction(self, search_tool):
            """Test que scroll deshabilita sorting direction"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(scroll=1, sort_direction="desc")
        assert "When using scroll, sorting is disabled" in str(exc_info.value)

    def test_scroll_valid_usage(self, search_tool):
        """Test uso válido de scroll"""
        # Scroll con valores por defecto debe ser válido
        await search_tool(scroll=1)
        # No debe lanzar excepción

    def test_date_validation_flexible_formats(self, search_tool):
        """Test validación flexible de fechas - acepta múltiples formatos"""
        # Fecha con timezone Z (formato completo)
        await search_tool(arrival_start="2024-01-01T00:00:00Z")

        # Solo fecha (se normaliza automáticamente)
        await search_tool(arrival_start="2024-01-01")

        # Fecha con tiempo sin timezone (se normaliza automáticamente)
        await search_tool(arrival_start="2024-01-01T00:00:00")

        # Fecha con timezone offset
        await search_tool(arrival_start="2024-01-01T00:00:00+00:00")

        # Fecha con microsegundos
        await search_tool(arrival_start="2024-01-01T00:00:00.123Z")

    def test_date_validation_with_timezone(self, search_tool):
        """Test validación de fechas con timezone"""
        # Fecha con Z
        await search_tool(arrival_start="2024-01-01T00:00:00Z")

        # Fecha con timezone offset
        await search_tool(arrival_start="2024-01-01T00:00:00+00:00")

        # Fecha con microsegundos
        await search_tool(arrival_start="2024-01-01T00:00:00.123Z")

    def test_status_validation_single(self, search_tool):
        """Test validación de status individual"""
        # Status válido
        await search_tool(status="Confirmed")

        # Status inválido
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(status="InvalidStatus")
        assert "Invalid status" in str(exc_info.value)

    def test_status_validation_list(self, search_tool):
        """Test validación de status como lista"""
        # Lista válida
        await search_tool(status=["Confirmed", "Checked In"])

        # Lista con status inválido
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(status=["Confirmed", "InvalidStatus"])
        assert "Invalid status" in str(exc_info.value)

    def test_status_validation_comma_separated(self, search_tool):
        """Test validación de status separado por comas"""
        # String con comas válido
        await search_tool(status="Confirmed,Checked In")

        # String con comas inválido
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(status="Confirmed,InvalidStatus")
        assert "Invalid status" in str(exc_info.value)

    def test_in_house_today_validation(self, search_tool):
        """Test validación de in_house_today"""
        # Valores válidos
        await search_tool(in_house_today=0)
        await search_tool(in_house_today=1)

        # Valor inválido (debe ser 0 o 1)
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(in_house_today=2)
        # Esto debería fallar en la validación de tipo

    def test_id_parsing_single(self, search_tool):
        """Test parsing de ID único"""
        # ID único como string
        await search_tool(node_id="123")

        # ID único como entero
        await search_tool(node_id=123)

    def test_id_parsing_comma_separated(self, search_tool):
        """Test parsing de IDs separados por comas"""
        # IDs separados por comas
        await search_tool(node_id="123,456,789")

    def test_id_parsing_array_string(self, search_tool):
        """Test parsing de array en formato string"""
        # Array en formato string
        await search_tool(node_id="[123,456,789]")

    @pytest.mark.asyncio
        async def test_id_parsing_empty_string(self, search_tool):
            """Test parsing de string vacío"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(node_id="")
        assert "ID string cannot be empty" in str(exc_info.value)

    @pytest.mark.asyncio
        async def test_id_parsing_invalid_format(self, search_tool):
            """Test parsing de formato inválido"""
        with pytest.raises(ValidationError) as exc_info:
            await search_tool(node_id="invalid")
        assert "Invalid ID format" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_api_error_handling_401(self, search_tool, mock_api_client):
        """Test manejo de error 401"""
        mock_api_client.get.side_effect = Exception("401 Unauthorized")
        mock_api_client.get.side_effect.status_code = 401

        with pytest.raises(ValidationError) as exc_info:
            await search_tool()
        assert "Unauthorized: Invalid authentication credentials" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_api_error_handling_403(self, search_tool, mock_api_client):
        """Test manejo de error 403"""
        error = Exception("403 Forbidden")
        error.status_code = 403
        mock_api_client.get.side_effect = error

        with pytest.raises(ValidationError) as exc_info:
            await search_tool()
        assert "Forbidden: Insufficient permissions" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_api_error_handling_500(self, search_tool, mock_api_client):
        """Test manejo de error 500"""
        error = Exception("500 Internal Server Error")
        error.status_code = 500
        mock_api_client.get.side_effect = error

        with pytest.raises(ValidationError) as exc_info:
            await search_tool()
        assert "Internal Server Error: API temporarily unavailable" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_successful_api_call(self, search_tool, mock_api_client):
        """Test llamada exitosa a la API"""
        mock_response = {"data": "test"}
        mock_api_client.get.return_value = mock_response

        result = await search_tool()
        assert result == mock_response
        mock_api_client.get.assert_called_once()

    def test_query_string_building(self, search_tool):
        """Test construcción de query string"""
        # Este test verificaría que los parámetros se convierten correctamente
        # a query string, pero requiere acceso a la función interna
        pass


class TestDateValidation:
    """Tests específicos para validación de fechas"""

    def test_valid_iso_8601_formats(self):
        """Test formatos ISO 8601 válidos"""
        from src.trackhs_mcp.tools.search_reservations import _is_valid_date_format

        # Formatos válidos
        assert _is_valid_date_format("2024-01-01T00:00:00Z")
        assert _is_valid_date_format("2024-01-01T00:00:00+00:00")
        assert _is_valid_date_format("2024-01-01T00:00:00-05:00")
        assert _is_valid_date_format("2024-01-01T00:00:00.123Z")
        assert _is_valid_date_format("2024-01-01T00:00:00.123456Z")

    def test_invalid_iso_8601_formats(self):
        """Test formatos ISO 8601 inválidos"""
        from src.trackhs_mcp.tools.search_reservations import _is_valid_date_format

        # Formatos inválidos (solo los realmente inválidos)
        assert not _is_valid_date_format("01/01/2024")
        assert not _is_valid_date_format("invalid-date")
        assert not _is_valid_date_format("")
        assert not _is_valid_date_format("2025-01-01T")
        assert not _is_valid_date_format("2025-01-01T00:00:00X")

        # Formatos que SÍ son válidos (se normalizan automáticamente)
        assert _is_valid_date_format("2024-01-01")  # Solo fecha
        assert _is_valid_date_format("2024-01-01T00:00:00")  # Sin timezone
        assert _is_valid_date_format("2024-01-01 00:00:00")  # Con espacio


class TestIDParsing:
    """Tests específicos para parsing de IDs"""

    def test_parse_single_id(self):
        """Test parsing de ID único"""
        from src.trackhs_mcp.tools.search_reservations import _parse_id_string

        assert _parse_id_string("123") == 123
        assert _parse_id_string("0") == 0

    def test_parse_comma_separated_ids(self):
        """Test parsing de IDs separados por comas"""
        from src.trackhs_mcp.tools.search_reservations import _parse_id_string

        assert _parse_id_string("123,456,789") == [123, 456, 789]
        assert _parse_id_string("1,2") == [1, 2]

    def test_parse_array_string_ids(self):
        """Test parsing de array en formato string"""
        from src.trackhs_mcp.tools.search_reservations import _parse_id_string

        assert _parse_id_string("[123,456,789]") == [123, 456, 789]
        assert _parse_id_string("[1,2]") == [1, 2]

    def test_parse_empty_string(self):
        """Test parsing de string vacío"""
        from src.trackhs_mcp.tools.search_reservations import _parse_id_string

        with pytest.raises(ValidationError):
            _parse_id_string("")

    def test_parse_invalid_formats(self):
        """Test parsing de formatos inválidos"""
        from src.trackhs_mcp.tools.search_reservations import _parse_id_string

        with pytest.raises(ValidationError):
            _parse_id_string("invalid")

        with pytest.raises(ValidationError):
            _parse_id_string("123,invalid")

        with pytest.raises(ValidationError):
            _parse_id_string("[123,invalid]")


if __name__ == "__main__":
    pytest.main([__file__])
