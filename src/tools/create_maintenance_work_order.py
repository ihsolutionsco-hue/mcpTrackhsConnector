"""
Herramienta para crear órdenes de trabajo de mantenimiento
"""

from typing import Any, Dict

from ..schemas.work_order import MaintenanceWorkOrderParams, WorkOrderResponse
from ..utils.exceptions import TrackHSAPIError
from .base import BaseTool


class CreateMaintenanceWorkOrderTool(BaseTool):
    """Herramienta para crear órdenes de trabajo de mantenimiento"""

    @property
    def name(self) -> str:
        return "create_maintenance_work_order"

    @property
    def description(self) -> str:
        return """
        Crear una orden de trabajo de mantenimiento para una unidad.

        Permite crear órdenes de mantenimiento con:
        - Descripción detallada del problema
        - Prioridad (Baja, Media, Alta)
        - Costo y tiempo estimados
        - Fecha de recepción

        Args:
            unit_id: ID de la unidad que requiere mantenimiento
            summary: Resumen breve del problema
            description: Descripción detallada
            priority: Prioridad (1=Baja, 3=Media, 5=Alta)
            estimated_cost: Costo estimado
            estimated_time: Tiempo estimado en minutos
            date_received: Fecha de recepción

        Returns:
            Orden de trabajo creada con ID asignado
        """

    @property
    def input_schema(self) -> type:
        return MaintenanceWorkOrderParams

    @property
    def output_schema(self) -> type:
        return WorkOrderResponse

    def _execute_logic(
        self, validated_input: MaintenanceWorkOrderParams
    ) -> Dict[str, Any]:
        """
        Ejecuta la creación de orden de mantenimiento

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
                "api/pms/work-orders/maintenance", work_order_data
            )

            # Procesar resultado
            processed_result = self._process_api_response(result, "maintenance")

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error creando orden de mantenimiento",
                extra={
                    "unit_id": validated_input.unit_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise TrackHSAPIError(f"Error creando orden de mantenimiento: {str(e)}")

    def _prepare_work_order_data(
        self, validated_input: MaintenanceWorkOrderParams
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
            "summary": validated_input.summary,
            "description": validated_input.description,
            "priority": validated_input.priority,
        }

        if validated_input.estimated_cost is not None:
            data["estimatedCost"] = validated_input.estimated_cost

        if validated_input.estimated_time is not None:
            data["estimatedTime"] = validated_input.estimated_time

        if validated_input.date_received is not None:
            data["dateReceived"] = validated_input.date_received.strftime("%Y-%m-%d")

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
            "links": api_result.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}
