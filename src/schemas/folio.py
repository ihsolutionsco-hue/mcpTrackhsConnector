"""
Schemas para folios financieros según documentación oficial de TrackHS
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .base import BaseSchema


class FolioLinks(BaseModel):
    """Enlaces del folio"""

    self: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace a sí mismo"
    )
    logs: Optional[Dict[str, str]] = Field(default=None, description="Enlace a logs")


class ContactResponse(BaseModel):
    """Respuesta de contacto según documentación oficial"""

    id: int = Field(description="ID del contacto")
    firstName: Optional[str] = Field(default=None, description="Nombre")
    lastName: Optional[str] = Field(default=None, description="Apellido")
    primaryEmail: Optional[str] = Field(default=None, description="Email principal")
    secondaryEmail: Optional[str] = Field(default=None, description="Email secundario")
    homePhone: Optional[str] = Field(default=None, description="Teléfono de casa")
    cellPhone: Optional[str] = Field(default=None, description="Teléfono celular")
    workPhone: Optional[str] = Field(default=None, description="Teléfono de trabajo")
    otherPhone: Optional[str] = Field(default=None, description="Otro teléfono")
    fax: Optional[str] = Field(default=None, description="Fax")
    streetAddress: Optional[str] = Field(default=None, description="Dirección")
    country: Optional[str] = Field(default=None, description="País (código ISO 2)")
    postalCode: Optional[str] = Field(default=None, description="Código postal")
    region: Optional[str] = Field(default=None, description="Región")
    locality: Optional[str] = Field(default=None, description="Localidad")
    extendedAddress: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    notes: Optional[str] = Field(default=None, description="Notas")
    anniversary: Optional[str] = Field(default=None, description="Aniversario")
    birthdate: Optional[str] = Field(default=None, description="Fecha de nacimiento")
    isVip: Optional[bool] = Field(default=None, description="Es VIP")
    isBlacklist: Optional[bool] = Field(default=None, description="Está en lista negra")
    taxId: Optional[str] = Field(default=None, description="ID fiscal")
    noIdentity: Optional[bool] = Field(default=None, description="Sin identidad")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")


class CompanyResponse(BaseModel):
    """Respuesta de empresa según documentación oficial"""

    id: int = Field(description="ID de la empresa")
    type: str = Field(description="Tipo de empresa")
    isActive: Optional[bool] = Field(default=None, description="Está activa")
    name: str = Field(description="Nombre de la empresa")
    streetAddress: Optional[str] = Field(default=None, description="Dirección")
    extendedAddress: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    taxType: Optional[str] = Field(default=None, description="Tipo de impuesto")
    taxName: Optional[str] = Field(default=None, description="Nombre fiscal")
    taxId: Optional[str] = Field(default=None, description="ID fiscal")
    notes: Optional[str] = Field(default=None, description="Notas")
    website: Optional[str] = Field(default=None, description="Sitio web")
    email: Optional[str] = Field(default=None, description="Email")
    fax: Optional[str] = Field(default=None, description="Fax")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")


class FolioRuleResponse(BaseModel):
    """Respuesta de regla de folio según documentación oficial"""

    id: int = Field(description="ID de la regla")
    name: str = Field(description="Nombre de la regla")
    code: str = Field(description="Código de la regla")
    isActive: bool = Field(description="Está activa")
    type: str = Field(description="Tipo de regla")
    percentAmount: Optional[float] = Field(
        default=None, description="Cantidad porcentual"
    )
    breakdownRentMode: Optional[str] = Field(
        default=None, description="Modo de desglose de renta"
    )
    breakdownRentIncludeTax: Optional[bool] = Field(
        default=None, description="Renta incluye impuestos"
    )
    breakdownRentPercent: Optional[float] = Field(
        default=None, description="Porcentaje de renta"
    )
    breakdownRentNights: Optional[int] = Field(
        default=None, description="Noches de renta"
    )
    breakdownFeeMode: Optional[str] = Field(
        default=None, description="Modo de desglose de tarifas"
    )
    breakdownFeeIncludeTax: Optional[bool] = Field(
        default=None, description="Tarifas incluyen impuestos"
    )
    breakdownFeePercent: Optional[float] = Field(
        default=None, description="Porcentaje de tarifas"
    )
    breakdownChargesMode: Optional[str] = Field(
        default=None, description="Modo de desglose de cargos"
    )
    breakdownChargesIncludeTax: Optional[bool] = Field(
        default=None, description="Cargos incluyen impuestos"
    )
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")


class FolioRuleMapping(BaseModel):
    """Mapeo de regla de folio según documentación oficial"""

    id: int = Field(description="ID del mapeo")
    ruleId: int = Field(description="ID de la regla")
    startDate: Optional[str] = Field(default=None, description="Fecha de inicio")
    endDate: Optional[str] = Field(default=None, description="Fecha de fin")
    minNights: Optional[int] = Field(default=None, description="Noches mínimas")
    maxNights: Optional[int] = Field(default=None, description="Noches máximas")
    maxSpend: Optional[float] = Field(default=None, description="Gasto máximo")
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")
    rule: Optional[FolioRuleResponse] = Field(
        default=None, description="Regla asociada"
    )


class FolioEmbedded(BaseModel):
    """Datos embebidos del folio según documentación oficial"""

    contact: Optional[ContactResponse] = Field(default=None, description="Contacto")
    travelAgent: Optional[CompanyResponse] = Field(
        default=None, description="Agente de viajes"
    )
    company: Optional[CompanyResponse] = Field(default=None, description="Empresa")
    masterFolioRule: Optional[FolioRuleMapping] = Field(
        default=None, description="Regla de folio maestro"
    )
    masterFolio: Optional[Dict[str, Any]] = Field(
        default=None, description="Folio maestro"
    )


class FolioResponse(BaseModel):
    """Respuesta de folio según documentación oficial de TrackHS"""

    # Campos básicos requeridos
    id: int = Field(description="ID del folio")
    status: str = Field(description="Estado del folio (open/closed)")

    # Campos opcionales según tipo de folio
    type: Optional[str] = Field(
        default=None, description="Tipo de folio (guest/master)"
    )
    currentBalance: Optional[float] = Field(default=None, description="Balance actual")
    realizedBalance: Optional[float] = Field(
        default=None, description="Balance realizado"
    )
    closedDate: Optional[str] = Field(default=None, description="Fecha de cierre")
    endDate: Optional[str] = Field(default=None, description="Fecha de fin")
    startDate: Optional[str] = Field(default=None, description="Fecha de inicio")
    taxEmpty: Optional[bool] = Field(default=None, description="Exento de impuestos")
    companyId: Optional[int] = Field(default=None, description="ID de la empresa")
    contactId: Optional[int] = Field(default=None, description="ID del contacto")

    # Campos específicos de reserva
    reservationId: Optional[int] = Field(default=None, description="ID de la reserva")
    name: Optional[str] = Field(default=None, description="Nombre")
    checkInDate: Optional[str] = Field(default=None, description="Fecha de check-in")
    checkOutDate: Optional[str] = Field(default=None, description="Fecha de check-out")
    hasException: Optional[bool] = Field(default=None, description="Tiene excepción")
    exceptionMessage: Optional[str] = Field(
        default=None, description="Mensaje de excepción"
    )
    travelAgentId: Optional[int] = Field(
        default=None, description="ID del agente de viajes"
    )

    # Campos de comisiones
    agentCommission: Optional[float] = Field(
        default=None, description="Comisión del agente"
    )
    ownerCommission: Optional[float] = Field(
        default=None, description="Comisión del propietario"
    )
    ownerRevenue: Optional[float] = Field(
        default=None, description="Ingresos del propietario"
    )

    # Campos de folio maestro
    masterFolioId: Optional[int] = Field(
        default=None, description="ID del folio maestro"
    )
    masterFolioRuleId: Optional[int] = Field(
        default=None, description="ID de la regla del folio maestro"
    )

    # Campos de auditoría
    createdAt: Optional[str] = Field(default=None, description="Fecha de creación")
    updatedAt: Optional[str] = Field(default=None, description="Fecha de actualización")
    createdBy: Optional[str] = Field(default=None, description="Creado por")
    updatedBy: Optional[str] = Field(default=None, description="Actualizado por")

    # Enlaces y datos embebidos
    links: Optional[FolioLinks] = Field(
        default=None, description="Enlaces", alias="_links"
    )
    embedded: Optional[FolioEmbedded] = Field(
        default=None, description="Datos embebidos", alias="_embedded"
    )
