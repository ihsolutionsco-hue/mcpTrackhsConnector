"""
Configuración de tests para TrackHS MCP Server
"""

import os
from unittest.mock import Mock, patch

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# Configurar variables de entorno para tests
os.environ["TRACKHS_USERNAME"] = "test_user"
os.environ["TRACKHS_PASSWORD"] = "test_password"
os.environ["TRACKHS_BASE_URL"] = "https://api-test.trackhs.com/api"


@pytest.fixture
async def mcp_client():
    """Cliente MCP para tests"""
    from fastmcp.client.transports import FastMCPTransport

    from src.trackhs_mcp.server import mcp

    async with Client(transport=FastMCPTransport(mcp)) as client:
        yield client


@pytest.fixture
def mock_api_response():
    """Respuesta mock de la API TrackHS"""
    return {
        "page": 1,
        "page_count": 1,
        "page_size": 10,
        "total_items": 1,
        "_embedded": {
            "reservations": [
                {
                    "id": 12345,
                    "confirmation_number": "CONF123",
                    "guest_name": "John Doe",
                    "guest_email": "john@example.com",
                    "arrival_date": "2024-01-15",
                    "departure_date": "2024-01-20",
                    "status": "confirmed",
                    "unit_id": 100,
                    "total_amount": 500.0,
                    "balance": 0.0,
                }
            ]
        },
        "_links": {
            "self": {"href": "https://api-test.trackhs.com/api/reservations?page=1"},
            "first": {"href": "https://api-test.trackhs.com/api/reservations"},
            "last": {"href": "https://api-test.trackhs.com/api/reservations?page=1"},
        },
    }


@pytest.fixture
def mock_unit_response():
    """Respuesta mock para unidades"""
    return {
        "page": 1,
        "page_count": 1,
        "page_size": 10,
        "total_items": 1,
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
                    "address": "123 Beach St",
                    "amenities": ["WiFi", "Pool", "Parking"],
                    "is_active": True,
                    "is_bookable": True,
                }
            ]
        },
        "_links": {
            "self": {"href": "https://api-test.trackhs.com/api/units?page=1"},
            "first": {"href": "https://api-test.trackhs.com/api/units"},
            "last": {"href": "https://api-test.trackhs.com/api/units?page=1"},
        },
    }
