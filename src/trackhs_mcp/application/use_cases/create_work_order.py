"""
Caso de uso para crear órdenes de trabajo de mantenimiento.

Este módulo implementa la lógica de negocio para crear work orders
siguiendo los principios de Clean Architecture.
"""

from datetime import datetime
from typing import Any, Dict

from ...application.ports.api_client_port import ApiClientPort
from ...domain.entities.work_orders import (
    CreateWorkOrderParams,
    WorkOrder,
    WorkOrderResponse,
)
from ...domain.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    ServerError,
    ValidationError,
)


class CreateWorkOrderUseCase:
    """Caso de uso para crear órdenes de trabajo de mantenimiento."""

    def __init__(self, api_client: ApiClientPort):
        """Inicializar el caso de uso con el cliente API."""
        self.api_client = api_client

    async def execute(self, params: CreateWorkOrderParams) -> WorkOrderResponse:
        """
        Ejecutar la creación de una orden de trabajo.

        Args:
            params: Parámetros para crear la orden de trabajo

        Returns:
            WorkOrderResponse: Respuesta con la orden creada

        Raises:
            ValidationError: Si los parámetros son inválidos
            AuthenticationError: Si las credenciales son inválidas
            AuthorizationError: Si no hay permisos para crear work orders
            ApiError: Si hay error en la API
        """
        try:
            # Validar parámetros
            self._validate_params(params)

            # Construir payload para la API
            payload = self._build_payload(params)

            # Logging para debug
            import logging

            logger = logging.getLogger(__name__)
            logger.info(f"Payload being sent: {payload}")

            # Llamar a la API
            response_data = await self.api_client.post(
                "/api/pms/maintenance/work-orders", data=payload
            )

            # La API devuelve directamente el objeto del work order (201 Created)
            work_order = WorkOrder.from_api_response(response_data)
            return WorkOrderResponse(work_order=work_order)

        except ValidationError:
            raise
        except AuthenticationError:
            raise
        except AuthorizationError:
            raise
        except ApiError as e:
            if e.status_code == 401:
                raise AuthenticationError(
                    "No autorizado: Credenciales de autenticación inválidas o expiradas"
                )
            elif e.status_code == 403:
                raise AuthorizationError(
                    "Prohibido: Permisos insuficientes para crear work orders"
                )
            elif e.status_code == 422:
                # Capturar más detalles del error 422
                error_detail = f"Datos inválidos: {e.message}"
                if hasattr(e, "response_body"):
                    try:
                        import json

                        error_json = json.loads(e.response_body)
                        if "validation_messages" in error_json:
                            error_detail += (
                                f" | Validación: {error_json['validation_messages']}"
                            )
                        elif "detail" in error_json:
                            error_detail += f" | Detalle: {error_json['detail']}"
                    except:
                        error_detail += f" | Response: {e.response_body}"
                raise ValidationError(error_detail)
            elif e.status_code >= 500:
                raise ServerError(
                    "Error interno del servidor: La API está temporalmente no disponible"
                )
            else:
                raise ApiError(f"Error de API: {e.message}", e.status_code)
        except Exception as e:
            raise ApiError(f"Error inesperado al crear work order: {str(e)}")

    def _validate_params(self, params: CreateWorkOrderParams) -> None:
        """
        Validar parámetros de entrada.

        Args:
            params: Parámetros a validar

        Raises:
            ValidationError: Si los parámetros son inválidos
        """
        # Validar fecha de recepción
        if not self._is_valid_iso8601_date(params.date_received):
            raise ValidationError(
                "La fecha de recepción debe estar en formato ISO 8601"
            )

        # Validar fecha programada si se proporciona
        if params.date_scheduled and not self._is_valid_iso8601_date(
            params.date_scheduled
        ):
            raise ValidationError("La fecha programada debe estar en formato ISO 8601")

        # Validar prioridad
        valid_priorities = ["trivial", "low", "medium", "high", "critical"]
        if params.priority not in valid_priorities:
            raise ValidationError(
                f"La prioridad debe ser una de: {', '.join(valid_priorities)}"
            )

        # Validar costo estimado
        if params.estimated_cost < 0:
            raise ValidationError("El costo estimado no puede ser negativo")

        # Validar tiempo estimado
        if params.estimated_time <= 0:
            raise ValidationError("El tiempo estimado debe ser mayor a 0")

        # Validar IDs opcionales
        if params.user_id is not None and params.user_id <= 0:
            raise ValidationError("El ID de usuario debe ser un entero positivo")

        if params.vendor_id is not None and params.vendor_id <= 0:
            raise ValidationError("El ID de proveedor debe ser un entero positivo")

        # unitId es requerido por la API (aunque sea opcional en el parámetro)
        if params.unit_id is None or params.unit_id <= 0:
            raise ValidationError(
                "El ID de unidad es requerido por la API. Debe ser un entero positivo"
            )

        if params.reservation_id is not None and params.reservation_id <= 0:
            raise ValidationError("El ID de reserva debe ser un entero positivo")

        # Validar tiempo real si se proporciona
        if params.actual_time is not None and params.actual_time <= 0:
            raise ValidationError("El tiempo real debe ser mayor a 0")

    def _build_payload(self, params: CreateWorkOrderParams) -> Dict[str, Any]:
        """
        Construir payload para la API.

        Args:
            params: Parámetros de entrada

        Returns:
            Dict con el payload para la API
        """
        # Convertir fecha a formato ISO date (YYYY-MM-DD) si incluye timestamp
        date_received = params.date_received
        if "T" in date_received:
            date_received = date_received.split("T")[0]

        # Mapear prioridad textual a numérica para la API
        priority_mapping = {
            "trivial": 1,
            "low": 1,
            "medium": 3,
            "high": 5,
            "critical": 5,
        }
        numeric_priority = priority_mapping.get(params.priority, 3)  # Default a medium

        payload = {
            "dateReceived": date_received,
            "priority": numeric_priority,
            "summary": params.summary,
            "estimatedCost": float(params.estimated_cost),
            "estimatedTime": int(params.estimated_time),
            "unitId": params.unit_id
            or 1,  # Siempre incluir unitId, usar 1 como default
        }

        # Agregar campos opcionales si están presentes
        if params.date_scheduled is not None:
            date_scheduled = params.date_scheduled
            if "T" in date_scheduled:
                date_scheduled = date_scheduled.split("T")[0]
            payload["dateScheduled"] = date_scheduled

        if params.user_id is not None:
            payload["userId"] = params.user_id

        if params.vendor_id is not None:
            payload["vendorId"] = params.vendor_id

        # unitId ya está incluido en el payload base

        if params.reservation_id is not None:
            payload["reservationId"] = params.reservation_id

        if params.reference_number is not None:
            payload["referenceNumber"] = params.reference_number

        if params.description is not None:
            payload["description"] = params.description

        if params.work_performed is not None:
            payload["workPerformed"] = params.work_performed

        if params.source is not None:
            payload["source"] = params.source

        if params.source_name is not None:
            payload["sourceName"] = params.source_name

        if params.source_phone is not None:
            payload["sourcePhone"] = params.source_phone

        if params.actual_time is not None:
            payload["actualTime"] = float(params.actual_time)

        if params.block_checkin is not None:
            payload["blockCheckin"] = params.block_checkin

        # Agregar status como campo opcional si está presente
        if params.status is not None:
            payload["status"] = (
                str(params.status.value)
                if hasattr(params.status, "value")
                else str(params.status)
            )

        return payload

    def _is_valid_iso8601_date(self, date_str: str) -> bool:
        """
        Validar formato de fecha ISO 8601.

        Args:
            date_str: String de fecha a validar

        Returns:
            bool: True si es válida, False en caso contrario
        """
        try:
            # Intentar parsear la fecha
            datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return True
        except (ValueError, TypeError):
            return False
