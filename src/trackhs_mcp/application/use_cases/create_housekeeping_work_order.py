"""
Use case para crear órdenes de trabajo de housekeeping.

Este módulo implementa la lógica de negocio para crear órdenes de trabajo
de housekeeping en TrackHS.
"""

from typing import TYPE_CHECKING, Any, Dict

from ...domain.entities.housekeeping_work_orders import (
    CreateHousekeepingWorkOrderParams,
    HousekeepingWorkOrder,
    HousekeepingWorkOrderResponse,
)

if TYPE_CHECKING:
    from ...infrastructure.adapters.trackhs_api_client import TrackHSApiClient


class CreateHousekeepingWorkOrderUseCase:
    """Use case para crear órdenes de trabajo de housekeeping."""

    def __init__(self, api_client: "TrackHSApiClient"):
        """
        Inicializa el use case.

        Args:
            api_client: Cliente API de TrackHS
        """
        self.api_client = api_client

    async def execute(
        self, params: CreateHousekeepingWorkOrderParams
    ) -> HousekeepingWorkOrderResponse:
        """
        Ejecuta la creación de una orden de trabajo de housekeeping.

        Args:
            params: Parámetros para crear la orden

        Returns:
            Respuesta con la orden creada o errores

        Raises:
            Exception: Si ocurre un error durante la creación
        """
        try:
            # Convertir parámetros a diccionario para la API
            request_data = self._prepare_request_data(params)

            # Llamar al API client
            response_data = await self.api_client.create_housekeeping_work_order(
                request_data
            )

            # Transformar respuesta a modelo de dominio
            work_order = self._transform_response(response_data)

            return HousekeepingWorkOrderResponse.success_response(work_order)

        except Exception as e:
            return HousekeepingWorkOrderResponse.error_response(
                f"Error al crear orden de trabajo de housekeeping: {str(e)}"
            )

    def _prepare_request_data(
        self, params: CreateHousekeepingWorkOrderParams
    ) -> Dict[str, Any]:
        """
        Prepara los datos de la petición para la API.

        Args:
            params: Parámetros del use case

        Returns:
            Diccionario con los datos para la API
        """
        import logging

        logger = logging.getLogger(__name__)

        # Log de debug para ver qué está recibiendo
        logger.error(f"DEBUG: Parámetros recibidos: {params.model_dump()}")
        logger.error(
            f"DEBUG: unit_id tipo: {type(params.unit_id)}, valor: {params.unit_id}"
        )
        logger.error(
            f"DEBUG: reservation_id tipo: {type(params.reservation_id)}, valor: {params.reservation_id}"
        )

        request_data = {
            "scheduledAt": params.scheduled_at,
        }

        # Agregar campos de unidad (exactamente uno)
        if params.unit_id:
            request_data["unitId"] = params.unit_id
        elif params.unit_block_id:
            request_data["unitBlockId"] = params.unit_block_id

        # Agregar campos de tipo de tarea (exactamente uno)
        if params.is_inspection is not None:
            request_data["isInspection"] = params.is_inspection
        elif params.clean_type_id:
            request_data["cleanTypeId"] = int(params.clean_type_id)

        # Agregar campos opcionales
        if params.user_id is not None:
            request_data["userId"] = params.user_id
        if params.vendor_id is not None:
            request_data["vendorId"] = params.vendor_id
        if params.reservation_id is not None:
            request_data["reservationId"] = int(params.reservation_id)
        if params.is_turn is not None:
            request_data["isTurn"] = params.is_turn
        if params.charge_owner is not None:
            request_data["chargeOwner"] = params.charge_owner
        if params.comments:
            request_data["comments"] = params.comments
        if params.cost is not None:
            request_data["cost"] = params.cost

        # Log de debug para ver qué se está enviando a la API
        logger.error(f"DEBUG: Request data final: {request_data}")
        logger.error(
            f"DEBUG: unitId tipo: {type(request_data.get('unitId'))}, valor: {request_data.get('unitId')}"
        )
        logger.error(
            f"DEBUG: reservationId tipo: {type(request_data.get('reservationId'))}, valor: {request_data.get('reservationId')}"
        )

        return request_data

    def _transform_response(
        self, response_data: Dict[str, Any]
    ) -> HousekeepingWorkOrder:
        """
        Transforma la respuesta de la API a modelo de dominio.

        Args:
            response_data: Datos de respuesta de la API

        Returns:
            Modelo de orden de trabajo de housekeeping
        """
        # Validar que response_data no sea None
        if response_data is None:
            raise ValueError("Response data cannot be None")

        # Manejar caso donde response_data es un string JSON
        if isinstance(response_data, str):
            # Limpiar espacios y validar que no esté vacío
            response_data = response_data.strip()
            if not response_data:
                raise ValueError("Response data cannot be empty string")

            try:
                import json

                response_data = json.loads(response_data)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Expected dict for API response, got string that cannot be parsed as JSON: {e}"
                )

        # Validar que response_data sea un diccionario
        if not isinstance(response_data, dict):
            raise ValueError(
                f"Expected dict for API response, got {type(response_data).__name__}: {response_data}"
            )
        return HousekeepingWorkOrder(
            id=response_data.get("id"),
            scheduled_at=response_data.get("scheduledAt"),
            status=response_data.get("status"),
            unit_id=response_data.get("unitId"),
            unit_block_id=response_data.get("unitBlockId"),
            is_inspection=response_data.get("isInspection"),
            clean_type_id=response_data.get("cleanTypeId"),
            time_estimate=response_data.get("timeEstimate"),
            actual_time=response_data.get("actualTime"),
            user_id=response_data.get("userId"),
            vendor_id=response_data.get("vendorId"),
            reservation_id=response_data.get("reservationId"),
            is_turn=response_data.get("isTurn"),
            is_manual=response_data.get("isManual"),
            charge_owner=response_data.get("chargeOwner"),
            comments=response_data.get("comments"),
            cost=response_data.get("cost"),
            created_at=response_data.get("createdAt"),
            updated_at=response_data.get("updatedAt"),
        )
