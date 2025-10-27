"""
Repository para órdenes de trabajo de TrackHS
Maneja todas las operaciones relacionadas con work orders
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..exceptions import APIError, NotFoundError, ValidationError
from .base import BaseRepository

logger = logging.getLogger(__name__)


class WorkOrderRepository(BaseRepository):
    """Repository para operaciones de órdenes de trabajo"""

    def __init__(self, api_client, cache_ttl: int = 300):
        super().__init__(api_client, cache_ttl)
        self.maintenance_endpoint = "api/pms/maintenance/work-orders"
        self.housekeeping_endpoint = "api/pms/housekeeping/work-orders"

    def get_by_id(self, work_order_id: int) -> Dict[str, Any]:
        """
        Obtener orden de trabajo por ID.

        Args:
            work_order_id: ID de la orden de trabajo

        Returns:
            Datos de la orden de trabajo

        Raises:
            NotFoundError: Si la orden no existe
            APIError: Si hay error de API
        """
        cache_key = f"work_order_{work_order_id}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Fetching work order {work_order_id} from API")
            # Intentar primero en mantenimiento, luego en housekeeping
            try:
                result = self.api_client.get(
                    f"{self.maintenance_endpoint}/{work_order_id}"
                )
            except NotFoundError:
                result = self.api_client.get(
                    f"{self.housekeeping_endpoint}/{work_order_id}"
                )

            # Guardar en cache
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"get_work_order_{work_order_id}")

    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buscar órdenes de trabajo con filtros.

        Args:
            filters: Filtros de búsqueda (page, size, status, priority, etc.)

        Returns:
            Resultados de búsqueda con metadatos de paginación
        """
        # Crear clave de cache basada en filtros
        cache_key = f"work_orders_search_{hash(frozenset(filters.items()))}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Searching work orders with filters: {filters}")
            # Buscar en ambos endpoints y combinar resultados
            maintenance_result = self.api_client.get(
                self.maintenance_endpoint, params=filters
            )
            housekeeping_result = self.api_client.get(
                self.housekeeping_endpoint, params=filters
            )

            # Combinar resultados (simplificado)
            combined_result = {
                "page": filters.get("page", 1),
                "page_size": filters.get("size", 10),
                "total_items": (
                    maintenance_result.get("total_items", 0)
                    + housekeeping_result.get("total_items", 0)
                ),
                "_embedded": {
                    "maintenance_work_orders": maintenance_result.get(
                        "_embedded", {}
                    ).get("work_orders", []),
                    "housekeeping_work_orders": housekeeping_result.get(
                        "_embedded", {}
                    ).get("work_orders", []),
                },
            }

            # Guardar en cache
            self._set_cached(cache_key, combined_result)

            return combined_result

        except Exception as e:
            self._handle_api_error(e, f"search_work_orders_{filters}")

    def create_maintenance_work_order(
        self,
        unit_id: int,
        summary: str,
        description: str,
        priority: int = 3,
        estimated_cost: Optional[float] = None,
        estimated_time: Optional[int] = None,
        date_received: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Crear orden de trabajo de mantenimiento.

        Args:
            unit_id: ID de la unidad
            summary: Resumen del problema
            description: Descripción detallada
            priority: Prioridad (1, 3, 5)
            estimated_cost: Costo estimado
            estimated_time: Tiempo estimado en minutos
            date_received: Fecha de recepción (YYYY-MM-DD)

        Returns:
            Datos de la orden creada

        Raises:
            ValidationError: Si los datos no son válidos
            APIError: Si hay error de API
        """
        # Validar datos
        self._validate_maintenance_work_order(
            unit_id, summary, description, priority, estimated_cost, estimated_time
        )

        work_order_data = {
            "unitId": unit_id,
            "summary": summary,
            "description": description,
            "priority": priority,
            "status": "pending",
            "dateReceived": date_received or datetime.now().strftime("%Y-%m-%d"),
        }

        if estimated_cost is not None:
            work_order_data["estimatedCost"] = estimated_cost
        if estimated_time is not None:
            work_order_data["estimatedTime"] = estimated_time

        try:
            logger.info(f"Creating maintenance work order for unit {unit_id}")
            result = self.api_client.post(self.maintenance_endpoint, work_order_data)

            # Limpiar cache relacionado
            self._clear_cache()

            return result

        except Exception as e:
            self._handle_api_error(e, f"create_maintenance_work_order_{unit_id}")

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
        Crear orden de trabajo de housekeeping.

        Args:
            unit_id: ID de la unidad
            scheduled_at: Fecha programada (YYYY-MM-DD)
            is_inspection: Si es inspección
            clean_type_id: ID del tipo de limpieza (requerido si no es inspección)
            comments: Comentarios adicionales
            cost: Costo del servicio

        Returns:
            Datos de la orden creada

        Raises:
            ValidationError: Si los datos no son válidos
            APIError: Si hay error de API
        """
        # Validar datos
        self._validate_housekeeping_work_order(
            unit_id, scheduled_at, is_inspection, clean_type_id
        )

        work_order_data = {
            "unitId": unit_id,
            "scheduledAt": scheduled_at,
            "status": "pending",
            "isInspection": is_inspection,
        }

        if clean_type_id is not None:
            work_order_data["cleanTypeId"] = clean_type_id
        if comments:
            work_order_data["comments"] = comments
        if cost is not None:
            work_order_data["cost"] = cost

        try:
            logger.info(f"Creating housekeeping work order for unit {unit_id}")
            result = self.api_client.post(self.housekeeping_endpoint, work_order_data)

            # Limpiar cache relacionado
            self._clear_cache()

            return result

        except Exception as e:
            self._handle_api_error(e, f"create_housekeeping_work_order_{unit_id}")

    def _validate_maintenance_work_order(
        self,
        unit_id: int,
        summary: str,
        description: str,
        priority: int,
        estimated_cost: Optional[float],
        estimated_time: Optional[int],
    ) -> None:
        """Validar datos de orden de mantenimiento"""
        if unit_id <= 0:
            raise ValidationError("unit_id debe ser mayor que 0")

        if not summary or len(summary.strip()) < 5:
            raise ValidationError("summary debe tener al menos 5 caracteres")

        if not description or len(description.strip()) < 10:
            raise ValidationError("description debe tener al menos 10 caracteres")

        if priority not in [1, 3, 5]:
            raise ValidationError("priority debe ser 1, 3 o 5")

        if estimated_cost is not None and estimated_cost < 0:
            raise ValidationError("estimated_cost no puede ser negativo")

        if estimated_time is not None and estimated_time < 0:
            raise ValidationError("estimated_time no puede ser negativo")

    def _validate_housekeeping_work_order(
        self,
        unit_id: int,
        scheduled_at: str,
        is_inspection: bool,
        clean_type_id: Optional[int],
    ) -> None:
        """Validar datos de orden de housekeeping"""
        if unit_id <= 0:
            raise ValidationError("unit_id debe ser mayor que 0")

        # Validar formato de fecha
        try:
            datetime.strptime(scheduled_at, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("scheduled_at debe tener formato YYYY-MM-DD")

        if not is_inspection and clean_type_id is None:
            raise ValidationError(
                "clean_type_id es requerido cuando is_inspection=False"
            )

        if clean_type_id is not None and clean_type_id <= 0:
            raise ValidationError("clean_type_id debe ser mayor que 0")

    def _test_connection(self) -> None:
        """Probar conexión con la API de work orders"""
        try:
            # Probar ambos endpoints
            self.api_client.get(self.maintenance_endpoint, {"page": 1, "size": 1})
            self.api_client.get(self.housekeeping_endpoint, {"page": 1, "size": 1})
        except Exception as e:
            raise APIError(f"Error conectando con API de work orders: {str(e)}")

    def get_work_order_summary(self, work_order_id: int) -> Dict[str, Any]:
        """
        Obtener resumen de una orden de trabajo.

        Args:
            work_order_id: ID de la orden de trabajo

        Returns:
            Resumen de la orden de trabajo
        """
        work_order = self.get_by_id(work_order_id)

        # Extraer solo datos básicos para el resumen
        summary = {
            "id": work_order.get("id"),
            "type": work_order.get("type", "unknown"),
            "status": work_order.get("status"),
            "priority": work_order.get("priority"),
            "summary": work_order.get("summary"),
            "unit_id": work_order.get("unitId"),
            "created_at": work_order.get("dateReceived")
            or work_order.get("scheduledAt"),
            "estimated_cost": work_order.get("estimatedCost"),
            "estimated_time": work_order.get("estimatedTime"),
        }

        return summary
