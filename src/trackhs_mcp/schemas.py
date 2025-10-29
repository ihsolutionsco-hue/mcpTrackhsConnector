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

    embedded: Dict[str, List[Dict[str, Any]]] = Field(
        alias="_embedded", description="Reservas encontradas"
    )
    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    links: Optional[Dict[str, Any]] = Field(
        alias="_links", description="Enlaces de navegación"
    )


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

    embedded: Dict[str, List[Dict[str, Any]]] = Field(
        alias="_embedded", description="Unidades encontradas"
    )
    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    links: Optional[Dict[str, Any]] = Field(
        alias="_links", description="Enlaces de navegación"
    )


class AmenityGroup(BaseModel):
    """Schema para el grupo de amenidad"""

    name: Optional[str] = Field(description="Nombre del grupo")


class AmenityLinks(BaseModel):
    """Schema para enlaces de amenidad"""

    self: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a la amenidad"
    )
    group: Optional[Dict[str, str]] = Field(default=None, description="Enlace al grupo")


class AmenityItem(BaseModel):
    """Schema para un item de amenidad individual"""

    id: Optional[int] = Field(default=None, description="ID de la amenidad")
    name: str = Field(description="Nombre de la amenidad")
    groupId: Optional[int] = Field(default=None, description="ID del grupo")
    group: Optional[AmenityGroup] = Field(
        default=None, description="Información del grupo"
    )
    homeawayType: Optional[str] = Field(default=None, description="Tipo de HomeAway")
    airbnbType: Optional[str] = Field(default=None, description="Tipo de Airbnb")
    tripadvisorType: Optional[str] = Field(
        default=None, description="Tipo de TripAdvisor"
    )
    marriottType: Optional[str] = Field(default=None, description="Tipo de Marriott")
    bookingDotComPropertyType: Optional[str] = Field(
        default=None, description="Tipo de propiedad de Booking.com"
    )
    bookingDotComAccommodationType: Optional[str] = Field(
        default=None, description="Tipo de alojamiento de Booking.com"
    )
    expediaPropertyType: Optional[str] = Field(
        default=None, description="Tipo de propiedad de Expedia"
    )
    expediaAccommodationType: Optional[str] = Field(
        default=None, description="Tipo de alojamiento de Expedia"
    )
    isFilterable: Optional[bool] = Field(default=None, description="Si es filtrable")
    isPublic: Optional[bool] = Field(default=None, description="Si es público")
    publicSearchable: Optional[bool] = Field(
        default=None, description="Si es buscable públicamente"
    )
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    links: Optional[AmenityLinks] = Field(
        default=None, alias="_links", description="Enlaces de la amenidad"
    )


class AmenitiesEmbedded(BaseModel):
    """Schema para la sección _embedded de amenidades"""

    amenities: List[AmenityItem] = Field(description="Lista de amenidades")


class AmenitiesLinks(BaseModel):
    """Schema para enlaces de navegación"""

    self: Dict[str, str] = Field(description="Enlace actual")
    first: Optional[Dict[str, str]] = Field(default=None, description="Primera página")
    last: Optional[Dict[str, str]] = Field(default=None, description="Última página")
    next: Optional[Dict[str, str]] = Field(default=None, description="Siguiente página")
    prev: Optional[Dict[str, str]] = Field(default=None, description="Página anterior")


class AmenitiesOutput(BaseModel):
    """Schema de salida para búsqueda de amenidades según OpenAPI spec"""

    links: AmenitiesLinks = Field(alias="_links", description="Enlaces de navegación")
    total_items: int = Field(description="Total de elementos")
    page_size: int = Field(description="Tamaño de página")
    page_count: int = Field(description="Total de páginas")
    page: int = Field(description="Página actual")
    embedded: AmenitiesEmbedded = Field(
        alias="_embedded", description="Amenidades encontradas"
    )


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
