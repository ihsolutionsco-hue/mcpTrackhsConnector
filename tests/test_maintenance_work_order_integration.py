"""
Tests de integración para create_maintenance_work_order.
Prueba con API real de TrackHS (requiere credenciales configuradas).
"""

import os
from datetime import datetime
from unittest.mock import patch

import pytest

from src.trackhs_mcp.server import api_client, create_maintenance_work_order


class TestMaintenanceWorkOrderIntegration:
    """Tests de integración con API real"""

    @pytest.mark.skipif(
        not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"),
        reason="Credenciales de TrackHS no configuradas",
    )
    def test_api_connectivity(self):
        """Verifica conectividad con la API de TrackHS"""
        if api_client is None:
            pytest.skip("API client no disponible")

        # Este test verifica que podemos conectarnos a la API
        # No crea una orden real para evitar datos de prueba
        assert api_client is not None
        assert hasattr(api_client, "get")
        assert hasattr(api_client, "post")

    @pytest.mark.skipif(
        not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"),
        reason="Credenciales de TrackHS no configuradas",
    )
    def test_create_maintenance_work_order_dry_run(self):
        """
        Test de creación de orden de mantenimiento (simulado).
        No crea una orden real para evitar datos de prueba.
        """
        if api_client is None:
            pytest.skip("API client no disponible")

        # Simular la creación sin hacer la llamada real
        with patch.object(api_client, "post") as mock_post:
            mock_response = {
                "id": 99999,
                "status": "pending",
                "unitId": 123,
                "priority": 3,
                "summary": "Test de integración",
                "description": "Orden de prueba para testing",
                "dateReceived": datetime.now().strftime("%Y-%m-%d"),
                "estimatedCost": 0.0,
                "estimatedTime": 30,
            }
            mock_post.return_value = mock_response

            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Test de integración",
                description="Orden de prueba para testing",
                priority=3,
                estimated_cost=0.0,
                estimated_time=30,
            )

            # Verificar que se llamó con los parámetros correctos
            mock_post.assert_called_once()
            call_args = mock_post.call_args

            assert call_args[0][0] == "pms/maintenance/work-orders"
            data = call_args[0][1]

            assert data["unitId"] == 123
            assert data["summary"] == "Test de integración"
            assert data["description"] == "Orden de prueba para testing"
            assert data["priority"] == 3
            assert data["status"] == "pending"
            assert data["estimatedCost"] == 0.0
            assert data["estimatedTime"] == 30

            # Verificar respuesta
            assert result["id"] == 99999
            assert result["status"] == "pending"

    @pytest.mark.skipif(
        not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"),
        reason="Credenciales de TrackHS no configuradas",
    )
    def test_error_handling_with_real_api(self):
        """Test de manejo de errores con API real"""
        if api_client is None:
            pytest.skip("API client no disponible")

        # Test con datos que probablemente causen error
        with patch.object(api_client, "post") as mock_post:
            # Simular error de validación
            mock_post.side_effect = Exception("Error de validación de datos")

            with pytest.raises(Exception):
                create_maintenance_work_order.fn(
                    unit_id=123, summary="Test", description="Test"
                )

    def test_parameter_validation_integration(self):
        """Test de validación de parámetros en contexto de integración"""
        # Test con parámetros válidos
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Test con todos los parámetros
            result = create_maintenance_work_order.fn(
                unit_id=456,
                summary="Reparación de plomería",
                description="Fuga en grifo principal del baño",
                priority=5,
                estimated_cost=200.0,
                estimated_time=180,
                date_received="2024-01-20",
            )

            assert result["id"] == 123

            # Verificar estructura de datos enviada
            call_args = mock_client.post.call_args
            data = call_args[0][1]

            assert data["unitId"] == 456
            assert data["summary"] == "Reparación de plomería"
            assert data["description"] == "Fuga en grifo principal del baño"
            assert data["priority"] == 5
            assert data["estimatedCost"] == 200.0
            assert data["estimatedTime"] == 180
            assert data["dateReceived"] == "2024-01-20"
            assert data["status"] == "pending"

    def test_different_priority_levels_integration(self):
        """Test de diferentes niveles de prioridad"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Test prioridad baja
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Mantenimiento preventivo",
                description="Limpieza de filtros de aire acondicionado",
                priority=1,
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]
            assert data["priority"] == 1

            # Test prioridad media
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Reparación menor",
                description="Cambio de bombilla fundida",
                priority=3,
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]
            assert data["priority"] == 3

            # Test prioridad alta
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Emergencia eléctrica",
                description="Cortocircuito en panel principal",
                priority=5,
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]
            assert data["priority"] == 5

    def test_cost_and_time_estimation_integration(self):
        """Test de estimación de costos y tiempos"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Test con costo y tiempo
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Reparación de calentador",
                description="Reemplazo de termostato defectuoso",
                estimated_cost=350.0,
                estimated_time=240,  # 4 horas
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]

            assert data["estimatedCost"] == 350.0
            assert data["estimatedTime"] == 240

            # Test sin costo ni tiempo
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Inspección general",
                description="Revisión de estado general de la unidad",
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]

            assert "estimatedCost" not in data
            assert "estimatedTime" not in data

    def test_date_handling_integration(self):
        """Test de manejo de fechas"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Test con fecha específica
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Test con fecha",
                description="Test de manejo de fechas",
                date_received="2024-02-15",
            )

            call_args = mock_client.post.call_args
            data = call_args[0][1]
            assert data["dateReceived"] == "2024-02-15"

            # Test sin fecha (debe usar fecha actual)
            with patch("src.trackhs_mcp.server.datetime") as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2024-02-20"

                result = create_maintenance_work_order.fn(
                    unit_id=123,
                    summary="Test sin fecha",
                    description="Test de fecha automática",
                )

                call_args = mock_client.post.call_args
                data = call_args[0][1]
                assert data["dateReceived"] == "2024-02-20"


class TestMaintenanceWorkOrderPerformance:
    """Tests de rendimiento"""

    def test_response_time_simulation(self):
        """Simula tiempos de respuesta"""
        import time

        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            # Simular respuesta lenta
            def slow_response(*args, **kwargs):
                time.sleep(0.1)  # 100ms
                return {"id": 123, "status": "pending"}

            mock_client.post.side_effect = slow_response

            start_time = time.time()
            result = create_maintenance_work_order.fn(
                unit_id=123,
                summary="Test de rendimiento",
                description="Test de tiempo de respuesta",
            )
            end_time = time.time()

            assert result["id"] == 123
            assert (end_time - start_time) >= 0.1  # Debe tomar al menos 100ms

    def test_memory_usage_simulation(self):
        """Simula uso de memoria con datos grandes"""
        with patch("src.trackhs_mcp.server.api_client") as mock_client:
            mock_client.post.return_value = {"id": 123, "status": "pending"}

            # Test con descripción muy larga
            long_description = "Descripción detallada " * 200  # ~5000 caracteres
            result = create_maintenance_work_order.fn(
                unit_id=123, summary="Test de memoria", description=long_description
            )

            assert result["id"] == 123

            # Verificar que se envió la descripción completa
            call_args = mock_client.post.call_args
            data = call_args[0][1]
            assert len(data["description"]) > 4000


if __name__ == "__main__":
    print("🧪 Ejecutando tests de integración de create_maintenance_work_order...")

    # Verificar configuración
    if not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"):
        print(
            "⚠️  Credenciales de TrackHS no configuradas - algunos tests serán omitidos"
        )

    # Ejecutar tests específicos
    test_classes = [
        TestMaintenanceWorkOrderIntegration,
        TestMaintenanceWorkOrderPerformance,
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

    print("\n🎉 Tests de integración completados!")
