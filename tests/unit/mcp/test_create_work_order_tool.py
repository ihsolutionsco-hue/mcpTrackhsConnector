"""
Tests unitarios para la herramienta MCP create_maintenance_work_order.

Este módulo contiene tests para validar el comportamiento de la herramienta
MCP de creación de work orders siguiendo el patrón de tests existentes.
"""

from datetime import datetime
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


class TestCreateMaintenanceWorkOrderTool:
    """Tests para la herramienta create_maintenance_work_order."""

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

    async def test_tool_registration(self, mock_mcp, mock_api_client):
        """Test que la herramienta se registra correctamente."""
        register_create_maintenance_work_order(mcp=mock_mcp, api_client=mock_api_client)

        # Verificar que se llamó mcp.tool
        mock_mcp.tool.assert_called_once()
        call_args = mock_mcp.tool.call_args

        # Verificar nombre de la herramienta
        assert call_args[1]["name"] == "create_maintenance_work_order"
        assert "description" in call_args[1]

    async def test_successful_creation_minimal(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test creación exitosa con campos mínimos."""
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
        print(f"Result type: {type(result)}")
        print(f"Result content: {result}")
        assert result["success"] is True
        assert result["work_order"]["id"] == 67890
        assert result["work_order"]["summary"] == "Mantenimiento preventivo"
        assert result["message"] == "Orden de trabajo creada exitosamente"

        # Verificar llamada a API
        mock_api_client.post.assert_called_once()
        call_args = mock_api_client.post.call_args
        assert call_args[0][0] == "/pms/maintenance/work-orders"
        assert call_args[1]["data"]["dateReceived"] == "2024-01-15"
        assert call_args[1]["data"]["priority"] == 3
        assert call_args[1]["data"]["status"] == "not-started"

    async def test_successful_creation_complete(
        self, tool_function, mock_api_client, sample_work_order_response
    ):
        """Test creación exitosa con todos los campos."""
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
            source="Guest Request",
            source_name="Juan Pérez",
            source_phone="+1234567890",
            block_checkin=True,
        )

        # Verificar resultado
        assert result["success"] is True
        assert result["work_order"]["id"] == 12345
        assert (
            result["work_order"]["summary"]
            == "Reparar aire acondicionado en unidad 101"
        )

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
        assert payload["source"] == "Guest Request"
        assert payload["sourceName"] == "Juan Pérez"
        assert payload["sourcePhone"] == "+1234567890"
        assert payload["blockCheckin"] is True

    async def test_type_conversion_string_to_int(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test conversión de tipos string a int."""
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

        result = await tool_function(
            date_received="2024-01-15",
            priority="3",  # String
            status="not-started",
            summary="Test",
            estimated_cost="75.50",  # String
            estimated_time="60",  # String
            user_id="1",  # String
            vendor_id="456",  # String
            unit_id="123",  # String
            reservation_id="37165851",  # String
            actual_time="90",  # String
        )

        assert result["success"] is True

        # Verificar conversión en payload
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]
        assert payload["priority"] == 3
        assert payload["estimatedCost"] == 75.50
        assert payload["estimatedTime"] == 60
        assert payload["userId"] == 1
        assert payload["vendorId"] == 456
        assert payload["unitId"] == 123
        assert payload["reservationId"] == 37165851
        assert payload["actualTime"] == 90

    async def test_type_conversion_string_to_bool(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test conversión de tipos string a bool."""
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
            block_checkin="true",  # String
        )

        assert result["success"] is True

        # Verificar conversión en payload
        call_args = mock_api_client.post.call_args
        payload = call_args[1]["data"]
        assert payload["blockCheckin"] is True

    async def test_validation_missing_required_fields(self, tool_function):
        """Test validación de campos requeridos faltantes."""
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

    async def test_validation_invalid_date_format(self, tool_function):
        """Test validación de formato de fecha inválido."""
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

    async def test_validation_invalid_priority(self, tool_function):
        """Test validación de prioridad inválida."""
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

    async def test_validation_invalid_status(self, tool_function):
        """Test validación de estado inválido."""
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

    async def test_validation_negative_cost(self, tool_function):
        """Test validación de costo negativo."""
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

    async def test_validation_zero_time(self, tool_function):
        """Test validación de tiempo cero."""
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

    async def test_validation_invalid_scheduled_date(self, tool_function):
        """Test validación de fecha programada inválida."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
            date_scheduled="16-01-2024",  # Formato inválido
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "fecha programada debe estar en formato ISO 8601" in result["message"]

    async def test_validation_negative_ids(self, tool_function):
        """Test validación de IDs negativos."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
            user_id=-1,  # Negativo
            vendor_id=0,  # Cero
            unit_id=-5,  # Negativo
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "ID de usuario debe ser un entero positivo" in result["message"]

    async def test_validation_zero_actual_time(self, tool_function):
        """Test validación de tiempo real cero."""
        result = await tool_function(
            date_received="2024-01-15",
            priority=3,
            status="not-started",
            summary="Test",
            estimated_cost=75.50,
            estimated_time=60,
            actual_time=0,  # Cero
        )

        assert result["success"] is False
        assert result["error"] == "Datos inválidos"
        assert "tiempo real debe ser mayor a 0" in result["message"]

    async def test_authentication_error(self, tool_function, mock_api_client):
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

    async def test_authorization_error(self, tool_function, mock_api_client):
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

    async def test_api_error_401(self, tool_function, mock_api_client):
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

    async def test_api_error_403(self, tool_function, mock_api_client):
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

    async def test_api_error_422(self, tool_function, mock_api_client):
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

    async def test_api_error_500(self, tool_function, mock_api_client):
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

    async def test_unexpected_error(self, tool_function, mock_api_client):
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

    async def test_all_valid_statuses(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test todos los estados válidos."""
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

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
            result = await tool_function(
                date_received="2024-01-15",
                priority=3,
                status=status,
                summary="Test",
                estimated_cost=75.50,
                estimated_time=60,
            )

            assert result["success"] is True, f"Status {status} should be valid"

    async def test_all_valid_priorities(
        self, tool_function, mock_api_client, sample_work_order_minimal
    ):
        """Test todas las prioridades válidas."""
        from unittest.mock import AsyncMock

        mock_api_client.post = AsyncMock(return_value=sample_work_order_minimal)

        valid_priorities = [1, 3, 5]

        for priority in valid_priorities:
            result = await tool_function(
                date_received="2024-01-15",
                priority=priority,
                status="not-started",
                summary="Test",
                estimated_cost=75.50,
                estimated_time=60,
            )

            assert result["success"] is True, f"Priority {priority} should be valid"

    async def test_response_format(
        self, tool_function, mock_api_client, sample_work_order_response
    ):
        """Test formato de respuesta correcto."""
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
        assert "success" in result
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
