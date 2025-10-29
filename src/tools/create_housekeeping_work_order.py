"""
Herramienta para crear órdenes de trabajo de housekeeping
"""

from typing import Any, Dict

from ..schemas.work_order import HousekeepingWorkOrderParams, WorkOrderResponse
from ..utils.exceptions import TrackHSAPIError
from .base import BaseTool


class CreateHousekeepingWorkOrderTool(BaseTool):
    """Herramienta para crear órdenes de trabajo de housekeeping"""

    @property
    def name(self) -> str:
        return "create_housekeeping_work_order"

    @property
    def description(self) -> str:
        return """
        Crear una orden de trabajo de housekeeping (limpieza) para una unidad.

        Permite crear órdenes de limpieza con:
        - Fecha programada
        - Tipo de limpieza (normal o inspección)
        - Comentarios especiales
        - Costo del servicio

        Args:
            unit_id: ID de la unidad que requiere limpieza
            scheduled_at: Fecha programada
            is_inspection: True si es inspección, False si es limpieza
            clean_type_id: ID del tipo de limpieza
            comments: Comentarios especiales
            cost: Costo del servicio

        Returns:
            Orden de trabajo creada con ID asignado
        """

    @property
    def input_schema(self) -> type:
        return HousekeepingWorkOrderParams

    @property
    def output_schema(self) -> type:
        return WorkOrderResponse

    def _execute_logic(
        self, validated_input: HousekeepingWorkOrderParams
    ) -> Dict[str, Any]:
        """
        Ejecuta la creación de orden de housekeeping

        Args:
            validated_input: Parámetros validados

        Returns:
            Orden de trabajo creada
        """
        # Preparar datos para la API
        work_order_data = self._prepare_work_order_data(validated_input)

        # Realizar llamada a la API
        try:
            result = self.api_client.post(
                "api/pms/work-orders/housekeeping", work_order_data
            )

            # Procesar resultado
            processed_result = self._process_api_response(result, "housekeeping")

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error creando orden de housekeeping",
                extra={
                    "unit_id": validated_input.unit_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise TrackHSAPIError(f"Error creando orden de housekeeping: {str(e)}")

    def _prepare_work_order_data(
        self, validated_input: HousekeepingWorkOrderParams
    ) -> Dict[str, Any]:
        """
        Prepara datos para la llamada a la API

        Args:
            validated_input: Parámetros validados

        Returns:
            Datos formateados para la API
        """
        data = {
            "unitId": validated_input.unit_id,
            "scheduledAt": validated_input.scheduled_at.strftime("%Y-%m-%d"),
            "isInspection": validated_input.is_inspection,
        }

        if validated_input.clean_type_id is not None:
            data["cleanTypeId"] = validated_input.clean_type_id

        if validated_input.comments is not None:
            data["comments"] = validated_input.comments

        if validated_input.cost is not None:
            data["cost"] = validated_input.cost

        return data

    def _process_api_response(
        self, api_result: Dict[str, Any], work_order_type: str
    ) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API

        Args:
            api_result: Respuesta de la API
            work_order_type: Tipo de orden de trabajo

        Returns:
            Orden de trabajo procesada
        """
        processed = {
            "id": api_result.get("id"),
            "type": work_order_type,
            "unit_id": api_result.get("unitId"),
            "status": api_result.get("status"),
            "summary": api_result.get("summary"),
            "description": api_result.get("description"),
            "priority": api_result.get("priority"),
            "estimated_cost": api_result.get("estimatedCost"),
            "estimated_time": api_result.get("estimatedTime"),
            "created_at": api_result.get("createdAt"),
            "scheduled_at": api_result.get("scheduledAt"),
            "is_inspection": api_result.get("isInspection"),
            "clean_type_id": api_result.get("cleanTypeId"),
            "comments": api_result.get("comments"),
            "cost": api_result.get("cost"),
            "links": api_result.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}
