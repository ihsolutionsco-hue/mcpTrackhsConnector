"""
Tests unitarios para pagination utility
Implementando el patrón oficial de FastMCP para testing
"""

from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from trackhs_mcp.infrastructure.utils.pagination import (
    PageInfo,
    PaginationConfig,
    PaginationMode,
    PaginationResult,
    PaginationUtility,
)


class TestPaginationUtility:
    """Tests para PaginationUtility"""

    @pytest.fixture
    def default_config(self):
        """Configuración por defecto para testing"""
        return PaginationConfig()

    @pytest.fixture
    def custom_config(self):
        """Configuración personalizada para testing"""
        return PaginationConfig(
            max_page_size=500,
            max_total_results=5000,
            scroll_timeout="5m",
            enable_auto_scroll=False,
            preserve_order=False,
        )

    @pytest.fixture
    def pagination_utility(self, default_config):
        """Instancia de PaginationUtility con configuración por defecto"""
        return PaginationUtility(default_config)

    @pytest.fixture
    def custom_pagination_utility(self, custom_config):
        """Instancia de PaginationUtility con configuración personalizada"""
        return PaginationUtility(custom_config)

    def test_pagination_utility_initialization_default(self):
        """Test inicialización con configuración por defecto"""
        # Act
        utility = PaginationUtility()

        # Assert
        assert utility.config.mode == PaginationMode.STANDARD
        assert utility.config.max_page_size == 1000
        assert utility.config.max_total_results == 10000
        assert utility.config.scroll_timeout == "1m"
        assert utility.config.enable_auto_scroll == True
        assert utility.config.preserve_order == True
        assert utility._scroll_cache == {}

    def test_pagination_utility_initialization_custom(self, custom_config):
        """Test inicialización con configuración personalizada"""
        # Act
        utility = PaginationUtility(custom_config)

        # Assert
        assert utility.config == custom_config
        assert utility.config.max_page_size == 500
        assert utility.config.max_total_results == 5000
        assert utility.config.scroll_timeout == "5m"
        assert utility.config.enable_auto_scroll == False
        assert utility.config.preserve_order == False

    def test_validate_pagination_params_valid(self, pagination_utility):
        """Test validación de parámetros válidos"""
        # Act
        result = pagination_utility.validate_pagination_params(page=2, size=10)

        # Assert
        assert result["page"] == 2
        assert result["size"] == 10
        assert result["offset"] == 10

    def test_validate_pagination_params_page_too_small(self, pagination_utility):
        """Test validación con página muy pequeña"""
        # Act
        result = pagination_utility.validate_pagination_params(page=0, size=10)

        # Assert
        assert result["page"] == 1  # Se corrige automáticamente
        assert result["size"] == 10
        assert result["offset"] == 0

    def test_validate_pagination_params_size_too_small(self, pagination_utility):
        """Test validación con tamaño muy pequeño"""
        # Act
        result = pagination_utility.validate_pagination_params(page=1, size=0)

        # Assert
        assert result["page"] == 1
        assert result["size"] == 1  # Se corrige automáticamente
        assert result["offset"] == 0

    def test_validate_pagination_params_size_too_large(self, pagination_utility):
        """Test validación con tamaño muy grande"""
        # Act
        result = pagination_utility.validate_pagination_params(page=1, size=2000)

        # Assert
        assert result["page"] == 1
        assert result["size"] == 1000  # Se limita al máximo
        assert result["offset"] == 0

    def test_validate_pagination_params_exceeds_max_total(self, pagination_utility):
        """Test validación que excede el total máximo de resultados"""
        # Act & Assert
        with pytest.raises(ValueError, match="Total de resultados solicitados"):
            pagination_utility.validate_pagination_params(page=1000, size=20)

    def test_validate_pagination_params_custom_limits(self, custom_pagination_utility):
        """Test validación con límites personalizados"""
        # Act
        result = custom_pagination_utility.validate_pagination_params(page=1, size=600)

        # Assert
        assert result["page"] == 1
        assert result["size"] == 500  # Se limita al máximo personalizado
        assert result["offset"] == 0

    def test_calculate_page_info_basic(self, pagination_utility):
        """Test cálculo de información de página básica"""
        # Act
        page_info = pagination_utility.calculate_page_info(
            page=2, size=10, total_items=25
        )

        # Assert
        assert page_info.page == 2
        assert page_info.size == 10
        assert page_info.total_items == 25
        assert page_info.total_pages == 3
        assert page_info.has_next == True
        assert page_info.has_previous == True
        assert page_info.next_page == 3
        assert page_info.previous_page == 1

    def test_calculate_page_info_first_page(self, pagination_utility):
        """Test cálculo de información de primera página"""
        # Act
        page_info = pagination_utility.calculate_page_info(
            page=1, size=10, total_items=25
        )

        # Assert
        assert page_info.page == 1
        assert page_info.has_next == True
        assert page_info.has_previous == False
        assert page_info.next_page == 2
        assert page_info.previous_page is None

    def test_calculate_page_info_last_page(self, pagination_utility):
        """Test cálculo de información de última página"""
        # Act
        page_info = pagination_utility.calculate_page_info(
            page=3, size=10, total_items=25
        )

        # Assert
        assert page_info.page == 3
        assert page_info.has_next == False
        assert page_info.has_previous == True
        assert page_info.next_page is None
        assert page_info.previous_page == 2

    def test_calculate_page_info_no_items(self, pagination_utility):
        """Test cálculo de información sin elementos"""
        # Act
        page_info = pagination_utility.calculate_page_info(
            page=1, size=10, total_items=0
        )

        # Assert
        assert page_info.page == 1
        assert page_info.total_items == 0
        assert page_info.total_pages == 0
        assert page_info.has_next == False
        assert page_info.has_previous == False
        assert page_info.next_page is None
        assert page_info.previous_page is None

    def test_calculate_page_info_exact_fit(self, pagination_utility):
        """Test cálculo de información con ajuste exacto"""
        # Act
        page_info = pagination_utility.calculate_page_info(
            page=2, size=10, total_items=20
        )

        # Assert
        assert page_info.page == 2
        assert page_info.total_pages == 2
        assert page_info.has_next == False
        assert page_info.has_previous == True

    def test_generate_links_basic(self, pagination_utility):
        """Test generación de enlaces básicos"""
        # Arrange
        page_info = PageInfo(
            page=2,
            size=10,
            total_items=25,
            total_pages=3,
            has_next=True,
            has_previous=True,
            next_page=3,
            previous_page=1,
        )
        base_url = "https://api.example.com/reservations"
        query_params = {"search": "test", "status": "active"}

        # Act
        links = pagination_utility.generate_links(base_url, page_info, query_params)

        # Assert
        assert "self" in links
        assert "first" in links
        assert "last" in links
        assert "next" in links
        assert "prev" in links
        assert "page=2" in links["self"]
        assert "page=1" in links["first"]
        assert "page=3" in links["last"]
        assert "page=3" in links["next"]
        assert "page=1" in links["prev"]

    def test_generate_links_first_page(self, pagination_utility):
        """Test generación de enlaces para primera página"""
        # Arrange
        page_info = PageInfo(
            page=1,
            size=10,
            total_items=25,
            total_pages=3,
            has_next=True,
            has_previous=False,
            next_page=2,
            previous_page=None,
        )
        base_url = "https://api.example.com/reservations"
        query_params = {}

        # Act
        links = pagination_utility.generate_links(base_url, page_info, query_params)

        # Assert
        assert "self" in links
        assert "first" in links
        assert "last" in links
        assert "next" in links
        assert "prev" not in links  # No hay página anterior

    def test_generate_links_last_page(self, pagination_utility):
        """Test generación de enlaces para última página"""
        # Arrange
        page_info = PageInfo(
            page=3,
            size=10,
            total_items=25,
            total_pages=3,
            has_next=False,
            has_previous=True,
            next_page=None,
            previous_page=2,
        )
        base_url = "https://api.example.com/reservations"
        query_params = {"filter": "active"}

        # Act
        links = pagination_utility.generate_links(base_url, page_info, query_params)

        # Assert
        assert "self" in links
        assert "first" in links
        assert "last" in links
        assert "next" not in links  # No hay página siguiente
        assert "prev" in links

    def test_generate_links_single_page(self, pagination_utility):
        """Test generación de enlaces para página única"""
        # Arrange
        page_info = PageInfo(
            page=1,
            size=10,
            total_items=5,
            total_pages=1,
            has_next=False,
            has_previous=False,
            next_page=None,
            previous_page=None,
        )
        base_url = "https://api.example.com/reservations"
        query_params = {}

        # Act
        links = pagination_utility.generate_links(base_url, page_info, query_params)

        # Assert
        assert "self" in links
        assert "first" in links
        assert "last" in links
        assert "next" not in links
        assert "prev" not in links

    def test_process_scroll_response_basic(self, pagination_utility):
        """Test procesamiento de respuesta de scroll básica"""
        # Arrange
        response = {
            "_embedded": {
                "reservations": [
                    {"id": 1, "name": "Reservation 1"},
                    {"id": 2, "name": "Reservation 2"},
                ]
            },
            "total_items": 100,
            "_links": {
                "self": {"href": "/api/reservations"},
                "next": {"href": "/api/reservations?scroll_id=abc123"},
            },
            "_scroll_id": "abc123",
        }

        # Act
        result = pagination_utility.process_scroll_response(response)

        # Assert
        assert len(result.data) == 2
        assert result.data[0]["id"] == 1
        assert result.data[1]["id"] == 2
        assert result.page_info.page == 1
        assert result.page_info.size == 2
        assert result.page_info.total_items == 100
        assert result.page_info.scroll_id == "abc123"
        assert result.scroll_id == "abc123"
        assert result.metadata["scroll_mode"] == True

    def test_process_scroll_response_no_next(self, pagination_utility):
        """Test procesamiento de respuesta de scroll sin siguiente página"""
        # Arrange
        response = {
            "_embedded": {"reservations": [{"id": 1, "name": "Reservation 1"}]},
            "total_items": 1,
            "_links": {"self": {"href": "/api/reservations"}},
        }

        # Act
        result = pagination_utility.process_scroll_response(response)

        # Assert
        assert len(result.data) == 1
        assert result.page_info.has_next == False
        assert result.page_info.scroll_id is None
        assert result.scroll_id is None

    def test_process_scroll_response_empty(self, pagination_utility):
        """Test procesamiento de respuesta de scroll vacía"""
        # Arrange
        response = {
            "_embedded": {"reservations": []},
            "total_items": 0,
            "_links": {"self": {"href": "/api/reservations"}},
        }

        # Act
        result = pagination_utility.process_scroll_response(response)

        # Assert
        assert len(result.data) == 0
        assert result.page_info.total_items == 0
        assert result.page_info.has_next == False
        assert result.page_info.has_previous == False

    def test_process_standard_response_basic(self, pagination_utility):
        """Test procesamiento de respuesta estándar básica"""
        # Arrange
        response = {
            "_embedded": {
                "reservations": [
                    {"id": 1, "name": "Reservation 1"},
                    {"id": 2, "name": "Reservation 2"},
                ]
            },
            "page": 2,
            "page_count": 5,
            "page_size": 10,
            "total_items": 50,
            "_links": {
                "self": {"href": "/api/reservations?page=2"},
                "first": {"href": "/api/reservations?page=1"},
                "last": {"href": "/api/reservations?page=5"},
                "next": {"href": "/api/reservations?page=3"},
                "prev": {"href": "/api/reservations?page=1"},
            },
        }

        # Act
        result = pagination_utility.process_standard_response(response, page=2, size=10)

        # Assert
        assert len(result.data) == 2
        assert result.data[0]["id"] == 1
        assert result.data[1]["id"] == 2
        assert result.page_info.page == 2
        assert result.page_info.size == 10
        assert result.page_info.total_items == 50
        assert result.page_info.total_pages == 5
        assert result.page_info.has_next == True
        assert result.page_info.has_previous == True
        assert result.scroll_id is None
        assert result.metadata["scroll_mode"] == False

    def test_process_standard_response_last_page(self, pagination_utility):
        """Test procesamiento de respuesta estándar última página"""
        # Arrange
        response = {
            "_embedded": {
                "reservations": [
                    {"id": 49, "name": "Reservation 49"},
                    {"id": 50, "name": "Reservation 50"},
                ]
            },
            "page": 5,
            "page_count": 5,
            "page_size": 10,
            "total_items": 50,
            "_links": {
                "self": {"href": "/api/reservations?page=5"},
                "first": {"href": "/api/reservations?page=1"},
                "last": {"href": "/api/reservations?page=5"},
                "prev": {"href": "/api/reservations?page=4"},
            },
        }

        # Act
        result = pagination_utility.process_standard_response(response, page=5, size=10)

        # Assert
        assert len(result.data) == 2
        assert result.page_info.page == 5
        assert result.page_info.has_next == False
        assert result.page_info.has_previous == True

    def test_process_standard_response_empty(self, pagination_utility):
        """Test procesamiento de respuesta estándar vacía"""
        # Arrange
        response = {
            "_embedded": {"reservations": []},
            "page": 1,
            "page_count": 0,
            "page_size": 10,
            "total_items": 0,
            "_links": {
                "self": {"href": "/api/reservations?page=1"},
                "first": {"href": "/api/reservations?page=1"},
                "last": {"href": "/api/reservations?page=1"},
            },
        }

        # Act
        result = pagination_utility.process_standard_response(response, page=1, size=10)

        # Assert
        assert len(result.data) == 0
        assert result.page_info.total_items == 0
        assert result.page_info.total_pages == 0
        assert result.page_info.has_next == False
        assert result.page_info.has_previous == False

    def test_pagination_mode_enum(self):
        """Test enum PaginationMode"""
        # Assert
        assert PaginationMode.STANDARD.value == "standard"
        assert PaginationMode.SCROLL.value == "scroll"
        assert PaginationMode.CURSOR.value == "cursor"

    def test_pagination_config_defaults(self):
        """Test valores por defecto de PaginationConfig"""
        # Act
        config = PaginationConfig()

        # Assert
        assert config.mode == PaginationMode.STANDARD
        assert config.max_page_size == 1000
        assert config.max_total_results == 10000
        assert config.scroll_timeout == "1m"
        assert config.enable_auto_scroll == True
        assert config.preserve_order == True

    def test_pagination_config_custom(self):
        """Test configuración personalizada de PaginationConfig"""
        # Act
        config = PaginationConfig(
            mode=PaginationMode.SCROLL,
            max_page_size=500,
            max_total_results=5000,
            scroll_timeout="5m",
            enable_auto_scroll=False,
            preserve_order=False,
        )

        # Assert
        assert config.mode == PaginationMode.SCROLL
        assert config.max_page_size == 500
        assert config.max_total_results == 5000
        assert config.scroll_timeout == "5m"
        assert config.enable_auto_scroll == False
        assert config.preserve_order == False

    def test_page_info_creation(self):
        """Test creación de PageInfo"""
        # Act
        page_info = PageInfo(
            page=2,
            size=10,
            total_items=25,
            total_pages=3,
            has_next=True,
            has_previous=True,
            next_page=3,
            previous_page=1,
            scroll_id="abc123",
        )

        # Assert
        assert page_info.page == 2
        assert page_info.size == 10
        assert page_info.total_items == 25
        assert page_info.total_pages == 3
        assert page_info.has_next == True
        assert page_info.has_previous == True
        assert page_info.next_page == 3
        assert page_info.previous_page == 1
        assert page_info.scroll_id == "abc123"

    def test_pagination_result_creation(self):
        """Test creación de PaginationResult"""
        # Arrange
        data = [{"id": 1}, {"id": 2}]
        page_info = PageInfo(
            page=1,
            size=10,
            total_items=2,
            total_pages=1,
            has_next=False,
            has_previous=False,
        )
        links = {"self": "/api/reservations?page=1"}
        metadata = {"scroll_mode": False}

        # Act
        result = PaginationResult(
            data=data,
            page_info=page_info,
            links=links,
            metadata=metadata,
            scroll_id=None,
        )

        # Assert
        assert result.data == data
        assert result.page_info == page_info
        assert result.links == links
        assert result.metadata == metadata
        assert result.scroll_id is None

    def test_scroll_cache_management(self, pagination_utility):
        """Test manejo de cache de scroll"""
        # Arrange
        scroll_id = "test_scroll_123"
        scroll_data = {"data": "test"}

        # Act
        pagination_utility._scroll_cache[scroll_id] = scroll_data

        # Assert
        assert scroll_id in pagination_utility._scroll_cache
        assert pagination_utility._scroll_cache[scroll_id] == scroll_data

    def test_validate_pagination_params_edge_cases(self, pagination_utility):
        """Test casos edge de validación de parámetros"""
        # Test página negativa
        result = pagination_utility.validate_pagination_params(page=-5, size=10)
        assert result["page"] == 1

        # Test tamaño negativo
        result = pagination_utility.validate_pagination_params(page=1, size=-5)
        assert result["size"] == 1

        # Test límite exacto
        result = pagination_utility.validate_pagination_params(page=10, size=1000)
        assert result["page"] == 10
        assert result["size"] == 1000
        assert result["offset"] == 9000

    def test_calculate_page_info_edge_cases(self, pagination_utility):
        """Test casos edge de cálculo de información de página"""
        # Test con total_items negativo
        page_info = pagination_utility.calculate_page_info(
            page=1, size=10, total_items=-5
        )
        assert page_info.total_items == -5
        assert page_info.total_pages == 0

        # Test con size muy grande
        page_info = pagination_utility.calculate_page_info(
            page=1, size=1000, total_items=5
        )
        assert page_info.size == 1000
        assert page_info.total_pages == 1

    def test_generate_links_edge_cases(self, pagination_utility):
        """Test casos edge de generación de enlaces"""
        # Test con base_url vacía
        page_info = PageInfo(
            page=1,
            size=10,
            total_items=10,
            total_pages=1,
            has_next=False,
            has_previous=False,
        )
        links = pagination_utility.generate_links("", page_info, {})
        assert "self" in links
        assert (
            links["self"] == "?page=1"
        )  # Se genera parámetro page aunque base_url esté vacía

        # Test con query_params vacío
        links = pagination_utility.generate_links("https://api.com", page_info, {})
        assert "self" in links
        assert "page=1" in links["self"]

    def test_process_scroll_response_missing_fields(self, pagination_utility):
        """Test procesamiento de respuesta de scroll con campos faltantes"""
        # Arrange
        response = {}  # Respuesta vacía

        # Act
        result = pagination_utility.process_scroll_response(response)

        # Assert
        assert result.data == []
        assert result.page_info.total_items == 0
        assert result.page_info.scroll_id is None
        assert result.scroll_id is None

    def test_process_standard_response_missing_fields(self, pagination_utility):
        """Test procesamiento de respuesta estándar con campos faltantes"""
        # Arrange
        response = {}  # Respuesta vacía

        # Act
        result = pagination_utility.process_standard_response(response, page=1, size=10)

        # Assert
        assert result.data == []
        assert result.page_info.page == 1
        assert result.page_info.size == 10
        assert result.page_info.total_items == 0
        assert result.page_info.total_pages == 0
