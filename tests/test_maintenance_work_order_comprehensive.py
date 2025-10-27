"""
Tests comprehensivos para create_maintenance_work_order.
Cubre validación de parámetros, manejo de errores, y casos edge.
"""

import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.trackhs_mcp.exceptions import (
    APIError,
    AuthenticationError,
    TrackHSError,
    ValidationError,
)
from src.trackhs_mcp.server import create_maintenance_work_order


class TestMaintenanceWorkOrderValidation:
    """Tests de validación de parámetros"""

    def test_required_parameters_validation(self):
        """Verifica que los parámetros requeridos son validados correctamente"""
        # Test con parámetros mínimos requeridos
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Debe funcionar con parámetros mínimos
            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test summary", description="Test description"
            )
            assert result["id"] == 123

    def test_unit_id_validation(self):
        """Verifica validación de unit_id"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # unit_id debe ser mayor que 0 - FastMCP valida esto a nivel de schema
            # La validación ocurre antes de que se ejecute la función
            with pytest.raises((ValueError, TypeError, AssertionError)):
                create_maintenance_work_order.fn(
                    unit_id=0, summary="Test", description="Test"
                )

    def test_summary_length_validation(self):
        """Verifica validación de longitud de summary"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Summary muy corto
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="", description="Test description"
                )

            # Summary muy largo (más de 500 caracteres)
            long_summary = "x" * 501
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary=long_summary, description="Test description"
                )

    def test_description_length_validation(self):
        """Verifica validación de longitud de description"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Description muy corta
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test summary", description=""
                )

            # Description muy larga (más de 5000 caracteres)
            long_description = "x" * 5001
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test summary", description=long_description
                )

    def test_priority_validation(self):
        """Verifica validación de prioridad"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Prioridades válidas
            for priority in [1, 3, 5]:
                result = create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test", priority=priority
                )
                assert result["id"] == 123

            # Prioridad inválida
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123,
                    summary="Test",
                    description="Test",
                    priority=2,  # Prioridad inválida
                )

    def test_estimated_cost_validation(self):
        """Verifica validación de costo estimado"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Costo válido
            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test", description="Test", estimated_cost=100.50
            )
            assert result["id"] == 123

            # Costo negativo
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123,
                    summary="Test",
                    description="Test",
                    estimated_cost=-10.0,
                )

    def test_estimated_time_validation(self):
        """Verifica validación de tiempo estimado"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Tiempo válido
            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test", description="Test", estimated_time=120
            )
            assert result["id"] == 123

            # Tiempo negativo
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test", estimated_time=-30
                )

    def test_date_received_validation(self):
        """Verifica validación de fecha de recepción"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Fecha válida
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Test",
                description="Test",
                date_received="2024-01-15",
            )
            assert result["id"] == 123

            # Formato de fecha inválido
            with pytest.raises(ValueError):
                create_maintenance_work_order.fn(
                    unit_id=123,
                    summary="Test",
                    description="Test",
                    date_received="15-01-2024",  # Formato incorrecto
                )


class TestMaintenanceWorkOrderDataPreparation:
    """Tests de preparación de datos"""

    def test_data_structure_with_all_parameters(self):
        """Verifica estructura de datos con todos los parámetros"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            result = create_maintenance_work_order.fn(
                unit_id=456,
                summary="Fuga en grifo",
                description="Grifo del baño principal gotea constantemente",
                priority=3,
                estimated_cost=150.0,
                estimated_time=90,
                date_received="2024-01-15",
            )

            # Verificar que se llamó con los datos correctos
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args

            assert call_args[0][0] == "pms/maintenance/work-orders"
            data = call_args[0][1]

            assert data["unitId"] == 456
            assert data["summary"] == "Fuga en grifo"
            assert (
                data["description"] == "Grifo del baño principal gotea constantemente"
            )
            assert data["priority"] == 3
            assert data["status"] == "pending"
            assert data["estimatedCost"] == 150.0
            assert data["estimatedTime"] == 90
            assert data["dateReceived"] == "2024-01-15"

    def test_data_structure_with_minimal_parameters(self):
        """Verifica estructura de datos con parámetros mínimos"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            result = create_maintenance_work_order.fn(
                unit_id=789, summary="Test summary", description="Test description"
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]

            assert data["unitId"] == 789
            assert data["summary"] == "Test summary"
            assert data["description"] == "Test description"
            assert data["priority"] == 3  # Default
            assert data["status"] == "pending"
            assert "estimatedCost" not in data
            assert "estimatedTime" not in data
            # dateReceived debe ser la fecha actual
            assert "dateReceived" in data

    def test_default_date_received(self):
        """Verifica que se usa la fecha actual cuando no se proporciona date_received"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            with patch("src.trackhs_mcp.server.datetime") as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2024-01-20"

                result = create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

                call_args = mock_client.post.call_args
                data = call_args[0][1]
                assert data["dateReceived"] == "2024-01-20"


class TestMaintenanceWorkOrderErrorHandling:
    """Tests de manejo de errores"""

    def test_api_client_not_available(self):
        """Verifica manejo cuando api_client no está disponible"""
        with patch("src.trackhs_mcp.server.api_client", None):
            with pytest.raises(AuthenticationError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

    def test_api_error_handling(self):
        """Verifica manejo de errores de API"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.side_effect = APIError("Error de API")

            with pytest.raises(APIError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

    def test_authentication_error_handling(self):
        """Verifica manejo de errores de autenticación"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.side_effect = AuthenticationError("Credenciales inválidas")

            with pytest.raises(AuthenticationError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

    def test_validation_error_handling(self):
        """Verifica manejo de errores de validación"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.side_effect = ValidationError("Datos inválidos")

            with pytest.raises(ValidationError):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

    def test_generic_error_handling(self):
        """Verifica manejo de errores genéricos"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.side_effect = Exception("Error inesperado")

            with pytest.raises(Exception):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )


class TestMaintenanceWorkOrderResponseValidation:
    """Tests de validación de respuesta"""

    def test_successful_response_validation(self):
        """Verifica validación de respuesta exitosa"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_response = {
                "id": 123,
                "status": "pending",
                "unitId": 456,
                "priority": 3,
                "summary": "Test summary",
                "description": "Test description",
            }
            mock_client.post.return_value = mock_response

            result = create_maintenance_work_order.fn(
                unit_id=456, summary="Test summary", description="Test description"
            )

            assert result["id"] == 123
            assert result["status"] == "pending"

    def test_response_validation_with_extra_fields(self):
        """Verifica que campos adicionales en la respuesta son manejados"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_response = {
                "id": 123,
                "status": "pending",
                "unitId": 456,
                "priority": 3,
                "summary": "Test summary",
                "description": "Test description",
                "extraField": "extra_value",
                "anotherField": 999,
            }
            mock_client.post.return_value = mock_response

            result = create_maintenance_work_order.fn(
                unit_id=456, summary="Test summary", description="Test description"
            )

            # Debe incluir campos extra debido a model_config = {"extra": "allow"}
            assert result["extraField"] == "extra_value"
            assert result["anotherField"] == 999


class TestMaintenanceWorkOrderLogging:
    """Tests de logging"""

    def test_success_logging(self):
        """Verifica logging de éxito"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_response = {"id": 123, "status": "pending"}
            mock_client.post.return_value = mock_response

            with patch("src.trackhs_mcp.server.logger") as mock_logger:
                result = create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

                # Verificar que se logueó la creación
                mock_logger.info.assert_any_call(
                    "Creando orden de mantenimiento para unidad 123, prioridad: 3"
                )
                mock_logger.info.assert_any_call(
                    "Orden de mantenimiento creada exitosamente. ID: 123"
                )

    def test_error_logging(self):
        """Verifica logging de errores"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.side_effect = Exception("Error de prueba")

            with patch("src.trackhs_mcp.server.logger") as mock_logger:
                with pytest.raises(Exception):
                    create_maintenance_work_order.fn(
                        unit_id=123, summary="Test", description="Test"
                    )

                # Verificar que se logueó el error
                mock_logger.error.assert_called_with(
                    "Error creando orden de mantenimiento: Error de prueba"
                )


class TestMaintenanceWorkOrderEdgeCases:
    """Tests de casos edge"""

    def test_very_long_summary(self):
        """Verifica manejo de summary en el límite de longitud"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Summary de exactamente 500 caracteres (límite máximo)
            max_summary = "x" * 500
            result = create_maintenance_work_order.fn(
                unit_id=123, summary=max_summary, description="Test description"
            )
            assert result["id"] == 123

    def test_very_long_description(self):
        """Verifica manejo de description en el límite de longitud"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Description de exactamente 5000 caracteres (límite máximo)
            max_description = "x" * 5000
            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test summary", description=max_description
            )
            assert result["id"] == 123

    def test_zero_estimated_cost(self):
        """Verifica manejo de costo estimado cero"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test", description="Test", estimated_cost=0.0
            )
            assert result["id"] == 123

    def test_zero_estimated_time(self):
        """Verifica manejo de tiempo estimado cero"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test", description="Test", estimated_time=0
            )
            assert result["id"] == 123


if __name__ == "__main__":
    print("🧪 Ejecutando tests comprehensivos de create_maintenance_work_order...")

    # Ejecutar tests específicos
    test_classes = [
        TestMaintenanceWorkOrderValidation,
        TestMaintenanceWorkOrderDataPreparation,
        TestMaintenanceWorkOrderErrorHandling,
        TestMaintenanceWorkOrderResponseValidation,
        TestMaintenanceWorkOrderLogging,
        TestMaintenanceWorkOrderEdgeCases,
    ]

    for test_class in test_classes:
        print(f"\n📋 Ejecutando {test_class.__name__}...")
        test_instance = test_class()

        for method_name in dir(test_instance):
            if method_name.startswith("test_"):
                try:
                    method = getattr(test_instance, method_name)
                    method()
                    print(f"  ✅ {method_name}")
                except Exception as e:
                    print(f"  ❌ {method_name}: {e}")

    print("\n🎉 Tests comprehensivos completados!")
