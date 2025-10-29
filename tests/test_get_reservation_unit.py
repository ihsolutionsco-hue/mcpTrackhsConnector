"""
Pruebas unitarias para el tool get_reservation actualizado con API V2
"""

import json
import os
import sys
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastmcp.exceptions import ToolError

from trackhs_mcp.client import TrackHSClient
from trackhs_mcp.schemas import ReservationDetailOutput
from trackhs_mcp.server import get_reservation


class TestGetReservationUnit:
    """Pruebas unitarias para get_reservation"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.valid_reservation_id = 12345
        self.invalid_reservation_id = 0
        self.nonexistent_reservation_id = 99999

    @patch("src.trackhs_mcp.server.api_client")
    def test_get_reservation_success(self, mock_api_client):
        """Test exitoso de obtención de reserva"""
        # Mock de respuesta exitosa de la API V2
        mock_response = {
            "id": 12345,
            "alternates": ["ALT123", "ALT456"],
            "currency": "USD",
            "unitId": 789,
            "unitTypeId": 101,
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "arrivalTime": "2024-01-15T15:00:00Z",
            "departureTime": "2024-01-20T11:00:00Z",
            "nights": 5.0,
            "earlyArrival": False,
            "lateDeparture": False,
            "status": "Confirmed",
            "isUnitLocked": False,
            "isUnitAssigned": True,
            "isUnitTypeLocked": False,
            "isChannelLocked": False,
            "cancelledAt": None,
            "cancellationReasonId": None,
            "occupants": [
                {
                    "typeId": 1,
                    "name": "Adult",
                    "handle": "adult",
                    "quantity": 2,
                    "included": True,
                    "extraQuantity": 0,
                    "ratePerPersonPerStay": "0.00",
                    "ratePerStay": "0.00",
                }
            ],
            "securityDeposit": {"required": "200.00", "remaining": 200},
            "updatedAt": "2024-01-10T10:30:00Z",
            "createdAt": "2024-01-10T10:00:00Z",
            "bookedAt": "2024-01-10T10:00:00Z",
            "guestBreakdown": {
                "grossRent": "1000.00",
                "netRent": "1000.00",
                "total": "1200.00",
                "balance": "0.00",
            },
            "ownerBreakdown": {"grossRent": "1000.00", "netRevenue": "900.00"},
            "contactId": 456,
            "channelId": 1,
            "subChannel": "Direct",
            "folioId": 789,
            "guaranteePolicyId": 1,
            "cancellationPolicyId": 1,
            "userId": 100,
            "travelAgentId": None,
            "campaignId": None,
            "typeId": 1,
            "rateTypeId": 1,
            "unitCodeId": 1,
            "cancelledById": None,
            "paymentMethodId": 1,
            "quoteId": None,
            "promoCodeId": None,
            "groupId": 1,
            "holdExpiresAt": None,
            "isTaxable": True,
            "inviteUuid": None,
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "source": "Web",
            "agreementStatus": "not-needed",
            "automatePayment": False,
            "revenueRealizedMethod": "nightly",
            "paymentPlan": [
                {"date": "2024-01-15", "amount": "600.00"},
                {"date": "2024-01-20", "amount": "600.00"},
            ],
            "rateType": {"id": 1, "name": "Standard", "code": "STD"},
            "travelInsuranceProducts": [],
            "_embedded": {
                "unit": {
                    "id": 789,
                    "name": "Luxury Apartment",
                    "shortName": "LUX-APT",
                    "unitCode": "A101",
                },
                "contact": {
                    "id": 456,
                    "firstName": "John",
                    "lastName": "Doe",
                    "primaryEmail": "john.doe@example.com",
                },
            },
            "_links": {
                "self": {"href": "/api/v2/pms/reservations/12345"},
                "logs": {"href": "/api/v2/pms/reservations/12345/logs"},
                "notes": {"href": "/api/v2/pms/reservations/12345/notes"},
            },
        }

        # Configurar el mock
        mock_api_client.get.return_value = mock_response

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)

        # Verificaciones
        assert result == mock_response
        mock_api_client.get.assert_called_once_with(
            f"api/v2/pms/reservations/{self.valid_reservation_id}"
        )

    @patch("src.trackhs_mcp.server.api_client")
    def test_get_reservation_api_client_none(self, mock_api_client):
        """Test cuando api_client es None"""
        mock_api_client.__bool__ = Mock(return_value=False)
        mock_api_client = None

        with pytest.raises(ToolError, match="Cliente API no disponible"):
            get_reservation(self.valid_reservation_id)

    @patch("src.trackhs_mcp.server.api_client")
    def test_get_reservation_not_found(self, mock_api_client):
        """Test cuando la reserva no existe (404)"""
        mock_api_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(ToolError, match="Reserva 99999 no encontrada en TrackHS"):
            get_reservation(self.nonexistent_reservation_id)

    @patch("src.trackhs_mcp.server.api_client")
    def test_get_reservation_api_error(self, mock_api_client):
        """Test cuando hay un error de API"""
        mock_api_client.get.side_effect = Exception("500 Internal Server Error")

        with pytest.raises(ToolError, match="Error obteniendo reserva"):
            get_reservation(self.valid_reservation_id)

    def test_get_reservation_invalid_id(self):
        """Test con ID de reserva inválido"""
        with pytest.raises(ValueError):
            get_reservation(self.invalid_reservation_id)

    def test_reservation_detail_output_schema_validation(self):
        """Test que el schema ReservationDetailOutput valida correctamente"""
        # Datos de prueba válidos
        valid_data = {
            "id": 12345,
            "currency": "USD",
            "unitId": 789,
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "status": "Confirmed",
            "nights": 5.0,
            "isUnitLocked": False,
            "isUnitAssigned": True,
            "occupants": [],
            "securityDeposit": {"required": "200.00", "remaining": 200},
            "updatedAt": "2024-01-10T10:30:00Z",
            "createdAt": "2024-01-10T10:00:00Z",
            "bookedAt": "2024-01-10T10:00:00Z",
            "guestBreakdown": {"grossRent": "1000.00"},
            "ownerBreakdown": {"grossRent": "1000.00"},
            "contactId": 456,
            "channelId": 1,
            "folioId": 789,
            "guaranteePolicyId": 1,
            "cancellationPolicyId": 1,
            "userId": 100,
            "typeId": 1,
            "rateTypeId": 1,
            "unitCodeId": 1,
            "groupId": 1,
            "isTaxable": True,
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "source": "Web",
            "agreementStatus": "not-needed",
            "automatePayment": False,
            "revenueRealizedMethod": "nightly",
            "paymentPlan": [],
            "rateType": {"id": 1, "name": "Standard"},
            "travelInsuranceProducts": [],
            "embedded": {"unit": {"id": 789}},
            "links": {"self": {"href": "/api/v2/pms/reservations/12345"}},
            "additional_data": {},
        }

        # Debe crear el modelo sin errores
        reservation = ReservationDetailOutput(**valid_data)
        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.status == "Confirmed"

    def test_reservation_detail_output_schema_optional_fields(self):
        """Test que los campos opcionales funcionan correctamente"""
        # Datos mínimos requeridos
        minimal_data = {"id": 12345}

        # Debe crear el modelo con solo el campo requerido
        reservation = ReservationDetailOutput(**minimal_data)
        assert reservation.id == 12345
        assert reservation.currency is None
        assert reservation.unitId is None

    def test_reservation_detail_output_schema_field_types(self):
        """Test que los tipos de campos son correctos"""
        data = {
            "id": 12345,
            "alternates": ["ALT1", "ALT2"],
            "currency": "USD",
            "unitId": 789,
            "nights": 5.5,
            "earlyArrival": True,
            "lateDeparture": False,
            "isUnitLocked": True,
            "occupants": [{"typeId": 1, "name": "Adult"}],
            "securityDeposit": {"required": "200.00"},
            "paymentPlan": [{"date": "2024-01-15", "amount": "600.00"}],
            "travelInsuranceProducts": [{"id": 1, "status": "optin"}],
            "embedded": {"unit": {"id": 789}},
            "links": {"self": {"href": "/api/v2/pms/reservations/12345"}},
            "additional_data": {"custom": "value"},
        }

        reservation = ReservationDetailOutput(**data)

        # Verificar tipos
        assert isinstance(reservation.id, int)
        assert isinstance(reservation.alternates, list)
        assert isinstance(reservation.currency, str)
        assert isinstance(reservation.nights, float)
        assert isinstance(reservation.earlyArrival, bool)
        assert isinstance(reservation.occupants, list)
        assert isinstance(reservation.securityDeposit, dict)
        assert isinstance(reservation.paymentPlan, list)
        assert isinstance(reservation.travelInsuranceProducts, list)
        assert isinstance(reservation.embedded, dict)
        assert isinstance(reservation.links, dict)
        assert isinstance(reservation.additional_data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
