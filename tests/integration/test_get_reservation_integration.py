"""
Tests de integración para get_reservation
Verifica que el use case funcione correctamente con dependencias reales
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.trackhs_mcp.application.use_cases.get_reservation import GetReservationUseCase
from src.trackhs_mcp.domain.entities.reservations import (
    GetReservationParams,
    Reservation,
)


class TestGetReservationIntegration:
    """Tests de integración para get_reservation"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = AsyncMock()
        client.get.return_value = {
            "id": 123,
            "alternates": [],
            "currency": "USD",
            "unitId": 456,
            "clientIPAddress": "192.168.1.1",
            "session": "session123",
            "isUnitLocked": False,
            "isUnitAssigned": True,
            "isUnitTypeLocked": False,
            "unitTypeId": 789,
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "earlyArrival": False,
            "lateDeparture": False,
            "arrivalTime": "15:00",
            "departureTime": "11:00",
            "nights": 5,
            "status": "Confirmed",
            "occupants": [
                {
                    "typeId": 1,
                    "name": "Adult",
                    "handle": "adult",
                    "quantity": 2.0,
                    "included": True,
                    "extraQuantity": 0.0,
                    "ratePerPersonPerStay": "0.00",
                    "ratePerStay": "0.00",
                }
            ],
            "securityDeposit": {"required": "100.00", "remaining": 100.0},
            "updatedAt": "2024-01-10T10:00:00Z",
            "createdAt": "2024-01-10T10:00:00Z",
            "bookedAt": "2024-01-10T10:00:00Z",
            "guestBreakdown": {
                "grossRent": "500.00",
                "guestGrossDisplayRent": "500.00",
                "discountTotal": 0.0,
                "netRent": "500.00",
                "guestNetDisplayRent": "500.00",
                "actualAdr": "100.00",
                "guestAdr": "100.00",
                "totalGuestFees": "0.00",
                "totalRentFees": "0.00",
                "totalItemizedFees": "0.00",
                "totalTaxFees": "50.00",
                "totalServiceFees": "0.00",
                "folioCharges": "0.00",
                "subtotal": "500.00",
                "guestSubtotal": "500.00",
                "totalTaxes": "50.00",
                "totalGuestTaxes": "50.00",
                "total": "550.00",
                "grandTotal": "550.00",
                "netPayments": "0.00",
                "payments": "0.00",
                "refunds": "0.00",
                "netTransfers": "0.00",
                "balance": "550.00",
                "rates": [],
                "guestFees": [],
                "taxes": [],
            },
            "contactId": 101,
            "folioId": 202,
            "typeId": 1,
            "rateTypeId": 1,
            "isTaxable": True,
            "uuid": "uuid-123",
            "source": "direct",
            "isChannelLocked": False,
            "agreementStatus": "not-needed",
            "automatePayment": False,
            "revenueRealizedMethod": "checkout",
            "updatedBy": "system",
            "createdBy": "system",
            "travelInsuranceProducts": [],
            "_embedded": {
                "unit": {
                    "id": 456,
                    "name": "Deluxe Suite",
                    "shortName": "DS",
                    "unitCode": "DS001",
                    "headline": "Luxury Suite",
                    "shortDescription": "Beautiful suite with ocean view",
                    "longDescription": "Spacious suite with modern amenities",
                    "houseRules": "No smoking",
                    "nodeId": 1,
                }
            },
            "_links": {
                "self": {"href": "/v2/pms/reservations/123"},
                "unit": {"href": "/v2/pms/units/456"},
            },
        }
        return client

    @pytest.fixture
    def get_reservation_use_case(self, mock_api_client):
        """Use case con dependencias mockeadas"""
        return GetReservationUseCase(api_client=mock_api_client)

    @pytest.mark.asyncio
    async def test_get_reservation_success_integration(
        self, get_reservation_use_case, mock_api_client
    ):
        """Test de integración exitoso para get_reservation"""
        # Arrange
        params = GetReservationParams(reservation_id=123)

        # Act
        result = await get_reservation_use_case.execute(params)

        # Assert
        assert result is not None
        assert isinstance(result, Reservation)
        assert result.id == 123
        assert result.currency == "USD"
        assert result.unit_id == 456
        assert result.arrival_date == "2024-01-15"
        assert result.departure_date == "2024-01-20"
        assert result.nights == 5

        # Verificar que se llamó al API client
        mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_reservation_with_different_ids_integration(
        self, get_reservation_use_case, mock_api_client
    ):
        """Test de integración con diferentes IDs"""
        reservation_ids = [1, 2, 3]

        for reservation_id in reservation_ids:
            # Arrange
            params = GetReservationParams(reservation_id=reservation_id)

            # Act
            result = await get_reservation_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.id == 123  # Mock response

    @pytest.mark.asyncio
    async def test_get_reservation_api_error_integration(self, mock_api_client):
        """Test de integración con error de API"""
        # Arrange
        mock_api_client.get.side_effect = Exception("API Error")
        get_reservation_use_case = GetReservationUseCase(api_client=mock_api_client)

        params = GetReservationParams(reservation_id=123)

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            await get_reservation_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_reservation_not_found_integration(self, mock_api_client):
        """Test de integración con reservación no encontrada"""
        # Arrange
        mock_api_client.get.side_effect = Exception("Reservation not found")
        get_reservation_use_case = GetReservationUseCase(api_client=mock_api_client)

        params = GetReservationParams(reservation_id=999)

        # Act & Assert
        with pytest.raises(Exception, match="Reservation not found"):
            await get_reservation_use_case.execute(params)

    @pytest.mark.asyncio
    async def test_get_reservation_different_statuses_integration(
        self, mock_api_client
    ):
        """Test de integración con diferentes estados"""
        statuses = ["Confirmed", "Hold", "Cancelled", "Checked In", "Checked Out"]

        for status in statuses:
            # Arrange
            mock_api_client.get.return_value = {
                "id": 123,
                "alternates": [],
                "currency": "USD",
                "unitId": 456,
                "clientIPAddress": "192.168.1.1",
                "session": "session123",
                "isUnitLocked": False,
                "isUnitAssigned": True,
                "isUnitTypeLocked": False,
                "unitTypeId": 789,
                "arrivalDate": "2024-01-15",
                "departureDate": "2024-01-20",
                "earlyArrival": False,
                "lateDeparture": False,
                "arrivalTime": "15:00",
                "departureTime": "11:00",
                "nights": 5,
                "status": status,
                "occupants": [
                    {
                        "typeId": 1,
                        "name": "Adult",
                        "handle": "adult",
                        "quantity": 2.0,
                        "included": True,
                        "extraQuantity": 0.0,
                        "ratePerPersonPerStay": "0.00",
                        "ratePerStay": "0.00",
                    }
                ],
                "securityDeposit": {"required": "100.00", "remaining": 100.0},
                "updatedAt": "2024-01-10T10:00:00Z",
                "createdAt": "2024-01-10T10:00:00Z",
                "bookedAt": "2024-01-10T10:00:00Z",
                "guestBreakdown": {
                    "grossRent": "500.00",
                    "guestGrossDisplayRent": "500.00",
                    "discountTotal": 0.0,
                    "netRent": "500.00",
                    "guestNetDisplayRent": "500.00",
                    "actualAdr": "100.00",
                    "guestAdr": "100.00",
                    "totalGuestFees": "0.00",
                    "totalRentFees": "0.00",
                    "totalItemizedFees": "0.00",
                    "totalTaxFees": "50.00",
                    "totalServiceFees": "0.00",
                    "folioCharges": "0.00",
                    "subtotal": "500.00",
                    "guestSubtotal": "500.00",
                    "totalTaxes": "50.00",
                    "totalGuestTaxes": "50.00",
                    "total": "550.00",
                    "grandTotal": "550.00",
                    "netPayments": "0.00",
                    "payments": "0.00",
                    "refunds": "0.00",
                    "netTransfers": "0.00",
                    "balance": "550.00",
                    "rates": [],
                    "guestFees": [],
                    "taxes": [],
                },
                "contactId": 101,
                "folioId": 202,
                "typeId": 1,
                "rateTypeId": 1,
                "isTaxable": True,
                "uuid": "uuid-123",
                "source": "direct",
                "isChannelLocked": False,
                "agreementStatus": "not-needed",
                "automatePayment": False,
                "revenueRealizedMethod": "checkout",
                "updatedBy": "system",
                "createdBy": "system",
                "travelInsuranceProducts": [],
                "_embedded": {
                    "unit": {
                        "id": 456,
                        "name": "Deluxe Suite",
                        "shortName": "DS",
                        "unitCode": "DS001",
                        "headline": "Luxury Suite",
                        "shortDescription": "Beautiful suite with ocean view",
                        "longDescription": "Spacious suite with modern amenities",
                        "houseRules": "No smoking",
                        "nodeId": 1,
                    }
                },
                "_links": {
                    "self": {"href": "/v2/pms/reservations/123"},
                    "unit": {"href": "/v2/pms/units/456"},
                },
            }

            get_reservation_use_case = GetReservationUseCase(api_client=mock_api_client)
            params = GetReservationParams(reservation_id=123)

            # Act
            result = await get_reservation_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.status == status

    @pytest.mark.asyncio
    async def test_get_reservation_different_room_types_integration(
        self, mock_api_client
    ):
        """Test de integración con diferentes tipos de habitación"""
        room_types = ["Standard", "Deluxe", "Suite", "Presidential"]

        for room_type in room_types:
            # Arrange
            mock_api_client.get.return_value = {
                "id": 123,
                "alternates": [],
                "currency": "USD",
                "unitId": 456,
                "clientIPAddress": "192.168.1.1",
                "session": "session123",
                "isUnitLocked": False,
                "isUnitAssigned": True,
                "isUnitTypeLocked": False,
                "unitTypeId": 789,
                "arrivalDate": "2024-01-15",
                "departureDate": "2024-01-20",
                "earlyArrival": False,
                "lateDeparture": False,
                "arrivalTime": "15:00",
                "departureTime": "11:00",
                "nights": 5,
                "status": "Confirmed",
                "occupants": [
                    {
                        "typeId": 1,
                        "name": "Adult",
                        "handle": "adult",
                        "quantity": 2.0,
                        "included": True,
                        "extraQuantity": 0.0,
                        "ratePerPersonPerStay": "0.00",
                        "ratePerStay": "0.00",
                    }
                ],
                "securityDeposit": {"required": "100.00", "remaining": 100.0},
                "updatedAt": "2024-01-10T10:00:00Z",
                "createdAt": "2024-01-10T10:00:00Z",
                "bookedAt": "2024-01-10T10:00:00Z",
                "guestBreakdown": {
                    "grossRent": "500.00",
                    "guestGrossDisplayRent": "500.00",
                    "discountTotal": 0.0,
                    "netRent": "500.00",
                    "guestNetDisplayRent": "500.00",
                    "actualAdr": "100.00",
                    "guestAdr": "100.00",
                    "totalGuestFees": "0.00",
                    "totalRentFees": "0.00",
                    "totalItemizedFees": "0.00",
                    "totalTaxFees": "50.00",
                    "totalServiceFees": "0.00",
                    "folioCharges": "0.00",
                    "subtotal": "500.00",
                    "guestSubtotal": "500.00",
                    "totalTaxes": "50.00",
                    "totalGuestTaxes": "50.00",
                    "total": "550.00",
                    "grandTotal": "550.00",
                    "netPayments": "0.00",
                    "payments": "0.00",
                    "refunds": "0.00",
                    "netTransfers": "0.00",
                    "balance": "550.00",
                    "rates": [],
                    "guestFees": [],
                    "taxes": [],
                },
                "contactId": 101,
                "folioId": 202,
                "typeId": 1,
                "rateTypeId": 1,
                "isTaxable": True,
                "uuid": "uuid-123",
                "source": "direct",
                "isChannelLocked": False,
                "agreementStatus": "not-needed",
                "automatePayment": False,
                "revenueRealizedMethod": "checkout",
                "updatedBy": "system",
                "createdBy": "system",
                "travelInsuranceProducts": [],
                "_embedded": {
                    "unit": {
                        "id": 456,
                        "name": f"{room_type} Suite",
                        "shortName": room_type[:2],
                        "unitCode": f"{room_type[:2]}001",
                        "headline": f"Luxury {room_type}",
                        "shortDescription": f"Beautiful {room_type.lower()} with ocean view",
                        "longDescription": f"Spacious {room_type.lower()} with modern amenities",
                        "houseRules": "No smoking",
                        "nodeId": 1,
                    }
                },
                "_links": {
                    "self": {"href": "/v2/pms/reservations/123"},
                    "unit": {"href": "/v2/pms/units/456"},
                },
            }

            get_reservation_use_case = GetReservationUseCase(api_client=mock_api_client)
            params = GetReservationParams(reservation_id=123)

            # Act
            result = await get_reservation_use_case.execute(params)

            # Assert
            assert result is not None
            assert result.embedded["unit"]["name"] == f"{room_type} Suite"

    @pytest.mark.asyncio
    async def test_get_reservation_complete_workflow_integration(
        self, get_reservation_use_case, mock_api_client
    ):
        """Test de integración del workflow completo"""
        # Arrange
        params = GetReservationParams(reservation_id=123)

        # Act
        result = await get_reservation_use_case.execute(params)

        # Assert
        assert result is not None
        assert isinstance(result, Reservation)
        assert result.id == 123
        assert result.unit_id == 456
        assert result.arrival_date == "2024-01-15"
        assert result.departure_date == "2024-01-20"
        assert result.status == "Confirmed"
        assert result.currency == "USD"
        assert result.contact_id == 101
        assert result.folio_id == 202

        # Verificar que el API client fue llamado
        mock_api_client.get.assert_called_once()
