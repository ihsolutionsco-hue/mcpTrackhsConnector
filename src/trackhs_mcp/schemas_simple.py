"""
Schemas simplificados para FastMCP
Solo output schemas necesarios para las herramientas MCP
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

# =============================================================================
# OUTPUT SCHEMAS PARA HERRAMIENTAS MCP
# =============================================================================


class ReservationSearchOutput(BaseModel):
    """Schema de salida para búsqueda de reservas"""

    _embedded: Dict[str, List[Dict[str, Any]]] = Field(
        description="Reservas encontradas"
    )
    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    _links: Optional[Dict[str, Any]] = Field(description="Enlaces de navegación")


class ReservationDetailOutput(BaseModel):
    """Schema de salida para detalles de reserva"""

    id: int = Field(description="ID de la reserva")
    confirmation_number: Optional[str] = Field(description="Número de confirmación")
    guest_name: Optional[str] = Field(description="Nombre del huésped")
    email: Optional[str] = Field(description="Email del huésped")
    phone: Optional[str] = Field(description="Teléfono del huésped")
    arrival_date: Optional[str] = Field(description="Fecha de llegada")
    departure_date: Optional[str] = Field(description="Fecha de salida")
    status: Optional[str] = Field(description="Estado de la reserva")
    unit_id: Optional[int] = Field(description="ID de la unidad")
    total_amount: Optional[float] = Field(description="Monto total")
    balance: Optional[float] = Field(description="Balance pendiente")
    # Campos adicionales que pueden estar presentes
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UnitSearchOutput(BaseModel):
    """Schema de salida para búsqueda de unidades"""

    _embedded: Dict[str, List[Dict[str, Any]]] = Field(
        description="Unidades encontradas"
    )
    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    _links: Optional[Dict[str, Any]] = Field(description="Enlaces de navegación")


class AmenitiesOutput(BaseModel):
    """Schema de salida para búsqueda de amenidades"""

    _embedded: Dict[str, List[Dict[str, Any]]] = Field(
        description="Amenidades encontradas"
    )
    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    _links: Optional[Dict[str, Any]] = Field(description="Enlaces de navegación")


class FolioDetailOutput(BaseModel):
    """Schema de salida para folio financiero"""

    reservation_id: int = Field(description="ID de la reserva")
    total_charges: Optional[float] = Field(description="Total de cargos")
    total_payments: Optional[float] = Field(description="Total de pagos")
    balance: Optional[float] = Field(description="Balance pendiente")
    charges: Optional[List[Dict[str, Any]]] = Field(description="Lista de cargos")
    payments: Optional[List[Dict[str, Any]]] = Field(description="Lista de pagos")
    # Campos adicionales que pueden estar presentes
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class WorkOrderOutput(BaseModel):
    """Schema de salida para órdenes de trabajo"""

    id: int = Field(description="ID de la orden")
    unit_id: int = Field(description="ID de la unidad")
    summary: str = Field(description="Resumen del trabajo")
    description: Optional[str] = Field(description="Descripción detallada")
    status: str = Field(description="Estado de la orden")
    priority: Optional[int] = Field(description="Prioridad (1=Baja, 3=Media, 5=Alta)")
    created_at: Optional[str] = Field(description="Fecha de creación")
    updated_at: Optional[str] = Field(description="Fecha de actualización")
    # Campos adicionales que pueden estar presentes
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict)


# =============================================================================
# SCHEMAS JSON PARA FASTMCP
# =============================================================================

# Schemas JSON generados automáticamente desde los modelos Pydantic
RESERVATION_SEARCH_OUTPUT_SCHEMA = ReservationSearchOutput.model_json_schema()
RESERVATION_DETAIL_OUTPUT_SCHEMA = ReservationDetailOutput.model_json_schema()
UNIT_SEARCH_OUTPUT_SCHEMA = UnitSearchOutput.model_json_schema()
AMENITIES_OUTPUT_SCHEMA = AmenitiesOutput.model_json_schema()
FOLIO_DETAIL_OUTPUT_SCHEMA = FolioDetailOutput.model_json_schema()
WORK_ORDER_DETAIL_OUTPUT_SCHEMA = WorkOrderOutput.model_json_schema()


# =============================================================================
# TIPOS DE RESPUESTA SIMPLIFICADOS
# =============================================================================

# Tipos de respuesta que pueden ser retornados por las herramientas
ReservationResponse = ReservationDetailOutput
UnitResponse = UnitSearchOutput
FolioResponse = FolioDetailOutput
WorkOrderResponse = WorkOrderOutput
