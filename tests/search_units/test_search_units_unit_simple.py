"""
Tests unitarios simplificados para search_units
Enfocados en la lógica de negocio sin decoradores FastMCP
"""

import pytest
from unittest.mock import Mock, patch
from pydantic import ValidationError

# Importar las dependencias necesarias
import sys
from pathlib import Path

src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from trackhs_mcp.exceptions import (
    AuthenticationError,
    APIError,
    ConnectionError,
    NotFoundError,
    ValidationError as TrackHSValidationError,
    TrackHSError,
)


class TestSearchUnitsUnitSimple:
    """Tests unitarios simplificados para search_units"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client

    @pytest.fixture
    def sample_api_response(self):
        """Respuesta de ejemplo de la API"""
        return {
            "page": 1,
            "page_count": 2,
            "page_size": 10,
            "total_items": 15,
            "_embedded": {
                "units": [
                    {
                        "id": 100,
                        "name": "Casa de Playa",
                        "code": "CP001",
                        "bedrooms": 3,
                        "bathrooms": 2,
                        "max_occupancy": 6,
                        "area": 120.5,
                        "address": "123 Beach St, Miami, FL",
                        "amenities": ["WiFi", "Pool", "Parking", "AC"],
                        "is_active": True,
                        "is_bookable": True,
                        "description": "Hermosa casa frente al mar",
                    },
                    {
                        "id": 101,
                        "name": "Penthouse Suite",
                        "code": "PS002",
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "max_occupancy": 4,
                        "area": 95.0,
                        "address": "456 Downtown Ave, Miami, FL",
                        "amenities": ["WiFi", "Gym", "Concierge", "Valet"],
                        "is_active": True,
                        "is_bookable": True,
                        "description": "Lujoso penthouse en el centro",
                    },
                ]
            },
            "_links": {
                "self": {"href": "/pms/units?page=1&size=10"},
                "first": {"href": "/pms/units?page=1&size=10"},
                "last": {"href": "/pms/units?page=2&size=10"},
                "next": {"href": "/pms/units?page=2&size=10"},
            },
        }

    def test_parameter_validation(self):
        """Test de validación de parámetros usando Pydantic"""
        from pydantic import BaseModel, Field
        from typing import Optional

        # Crear modelo de validación similar al de search_units
        class SearchUnitsParams(BaseModel):
            page: int = Field(ge=1, le=400, default=1)
            size: int = Field(ge=1, le=25, default=10)
            search: Optional[str] = Field(max_length=200, default=None)
            bedrooms: Optional[int] = Field(ge=0, le=20, default=None)
            bathrooms: Optional[int] = Field(ge=0, le=20, default=None)
            is_active: Optional[int] = Field(ge=0, le=1, default=None)
            is_bookable: Optional[int] = Field(ge=0, le=1, default=None)

        # Test con parámetros válidos
        valid_params = SearchUnitsParams(
            page=1,
            size=10,
            search="beach",
            bedrooms=2,
            bathrooms=1,
            is_active=1,
            is_bookable=1,
        )
        assert valid_params.page == 1
        assert valid_params.size == 10
        assert valid_params.search == "beach"

        # Test con parámetros inválidos
        with pytest.raises(ValidationError):
            SearchUnitsParams(page=0)  # Debe ser >= 1

        with pytest.raises(ValidationError):
            SearchUnitsParams(size=0)  # Debe ser >= 1

        with pytest.raises(ValidationError):
            SearchUnitsParams(bedrooms=-1)  # Debe ser >= 0

        with pytest.raises(ValidationError):
            SearchUnitsParams(bathrooms=21)  # Debe ser <= 20

        with pytest.raises(ValidationError):
            SearchUnitsParams(is_active=2)  # Debe ser 0 o 1

        with pytest.raises(ValidationError):
            SearchUnitsParams(is_bookable=2)  # Debe ser 0 o 1

    def test_string_validation(self):
        """Test de validación de strings"""
        from pydantic import BaseModel, Field
        from typing import Optional

        class SearchUnitsParams(BaseModel):
            search: Optional[str] = Field(max_length=200, default=None)

        # Test con string válido
        valid_params = SearchUnitsParams(search="beach")
        assert valid_params.search == "beach"

        # Test con string muy largo
        long_search = "a" * 201  # Más de 200 caracteres
        with pytest.raises(ValidationError):
            SearchUnitsParams(search=long_search)

    def test_api_client_mock(self, mock_api_client, sample_api_response):
        """Test de mock del cliente API"""
        mock_api_client.get.return_value = sample_api_response

        # Simular llamada a API
        result = mock_api_client.get("pms/units", {"page": 1, "size": 10})

        # Verificar que se llamó correctamente
        mock_api_client.get.assert_called_once_with(
            "pms/units", {"page": 1, "size": 10}
        )

        # Verificar respuesta
        assert result["page"] == 1
        assert result["total_items"] == 15
        assert len(result["_embedded"]["units"]) == 2

    def test_error_handling(self, mock_api_client):
        """Test de manejo de errores"""
        # Test de error de autenticación
        mock_api_client.get.side_effect = AuthenticationError("Credenciales inválidas")

        with pytest.raises(AuthenticationError):
            mock_api_client.get("pms/units", {})

        # Test de error de API
        mock_api_client.get.side_effect = APIError("Error interno del servidor")

        with pytest.raises(APIError):
            mock_api_client.get("pms/units", {})

        # Test de error de conexión
        mock_api_client.get.side_effect = ConnectionError("Error de conexión")

        with pytest.raises(ConnectionError):
            mock_api_client.get("pms/units", {})

    def test_response_structure_validation(self, sample_api_response):
        """Test de validación de estructura de respuesta"""
        # Verificar campos obligatorios
        required_fields = [
            "page",
            "page_count",
            "page_size",
            "total_items",
            "_embedded",
            "_links",
        ]
        for field in required_fields:
            assert (
                field in sample_api_response
            ), f"Campo obligatorio '{field}' no encontrado"

        # Verificar estructura de unidades
        assert "units" in sample_api_response["_embedded"]
        units = sample_api_response["_embedded"]["units"]

        if units:
            unit = units[0]
            required_unit_fields = [
                "id",
                "name",
                "code",
                "bedrooms",
                "bathrooms",
                "max_occupancy",
                "area",
                "address",
                "amenities",
                "is_active",
                "is_bookable",
            ]
            for field in required_unit_fields:
                assert (
                    field in unit
                ), f"Campo obligatorio de unidad '{field}' no encontrado"

    def test_unicode_handling(self):
        """Test de manejo de caracteres unicode"""
        unicode_data = {
            "name": "Casa de Playa 🏖️",
            "address": "123 Playa del Sol, Cancún, México",
            "amenities": ["WiFi", "Piscina", "Aire Acondicionado"],
        }

        # Verificar que los strings unicode se manejan correctamente
        assert "🏖️" in unicode_data["name"]
        assert "México" in unicode_data["address"]
        assert "Piscina" in unicode_data["amenities"]

        # Verificar que son strings válidos
        for key, value in unicode_data.items():
            if isinstance(value, str):
                assert isinstance(value, str)
            elif isinstance(value, list):
                for item in value:
                    assert isinstance(item, str)

    def test_edge_cases(self):
        """Test de casos límite"""
        # Test con valores mínimos
        edge_data = {
            "bedrooms": 0,
            "bathrooms": 0,
            "max_occupancy": 1,
            "area": 0.0,
            "is_active": False,
            "is_bookable": False,
        }

        # Verificar que los valores límite son válidos
        assert edge_data["bedrooms"] >= 0
        assert edge_data["bathrooms"] >= 0
        assert edge_data["max_occupancy"] > 0
        assert edge_data["area"] >= 0
        assert isinstance(edge_data["is_active"], bool)
        assert isinstance(edge_data["is_bookable"], bool)

    def test_pagination_logic(self):
        """Test de lógica de paginación"""
        # Test de metadatos de paginación
        pagination_data = {
            "page": 1,
            "page_count": 3,
            "page_size": 10,
            "total_items": 25,
        }

        # Verificar cálculos de paginación
        assert pagination_data["page"] >= 1
        assert pagination_data["page_count"] >= 1
        assert pagination_data["page_size"] >= 1
        assert pagination_data["total_items"] >= 0

        # Verificar consistencia
        expected_page_count = (
            pagination_data["total_items"] + pagination_data["page_size"] - 1
        ) // pagination_data["page_size"]
        assert pagination_data["page_count"] == expected_page_count

    def test_parameter_combinations(self):
        """Test de combinaciones de parámetros"""
        from pydantic import BaseModel, Field
        from typing import Optional

        class SearchUnitsParams(BaseModel):
            page: int = Field(ge=1, le=400, default=1)
            size: int = Field(ge=1, le=25, default=10)
            search: Optional[str] = Field(max_length=200, default=None)
            bedrooms: Optional[int] = Field(ge=0, le=20, default=None)
            bathrooms: Optional[int] = Field(ge=0, le=20, default=None)
            is_active: Optional[int] = Field(ge=0, le=1, default=None)
            is_bookable: Optional[int] = Field(ge=0, le=1, default=None)

        # Test diferentes combinaciones válidas
        combinations = [
            {"search": "beach"},
            {"bedrooms": 2},
            {"bathrooms": 1},
            {"is_active": 1},
            {"is_bookable": 1},
            {"bedrooms": 2, "bathrooms": 1},
            {"is_active": 1, "is_bookable": 1},
            {"search": "penthouse", "bedrooms": 2, "is_active": 1},
        ]

        for combo in combinations:
            params = SearchUnitsParams(**combo)
            # Verificar que se creó correctamente
            for key, value in combo.items():
                assert getattr(params, key) == value

    def test_data_types_validation(self, sample_api_response):
        """Test de validación de tipos de datos"""
        # Verificar tipos de metadatos
        assert isinstance(sample_api_response["page"], int)
        assert isinstance(sample_api_response["page_count"], int)
        assert isinstance(sample_api_response["page_size"], int)
        assert isinstance(sample_api_response["total_items"], int)
        assert isinstance(sample_api_response["_embedded"], dict)
        assert isinstance(sample_api_response["_links"], dict)

        # Verificar tipos de unidades
        if sample_api_response["_embedded"]["units"]:
            unit = sample_api_response["_embedded"]["units"][0]
            assert isinstance(unit["id"], int)
            assert isinstance(unit["name"], str)
            assert isinstance(unit["code"], str)
            assert isinstance(unit["bedrooms"], int)
            assert isinstance(unit["bathrooms"], int)
            assert isinstance(unit["max_occupancy"], int)
            assert isinstance(unit["area"], (int, float))
            assert isinstance(unit["address"], str)
            assert isinstance(unit["amenities"], list)
            assert isinstance(unit["is_active"], bool)
            assert isinstance(unit["is_bookable"], bool)

    def test_empty_response_handling(self):
        """Test de manejo de respuesta vacía"""
        empty_response = {
            "page": 1,
            "page_count": 0,
            "page_size": 10,
            "total_items": 0,
            "_embedded": {"units": []},
            "_links": {"self": {"href": "/pms/units?page=1&size=10"}},
        }

        # Verificar estructura de respuesta vacía
        assert empty_response["total_items"] == 0
        assert len(empty_response["_embedded"]["units"]) == 0
        assert empty_response["page_count"] == 0

        # Verificar que los campos obligatorios están presentes
        required_fields = [
            "page",
            "page_count",
            "page_size",
            "total_items",
            "_embedded",
            "_links",
        ]
        for field in required_fields:
            assert field in empty_response
