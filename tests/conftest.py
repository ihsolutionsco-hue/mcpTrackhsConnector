"""
Configuración super simple de pytest para TrackHS MCP Connector MVP
Enfoque: Solo lo esencial para validar el protocolo MCP
"""

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

# Agregar el directorio src al PYTHONPATH para todos los tests
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Configurar variables de entorno para testing MCP
os.environ.setdefault("TRACKHS_API_URL", "https://api-test.trackhs.com/api")
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_TIMEOUT", "30")
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8080")
os.environ.setdefault("CORS_ORIGINS", "https://elevenlabs.io,https://app.elevenlabs.io")


@pytest.fixture
def mock_api_client():
    """Mock del API client para tests MCP"""
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.request = AsyncMock()
    client.close = Mock()

    # Context manager support
    client.__enter__ = Mock(return_value=client)
    client.__exit__ = Mock(return_value=None)

    # Configurar config mock para compatibilidad
    client.config = Mock()
    client.config.base_url = "https://api-test.trackhs.com/api"
    client.config.timeout = 30

    return client


@pytest.fixture
def mock_config():
    """Mock de configuración TrackHS para tests MCP"""
    from trackhs_mcp.domain.value_objects.config import TrackHSConfig

    return TrackHSConfig(
        base_url="https://api-test.trackhs.com/api",
        username="test_user",
        password="test_password",
        timeout=30,
    )


@pytest.fixture
def sample_mcp_tool_response():
    """Datos de ejemplo para respuestas de herramientas MCP"""
    return {
        "data": [
            {
                "id": 37165851,
                "status": "Confirmed",
                "arrivalDate": "2024-01-15",
                "departureDate": "2024-01-20",
                "nights": 5,
                "currency": "USD",
                "unitId": 1,
                "contactId": 1,
                "folioId": 1,
                "uuid": "uuid-37165851",
                "source": "airbnb",
                "guestBreakdown": {
                    "grossRent": "1000.00",
                    "netRent": "950.00",
                    "total": "1000.00",
                    "balance": "0.00",
                },
                "_embedded": {
                    "unit": {
                        "id": 1,
                        "name": "Test Unit",
                        "unitCode": "TU001",
                        "bedrooms": 2,
                        "fullBathrooms": 1,
                        "maxOccupancy": 4,
                        "petsFriendly": False,
                        "isActive": True,
                    },
                    "contact": {
                        "id": 1,
                        "firstName": "John",
                        "lastName": "Doe",
                        "primaryEmail": "john.doe@example.com",
                        "cellPhone": "+1234567890",
                    },
                },
                "_links": {
                    "self": {
                        "href": "https://api-test.trackhs.com/api/v2/pms/reservations/37165851"
                    }
                },
            }
        ],
        "total": 1,
        "page": 0,
        "size": 10,
        "_links": {
            "self": {"href": "https://api-test.trackhs.com/api/v2/pms/reservations"},
            "next": None,
        },
    }


@pytest.fixture
def sample_mcp_resource_data():
    """Datos de ejemplo para recursos MCP"""
    return {
        "schemas": {
            "reservations-v2": "Schema para Reservations API V2",
            "reservation-detail-v2": "Schema para Get Reservation V2",
            "folio": "Schema para Folios API",
            "units": "Schema para Units API",
            "amenities": "Schema para Amenities API",
            "work-orders": "Schema para Work Orders API",
        },
        "documentation": {
            "api-v2": "Documentación esencial de Reservations API V2",
            "folio-api": "Documentación esencial de Folios API",
            "amenities-api": "Documentación esencial de Amenities API",
            "work-orders-api": "Documentación esencial de Work Orders API",
        },
        "examples": {
            "search-queries": "Ejemplos de búsquedas de reservas",
            "folio-operations": "Ejemplos de operaciones con folios",
            "amenities": "Ejemplos de búsquedas de amenidades",
            "work-orders": "Ejemplos de creación de órdenes de trabajo",
        },
        "references": {
            "status-values": "Valores válidos para parámetros de estado",
            "date-formats": "Formatos de fecha soportados por la API",
        },
    }


@pytest.fixture
def sample_mcp_prompt_data():
    """Datos de ejemplo para prompts MCP"""
    return {
        "search-reservations-by-dates": {
            "name": "search-reservations-by-dates",
            "description": "Búsqueda por rango de fechas",
            "parameters": ["start_date", "end_date", "include_financials"],
        },
        "search-reservations-by-guest": {
            "name": "search-reservations-by-guest",
            "description": "Búsqueda por información del huésped",
            "parameters": ["guest_name", "contact_id", "include_financials"],
        },
        "search-reservations-advanced": {
            "name": "search-reservations-advanced",
            "description": "Búsqueda avanzada con múltiples filtros",
            "parameters": ["filters", "include_financials"],
        },
    }


# Marcadores para diferentes tipos de tests MCP
def pytest_configure(config):
    """Configurar marcadores personalizados para tests MCP"""
    config.addinivalue_line("markers", "mcp_protocol: MCP Protocol tests")
    config.addinivalue_line("markers", "mcp_server: MCP Server tests")
    config.addinivalue_line("markers", "mcp_tools: MCP Tools tests")
    config.addinivalue_line("markers", "mcp_resources: MCP Resources tests")
    config.addinivalue_line("markers", "mcp_prompts: MCP Prompts tests")
