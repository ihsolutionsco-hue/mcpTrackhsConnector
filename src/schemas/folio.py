"""
Schemas para folios financieros
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseSchema


class FolioItem(BaseModel):
    """Item del folio financiero"""

    id: int = Field(description="ID del item")
    description: str = Field(description="Descripción del item")
    amount: float = Field(description="Monto")
    currency: str = Field(description="Moneda")
    category: Optional[str] = Field(default=None, description="Categoría")
    type: Optional[str] = Field(default=None, description="Tipo (charge/credit)")
    date: Optional[str] = Field(default=None, description="Fecha")


class FolioResponse(BaseModel):
    """Respuesta de folio financiero"""

    reservation_id: int = Field(description="ID de la reserva")
    total_amount: float = Field(description="Monto total")
    currency: str = Field(description="Moneda")
    balance: float = Field(description="Balance actual")

    # Items del folio
    items: List[FolioItem] = Field(description="Items del folio")

    # Desglose por categorías
    guest_charges: Optional[float] = Field(
        default=None, description="Cargos del huésped"
    )
    owner_charges: Optional[float] = Field(
        default=None, description="Cargos del propietario"
    )
    taxes: Optional[float] = Field(default=None, description="Impuestos")
    fees: Optional[float] = Field(default=None, description="Tarifas")

    # Fechas
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )

    # Enlaces
    links: Optional[Dict[str, str]] = Field(
        default=None, description="Enlaces relacionados"
    )
