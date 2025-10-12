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
        "unit_id": 1,
        "client_ip_address": "192.168.1.1",
        "session": "session_data",
        "is_unit_locked": False,
        "is_unit_assigned": True,
        "is_unit_type_locked": False,
        "unit_type_id": 1,
        "arrival_date": "2024-01-15",
        "departure_date": "2024-01-20",
        "early_arrival": False,
        "late_departure": False,
        "arrival_time": "2024-01-15T15:00:00Z",
        "departure_time": "2024-01-20T11:00:00Z",
        "nights": 5,
        "status": "Confirmed",
        "cancelled_at": None,
        "occupants": [
            {
                "type_id": 1,
                "name": "Adults",
                "handle": "adults",
                "quantity": 2,
                "included": True,
                "extra_quantity": 0,
                "rate_per_person_per_stay": "0.00",
                "rate_per_stay": "0.00",
            }
        ],
        "security_deposit": {"required": "100.00", "remaining": 100},
        "updated_at": "2024-01-10T10:00:00Z",
        "created_at": "2024-01-10T10:00:00Z",
        "booked_at": "2024-01-10T10:00:00Z",
        "contact_id": 1,
        "channel_id": 1,
        "sub_channel": "direct",
        "folio_id": 1,
        "guarantee_policy_id": 1,
        "cancellation_policy_id": 1,
        "cancellation_reason_id": None,
        "user_id": 1,
        "travel_agent_id": None,
        "campaign_id": None,
        "type_id": 1,
        "rate_type_id": 1,
        "unit_code_id": 1,
        "cancelled_by_id": None,
        "payment_method_id": 1,
        "quote_id": None,
        "hold_expires_at": None,
        "is_taxable": True,
        "invite_uuid": None,
        "uuid": "uuid-12345",
        "source": "direct",
        "is_channel_locked": False,
        "agreement_status": "not-needed",
        "automate_payment": False,
        "revenue_realized_method": "nightly",
        "schedule_type1": None,
        "schedule_percentage1": None,
        "schedule_type2": None,
        "schedule_percentage2": None,
        "promo_code_id": None,
        "updated_by": "system",
        "created_by": "system",
        "group_id": None,
        "payment_plan": [],
        "rate_type": {
            "id": 1,
            "type": "standard",
            "code": "STD",
            "name": "Standard Rate",
        },
        "travel_insurance_products": [],
        "guest_breakdown": {
            "gross_rent": "1000.00",
            "guest_gross_display_rent": "1000.00",
            "discount": "0.00",
            "promo_value": "0.00",
            "discount_total": 0,
            "net_rent": "950.00",
            "guest_net_display_rent": "950.00",
            "actual_adr": "190.00",
            "guest_adr": "190.00",
            "total_guest_fees": "50.00",
            "total_rent_fees": "0.00",
            "total_itemized_fees": "0.00",
            "total_tax_fees": "0.00",
            "total_service_fees": "0.00",
            "folio_charges": "0.00",
            "subtotal": "1000.00",
            "guest_subtotal": "1000.00",
            "total_taxes": "0.00",
            "total_guest_taxes": "0.00",
            "total": "1000.00",
            "grand_total": "1000.00",
            "net_payments": "1000.00",
            "payments": "1000.00",
            "refunds": "0.00",
            "net_transfers": "0.00",
            "balance": "0.00",
            "rates": [],
            "guest_fees": [],
            "taxes": [],
        },
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
