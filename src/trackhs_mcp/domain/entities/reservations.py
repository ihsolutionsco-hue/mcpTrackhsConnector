"""
Modelos Pydantic para Reservations de Track HS API V2
Basado en la especificación completa de la API Search Reservations V2
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class Guest(BaseModel):
    """Modelo de Guest"""

    id: int = Field(..., description="ID único del huésped")
    first_name: str = Field(..., description="Nombre del huésped")
    last_name: str = Field(..., description="Apellido del huésped")
    email: str = Field(..., description="Email del huésped")
    phone: Optional[str] = Field(default=None, description="Teléfono del huésped")
    nationality: Optional[str] = Field(
        default=None, description="Nacionalidad del huésped"
    )
    document_type: Optional[str] = Field(default=None, description="Tipo de documento")
    document_number: Optional[str] = Field(
        default=None, description="Número de documento"
    )


class Property(BaseModel):
    """Modelo de Property"""

    id: int = Field(..., description="ID único de la propiedad")
    name: str = Field(..., description="Nombre de la propiedad")
    address: str = Field(..., description="Dirección de la propiedad")
    city: str = Field(..., description="Ciudad")
    country: str = Field(..., description="País")
    property_type: str = Field(..., description="Tipo de propiedad")
    bedrooms: int = Field(..., description="Número de habitaciones")
    bathrooms: int = Field(..., description="Número de baños")
    max_guests: int = Field(..., description="Máximo de huéspedes")


class SecurityDeposit(BaseModel):
    """Modelo de SecurityDeposit"""

    required: str = Field(
        ..., description="Monto total requerido del depósito de seguridad"
    )
    remaining: float = Field(
        ..., description="Monto restante del depósito de seguridad"
    )


class Occupant(BaseModel):
    """Modelo de Occupant"""

    type_id: int = Field(..., description="ID del tipo de ocupante")
    name: str = Field(..., description="Nombre del ocupante")
    handle: str = Field(..., description="Handle del ocupante")
    quantity: float = Field(..., description="Cantidad")
    included: bool = Field(..., description="Si está incluido en el precio de renta")
    extra_quantity: float = Field(..., description="Cantidad extra permitida")
    rate_per_person_per_stay: str = Field(
        ..., description="Tarifa por persona por estadía"
    )
    rate_per_stay: str = Field(..., description="Tarifa por estadía")


class Rate(BaseModel):
    """Modelo de Rate"""

    date: str = Field(..., description="Fecha")
    rate: str = Field(..., description="Tarifa")
    nights: int = Field(..., description="Noches")
    is_quoted: bool = Field(..., description="Si está cotizada")


class GuestFee(BaseModel):
    """Modelo de GuestFee"""

    id: str = Field(..., description="ID de la tarifa")
    name: str = Field(..., description="Nombre de la tarifa")
    display_as: Literal["itemize", "rent", "tax", "service"] = Field(
        ..., description="Cómo mostrar"
    )
    quantity: str = Field(..., description="Cantidad")
    unit_value: str = Field(..., description="Valor unitario")
    value: str = Field(..., description="Valor")


class Tax(BaseModel):
    """Modelo de Tax"""

    id: int = Field(..., description="ID del impuesto")
    name: str = Field(..., description="Nombre del impuesto")
    amount: str = Field(..., description="Monto del impuesto")


class OwnerFee(BaseModel):
    """Modelo de OwnerFee"""

    id: str = Field(..., description="ID de la tarifa")
    name: str = Field(..., description="Nombre de la tarifa")
    display_as: Literal["itemize", "rent", "tax", "service"] = Field(
        ..., description="Cómo mostrar"
    )
    quantity: str = Field(..., description="Cantidad")
    unit_value: str = Field(..., description="Valor unitario")
    value: str = Field(..., description="Valor")


class OwnerBreakdown(BaseModel):
    """Modelo de OwnerBreakdown"""

    gross_rent: str = Field(..., description="Renta bruta del propietario")
    fee_revenue: str = Field(..., description="Ingresos por tarifas")
    gross_revenue: str = Field(..., description="Ingresos brutos")
    manager_commission: str = Field(..., description="Comisión del manager")
    agent_commission: str = Field(..., description="Comisión del agente")
    net_revenue: str = Field(..., description="Ingresos netos")
    owner_fees: List[OwnerFee] = Field(..., description="Tarifas del propietario")


class GuestBreakdown(BaseModel):
    """Modelo de GuestBreakdown"""

    gross_rent: str = Field(..., description="Renta bruta")
    guest_gross_display_rent: str = Field(
        ..., description="Renta bruta mostrada al huésped"
    )
    discount: str = Field(..., description="Descuento")
    promo_value: str = Field(..., description="Valor promocional")
    discount_total: float = Field(..., description="Total de descuentos")
    net_rent: str = Field(..., description="Renta neta")
    guest_net_display_rent: str = Field(
        ..., description="Renta neta mostrada al huésped"
    )
    actual_adr: str = Field(..., description="ADR actual")
    guest_adr: str = Field(..., description="ADR del huésped")
    total_guest_fees: str = Field(..., description="Total de tarifas del huésped")
    total_rent_fees: str = Field(..., description="Total de tarifas de renta")
    total_itemized_fees: str = Field(..., description="Total de tarifas detalladas")
    total_tax_fees: str = Field(..., description="Total de tarifas de impuestos")
    total_service_fees: str = Field(..., description="Total de tarifas de servicio")
    folio_charges: str = Field(..., description="Cargos del folio")
    subtotal: str = Field(..., description="Subtotal")
    guest_subtotal: str = Field(..., description="Subtotal del huésped")
    total_taxes: str = Field(..., description="Total de impuestos")
    total_guest_taxes: str = Field(..., description="Total de impuestos del huésped")
    total: str = Field(..., description="Total")
    grand_total: str = Field(..., description="Gran total")
    net_payments: str = Field(..., description="Pagos netos")
    payments: str = Field(..., description="Pagos")
    refunds: str = Field(..., description="Reembolsos")
    net_transfers: str = Field(..., description="Transferencias netas")
    balance: str = Field(..., description="Balance")
    rates: List[Rate] = Field(..., description="Tarifas")
    guest_fees: List[GuestFee] = Field(..., description="Tarifas del huésped")
    taxes: List[Tax] = Field(..., description="Impuestos")


class GuaranteePolicy(BaseModel):
    """Modelo de GuaranteePolicy"""

    id: int = Field(..., description="ID de la política")
    name: str = Field(..., description="Nombre de la política")
    type: Literal["Hold", "Guarantee", "FullDeposit"] = Field(
        ..., description="Tipo de política"
    )
    hold: Dict[str, int] = Field(..., description="Configuración de retención")


class CancellationBreakpoint(BaseModel):
    """Modelo de CancellationBreakpoint"""

    start: int = Field(..., description="Inicio del rango")
    end: int = Field(..., description="Fin del rango")
    non_refundable: bool = Field(..., description="No reembolsable")
    non_cancelable: bool = Field(..., description="No cancelable")
    penalty_nights: int = Field(..., description="Noches de penalización")
    penalty_percent: str = Field(..., description="Porcentaje de penalización")
    penalty_flat: str = Field(..., description="Penalización fija")
    description: str = Field(..., description="Descripción")


class CancellationPolicy(BaseModel):
    """Modelo de CancellationPolicy"""

    id: int = Field(..., description="ID de la política")
    name: str = Field(..., description="Nombre de la política")
    time: str = Field(..., description="Tiempo")
    timezone: str = Field(..., description="Zona horaria")
    breakpoints: List[CancellationBreakpoint] = Field(
        ..., description="Puntos de quiebre"
    )


class PaymentPlan(BaseModel):
    """Modelo de PaymentPlan"""

    date: str = Field(..., description="Fecha")
    amount: str = Field(..., description="Monto")


class TravelInsuranceProduct(BaseModel):
    """Modelo de TravelInsuranceProduct"""

    id: int = Field(..., description="ID del producto")
    status: Literal["optin", "funded", "cancelled"] = Field(..., description="Estado")
    type: Literal["Travel Insurance", "Master Cancel", "Damage Deposit"] = Field(
        ..., description="Tipo"
    )
    provider: str = Field(..., description="Proveedor")
    provider_id: int = Field(..., description="ID del proveedor")
    amount: str = Field(..., description="Monto")


class Reservation(BaseModel):
    """Modelo de Reservation V2 - Basado en la especificación completa de la API"""

    id: int = Field(..., description="ID único de la reserva")
    alternates: Optional[List[str]] = Field(
        default=None, description="IDs de confirmación alternativos"
    )
    currency: str = Field(..., description="Moneda de la reserva")
    unit_id: int = Field(..., description="ID de la unidad")
    client_ip_address: Optional[str] = Field(
        default=None, description="Dirección IP del cliente"
    )
    session: Optional[str] = Field(
        default=None, description="Datos de sesión para detección de fraude"
    )
    is_unit_locked: bool = Field(..., description="Si la unidad está bloqueada")
    is_unit_assigned: bool = Field(..., description="Si la unidad está asignada")
    is_unit_type_locked: bool = Field(
        ..., description="Si el tipo de unidad está bloqueado"
    )
    unit_type_id: int = Field(..., description="ID del tipo de unidad")
    arrival_date: str = Field(..., description="Fecha de llegada (ISO 8601)")
    departure_date: str = Field(..., description="Fecha de salida (ISO 8601)")
    early_arrival: bool = Field(..., description="Llegada temprana")
    late_departure: bool = Field(..., description="Salida tardía")
    arrival_time: str = Field(..., description="Hora de llegada (ISO 8601)")
    departure_time: str = Field(..., description="Hora de salida (ISO 8601)")
    nights: float = Field(..., description="Número de noches")
    status: Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"] = (
        Field(..., description="Estado de la reserva")
    )
    cancelled_at: Optional[str] = Field(
        default=None, description="Fecha de cancelación (ISO 8601)"
    )
    occupants: List[Occupant] = Field(..., description="Ocupantes")
    security_deposit: SecurityDeposit = Field(..., description="Depósito de seguridad")
    updated_at: str = Field(..., description="Fecha de actualización (ISO 8601)")
    created_at: str = Field(..., description="Fecha de creación (ISO 8601)")
    booked_at: str = Field(..., description="Fecha de reserva (ISO 8601)")
    guest_breakdown: GuestBreakdown = Field(..., description="Desglose del huésped")
    owner_breakdown: Optional[OwnerBreakdown] = Field(
        default=None, description="Desglose del propietario"
    )
    discount_reason_id: Optional[int] = Field(
        default=None, description="ID de la razón del descuento"
    )
    discount_notes: Optional[str] = Field(
        default=None, description="Notas del descuento"
    )
    contact_id: int = Field(..., description="ID del contacto")
    channel_id: int = Field(..., description="ID del canal")
    sub_channel: Optional[str] = Field(default=None, description="Subcanal")
    folio_id: int = Field(..., description="ID del folio")
    guarantee_policy_id: Optional[int] = Field(
        default=None, description="ID de la política de garantía"
    )
    cancellation_policy_id: Optional[int] = Field(
        default=None, description="ID de la política de cancelación"
    )
    cancellation_reason_id: Optional[int] = Field(
        default=None, description="ID de la razón de cancelación"
    )
    user_id: int = Field(..., description="ID del usuario")
    travel_agent_id: Optional[int] = Field(
        default=None, description="ID del agente de viajes"
    )
    campaign_id: Optional[int] = Field(default=None, description="ID de la campaña")
    type_id: int = Field(..., description="ID del tipo")
    rate_type_id: int = Field(..., description="ID del tipo de tarifa")
    unit_code_id: Optional[int] = Field(
        default=None, description="ID del código de unidad"
    )
    cancelled_by_id: Optional[int] = Field(
        default=None, description="ID de quien canceló"
    )
    payment_method_id: Optional[int] = Field(
        default=None, description="ID del método de pago"
    )
    quote_id: Optional[int] = Field(default=None, description="ID de la cotización")
    hold_expires_at: Optional[str] = Field(
        default=None, description="Fecha de expiración de la retención"
    )
    is_taxable: bool = Field(..., description="Si es gravable")
    invite_uuid: Optional[str] = Field(
        default=None, description="UUID de la invitación"
    )
    uuid: str = Field(..., description="UUID de la reserva")
    source: str = Field(..., description="Fuente de la reserva")
    is_channel_locked: bool = Field(..., description="Si el canal está bloqueado")
    agreement_status: Literal[
        "not-needed", "not-sent", "sent", "viewed", "received"
    ] = Field(..., description="Estado del acuerdo")
    automate_payment: bool = Field(..., description="Si el pago es automático")
    revenue_realized_method: str = Field(
        ..., description="Método de realización de ingresos"
    )
    schedule_type1: Optional[str] = Field(
        default=None, description="Tipo de programación 1"
    )
    schedule_percentage1: Optional[float] = Field(
        default=None, description="Porcentaje de programación 1"
    )
    schedule_type2: Optional[str] = Field(
        default=None, description="Tipo de programación 2"
    )
    schedule_percentage2: Optional[float] = Field(
        default=None, description="Porcentaje de programación 2"
    )
    promo_code_id: Optional[int] = Field(
        default=None, description="ID del código promocional"
    )
    updated_by: str = Field(..., description="Actualizado por")
    created_by: str = Field(..., description="Creado por")
    group_id: Optional[int] = Field(default=None, description="ID del grupo")
    payment_plan: List[PaymentPlan] = Field(..., description="Plan de pagos")
    travel_insurance_products: List[TravelInsuranceProduct] = Field(
        ..., description="Productos de seguro de viaje"
    )
    embedded: Dict[str, Any] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")


class SearchReservationsParams(PaginationParams, SearchParams):
    """Parámetros para buscar reservas V2 - Basado en la especificación completa"""

    sort_column: Optional[
        Literal[
            "name",
            "status",
            "altCon",
            "agreementStatus",
            "type",
            "guest",
            "guests",
            "unit",
            "units",
            "checkin",
            "checkout",
            "nights",
        ]
    ] = Field(default="name", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    tags: Optional[str] = Field(default=None, description="Búsqueda por ID de tag")
    node_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del nodo específico"
    )
    unit_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) de la unidad específica"
    )
    reservation_type_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del tipo de reserva específico"
    )
    contact_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del contacto específico"
    )
    travel_agent_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del agente de viajes específico"
    )
    campaign_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) de la campaña específica"
    )
    user_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del usuario específico"
    )
    unit_type_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del tipo de unidad específico"
    )
    rate_type_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del tipo de tarifa específico"
    )
    booked_start: Optional[str] = Field(
        default=None, description="Fecha de inicio de reserva (ISO 8601)"
    )
    booked_end: Optional[str] = Field(
        default=None, description="Fecha de fin de reserva (ISO 8601)"
    )
    arrival_start: Optional[str] = Field(
        default=None, description="Fecha de inicio de llegada (ISO 8601)"
    )
    arrival_end: Optional[str] = Field(
        default=None, description="Fecha de fin de llegada (ISO 8601)"
    )
    departure_start: Optional[str] = Field(
        default=None, description="Fecha de inicio de salida (ISO 8601)"
    )
    departure_end: Optional[str] = Field(
        default=None, description="Fecha de fin de salida (ISO 8601)"
    )
    updated_since: Optional[str] = Field(
        default=None, description="Fecha de actualización desde (ISO 8601)"
    )
    scroll: Optional[Union[int, str]] = Field(
        default=None,
        description="Scroll de Elasticsearch (1 para empezar, string para continuar)",
    )
    in_house_today: Optional[Literal[0, 1]] = Field(
        default=None, description="Filtrar por en casa hoy"
    )
    status: Optional[
        Union[
            Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"],
            List[str],
        ]
    ] = Field(default=None, description="Estado(s) de la reserva")
    group_id: Optional[int] = Field(default=None, description="ID del grupo conectado")
    checkin_office_id: Optional[int] = Field(
        default=None, description="ID de la oficina de check-in"
    )


class SearchReservationsResponse(BaseModel):
    """Respuesta de búsqueda de reservas"""

    embedded: Dict[str, List[Reservation]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., alias="total_items", description="Total de elementos")
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")


class GetReservationParams(BaseModel):
    """Parámetros para obtener una reserva específica"""

    reservation_id: int = Field(..., description="ID de la reserva")


class ReservationResponse(BaseModel):
    """Respuesta de una reserva específica"""

    data: Reservation = Field(..., description="Datos de la reserva")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")


# Modelos embebidos para la respuesta completa de la API V2
class UnitEmbedded(BaseModel):
    """Modelo para unidad embebida en respuesta de reservación"""

    id: int = Field(..., description="ID de la unidad")
    name: str = Field(..., description="Nombre de la unidad")
    short_name: Optional[str] = Field(default=None, description="Nombre corto")
    unit_code: Optional[str] = Field(default=None, description="Código de la unidad")
    headline: Optional[str] = Field(default=None, description="Título")
    short_description: Optional[str] = Field(
        default=None, description="Descripción corta"
    )
    long_description: Optional[str] = Field(
        default=None, description="Descripción larga"
    )
    house_rules: Optional[str] = Field(default=None, description="Reglas de la casa")
    node_id: int = Field(..., description="ID del nodo")
    unit_type: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de unidad"
    )
    lodging_type: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de alojamiento"
    )
    directions: Optional[str] = Field(default=None, description="Direcciones")
    checkin_details: Optional[str] = Field(
        default=None, description="Detalles de check-in"
    )
    timezone: str = Field(..., description="Zona horaria")
    checkin_time: str = Field(..., description="Hora de check-in")
    has_early_checkin: bool = Field(..., description="Permite check-in temprano")
    early_checkin_time: Optional[str] = Field(
        default=None, description="Hora de check-in temprano"
    )
    checkout_time: str = Field(..., description="Hora de check-out")
    has_late_checkout: bool = Field(..., description="Permite check-out tardío")
    late_checkout_time: Optional[str] = Field(
        default=None, description="Hora de check-out tardío"
    )
    min_booking_window: Optional[int] = Field(
        default=None, description="Ventana mínima de reserva"
    )
    max_booking_window: Optional[int] = Field(
        default=None, description="Ventana máxima de reserva"
    )
    website: Optional[str] = Field(default=None, description="Sitio web")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    street_address: str = Field(..., description="Dirección")
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: str = Field(..., description="Localidad")
    region: str = Field(..., description="Región")
    postal_code: str = Field(..., description="Código postal")
    country: str = Field(..., description="País")
    longitude: Optional[float] = Field(default=None, description="Longitud")
    latitude: Optional[float] = Field(default=None, description="Latitud")
    pets_friendly: bool = Field(..., description="Permite mascotas")
    max_pets: int = Field(..., description="Máximo de mascotas")
    events_allowed: bool = Field(..., description="Permite eventos")
    smoking_allowed: bool = Field(..., description="Permite fumar")
    children_allowed: bool = Field(..., description="Permite niños")
    minimum_age_limit: Optional[int] = Field(default=None, description="Edad mínima")
    is_accessible: bool = Field(..., description="Es accesible")
    area: Optional[float] = Field(default=None, description="Área")
    floors: Optional[float] = Field(default=None, description="Pisos")
    max_occupancy: int = Field(..., description="Ocupación máxima")
    security_deposit: str = Field(..., description="Depósito de seguridad")
    bedrooms: int = Field(..., description="Habitaciones")
    full_bathrooms: int = Field(..., description="Baños completos")
    three_quarter_bathrooms: int = Field(..., description="Baños de 3/4")
    half_bathrooms: int = Field(..., description="Medios baños")
    bed_types: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Tipos de cama"
    )
    rooms: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Habitaciones"
    )
    amenities: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Amenidades"
    )
    amenity_description: Optional[str] = Field(
        default=None, description="Descripción de amenidades"
    )
    cover_image: Optional[str] = Field(default=None, description="Imagen de portada")
    tax_id: Optional[int] = Field(default=None, description="ID de impuesto")
    local_office: Optional[Dict[str, Any]] = Field(
        default=None, description="Oficina local"
    )
    regulations: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Regulaciones"
    )
    updated: Optional[Dict[str, str]] = Field(
        default=None, description="Actualizaciones"
    )
    updated_at: str = Field(..., description="Fecha de actualización")
    created_at: str = Field(..., description="Fecha de creación")
    is_active: bool = Field(..., description="Está activo")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class ContactEmbedded(BaseModel):
    """Modelo para contacto embebido en respuesta de reservación"""

    id: int = Field(..., description="ID del contacto")
    first_name: str = Field(..., description="Nombre")
    last_name: str = Field(..., description="Apellido")
    name: str = Field(..., description="Nombre completo")
    primary_email: str = Field(..., description="Email principal")
    secondary_email: Optional[str] = Field(default=None, description="Email secundario")
    home_phone: Optional[str] = Field(default=None, description="Teléfono casa")
    cell_phone: Optional[str] = Field(default=None, description="Teléfono celular")
    work_phone: Optional[str] = Field(default=None, description="Teléfono trabajo")
    other_phone: Optional[str] = Field(default=None, description="Otro teléfono")
    fax: Optional[str] = Field(default=None, description="Fax")
    street_address: Optional[str] = Field(default=None, description="Dirección")
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal_code: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    notes: Optional[str] = Field(default=None, description="Notas")
    anniversary: Optional[str] = Field(default=None, description="Aniversario")
    birthdate: Optional[str] = Field(default=None, description="Fecha de nacimiento")
    no_identity: Optional[bool] = Field(default=None, description="Sin identidad")
    is_vip: Optional[bool] = Field(default=None, description="Es VIP")
    is_blacklist: Optional[bool] = Field(
        default=None, description="Está en lista negra"
    )
    is_dnr: Optional[bool] = Field(default=None, description="No reenviar")
    tags: Optional[List[Dict[str, Any]]] = Field(default=None, description="Etiquetas")
    references: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Referencias"
    )
    custom: Optional[Dict[str, Any]] = Field(
        default=None, description="Campos personalizados"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    created_at: str = Field(..., description="Fecha de creación")
    is_owner_contact: bool = Field(..., description="Es contacto del propietario")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class GuaranteePolicyEmbedded(BaseModel):
    """Modelo para política de garantía embebida"""

    id: int = Field(..., description="ID de la política")
    is_active: bool = Field(..., description="Está activa")
    is_default: bool = Field(..., description="Es por defecto")
    name: str = Field(..., description="Nombre")
    description: Optional[str] = Field(default=None, description="Descripción")
    before_arrival_start: Optional[int] = Field(
        default=None, description="Inicio antes de llegada"
    )
    before_arrival_end: Optional[int] = Field(
        default=None, description="Fin antes de llegada"
    )
    type: Literal["Hold", "Guarantee", "FullDeposit"] = Field(..., description="Tipo")
    hold_limit: Optional[int] = Field(default=None, description="Límite de retención")
    deposit_type: Optional[str] = Field(default=None, description="Tipo de depósito")
    amount: Optional[str] = Field(default=None, description="Monto")
    include_tax: bool = Field(..., description="Incluye impuestos")
    include_fees: bool = Field(..., description="Incluye tarifas")
    include_travel_insurance: bool = Field(..., description="Incluye seguro de viaje")
    travel_insurance_with_first_payment: bool = Field(
        ..., description="Seguro con primer pago"
    )
    is_automatic_cancel: bool = Field(..., description="Cancelación automática")
    include_folio_charges: bool = Field(..., description="Incluye cargos del folio")
    has_payment_schedule: bool = Field(..., description="Tiene cronograma de pagos")
    priority: Optional[int] = Field(default=None, description="Prioridad")
    breakpoints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Puntos de quiebre"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class CancellationPolicyEmbedded(BaseModel):
    """Modelo para política de cancelación embebida"""

    id: int = Field(..., description="ID de la política")
    is_default: bool = Field(..., description="Es por defecto")
    is_active: bool = Field(..., description="Está activa")
    name: str = Field(..., description="Nombre")
    code: Optional[str] = Field(default=None, description="Código")
    charge_as: Literal["fee", "split"] = Field(..., description="Cobrar como")
    can_exceed_balance: bool = Field(..., description="Puede exceder balance")
    cancel_time: Optional[str] = Field(default=None, description="Hora de cancelación")
    cancel_timezone: Optional[str] = Field(
        default=None, description="Zona horaria de cancelación"
    )
    post_date: Literal["now", "checkin", "checkout"] = Field(
        ..., description="Fecha de publicación"
    )
    airbnb_type: Optional[str] = Field(default=None, description="Tipo Airbnb")
    marriott_type: Optional[str] = Field(default=None, description="Tipo Marriott")
    tripadvisor_type: Optional[str] = Field(
        default=None, description="Tipo TripAdvisor"
    )
    homeaway_type: Optional[str] = Field(default=None, description="Tipo HomeAway")
    breakpoints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Puntos de quiebre"
    )
    priority: Optional[int] = Field(default=None, description="Prioridad")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    date_group_id: Optional[int] = Field(
        default=None, description="ID del grupo de fecha"
    )
    date_range_type: Optional[str] = Field(
        default=None, description="Tipo de rango de fecha"
    )
    start_date: Optional[str] = Field(default=None, description="Fecha de inicio")
    end_date: Optional[str] = Field(default=None, description="Fecha de fin")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class UserEmbedded(BaseModel):
    """Modelo para usuario embebido en respuesta de reservación"""

    id: int = Field(..., description="ID del usuario")
    is_active: bool = Field(..., description="Está activo")
    name: str = Field(..., description="Nombre")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    email: Optional[str] = Field(default=None, description="Email")
    username: Optional[str] = Field(default=None, description="Nombre de usuario")
    role_id: Optional[int] = Field(default=None, description="ID del rol")
    team_id: Optional[int] = Field(default=None, description="ID del equipo")
    vendor_id: Optional[int] = Field(default=None, description="ID del proveedor")
    assignable: Optional[List[str]] = Field(default=None, description="Asignable")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class ReservationTypeEmbedded(BaseModel):
    """Modelo para tipo de reservación embebido"""

    id: int = Field(..., description="ID del tipo")
    name: str = Field(..., description="Nombre del sistema")
    public_name: str = Field(..., description="Nombre público")
    code: str = Field(..., description="Código")
    description: Optional[str] = Field(default=None, description="Descripción")
    is_active: bool = Field(..., description="Está activo")
    is_commissionable: bool = Field(..., description="Es comisionable")
    type_color: Optional[str] = Field(default=None, description="Color del tipo")
    charge_rates: Optional[bool] = Field(
        default=None, description="Cobrar tarifas", deprecated=True
    )
    charge_rent: Literal["owner", "guest", "none"] = Field(
        ..., description="Cobrar renta"
    )
    rent_earned: Literal["owner", "account", "auto"] = Field(
        ..., description="Renta ganada"
    )
    requires_agreement: bool = Field(..., description="Requiere acuerdo")
    require_payment: bool = Field(..., description="Requiere pago")
    cleaning_options_id: Optional[int] = Field(
        default=None, description="ID de opciones de limpieza"
    )
    realize_rates: Literal["nightly", "checkin", "checkout", "monthly"] = Field(
        ..., description="Realizar tarifas"
    )
    is_locked: bool = Field(..., description="Está bloqueado")
    send_portal_invited: bool = Field(..., description="Enviar invitación al portal")
    portal_reservation_breakdown: bool = Field(
        ..., description="Desglose de reserva en portal"
    )
    show_folio_transactions: bool = Field(
        ..., description="Mostrar transacciones del folio"
    )
    is_owner: bool = Field(..., description="Es propietario")
    schedule_type1: Optional[str] = Field(
        default=None, description="Tipo de programación 1"
    )
    schedule_percentage1: Optional[int] = Field(
        default=None, description="Porcentaje de programación 1"
    )
    schedule_type2: Optional[str] = Field(
        default=None, description="Tipo de programación 2"
    )
    schedule_percentage2: Optional[int] = Field(
        default=None, description="Porcentaje de programación 2"
    )
    owner_stay: bool = Field(..., description="Estadía del propietario")
    personal_use: bool = Field(..., description="Uso personal")
    auto_select: bool = Field(..., description="Selección automática")
    security_deposit_type: Optional[str] = Field(
        default=None, description="Tipo de depósito de seguridad"
    )
    defer_disbursement: bool = Field(..., description="Diferir desembolso")
    defer_disbursement_date: Optional[str] = Field(
        default=None, description="Fecha de desembolso diferido"
    )
    pos_default_allow: bool = Field(..., description="Permitir POS por defecto")
    pos_default_limit: Optional[str] = Field(
        default=None, description="Límite POS por defecto"
    )
    created_at: str = Field(..., description="Fecha de creación")
    created_by: str = Field(..., description="Creado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class RateTypeEmbedded(BaseModel):
    """Modelo para tipo de tarifa embebido"""

    id: int = Field(..., description="ID del tipo de tarifa")
    type: Optional[str] = Field(default=None, description="Tipo")
    code: Optional[str] = Field(default=None, description="Código")
    name: Optional[str] = Field(default=None, description="Nombre")
    is_auto_select: bool = Field(..., description="Selección automática")
    occupancy_pricing_by_type: bool = Field(
        ..., description="Precio por ocupación por tipo"
    )
    is_all_channels: bool = Field(..., description="Todos los canales")
    channel_ids: Optional[List[int]] = Field(default=None, description="IDs de canales")
    is_active: bool = Field(..., description="Está activo")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    parent_rate_id: Optional[int] = Field(
        default=None, description="ID de tarifa padre"
    )
    rent_type: Optional[str] = Field(default=None, description="Tipo de renta")
    rent_amount: Optional[str] = Field(default=None, description="Monto de renta")
    min_los_type: Optional[str] = Field(
        default=None, description="Tipo de estadía mínima"
    )
    min_los_amount: Optional[float] = Field(
        default=None, description="Cantidad de estadía mínima"
    )
    max_los_type: Optional[str] = Field(
        default=None, description="Tipo de estadía máxima"
    )
    max_los_amount: Optional[float] = Field(
        default=None, description="Cantidad de estadía máxima"
    )
    cta_override: bool = Field(..., description="Anulación CTA")
    cta: Optional[Dict[str, bool]] = Field(default=None, description="CTA")
    ctd_override: bool = Field(..., description="Anulación CTD")
    ctd: Optional[Dict[str, bool]] = Field(default=None, description="CTD")
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )


class ReservationFilters(BaseModel):
    """Filtros para reservas"""

    status: Optional[
        Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"]
    ] = Field(default=None, description="Estado")
    channel: Optional[str] = Field(default=None, description="Canal")
    property_id: Optional[str] = Field(default=None, description="ID de la propiedad")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
    guest_email: Optional[str] = Field(default=None, description="Email del huésped")
    booking_reference: Optional[str] = Field(
        default=None, description="Referencia de reserva"
    )
