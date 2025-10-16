"""
Herramienta MCP para crear órdenes de trabajo de mantenimiento.

Esta herramienta permite crear work orders en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from trackhs_mcp.application.ports.api_client_port import ApiClientPort
from trackhs_mcp.application.use_cases.create_work_order import CreateWorkOrderUseCase
from trackhs_mcp.domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrderResponse,
    WorkOrderStatus,
)
from trackhs_mcp.domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)
from trackhs_mcp.infrastructure.utils.date_validation import is_valid_iso8601_date

# from trackhs_mcp.infrastructure.utils.error_handling import error_handler
from trackhs_mcp.infrastructure.utils.type_normalization import (
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
        description="Crear una nueva orden de trabajo de mantenimiento en TrackHS",
    )
    def create_maintenance_work_order(
        date_received: str,
        priority: Union[int, str],
        status: str,
        summary: str,
        estimated_cost: Union[float, str],
        estimated_time: Union[int, str],
        date_scheduled: Optional[str] = None,
        user_id: Optional[Union[int, str]] = None,
        vendor_id: Optional[Union[int, str]] = None,
        unit_id: Optional[Union[int, str]] = None,
        reservation_id: Optional[Union[int, str]] = None,
        reference_number: Optional[str] = None,
        description: Optional[str] = None,
        work_performed: Optional[str] = None,
        source: Optional[str] = None,
        source_name: Optional[str] = None,
        source_phone: Optional[str] = None,
        actual_time: Optional[Union[int, str]] = None,
        block_checkin: Optional[Union[bool, str]] = None,
    ) -> Dict[str, Any]:
        """
        Crear una nueva orden de trabajo de mantenimiento.

        Esta herramienta permite crear órdenes de trabajo de mantenimiento en TrackHS
        con todos los campos requeridos y opcionales disponibles en la API.

        **Campos Requeridos:**
        - date_received: Fecha de recepción en formato ISO 8601 (ej: "2024-01-15" o "2024-01-15T10:30:00Z")
        - priority: Prioridad de la orden (1=Baja, 3=Media, 5=Alta)
        - status: Estado de la orden (open, not-started, in-progress, completed, processed, vendor-*, cancelled)
        - summary: Resumen de la orden de trabajo
        - estimated_cost: Costo estimado (debe ser >= 0)
        - estimated_time: Tiempo estimado en minutos (debe ser > 0)

        **Campos Opcionales:**
        - date_scheduled: Fecha programada en formato ISO 8601
        - user_id: ID del usuario responsable
        - vendor_id: ID del proveedor asignado
        - unit_id: ID de la unidad relacionada
        - reservation_id: ID de la reserva relacionada
        - reference_number: Número de referencia
        - description: Descripción detallada
        - work_performed: Trabajo realizado
        - source: Fuente de la orden
        - source_name: Nombre de la fuente
        - source_phone: Teléfono de la fuente
        - actual_time: Tiempo real en minutos
        - block_checkin: Si debe bloquear el check-in (true/false)

        **Ejemplos de Uso:**

        # Creación básica
        create_maintenance_work_order(
            date_received="2024-01-15",
            priority=5,
            status="open",
            summary="Reparar aire acondicionado",
            estimated_cost=150.00,
            estimated_time=120
        )

        # Creación completa
        create_maintenance_work_order(
            date_received="2024-01-15T10:30:00Z",
            priority=3,
            status="in-progress",
            summary="Mantenimiento preventivo",
            estimated_cost=200.50,
            estimated_time=180,
            date_scheduled="2024-01-16T09:00:00Z",
            unit_id=123,
            vendor_id=456,
            description="Mantenimiento programado del sistema HVAC",
            source="Guest Request",
            source_name="Juan Pérez",
            source_phone="+1234567890",
            block_checkin=True
        )

        **Estados Válidos:**
        - open: Abierta
        - not-started: No iniciada
        - in-progress: En progreso
        - completed: Completada
        - processed: Procesada
        - vendor-assigned: Asignada a proveedor
        - vendor-accepted: Aceptada por proveedor
        - vendor-rejected: Rechazada por proveedor
        - vendor-completed: Completada por proveedor
        - cancelled: Cancelada

        **Prioridades:**
        - 1: Baja prioridad
        - 3: Media prioridad
        - 5: Alta prioridad

        Returns:
            Dict con la orden de trabajo creada incluyendo ID, fechas, y metadatos
        """
        try:
            # Normalizar tipos de entrada
            priority = normalize_string_to_int(priority)
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
                    "La fecha de recepción debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)"
                )

            if priority not in [1, 3, 5]:
                raise ValidationError(
                    "La prioridad debe ser 1 (Baja), 3 (Media) o 5 (Alta)"
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

            # Crear parámetros
            params = CreateWorkOrderParams(
                dateReceived=date_received,
                priority=priority,
                status=WorkOrderStatus(status),
                summary=summary.strip(),
                estimatedCost=estimated_cost,
                estimatedTime=estimated_time,
                dateScheduled=date_scheduled,
                userId=user_id,
                vendorId=vendor_id,
                unitId=unit_id,
                reservationId=reservation_id,
                referenceNumber=reference_number,
                description=description,
                workPerformed=work_performed,
                source=source,
                sourceName=source_name,
                sourcePhone=source_phone,
                actualTime=actual_time,
                blockCheckin=block_checkin,
            )

            # Ejecutar caso de uso
            use_case = CreateWorkOrderUseCase(api_client)
            response = use_case.execute(params)

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
