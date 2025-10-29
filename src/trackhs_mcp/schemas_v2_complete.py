"""
Schema completo para Get Reservation V2 API según documentación oficial
Incluye todos los campos y estructuras de la API V2 de TrackHS
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

# =============================================================================
# SCHEMAS DETALLADOS PARA API V2
# =============================================================================


class OccupantDetail(BaseModel):
    """Detalles de ocupante según API V2"""

    typeId: Optional[int] = Field(default=None, description="ID del tipo de ocupante")
    name: Optional[str] = Field(default=None, description="Nombre del tipo de ocupante")
    handle: Optional[str] = Field(default=None, description="Handle del ocupante")
    quantity: Optional[float] = Field(default=None, description="Cantidad de ocupantes")
    included: Optional[bool] = Field(
        default=None, description="Si están incluidos en el precio"
    )
    extraQuantity: Optional[float] = Field(
        default=None, description="Cantidad extra permitida"
    )
    ratePerPersonPerStay: Optional[str] = Field(
        default=None, description="Tarifa por persona por estadía"
    )
    ratePerStay: Optional[str] = Field(default=None, description="Tarifa por estadía")


class SecurityDepositDetail(BaseModel):
    """Detalles del depósito de seguridad"""

    required: Optional[str] = Field(default=None, description="Monto total requerido")
    remaining: Optional[float] = Field(default=None, description="Monto restante")


class RateDetail(BaseModel):
    """Detalles de tarifa diaria"""

    date: Optional[str] = Field(default=None, description="Fecha en formato ISO 8601")
    rate: Optional[str] = Field(default=None, description="Tarifa en formato numérico")
    nights: Optional[int] = Field(default=None, description="Número de noches")
    isQuoted: Optional[bool] = Field(default=None, description="Si es cotizada")


class GuestFeeDetail(BaseModel):
    """Detalles de tarifa del huésped"""

    id: Optional[str] = Field(default=None, description="ID de la tarifa")
    name: Optional[str] = Field(default=None, description="Nombre de la tarifa")
    displayAs: Optional[str] = Field(
        default=None, description="Cómo mostrar (itemize, rent, tax, service)"
    )
    quantity: Optional[str] = Field(default=None, description="Cantidad")
    unitValue: Optional[str] = Field(default=None, description="Valor por unidad")
    value: Optional[str] = Field(default=None, description="Valor total")


class TaxDetail(BaseModel):
    """Detalles de impuesto"""

    id: Optional[int] = Field(default=None, description="ID del impuesto")
    name: Optional[str] = Field(default=None, description="Nombre del impuesto")
    amount: Optional[str] = Field(default=None, description="Monto del impuesto")


class GuestBreakdownDetail(BaseModel):
    """Desglose financiero completo del huésped"""

    grossRent: Optional[str] = Field(default=None, description="Renta bruta")
    guestGrossDisplayRent: Optional[str] = Field(
        default=None, description="Renta bruta mostrada al huésped"
    )
    discount: Optional[str] = Field(default=None, description="Descuento total")
    promoValue: Optional[str] = Field(default=None, description="Valor promocional")
    discountTotal: Optional[float] = Field(
        default=None, description="Total de descuentos"
    )
    netRent: Optional[str] = Field(default=None, description="Renta neta")
    guestNetDisplayRent: Optional[str] = Field(
        default=None, description="Renta neta mostrada al huésped"
    )
    actualAdr: Optional[str] = Field(default=None, description="ADR real")
    guestAdr: Optional[str] = Field(default=None, description="ADR del huésped")
    totalGuestFees: Optional[str] = Field(
        default=None, description="Total de tarifas del huésped"
    )
    totalRentFees: Optional[str] = Field(
        default=None, description="Total de tarifas de renta"
    )
    totalItemizedFees: Optional[str] = Field(
        default=None, description="Total de tarifas detalladas"
    )
    totalTaxFees: Optional[str] = Field(
        default=None, description="Total de tarifas de impuestos"
    )
    totalServiceFees: Optional[str] = Field(
        default=None, description="Total de tarifas de servicio"
    )
    folioCharges: Optional[str] = Field(default=None, description="Cargos del folio")
    subtotal: Optional[str] = Field(default=None, description="Subtotal")
    guestSubtotal: Optional[str] = Field(
        default=None, description="Subtotal del huésped"
    )
    totalTaxes: Optional[str] = Field(default=None, description="Total de impuestos")
    totalGuestTaxes: Optional[str] = Field(
        default=None, description="Total de impuestos del huésped"
    )
    total: Optional[str] = Field(default=None, description="Total")
    grandTotal: Optional[str] = Field(default=None, description="Gran total")
    netPayments: Optional[str] = Field(default=None, description="Pagos netos")
    payments: Optional[str] = Field(default=None, description="Pagos")
    refunds: Optional[str] = Field(default=None, description="Reembolsos")
    netTransfers: Optional[str] = Field(
        default=None, description="Transferencias netas"
    )
    balance: Optional[str] = Field(default=None, description="Balance")
    rates: Optional[List[RateDetail]] = Field(
        default=None, description="Tarifas diarias"
    )
    guestFees: Optional[List[GuestFeeDetail]] = Field(
        default=None, description="Tarifas del huésped"
    )
    taxes: Optional[List[TaxDetail]] = Field(default=None, description="Impuestos")


class OwnerFeeDetail(BaseModel):
    """Detalles de tarifa del propietario"""

    id: Optional[str] = Field(default=None, description="ID de la tarifa")
    name: Optional[str] = Field(default=None, description="Nombre de la tarifa")
    displayAs: Optional[str] = Field(default=None, description="Cómo mostrar")
    quantity: Optional[str] = Field(default=None, description="Cantidad")
    unitValue: Optional[str] = Field(default=None, description="Valor por unidad")
    value: Optional[str] = Field(default=None, description="Valor total")


class OwnerBreakdownDetail(BaseModel):
    """Desglose financiero completo del propietario"""

    grossRent: Optional[str] = Field(
        default=None, description="Renta bruta del propietario"
    )
    feeRevenue: Optional[str] = Field(default=None, description="Ingresos por tarifas")
    grossRevenue: Optional[str] = Field(default=None, description="Ingresos brutos")
    managerCommission: Optional[str] = Field(
        default=None, description="Comisión del manager"
    )
    agentCommission: Optional[str] = Field(
        default=None, description="Comisión del agente"
    )
    netRevenue: Optional[str] = Field(default=None, description="Ingresos netos")
    ownerFees: Optional[List[OwnerFeeDetail]] = Field(
        default=None, description="Tarifas del propietario"
    )


class PaymentPlanDetail(BaseModel):
    """Detalles del plan de pago"""

    date: Optional[str] = Field(default=None, description="Fecha en formato ISO 8601")
    amount: Optional[str] = Field(default=None, description="Monto en formato numérico")


class RateTypeDetail(BaseModel):
    """Detalles del tipo de tarifa"""

    id: Optional[int] = Field(default=None, description="ID del tipo de tarifa")
    name: Optional[str] = Field(default=None, description="Nombre del tipo de tarifa")
    code: Optional[str] = Field(default=None, description="Código del tipo de tarifa")


class TravelInsuranceProduct(BaseModel):
    """Producto de seguro de viaje"""

    id: Optional[int] = Field(default=None, description="ID del producto")
    status: Optional[str] = Field(
        default=None, description="Estado (optin, funded, cancelled)"
    )
    type: Optional[str] = Field(
        default=None,
        description="Tipo (Travel Insurance, Master Cancel, Damage Deposit)",
    )
    provider: Optional[str] = Field(default=None, description="Proveedor")
    providerId: Optional[int] = Field(default=None, description="ID del proveedor")
    amount: Optional[str] = Field(default=None, description="Monto")


class UnitEmbedded(BaseModel):
    """Unidad embebida con detalles completos"""

    id: Optional[int] = Field(default=None, description="ID de la unidad")
    name: Optional[str] = Field(default=None, description="Nombre de la unidad")
    shortName: Optional[str] = Field(default=None, description="Nombre corto")
    unitCode: Optional[str] = Field(default=None, description="Código de la unidad")
    headline: Optional[str] = Field(default=None, description="Título")
    shortDescription: Optional[str] = Field(
        default=None, description="Descripción corta"
    )
    longDescription: Optional[str] = Field(
        default=None, description="Descripción larga"
    )
    houseRules: Optional[str] = Field(default=None, description="Reglas de la casa")
    nodeId: Optional[int] = Field(default=None, description="ID del nodo")
    timezone: Optional[str] = Field(default=None, description="Zona horaria")
    checkinTime: Optional[str] = Field(default=None, description="Hora de check-in")
    hasEarlyCheckin: Optional[bool] = Field(
        default=None, description="Permite check-in temprano"
    )
    earlyCheckinTime: Optional[str] = Field(
        default=None, description="Hora de check-in temprano"
    )
    checkoutTime: Optional[str] = Field(default=None, description="Hora de check-out")
    hasLateCheckout: Optional[bool] = Field(
        default=None, description="Permite check-out tardío"
    )
    lateCheckoutTime: Optional[str] = Field(
        default=None, description="Hora de check-out tardío"
    )
    minBookingWindow: Optional[int] = Field(
        default=None, description="Ventana mínima de reserva"
    )
    maxBookingWindow: Optional[int] = Field(
        default=None, description="Ventana máxima de reserva"
    )
    website: Optional[str] = Field(default=None, description="Sitio web")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    streetAddress: Optional[str] = Field(default=None, description="Dirección")
    extendedAddress: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postalCode: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    longitude: Optional[float] = Field(default=None, description="Longitud")
    latitude: Optional[float] = Field(default=None, description="Latitud")
    petsFriendly: Optional[bool] = Field(default=None, description="Permite mascotas")
    maxPets: Optional[int] = Field(default=None, description="Máximo de mascotas")
    eventsAllowed: Optional[bool] = Field(default=None, description="Permite eventos")
    smokingAllowed: Optional[bool] = Field(default=None, description="Permite fumar")
    childrenAllowed: Optional[bool] = Field(default=None, description="Permite niños")
    minimumAgeLimit: Optional[int] = Field(default=None, description="Edad mínima")
    isAccessible: Optional[bool] = Field(default=None, description="Es accesible")
    area: Optional[float] = Field(default=None, description="Área")
    floors: Optional[float] = Field(default=None, description="Pisos")
    maxOccupancy: Optional[int] = Field(default=None, description="Ocupación máxima")
    securityDeposit: Optional[str] = Field(
        default=None, description="Depósito de seguridad"
    )
    bedrooms: Optional[int] = Field(default=None, description="Dormitorios")
    fullBathrooms: Optional[int] = Field(default=None, description="Baños completos")
    threeQuarterBathrooms: Optional[int] = Field(
        default=None, description="Baños de 3/4"
    )
    halfBathrooms: Optional[int] = Field(default=None, description="Medios baños")
    isActive: Optional[bool] = Field(default=None, description="Es activa")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")


class ContactEmbedded(BaseModel):
    """Contacto embebido con detalles completos"""

    id: Optional[int] = Field(default=None, description="ID del contacto")
    firstName: Optional[str] = Field(default=None, description="Nombre")
    lastName: Optional[str] = Field(default=None, description="Apellido")
    name: Optional[str] = Field(default=None, description="Nombre completo")
    primaryEmail: Optional[str] = Field(default=None, description="Email principal")
    secondaryEmail: Optional[str] = Field(default=None, description="Email secundario")
    homePhone: Optional[str] = Field(default=None, description="Teléfono de casa")
    cellPhone: Optional[str] = Field(default=None, description="Teléfono celular")
    workPhone: Optional[str] = Field(default=None, description="Teléfono de trabajo")
    otherPhone: Optional[str] = Field(default=None, description="Otro teléfono")
    fax: Optional[str] = Field(default=None, description="Fax")
    streetAddress: Optional[str] = Field(default=None, description="Dirección")
    extendedAddress: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postalCode: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    notes: Optional[str] = Field(default=None, description="Notas")
    anniversary: Optional[str] = Field(default=None, description="Aniversario")
    birthdate: Optional[str] = Field(default=None, description="Fecha de nacimiento")
    noIdentity: Optional[bool] = Field(default=None, description="Sin identidad")
    isVip: Optional[bool] = Field(default=None, description="Es VIP")
    isBlacklist: Optional[bool] = Field(default=None, description="Está en lista negra")
    isDNR: Optional[bool] = Field(default=None, description="Es DNR")
    isOwnerContact: Optional[bool] = Field(
        default=None, description="Es contacto del propietario"
    )
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")


class EmbeddedData(BaseModel):
    """Datos embebidos completos"""

    unit: Optional[UnitEmbedded] = Field(
        default=None, description="Información de la unidad"
    )
    contact: Optional[ContactEmbedded] = Field(
        default=None, description="Información del contacto"
    )
    guaranteePolicy: Optional[Dict[str, Any]] = Field(
        default=None, description="Política de garantía"
    )
    cancellationPolicy: Optional[Dict[str, Any]] = Field(
        default=None, description="Política de cancelación"
    )
    user: Optional[Dict[str, Any]] = Field(
        default=None, description="Información del usuario"
    )
    type: Optional[Dict[str, Any]] = Field(default=None, description="Tipo de reserva")
    rateType: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de tarifa"
    )


class LinksData(BaseModel):
    """Enlaces relacionados"""

    self: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a sí mismo"
    )
    logs: Optional[Dict[str, str]] = Field(default=None, description="Enlace a logs")
    notes: Optional[Dict[str, str]] = Field(default=None, description="Enlace a notas")
    fees: Optional[Dict[str, str]] = Field(default=None, description="Enlace a tarifas")
    checkin: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a check-in"
    )
    cancel: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a cancelar"
    )
    tags: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a etiquetas"
    )
    rates: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a tarifas"
    )
    discount: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a descuentos"
    )


class ReservationDetailOutputV2(BaseModel):
    """Schema completo para Get Reservation V2 API según documentación oficial"""

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

    # Ocupantes con detalles completos
    occupants: Optional[List[OccupantDetail]] = Field(
        default=None, description="Lista de ocupantes"
    )

    # Depósito de seguridad con detalles
    securityDeposit: Optional[SecurityDepositDetail] = Field(
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

    # Desglose financiero del huésped con detalles completos
    guestBreakdown: Optional[GuestBreakdownDetail] = Field(
        default=None, description="Desglose financiero del huésped"
    )

    # Desglose financiero del propietario con detalles completos
    ownerBreakdown: Optional[OwnerBreakdownDetail] = Field(
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

    # Plan de pago con detalles
    paymentPlan: Optional[List[PaymentPlanDetail]] = Field(
        default=None, description="Plan de pago"
    )

    # Información de tarifas con detalles
    rateType: Optional[RateTypeDetail] = Field(
        default=None, description="Tipo de tarifa"
    )

    # Productos de seguro de viaje con detalles
    travelInsuranceProducts: Optional[List[TravelInsuranceProduct]] = Field(
        default=None, description="Productos de seguro de viaje"
    )

    # Información embebida completa
    embedded: Optional[EmbeddedData] = Field(
        default=None, alias="_embedded", description="Datos embebidos completos"
    )

    # Enlaces completos
    links: Optional[LinksData] = Field(
        default=None, alias="_links", description="Enlaces relacionados"
    )

    # Campos adicionales para compatibilidad
    additional_data: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Datos adicionales"
    )
