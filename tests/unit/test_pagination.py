"""
Tests unitarios para utilidades de paginación
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.trackhs_mcp.core.pagination import (
    PageInfo,
    PaginationConfig,
    PaginationMode,
    PaginationResult,
    PaginationUtility,
)


class TestPaginationMode:
    """Tests para PaginationMode"""

    @pytest.mark.unit
    def test_pagination_mode_values(self):
        """Test valores de PaginationMode"""
        assert PaginationMode.STANDARD.value == "standard"
        assert PaginationMode.SCROLL.value == "scroll"
        assert PaginationMode.CURSOR.value == "cursor"


class TestPaginationConfig:
    """Tests para PaginationConfig"""

    @pytest.mark.unit
    def test_pagination_config_defaults(self):
        """Test configuración de paginación con valores por defecto"""
        config = PaginationConfig()

        assert config.mode == PaginationMode.STANDARD
        assert config.max_page_size == 1000
        assert config.max_total_results == 10000
        assert config.scroll_timeout == "1m"
        assert config.enable_auto_scroll is True
        assert config.preserve_order is True

    @pytest.mark.unit
    def test_pagination_config_custom(self):
        """Test configuración de paginación personalizada"""
        config = PaginationConfig(
            mode=PaginationMode.SCROLL,
            max_page_size=500,
            max_total_results=5000,
            scroll_timeout="2m",
            enable_auto_scroll=False,
            preserve_order=False,
        )

        assert config.mode == PaginationMode.SCROLL
        assert config.max_page_size == 500
        assert config.max_total_results == 5000
        assert config.scroll_timeout == "2m"
        assert config.enable_auto_scroll is False
        assert config.preserve_order is False


class TestPageInfo:
    """Tests para PageInfo"""

    @pytest.mark.unit
    def test_page_info_creation(self):
        """Test creación de PageInfo"""
        page_info = PageInfo(
            page=2,
            size=10,
            total_items=50,
            total_pages=5,
            has_next=True,
            has_previous=True,
        )

        assert page_info.page == 2
        assert page_info.size == 10
        assert page_info.total_pages == 5
        assert page_info.total_items == 50
        assert page_info.has_next is True
        assert page_info.has_previous is True


class TestPaginationResult:
    """Tests para PaginationResult"""

    @pytest.mark.unit
    def test_pagination_result_creation(self):
        """Test creación de PaginationResult"""
        page_info = PageInfo(1, 10, 1, 10, False, False)
        data = [{"id": 1}, {"id": 2}]
        links = {"self": {"hre": "/test"}}

        result = PaginationResult(
            data=data, page_info=page_info, links=links, scroll_id="scroll123"
        )

        assert result.data == data
        assert result.page_info == page_info
        assert result.links == links
        assert result.scroll_id == "scroll123"


class TestPaginationUtility:
    """Tests para PaginationUtility"""

    @pytest.fixture
    def pagination_utility(self):
        """Crear PaginationUtility para testing"""
        return PaginationUtility()

    @pytest.fixture
    def mock_api_client(self):
        """Mock del API client"""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.mark.unit
    def test_pagination_utility_init(self, pagination_utility):
        """Test inicialización de PaginationUtility"""
        assert pagination_utility.config is not None
        assert pagination_utility._scroll_cache == {}

    @pytest.mark.unit
    def test_pagination_utility_init_with_config(self):
        """Test inicialización con configuración personalizada"""
        config = PaginationConfig(max_page_size=500)
        utility = PaginationUtility(config)

        assert utility.config == config

    @pytest.mark.unit
    def test_validate_pagination_params_valid(self, pagination_utility):
        """Test validación de parámetros válidos"""
        params = {"page": 1, "size": 10}

        # No debe lanzar excepción
        pagination_utility.validate_pagination_params(params)

    @pytest.mark.unit
    def test_validate_pagination_params_invalid_page(self, pagination_utility):
        """Test validación con página inválida"""
        params = {"page": 0, "size": 10}

        with pytest.raises(ValueError, match="Page must be >= 1"):
            pagination_utility.validate_pagination_params(params)

    @pytest.mark.unit
    def test_validate_pagination_params_invalid_size(self, pagination_utility):
        """Test validación con tamaño inválido"""
        params = {"page": 1, "size": 0}

        with pytest.raises(ValueError, match="Size must be >= 1"):
            pagination_utility.validate_pagination_params(params)

    @pytest.mark.unit
    def test_validate_pagination_params_size_exceeds_max(self, pagination_utility):
        """Test validación con tamaño que excede el máximo"""
        params = {"page": 1, "size": 2000}  # Mayor que max_page_size (1000)

        with pytest.raises(ValueError, match="Size exceeds maximum"):
            pagination_utility.validate_pagination_params(params)

    @pytest.mark.unit
    def test_calculate_page_info(self, pagination_utility):
        """Test cálculo de información de página"""
        response_data = {"page": 2, "page_size": 10, "total_items": 50}

        page_info = pagination_utility.calculate_page_info(response_data)

        assert page_info.current_page == 2
        assert page_info.page_size == 10
        assert page_info.total_pages == 5
        assert page_info.total_items == 50
        assert page_info.has_next is True
        assert page_info.has_previous is True

    @pytest.mark.unit
    def test_calculate_page_info_last_page(self, pagination_utility):
        """Test cálculo de información de página para la última página"""
        response_data = {"page": 5, "page_size": 10, "total_items": 50}

        page_info = pagination_utility.calculate_page_info(response_data)

        assert page_info.current_page == 5
        assert page_info.has_next is False
        assert page_info.has_previous is True

    @pytest.mark.unit
    def test_calculate_page_info_first_page(self, pagination_utility):
        """Test cálculo de información de página para la primera página"""
        response_data = {"page": 1, "page_size": 10, "total_items": 50}

        page_info = pagination_utility.calculate_page_info(response_data)

        assert page_info.current_page == 1
        assert page_info.has_next is True
        assert page_info.has_previous is False

    @pytest.mark.unit
    def test_generate_links(self, pagination_utility):
        """Test generación de enlaces"""
        page_info = PageInfo(2, 10, 5, 50, True, True)
        base_url = "/test"

        links = pagination_utility.generate_links(page_info, base_url)

        assert "sel" in links
        assert "first" in links
        assert "last" in links
        assert "next" in links
        assert "prev" in links

        assert links["sel"]["hre"] == "/test?page=2&size=10"
        assert links["first"]["hre"] == "/test?page=1&size=10"
        assert links["last"]["hre"] == "/test?page=5&size=10"
        assert links["next"]["hre"] == "/test?page=3&size=10"
        assert links["prev"]["hre"] == "/test?page=1&size=10"

    @pytest.mark.unit
    def test_generate_links_first_page(self, pagination_utility):
        """Test generación de enlaces para primera página"""
        page_info = PageInfo(1, 10, 5, 50, True, False)
        base_url = "/test"

        links = pagination_utility.generate_links(page_info, base_url)

        assert "prev" not in links  # No debe tener enlace previo
        assert "next" in links

    @pytest.mark.unit
    def test_generate_links_last_page(self, pagination_utility):
        """Test generación de enlaces para última página"""
        page_info = PageInfo(5, 10, 5, 50, False, True)
        base_url = "/test"

        links = pagination_utility.generate_links(page_info, base_url)

        assert "next" not in links  # No debe tener enlace siguiente
        assert "prev" in links

    @pytest.mark.unit
    def test_process_scroll_response(self, pagination_utility):
        """Test procesamiento de respuesta de scroll"""
        response_data = {
            "_embedded": {"reservations": [{"id": 1}, {"id": 2}]},
            "_links": {"next": {"hre": "/next"}},
            "scroll_id": "scroll123",
        }

        result = pagination_utility.process_scroll_response(response_data, "/test")

        assert len(result.data) == 2
        assert result.scroll_id == "scroll123"
        assert "next" in result.links

    @pytest.mark.unit
    def test_process_standard_response(self, pagination_utility):
        """Test procesamiento de respuesta estándar"""
        response_data = {
            "_embedded": {"reservations": [{"id": 1}, {"id": 2}]},
            "page": 1,
            "page_size": 10,
            "total_items": 20,
        }

        result = pagination_utility.process_standard_response(response_data, "/test")

        assert len(result.data) == 2
        assert result.page_info.current_page == 1
        assert result.page_info.page_size == 10
        assert result.page_info.total_items == 20

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_paginate_async_standard_mode(
        self, pagination_utility, mock_api_client
    ):
        """Test paginación asíncrona en modo estándar"""
        mock_api_client.get.return_value = {
            "_embedded": {"reservations": [{"id": 1}]},
            "page": 1,
            "page_size": 10,
            "total_items": 10,
        }

        results = []
        async for result in pagination_utility.paginate_async(
            mock_api_client, "/test", {}
        ):
            results.append(result)

        assert len(results) == 1
        assert len(results[0].data) == 1
        mock_api_client.get.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_paginate_async_scroll_mode(
        self, pagination_utility, mock_api_client
    ):
        """Test paginación asíncrona en modo scroll"""
        # Configurar para modo scroll
        pagination_utility.config.mode = PaginationMode.SCROLL

        mock_api_client.get.return_value = {
            "_embedded": {"reservations": [{"id": 1}]},
            "_links": {"next": {"hre": "/next"}},
            "scroll_id": "scroll123",
        }

        results = []
        async for result in pagination_utility.paginate_async(
            mock_api_client, "/test", {}
        ):
            results.append(result)
            break  # Solo una iteración para el test

        assert len(results) == 1
        assert results[0].scroll_id == "scroll123"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_all_pages(self, pagination_utility, mock_api_client):
        """Test obtención de todas las páginas"""
        # Crear resultados de paginación simulados
        from src.trackhs_mcp.core.pagination import PaginationResult

        result1 = PaginationResult(
            data=[{"id": 1}, {"id": 2}],
            page=1,
            page_size=2,
            total_items=4,
            has_next=True,
        )
        result2 = PaginationResult(
            data=[{"id": 3}, {"id": 4}],
            page=2,
            page_size=2,
            total_items=4,
            has_next=False,
        )

        results = [result1, result2]
        all_data = pagination_utility.get_all_pages(results)

        assert len(all_data) == 4
        assert all_data[0]["id"] == 1
        assert all_data[3]["id"] == 4

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_summary(self, pagination_utility, mock_api_client):
        """Test obtención de resumen"""
        # Crear resultados de paginación simulados
        from src.trackhs_mcp.core.pagination import PaginationResult

        result1 = PaginationResult(
            data=[{"id": 1}, {"id": 2}],
            page=1,
            page_size=2,
            total_items=4,
            has_next=True,
        )
        result2 = PaginationResult(
            data=[{"id": 3}, {"id": 4}],
            page=2,
            page_size=2,
            total_items=4,
            has_next=False,
        )

        results = [result1, result2]
        summary = pagination_utility.get_summary(results)

        assert "total_items" in summary
        assert "total_pages" in summary
        assert "pages_processed" in summary
        assert summary["total_items"] == 4
        assert summary["total_pages"] == 2
