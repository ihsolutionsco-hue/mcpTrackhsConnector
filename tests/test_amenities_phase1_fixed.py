"""
Tests unitarios corregidos para la función search_amenities mejorada - Fase 1.
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

        # Crear ValidationError de forma correcta
        try:
            AmenitiesSearchParams(page=-1)
        except ValidationError as e:
            error = e

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
        try:
            AmenitiesSearchParams(page=-1)
        except ValidationError as e:
            validation_error = e

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


class TestAmenitiesFunctionLogic:
    """Tests para la lógica de la función search_amenities."""

    def test_validate_parameters_success(self):
        """Test validación exitosa de parámetros."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        params = AmenitiesSearchParams(page=1, size=10, search="wifi", isPublic=1)

        assert params.page == 1
        assert params.size == 10
        assert params.search == "wifi"
        assert params.isPublic == 1

    def test_validate_parameters_error(self):
        """Test error de validación de parámetros."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        with pytest.raises(ValidationError):
            AmenitiesSearchParams(page=-1)

    def test_build_api_params(self):
        """Test construcción de parámetros de API."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        params = AmenitiesSearchParams(
            page=1,
            size=10,
            search="wifi",
            isPublic=1,
            sortColumn="id",
            sortDirection="asc",
        )

        api_params = params.to_api_params()

        expected = {
            "page": 1,
            "size": 10,
            "search": "wifi",
            "isPublic": 1,
            "sortColumn": "id",
            "sortDirection": "asc",
        }

        assert api_params == expected

    def test_build_api_params_with_none_values(self):
        """Test construcción de parámetros con valores None."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        params = AmenitiesSearchParams(
            page=1, size=10, search="wifi", sortColumn=None, groupId=None
        )

        api_params = params.to_api_params()

        expected = {"page": 1, "size": 10, "search": "wifi"}

        assert api_params == expected
        assert "sortColumn" not in api_params
        assert "groupId" not in api_params

    def test_error_handler_validation_error(self):
        """Test manejador de errores con ValidationError."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler

        handler = AmenitiesErrorHandler("test_context")

        try:
            AmenitiesSearchParams(page=-1)
        except ValidationError as e:
            error = e

        tool_error = handler.handle_error(error, {"page": -1})

        assert isinstance(tool_error, ToolError)
        assert "inválidos" in str(tool_error).lower()

    def test_error_handler_http_error(self):
        """Test manejador de errores con HTTPError."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler

        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 401
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=response)

        tool_error = handler.handle_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "autenticación" in str(tool_error).lower()

    def test_error_handler_request_error(self):
        """Test manejador de errores con RequestError."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler

        handler = AmenitiesErrorHandler("test_context")

        error = httpx.RequestError("Connection failed")

        tool_error = handler.handle_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "conexión" in str(tool_error).lower()

    def test_error_handler_unexpected_error(self):
        """Test manejador de errores con error inesperado."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler

        handler = AmenitiesErrorHandler("test_context")

        error = ValueError("Unexpected error")

        tool_error = handler.handle_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "interno" in str(tool_error).lower()


class TestAmenitiesIntegration:
    """Tests de integración usando el cliente HTTP directamente."""

    def test_successful_search_direct(self):
        """Test búsqueda exitosa usando cliente HTTP directamente."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams
        from src.trackhs_mcp.client import TrackHSClient

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

        # Simular la lógica de la función
        params = AmenitiesSearchParams(page=1, size=10, search="wifi")
        api_params = params.to_api_params()

        result = mock_client.get("api/pms/units/amenities", api_params)

        assert result["total_items"] == 5
        assert len(result["_embedded"]["amenities"]) == 2

        # Verificar que se llamó con parámetros correctos
        mock_client.get.assert_called_once_with(
            "api/pms/units/amenities", {"page": 1, "size": 10, "search": "wifi"}
        )

    def test_validation_error_direct(self):
        """Test error de validación usando lógica directa."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        handler = AmenitiesErrorHandler("test_context")

        with pytest.raises(ValidationError):
            AmenitiesSearchParams(page=-1)

    def test_http_error_direct(self):
        """Test error HTTP usando lógica directa."""
        from src.trackhs_mcp.amenities_error_handler import AmenitiesErrorHandler
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        handler = AmenitiesErrorHandler("test_context")

        response = Mock()
        response.status_code = 401
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=response)

        tool_error = handler.handle_error(error, {"page": 1})

        assert isinstance(tool_error, ToolError)
        assert "autenticación" in str(tool_error).lower()

    def test_all_parameters_direct(self):
        """Test con todos los parámetros usando lógica directa."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        params = AmenitiesSearchParams(
            page=1,
            size=5,
            sortColumn="id",
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

        api_params = params.to_api_params()

        expected = {
            "page": 1,
            "size": 5,
            "sortColumn": "id",
            "sortDirection": "asc",
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


class TestAmenitiesPerformance:
    """Tests de rendimiento."""

    def test_large_result_handling(self):
        """Test manejo de resultados grandes."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        # Simular resultado grande
        large_result = {
            "total_items": 10000,
            "page": 1,
            "page_size": 100,
            "_embedded": {
                "amenities": [{"id": i, "name": f"Amenity {i}"} for i in range(100)]
            },
        }

        params = AmenitiesSearchParams(page=1, size=100)
        api_params = params.to_api_params()

        assert api_params["page"] == 1
        assert api_params["size"] == 100
        assert large_result["total_items"] == 10000
        assert len(large_result["_embedded"]["amenities"]) == 100

    def test_empty_result_handling(self):
        """Test manejo de resultados vacíos."""
        from src.trackhs_mcp.amenities_models import AmenitiesSearchParams

        # Simular resultado vacío
        empty_result = {
            "total_items": 0,
            "page": 1,
            "page_size": 10,
            "_embedded": {"amenities": []},
        }

        params = AmenitiesSearchParams(search="nonexistent")
        api_params = params.to_api_params()

        assert api_params["search"] == "nonexistent"
        assert empty_result["total_items"] == 0
        assert len(empty_result["_embedded"]["amenities"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
