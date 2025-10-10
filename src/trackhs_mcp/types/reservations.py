"""
Modelos Pydantic para Reservations de Track HS API
"""

from typing import Optional, Literal, List, Dict, Any, Union
from pydantic import BaseModel, Field
from .base import PaginationParams, SearchParams

class Guest(BaseModel):
    """Modelo de Guest"""
    id: int = Field(..., description="ID único del huésped")
    first_name: str = Field(..., description="Nombre del huésped")
    last_name: str = Field(..., description="Apellido del huésped")
    email: str = Field(..., description="Email del huésped")
    phone: Optional[str] = Field(default=None, description="Teléfono del huésped")
    nationality: Optional[str] = Field(default=None, description="Nacionalidad del huésped")
    document_type: Optional[str] = Field(default=None, description="Tipo de documento")
    document_number: Optional[str] = Field(default=None, description="Número de documento")

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

class Occupant(BaseModel):
    """Modelo de Occupant"""
    type_id: int = Field(..., description="ID del tipo de ocupante")
    name: str = Field(..., description="Nombre del ocupante")
    handle: str = Field(..., description="Handle del ocupante")
    quantity: int = Field(..., description="Cantidad")
    included: bool = Field(..., description="Si está incluido")
    extra_quantity: int = Field(..., description="Cantidad extra")
    rate_per_person_per_stay: str = Field(..., description="Tarifa por persona por estadía")
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
    display_as: Literal["itemize", "rent", "tax", "service"] = Field(..., description="Cómo mostrar")
    quantity: str = Field(..., description="Cantidad")
    unit_value: str = Field(..., description="Valor unitario")
    value: str = Field(..., description="Valor")

class Tax(BaseModel):
    """Modelo de Tax"""
    id: int = Field(..., description="ID del impuesto")
    name: str = Field(..., description="Nombre del impuesto")
    amount: str = Field(..., description="Monto del impuesto")

class GuestBreakdown(BaseModel):
    """Modelo de GuestBreakdown"""
    gross_rent: str = Field(..., description="Renta bruta")
    guest_gross_display_rent: str = Field(..., description="Renta bruta mostrada al huésped")
    discount: str = Field(..., description="Descuento")
    promo_value: str = Field(..., description="Valor promocional")
    discount_total: int = Field(..., description="Total de descuentos")
    net_rent: str = Field(..., description="Renta neta")
    guest_net_display_rent: str = Field(..., description="Renta neta mostrada al huésped")
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
    type: Literal["Hold", "Guarantee", "FullDeposit"] = Field(..., description="Tipo de política")
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
    breakpoints: List[CancellationBreakpoint] = Field(..., description="Puntos de quiebre")

class PaymentPlan(BaseModel):
    """Modelo de PaymentPlan"""
    date: str = Field(..., description="Fecha")
    amount: str = Field(..., description="Monto")

class TravelInsuranceProduct(BaseModel):
    """Modelo de TravelInsuranceProduct"""
    id: int = Field(..., description="ID del producto")
    status: Literal["optin", "funded", "cancelled"] = Field(..., description="Estado")
    type: Literal["Travel Insurance", "Master Cancel", "Damage Deposit"] = Field(..., description="Tipo")
    provider: str = Field(..., description="Proveedor")
    provider_id: int = Field(..., description="ID del proveedor")
    amount: str = Field(..., description="Monto")

class Reservation(BaseModel):
    """Modelo de Reservation"""
    id: int = Field(..., description="ID único de la reserva")
    alternates: Optional[List[str]] = Field(default=None, description="Alternativas")
    currency: str = Field(..., description="Moneda")
    unit_id: int = Field(..., description="ID de la unidad")
    is_unit_locked: bool = Field(..., description="Si la unidad está bloqueada")
    is_unit_assigned: bool = Field(..., description="Si la unidad está asignada")
    is_unit_type_locked: bool = Field(..., description="Si el tipo de unidad está bloqueado")
    unit_type_id: int = Field(..., description="ID del tipo de unidad")
    arrival_date: str = Field(..., description="Fecha de llegada")
    departure_date: str = Field(..., description="Fecha de salida")
    early_arrival: bool = Field(..., description="Llegada temprana")
    late_departure: bool = Field(..., description="Salida tardía")
    arrival_time: str = Field(..., description="Hora de llegada")
    departure_time: str = Field(..., description="Hora de salida")
    nights: int = Field(..., description="Noches")
    status: Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"] = Field(..., description="Estado")
    cancelled_at: Optional[str] = Field(default=None, description="Fecha de cancelación")
    occupants: List[Occupant] = Field(..., description="Ocupantes")
    security_deposit: Dict[str, str] = Field(..., description="Depósito de seguridad")
    updated_at: str = Field(..., description="Fecha de actualización")
    created_at: str = Field(..., description="Fecha de creación")
    booked_at: str = Field(..., description="Fecha de reserva")
    guest_breakdown: GuestBreakdown = Field(..., description="Desglose del huésped")
    type: Dict[str, Union[int, str]] = Field(..., description="Tipo")
    guarantee_policy: GuaranteePolicy = Field(..., description="Política de garantía")
    cancellation_policy: CancellationPolicy = Field(..., description="Política de cancelación")
    payment_plan: List[PaymentPlan] = Field(..., description="Plan de pagos")
    rate_type: Dict[str, Union[int, str]] = Field(..., description="Tipo de tarifa")
    travel_insurance_products: List[TravelInsuranceProduct] = Field(..., description="Productos de seguro de viaje")
    _embedded: Dict[str, Any] = Field(..., description="Datos embebidos")
    _links: Dict[str, Dict[str, str]] = Field(..., description="Enlaces")

class SearchReservationsParams(PaginationParams, SearchParams):
    """Parámetros para buscar reservas"""
    sort_column: Optional[Literal["name", "status", "altConf", "agreementStatus", "type", "guest", "guests", "unit", "units", "checkin", "checkout", "nights"]] = Field(default="name", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(default="asc", description="Dirección de ordenamiento")
    tags: Optional[str] = Field(default=None, description="Tags")
    node_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del nodo")
    unit_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID de la unidad")
    reservation_type_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del tipo de reserva")
    contact_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del contacto")
    travel_agent_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del agente de viajes")
    campaign_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID de la campaña")
    user_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del usuario")
    unit_type_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del tipo de unidad")
    rate_type_id: Optional[Union[int, List[int]]] = Field(default=None, description="ID del tipo de tarifa")
    booked_start: Optional[str] = Field(default=None, description="Fecha de inicio de reserva")
    booked_end: Optional[str] = Field(default=None, description="Fecha de fin de reserva")
    arrival_start: Optional[str] = Field(default=None, description="Fecha de inicio de llegada")
    arrival_end: Optional[str] = Field(default=None, description="Fecha de fin de llegada")
    departure_start: Optional[str] = Field(default=None, description="Fecha de inicio de salida")
    departure_end: Optional[str] = Field(default=None, description="Fecha de fin de salida")
    in_house_today: Optional[Literal[0, 1]] = Field(default=None, description="En casa hoy")
    status: Optional[Union[Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"], List[str]]] = Field(default=None, description="Estado")
    group_id: Optional[int] = Field(default=None, description="ID del grupo")
    checkin_office_id: Optional[int] = Field(default=None, description="ID de la oficina de check-in")

class SearchReservationsResponse(BaseModel):
    """Respuesta de búsqueda de reservas"""
    _embedded: Dict[str, List[Reservation]] = Field(..., description="Datos embebidos")
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    _links: Dict[str, Dict[str, str]] = Field(..., description="Enlaces")

class GetReservationParams(BaseModel):
    """Parámetros para obtener una reserva específica"""
    reservation_id: int = Field(..., description="ID de la reserva")

class ReservationResponse(BaseModel):
    """Respuesta de una reserva específica"""
    data: Reservation = Field(..., description="Datos de la reserva")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")

class ReservationFilters(BaseModel):
    """Filtros para reservas"""
    status: Optional[Literal["Hold", "Confirmed", "Checked Out", "Checked In", "Cancelled"]] = Field(default=None, description="Estado")
    channel: Optional[str] = Field(default=None, description="Canal")
    property_id: Optional[str] = Field(default=None, description="ID de la propiedad")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
    guest_email: Optional[str] = Field(default=None, description="Email del huésped")
    booking_reference: Optional[str] = Field(default=None, description="Referencia de reserva")
