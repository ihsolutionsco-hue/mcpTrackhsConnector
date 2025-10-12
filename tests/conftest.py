"""
Configuración global de pytest para Track HS MCP Connector
"""

import asyncio
import os
import sys
from pathlib import Path

# No unused imports
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


@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para toda la sesión de tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_api_client():
    """Mock del API client para tests unitarios"""
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.request = AsyncMock()
    return client


@pytest.fixture
def mock_auth():
    """Mock de autenticación"""
    auth = Mock()
    auth.get_headers.return_value = {
        "Authorization": "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    auth.validate_credentials.return_value = True
    return auth


@pytest.fixture
def sample_reservation_data():
    """Datos de ejemplo de una reserva"""
    return {
        "id": 12345,
        "alternates": ["ALT123"],
        "currency": "USD",
        "unitId": 1,
        "clientIPAddress": "192.168.1.1",
        "session": "session_data",
        "isUnitLocked": False,
        "isUnitAssigned": True,
        "isUnitTypeLocked": False,
        "unitTypeId": 1,
        "arrivalDate": "2024-01-15",
        "departureDate": "2024-01-20",
        "earlyArrival": False,
        "lateDeparture": False,
        "arrivalTime": "2024-01-15T15:00:00Z",
        "departureTime": "2024-01-20T11:00:00Z",
        "nights": 5,
        "status": "Confirmed",
        "cancelledAt": None,
        "occupants": [
            {
                "typeId": 1,
                "name": "Adults",
                "handle": "adults",
                "quantity": 2,
                "included": True,
                "extraQuantity": 0,
                "ratePerPersonPerStay": "0.00",
                "ratePerStay": "0.00",
            }
        ],
        "securityDeposit": {"required": "100.00", "remaining": 100},
        "updatedAt": "2024-01-10T10:00:00Z",
        "createdAt": "2024-01-10T10:00:00Z",
        "bookedAt": "2024-01-10T10:00:00Z",
        "contactId": 1,
        "channelId": 1,
        "subChannel": "direct",
        "folioId": 1,
        "guaranteePolicyId": 1,
        "cancellationPolicyId": 1,
        "cancellationReasonId": None,
        "userId": 1,
        "travelAgentId": None,
        "campaignId": None,
        "typeId": 1,
        "rateTypeId": 1,
        "unitCodeId": 1,
        "cancelledById": None,
        "paymentMethodId": 1,
        "quoteId": None,
        "holdExpiresAt": None,
        "isTaxable": True,
        "inviteUuid": None,
        "uuid": "uuid-12345",
        "source": "direct",
        "isChannelLocked": False,
        "agreementStatus": "not-needed",
        "automatePayment": False,
        "revenueRealizedMethod": "nightly",
        "scheduleType1": None,
        "schedulePercentage1": None,
        "scheduleType2": None,
        "schedulePercentage2": None,
        "promoCodeId": None,
        "updatedBy": "system",
        "createdBy": "system",
        "groupId": None,
        "paymentPlan": [],
        "rateType": {
            "id": 1,
            "type": "standard",
            "code": "STD",
            "name": "Standard Rate",
        },
        "travelInsuranceProducts": [],
        "_embedded": {
            "unit": {
                "id": 1,
                "name": "Test Unit",
                "shortName": "TU",
                "unitCode": "TU001",
                "headline": "Beautiful Test Unit",
                "shortDescription": "A lovely test unit",
                "longDescription": "A beautiful test unit with all amenities",
                "houseRules": "No smoking, no pets",
                "nodeId": 1,
                "unitType": {"id": 1, "name": "Apartment"},
                "lodgingType": {"id": 1, "name": "Vacation Rental"},
                "directions": "Turn left at the main street",
                "checkinDetails": "Check-in at 3 PM",
                "timezone": "America/New_York",
                "checkinTime": "15:00",
                "hasEarlyCheckin": True,
                "earlyCheckinTime": "12:00",
                "checkoutTime": "11:00",
                "hasLateCheckout": True,
                "lateCheckoutTime": "14:00",
                "minBookingWindow": 1,
                "maxBookingWindow": 365,
                "website": "https://example.com",
                "phone": "+1234567890",
                "streetAddress": "123 Main St",
                "extendedAddress": "Apt 1",
                "locality": "Test City",
                "region": "Test State",
                "postalCode": "12345",
                "country": "US",
                "longitude": -74.0059,
                "latitude": 40.7128,
                "petsFriendly": False,
                "maxPets": 0,
                "eventsAllowed": False,
                "smokingAllowed": False,
                "childrenAllowed": True,
                "minimumAgeLimit": None,
                "isAccessible": True,
                "area": 100.0,
                "floors": 1,
                "maxOccupancy": 4,
                "securityDeposit": "100.00",
                "bedrooms": 2,
                "fullBathrooms": 1,
                "threeQuarterBathrooms": 0,
                "halfBathrooms": 0,
                "bedTypes": [],
                "rooms": [],
                "amenities": [],
                "amenityDescription": "All modern amenities",
                "coverImage": "https://example.com/image.jpg",
                "taxId": 1,
                "localOffice": {
                    "name": "Test Office",
                    "directions": "Office directions",
                    "email": "office@example.com",
                    "phone": "+1234567890",
                    "latitude": "-74.0059",
                    "longitude": "40.7128",
                    "streetAddress": "123 Office St",
                    "extendedAddress": "Suite 100",
                    "locality": "Test City",
                    "region": "Test State",
                    "postalCode": "12345",
                    "country": "US",
                },
                "regulations": [],
                "updated": {
                    "availability": "2024-01-10T10:00:00Z",
                    "content": "2024-01-10T10:00:00Z",
                    "pricing": "2024-01-10T10:00:00Z",
                },
                "updatedAt": "2024-01-10T10:00:00Z",
                "createdAt": "2024-01-10T10:00:00Z",
                "isActive": True,
                "_links": {
                    "self": {"href": "https://api-test.trackhs.com/api/v2/pms/units/1"}
                },
            },
            "contact": {
                "id": 1,
                "firstName": "John",
                "lastName": "Doe",
                "name": "John Doe",
                "primaryEmail": "john.doe@example.com",
                "secondaryEmail": None,
                "homePhone": None,
                "cellPhone": "+1234567890",
                "workPhone": None,
                "otherPhone": None,
                "fax": None,
                "streetAddress": "123 Guest St",
                "extendedAddress": None,
                "locality": "Guest City",
                "region": "Guest State",
                "postalCode": "54321",
                "country": "US",
                "notes": "VIP guest",
                "anniversary": None,
                "birthdate": None,
                "noIdentity": False,
                "isVip": True,
                "isBlacklist": False,
                "isDNR": False,
                "tags": [],
                "references": [],
                "custom": {},
                "updatedBy": "system",
                "createdBy": "system",
                "updatedAt": "2024-01-10T10:00:00Z",
                "createdAt": "2024-01-10T10:00:00Z",
                "isOwnerContact": False,
                "_links": {
                    "self": {
                        "href": "https://api-test.trackhs.com/api/v2/pms/contacts/1"
                    }
                },
            },
        },
        "_links": {
            "self": {
                "href": "https://api-test.trackhs.com/api/v2/pms/reservations/12345"
            }
        },
    }


@pytest.fixture
def sample_search_response():
    """Respuesta de ejemplo de búsqueda de reservas"""
    return {
        "_embedded": {
            "reservations": [
                {
                    "id": 12345,
                    "status": "Confirmed",
                    "arrivalDate": "2024-01-15",
                    "departureDate": "2024-01-20",
                    "nights": 5,
                    "currency": "USD",
                }
            ]
        },
        "page": 1,
        "page_count": 1,
        "page_size": 10,
        "total_items": 1,
        "_links": {
            "self": {
                "href": "https://api-test.trackhs.com/api/v2/pms/reservations?page=1"
            },
            "first": {
                "href": "https://api-test.trackhs.com/api/v2/pms/reservations?page=1"
            },
            "last": {
                "href": "https://api-test.trackhs.com/api/v2/pms/reservations?page=1"
            },
        },
    }


@pytest.fixture
def mock_trackhs_config():
    """Configuración mock de Track HS"""
    from trackhs_mcp.domain.value_objects.config import TrackHSConfig

    return TrackHSConfig(
        base_url="https://api-test.trackhs.com/api",
        username="test_user",
        password="test_password",
        timeout=30,
    )


@pytest.fixture
def mock_mcp():
    """Mock del servidor MCP"""
    mcp = Mock()
    mcp.tool = Mock()
    mcp.resource = Mock()
    mcp.prompt = Mock()
    return mcp


# Marcadores para diferentes tipos de tests
def pytest_configure(config):
    """Configurar marcadores personalizados"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "api: Tests that require API access")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "network: Tests that require network access")
