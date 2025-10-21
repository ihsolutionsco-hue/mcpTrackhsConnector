"""
Herramienta MCP para crear órdenes de trabajo de housekeeping.

Esta herramienta permite crear work orders de housekeeping en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from typing import Any, Dict, Optional, Union

from pydantic import Field

from trackhs_mcp.application.ports.api_client_port import ApiClientPort
from trackhs_mcp.application.use_cases.create_housekeeping_work_order import (
    CreateHousekeepingWorkOrderUseCase,
)
from trackhs_mcp.domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrderResponse,
    HousekeepingWorkOrderStatus,
)
from trackhs_mcp.domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
)
from trackhs_mcp.infrastructure.utils.date_validation import is_valid_iso8601_date
from trackhs_mcp.infrastructure.utils.type_normalization import (
    normalize_optional_binary_int,
    normalize_optional_float,
    normalize_optional_int,
    normalize_string_to_bool,
    normalize_string_to_float,
    normalize_string_to_int,
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
        description="Crear una nueva orden de trabajo de housekeeping en TrackHS",
    )
    async def create_housekeeping_work_order(
        scheduled_at: str = Field(
            description="Scheduled date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ). Example: '2024-01-15T10:00:00Z'",
            pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$",
            min_length=10,
            max_length=20,
        ),
        status: str = Field(
            description="Work order status. Valid: pending, not-started, in-progress, completed, processed, cancelled, exception",
            min_length=1,
            max_length=50,
        ),
        unit_id: Optional[Union[int, float, str]] = Field(
            default=None,
            description="Unit ID (positive integer). Required if unit_block_id not provided. Example: 123",
            ge=1,
        ),
        unit_block_id: Optional[Union[int, float, str]] = Field(
            default=None,
            description="Unit block ID (positive integer). Required if unit_id not provided. Example: 456",
            ge=1,
        ),
        is_inspection: Optional[Union[int, float, str]] = Field(
            default=None,
            description="Is inspection flag (0=no, 1=yes). Required if clean_type_id not provided",
            ge=0,
            le=1,
        ),
        clean_type_id: Optional[Union[int, float, str]] = Field(
            default=None,
            description="Clean type ID (positive integer). Required if is_inspection not provided. Example: 5",
            ge=1,
        ),
        time_estimate: Optional[float] = Field(
            default=None,
            description="Estimated time in minutes (must be >= 0). Example: 60.0",
            ge=0.0,
        ),
        actual_time: Optional[float] = Field(
            default=None,
            description="Actual time spent in minutes (must be >= 0). Example: 75.5",
            ge=0.0,
        ),
        user_id: Optional[int] = Field(
            default=None,
            description="Assigned user ID (positive integer). Example: 789",
            ge=1,
        ),
        vendor_id: Optional[int] = Field(
            default=None, description="Vendor ID (positive integer). Example: 321", ge=1
        ),
        reservation_id: Optional[int] = Field(
            default=None,
            description="Related reservation ID (positive integer). Example: 987654",
            ge=1,
        ),
        is_turn: Optional[int] = Field(
            default=None, description="Is turn flag (0=no, 1=yes)", ge=0, le=1
        ),
        is_manual: Optional[int] = Field(
            default=None, description="Is manual flag (0=no, 1=yes)", ge=0, le=1
        ),
        charge_owner: Optional[int] = Field(
            default=None, description="Charge owner flag (0=no, 1=yes)", ge=0, le=1
        ),
        comments: Optional[str] = Field(
            default=None, description="Additional comments or notes", max_length=2000
        ),
        cost: Optional[float] = Field(
            default=None,
            description="Cost of the work order (must be >= 0). Example: 125.50",
            ge=0.0,
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
                    "scheduled_at debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)"
                )

            # Validar estado
            valid_statuses = [s.value for s in HousekeepingWorkOrderStatus]
            if status not in valid_statuses:
                raise ValidationError(
                    f"status debe ser uno de: {', '.join(valid_statuses)}"
                )

            # Validar campos de unidad (exactamente uno requerido)
            unit_id_norm = normalize_optional_int(unit_id, "unit_id")
            unit_block_id_norm = normalize_optional_int(unit_block_id, "unit_block_id")

            if not unit_id_norm and not unit_block_id_norm:
                raise ValidationError(
                    "Se requiere exactamente uno de unit_id o unit_block_id"
                )
            if unit_id_norm and unit_block_id_norm:
                raise ValidationError(
                    "No se pueden especificar ambos unit_id y unit_block_id"
                )

            # Validar campos de tipo de tarea (exactamente uno requerido)
            is_inspection_norm = normalize_optional_binary_int(
                is_inspection, "is_inspection"
            )
            clean_type_id_norm = normalize_optional_int(clean_type_id, "clean_type_id")

            if not is_inspection_norm and not clean_type_id_norm:
                raise ValidationError(
                    "Se requiere exactamente uno de is_inspection o clean_type_id"
                )
            if is_inspection_norm and clean_type_id_norm:
                raise ValidationError(
                    "No se pueden especificar ambos is_inspection y clean_type_id"
                )

            # Normalizar campos opcionales
            time_estimate_norm = normalize_optional_float(
                time_estimate, "time_estimate"
            )
            actual_time_norm = normalize_optional_float(actual_time, "actual_time")
            user_id_norm = normalize_optional_int(user_id, "user_id")
            vendor_id_norm = normalize_optional_int(vendor_id, "vendor_id")
            reservation_id_norm = normalize_optional_int(
                reservation_id, "reservation_id"
            )
            is_turn_norm = normalize_optional_binary_int(is_turn, "is_turn")
            is_manual_norm = normalize_optional_binary_int(is_manual, "is_manual")
            charge_owner_norm = normalize_optional_binary_int(
                charge_owner, "charge_owner"
            )
            cost_norm = normalize_optional_float(cost, "cost")

            # Validar valores numéricos
            if time_estimate_norm is not None and time_estimate_norm < 0:
                raise ValidationError("time_estimate debe ser >= 0")
            if actual_time_norm is not None and actual_time_norm < 0:
                raise ValidationError("actual_time debe ser >= 0")
            if cost_norm is not None and cost_norm < 0:
                raise ValidationError("cost debe ser >= 0")

            # Validar IDs positivos
            if user_id_norm is not None and user_id_norm <= 0:
                raise ValidationError("user_id debe ser un entero positivo")
            if vendor_id_norm is not None and vendor_id_norm <= 0:
                raise ValidationError("vendor_id debe ser un entero positivo")
            if reservation_id_norm is not None and reservation_id_norm <= 0:
                raise ValidationError("reservation_id debe ser un entero positivo")
            if clean_type_id_norm is not None and clean_type_id_norm <= 0:
                raise ValidationError("clean_type_id debe ser un entero positivo")

            # Crear parámetros del use case
            params = CreateHousekeepingWorkOrderParams(
                scheduled_at=scheduled_at,
                status=HousekeepingWorkOrderStatus(status),
                unit_id=unit_id_norm,
                unit_block_id=unit_block_id_norm,
                is_inspection=is_inspection_norm,
                clean_type_id=clean_type_id_norm,
                time_estimate=time_estimate_norm,
                actual_time=actual_time_norm,
                user_id=user_id_norm,
                vendor_id=vendor_id_norm,
                reservation_id=reservation_id_norm,
                is_turn=is_turn_norm,
                is_manual=is_manual_norm,
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
