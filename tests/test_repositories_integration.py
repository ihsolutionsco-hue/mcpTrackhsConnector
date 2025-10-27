"""
Tests de integración para repositories de TrackHS MCP Server
Prueba la funcionalidad completa de repositories con mocks de API
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.trackhs_mcp.repositories import (
    ReservationRepository,
    UnitRepository,
    WorkOrderRepository,
)
from src.trackhs_mcp.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)


class TestReservationRepository:
    """Tests para ReservationRepository"""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client
    
    @pytest.fixture
    def reservation_repo(self, mock_api_client):
        """Instancia de ReservationRepository para testing"""
        return ReservationRepository(mock_api_client, cache_ttl=60)
    
    def test_get_by_id_success(self, reservation_repo, mock_api_client):
        """Test obtener reserva por ID exitoso"""
        # Arrange
        reservation_id = 12345
        expected_response = {
            "id": reservation_id,
            "confirmation_number": "CONF123",
            "guest": {"name": "John Doe", "email": "john@example.com"},
            "arrival_date": "2024-01-15",
            "departure_date": "2024-01-20",
            "status": "confirmed"
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = reservation_repo.get_by_id(reservation_id)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(f"pms/reservations/{reservation_id}")
    
    def test_get_by_id_not_found(self, reservation_repo, mock_api_client):
        """Test obtener reserva por ID que no existe"""
        # Arrange
        reservation_id = 99999
        mock_api_client.get.side_effect = NotFoundError("Reserva no encontrada")
        
        # Act & Assert
        with pytest.raises(NotFoundError):
            reservation_repo.get_by_id(reservation_id)
    
    def test_search_reservations(self, reservation_repo, mock_api_client):
        """Test búsqueda de reservas"""
        # Arrange
        filters = {
            "page": 1,
            "size": 10,
            "status": "confirmed"
        }
        expected_response = {
            "page": 1,
            "page_count": 1,
            "page_size": 10,
            "total_items": 1,
            "_embedded": {
                "reservations": [
                    {
                        "id": 12345,
                        "confirmation_number": "CONF123",
                        "status": "confirmed"
                    }
                ]
            }
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = reservation_repo.search(filters)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with("pms/reservations", params=filters)
    
    def test_get_folio(self, reservation_repo, mock_api_client):
        """Test obtener folio de reserva"""
        # Arrange
        reservation_id = 12345
        expected_folio = {
            "reservation_id": reservation_id,
            "balance": 500.0,
            "charges": [],
            "payments": []
        }
        mock_api_client.get.return_value = expected_folio
        
        # Act
        result = reservation_repo.get_folio(reservation_id)
        
        # Assert
        assert result == expected_folio
        mock_api_client.get.assert_called_once_with(f"pms/reservations/{reservation_id}/folio")
    
    def test_search_by_date_range(self, reservation_repo, mock_api_client):
        """Test búsqueda por rango de fechas"""
        # Arrange
        start_date = "2024-01-15"
        end_date = "2024-01-20"
        expected_filters = {
            "arrival_start": start_date,
            "arrival_end": end_date
        }
        mock_api_client.get.return_value = {"page": 1, "total_items": 0, "_embedded": {"reservations": []}}
        
        # Act
        reservation_repo.search_by_date_range(start_date, end_date)
        
        # Assert
        mock_api_client.get.assert_called_once_with("pms/reservations", params=expected_filters)
    
    def test_cache_functionality(self, reservation_repo, mock_api_client):
        """Test funcionalidad de cache"""
        # Arrange
        reservation_id = 12345
        expected_response = {"id": reservation_id, "status": "confirmed"}
        mock_api_client.get.return_value = expected_response
        
        # Act - Primera llamada
        result1 = reservation_repo.get_by_id(reservation_id)
        
        # Act - Segunda llamada (debería usar cache)
        result2 = reservation_repo.get_by_id(reservation_id)
        
        # Assert
        assert result1 == result2
        # Solo debería llamar a la API una vez debido al cache
        mock_api_client.get.assert_called_once()
    
    def test_health_check_healthy(self, reservation_repo, mock_api_client):
        """Test health check cuando está saludable"""
        # Arrange
        mock_api_client.get.return_value = {"page": 1, "size": 1}
        
        # Act
        health = reservation_repo.health_check()
        
        # Assert
        assert health["status"] == "healthy"
        assert "cache_metrics" in health
        assert "cache_ttl" in health
    
    def test_health_check_unhealthy(self, reservation_repo, mock_api_client):
        """Test health check cuando no está saludable"""
        # Arrange
        mock_api_client.get.side_effect = APIError("API no disponible")
        
        # Act
        health = reservation_repo.health_check()
        
        # Assert
        assert health["status"] == "unhealthy"
        assert "error" in health


class TestUnitRepository:
    """Tests para UnitRepository"""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client
    
    @pytest.fixture
    def unit_repo(self, mock_api_client):
        """Instancia de UnitRepository para testing"""
        return UnitRepository(mock_api_client, cache_ttl=60)
    
    def test_get_by_id_success(self, unit_repo, mock_api_client):
        """Test obtener unidad por ID exitoso"""
        # Arrange
        unit_id = 100
        expected_response = {
            "id": unit_id,
            "name": "Casa de Playa",
            "code": "CP001",
            "bedrooms": 3,
            "bathrooms": 2
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = unit_repo.get_by_id(unit_id)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(f"pms/units/{unit_id}")
    
    def test_search_units(self, unit_repo, mock_api_client):
        """Test búsqueda de unidades"""
        # Arrange
        filters = {
            "page": 1,
            "size": 10,
            "bedrooms": 2
        }
        expected_response = {
            "page": 1,
            "total_items": 1,
            "_embedded": {
                "units": [
                    {
                        "id": 100,
                        "name": "Casa de Playa",
                        "bedrooms": 2
                    }
                ]
            }
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = unit_repo.search(filters)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with("pms/units", params=filters)
    
    def test_search_amenities(self, unit_repo, mock_api_client):
        """Test búsqueda de amenidades"""
        # Arrange
        filters = {"page": 1, "size": 10}
        expected_response = {
            "page": 1,
            "total_items": 3,
            "_embedded": {
                "amenities": [
                    {"id": 1, "name": "WiFi"},
                    {"id": 2, "name": "Pool"},
                    {"id": 3, "name": "Parking"}
                ]
            }
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = unit_repo.search_amenities(filters)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with("pms/units/amenities", params=filters)
    
    def test_search_by_capacity(self, unit_repo, mock_api_client):
        """Test búsqueda por capacidad"""
        # Arrange
        bedrooms = 2
        bathrooms = 1
        mock_api_client.get.return_value = {"page": 1, "total_items": 0, "_embedded": {"units": []}}
        
        # Act
        unit_repo.search_by_capacity(bedrooms=bedrooms, bathrooms=bathrooms)
        
        # Assert
        expected_filters = {"bedrooms": bedrooms, "bathrooms": bathrooms}
        mock_api_client.get.assert_called_once_with("pms/units", params=expected_filters)
    
    def test_get_unit_summary(self, unit_repo, mock_api_client):
        """Test obtener resumen de unidad"""
        # Arrange
        unit_id = 100
        unit_data = {
            "id": unit_id,
            "name": "Casa de Playa",
            "code": "CP001",
            "bedrooms": 3,
            "bathrooms": 2,
            "max_occupancy": 6,
            "area": 120.5,
            "address": "123 Beach St",
            "amenities": ["WiFi", "Pool"],
            "is_active": True,
            "is_bookable": True
        }
        mock_api_client.get.return_value = unit_data
        
        # Act
        summary = unit_repo.get_unit_summary(unit_id)
        
        # Assert
        expected_summary = {
            "id": unit_id,
            "name": "Casa de Playa",
            "code": "CP001",
            "bedrooms": 3,
            "bathrooms": 2,
            "max_occupancy": 6,
            "area": 120.5,
            "address": "123 Beach St",
            "is_active": True,
            "is_bookable": True,
            "amenities_count": 2
        }
        assert summary == expected_summary


class TestWorkOrderRepository:
    """Tests para WorkOrderRepository"""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client
    
    @pytest.fixture
    def work_order_repo(self, mock_api_client):
        """Instancia de WorkOrderRepository para testing"""
        return WorkOrderRepository(mock_api_client, cache_ttl=60)
    
    def test_create_maintenance_work_order_success(self, work_order_repo, mock_api_client):
        """Test crear orden de mantenimiento exitosa"""
        # Arrange
        work_order_data = {
            "unitId": 123,
            "summary": "Fuga en grifo",
            "description": "Grifo del baño principal gotea",
            "priority": 3,
            "status": "pending",
            "dateReceived": "2024-01-15"
        }
        expected_response = {
            "id": 456,
            "status": "pending",
            "unitId": 123,
            "summary": "Fuga en grifo"
        }
        mock_api_client.post.return_value = expected_response
        
        # Act
        result = work_order_repo.create_maintenance_work_order(
            unit_id=123,
            summary="Fuga en grifo",
            description="Grifo del baño principal gotea",
            priority=3
        )
        
        # Assert
        assert result == expected_response
        mock_api_client.post.assert_called_once_with("pms/maintenance/work-orders", work_order_data)
    
    def test_create_maintenance_work_order_validation_error(self, work_order_repo):
        """Test validación de datos de orden de mantenimiento"""
        # Act & Assert
        with pytest.raises(ValidationError):
            work_order_repo.create_maintenance_work_order(
                unit_id=0,  # ID inválido
                summary="Test",
                description="Test description"
            )
    
    def test_create_housekeeping_work_order_success(self, work_order_repo, mock_api_client):
        """Test crear orden de housekeeping exitosa"""
        # Arrange
        work_order_data = {
            "unitId": 123,
            "scheduledAt": "2024-01-15",
            "status": "pending",
            "isInspection": False,
            "cleanTypeId": 1
        }
        expected_response = {
            "id": 789,
            "status": "pending",
            "unitId": 123,
            "scheduledAt": "2024-01-15"
        }
        mock_api_client.post.return_value = expected_response
        
        # Act
        result = work_order_repo.create_housekeeping_work_order(
            unit_id=123,
            scheduled_at="2024-01-15",
            is_inspection=False,
            clean_type_id=1
        )
        
        # Assert
        assert result == expected_response
        mock_api_client.post.assert_called_once_with("pms/housekeeping/work-orders", work_order_data)
    
    def test_create_housekeeping_work_order_validation_error(self, work_order_repo):
        """Test validación de datos de orden de housekeeping"""
        # Act & Assert
        with pytest.raises(ValidationError):
            work_order_repo.create_housekeeping_work_order(
                unit_id=123,
                scheduled_at="2024-01-15",
                is_inspection=False,
                clean_type_id=None  # Requerido cuando no es inspección
            )
    
    def test_get_by_id_maintenance(self, work_order_repo, mock_api_client):
        """Test obtener orden de mantenimiento por ID"""
        # Arrange
        work_order_id = 456
        expected_response = {
            "id": work_order_id,
            "type": "maintenance",
            "status": "pending",
            "unitId": 123
        }
        mock_api_client.get.return_value = expected_response
        
        # Act
        result = work_order_repo.get_by_id(work_order_id)
        
        # Assert
        assert result == expected_response
        mock_api_client.get.assert_called_once_with(f"pms/maintenance/work-orders/{work_order_id}")
    
    def test_get_by_id_housekeeping_fallback(self, work_order_repo, mock_api_client):
        """Test obtener orden de housekeeping por ID (fallback)"""
        # Arrange
        work_order_id = 789
        expected_response = {
            "id": work_order_id,
            "type": "housekeeping",
            "status": "pending",
            "unitId": 123
        }
        
        # Simular que no se encuentra en mantenimiento, pero sí en housekeeping
        mock_api_client.get.side_effect = [
            NotFoundError("No encontrado en mantenimiento"),
            expected_response
        ]
        
        # Act
        result = work_order_repo.get_by_id(work_order_id)
        
        # Assert
        assert result == expected_response
        assert mock_api_client.get.call_count == 2
    
    def test_search_work_orders(self, work_order_repo, mock_api_client):
        """Test búsqueda de órdenes de trabajo"""
        # Arrange
        filters = {"page": 1, "size": 10, "status": "pending"}
        
        maintenance_response = {
            "page": 1,
            "total_items": 1,
            "_embedded": {"work_orders": [{"id": 1, "type": "maintenance"}]}
        }
        housekeeping_response = {
            "page": 1,
            "total_items": 1,
            "_embedded": {"work_orders": [{"id": 2, "type": "housekeeping"}]}
        }
        
        mock_api_client.get.side_effect = [maintenance_response, housekeeping_response]
        
        # Act
        result = work_order_repo.search(filters)
        
        # Assert
        assert result["total_items"] == 2
        assert "maintenance_work_orders" in result["_embedded"]
        assert "housekeeping_work_orders" in result["_embedded"]
        assert mock_api_client.get.call_count == 2


class TestRepositoryIntegration:
    """Tests de integración entre repositories"""
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API"""
        client = Mock()
        return client
    
    @pytest.fixture
    def repositories(self, mock_api_client):
        """Instancias de todos los repositories"""
        return {
            "reservation": ReservationRepository(mock_api_client, cache_ttl=60),
            "unit": UnitRepository(mock_api_client, cache_ttl=60),
            "work_order": WorkOrderRepository(mock_api_client, cache_ttl=60)
        }
    
    def test_full_workflow(self, repositories, mock_api_client):
        """Test flujo completo de trabajo"""
        # Arrange
        reservation_id = 12345
        unit_id = 100
        
        # Mock responses
        reservation_data = {
            "id": reservation_id,
            "unit": {"id": unit_id, "name": "Casa de Playa"},
            "status": "confirmed"
        }
        unit_data = {
            "id": unit_id,
            "name": "Casa de Playa",
            "bedrooms": 3,
            "bathrooms": 2
        }
        work_order_data = {
            "id": 456,
            "status": "pending",
            "unitId": unit_id
        }
        
        mock_api_client.get.side_effect = [reservation_data, unit_data]
        mock_api_client.post.return_value = work_order_data
        
        # Act - Flujo completo
        # 1. Obtener reserva
        reservation = repositories["reservation"].get_by_id(reservation_id)
        
        # 2. Obtener unidad
        unit = repositories["unit"].get_by_id(unit_id)
        
        # 3. Crear orden de trabajo
        work_order = repositories["work_order"].create_maintenance_work_order(
            unit_id=unit_id,
            summary="Mantenimiento post-reserva",
            description="Limpieza y verificación después de checkout",
            priority=3
        )
        
        # Assert
        assert reservation["id"] == reservation_id
        assert unit["id"] == unit_id
        assert work_order["unitId"] == unit_id
        assert work_order["status"] == "pending"
    
    def test_cache_invalidation_across_repositories(self, repositories, mock_api_client):
        """Test invalidación de cache entre repositories"""
        # Arrange
        unit_id = 100
        unit_data = {"id": unit_id, "name": "Casa de Playa"}
        mock_api_client.get.return_value = unit_data
        
        # Act - Obtener unidad (se cachea)
        unit1 = repositories["unit"].get_by_id(unit_id)
        
        # Act - Limpiar cache
        repositories["unit"]._clear_cache()
        
        # Act - Obtener unidad nuevamente (debería llamar API)
        unit2 = repositories["unit"].get_by_id(unit_id)
        
        # Assert
        assert unit1 == unit2
        assert mock_api_client.get.call_count == 2  # Dos llamadas a API
    
    def test_error_handling_consistency(self, repositories, mock_api_client):
        """Test consistencia en manejo de errores"""
        # Arrange
        mock_api_client.get.side_effect = APIError("Error de API")
        
        # Act & Assert - Todos los repositories deberían manejar errores igual
        for repo_name, repo in repositories.items():
            with pytest.raises(APIError):
                if hasattr(repo, 'get_by_id'):
                    repo.get_by_id(1)
                elif hasattr(repo, 'search'):
                    repo.search({})
