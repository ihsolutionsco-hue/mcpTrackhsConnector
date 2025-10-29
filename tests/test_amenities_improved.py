"""
Tests unitarios para la función search_amenities mejorada.
Demuestra mejores prácticas de testing con FastMCP.
"""

from unittest.mock import Mock, patch

import httpx
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from src.trackhs_mcp.amenities_improved import (
    AmenitiesSearchParams,
    _build_amenities_params,
    _handle_amenities_error,
    search_amenities_improved,
)


class TestAmenitiesSearchParams:
    """Tests para el modelo Pydantic de validación."""

    def test_valid_params(self):
        """Test parámetros válidos."""
        params = AmenitiesSearchParams(page=1, size=10, search="wifi", isPublic=1)

        assert params.page == 1
        assert params.size == 10
        assert params.search == "wifi"
        assert params.isPublic == 1
        assert params.sortColumn is None

    def test_default_values(self):
        """Test valores por defecto."""
        params = AmenitiesSearchParams()

        assert params.page == 1
        assert params.size == 10
        assert params.sortColumn is None
        assert params.search is None

    def test_validation_errors(self):
        """Test errores de validación."""
        with pytest.raises(ValidationError) as exc_info:
            AmenitiesSearchParams(page=-1)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("page",) for error in errors)

    def test_string_validation(self):
        """Test validación de strings."""
        # String vacío debe convertirse a None
        params = AmenitiesSearchParams(search="   ")
        assert params.search is None

        # String válido debe mantenerse
        params = AmenitiesSearchParams(search="wifi")
        assert params.search == "wifi"

        # String muy corto debe fallar
        with pytest.raises(ValidationError):
            AmenitiesSearchParams(search="a")

    def test_enum_validation(self):
        """Test validación de enums."""
        # Valores válidos
        params = AmenitiesSearchParams(sortColumn="id", sortDirection="asc")
        assert params.sortColumn == "id"
        assert params.sortDirection == "asc"

        # Valores inválidos
        with pytest.raises(ValidationError):
            AmenitiesSearchParams(sortColumn="invalid")

        with pytest.raises(ValidationError):
            AmenitiesSearchParams(sortDirection="invalid")


class TestBuildAmenitiesParams:
    """Tests para construcción de parámetros de API."""

    def test_basic_params(self):
        """Test parámetros básicos."""
        params = AmenitiesSearchParams(page=1, size=10)
        api_params = _build_amenities_params(params)

        assert api_params == {"page": 1, "size": 10}

    def test_all_params(self):
        """Test todos los parámetros."""
        params = AmenitiesSearchParams(
            page=2,
            size=20,
            sortColumn="name",
            sortDirection="desc",
            search="wifi",
            groupId=1,
            isPublic=1,
            publicSearchable=1,
            isFilterable=1,
            homeawayType="pool%",
            airbnbType="ac",
            tripadvisorType="wifi%",
            marriottType="pool%",
        )

        api_params = _build_amenities_params(params)

        expected = {
            "page": 2,
            "size": 20,
            "sortColumn": "name",
            "sortDirection": "desc",
            "search": "wifi",
            "groupId": 1,
            "isPublic": 1,
            "publicSearchable": 1,
            "isFilterable": 1,
            "homeawayType": "pool%",
            "airbnbType": "ac",
            "tripadvisorType": "wifi%",
            "marriottType": "pool%",
        }

        assert api_params == expected

    def test_none_params_filtered(self):
        """Test que parámetros None no se incluyen."""
        params = AmenitiesSearchParams(
            page=1,
            size=10,
            search="wifi",
            sortColumn=None,  # No debe incluirse
            groupId=None,  # No debe incluirse
        )

        api_params = _build_amenities_params(params)

        assert "sortColumn" not in api_params
        assert "groupId" not in api_params
        assert api_params["search"] == "wifi"


class TestHandleAmenitiesError:
    """Tests para manejo de errores."""

    def test_validation_error(self):
        """Test error de validación."""
        error = ValidationError.from_exception_data(
            "AmenitiesSearchParams",
            [
                {
                    "type": "value_error",
                    "loc": ("page",),
                    "msg": "Value must be positive",
                }
            ],
        )

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "Parámetros inválidos" in str(tool_error)
        assert "page" in str(tool_error)

    def test_http_401_error(self):
        """Test error HTTP 401."""
        response = Mock()
        response.status_code = 401
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=response)

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "autenticación" in str(tool_error).lower()

    def test_http_403_error(self):
        """Test error HTTP 403."""
        response = Mock()
        response.status_code = 403
        error = httpx.HTTPStatusError("Forbidden", request=Mock(), response=response)

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "autorización" in str(tool_error).lower()

    def test_http_404_error(self):
        """Test error HTTP 404."""
        response = Mock()
        response.status_code = 404
        error = httpx.HTTPStatusError("Not Found", request=Mock(), response=response)

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "no encontrado" in str(tool_error).lower()

    def test_http_500_error(self):
        """Test error HTTP 500."""
        response = Mock()
        response.status_code = 500
        error = httpx.HTTPStatusError(
            "Internal Server Error", request=Mock(), response=response
        )

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "servidor" in str(tool_error).lower()

    def test_request_error(self):
        """Test error de conexión."""
        error = httpx.RequestError("Connection failed")

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "conexión" in str(tool_error).lower()

    def test_unexpected_error(self):
        """Test error inesperado."""
        error = ValueError("Unexpected error")

        tool_error = _handle_amenities_error(error)

        assert isinstance(tool_error, ToolError)
        assert "interno" in str(tool_error).lower()


class TestSearchAmenitiesImproved:
    """Tests para la función principal."""

    def test_no_api_client(self):
        """Test sin cliente API."""
        with pytest.raises(ToolError) as exc_info:
            search_amenities_improved(api_client=None)

        assert "no disponible" in str(exc_info.value).lower()

    def test_validation_error(self):
        """Test error de validación de parámetros."""
        mock_client = Mock()

        with pytest.raises(ToolError) as exc_info:
            search_amenities_improved(api_client=mock_client, page=-1)  # Valor inválido

        assert "inválidos" in str(exc_info.value).lower()

    @patch("src.trackhs_mcp.amenities_improved.logger")
    def test_successful_search(self, mock_logger):
        """Test búsqueda exitosa."""
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 5,
            "page": 1,
            "page_size": 10,
            "_embedded": {
                "amenities": [{"id": 1, "name": "WiFi"}, {"id": 2, "name": "Pool"}]
            },
        }

        result = search_amenities_improved(
            api_client=mock_client, page=1, size=10, search="wifi"
        )

        assert result["total_items"] == 5
        assert len(result["_embedded"]["amenities"]) == 2

        # Verificar que se llamó con parámetros correctos
        mock_client.get.assert_called_once_with(
            "api/pms/units/amenities", {"page": 1, "size": 10, "search": "wifi"}
        )

        # Verificar logging
        mock_logger.info.assert_called()

    def test_http_error_handling(self):
        """Test manejo de errores HTTP."""
        mock_client = Mock()
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=Mock(), response=Mock(status_code=401)
        )

        with pytest.raises(ToolError) as exc_info:
            search_amenities_improved(api_client=mock_client)

        assert "autenticación" in str(exc_info.value).lower()

    def test_unexpected_response(self):
        """Test respuesta inesperada."""
        mock_client = Mock()
        mock_client.get.return_value = "not a dict"  # Respuesta inválida

        with pytest.raises(ToolError) as exc_info:
            search_amenities_improved(api_client=mock_client)

        assert "inesperada" in str(exc_info.value).lower()


# Tests de integración con FastMCP (requieren servidor real)
@pytest.mark.integration
class TestAmenitiesIntegration:
    """Tests de integración con FastMCP."""

    @pytest.fixture
    async def amenities_client(self):
        """Fixture para cliente de amenidades."""
        # Este test requeriría un servidor FastMCP real
        # async with Client(transport=mcp) as client:
        #     yield client
        pytest.skip("Requiere servidor FastMCP real")

    @pytest.mark.asyncio
    async def test_basic_search(self, amenities_client):
        """Test búsqueda básica."""
        result = await amenities_client.call_tool(
            "search_amenities", {"page": 1, "size": 5}
        )

        assert result.data["total_items"] >= 0
        assert "amenities" in result.data["_embedded"]

    @pytest.mark.asyncio
    async def test_search_with_filters(self, amenities_client):
        """Test búsqueda con filtros."""
        result = await amenities_client.call_tool(
            "search_amenities", {"search": "wifi", "isPublic": 1, "isFilterable": 1}
        )

        assert result.data["total_items"] >= 0

    @pytest.mark.asyncio
    async def test_validation_error(self, amenities_client):
        """Test error de validación."""
        with pytest.raises(ToolError):
            await amenities_client.call_tool(
                "search_amenities", {"page": -1, "size": 5}  # Valor inválido
            )


# Tests de rendimiento
class TestAmenitiesPerformance:
    """Tests de rendimiento."""

    def test_large_result_handling(self):
        """Test manejo de resultados grandes."""
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 10000,
            "page": 1,
            "page_size": 100,
            "_embedded": {
                "amenities": [{"id": i, "name": f"Amenity {i}"} for i in range(100)]
            },
        }

        result = search_amenities_improved(api_client=mock_client, page=1, size=100)

        assert result["total_items"] == 10000
        assert len(result["_embedded"]["amenities"]) == 100

    def test_empty_result_handling(self):
        """Test manejo de resultados vacíos."""
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 0,
            "page": 1,
            "page_size": 10,
            "_embedded": {"amenities": []},
        }

        result = search_amenities_improved(api_client=mock_client, search="nonexistent")

        assert result["total_items"] == 0
        assert len(result["_embedded"]["amenities"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
