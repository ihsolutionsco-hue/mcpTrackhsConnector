"""
Servicio de Work Orders para TrackHS.
Contiene la lógica de negocio para órdenes de trabajo.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from ..exceptions import TrackHSError, ValidationError
from ..repositories import WorkOrderRepository

logger = logging.getLogger(__name__)


class WorkOrderService:
    """
    Servicio para gestión de órdenes de trabajo.

    Separa la lógica de negocio de las herramientas MCP,
    permitiendo testing y reutilización.
    """

    # Clean types válidos obtenidos de la API
    VALID_CLEAN_TYPES = {3, 4, 5, 6, 7, 8, 9, 10}

    def __init__(self, work_order_repo: WorkOrderRepository):
        self.work_order_repo = work_order_repo

    def create_maintenance_work_order(
        self,
        unit_id: int,
        summary: str,
        description: str,
        priority: Literal[1, 3, 5] = 3,
        estimated_cost: Optional[float] = None,
        estimated_time: Optional[int] = None,
        date_received: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Crear una orden de trabajo de mantenimiento.

        Args:
            unit_id: ID de la unidad
            summary: Resumen del problema
            description: Descripción detallada
            priority: Prioridad (1=Baja, 3=Media, 5=Alta)
            estimated_cost: Costo estimado
            estimated_time: Tiempo estimado en minutos
            date_received: Fecha de recepción (YYYY-MM-DD)

        Returns:
            Diccionario con la orden creada

        Raises:
            ValidationError: Si los datos no son válidos
            TrackHSError: Si hay error en la API
        """
        # Validaciones de negocio
        if not summary.strip():
            raise ValidationError("El resumen no puede estar vacío")

        if not description.strip():
            raise ValidationError("La descripción no puede estar vacía")

        if estimated_cost is not None and estimated_cost < 0:
            raise ValidationError("El costo estimado no puede ser negativo")

        if estimated_time is not None and estimated_time < 0:
            raise ValidationError("El tiempo estimado no puede ser negativo")

        # Usar fecha actual si no se proporciona
        if date_received is None:
            date_received = datetime.now().strftime("%Y-%m-%d")

        logger.info(
            f"Creando orden de mantenimiento para unidad {unit_id}, prioridad: {priority}"
        )

        try:
            result = self.work_order_repo.create_maintenance_work_order(
                unit_id=unit_id,
                summary=summary,
                description=description,
                priority=priority,
                estimated_cost=estimated_cost,
                estimated_time=estimated_time,
                date_received=date_received,
            )

            logger.info(
                f"Orden de mantenimiento creada exitosamente. ID: {result.get('id', 'N/A')}"
            )
            return result

        except Exception as e:
            logger.error(f"Error creando orden de mantenimiento: {str(e)}")
            raise TrackHSError(f"Error creando orden de mantenimiento: {str(e)}")

    def create_housekeeping_work_order(
        self,
        unit_id: int,
        scheduled_at: str,
        is_inspection: bool = False,
        clean_type_id: Optional[int] = None,
        comments: Optional[str] = None,
        cost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Crear una orden de trabajo de housekeeping.

        Args:
            unit_id: ID de la unidad
            scheduled_at: Fecha programada (YYYY-MM-DD)
            is_inspection: True si es inspección, False si es limpieza
            clean_type_id: ID del tipo de limpieza (requerido si no es inspección)
            comments: Comentarios adicionales
            cost: Costo del servicio

        Returns:
            Diccionario con la orden creada

        Raises:
            ValidationError: Si los datos no son válidos
            TrackHSError: Si hay error en la API
        """
        # Validaciones de negocio
        if not is_inspection and clean_type_id is None:
            raise ValidationError("clean_type_id es requerido para órdenes de limpieza")

        if clean_type_id is not None and clean_type_id not in self.VALID_CLEAN_TYPES:
            valid_types_str = ", ".join(map(str, sorted(self.VALID_CLEAN_TYPES)))
            raise ValidationError(
                f"clean_type_id inválido: {clean_type_id}. Tipos válidos: {valid_types_str}"
            )

        if cost is not None and cost < 0:
            raise ValidationError("El costo no puede ser negativo")

        # Validar formato de fecha
        try:
            datetime.strptime(scheduled_at, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Formato de fecha inválido. Use YYYY-MM-DD")

        logger.info(
            f"Creando orden de housekeeping para unidad {unit_id}, fecha: {scheduled_at}, inspección: {is_inspection}"
        )

        try:
            result = self.work_order_repo.create_housekeeping_work_order(
                unit_id=unit_id,
                scheduled_at=scheduled_at,
                is_inspection=is_inspection,
                clean_type_id=clean_type_id,
                comments=comments,
                cost=cost,
            )

            logger.info(
                f"Orden de housekeeping creada exitosamente. ID: {result.get('id', 'N/A')}"
            )
            return result

        except Exception as e:
            logger.error(f"Error creando orden de housekeeping: {str(e)}")
            raise TrackHSError(f"Error creando orden de housekeeping: {str(e)}")

    def get_work_order_status(self, work_order_id: int) -> Dict[str, Any]:
        """
        Obtener el estado de una orden de trabajo.

        Args:
            work_order_id: ID de la orden

        Returns:
            Estado de la orden
        """
        # TODO: Implementar cuando la API lo soporte
        raise NotImplementedError("get_work_order_status no implementado aún")

    def update_work_order_status(
        self, work_order_id: int, status: str
    ) -> Dict[str, Any]:
        """
        Actualizar el estado de una orden de trabajo.

        Args:
            work_order_id: ID de la orden
            status: Nuevo estado

        Returns:
            Orden actualizada
        """
        # TODO: Implementar cuando la API lo soporte
        raise NotImplementedError("update_work_order_status no implementado aún")
