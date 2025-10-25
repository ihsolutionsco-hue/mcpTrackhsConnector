"""
Herramienta MCP para crear órdenes de trabajo de housekeeping.

Esta herramienta permite crear work orders de housekeeping en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from typing import Any, Dict, Optional, Union

from pydantic import Field

from ...application.ports.api_client_port import ApiClientPort
from ...application.use_cases.create_housekeeping_work_order import (
    CreateHousekeepingWorkOrderUseCase,
)
from ...domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrderStatus,
)
from ...domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)
from ..utils.date_validation import (
    is_valid_iso8601_date,
    normalize_date_to_iso8601,
)


def register_create_housekeeping_work_order(mcp, api_client: ApiClientPort):
    """
    Registrar la herramienta MCP para crear housekeeping work orders.

    Args:
        mcp: Instancia del servidor MCP
        api_client: Cliente API para TrackHS
    """

    @mcp.tool(
        name="create_housekeeping_work_order",
        description="Crear una nueva orden de trabajo de housekeeping en TrackHS. 🔧 IMPORTANTE PARA LLM: Todos los IDs deben ser números enteros (int), no strings. Booleanos deben ser true/false, no 'true'/'false'. Fechas en formato ISO 8601.",
    )
    async def create_housekeeping_work_order(
        scheduled_at: str = Field(
            description="Scheduled date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DD HH:MM:SS). Example: '2024-01-15T10:00:00Z' or '2024-01-15 10:00:00'",
            pattern=r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}:\d{2}(Z)?)?$",
            min_length=10,
            max_length=20,
        ),
        status: str = Field(
            description="Work order status. Valid: pending, not-started, in-progress, completed, processed, cancelled, exception",
        ),
        unit_id: int = Field(
            description="Unit ID (positive integer). Required. Example: 123. ⚠️ NOTE: Unit 1 has restrictions for inspections (is_inspection=true) - use clean_type_id instead. 🔧 FOR LLM: Always pass as integer (123), never as string ('123').",
        ),
        unit_block_id: Optional[int] = Field(
            default=None,
            description="Unit block ID (positive integer). Optional. Example: 456. 🔧 FOR LLM: Pass as integer (456) or omit entirely, never as string ('456').",
        ),
        is_inspection: Optional[bool] = Field(
            default=None,
            description="Is inspection flag (true=yes, false=no). Required if clean_type_id not provided. ⚠️ RESTRICTION: Unit 1 does not support inspections - use clean_type_id instead. 🔧 FOR LLM: Pass as boolean (true/false), never as string ('true'/'false').",
        ),
        clean_type_id: Optional[int] = Field(
            default=None,
            description="Clean type ID (positive integer). Required if is_inspection not provided. ✅ RECOMMENDED for Unit 1 to avoid server errors. Available: 1=Carpet Cleaning, 2=Deep Clean, 3=Departure Clean, 4=Guest Request, 5=Pack and Play, 6=Pre-Arrival Inspection, 7=Refresh Clean. 🔧 FOR LLM: Pass as integer (5), never as string ('5').",
        ),
        user_id: Optional[int] = Field(
            default=None,
            description="Assigned user ID (positive integer). Example: 789. 🔧 FOR LLM: Pass as integer (789) or omit, never as string ('789').",
        ),
        vendor_id: Optional[int] = Field(
            default=None,
            description="Vendor ID (positive integer). Example: 321. 🔧 FOR LLM: Pass as integer (321) or omit, never as string ('321').",
        ),
        reservation_id: Optional[int] = Field(
            default=None,
            description="Related reservation ID (positive integer). Example: 987654. 🔧 FOR LLM: Pass as integer (987654) or omit, never as string ('987654').",
        ),
        is_turn: Optional[bool] = Field(
            default=None,
            description="Is turn flag (true=yes, false=no). 🔧 FOR LLM: Pass as boolean (true/false) or omit, never as string ('true'/'false').",
        ),
        charge_owner: Optional[bool] = Field(
            default=None,
            description="Charge owner flag (true=yes, false=no). 🔧 FOR LLM: Pass as boolean (true/false) or omit, never as string ('true'/'false').",
        ),
        comments: Optional[str] = Field(
            default=None, description="Additional comments or notes", max_length=2000
        ),
        cost: Optional[float] = Field(
            default=None,
            description="Cost of the work order (must be >= 0). Example: 125.50. 🔧 FOR LLM: Pass as float (125.50) or omit, never as string ('125.50').",
        ),
    ) -> Dict[str, Any]:
        """
        Create a new housekeeping work order in TrackHS.

        Creates housekeeping work orders with scheduling, assignments, and task types.
        Requires either unit_id or unit_block_id (exactly one), and either is_inspection
        or clean_type_id (exactly one). Validates all inputs and returns complete order data.
        """
        try:
            # Validar fecha programada
            if not is_valid_iso8601_date(scheduled_at):
                raise ValidationError(
                    "scheduled_at debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ o YYYY-MM-DD HH:MM:SS)"
                )

            # ⚠️ VALIDACIÓN ESPECÍFICA: Restricción conocida de la unidad 1
            if unit_id == 1 and is_inspection is True:
                raise ValidationError(
                    "❌ RESTRICCIÓN CONOCIDA: La unidad 1 no permite inspecciones (is_inspection=true). "
                    "Esto causa un error 500 del servidor TrackHS. "
                    "✅ SOLUCIÓN: Use clean_type_id en lugar de is_inspection para la unidad 1. "
                    "Clean types disponibles: 1=Carpet Cleaning, 2=Deep Clean, 3=Departure Clean, "
                    "4=Guest Request, 5=Pack and Play, 6=Pre-Arrival Inspection, 7=Refresh Clean"
                )

            # Normalizar fecha a formato ISO 8601 estándar
            scheduled_at_normalized = normalize_date_to_iso8601(scheduled_at)

            # Validar campos de tipo de tarea (exactamente uno requerido)
            if not is_inspection and not clean_type_id:
                raise ValidationError(
                    "Se requiere exactamente uno de is_inspection o clean_type_id"
                )
            if is_inspection and clean_type_id:
                raise ValidationError(
                    "No se pueden especificar ambos is_inspection y clean_type_id"
                )

            # Validar valores numéricos
            if cost is not None and cost < 0:
                raise ValidationError("cost debe ser >= 0")

            # Validar IDs positivos
            if unit_id <= 0:
                raise ValidationError(
                    "❌ unit_id debe ser un entero positivo. 🔧 PARA LLM: Use unit_id=123 (integer), no unit_id='123' (string)"
                )
            if unit_block_id is not None and unit_block_id <= 0:
                raise ValidationError(
                    "❌ unit_block_id debe ser un entero positivo. 🔧 PARA LLM: Use unit_block_id=456 (integer), no unit_block_id='456' (string)"
                )
            if user_id is not None and user_id <= 0:
                raise ValidationError(
                    "❌ user_id debe ser un entero positivo. 🔧 PARA LLM: Use user_id=789 (integer), no user_id='789' (string)"
                )
            if vendor_id is not None and vendor_id <= 0:
                raise ValidationError(
                    "❌ vendor_id debe ser un entero positivo. 🔧 PARA LLM: Use vendor_id=321 (integer), no vendor_id='321' (string)"
                )
            if reservation_id is not None and reservation_id <= 0:
                raise ValidationError(
                    "❌ reservation_id debe ser un entero positivo. 🔧 PARA LLM: Use reservation_id=987654 (integer), no reservation_id='987654' (string)"
                )
            if clean_type_id is not None and clean_type_id <= 0:
                raise ValidationError(
                    "❌ clean_type_id debe ser un entero positivo. 🔧 PARA LLM: Use clean_type_id=5 (integer), no clean_type_id='5' (string)"
                )

            # Crear parámetros del use case
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at=scheduled_at_normalized,
                status=status,
                unit_id=unit_id,
                unit_block_id=unit_block_id,
                is_inspection=is_inspection,
                clean_type_id=clean_type_id,
                user_id=user_id,
                vendor_id=vendor_id,
                reservation_id=reservation_id,
                is_turn=is_turn,
                charge_owner=charge_owner,
                comments=comments,
                cost=cost,
            )

            # Ejecutar use case
            use_case = CreateHousekeepingWorkOrderUseCase(api_client)
            response = await use_case.execute(params)

            if not response.success:
                raise ApiError(f"Error al crear orden de trabajo: {response.message}")

            return {
                "success": response.success,
                "data": response.data.dict() if response.data else None,
                "message": response.message,
            }

        except ValidationError:
            raise
        except ApiError:
            raise
        except AuthenticationError:
            raise
        except AuthorizationError:
            raise
        except Exception as e:
            raise ApiError(f"Error inesperado al crear orden de trabajo: {str(e)}")
