"""
Schemas simplificados para FastMCP
Solo output schemas necesarios para las herramientas MCP
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

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
    """Schema de salida para detalles de reserva V2 - Completo según API TrackHS V2"""

    # Campos básicos de la reserva
    id: int = Field(description="ID de la reserva")
    alternates: Optional[List[str]] = Field(
        default=None, description="Números de confirmación alternativos"
    )
    currency: Optional[str] = Field(default=None, description="Moneda de la reserva")
    unitId: Optional[int] = Field(default=None, description="ID de la unidad")
    unitTypeId: Optional[int] = Field(default=None, description="ID del tipo de unidad")

    # Campos de seguridad y fraude
    clientIPAddress: Optional[str] = Field(
        default=None, description="IP del cliente para detección de fraude"
    )
    session: Optional[str] = Field(
        default=None, description="Datos de sesión para detección de fraude"
    )

    # Información de fechas
    arrivalDate: Optional[str] = Field(
        default=None, description="Fecha de llegada (ISO 8601)"
    )
    departureDate: Optional[str] = Field(
        default=None, description="Fecha de salida (ISO 8601)"
    )
    arrivalTime: Optional[str] = Field(
        default=None, description="Fecha y hora de llegada (ISO 8601)"
    )
    departureTime: Optional[str] = Field(
        default=None, description="Fecha y hora de salida (ISO 8601)"
    )
    nights: Optional[float] = Field(default=None, description="Número de noches")
    earlyArrival: Optional[bool] = Field(default=None, description="Llegada temprana")
    lateDeparture: Optional[bool] = Field(default=None, description="Salida tardía")

    # Estado y bloqueos
    status: Optional[str] = Field(default=None, description="Estado de la reserva")
    isUnitLocked: Optional[bool] = Field(default=None, description="Unidad bloqueada")
    isUnitAssigned: Optional[bool] = Field(default=None, description="Unidad asignada")
    isUnitTypeLocked: Optional[bool] = Field(
        default=None, description="Tipo de unidad bloqueado"
    )
    isChannelLocked: Optional[bool] = Field(default=None, description="Canal bloqueado")

    # Información de cancelación
    cancelledAt: Optional[str] = Field(
        default=None, description="Fecha de cancelación (ISO 8601)"
    )
    cancellationReasonId: Optional[int] = Field(
        default=None, description="ID del motivo de cancelación"
    )

    # Ocupantes
    occupants: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Lista de ocupantes"
    )

    # Depósito de seguridad
    securityDeposit: Optional[Dict[str, Any]] = Field(
        default=None, description="Detalles del depósito de seguridad"
    )

    # Fechas de auditoría
    updatedAt: Optional[str] = Field(
        default=None, description="Fecha de última actualización (ISO 8601)"
    )
    createdAt: Optional[str] = Field(
        default=None, description="Fecha de creación (ISO 8601)"
    )
    bookedAt: Optional[str] = Field(
        default=None, description="Fecha de reserva (ISO 8601)"
    )

    # Desglose financiero del huésped
    guestBreakdown: Optional[Dict[str, Any]] = Field(
        default=None, description="Desglose financiero del huésped"
    )

    # Desglose financiero del propietario
    ownerBreakdown: Optional[Dict[str, Any]] = Field(
        default=None, description="Desglose financiero del propietario"
    )

    # Campos de descuento
    discountReasonId: Optional[int] = Field(
        default=None, description="ID del motivo de descuento"
    )
    discountNotes: Optional[str] = Field(
        default=None, description="Notas del descuento"
    )

    # IDs de referencia
    contactId: Optional[int] = Field(default=None, description="ID del contacto")
    channelId: Optional[int] = Field(default=None, description="ID del canal")
    subChannel: Optional[str] = Field(default=None, description="Subcanal")
    folioId: Optional[int] = Field(default=None, description="ID del folio")
    guaranteePolicyId: Optional[int] = Field(
        default=None, description="ID de la política de garantía"
    )
    cancellationPolicyId: Optional[int] = Field(
        default=None, description="ID de la política de cancelación"
    )
    userId: Optional[int] = Field(default=None, description="ID del usuario")
    travelAgentId: Optional[int] = Field(
        default=None, description="ID del agente de viajes"
    )
    campaignId: Optional[int] = Field(default=None, description="ID de la campaña")
    typeId: Optional[int] = Field(default=None, description="ID del tipo")
    rateTypeId: Optional[int] = Field(default=None, description="ID del tipo de tarifa")
    unitCodeId: Optional[int] = Field(
        default=None, description="ID del código de unidad"
    )
    cancelledById: Optional[int] = Field(
        default=None, description="ID de quien canceló"
    )
    paymentMethodId: Optional[int] = Field(
        default=None, description="ID del método de pago"
    )
    quoteId: Optional[int] = Field(default=None, description="ID de la cotización")
    promoCodeId: Optional[int] = Field(
        default=None, description="ID del código promocional"
    )
    groupId: Optional[int] = Field(default=None, description="ID del grupo")

    # Configuraciones adicionales
    holdExpiresAt: Optional[str] = Field(
        default=None, description="Fecha de expiración de la reserva (ISO 8601)"
    )
    isTaxable: Optional[bool] = Field(default=None, description="Sujeto a impuestos")
    inviteUuid: Optional[str] = Field(default=None, description="UUID de invitación")
    uuid: Optional[str] = Field(default=None, description="UUID de la reserva")
    source: Optional[str] = Field(default=None, description="Fuente de la reserva")
    agreementStatus: Optional[str] = Field(
        default=None, description="Estado del acuerdo"
    )
    automatePayment: Optional[bool] = Field(
        default=None, description="Pago automatizado"
    )
    revenueRealizedMethod: Optional[str] = Field(
        default=None, description="Método de realización de ingresos"
    )

    # Programación de pagos
    scheduleType1: Optional[str] = Field(
        default=None, description="Tipo de programación 1"
    )
    schedulePercentage1: Optional[float] = Field(
        default=None, description="Porcentaje de programación 1"
    )
    scheduleType2: Optional[str] = Field(
        default=None, description="Tipo de programación 2"
    )
    schedulePercentage2: Optional[float] = Field(
        default=None, description="Porcentaje de programación 2"
    )

    # Usuarios de auditoría
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")
    createdBy: Optional[str] = Field(default=None, description="Creado por")

    # Plan de pago
    paymentPlan: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Plan de pago"
    )

    # Información de tarifas
    rateType: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de tarifa"
    )

    # Productos de seguro de viaje
    travelInsuranceProducts: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Productos de seguro de viaje"
    )

    # Información embebida
    embedded: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="_embedded",
        description="Datos embebidos (unidad, contacto, políticas, etc.)",
    )

    # Enlaces
    links: Optional[Dict[str, Any]] = Field(
        default=None, alias="_links", description="Enlaces relacionados"
    )

    # Campos adicionales para compatibilidad
    additional_data: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Datos adicionales"
    )


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

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = Field(default=None, description="ID de la amenidad")
    name: str = Field(description="Nombre de la amenidad")
    groupId: Optional[int] = Field(default=None, description="ID del grupo")
    group: Optional[str] = Field(
        default=None, description="Nombre del grupo (normalizado a string)"
    )
    homeawayType: Optional[str] = Field(default=None, description="Tipo de HomeAway")
    airbnbType: Optional[str] = Field(default=None, description="Tipo de Airbnb")
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
