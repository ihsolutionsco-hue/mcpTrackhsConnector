"""
Configuración simplificada de pytest para TrackHS MCP Connector MVP
"""

import asyncio
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

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_API_URL", "https://api-test.trackhs.com/api")
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_TIMEOUT", "30")
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8080")
os.environ.setdefault("CORS_ORIGINS", "https://elevenlabs.io,https://app.elevenlabs.io")


@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para toda la sesión de tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_api_client():
    """Mock del API client para tests críticos"""
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
    """Mock de configuración TrackHS"""
    from trackhs_mcp.domain.value_objects.config import TrackHSConfig

    return TrackHSConfig(
        base_url="https://api-test.trackhs.com/api",
        username="test_user",
        password="test_password",
        timeout=30,
    )


@pytest.fixture
def sample_reservation_data():
    """Datos de ejemplo de una reserva"""
    return {
        "id": 37165851,
        "status": "Confirmed",
        "arrivalDate": "2024-01-15",
        "departureDate": "2024-01-20",
        "nights": 5,
        "currency": "USD",
        "unitId": 1,
        "contactId": 1,
        "channelId": 1,
        "subChannel": "airbnb",
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


@pytest.fixture
def sample_folio_data():
    """Datos de ejemplo de un folio"""
    return {
        "id": 12345,
        "status": "open",
        "type": "guest",
        "currentBalance": 150.00,
        "realizedBalance": 100.00,
        "startDate": "2024-01-15",
        "endDate": "2024-01-20",
        "contactId": 1,
        "reservationId": 37165851,
        "name": "Guest Folio - John Doe",
        "createdAt": "2024-01-10T10:00:00Z",
        "updatedAt": "2024-01-10T10:00:00Z",
        "_embedded": {
            "contact": {
                "id": 1,
                "firstName": "John",
                "lastName": "Doe",
                "primaryEmail": "john@example.com",
            },
        },
        "_links": {
            "self": {"href": "/api/pms/folios/12345"},
        },
    }


@pytest.fixture
def sample_unit_data():
    """Datos de ejemplo de una unidad"""
    return {
        "id": 1,
        "name": "Villa Paradise",
        "shortName": "VP001",
        "unitCode": "VP001",
        "nodeId": 1,
        "bedrooms": 3,
        "fullBathrooms": 2,
        "maxOccupancy": 6,
        "petsFriendly": True,
        "eventsAllowed": False,
        "smokingAllowed": False,
        "childrenAllowed": True,
        "isAccessible": True,
        "isActive": True,
        "updatedAt": "2024-01-15T10:30:00Z",
        "createdAt": "2024-01-15T10:30:00Z",
        "_links": {"self": {"href": "https://api-test.trackhs.com/api/pms/units/1"}},
    }


@pytest.fixture
def sample_amenity_data():
    """Datos de ejemplo de una amenidad"""
    return {
        "id": 1,
        "name": "WiFi",
        "description": "Free WiFi internet access",
        "category": "Internet",
        "isActive": True,
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:30:00Z",
        "_links": {
            "self": {"href": "https://api-test.trackhs.com/api/pms/amenities/1"}
        },
    }


@pytest.fixture
def sample_work_order_data():
    """Datos de ejemplo de una orden de trabajo"""
    return {
        "id": 12345,
        "dateReceived": "2024-01-15",
        "priority": 5,
        "status": "open",
        "summary": "Reparar aire acondicionado en unidad 101",
        "estimatedCost": 150.00,
        "estimatedTime": 120,
        "unitId": 123,
        "reservationId": 37165851,
        "referenceNumber": "WO-2024-001",
        "description": "El aire acondicionado de la unidad 101 no está funcionando correctamente",
        "source": "Guest Request",
        "sourceName": "Juan Pérez",
        "sourcePhone": "+1234567890",
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:30:00Z",
        "_embedded": {
            "unit": {
                "id": 123,
                "name": "Unit 101",
                "unitCode": "U101",
                "nodeId": 1,
            },
        },
        "_links": {
            "self": {"href": "/api/pms/maintenance/work-orders/12345"},
        },
    }


# Marcadores para diferentes tipos de tests
def pytest_configure(config):
    """Configurar marcadores personalizados"""
    config.addinivalue_line("markers", "critical: Critical functionality tests")
    config.addinivalue_line("markers", "smoke: Smoke tests for quick validation")
