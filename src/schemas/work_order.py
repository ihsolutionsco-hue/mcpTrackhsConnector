"""
Schemas para órdenes de trabajo
"""

from datetime import date
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .base import BaseSchema


class MaintenanceWorkOrderParams(BaseModel):
    """Parámetros para crear orden de mantenimiento"""

    unitId: int = Field(gt=0, description="ID de la unidad que requiere mantenimiento")
    summary: str = Field(
        min_length=1, max_length=500, description="Resumen breve del problema"
    )
    description: str = Field(
        min_length=1, max_length=5000, description="Descripción detallada"
    )
    priority: int = Field(default=3, description="Prioridad: 1=Baja, 3=Media, 5=Alta")
    estimatedCost: Optional[float] = Field(
        default=None, ge=0, description="Costo estimado"
    )
    estimatedTime: Optional[int] = Field(
        default=None, ge=0, description="Tiempo estimado en minutos"
    )
    dateReceived: Optional[date] = Field(default=None, description="Fecha de recepción")


class HousekeepingWorkOrderParams(BaseModel):
    """Parámetros para crear orden de housekeeping"""

    unitId: int = Field(gt=0, description="ID de la unidad que requiere limpieza")
    scheduledAt: date = Field(description="Fecha programada")
    isInspection: bool = Field(
        default=False, description="True si es inspección, False si es limpieza"
    )
    cleanTypeId: Optional[int] = Field(
        default=None, gt=0, description="ID del tipo de limpieza"
    )
    comments: Optional[str] = Field(
        default=None, max_length=2000, description="Comentarios especiales"
    )
    cost: Optional[float] = Field(default=None, ge=0, description="Costo del servicio")


class WorkOrderResponse(BaseModel):
    """Respuesta de orden de trabajo creada"""

    id: int = Field(description="ID de la orden de trabajo")
    type: str = Field(description="Tipo de orden (maintenance/housekeeping)")
    unit_id: int = Field(description="ID de la unidad")
    status: str = Field(description="Estado de la orden")
    summary: Optional[str] = Field(default=None, description="Resumen")
    description: Optional[str] = Field(default=None, description="Descripción")
    priority: Optional[int] = Field(default=None, description="Prioridad")
    estimated_cost: Optional[float] = Field(default=None, description="Costo estimado")
    estimated_time: Optional[int] = Field(default=None, description="Tiempo estimado")
    created_at: str = Field(description="Fecha de creación")
    scheduled_at: Optional[str] = Field(default=None, description="Fecha programada")

    # Campos específicos de housekeeping
    is_inspection: Optional[bool] = Field(default=None, description="Es inspección")
    clean_type_id: Optional[int] = Field(
        default=None, description="ID del tipo de limpieza"
    )
    comments: Optional[str] = Field(default=None, description="Comentarios")
    cost: Optional[float] = Field(default=None, description="Costo del servicio")

    # Enlaces
    links: Optional[Dict[str, str]] = Field(
        default=None, description="Enlaces relacionados"
    )
