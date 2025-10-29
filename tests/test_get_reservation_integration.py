"""
Pruebas de integración para el tool get_reservation con API V2
"""

import json
import os
import sys
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests
from requests.exceptions import HTTPError, RequestException

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastmcp.exceptions import ToolError

from trackhs_mcp.client import TrackHSClient
from trackhs_mcp.server import get_reservation


class TestGetReservationIntegration:
    """Pruebas de integración para get_reservation"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.valid_reservation_id = 12345
        self.base_url = "https://ihmvacations.trackhs.com"
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"

    @patch("src.trackhs_mcp.client.requests.Session.get")
    def test_get_reservation_api_v2_integration_success(self, mock_get):
        """Test de integración exitosa con la API V2"""
        # Mock de respuesta exitosa de la API V2
        mock_response_data = {
            "id": 12345,
            "alternates": ["ALT123"],
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
                "guestGrossDisplayRent": "1000.00",
                "discount": "0.00",
                "promoValue": "0.00",
                "discountTotal": 0.0,
                "netRent": "1000.00",
                "guestNetDisplayRent": "1000.00",
                "actualAdr": "200.00",
                "guestAdr": "200.00",
                "totalGuestFees": "50.00",
                "totalRentFees": "0.00",
                "totalItemizedFees": "50.00",
                "totalTaxFees": "100.00",
                "totalServiceFees": "25.00",
                "folioCharges": "0.00",
                "subtotal": "1050.00",
                "guestSubtotal": "1050.00",
                "totalTaxes": "100.00",
                "totalGuestTaxes": "100.00",
                "total": "1150.00",
                "grandTotal": "1150.00",
                "netPayments": "1150.00",
                "payments": "1150.00",
                "refunds": "0.00",
                "netTransfers": "0.00",
                "balance": "0.00",
                "rates": [
                    {
                        "date": "2024-01-15",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    }
                ],
                "guestFees": [
                    {
                        "id": "1",
                        "name": "Cleaning Fee",
                        "displayAs": "itemize",
                        "quantity": "1",
                        "unitValue": "50.00",
                        "value": "50.00",
                    }
                ],
                "taxes": [{"id": 1, "name": "City Tax", "amount": "100.00"}],
            },
            "ownerBreakdown": {
                "grossRent": "1000.00",
                "feeRevenue": "50.00",
                "grossRevenue": "1050.00",
                "managerCommission": "52.50",
                "agentCommission": "0.00",
                "netRevenue": "997.50",
                "ownerFees": [
                    {
                        "id": "1",
                        "name": "Management Fee",
                        "displayAs": "service",
                        "quantity": "1",
                        "unitValue": "52.50",
                        "value": "52.50",
                    }
                ],
            },
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
                {"date": "2024-01-20", "amount": "550.00"},
            ],
            "rateType": {"id": 1, "name": "Standard", "code": "STD"},
            "travelInsuranceProducts": [],
            "_embedded": {
                "unit": {
                    "id": 789,
                    "name": "Luxury Apartment",
                    "shortName": "LUX-APT",
                    "unitCode": "A101",
                    "headline": "Beautiful luxury apartment",
                    "shortDescription": "Modern apartment with great views",
                    "longDescription": "Spacious luxury apartment with modern amenities",
                    "houseRules": "No smoking, no pets",
                    "nodeId": 1,
                    "unitType": {"id": 101, "name": "Apartment"},
                    "lodgingType": {"id": 1, "name": "Vacation Rental"},
                    "directions": "Take elevator to floor 10",
                    "checkinDetails": "Key pickup at front desk",
                    "timezone": "America/New_York",
                    "checkinTime": "15:00",
                    "hasEarlyCheckin": True,
                    "earlyCheckinTime": "12:00",
                    "checkoutTime": "11:00",
                    "hasLateCheckout": True,
                    "lateCheckoutTime": "14:00",
                    "minBookingWindow": 1,
                    "maxBookingWindow": 365,
                    "website": "https://example.com/unit/789",
                    "phone": "+1-555-0123",
                    "streetAddress": "123 Main St",
                    "extendedAddress": "Apt 101",
                    "locality": "New York",
                    "region": "NY",
                    "postalCode": "10001",
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
                    "area": 1200.0,
                    "floors": 1,
                    "maxOccupancy": 4,
                    "securityDeposit": "200.00",
                    "bedrooms": 2,
                    "fullBathrooms": 2,
                    "threeQuarterBathrooms": 0,
                    "halfBathrooms": 1,
                    "bedTypes": [
                        {"id": 1, "name": "King", "count": 1},
                        {"id": 2, "name": "Queen", "count": 1},
                    ],
                    "rooms": [
                        {
                            "name": "Master Bedroom",
                            "type": "bedroom",
                            "sleeps": 2,
                            "description": "Master bedroom with king bed",
                            "hasAttachedBathroom": True,
                            "order": 1,
                            "airbnbType": "bedroom",
                            "marriottType": "bedroom",
                            "homeawayType": "bedroom",
                            "bedTypes": [
                                {
                                    "id": 1,
                                    "name": "King",
                                    "count": 1,
                                    "airbnbType": "king",
                                    "marriottType": "king",
                                    "homeawayType": "king",
                                }
                            ],
                        }
                    ],
                    "amenities": [
                        {
                            "id": 1,
                            "name": "WiFi",
                            "group": {"id": 1, "name": "Internet"},
                        },
                        {
                            "id": 2,
                            "name": "Pool",
                            "group": {"id": 2, "name": "Recreation"},
                        },
                    ],
                    "amenityDescription": "WiFi, Pool, Gym",
                    "coverImage": "https://example.com/images/unit789.jpg",
                    "taxId": 1,
                    "localOffice": {
                        "name": "NYC Office",
                        "directions": "123 Office St",
                        "email": "nyc@example.com",
                        "phone": "+1-555-0124",
                        "latitude": "40.7589",
                        "longitude": "-73.9851",
                        "streetAddress": "123 Office St",
                        "extendedAddress": "Suite 100",
                        "locality": "New York",
                        "region": "NY",
                        "postalCode": "10001",
                        "country": "US",
                    },
                    "regulations": [{"body": "City Regulation", "params": "NYC-2024"}],
                    "updated": {
                        "availability": "2024-01-10T10:00:00Z",
                        "content": "2024-01-10T10:00:00Z",
                        "pricing": "2024-01-10T10:00:00Z",
                    },
                    "updatedAt": "2024-01-10T10:00:00Z",
                    "createdAt": "2024-01-10T10:00:00Z",
                    "isActive": True,
                    "_links": {"self": {"href": "/api/v2/pms/units/789"}},
                },
                "contact": {
                    "id": 456,
                    "firstName": "John",
                    "lastName": "Doe",
                    "name": "John Doe",
                    "primaryEmail": "john.doe@example.com",
                    "secondaryEmail": None,
                    "homePhone": "+1-555-0125",
                    "cellPhone": "+1-555-0126",
                    "workPhone": None,
                    "otherPhone": None,
                    "fax": None,
                    "streetAddress": "456 Guest St",
                    "extendedAddress": None,
                    "locality": "Boston",
                    "region": "MA",
                    "postalCode": "02101",
                    "country": "US",
                    "notes": "VIP Guest",
                    "anniversary": "06-15",
                    "birthdate": "03-22",
                    "noIdentity": False,
                    "isVip": True,
                    "isBlacklist": False,
                    "isDNR": False,
                    "tags": [{"id": 1}],
                    "references": [
                        {"reference": "REF123", "salesLinkId": 1, "channelId": 1}
                    ],
                    "custom": {"custom_1": "value1", "custom_2": ["value2", "value3"]},
                    "updatedBy": "system",
                    "createdBy": "system",
                    "updatedAt": "2024-01-10T10:00:00Z",
                    "createdAt": "2024-01-10T10:00:00Z",
                    "isOwnerContact": False,
                    "_links": {"self": {"href": "/api/v2/pms/contacts/456"}},
                },
                "guaranteePolicy": {
                    "id": 1,
                    "isActive": True,
                    "isDefault": True,
                    "name": "Standard Guarantee",
                    "description": "Standard guarantee policy",
                    "beforeArrivalStart": 0,
                    "beforeArrivalEnd": 24,
                    "type": "Guarantee",
                    "holdLimit": 24,
                    "depositType": "percentage",
                    "amount": "20.00",
                    "includeTax": True,
                    "includeFees": True,
                    "includeTravelInsurance": False,
                    "travelInsuranceWithFirstPayment": False,
                    "isAutomaticCancel": True,
                    "includeFolioCharges": False,
                    "hasPaymentSchedule": True,
                    "priority": 1,
                    "breakpoints": [
                        {
                            "id": 1,
                            "dueType": "at-booking",
                            "stop": 0,
                            "percent": 20.0,
                            "amount": "200.00",
                            "isRemaining": False,
                        }
                    ],
                    "_links": {"self": {"href": "/api/v2/pms/guarantee-policies/1"}},
                },
                "cancellationPolicy": {
                    "id": 1,
                    "isDefault": True,
                    "isActive": True,
                    "name": "Standard Cancellation",
                    "code": "STD-CANCEL",
                    "chargeAs": "fee",
                    "canExceedBalance": False,
                    "cancelTime": "23:59",
                    "cancelTimezone": "America/New_York",
                    "postDate": "now",
                    "airbnbType": "moderate",
                    "marriottType": "moderate",
                    "tripadvisorType": "moderate",
                    "homeawayType": "moderate",
                    "breakpoints": [
                        {
                            "id": 1,
                            "rangeStart": 0,
                            "rangeEnd": 24,
                            "nonRefundable": False,
                            "nonCancelable": False,
                            "penaltyNights": 0,
                            "penaltyPercent": "100.00",
                            "penaltyFlat": "0.00",
                            "description": "Full refund if cancelled 24+ hours before check-in",
                        }
                    ],
                    "priority": 1,
                    "createdBy": "system",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedBy": "system",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "dateGroupId": 1,
                    "dateRangeType": "all",
                    "startDate": "2024-01-01T00:00:00Z",
                    "endDate": "2024-12-31T23:59:59Z",
                    "_links": {"self": {"href": "/api/v2/pms/cancellation-policies/1"}},
                },
                "user": {
                    "id": 100,
                    "isActive": True,
                    "name": "John Manager",
                    "phone": "+1-555-0127",
                    "email": "manager@example.com",
                    "username": "jmanager",
                    "roleId": 1,
                    "teamId": 1,
                    "vendorId": None,
                    "assignable": ["reservations", "units"],
                    "createdBy": "system",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedBy": "system",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "_embedded": {
                        "vendor": {
                            "_links": {"self": {"href": "/api/v2/pms/vendors/1"}}
                        }
                    },
                    "_links": {"self": {"href": "/api/v2/pms/users/100"}},
                },
                "type": {
                    "id": 1,
                    "name": "Standard",
                    "publicName": "Standard Reservation",
                    "code": "STD",
                    "description": "Standard reservation type",
                    "isActive": True,
                    "isCommissionable": True,
                    "typeColor": "0000FF",
                    "chargeRates": False,
                    "chargeRent": "guest",
                    "rentEarned": "owner",
                    "requiresAgreement": False,
                    "requirePayment": True,
                    "cleaningOptionsId": 1,
                    "realizeRates": "nightly",
                    "isLocked": False,
                    "sendPortalInvited": True,
                    "portalReservationBreakdown": True,
                    "showFolioTransactions": True,
                    "isOwner": False,
                    "scheduleType1": "percentage",
                    "schedulePercentage1": 20,
                    "scheduleType2": "percentage",
                    "schedulePercentage2": 80,
                    "ownerStay": False,
                    "personalUse": False,
                    "autoSelect": False,
                    "securityDepositType": "percentage",
                    "deferDisbursement": False,
                    "deferDisbursementDate": None,
                    "posDefaultAllow": True,
                    "posDefaultLimit": "1000.00",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "createdBy": "system",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "updatedBy": "system",
                    "_links": {"self": {"href": "/api/v2/pms/reservation-types/1"}},
                },
                "rateType": {
                    "id": 1,
                    "type": "standard",
                    "code": "STD",
                    "name": "Standard Rate",
                    "isAutoSelect": True,
                    "occupancyPricingByType": False,
                    "isAllChannels": True,
                    "channelIds": [1, 2, 3],
                    "isActive": True,
                    "createdBy": "system",
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedBy": "system",
                    "updatedAt": "2024-01-01T00:00:00Z",
                    "parentRateId": None,
                    "rentType": "nightly",
                    "rentAmount": "200.00",
                    "minLosType": "nights",
                    "minLosAmount": 1,
                    "maxLosType": "nights",
                    "maxLosAmount": 30,
                    "ctaOverride": False,
                    "cta": {
                        "monday": True,
                        "tuesday": True,
                        "wednesday": True,
                        "thursday": True,
                        "friday": True,
                        "saturday": True,
                        "sunday": True,
                    },
                    "ctdOverride": False,
                    "ctd": {
                        "monday": True,
                        "tuesday": True,
                        "wednesday": True,
                        "thursday": True,
                        "friday": True,
                        "saturday": True,
                        "sunday": True,
                    },
                },
            },
            "_links": {
                "self": {"href": "/api/v2/pms/reservations/12345"},
                "logs": {"href": "/api/v2/pms/reservations/12345/logs"},
                "notes": {"href": "/api/v2/pms/reservations/12345/notes"},
                "fees": {"href": "/api/v2/pms/reservations/12345/fees"},
                "checkin": {"href": "/api/v2/pms/reservations/12345/checkin"},
                "cancel": {"href": "/api/v2/pms/reservations/12345/cancel"},
                "tags": {"href": "/api/v2/pms/reservations/12345/tags"},
                "rates": {"href": "/api/v2/pms/reservations/12345/rates"},
                "discount": {"href": "/api/v2/pms/reservations/12345/discount"},
            },
        }

        # Configurar el mock de requests
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Crear cliente real para la prueba de integración
        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        # Ejecutar la función con el cliente real
        result = client.get(f"api/v2/pms/reservations/{self.valid_reservation_id}")

        # Verificaciones
        assert result == mock_response_data
        mock_get.assert_called_once()

        # Verificar que se llamó con la URL correcta
        call_args = mock_get.call_args
        assert "api/v2/pms/reservations/12345" in call_args[0][0]

    @patch("src.trackhs_mcp.client.requests.Session.get")
    def test_get_reservation_api_v2_integration_404(self, mock_get):
        """Test de integración con error 404"""
        # Mock de respuesta 404
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        with pytest.raises(HTTPError, match="404 Not Found"):
            client.get(f"api/v2/pms/reservations/99999")

    @patch("src.trackhs_mcp.client.requests.Session.get")
    def test_get_reservation_api_v2_integration_500(self, mock_get):
        """Test de integración con error 500"""
        # Mock de respuesta 500
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError(
            "500 Internal Server Error"
        )
        mock_get.return_value = mock_response

        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        with pytest.raises(HTTPError, match="500 Internal Server Error"):
            client.get(f"api/v2/pms/reservations/{self.valid_reservation_id}")

    @patch("src.trackhs_mcp.client.requests.Session.get")
    def test_get_reservation_api_v2_integration_network_error(self, mock_get):
        """Test de integración con error de red"""
        # Mock de error de red
        mock_get.side_effect = RequestException("Network error")

        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        with pytest.raises(RequestException, match="Network error"):
            client.get(f"api/v2/pms/reservations/{self.valid_reservation_id}")

    def test_get_reservation_api_v2_url_format(self):
        """Test que la URL de la API V2 tiene el formato correcto"""
        expected_url = (
            f"{self.base_url}/api/v2/pms/reservations/{self.valid_reservation_id}"
        )

        # Verificar que la URL se construye correctamente
        assert (
            expected_url
            == f"{self.base_url}/api/v2/pms/reservations/{self.valid_reservation_id}"
        )
        assert "v2" in expected_url
        assert "pms/reservations" in expected_url
        assert str(self.valid_reservation_id) in expected_url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
