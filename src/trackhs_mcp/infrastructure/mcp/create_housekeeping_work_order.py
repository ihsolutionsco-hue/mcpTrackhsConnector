"""
Herramienta MCP para crear órdenes de trabajo de housekeeping.

Esta herramienta permite crear work orders de housekeeping en TrackHS siguiendo
el patrón de herramientas MCP existentes.
"""

from typing import Any, Dict, Optional, Union

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
        scheduled_at: str,
        status: str,
        unit_id: Optional[Union[int, str]] = None,
        unit_block_id: Optional[Union[int, str]] = None,
        is_inspection: Optional[Union[bool, str]] = None,
        clean_type_id: Optional[Union[int, str]] = None,
        time_estimate: Optional[Union[float, str]] = None,
        actual_time: Optional[Union[float, str]] = None,
        user_id: Optional[Union[int, str]] = None,
        vendor_id: Optional[Union[int, str]] = None,
        reservation_id: Optional[Union[int, str]] = None,
        is_turn: Optional[Union[bool, str]] = None,
        is_manual: Optional[Union[bool, str]] = None,
        charge_owner: Optional[Union[bool, str]] = None,
        comments: Optional[str] = None,
        cost: Optional[Union[float, str]] = None,
    ) -> Dict[str, Any]:
        """
        Crear una nueva orden de trabajo de housekeeping.

        Esta herramienta permite crear órdenes de trabajo de housekeeping en TrackHS
        con todos los campos requeridos y opcionales disponibles en la API.

        **Campos Requeridos:**
        - scheduled_at: Fecha programada en formato ISO 8601 (ej: "2024-01-15" o "2024-01-15T10:30:00Z")
        - status: Estado de la orden (pending, not-started, in-progress, completed, processed, cancelled, exception)
        - unit_id o unit_block_id: ID de la unidad o bloque de unidad (exactamente uno requerido)
        - is_inspection o clean_type_id: Tipo de tarea (exactamente uno requerido)

        **Campos Opcionales:**
        - time_estimate: Tiempo estimado en minutos (debe ser >= 0)
        - actual_time: Tiempo real en minutos (debe ser >= 0)
        - user_id: ID del usuario asignado
        - vendor_id: ID del proveedor
        - reservation_id: ID de la reserva relacionada
        - is_turn: Si es un turno (true/false)
        - is_manual: Si es manual (true/false)
        - charge_owner: Si se cobra al propietario (true/false)
        - comments: Comentarios adicionales
        - cost: Costo de la orden (debe ser >= 0)

        **Ejemplos de Uso:**

        # Crear inspección
        create_housekeeping_work_order(
            scheduled_at="2024-01-15",
            status="pending",
            unit_id=123,
            is_inspection=True
        )

        # Crear limpieza con tipo específico
        create_housekeeping_work_order(
            scheduled_at="2024-01-15T10:00:00Z",
            status="not-started",
            unit_id=123,
            clean_type_id=5,
            time_estimate=60,
            is_turn=True
        )

        # Crear orden completa
        create_housekeeping_work_order(
            scheduled_at="2024-01-15T14:30:00Z",
            status="pending",
            unit_id=456,
            is_inspection=False,
            clean_type_id=3,
            time_estimate=90,
            user_id=789,
            is_turn=True,
            comments="Limpieza profunda requerida"
        )

        **Estados Válidos:**
        - pending: Pendiente
        - not-started: No iniciada
        - in-progress: En progreso
        - completed: Completada
        - processed: Procesada
        - cancelled: Cancelada
        - exception: Excepción

        **Validaciones:**
        - scheduled_at debe estar en formato ISO 8601
        - status debe ser uno de los estados válidos
        - Exactamente uno de unit_id o unit_block_id debe estar presente
        - Exactamente uno de is_inspection o clean_type_id debe estar presente
        - time_estimate y actual_time deben ser >= 0
        - cost debe ser >= 0
        - Todos los IDs deben ser enteros positivos

        **Manejo de Errores:**
        - 400: Datos de entrada inválidos
        - 401: Credenciales inválidas o expiradas
        - 403: Permisos insuficientes
        - 404: Recurso no encontrado
        - 500: Error interno del servidor

        Returns:
            Dict con la respuesta de la API incluyendo la orden creada

        Raises:
            ValidationError: Si los datos de entrada son inválidos
            ApiError: Si ocurre un error en la API
            AuthenticationError: Si las credenciales son inválidas
            AuthorizationError: Si no hay permisos suficientes
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
            unit_id_norm = (
                normalize_string_to_int(unit_id) if unit_id is not None else None
            )
            unit_block_id_norm = (
                normalize_string_to_int(unit_block_id)
                if unit_block_id is not None
                else None
            )

            if not unit_id_norm and not unit_block_id_norm:
                raise ValidationError(
                    "Se requiere exactamente uno de unit_id o unit_block_id"
                )
            if unit_id_norm and unit_block_id_norm:
                raise ValidationError(
                    "No se pueden especificar ambos unit_id y unit_block_id"
                )

            # Validar campos de tipo de tarea (exactamente uno requerido)
            is_inspection_norm = (
                normalize_string_to_bool(is_inspection)
                if is_inspection is not None
                else None
            )
            clean_type_id_norm = (
                normalize_string_to_int(clean_type_id)
                if clean_type_id is not None
                else None
            )

            if not is_inspection_norm and not clean_type_id_norm:
                raise ValidationError(
                    "Se requiere exactamente uno de is_inspection o clean_type_id"
                )
            if is_inspection_norm and clean_type_id_norm:
                raise ValidationError(
                    "No se pueden especificar ambos is_inspection y clean_type_id"
                )

            # Normalizar campos opcionales
            time_estimate_norm = (
                normalize_string_to_float(time_estimate)
                if time_estimate is not None
                else None
            )
            actual_time_norm = (
                normalize_string_to_float(actual_time)
                if actual_time is not None
                else None
            )
            user_id_norm = (
                normalize_string_to_int(user_id) if user_id is not None else None
            )
            vendor_id_norm = (
                normalize_string_to_int(vendor_id) if vendor_id is not None else None
            )
            reservation_id_norm = (
                normalize_string_to_int(reservation_id)
                if reservation_id is not None
                else None
            )
            is_turn_norm = (
                normalize_string_to_bool(is_turn) if is_turn is not None else None
            )
            is_manual_norm = (
                normalize_string_to_bool(is_manual) if is_manual is not None else None
            )
            charge_owner_norm = (
                normalize_string_to_bool(charge_owner)
                if charge_owner is not None
                else None
            )
            cost_norm = normalize_string_to_float(cost) if cost is not None else None

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
