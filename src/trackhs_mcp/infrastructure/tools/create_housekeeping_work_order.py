"""
Herramienta MCP para crear órdenes de trabajo de housekeeping.

Esta herramienta permite crear work orders de housekeeping en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from typing import Annotated, Any, Dict, Optional, Union

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
from ..utils.type_normalization import (
    normalize_bool,
    normalize_float,
    normalize_int,
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
        description="Crear una nueva orden de trabajo de housekeeping en TrackHS. 🔧 IMPORTANTE PARA LLM: FastMCP convierte automáticamente strings a integers/booleans/floats. Puedes usar tanto integers (123) como strings ('123'), tanto booleans (true) como strings ('true'). Fechas en formato ISO 8601.",
    )
    async def create_housekeeping_work_order(
        scheduled_at: Annotated[
            str,
            Field(
                description="Scheduled date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DD HH:MM:SS). Example: '2024-01-15T10:00:00Z' or '2024-01-15 10:00:00'",
                pattern=r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}:\d{2}(Z)?)?$",
                min_length=10,
                max_length=20,
            ),
        ],
        status: Annotated[
            str,
            Field(
                description="Work order status. Valid: pending, not-started, in-progress, completed, processed, cancelled, exception",
            ),
        ],
        unit_id: Annotated[
            Union[int, str],
            Field(
                description="Unit ID (positive integer). Required. Example: 123. ⚠️ NOTE: Unit 1 has restrictions for inspections (is_inspection=true) - use clean_type_id instead. 🔧 FOR LLM: Accepts both integer (123) and string ('123') - FastMCP converts automatically.",
            ),
        ],
        unit_block_id: Annotated[
            Optional[Union[int, str]],
            Field(
                default=None,
                description="Unit block ID (positive integer). Optional. Example: 456. 🔧 FOR LLM: Accepts both integer (456) and string ('456') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        is_inspection: Annotated[
            Optional[Union[bool, str]],
            Field(
                default=None,
                description="Is inspection flag (true=yes, false=no). Required if clean_type_id not provided. ⚠️ RESTRICTION: Unit 1 does not support inspections - use clean_type_id instead. 🔧 FOR LLM: Accepts both boolean (true/false) and string ('true'/'false') - FastMCP converts automatically.",
            ),
        ],
        clean_type_id: Annotated[
            Optional[Union[int, str]],
            Field(
                default=None,
                description="Clean type ID (positive integer). Required if is_inspection not provided. ✅ RECOMMENDED for Unit 1 to avoid server errors. Available: 1=Carpet Cleaning, 2=Deep Clean, 3=Departure Clean, 4=Guest Request, 5=Pack and Play, 6=Pre-Arrival Inspection, 7=Refresh Clean. 🔧 FOR LLM: Accepts both integer (5) and string ('5') - FastMCP converts automatically.",
            ),
        ],
        user_id: Annotated[
            Optional[Union[int, str]],
            Field(
                default=None,
                description="Assigned user ID (positive integer). Example: 789. 🔧 FOR LLM: Accepts both integer (789) and string ('789') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        vendor_id: Annotated[
            Optional[Union[int, str]],
            Field(
                default=None,
                description="Vendor ID (positive integer). Example: 321. 🔧 FOR LLM: Accepts both integer (321) and string ('321') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        reservation_id: Annotated[
            Optional[Union[int, str]],
            Field(
                default=None,
                description="Related reservation ID (positive integer). Example: 987654. 🔧 FOR LLM: Accepts both integer (987654) and string ('987654') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        is_turn: Annotated[
            Optional[Union[bool, str]],
            Field(
                default=None,
                description="Is turn flag (true=yes, false=no). 🔧 FOR LLM: Accepts both boolean (true/false) and string ('true'/'false') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        charge_owner: Annotated[
            Optional[Union[bool, str]],
            Field(
                default=None,
                description="Charge owner flag (true=yes, false=no). 🔧 FOR LLM: Accepts both boolean (true/false) and string ('true'/'false') or omit entirely - FastMCP converts automatically.",
            ),
        ],
        comments: Annotated[
            Optional[str],
            Field(
                default=None,
                description="Additional comments or notes",
                max_length=2000,
            ),
        ],
        cost: Annotated[
            Optional[Union[float, str]],
            Field(
                default=None,
                description="Cost of the work order (must be >= 0). Example: 125.50. 🔧 FOR LLM: Accepts both float (125.50) and string ('125.50') or omit entirely - FastMCP converts automatically.",
            ),
        ],
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

            # Normalizar tipos Union a tipos nativos
            unit_id_norm = normalize_int(unit_id, "unit_id")
            unit_block_id_norm = (
                normalize_int(unit_block_id, "unit_block_id")
                if unit_block_id is not None
                else None
            )
            is_inspection_norm = (
                normalize_bool(is_inspection, "is_inspection")
                if is_inspection is not None
                else None
            )
            clean_type_id_norm = (
                normalize_int(clean_type_id, "clean_type_id")
                if clean_type_id is not None
                else None
            )
            user_id_norm = (
                normalize_int(user_id, "user_id") if user_id is not None else None
            )
            vendor_id_norm = (
                normalize_int(vendor_id, "vendor_id") if vendor_id is not None else None
            )
            reservation_id_norm = (
                normalize_int(reservation_id, "reservation_id")
                if reservation_id is not None
                else None
            )
            is_turn_norm = (
                normalize_bool(is_turn, "is_turn") if is_turn is not None else None
            )
            charge_owner_norm = (
                normalize_bool(charge_owner, "charge_owner")
                if charge_owner is not None
                else None
            )
            cost_norm = normalize_float(cost, "cost") if cost is not None else None

            # ⚠️ VALIDACIÓN ESPECÍFICA: Restricción conocida de la unidad 1
            if unit_id_norm == 1 and is_inspection_norm is True:
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
            if not is_inspection_norm and not clean_type_id_norm:
                raise ValidationError(
                    "Se requiere exactamente uno de is_inspection o clean_type_id"
                )
            if is_inspection_norm and clean_type_id_norm:
                raise ValidationError(
                    "No se pueden especificar ambos is_inspection y clean_type_id"
                )

            # Validar valores numéricos
            if cost_norm is not None and cost_norm < 0:
                raise ValidationError("cost debe ser >= 0")

            # Validar IDs positivos
            if unit_id_norm <= 0:
                raise ValidationError(
                    "❌ unit_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 123 or '123'"
                )
            if unit_block_id_norm is not None and unit_block_id_norm <= 0:
                raise ValidationError(
                    "❌ unit_block_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 456 or '456'"
                )
            if user_id_norm is not None and user_id_norm <= 0:
                raise ValidationError(
                    "❌ user_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 789 or '789'"
                )
            if vendor_id_norm is not None and vendor_id_norm <= 0:
                raise ValidationError(
                    "❌ vendor_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 321 or '321'"
                )
            if reservation_id_norm is not None and reservation_id_norm <= 0:
                raise ValidationError(
                    "❌ reservation_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 987654 or '987654'"
                )
            if clean_type_id_norm is not None and clean_type_id_norm <= 0:
                raise ValidationError(
                    "❌ clean_type_id debe ser un entero positivo. 🔧 PARA LLM: FastMCP converts strings to integers automatically - use either 5 or '5'"
                )

            # Crear parámetros del use case
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at=scheduled_at_normalized,
                status=status,
                unit_id=unit_id_norm,
                unit_block_id=unit_block_id_norm,
                is_inspection=is_inspection_norm,
                clean_type_id=clean_type_id_norm,
                user_id=user_id_norm,
                vendor_id=vendor_id_norm,
                reservation_id=reservation_id_norm,
                is_turn=is_turn_norm,
                charge_owner=charge_owner_norm,
                comments=comments,
                cost=cost_norm,
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
