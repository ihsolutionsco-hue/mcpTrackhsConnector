"""
Pruebas end-to-end para el tool get_reservation con API V2
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastmcp.exceptions import ToolError

from trackhs_mcp.schemas import ReservationDetailOutput
from trackhs_mcp.server import get_reservation, mcp


class TestGetReservationE2E:
    """Pruebas end-to-end para get_reservation"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.valid_reservation_id = 12345
        self.test_reservation_data = {
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
                },
                {
                    "typeId": 2,
                    "name": "Child",
                    "handle": "child",
                    "quantity": 1,
                    "included": True,
                    "extraQuantity": 0,
                    "ratePerPersonPerStay": "0.00",
                    "ratePerStay": "0.00",
                },
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
                "totalGuestFees": "75.00",
                "totalRentFees": "0.00",
                "totalItemizedFees": "75.00",
                "totalTaxFees": "100.00",
                "totalServiceFees": "25.00",
                "folioCharges": "0.00",
                "subtotal": "1075.00",
                "guestSubtotal": "1075.00",
                "totalTaxes": "100.00",
                "totalGuestTaxes": "100.00",
                "total": "1175.00",
                "grandTotal": "1175.00",
                "netPayments": "1175.00",
                "payments": "1175.00",
                "refunds": "0.00",
                "netTransfers": "0.00",
                "balance": "0.00",
                "rates": [
                    {
                        "date": "2024-01-15",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    },
                    {
                        "date": "2024-01-16",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    },
                    {
                        "date": "2024-01-17",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    },
                    {
                        "date": "2024-01-18",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    },
                    {
                        "date": "2024-01-19",
                        "rate": "200.00",
                        "nights": 1,
                        "isQuoted": True,
                    },
                ],
                "guestFees": [
                    {
                        "id": "1",
                        "name": "Cleaning Fee",
                        "displayAs": "itemize",
                        "quantity": "1",
                        "unitValue": "50.00",
                        "value": "50.00",
                    },
                    {
                        "id": "2",
                        "name": "Service Fee",
                        "displayAs": "service",
                        "quantity": "1",
                        "unitValue": "25.00",
                        "value": "25.00",
                    },
                ],
                "taxes": [{"id": 1, "name": "City Tax", "amount": "100.00"}],
            },
            "ownerBreakdown": {
                "grossRent": "1000.00",
                "feeRevenue": "75.00",
                "grossRevenue": "1075.00",
                "managerCommission": "53.75",
                "agentCommission": "0.00",
                "netRevenue": "1021.25",
                "ownerFees": [
                    {
                        "id": "1",
                        "name": "Management Fee",
                        "displayAs": "service",
                        "quantity": "1",
                        "unitValue": "53.75",
                        "value": "53.75",
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
                {"date": "2024-01-20", "amount": "575.00"},
            ],
            "rateType": {"id": 1, "name": "Standard", "code": "STD"},
            "travelInsuranceProducts": [],
            "_embedded": {
                "unit": {
                    "id": 789,
                    "name": "Luxury Apartment",
                    "shortName": "LUX-APT",
                    "unitCode": "A101",
                    "headline": "Beautiful luxury apartment with city views",
                    "shortDescription": "Modern 2-bedroom apartment with great amenities",
                    "longDescription": "Spacious luxury apartment with modern amenities, located in the heart of the city with stunning views",
                    "houseRules": "No smoking, no pets, no parties after 10 PM",
                    "nodeId": 1,
                    "unitType": {"id": 101, "name": "Apartment"},
                    "lodgingType": {"id": 1, "name": "Vacation Rental"},
                    "directions": "Take elevator to floor 10, turn left, unit A101",
                    "checkinDetails": "Key pickup at front desk, valid ID required",
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
                            "description": "Master bedroom with king bed and en-suite bathroom",
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
                        },
                        {
                            "name": "Guest Bedroom",
                            "type": "bedroom",
                            "sleeps": 2,
                            "description": "Guest bedroom with queen bed",
                            "hasAttachedBathroom": False,
                            "order": 2,
                            "airbnbType": "bedroom",
                            "marriottType": "bedroom",
                            "homeawayType": "bedroom",
                            "bedTypes": [
                                {
                                    "id": 2,
                                    "name": "Queen",
                                    "count": 1,
                                    "airbnbType": "queen",
                                    "marriottType": "queen",
                                    "homeawayType": "queen",
                                }
                            ],
                        },
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
                        {
                            "id": 3,
                            "name": "Gym",
                            "group": {"id": 2, "name": "Recreation"},
                        },
                        {
                            "id": 4,
                            "name": "Parking",
                            "group": {"id": 3, "name": "Transportation"},
                        },
                    ],
                    "amenityDescription": "WiFi, Pool, Gym, Parking",
                    "coverImage": "https://example.com/images/unit789.jpg",
                    "taxId": 1,
                    "localOffice": {
                        "name": "NYC Office",
                        "directions": "123 Office St, Suite 100",
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
                    "regulations": [
                        {"body": "City Regulation", "params": "NYC-2024"},
                        {"body": "Building Rules", "params": "BLD-2024"},
                    ],
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
                    "secondaryEmail": "john.doe.backup@example.com",
                    "homePhone": "+1-555-0125",
                    "cellPhone": "+1-555-0126",
                    "workPhone": "+1-555-0127",
                    "otherPhone": None,
                    "fax": None,
                    "streetAddress": "456 Guest St",
                    "extendedAddress": "Apt 2B",
                    "locality": "Boston",
                    "region": "MA",
                    "postalCode": "02101",
                    "country": "US",
                    "notes": "VIP Guest, prefers high floors",
                    "anniversary": "06-15",
                    "birthdate": "03-22",
                    "noIdentity": False,
                    "isVip": True,
                    "isBlacklist": False,
                    "isDNR": False,
                    "tags": [{"id": 1}, {"id": 2}],
                    "references": [
                        {"reference": "REF123", "salesLinkId": 1, "channelId": 1},
                        {"reference": "REF456", "salesLinkId": 2, "channelId": 2},
                    ],
                    "custom": {
                        "custom_1": "VIP Status",
                        "custom_2": ["High Priority", "Repeat Guest"],
                        "custom_3": "Loyalty Member",
                    },
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
                    "description": "Standard guarantee policy for all reservations",
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
                        },
                        {
                            "id": 2,
                            "dueType": "before-checkin",
                            "stop": 7,
                            "percent": 50.0,
                            "amount": "500.00",
                            "isRemaining": False,
                        },
                        {
                            "id": 3,
                            "dueType": "at-checkin",
                            "stop": 0,
                            "percent": 30.0,
                            "amount": "300.00",
                            "isRemaining": True,
                        },
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
                        },
                        {
                            "id": 2,
                            "rangeStart": 24,
                            "rangeEnd": 72,
                            "nonRefundable": False,
                            "nonCancelable": False,
                            "penaltyNights": 1,
                            "penaltyPercent": "50.00",
                            "penaltyFlat": "0.00",
                            "description": "50% refund if cancelled 24-72 hours before check-in",
                        },
                        {
                            "id": 3,
                            "rangeStart": 72,
                            "rangeEnd": 0,
                            "nonRefundable": True,
                            "nonCancelable": False,
                            "penaltyNights": 0,
                            "penaltyPercent": "0.00",
                            "penaltyFlat": "0.00",
                            "description": "No refund if cancelled less than 72 hours before check-in",
                        },
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
                    "assignable": ["reservations", "units", "contacts"],
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
                    "description": "Standard reservation type for regular bookings",
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

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_get_reservation_complete_flow(self, mock_api_client):
        """Test end-to-end completo del flujo get_reservation"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)

        # Verificaciones básicas
        assert result is not None
        assert isinstance(result, dict)
        assert result["id"] == self.valid_reservation_id

        # Verificar que se llamó con la URL correcta de la API V2
        mock_api_client.get.assert_called_once_with(
            f"api/v2/pms/reservations/{self.valid_reservation_id}"
        )

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_data_validation(self, mock_api_client):
        """Test end-to-end de validación de datos de reserva"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)

        # Validar con el schema Pydantic
        reservation = ReservationDetailOutput(**result)

        # Verificaciones de campos básicos
        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.unitId == 789
        assert reservation.status == "Confirmed"
        assert reservation.nights == 5.0

        # Verificaciones de fechas
        assert reservation.arrivalDate == "2024-01-15"
        assert reservation.departureDate == "2024-01-20"
        assert reservation.arrivalTime == "2024-01-15T15:00:00Z"
        assert reservation.departureTime == "2024-01-20T11:00:00Z"

        # Verificaciones de estado
        assert reservation.isUnitLocked == False
        assert reservation.isUnitAssigned == True
        assert reservation.isChannelLocked == False

        # Verificaciones de ocupantes
        assert len(reservation.occupants) == 2
        assert reservation.occupants[0]["name"] == "Adult"
        assert reservation.occupants[1]["name"] == "Child"

        # Verificaciones de depósito de seguridad
        assert reservation.securityDeposit["required"] == "200.00"
        assert reservation.securityDeposit["remaining"] == 200

        # Verificaciones de desglose financiero
        assert reservation.guestBreakdown["grossRent"] == "1000.00"
        assert reservation.guestBreakdown["netRent"] == "1000.00"
        assert reservation.guestBreakdown["total"] == "1175.00"
        assert reservation.guestBreakdown["balance"] == "0.00"

        # Verificaciones de desglose del propietario
        assert reservation.ownerBreakdown["grossRent"] == "1000.00"
        assert reservation.ownerBreakdown["netRevenue"] == "1021.25"

        # Verificaciones de IDs de referencia
        assert reservation.contactId == 456
        assert reservation.channelId == 1
        assert reservation.folioId == 789
        assert reservation.userId == 100

        # Verificaciones de datos embebidos
        assert reservation.embedded is not None
        assert "unit" in reservation.embedded
        assert "contact" in reservation.embedded
        assert "guaranteePolicy" in reservation.embedded
        assert "cancellationPolicy" in reservation.embedded
        assert "user" in reservation.embedded
        assert "type" in reservation.embedded
        assert "rateType" in reservation.embedded

        # Verificaciones de enlaces
        assert reservation.links is not None
        assert "self" in reservation.links
        assert "logs" in reservation.links
        assert "notes" in reservation.links

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_financial_breakdown(self, mock_api_client):
        """Test end-to-end del desglose financiero detallado"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)
        reservation = ReservationDetailOutput(**result)

        # Verificar desglose del huésped
        guest_breakdown = reservation.guestBreakdown
        assert guest_breakdown["grossRent"] == "1000.00"
        assert guest_breakdown["guestGrossDisplayRent"] == "1000.00"
        assert guest_breakdown["discount"] == "0.00"
        assert guest_breakdown["promoValue"] == "0.00"
        assert guest_breakdown["discountTotal"] == 0.0
        assert guest_breakdown["netRent"] == "1000.00"
        assert guest_breakdown["guestNetDisplayRent"] == "1000.00"
        assert guest_breakdown["actualAdr"] == "200.00"
        assert guest_breakdown["guestAdr"] == "200.00"
        assert guest_breakdown["totalGuestFees"] == "75.00"
        assert guest_breakdown["totalRentFees"] == "0.00"
        assert guest_breakdown["totalItemizedFees"] == "75.00"
        assert guest_breakdown["totalTaxFees"] == "100.00"
        assert guest_breakdown["totalServiceFees"] == "25.00"
        assert guest_breakdown["folioCharges"] == "0.00"
        assert guest_breakdown["subtotal"] == "1075.00"
        assert guest_breakdown["guestSubtotal"] == "1075.00"
        assert guest_breakdown["totalTaxes"] == "100.00"
        assert guest_breakdown["totalGuestTaxes"] == "100.00"
        assert guest_breakdown["total"] == "1175.00"
        assert guest_breakdown["grandTotal"] == "1175.00"
        assert guest_breakdown["netPayments"] == "1175.00"
        assert guest_breakdown["payments"] == "1175.00"
        assert guest_breakdown["refunds"] == "0.00"
        assert guest_breakdown["netTransfers"] == "0.00"
        assert guest_breakdown["balance"] == "0.00"

        # Verificar tarifas por noche
        rates = guest_breakdown["rates"]
        assert len(rates) == 5
        for rate in rates:
            assert rate["rate"] == "200.00"
            assert rate["nights"] == 1
            assert rate["isQuoted"] == True

        # Verificar tarifas del huésped
        guest_fees = guest_breakdown["guestFees"]
        assert len(guest_fees) == 2
        assert guest_fees[0]["name"] == "Cleaning Fee"
        assert guest_fees[0]["value"] == "50.00"
        assert guest_fees[1]["name"] == "Service Fee"
        assert guest_fees[1]["value"] == "25.00"

        # Verificar impuestos
        taxes = guest_breakdown["taxes"]
        assert len(taxes) == 1
        assert taxes[0]["name"] == "City Tax"
        assert taxes[0]["amount"] == "100.00"

        # Verificar desglose del propietario
        owner_breakdown = reservation.ownerBreakdown
        assert owner_breakdown["grossRent"] == "1000.00"
        assert owner_breakdown["feeRevenue"] == "75.00"
        assert owner_breakdown["grossRevenue"] == "1075.00"
        assert owner_breakdown["managerCommission"] == "53.75"
        assert owner_breakdown["agentCommission"] == "0.00"
        assert owner_breakdown["netRevenue"] == "1021.25"

        # Verificar tarifas del propietario
        owner_fees = owner_breakdown["ownerFees"]
        assert len(owner_fees) == 1
        assert owner_fees[0]["name"] == "Management Fee"
        assert owner_fees[0]["value"] == "53.75"

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_embedded_data(self, mock_api_client):
        """Test end-to-end de datos embebidos"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)
        reservation = ReservationDetailOutput(**result)

        # Verificar datos de la unidad
        unit = reservation.embedded["unit"]
        assert unit["id"] == 789
        assert unit["name"] == "Luxury Apartment"
        assert unit["unitCode"] == "A101"
        assert unit["bedrooms"] == 2
        assert unit["fullBathrooms"] == 2
        assert unit["maxOccupancy"] == 4
        assert unit["petsFriendly"] == False
        assert unit["smokingAllowed"] == False
        assert unit["childrenAllowed"] == True
        assert unit["isAccessible"] == True

        # Verificar amenidades
        amenities = unit["amenities"]
        assert len(amenities) == 4
        amenity_names = [a["name"] for a in amenities]
        assert "WiFi" in amenity_names
        assert "Pool" in amenity_names
        assert "Gym" in amenity_names
        assert "Parking" in amenity_names

        # Verificar habitaciones
        rooms = unit["rooms"]
        assert len(rooms) == 2
        assert rooms[0]["name"] == "Master Bedroom"
        assert rooms[0]["type"] == "bedroom"
        assert rooms[0]["hasAttachedBathroom"] == True
        assert rooms[1]["name"] == "Guest Bedroom"
        assert rooms[1]["type"] == "bedroom"
        assert rooms[1]["hasAttachedBathroom"] == False

        # Verificar datos del contacto
        contact = reservation.embedded["contact"]
        assert contact["id"] == 456
        assert contact["firstName"] == "John"
        assert contact["lastName"] == "Doe"
        assert contact["primaryEmail"] == "john.doe@example.com"
        assert contact["isVip"] == True
        assert contact["isBlacklist"] == False

        # Verificar política de garantía
        guarantee_policy = reservation.embedded["guaranteePolicy"]
        assert guarantee_policy["id"] == 1
        assert guarantee_policy["name"] == "Standard Guarantee"
        assert guarantee_policy["type"] == "Guarantee"
        assert guarantee_policy["amount"] == "20.00"
        assert len(guarantee_policy["breakpoints"]) == 3

        # Verificar política de cancelación
        cancellation_policy = reservation.embedded["cancellationPolicy"]
        assert cancellation_policy["id"] == 1
        assert cancellation_policy["name"] == "Standard Cancellation"
        assert cancellation_policy["code"] == "STD-CANCEL"
        assert len(cancellation_policy["breakpoints"]) == 3

        # Verificar datos del usuario
        user = reservation.embedded["user"]
        assert user["id"] == 100
        assert user["name"] == "John Manager"
        assert user["email"] == "manager@example.com"
        assert user["isActive"] == True

        # Verificar tipo de reserva
        reservation_type = reservation.embedded["type"]
        assert reservation_type["id"] == 1
        assert reservation_type["name"] == "Standard"
        assert reservation_type["code"] == "STD"
        assert reservation_type["isActive"] == True

        # Verificar tipo de tarifa
        rate_type = reservation.embedded["rateType"]
        assert rate_type["id"] == 1
        assert rate_type["name"] == "Standard Rate"
        assert rate_type["code"] == "STD"
        assert rate_type["isActive"] == True

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_links(self, mock_api_client):
        """Test end-to-end de enlaces relacionados"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Ejecutar la función
        result = get_reservation(self.valid_reservation_id)
        reservation = ReservationDetailOutput(**result)

        # Verificar enlaces principales
        links = reservation.links
        assert "self" in links
        assert "logs" in links
        assert "notes" in links
        assert "fees" in links
        assert "checkin" in links
        assert "cancel" in links
        assert "tags" in links
        assert "rates" in links
        assert "discount" in links

        # Verificar URLs de enlaces
        assert links["self"]["href"] == "/api/v2/pms/reservations/12345"
        assert links["logs"]["href"] == "/api/v2/pms/reservations/12345/logs"
        assert links["notes"]["href"] == "/api/v2/pms/reservations/12345/notes"
        assert links["fees"]["href"] == "/api/v2/pms/reservations/12345/fees"
        assert links["checkin"]["href"] == "/api/v2/pms/reservations/12345/checkin"
        assert links["cancel"]["href"] == "/api/v2/pms/reservations/12345/cancel"
        assert links["tags"]["href"] == "/api/v2/pms/reservations/12345/tags"
        assert links["rates"]["href"] == "/api/v2/pms/reservations/12345/rates"
        assert links["discount"]["href"] == "/api/v2/pms/reservations/12345/discount"

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_performance(self, mock_api_client):
        """Test end-to-end de rendimiento"""
        # Configurar el mock
        mock_api_client.get.return_value = self.test_reservation_data

        # Medir tiempo de ejecución
        start_time = time.time()
        result = get_reservation(self.valid_reservation_id)
        end_time = time.time()

        # Verificar que la respuesta es rápida (menos de 1 segundo)
        execution_time = end_time - start_time
        assert execution_time < 1.0, f"Ejecución demasiado lenta: {execution_time:.3f}s"

        # Verificar que el resultado es válido
        assert result is not None
        assert result["id"] == self.valid_reservation_id

    @patch("src.trackhs_mcp.server.api_client")
    def test_e2e_reservation_error_handling(self, mock_api_client):
        """Test end-to-end de manejo de errores"""
        # Test con error 404
        mock_api_client.get.side_effect = Exception("404 Not Found")

        with pytest.raises(ToolError, match="Reserva 99999 no encontrada"):
            get_reservation(99999)

        # Test con error 500
        mock_api_client.get.side_effect = Exception("500 Internal Server Error")

        with pytest.raises(ToolError, match="Error obteniendo reserva"):
            get_reservation(self.valid_reservation_id)

        # Test con api_client None
        mock_api_client.__bool__ = Mock(return_value=False)
        mock_api_client = None

        with pytest.raises(ToolError, match="Cliente API no disponible"):
            get_reservation(self.valid_reservation_id)

    def test_e2e_mcp_tool_registration(self):
        """Test end-to-end de registro del tool en MCP"""
        # Verificar que el tool está registrado en MCP
        assert mcp is not None

        # Verificar que get_reservation está disponible
        tools = mcp.list_tools()
        tool_names = [tool.name for tool in tools]
        assert "get_reservation" in tool_names

    def test_e2e_schema_compatibility(self):
        """Test end-to-end de compatibilidad del schema"""
        # Crear instancia del schema con datos mínimos
        minimal_data = {"id": 12345}
        reservation = ReservationDetailOutput(**minimal_data)
        assert reservation.id == 12345

        # Crear instancia del schema con datos completos
        full_data = self.test_reservation_data
        reservation = ReservationDetailOutput(**full_data)
        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.status == "Confirmed"

        # Verificar que todos los campos opcionales funcionan
        assert reservation.alternates is not None
        assert reservation.occupants is not None
        assert reservation.securityDeposit is not None
        assert reservation.guestBreakdown is not None
        assert reservation.ownerBreakdown is not None
        assert reservation.embedded is not None
        assert reservation.links is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
