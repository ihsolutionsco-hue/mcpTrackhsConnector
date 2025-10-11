"""
Tests unitarios para tipos y modelos Pydantic
"""

import pytest
from pydantic import ValidationError

from src.trackhs_mcp.domain.value_objects.config import TrackHSConfig
from src.trackhs_mcp.domain.value_objects.request import (
    PaginationParams,
    RequestOptions,
    SearchParams,
    TrackHSResponse,
)
from src.trackhs_mcp.infrastructure.utils.error_handling import ApiError


class TestTrackHSConfig:
    """Tests para TrackHSConfig"""

    @pytest.mark.unit
    def test_valid_config(self):
        """Test configuración válida"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="test_user",
            password="test_password",
            timeout=30,
        )

        assert config.base_url == "https://api.trackhs.com/api"
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.timeout == 30

    @pytest.mark.unit
    def test_config_with_defaults(self):
        """Test configuración con valores por defecto"""
        config = TrackHSConfig(
            base_url="https://api.trackhs.com/api",
            username="test_user",
            password="test_password",
        )

        assert config.timeout == 30  # Valor por defecto

    @pytest.mark.unit
    def test_config_missing_required_fields(self):
        """Test configuración con campos requeridos faltantes"""
        with pytest.raises(ValidationError):
            TrackHSConfig(
                base_url="https://api.trackhs.com/api",
                username="test_user",
                # password faltante
            )

    @pytest.mark.unit
    def test_config_invalid_types(self):
        """Test configuración con tipos inválidos"""
        with pytest.raises(ValidationError):
            TrackHSConfig(
                base_url="https://api.trackhs.com/api",
                username="test_user",
                password="test_password",
                timeout="invalid",  # Debe ser int
            )


class TestRequestOptions:
    """Tests para RequestOptions"""

    @pytest.mark.unit
    def test_valid_request_options(self):
        """Test opciones de petición válidas"""
        options = RequestOptions(
            method="POST",
            headers={"Content-Type": "application/json"},
            body='{"key": "value"}',
        )

        assert options.method == "POST"
        assert options.headers == {"Content-Type": "application/json"}
        assert options.body == '{"key": "value"}'

    @pytest.mark.unit
    def test_request_options_with_defaults(self):
        """Test opciones de petición con valores por defecto"""
        options = RequestOptions()

        assert options.method == "GET"
        assert options.headers is None
        assert options.body is None

    @pytest.mark.unit
    def test_request_options_invalid_method(self):
        """Test opciones de petición con método inválido"""
        with pytest.raises(ValidationError):
            RequestOptions(method="INVALID")


class TestApiError:
    """Tests para ApiError"""

    @pytest.mark.unit
    def test_api_error_creation(self):
        """Test creación de ApiError"""
        error = ApiError("Test error", 404, "Not Found")

        assert error.message == "Test error"
        assert error.status == 404
        assert error.status_text == "Not Found"
        assert str(error) == "Test error"

    @pytest.mark.unit
    def test_api_error_without_status(self):
        """Test ApiError sin status"""
        error = ApiError("Test error")

        assert error.message == "Test error"
        assert error.status is None
        assert error.status_text is None

    @pytest.mark.unit
    def test_api_error_inheritance(self):
        """Test que ApiError hereda de Exception"""
        error = ApiError("Test error")
        assert isinstance(error, Exception)


class TestTrackHSResponse:
    """Tests para TrackHSResponse"""

    @pytest.mark.unit
    def test_valid_response(self):
        """Test respuesta válida"""
        response = TrackHSResponse(
            data={"key": "value"}, success=True, message="Success"
        )

        assert response.data == {"key": "value"}
        assert response.success == True
        assert response.message == "Success"

    @pytest.mark.unit
    def test_response_with_defaults(self):
        """Test respuesta con valores por defecto"""
        response = TrackHSResponse(data={"key": "value"}, success=True)

        assert response.data == {"key": "value"}
        assert response.success == True
        assert response.message is None

    @pytest.mark.unit
    def test_response_invalid_status(self):
        """Test respuesta con status inválido"""
        with pytest.raises(ValidationError):
            TrackHSResponse(data={"key": "value"}, status="invalid")  # Debe ser int


class TestPaginationParams:
    """Tests para PaginationParams"""

    @pytest.mark.unit
    def test_valid_pagination_params(self):
        """Test parámetros de paginación válidos"""
        params = PaginationParams(
            page=1, size=10, sort_column="name", sort_direction="asc"
        )

        assert params.page == 1
        assert params.size == 10
        assert params.sort_column == "name"
        assert params.sort_direction == "asc"

    @pytest.mark.unit
    def test_pagination_params_with_defaults(self):
        """Test parámetros de paginación con valores por defecto"""
        params = PaginationParams()

        assert params.page == 1
        assert params.size == 10
        assert params.sort_column == "id"
        assert params.sort_direction == "asc"

    @pytest.mark.unit
    def test_pagination_params_invalid_page(self):
        """Test parámetros de paginación con página inválida"""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)  # Debe ser >= 1

    @pytest.mark.unit
    def test_pagination_params_invalid_size(self):
        """Test parámetros de paginación con tamaño inválido"""
        with pytest.raises(ValidationError):
            PaginationParams(size=0)  # Debe ser >= 1

    @pytest.mark.unit
    def test_pagination_params_invalid_sort_direction(self):
        """Test parámetros de paginación con dirección de ordenamiento inválida"""
        with pytest.raises(ValidationError):
            PaginationParams(sort_direction="invalid")  # Debe ser "asc" o "desc"


class TestSearchParams:
    """Tests para SearchParams"""

    @pytest.mark.unit
    def test_valid_search_params(self):
        """Test parámetros de búsqueda válidos"""
        params = SearchParams(search="test query", tags="tag1,tag2", node_id=[1, 2, 3])

        assert params.search == "test query"
        assert params.tags == "tag1,tag2"
        assert params.node_id == [1, 2, 3]

    @pytest.mark.unit
    def test_search_params_with_defaults(self):
        """Test parámetros de búsqueda con valores por defecto"""
        params = SearchParams()

        assert params.search is None
        assert params.tags is None
        assert params.node_id is None

    @pytest.mark.unit
    def test_search_params_single_node_id(self):
        """Test parámetros de búsqueda con node_id único"""
        params = SearchParams(node_id=1)
        assert params.node_id == 1

    @pytest.mark.unit
    def test_search_params_list_node_id(self):
        """Test parámetros de búsqueda con node_id como lista"""
        params = SearchParams(node_id=[1, 2, 3])
        assert params.node_id == [1, 2, 3]
