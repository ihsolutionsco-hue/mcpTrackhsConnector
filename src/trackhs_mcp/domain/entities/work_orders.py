"""
Entidades de dominio para Work Orders de TrackHS.

Este módulo define las entidades y value objects relacionados con órdenes de trabajo
de mantenimiento en el sistema TrackHS.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkOrderStatus(str, Enum):
    """Estados válidos para una orden de trabajo."""

    OPEN = "open"
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    PROCESSED = "processed"
    VENDOR_NOT_START = "vendor-not-start"
    VENDOR_ASSIGNED = "vendor-assigned"
    VENDOR_DECLINED = "vendor-declined"
    VENDOR_COMPLETED = "vendor-completed"
    USER_COMPLETED = "user-completed"
    CANCELLED = "cancelled"


class WorkOrderPriority(int, Enum):
    """Prioridades válidas para una orden de trabajo."""

    LOW = 1
    MEDIUM = 3
    HIGH = 5


class WorkOrderProblem(BaseModel):
    """Modelo para problemas/categorías de work orders."""

    id: int
    name: str
    description: Optional[str] = None


class CreateWorkOrderParams(BaseModel):
    """Parámetros para crear una nueva orden de trabajo."""

    # Campos requeridos
    date_received: str = Field(
        ..., alias="dateReceived", description="Fecha de recepción en formato ISO 8601"
    )
    priority: int = Field(..., description="Prioridad: 5 (Alta), 3 (Media), 1 (Baja)")
    status: WorkOrderStatus = Field(..., description="Estado de la orden de trabajo")
    summary: str = Field(
        ..., min_length=1, description="Resumen de la orden de trabajo"
    )
    estimated_cost: float = Field(
        ..., alias="estimatedCost", ge=0, description="Costo estimado"
    )
    estimated_time: int = Field(
        ..., alias="estimatedTime", gt=0, description="Tiempo estimado en minutos"
    )

    # Campos opcionales
    date_scheduled: Optional[str] = Field(
        None, alias="dateScheduled", description="Fecha programada en formato ISO 8601"
    )
    user_id: Optional[int] = Field(
        None, alias="userId", gt=0, description="ID del usuario"
    )
    vendor_id: Optional[int] = Field(
        None, alias="vendorId", gt=0, description="ID del proveedor"
    )
    unit_id: Optional[int] = Field(
        None, alias="unitId", gt=0, description="ID de la unidad"
    )
    reservation_id: Optional[int] = Field(
        None, alias="reservationId", gt=0, description="ID de la reserva"
    )
    reference_number: Optional[str] = Field(
        None, alias="referenceNumber", description="Número de referencia"
    )
    description: Optional[str] = Field(None, description="Descripción detallada")
    work_performed: Optional[str] = Field(
        None, alias="workPerformed", description="Trabajo realizado"
    )
    source: Optional[str] = Field(None, description="Fuente de la orden")
    source_name: Optional[str] = Field(
        None, alias="sourceName", description="Nombre de la fuente"
    )
    source_phone: Optional[str] = Field(
        None, alias="sourcePhone", description="Teléfono de la fuente"
    )
    actual_time: Optional[int] = Field(
        None, alias="actualTime", gt=0, description="Tiempo real en minutos"
    )
    block_checkin: Optional[bool] = Field(
        None, alias="blockCheckin", description="Bloquear check-in"
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        """Validar que la prioridad sea válida."""
        if v not in [1, 3, 5]:
            raise ValueError("La prioridad debe ser 1 (Baja), 3 (Media) o 5 (Alta)")
        return v

    @field_validator("date_received", "date_scheduled")
    @classmethod
    def validate_date_format(cls, v):
        """Validar formato de fecha ISO 8601."""
        if v is not None:
            try:
                datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(
                    "La fecha debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)"
                )
        return v

    @field_validator("estimated_cost")
    @classmethod
    def validate_estimated_cost(cls, v):
        """Validar que el costo estimado sea no negativo."""
        if v < 0:
            raise ValueError("El costo estimado no puede ser negativo")
        return v

    @field_validator("estimated_time")
    @classmethod
    def validate_estimated_time(cls, v):
        """Validar que el tiempo estimado sea positivo."""
        if v <= 0:
            raise ValueError("El tiempo estimado debe ser mayor a 0")
        return v


class WorkOrder(BaseModel):
    """Modelo principal para una orden de trabajo."""

    # Campos básicos
    id: int
    date_received: str = Field(alias="dateReceived")
    priority: int
    status: WorkOrderStatus
    summary: str
    estimated_cost: float = Field(alias="estimatedCost")
    estimated_time: int = Field(alias="estimatedTime")

    # Campos opcionales
    date_scheduled: Optional[str] = Field(None, alias="dateScheduled")
    user_id: Optional[int] = Field(None, alias="userId")
    vendor_id: Optional[int] = Field(None, alias="vendorId")
    unit_id: Optional[int] = Field(None, alias="unitId")
    reservation_id: Optional[int] = Field(None, alias="reservationId")
    reference_number: Optional[str] = Field(None, alias="referenceNumber")
    description: Optional[str] = None
    work_performed: Optional[str] = Field(None, alias="workPerformed")
    source: Optional[str] = None
    source_name: Optional[str] = Field(None, alias="sourceName")
    source_phone: Optional[str] = Field(None, alias="sourcePhone")
    actual_time: Optional[int] = Field(None, alias="actualTime")
    block_checkin: Optional[bool] = Field(None, alias="blockCheckin")

    # Campos de auditoría
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    created_by: Optional[str] = Field(None, alias="createdBy")
    updated_by: Optional[str] = Field(None, alias="updatedBy")

    # Campos embebidos
    _embedded: Optional[Dict[str, Any]] = None
    _links: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "WorkOrder":
        """Crear instancia desde respuesta de API."""
        # Crear una copia del diccionario para no modificar el original
        data_copy = data.copy()

        # Extraer campos embebidos si existen
        embedded = data_copy.pop("_embedded", None)
        links = data_copy.pop("_links", None)

        # Crear instancia
        work_order = cls(**data_copy)

        # Asignar campos embebidos si existen
        if embedded is not None:
            work_order._embedded = embedded
        if links is not None:
            work_order._links = links

        return work_order

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario incluyendo campos embebidos."""
        data = self.model_dump(by_alias=True)
        if self._embedded:
            data["_embedded"] = self._embedded
        if self._links:
            data["_links"] = self._links
        return data


class WorkOrderResponse(BaseModel):
    """Respuesta completa de la API para work orders."""

    work_order: WorkOrder
    success: bool = True
    message: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_api_data(cls, data: Dict[str, Any]) -> "WorkOrderResponse":
        """Crear respuesta desde datos de API."""
        work_order = WorkOrder.from_api_response(data)
        return cls(work_order=work_order)
