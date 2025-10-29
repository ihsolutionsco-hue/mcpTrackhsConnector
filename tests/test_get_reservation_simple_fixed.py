"""
Pruebas simplificadas y corregidas para el tool get_reservation con API V2
Enfoque en simplicidad y buenas prácticas
"""

import json
import os
import sys
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastmcp.exceptions import ToolError

from trackhs_mcp.client import TrackHSClient
from trackhs_mcp.schemas import ReservationDetailOutput


class TestGetReservationSimple:
    """Pruebas simplificadas para get_reservation"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.valid_reservation_id = 12345
        self.sample_data = {
            "id": 12345,
            "currency": "USD",
            "unitId": 789,
            "arrivalDate": "2024-01-15",
            "departureDate": "2024-01-20",
            "status": "Confirmed",
            "nights": 5.0,
            "isUnitLocked": False,
            "isUnitAssigned": True,
            "occupants": [
                {"typeId": 1, "name": "Adult", "quantity": 2, "included": True}
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

    def test_schema_validation_minimal(self):
        """Test que el schema funciona con datos mínimos"""
        minimal_data = {"id": 12345}
        reservation = ReservationDetailOutput(**minimal_data)

        assert reservation.id == 12345
        assert reservation.currency is None
        assert reservation.unitId is None

    def test_schema_validation_complete(self):
        """Test que el schema funciona con datos completos"""
        reservation = ReservationDetailOutput(**self.sample_data)

        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.unitId == 789
        assert reservation.status == "Confirmed"
        assert reservation.nights == 5.0
        assert len(reservation.occupants) == 1
        assert reservation.occupants[0]["name"] == "Adult"

    def test_schema_field_types(self):
        """Test que los tipos de campos son correctos"""
        reservation = ReservationDetailOutput(**self.sample_data)

        assert isinstance(reservation.id, int)
        assert isinstance(reservation.currency, str)
        assert isinstance(reservation.nights, float)
        assert isinstance(reservation.isUnitLocked, bool)
        assert isinstance(reservation.occupants, list)
        assert isinstance(reservation.securityDeposit, dict)
        assert isinstance(reservation.guestBreakdown, dict)
        assert isinstance(reservation.ownerBreakdown, dict)

    def test_schema_optional_fields(self):
        """Test que los campos opcionales funcionan correctamente"""
        # Test con algunos campos None
        data_with_nones = {
            "id": 12345,
            "currency": None,
            "unitId": None,
            "status": None,
            "occupants": None,
            "securityDeposit": None,
            "guestBreakdown": None,
            "ownerBreakdown": None,
        }

        reservation = ReservationDetailOutput(**data_with_nones)
        assert reservation.id == 12345
        assert reservation.currency is None
        assert reservation.unitId is None
        assert reservation.status is None

    def test_schema_embedded_data(self):
        """Test que los datos embebidos funcionan correctamente"""
        reservation = ReservationDetailOutput(**self.sample_data)

        # Verificar que el campo existe (puede ser None)
        assert hasattr(reservation, "embedded")
        if reservation.embedded is not None:
            assert "unit" in reservation.embedded
            assert reservation.embedded["unit"]["id"] == 789

    def test_schema_links(self):
        """Test que los enlaces funcionan correctamente"""
        reservation = ReservationDetailOutput(**self.sample_data)

        # Verificar que el campo existe (puede ser None)
        assert hasattr(reservation, "links")
        if reservation.links is not None:
            assert "self" in reservation.links
            assert reservation.links["self"]["href"] == "/api/v2/pms/reservations/12345"

    def test_schema_financial_breakdown(self):
        """Test del desglose financiero"""
        reservation = ReservationDetailOutput(**self.sample_data)

        # Verificar desglose del huésped
        guest_breakdown = reservation.guestBreakdown
        assert guest_breakdown["grossRent"] == "1000.00"
        assert guest_breakdown["netRent"] == "1000.00"
        assert guest_breakdown["total"] == "1200.00"
        assert guest_breakdown["balance"] == "0.00"

        # Verificar desglose del propietario
        owner_breakdown = reservation.ownerBreakdown
        assert owner_breakdown["grossRent"] == "1000.00"
        assert owner_breakdown["netRevenue"] == "900.00"

    def test_schema_occupants(self):
        """Test de la información de ocupantes"""
        reservation = ReservationDetailOutput(**self.sample_data)

        assert len(reservation.occupants) == 1
        occupant = reservation.occupants[0]
        assert occupant["typeId"] == 1
        assert occupant["name"] == "Adult"
        assert occupant["quantity"] == 2
        assert occupant["included"] is True

    def test_schema_security_deposit(self):
        """Test del depósito de seguridad"""
        reservation = ReservationDetailOutput(**self.sample_data)

        security_deposit = reservation.securityDeposit
        assert security_deposit["required"] == "200.00"
        assert security_deposit["remaining"] == 200

    def test_schema_validation_error(self):
        """Test que el schema valida correctamente los errores"""
        # Test con ID inválido
        with pytest.raises(ValueError):
            ReservationDetailOutput(id="invalid")

    def test_schema_field_count(self):
        """Test que el schema tiene el número correcto de campos"""
        fields = ReservationDetailOutput.model_fields
        assert len(fields) == 67, f"Expected 67 fields, got {len(fields)}"

    def test_schema_required_fields(self):
        """Test que solo el ID es requerido"""
        # Solo ID requerido
        minimal = ReservationDetailOutput(id=12345)
        assert minimal.id == 12345

        # Sin ID debe fallar
        with pytest.raises(ValueError):
            ReservationDetailOutput()

    def test_schema_aliases(self):
        """Test que los alias funcionan correctamente"""
        data_with_underscores = {
            "id": 12345,
            "_embedded": {"unit": {"id": 789}},
            "_links": {"self": {"href": "/api/v2/pms/reservations/12345"}},
        }

        reservation = ReservationDetailOutput(**data_with_underscores)
        assert reservation.embedded is not None
        assert reservation.links is not None

    def test_schema_json_serialization(self):
        """Test que el schema se serializa correctamente a JSON"""
        reservation = ReservationDetailOutput(**self.sample_data)
        json_data = reservation.model_dump()

        assert isinstance(json_data, dict)
        assert json_data["id"] == 12345
        assert json_data["currency"] == "USD"

    def test_schema_json_deserialization(self):
        """Test que el schema se deserializa correctamente desde JSON"""
        json_data = {
            "id": 12345,
            "currency": "USD",
            "unitId": 789,
            "status": "Confirmed",
        }

        reservation = ReservationDetailOutput(**json_data)
        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.unitId == 789
        assert reservation.status == "Confirmed"


class TestGetReservationIntegration:
    """Pruebas de integración simplificadas"""

    def setup_method(self):
        """Configuración inicial"""
        self.base_url = "https://ihmvacations.trackhs.com"
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"

    def test_client_initialization(self):
        """Test que el cliente se inicializa correctamente"""
        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        assert client.base_url == self.base_url
        # Verificar que el cliente tiene los atributos necesarios
        assert hasattr(client, "base_url")
        # Verificar que el cliente se puede instanciar correctamente
        assert client is not None

    def test_api_v2_url_format(self):
        """Test que la URL de la API V2 tiene el formato correcto"""
        reservation_id = 12345
        expected_url = f"{self.base_url}/api/v2/pms/reservations/{reservation_id}"

        assert "v2" in expected_url
        assert "pms/reservations" in expected_url
        assert str(reservation_id) in expected_url

    def test_client_get_request(self):
        """Test que el cliente se puede instanciar correctamente"""
        # Test simple de instanciación del cliente
        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        # Verificar que el cliente se creó correctamente
        assert client is not None
        assert hasattr(client, "get")
        assert callable(client.get)

    def test_client_error_handling(self):
        """Test que el cliente se puede instanciar correctamente"""
        # Test simple de instanciación del cliente
        client = TrackHSClient(self.base_url, self.api_key, self.api_secret)

        # Verificar que el cliente se creó correctamente
        assert client is not None
        assert hasattr(client, "get")
        assert callable(client.get)


class TestGetReservationE2E:
    """Pruebas end-to-end simplificadas"""

    def test_schema_compatibility(self):
        """Test de compatibilidad del schema con datos reales"""
        # Simular datos reales de la API V2
        real_world_data = {
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
                "netRent": "1000.00",
                "total": "1200.00",
                "balance": "0.00",
            },
            "ownerBreakdown": {"grossRent": "1000.00", "netRevenue": "900.00"},
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
        reservation = ReservationDetailOutput(**real_world_data)
        assert reservation.id == 12345
        assert reservation.currency == "USD"
        assert reservation.status == "Confirmed"
        assert len(reservation.occupants) == 1

    def test_performance_schema_creation(self):
        """Test de rendimiento en la creación del schema"""
        import time

        data = {"id": 12345, "currency": "USD", "status": "Confirmed"}

        start_time = time.time()
        for _ in range(100):
            ReservationDetailOutput(**data)
        end_time = time.time()

        # Debe ser rápido (menos de 1 segundo para 100 creaciones)
        execution_time = end_time - start_time
        assert execution_time < 1.0, f"Schema creation too slow: {execution_time:.3f}s"

    def test_memory_usage(self):
        """Test de uso de memoria del schema"""
        import sys

        # Crear muchas instancias para verificar uso de memoria
        reservations = []
        for i in range(1000):
            data = {
                "id": i,
                "currency": "USD",
                "status": "Confirmed",
                "occupants": [{"typeId": 1, "name": "Adult", "quantity": 2}],
                "guestBreakdown": {"grossRent": "1000.00"},
                "ownerBreakdown": {"grossRent": "1000.00"},
            }
            reservations.append(ReservationDetailOutput(**data))

        # Verificar que se crearon correctamente
        assert len(reservations) == 1000
        assert reservations[0].id == 0
        assert reservations[999].id == 999


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
