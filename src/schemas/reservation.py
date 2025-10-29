"""
Schemas para reservas
"""

from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseSchema, PaginationParams, PaginationResponse


class ReservationSearchParams(PaginationParams):
    """Parámetros de búsqueda de reservas"""

    search: Optional[str] = Field(
        default=None, max_length=200, description="Búsqueda de texto"
    )
    arrival_start: Optional[date] = Field(
        default=None, description="Fecha de llegada inicio"
    )
    arrival_end: Optional[date] = Field(
        default=None, description="Fecha de llegada fin"
    )
    status: Optional[str] = Field(
        default=None, max_length=50, description="Estado de reserva"
    )


class ReservationDetailResponse(BaseModel):
    """Respuesta detallada de reserva"""

    id: int = Field(description="ID de la reserva")
    confirmation_number: Optional[str] = Field(
        default=None, description="Número de confirmación"
    )
    currency: Optional[str] = Field(default=None, description="Moneda de la reserva")
    unit_id: Optional[int] = Field(default=None, description="ID de la unidad")
    unit_type_id: Optional[int] = Field(
        default=None, description="ID del tipo de unidad"
    )
    arrival_date: Optional[str] = Field(default=None, description="Fecha de llegada")
    departure_date: Optional[str] = Field(default=None, description="Fecha de salida")
    status: Optional[str] = Field(default=None, description="Estado de la reserva")
    total_amount: Optional[float] = Field(default=None, description="Monto total")
    guest_count: Optional[int] = Field(default=None, description="Número de huéspedes")

    # Campos adicionales de la API
    alternates: Optional[List[str]] = Field(
        default=None, description="Números de confirmación alternativos"
    )
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )

    # Datos embebidos
    unit: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos de la unidad"
    )
    contact: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos de contacto"
    )
    policies: Optional[Dict[str, Any]] = Field(
        default=None, description="Políticas de la reserva"
    )

    # Enlaces
    links: Optional[Dict[str, str]] = Field(
        default=None, description="Enlaces relacionados"
    )


class ReservationSearchResponse(PaginationResponse):
    """Respuesta de búsqueda de reservas"""

    reservations: List[ReservationDetailResponse] = Field(
        description="Lista de reservas encontradas"
    )
