"""
Tests end-to-end para la herramienta create_maintenance_work_order.

Este módulo contiene tests E2E que validan el flujo completo de creación
de work orders desde la herramienta MCP hasta la API de TrackHS.
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from trackhs_mcp.domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)
from trackhs_mcp.infrastructure.mcp.create_maintenance_work_order import (
    register_create_maintenance_work_order,
)


class TestCreateWorkOrderE2E:
    """Tests E2E para create_maintenance_work_order."""

    @pytest.fixture
    def mock_mcp(self):
        """Mock del servidor MCP."""
        mcp = Mock()
        mcp.tool = Mock()
        return mcp

    @pytest.fixture
    def mock_api_client(self):
        """Mock del cliente API."""
        client = Mock()
        client.post = Mock()  # Síncrono para work orders
        return client

    @pytest.fixture
    def tool_function(self, mock_mcp, mock_api_client):
        """Función de herramienta registrada."""
        # Crear un mock que capture la función registrada
        registered_function = None

        def mock_tool_decorator(name=None, description=None):
            def decorator(func):
                nonlocal registered_function
                registered_function = func
                return func

            return decorator

        mock_mcp.tool = mock_tool_decorator
        register_create_maintenance_work_order(mcp=mock_mcp, api_client=mock_api_client)
        return registered_function

    @pytest.mark.e2e
    async def test_complete_flow_minimal_work_order(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test flujo completo con campos mínimos."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

        # Ejecutar función
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Mantenimiento preventivo",
            estimated_cost=75.50,
            estimated_time=60,
        )

        # Verificar resultado
        assert result["success"] is True
        assert result["work_order"]["id"] == 67890
        assert result["work_order"]["summary"] == "Mantenimiento preventivo"
        assert result["work_order"]["priority"] == 3
        assert result["work_order"]["status"] == "not-started"
        assert result["work_order"]["estimatedCost"] == 75.50
        assert result["work_order"]["estimatedTime"] == 60
        assert result["message"] == "Orden de trabajo creada exitosamente"

        # Verificar llamada a API
        mock_api_client.post.assert_called_once()
        call_args = mock_api_client.post.call_args
        assert call_args[0][0] == "/pms/maintenance/work-orders"

        payload = call_args[1]["data"]
        assert payload["dateReceived"] == "2024-01-15"
        assert payload["priority"] == 3
        assert payload["status"] == "not-started"
        assert payload["summary"] == "Mantenimiento preventivo"
        assert payload["estimatedCost"] == 75.50
        assert payload["estimatedTime"] == 60

    @pytest.mark.e2e
    async def test_complete_flow_full_work_order(
        self, tool_function, mock_api_client, sample_work_order_response
    ):
        """Test flujo completo con todos los campos."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_response)

        # Ejecutar función
        result = await tool_function(
            date_received="2024-01-15",
            priority=5,
            status="open",
            summary="Reparar aire acondicionado en unidad 101",
            estimated_cost=150.00,
            estimated_time=120,
            date_scheduled="2024-01-16T09:00:00Z",
            user_id=1,
            vendor_id=456,
            unit_id=123,
            reservation_id=37165851,
            reference_number="WO-2024-001",
            description="El aire acondicionado de la unidad 101 no está funcionando correctamente",
            work_performed="Diagnóstico inicial realizado",
            source="Guest Request",
            source_name="Juan Pérez",
            source_phone="+1234567890",
            actual_time=90,
            block_checkin=True,
        )

        # Verificar resultado
        assert result["success"] is True
        assert result["work_order"]["id"] == 12345
        assert (
            result["work_order"]["summary"]
            == "Reparar aire acondicionado en unidad 101"
        )
        assert result["work_order"]["priority"] == 5
        assert result["work_order"]["status"] == "open"
        assert result["work_order"]["estimatedCost"] == 150.00
        assert result["work_order"]["estimatedTime"] == 120
        assert result["work_order"]["dateScheduled"] == "2024-01-16T09:00:00Z"
        assert result["work_order"]["userId"] == 1
        assert result["work_order"]["vendorId"] == 456
        assert result["work_order"]["unitId"] == 123
        assert result["work_order"]["reservationId"] == 37165851
        assert result["work_order"]["referenceNumber"] == "WO-2024-001"
        assert (
            result["work_order"]["description"]
            == "El aire acondicionado de la unidad 101 no está funcionando correctamente"
        )
        assert result["work_order"]["workPerformed"] == "Diagnóstico inicial realizado"
        assert result["work_order"]["source"] == "Guest Request"
        assert result["work_order"]["sourceName"] == "Juan Pérez"
        assert result["work_order"]["sourcePhone"] == "+1234567890"
        assert result["work_order"]["actualTime"] == 90
        assert result["work_order"]["blockCheckin"] is True

        # Verificar payload completo
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]
        assert payload["dateScheduled"] == "2024-01-16T09:00:00Z"
        assert payload["userId"] == 1
        assert payload["vendorId"] == 456
        assert payload["unitId"] == 123
        assert payload["reservationId"] == 37165851
        assert payload["referenceNumber"] == "WO-2024-001"
        assert (
            payload["description"]
            == "El aire acondicionado de la unidad 101 no está funcionando correctamente"
        )
        assert payload["workPerformed"] == "Diagnóstico inicial realizado"
        assert payload["source"] == "Guest Request"
        assert payload["sourceName"] == "Juan Pérez"
        assert payload["sourcePhone"] == "+1234567890"
        assert payload["actualTime"] == 90
        assert payload["blockCheckin"] is True

    @pytest.mark.e2e
    async def test_high_priority_emergency_work_order(
        self, tool_function, mock_api_client, sample_work_order_high_priority
    ):
        """Test creación de work order de alta prioridad para emergencia."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_high_priority)

        # Ejecutar función
        result = await tool_function(
            date_received="2024-01-15T14:30:00Z",
            priority=5,
            status="in-progress",
            summary="Emergencia: Fuga de agua en unidad 205",
            estimated_cost=300.00,
            estimated_time=180,
            date_scheduled="2024-01-15T15:00:00Z",
            unit_id=205,
            description="Fuga de agua en el baño principal, requiere atención inmediata",
            source="Guest Call",
            source_name="María García",
            source_phone="+1987654321",
            block_checkin=True,
        )

        # Verificar resultado
        assert result["success"] is True
        assert result["work_order"]["id"] == 11111
        assert (
            result["work_order"]["summary"] == "Emergencia: Fuga de agua en unidad 205"
        )
        assert result["work_order"]["priority"] == 5
        assert result["work_order"]["status"] == "in-progress"
        assert result["work_order"]["estimatedCost"] == 300.00
        assert result["work_order"]["estimatedTime"] == 180
        assert result["work_order"]["unitId"] == 205
        assert result["work_order"]["blockCheckin"] is True

    @pytest.mark.e2e
    async def test_vendor_assigned_work_order(
        self, tool_function, mock_api_client, sample_work_order_vendor_assigned
    ):
        """Test creación de work order asignada a proveedor."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_vendor_assigned)

        # Ejecutar función
        result = await tool_function(
            date_received="2024-01-14",
            priority=3,
            status="vendor-assigned",
            summary="Instalación de nuevo sistema de seguridad",
            estimated_cost=500.00,
            estimated_time=240,
            date_scheduled="2024-01-17T08:00:00Z",
            vendor_id=789,
            unit_id=150,
            reference_number="SEC-2024-001",
            description="Instalación de sistema de cámaras de seguridad",
            source="Management Request",
            source_name="Carlos López",
            source_phone="+1555123456",
            block_checkin=False,
        )

        # Verificar resultado
        assert result["success"] is True
        assert result["work_order"]["id"] == 22222
        assert (
            result["work_order"]["summary"]
            == "Instalación de nuevo sistema de seguridad"
        )
        assert result["work_order"]["priority"] == 3
        assert result["work_order"]["status"] == "vendor-assigned"
        assert result["work_order"]["estimatedCost"] == 500.00
        assert result["work_order"]["estimatedTime"] == 240
        assert result["work_order"]["vendorId"] == 789
        assert result["work_order"]["unitId"] == 150
        assert result["work_order"]["referenceNumber"] == "SEC-2024-001"
        assert result["work_order"]["blockCheckin"] is False

    @pytest.mark.e2e
    async def test_type_conversion_string_parameters(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test conversión de tipos string a tipos correctos."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

        # Ejecutar función con parámetros string
        result = await tool_function(
            date_received="2024-01-15",
            priority="5",  # String
            status="open",
            summary="Test con strings",
            estimated_cost="150.50",  # String
            estimated_time="120",  # String
            user_id="1",  # String
            vendor_id="456",  # String
            unit_id="123",  # String
            reservation_id="37165851",  # String
            actual_time="90",  # String
            block_checkin="true",  # String
        )

        # Verificar resultado
        assert result["success"] is True

        # Verificar conversión en payload
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]
        assert payload["priority"] == 5
        assert payload["estimatedCost"] == 150.50
        assert payload["estimatedTime"] == 120
        assert payload["userId"] == 1
        assert payload["vendorId"] == 456
        assert payload["unitId"] == 123
        assert payload["reservationId"] == 37165851
        assert payload["actualTime"] == 90
        assert payload["blockCheckin"] is True

    @pytest.mark.e2e
    async def test_all_valid_priorities(self, tool_function, mock_api_client):
        """Test todas las prioridades válidas."""
        valid_priorities = [1, 3, 5]

        for priority in valid_priorities:
            # Crear mock dinámico para cada prioridad
            mock_response = {
                "id": 67890,
                "dateReceived": "2024-01-15",
                "priority": priority,
                "status": "not-started",
                "summary": f"Test priority {priority}",
                "estimatedCost": 75.50,
                "estimatedTime": 60,
                "createdAt": "2024-01-15T10:30:00Z",
                "updatedAt": "2024-01-15T10:30:00Z",
                "createdBy": "system",
                "updatedBy": "system",
                "_embedded": {},
                "_links": {"self": {"href": "/api/pms/maintenance/work-orders/67890"}},
            }
            from unittest.mock import AsyncMock

            mock_api_client.post = AsyncMock(return_value=mock_response)

            result = await tool_function(
                date_received="2024-01-15",
                priority=priority,
                status="not-started",
                summary=f"Test priority {priority}",
                estimated_cost=75.50,
                estimated_time=60,
            )

            assert result["success"] is True, f"Priority {priority} should be valid"
            assert result["work_order"]["priority"] == priority

    @pytest.mark.e2e
    async def test_all_valid_statuses(self, tool_function, mock_api_client):
        """Test todos los estados válidos."""
        valid_statuses = [
            "open",
            "not-started",
            "in-progress",
            "completed",
            "processed",
            "vendor-not-start",
            "vendor-assigned",
            "vendor-declined",
            "vendor-completed",
            "user-completed",
            "cancelled",
        ]

        for status in valid_statuses:
            # Crear mock dinámico para cada estado
            mock_response = {
                "id": 67890,
                "dateReceived": "2024-01-15",
                "priority": 3,
                "status": status,
                "summary": f"Test status {status}",
                "estimatedCost": 75.50,
                "estimatedTime": 60,
                "createdAt": "2024-01-15T10:30:00Z",
                "updatedAt": "2024-01-15T10:30:00Z",
                "createdBy": "system",
                "updatedBy": "system",
                "_embedded": {},
                "_links": {"self": {"href": "/api/pms/maintenance/work-orders/67890"}},
            }
            from unittest.mock import AsyncMock

            mock_api_client.post = AsyncMock(return_value=mock_response)

            result = await tool_function(
                date_received="2024-01-15",
                priority=3,
                status=status,
                summary=f"Test status {status}",
                estimated_cost=75.50,
                estimated_time=60,
            )

            assert result["success"] is True, f"Status {status} should be valid"
            assert result["work_order"]["status"] == status

    @pytest.mark.e2e
    async def test_validation_error_missing_required_fields(self, tool_function):
        """Test error de validación con campos requeridos faltantes."""
        # Fecha faltante
        result = await tool_function(
            date_received="",  # Vacío
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "fecha de recepción es requerida" in result["message"]

    @pytest.mark.e2e
    async def test_validation_error_invalid_date_format(self, tool_function):
        """Test error de validación con formato de fecha inválido."""
        result = await tool_function(
            date_received="15-01-2024",  # Formato inválido
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "formato ISO 8601" in result["message"]

    @pytest.mark.e2e
    async def test_validation_error_invalid_priority(self, tool_function):
        """Test error de validación con prioridad inválida."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=2,  # Inválida
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "prioridad debe ser 1 (Baja), 3 (Media) o 5 (Alta)" in result["message"]

    @pytest.mark.e2e
    async def test_validation_error_invalid_status(self, tool_function):
        """Test error de validación con estado inválido."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="invalid-status",  # Inválido
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "Estado inválido" in result["message"]

    @pytest.mark.e2e
    async def test_validation_error_negative_cost(self, tool_function):
        """Test error de validación con costo negativo."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=-10.0,  # Negativo
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "costo estimado no puede ser negativo" in result["message"]

    @pytest.mark.e2e
    async def test_validation_error_zero_time(self, tool_function):
        """Test error de validación con tiempo cero."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=0,  # Cero
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "tiempo estimado debe ser mayor a 0" in result["message"]

    @pytest.mark.e2e
    async def test_authentication_error_handling(self, tool_function, mock_api_client):
        """Test manejo de error de autenticación."""
        # Configurar mock para lanzar AuthenticationError
        mock_api_client.post.side_effect = AuthenticationError("Credenciales inválidas")

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "No autorizado"
        assert "Credenciales inválidas" in result["message"]

    @pytest.mark.e2e
    async def test_authorization_error_handling(self, tool_function, mock_api_client):
        """Test manejo de error de autorización."""
        # Configurar mock para lanzar AuthorizationError
        mock_api_client.post.side_effect = AuthorizationError("Permisos insuficientes")

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Prohibido"
        assert "Permisos insuficientes" in result["message"]

    @pytest.mark.e2e
    async def test_api_error_401_handling(self, tool_function, mock_api_client):
        """Test manejo de error 401 de API."""
        # Configurar mock para lanzar ApiError 401
        mock_api_client.post.side_effect = ApiError("Unauthorized", 401)

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "No autorizado"
        assert "Credenciales de autenticación inválidas" in result["message"]

    @pytest.mark.e2e
    async def test_api_error_403_handling(self, tool_function, mock_api_client):
        """Test manejo de error 403 de API."""
        # Configurar mock para lanzar ApiError 403
        mock_api_client.post.side_effect = ApiError("Forbidden", 403)

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Prohibido"
        assert "Permisos insuficientes" in result["message"]

    @pytest.mark.e2e
    async def test_api_error_422_handling(self, tool_function, mock_api_client):
        """Test manejo de error 422 de API."""
        # Configurar mock para lanzar ApiError 422
        mock_api_client.post.side_effect = ApiError("Validation failed", 422)

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "Validation failed" in result["message"]

    @pytest.mark.e2e
    async def test_api_error_500_handling(self, tool_function, mock_api_client):
        """Test manejo de error 500 de API."""
        # Configurar mock para lanzar ApiError 500
        mock_api_client.post.side_effect = ApiError("Internal Server Error", 500)

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Error inesperado"
        assert "Error interno del servidor" in result["message"]

    @pytest.mark.e2e
    async def test_unexpected_error_handling(self, tool_function, mock_api_client):
        """Test manejo de error inesperado."""
        # Configurar mock para lanzar excepción genérica
        mock_api_client.post.side_effect = Exception("Unexpected error")

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
        )

        assert result["success"] is False
        assert result["error"] == "Error de API"
        assert "Unexpected error" in result["message"]

    @pytest.mark.e2e
    async def test_response_format_with_embedded_data(
        self, tool_function, mock_api_client, sample_work_order_response
    ):
        """Test formato de respuesta con datos embebidos."""
        # Configurar mock
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_response)

        result = await tool_function(
            date_received="2024-01-15",
            priority=5,
            status="open",
            summary="Test",
            estimated_cost=150.00,
            estimated_time=120,
        )

        # Verificar estructura de respuesta
        assert result["success"] is True
        assert "work_order" in result
        assert "message" in result

        # Verificar estructura de work_order
        work_order = result["work_order"]
        assert "id" in work_order
        assert "dateReceived" in work_order
        assert "priority" in work_order
        assert "status" in work_order
        assert "summary" in work_order
        assert "estimatedCost" in work_order
        assert "estimatedTime" in work_order

        # Verificar datos embebidos
        assert "_embedded" in work_order
        assert "unit" in work_order["_embedded"]
        assert "vendor" in work_order["_embedded"]
        assert "user" in work_order["_embedded"]

        # Verificar enlaces
        assert "_links" in work_order
        assert "self" in work_order["_links"]
        assert "unit" in work_order["_links"]
        assert "vendor" in work_order["_links"]

    @pytest.mark.e2e
    async def test_iso8601_date_formats(self, tool_function, mock_api_client):
        """Test diferentes formatos de fecha ISO 8601."""
        valid_date_formats = [
            "2024-01-15",
            "2024-01-15T10:30:00Z",
            "2024-01-15T10:30:00+00:00",
            "2024-01-15T10:30:00-05:00",
        ]

        for date_format in valid_date_formats:
            # Crear mock dinámico para cada formato de fecha
            mock_response = {
                "id": 67890,
                "dateReceived": date_format,
                "priority": 3,
                "status": "not-started",
                "summary": f"Test date {date_format}",
                "estimatedCost": 75.50,
                "estimatedTime": 60,
                "createdAt": "2024-01-15T10:30:00Z",
                "updatedAt": "2024-01-15T10:30:00Z",
                "createdBy": "system",
                "updatedBy": "system",
                "_embedded": {},
                "_links": {"self": {"href": "/api/pms/maintenance/work-orders/67890"}},
            }
            from unittest.mock import AsyncMock

            mock_api_client.post = AsyncMock(return_value=mock_response)

            result = await tool_function(
                date_received=date_format,
                priority=3,
                status="not-started",
                summary=f"Test date {date_format}",
                estimated_cost=75.50,
                estimated_time=60,
            )

            assert (
                result["success"] is True
            ), f"Date format {date_format} should be valid"
            assert result["work_order"]["dateReceived"] == date_format
