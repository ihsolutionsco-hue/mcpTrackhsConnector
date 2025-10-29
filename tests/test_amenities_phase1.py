"""
Tests unitarios para la función search_amenities mejorada - Fase 1.
Implementa testing completo siguiendo mejores prácticas de FastMCP.
"""

from unittest.mock import Mock, patch

import httpx
import pytest
from fastmcp.exceptions import ToolError
from pydantic import ValidationError

from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler
from src.trackhs_mcp.amenities_models import AmenitiesSearchParams


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

    def test_to_api_params(self):
        """Test conversión a parámetros de API."""
        params = AmenitiesSearchParams(
            page=2,
            size=20,
            search="wifi",
            isPublic=1,
            sortColumn=None,  # No debe incluirse
            groupId=None,  # No debe incluirse
        )

        api_params = params.to_api_params()

        expected = {"page": 2, "size": 20, "search": "wifi", "isPublic": 1}

        assert api_params == expected
        assert "sortColumn" not in api_params
        assert "groupId" not in api_params


class TestAmenitiesErrorHandler:
    """Tests para el manejador de errores."""

    def test_validation_error(self):
        """Test error de validación."""
        handler = AmenitiesErrorHandler("test_context")

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

        tool_error = handler.handle_validation_error(error, {"page": -1})

        assert isinstance(tool_error, ToolError)
        assert "Parámetros inválidos" in str(tool_error)
        assert "page" in str(tool_error)

    def test_http_401_error(self):
        """Test error HTTP 401."""
        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 401
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=response)

        tool_error = handler.handle_http_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "autenticación" in str(tool_error).lower()

    def test_http_403_error(self):
        """Test error HTTP 403."""
        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 403
        error = httpx.HTTPStatusError("Forbidden", request=Mock(), response=response)

        tool_error = handler.handle_http_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "autorización" in str(tool_error).lower()

    def test_http_404_error(self):
        """Test error HTTP 404."""
        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 404
        error = httpx.HTTPStatusError("Not Found", request=Mock(), response=response)

        tool_error = handler.handle_http_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "no encontrado" in str(tool_error).lower()

    def test_http_500_error(self):
        """Test error HTTP 500."""
        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 500
        error = httpx.HTTPStatusError(
            "Internal Server Error", request=Mock(), response=response
        )

        tool_error = handler.handle_http_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "servidor" in str(tool_error).lower()

    def test_request_error(self):
        """Test error de conexión."""
        handler = AmenitiesErrorHandler("test_context")

        error = httpx.RequestError("Connection failed")

        tool_error = handler.handle_request_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "conexión" in str(tool_error).lower()

    def test_unexpected_error(self):
        """Test error inesperado."""
        handler = AmenitiesErrorHandler("test_context")

        error = ValueError("Unexpected error")

        tool_error = handler.handle_unexpected_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "interno" in str(tool_error).lower()

    def test_handle_error_unified(self):
        """Test manejo unificado de errores."""
        handler = AmenitiesErrorHandler("test_context")

        # Test ValidationError
        validation_error = ValidationError.from_exception_data(
            "AmenitiesSearchParams",
            [
                {
                    "type": "value_error",
                    "loc": ("page",),
                    "msg": "Value must be positive",
                }
            ],
        )

        tool_error = handler.handle_error(validation_error, {"page": -1})
        assert isinstance(tool_error, ToolError)
        assert "inválidos" in str(tool_error).lower()

        # Test HTTPError
        response = Mock()
        response.status_code = 401
        http_error = httpx.HTTPStatusError(
            "Unauthorized", request=Mock(), response=response
        )

        tool_error = handler.handle_error(http_error, {"page": 1})
        assert isinstance(tool_error, ToolError)
        assert "autenticación" in str(tool_error).lower()


class TestSearchAmenitiesIntegration:
    """Tests de integración para la función search_amenities."""

    @patch("src.trackhs_mcp.server.logger")
    def test_successful_search(self, mock_logger):
        """Test búsqueda exitosa."""
        from src.trackhs_mcp.server import search_amenities

        # Mock del cliente API
        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 5,
            "page": 1,
            "page_size": 10,
            "_embedded": {
                "amenities": [{"id": 1, "name": "WiFi"}, {"id": 2, "name": "Pool"}]
            },
        }

        # Reemplazar api_client global
        with patch("src.trackhs_mcp.server.api_client", mock_client):
            result = search_amenities(page=1, size=10, search="wifi")

        assert result["total_items"] == 5
        assert len(result["_embedded"]["amenities"]) == 2

        # Verificar que se llamó con parámetros correctos
        mock_client.get.assert_called_once_with(
            "api/pms/units/amenities", {"page": 1, "size": 10, "search": "wifi"}
        )

        # Verificar logging
        mock_logger.info.assert_called()

    def test_no_api_client(self):
        """Test sin cliente API."""
        from src.trackhs_mcp.server import search_amenities

        with patch("src.trackhs_mcp.server.api_client", None):
            with pytest.raises(ToolError) as exc_info:
                search_amenities(page=1, size=10)

            assert "no disponible" in str(exc_info.value).lower()

    def test_validation_error(self):
        """Test error de validación de parámetros."""
        from src.trackhs_mcp.server import search_amenities

        with patch("src.trackhs_mcp.server.api_client", Mock()):
            with pytest.raises(ToolError) as exc_info:
                search_amenities(page=-1)  # Valor inválido

            assert "inválidos" in str(exc_info.value).lower()

    @patch("src.trackhs_mcp.server.logger")
    def test_http_error_handling(self, mock_logger):
        """Test manejo de errores HTTP."""
        from src.trackhs_mcp.server import search_amenities

        mock_client = Mock()
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=Mock(), response=Mock(status_code=401)
        )

        with patch("src.trackhs_mcp.server.api_client", mock_client):
            with pytest.raises(ToolError) as exc_info:
                search_amenities(page=1, size=10)

            assert "autenticación" in str(exc_info.value).lower()

    @patch("src.trackhs_mcp.server.logger")
    def test_unexpected_response(self, mock_logger):
        """Test respuesta inesperada."""
        from src.trackhs_mcp.server import search_amenities

        mock_client = Mock()
        mock_client.get.return_value = "not a dict"  # Respuesta inválida

        with patch("src.trackhs_mcp.server.api_client", mock_client):
            with pytest.raises(ToolError) as exc_info:
                search_amenities(page=1, size=10)

            assert "inesperada" in str(exc_info.value).lower()

    @patch("src.trackhs_mcp.server.logger")
    def test_all_parameters(self, mock_logger):
        """Test con todos los parámetros."""
        from src.trackhs_mcp.server import search_amenities

        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 1,
            "page": 1,
            "page_size": 5,
            "_embedded": {"amenities": []},
        }

        with patch("src.trackhs_mcp.server.api_client", mock_client):
            result = search_amenities(
                page=1,
                size=5,
                sortColumn="name",
                sortDirection="asc",
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

        # Verificar que se llamó con todos los parámetros
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "api/pms/units/amenities"

        params = call_args[0][1]
        assert params["page"] == 1
        assert params["size"] == 5
        assert params["sortColumn"] == "name"
        assert params["sortDirection"] == "asc"
        assert params["search"] == "wifi"
        assert params["groupId"] == 1
        assert params["isPublic"] == 1
        assert params["publicSearchable"] == 1
        assert params["isFilterable"] == 1
        assert params["homeawayType"] == "pool%"
        assert params["airbnbType"] == "ac"
        assert params["tripadvisorType"] == "wifi%"
        assert params["marriottType"] == "pool%"


class TestAmenitiesPerformance:
    """Tests de rendimiento."""

    @patch("src.trackhs_mcp.server.logger")
    def test_large_result_handling(self, mock_logger):
        """Test manejo de resultados grandes."""
        from src.trackhs_mcp.server import search_amenities

        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 10000,
            "page": 1,
            "page_size": 100,
            "_embedded": {
                "amenities": [{"id": i, "name": f"Amenity {i}"} for i in range(100)]
            },
        }

        with patch("src.trackhs_mcp.server.api_client", mock_client):
            result = search_amenities(page=1, size=100)

        assert result["total_items"] == 10000
        assert len(result["_embedded"]["amenities"]) == 100

    @patch("src.trackhs_mcp.server.logger")
    def test_empty_result_handling(self, mock_logger):
        """Test manejo de resultados vacíos."""
        from src.trackhs_mcp.server import search_amenities

        mock_client = Mock()
        mock_client.get.return_value = {
            "total_items": 0,
            "page": 1,
            "page_size": 10,
            "_embedded": {"amenities": []},
        }

        with patch("src.trackhs_mcp.server.api_client", mock_client):
            result = search_amenities(search="nonexistent")

        assert result["total_items"] == 0
        assert len(result["_embedded"]["amenities"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
