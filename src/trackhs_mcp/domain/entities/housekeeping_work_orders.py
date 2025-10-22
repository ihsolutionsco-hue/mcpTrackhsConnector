"""
Entidades de dominio para Housekeeping Work Orders.

Este módulo define las entidades y modelos de datos para las órdenes de trabajo
de housekeeping en TrackHS, incluyendo validaciones y transformaciones.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HousekeepingWorkOrderStatus(str, Enum):
    """Estados válidos para órdenes de trabajo de housekeeping."""

    PENDING = "pending"
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    PROCESSED = "processed"
    CANCELLED = "cancelled"
    EXCEPTION = "exception"


class CreateHousekeepingWorkOrderParams(BaseModel):
    """Parámetros para crear una nueva orden de trabajo de housekeeping."""

    # Campos requeridos
    scheduled_at: str = Field(
        ..., alias="scheduledAt", description="Fecha programada en formato ISO 8601"
    )

    # Campos condicionales - exactamente uno de unit_id o unit_block_id
    unit_id: Optional[int] = Field(
        None, alias="unitId", gt=0, description="ID de la unidad"
    )
    unit_block_id: Optional[int] = Field(
        None, alias="unitBlockId", gt=0, description="ID del bloque de unidad"
    )

    # Campos condicionales - exactamente uno de is_inspection o clean_type_id
    is_inspection: Optional[bool] = Field(
        None, alias="isInspection", description="Si es una inspección"
    )
    clean_type_id: Optional[str] = Field(
        None, alias="cleanTypeId", description="ID del tipo de limpieza"
    )

    # Campos opcionales
    user_id: Optional[int] = Field(
        None, alias="userId", gt=0, description="ID del usuario asignado"
    )
    vendor_id: Optional[int] = Field(
        None, alias="vendorId", gt=0, description="ID del proveedor"
    )
    reservation_id: Optional[str] = Field(
        None, alias="reservationId", description="ID de la reserva"
    )
    is_turn: Optional[bool] = Field(None, alias="isTurn", description="Si es un turno")
    charge_owner: Optional[bool] = Field(
        None, alias="chargeOwner", description="Si se cobra al propietario"
    )
    comments: Optional[str] = Field(None, description="Comentarios adicionales")
    cost: Optional[float] = Field(None, ge=0, description="Costo de la orden")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @field_validator("scheduled_at")
    @classmethod
    def validate_scheduled_at(cls, v):
        """Valida el formato de fecha ISO 8601."""
        try:
            # Intentar parsear como ISO 8601
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(
                "scheduled_at debe estar en formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ)"
            )
        return v

    def model_post_init(self, __context):
        """Validaciones a nivel de modelo después de la inicialización."""
        # Validar campos de unidad
        if not self.unit_id and not self.unit_block_id:
            raise ValueError("Se requiere exactamente uno de unit_id o unit_block_id")
        if self.unit_id and self.unit_block_id:
            raise ValueError("No se pueden especificar ambos unit_id y unit_block_id")

        # Validar campos de tipo de tarea
        if not self.is_inspection and not self.clean_type_id:
            raise ValueError(
                "Se requiere exactamente uno de is_inspection o clean_type_id"
            )
        if self.is_inspection and self.clean_type_id:
            raise ValueError(
                "No se pueden especificar ambos is_inspection y clean_type_id"
            )


class HousekeepingWorkOrder(BaseModel):
    """Modelo de orden de trabajo de housekeeping."""

    id: int = Field(..., description="ID único de la orden")
    scheduled_at: str = Field(..., alias="scheduledAt", description="Fecha programada")
    status: HousekeepingWorkOrderStatus = Field(..., description="Estado actual")
    unit_id: Optional[int] = Field(None, alias="unitId", description="ID de la unidad")
    unit_block_id: Optional[int] = Field(
        None, alias="unitBlockId", description="ID del bloque de unidad"
    )
    is_inspection: Optional[bool] = Field(
        None, alias="isInspection", description="Si es inspección"
    )
    clean_type_id: Optional[int] = Field(
        None, alias="cleanTypeId", description="ID del tipo de limpieza"
    )
    time_estimate: Optional[float] = Field(
        None, alias="timeEstimate", description="Tiempo estimado"
    )
    actual_time: Optional[float] = Field(
        None, alias="actualTime", description="Tiempo real"
    )
    user_id: Optional[int] = Field(None, alias="userId", description="ID del usuario")
    vendor_id: Optional[int] = Field(
        None, alias="vendorId", description="ID del proveedor"
    )
    reservation_id: Optional[int] = Field(
        None, alias="reservationId", description="ID de la reserva"
    )
    is_turn: Optional[bool] = Field(None, alias="isTurn", description="Si es turno")
    is_manual: Optional[bool] = Field(
        None, alias="isManual", description="Si es manual"
    )
    charge_owner: Optional[bool] = Field(
        None, alias="chargeOwner", description="Si se cobra al propietario"
    )
    comments: Optional[str] = Field(None, description="Comentarios")
    cost: Optional[float] = Field(None, description="Costo")
    created_at: Optional[str] = Field(
        None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        None, alias="updatedAt", description="Fecha de actualización"
    )

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class HousekeepingWorkOrderResponse(BaseModel):
    """Respuesta de creación de orden de trabajo de housekeeping."""

    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[HousekeepingWorkOrder] = Field(
        None, description="Datos de la orden creada"
    )
    message: Optional[str] = Field(None, description="Mensaje de respuesta")
    errors: Optional[List[str]] = Field(None, description="Lista de errores")

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def success_response(
        cls, work_order: HousekeepingWorkOrder
    ) -> "HousekeepingWorkOrderResponse":
        """Crea una respuesta de éxito."""
        return cls(
            success=True,
            data=work_order,
            message="Orden de trabajo de housekeeping creada exitosamente",
        )

    @classmethod
    def error_response(
        cls, message: str, errors: Optional[List[str]] = None
    ) -> "HousekeepingWorkOrderResponse":
        """Crea una respuesta de error."""
        return cls(success=False, message=message, errors=errors or [])
