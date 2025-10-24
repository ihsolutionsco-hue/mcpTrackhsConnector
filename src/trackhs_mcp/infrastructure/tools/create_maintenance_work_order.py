"""
Herramienta MCP para crear órdenes de trabajo de mantenimiento.

Esta herramienta permite crear work orders en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from ...application.ports.api_client_port import ApiClientPort
from ...application.use_cases.create_work_order import CreateWorkOrderUseCase
from ...domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrderStatus,
)
from ...domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)
from ..utils.date_validation import is_valid_iso8601_date

# from ..utils.error_handling import error_handler
from ..utils.type_normalization import (
    normalize_string_to_bool,
    normalize_string_to_float,
    normalize_string_to_int,
)


def register_create_maintenance_work_order(mcp, api_client: ApiClientPort):
    """
    Registrar la herramienta MCP para crear work orders.

    Args:
        mcp: Instancia del servidor MCP
        api_client: Cliente API para TrackHS
    """

    @mcp.tool(
        name="create_maintenance_work_order",
        description="Crear una nueva orden de trabajo de mantenimiento en TrackHS. Ideal para llamadas de servicio al cliente, emergencias, mantenimiento preventivo y reparaciones. Soporta prioridades textuales intuitivas (trivial, low, medium, high, critical) y casos de uso reales de hospitalidad.",
    )
    async def create_maintenance_work_order(
        date_received: str = Field(
            description="Date received in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). Example: '2024-01-15'",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
            min_length=10,
            max_length=20,
        ),
        priority: str = Field(
            description="Priority level for customer service calls: trivial (minor issues), low (routine maintenance), medium (standard repairs), high (guest comfort issues), critical (emergencies like water leaks, electrical problems). Maps to API values: trivial/low→1, medium→3, high/critical→5",
            pattern="^(trivial|low|medium|high|critical)$",
        ),
        status: str = Field(
            description="Work order status. Valid: open, not-started, in-progress, completed, processed, vendor-assigned, vendor-accepted, vendor-rejected, vendor-completed, cancelled",
            min_length=1,
            max_length=50,
        ),
        summary: str = Field(
            description="Brief summary of the work order for customer service. Use clear, descriptive language like 'AC not working in bedroom', 'Water leak in bathroom', 'WiFi connectivity issues'. Required, non-empty.",
            min_length=1,
            max_length=500,
        ),
        estimated_cost: float = Field(
            description="Estimated cost in currency units (must be >= 0). Example: 150.00",
            ge=0.0,
        ),
        estimated_time: int = Field(
            description="Estimated time in minutes (must be > 0). Example: 120", ge=1
        ),
        date_scheduled: Optional[str] = Field(
            default=None,
            description="Scheduled date in ISO 8601 format. Example: '2024-01-16T09:00:00Z'",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
            min_length=10,
            max_length=20,
        ),
        user_id: Optional[int] = Field(
            default=None,
            description="ID of responsible user (positive integer). Example: 123",
            ge=1,
        ),
        vendor_id: Optional[int] = Field(
            default=None,
            description="ID of assigned vendor (positive integer). Example: 456",
            ge=1,
        ),
        unit_id: Optional[int] = Field(
            default=1,
            description="ID of related unit (positive integer). REQUIRED by API. Example: 789. Default: 1",
            ge=1,
        ),
        reservation_id: Optional[int] = Field(
            default=None,
            description="ID of related reservation (positive integer). Example: 101112",
            ge=1,
        ),
        reference_number: Optional[str] = Field(
            default=None, description="Reference number or external ID", max_length=100
        ),
        description: Optional[str] = Field(
            default=None,
            description="Detailed description of the work order",
            max_length=2000,
        ),
        work_performed: Optional[str] = Field(
            default=None, description="Description of work performed", max_length=2000
        ),
        source: Optional[str] = Field(
            default=None,
            description="Source of the work order for customer service tracking. Common values: 'Guest Request' (guest reported issue), 'Inspection' (routine inspection), 'Preventive Maintenance' (scheduled maintenance), 'Emergency' (urgent issues).",
            max_length=100,
        ),
        source_name: Optional[str] = Field(
            default=None,
            description="Name of the person who reported the issue (guest name, staff member, inspector). Example: 'Maria Garcia' for guest requests.",
            max_length=200,
        ),
        source_phone: Optional[str] = Field(
            default=None,
            description="Phone number of the person who reported the issue. Include country code. Example: '+1234567890' for US numbers, '+34612345678' for Spain.",
            max_length=50,
        ),
        actual_time: Optional[int] = Field(
            default=None,
            description="Actual time spent in minutes (must be > 0). Example: 90",
            ge=1,
        ),
        block_checkin: Optional[int] = Field(
            default=None, description="Block check-in flag: 0=no, 1=yes", ge=0, le=1
        ),
    ) -> Dict[str, Any]:
        """
        Create a new maintenance work order in TrackHS for customer service scenarios.

        Perfect for handling guest requests, emergencies, preventive maintenance, and repairs.
        Uses intuitive textual priorities (trivial, low, medium, high, critical) that automatically
        map to API values. Supports complete customer service workflows including guest contact
        information, source tracking, and emergency blocking.

        Common use cases:
        - Guest reports AC not working (priority: high)
        - Water leak emergency (priority: critical, block_checkin: true)
        - Routine maintenance (priority: low, source: 'Preventive Maintenance')
        - WiFi connectivity issues (priority: medium)
        - Vendor repairs (status: 'vendor-assigned')

        Returns complete work order data with ID and metadata for tracking.
        """
        try:
            # Detectar y convertir FieldInfo objects a None (cuando se llama directamente sin FastMCP)
            if type(date_scheduled).__name__ == "FieldInfo":
                date_scheduled = None
            if type(user_id).__name__ == "FieldInfo":
                user_id = None
            if type(vendor_id).__name__ == "FieldInfo":
                vendor_id = None
            if type(unit_id).__name__ == "FieldInfo":
                unit_id = None
            if type(reservation_id).__name__ == "FieldInfo":
                reservation_id = None
            if type(reference_number).__name__ == "FieldInfo":
                reference_number = None
            if type(description).__name__ == "FieldInfo":
                description = None
            if type(work_performed).__name__ == "FieldInfo":
                work_performed = None
            if type(source).__name__ == "FieldInfo":
                source = None
            if type(source_name).__name__ == "FieldInfo":
                source_name = None
            if type(source_phone).__name__ == "FieldInfo":
                source_phone = None
            if type(actual_time).__name__ == "FieldInfo":
                actual_time = None
            if type(block_checkin).__name__ == "FieldInfo":
                block_checkin = None

            # Validar prioridad textual con mensaje mejorado
            valid_priorities = ["trivial", "low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValidationError(
                    f"La prioridad debe ser una de: {', '.join(valid_priorities)}. "
                    f"Valor recibido: '{priority}'. "
                    f"Use prioridades textuales intuitivas: trivial (problemas menores), "
                    f"low (mantenimiento rutinario), medium (reparaciones estándar), "
                    f"high (problemas de comodidad), critical (emergencias)."
                )

            # Normalizar tipos de entrada (priority ya es string, no necesita normalización)
            estimated_cost = normalize_string_to_float(estimated_cost)
            estimated_time = normalize_string_to_int(estimated_time)

            # Normalizar campos opcionales
            if user_id is not None:
                user_id = normalize_string_to_int(user_id)
            if vendor_id is not None:
                vendor_id = normalize_string_to_int(vendor_id)
            if unit_id is not None:
                unit_id = normalize_string_to_int(unit_id)
            if reservation_id is not None:
                reservation_id = normalize_string_to_int(reservation_id)
            if actual_time is not None:
                actual_time = normalize_string_to_int(actual_time)
            if block_checkin is not None:
                block_checkin = normalize_string_to_bool(block_checkin)

            # Validar campos requeridos
            if not date_received or not date_received.strip():
                raise ValidationError("La fecha de recepción es requerida")

            if not is_valid_iso8601_date(date_received):
                raise ValidationError(
                    f"La fecha de recepción debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ). Valor recibido: {date_received}"
                )

            valid_priorities = ["trivial", "low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValidationError(
                    f"La prioridad debe ser una de: {', '.join(valid_priorities)}. Valor recibido: {priority}"
                )

            if not status or not status.strip():
                raise ValidationError("El estado es requerido")

            # Validar estado
            try:
                WorkOrderStatus(status)
            except ValueError:
                valid_statuses = [s.value for s in WorkOrderStatus]
                raise ValidationError(
                    f"Estado inválido. Estados válidos: {', '.join(valid_statuses)}"
                )

            if not summary or not summary.strip():
                raise ValidationError("El resumen es requerido")

            if estimated_cost < 0:
                raise ValidationError("El costo estimado no puede ser negativo")

            if estimated_time <= 0:
                raise ValidationError("El tiempo estimado debe ser mayor a 0")

            # Validar fecha programada si se proporciona
            if date_scheduled and not is_valid_iso8601_date(date_scheduled):
                raise ValidationError(
                    "La fecha programada debe estar en formato ISO 8601"
                )

            # Validar IDs opcionales
            if user_id is not None and user_id <= 0:
                raise ValidationError("El ID de usuario debe ser un entero positivo")
            if vendor_id is not None and vendor_id <= 0:
                raise ValidationError("El ID de proveedor debe ser un entero positivo")
            if unit_id is not None and unit_id <= 0:
                raise ValidationError("El ID de unidad debe ser un entero positivo")
            if reservation_id is not None and reservation_id <= 0:
                raise ValidationError("El ID de reserva debe ser un entero positivo")
            if actual_time is not None and actual_time <= 0:
                raise ValidationError("El tiempo real debe ser mayor a 0")

            # Crear parámetros usando los nombres correctos de la entidad
            params = CreateWorkOrderParams(
                date_received=date_received,
                priority=priority,
                status=WorkOrderStatus(status),
                summary=summary.strip(),
                estimated_cost=estimated_cost,
                estimated_time=estimated_time,
                date_scheduled=date_scheduled,
                user_id=user_id,
                vendor_id=vendor_id,
                unit_id=unit_id,
                reservation_id=reservation_id,
                reference_number=reference_number,
                description=description,
                work_performed=work_performed,
                source=source,
                source_name=source_name,
                source_phone=source_phone,
                actual_time=actual_time,
                block_checkin=block_checkin,
            )

            # Ejecutar caso de uso
            use_case = CreateWorkOrderUseCase(api_client)
            response = await use_case.execute(params)

            # Retornar respuesta
            return {
                "success": True,
                "work_order": response.work_order.to_dict(),
                "message": "Orden de trabajo creada exitosamente",
            }

        except ValidationError as e:
            return {
                "success": False,
                "error": "Datos inválidos",
                "message": str(e),
                "work_order": None,
            }
        except AuthenticationError as e:
            return {
                "success": False,
                "error": "No autorizado",
                "message": str(e),
                "work_order": None,
            }
        except AuthorizationError as e:
            return {
                "success": False,
                "error": "Prohibido",
                "message": str(e),
                "work_order": None,
            }
        except ApiError as e:
            return {
                "success": False,
                "error": "Error de API",
                "message": str(e),
                "work_order": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Error inesperado",
                "message": f"Error inesperado al crear work order: {str(e)}",
                "work_order": None,
            }
