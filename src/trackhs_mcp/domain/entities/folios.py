"""
Modelos Pydantic para Folios de Track HS API
Basado en la especificación completa de la API Get Folio
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Tag(BaseModel):
    """Modelo de Tag para folios y contactos"""

    id: int = Field(..., description="ID del tag")
    name: str = Field(..., description="Nombre del tag")


class Contact(BaseModel):
    """Modelo de Contact embebido en folio"""

    id: int = Field(..., description="ID del contacto")
    first_name: str = Field(..., alias="firstName", description="Nombre del contacto")
    last_name: str = Field(..., alias="lastName", description="Apellido del contacto")
    primary_email: Optional[str] = Field(
        default=None, alias="primaryEmail", description="Email principal"
    )
    secondary_email: Optional[str] = Field(
        default=None, alias="secondaryEmail", description="Email secundario"
    )
    home_phone: Optional[str] = Field(
        default=None, alias="homePhone", description="Teléfono de casa"
    )
    cell_phone: Optional[str] = Field(
        default=None, alias="cellPhone", description="Teléfono celular"
    )
    work_phone: Optional[str] = Field(
        default=None, alias="workPhone", description="Teléfono de trabajo"
    )
    other_phone: Optional[str] = Field(
        default=None, alias="otherPhone", description="Otro teléfono"
    )
    fax: Optional[str] = Field(default=None, description="Fax")
    street_address: Optional[str] = Field(
        default=None, alias="streetAddress", description="Dirección"
    )
    country: Optional[str] = Field(default=None, description="País (ISO 2 chars)")
    postal_code: Optional[str] = Field(
        default=None, alias="postalCode", description="Código postal"
    )
    region: Optional[str] = Field(default=None, description="Región")
    locality: Optional[str] = Field(default=None, description="Localidad")
    extended_address: Optional[str] = Field(
        default=None, alias="extendedAddress", description="Dirección extendida"
    )
    notes: Optional[str] = Field(default=None, description="Notas")
    anniversary: Optional[str] = Field(default=None, description="Aniversario (MM-DD)")
    birthdate: Optional[str] = Field(
        default=None, description="Fecha de nacimiento (MM-DD)"
    )
    is_vip: Optional[bool] = Field(default=None, alias="isVip", description="Es VIP")
    is_blacklist: Optional[bool] = Field(
        default=None, alias="isBlacklist", description="Está en lista negra"
    )
    tax_id: Optional[str] = Field(default=None, alias="taxId", description="ID fiscal")
    no_identity: Optional[bool] = Field(
        default=None, alias="noIdentity", description="Sin información de identidad"
    )
    tags: Optional[List[Tag]] = Field(default=None, description="Tags del contacto")
    custom_values: Optional[Dict[str, Any]] = Field(
        default=None, alias="customValues", description="Valores personalizados"
    )
    created_at: Optional[str] = Field(
        default=None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        default=None, alias="updatedAt", description="Fecha de actualización"
    )
    created_by: Optional[str] = Field(
        default=None, alias="createdBy", description="Creado por"
    )
    updated_by: Optional[str] = Field(
        default=None, alias="updatedBy", description="Actualizado por"
    )


class Company(BaseModel):
    """Modelo de Company embebido en folio"""

    id: int = Field(..., description="ID de la compañía")
    type: Literal["company", "agent", "vendor", "owner"] = Field(
        ..., description="Tipo de compañía"
    )
    name: str = Field(..., description="Nombre de la compañía")
    is_active: Optional[bool] = Field(
        default=None, alias="isActive", description="Está activa"
    )
    street_address: Optional[str] = Field(
        default=None, alias="streetAddress", description="Dirección"
    )
    extended_address: Optional[str] = Field(
        default=None, alias="extendedAddress", description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País (ISO 2 chars)")
    tax_type: Optional[str] = Field(
        default=None, alias="taxType", description="Tipo de impuesto"
    )
    tax_name: Optional[str] = Field(
        default=None, alias="taxName", description="Nombre fiscal"
    )
    tax_id: Optional[str] = Field(default=None, alias="taxId", description="ID fiscal")
    email: Optional[str] = Field(default=None, description="Email")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    fax: Optional[str] = Field(default=None, description="Fax")
    website: Optional[str] = Field(default=None, description="Sitio web")
    notes: Optional[str] = Field(default=None, description="Notas")
    tags: Optional[List[Tag]] = Field(default=None, description="Tags de la compañía")
    created_at: Optional[str] = Field(
        default=None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        default=None, alias="updatedAt", description="Fecha de actualización"
    )
    created_by: Optional[str] = Field(
        default=None, alias="createdBy", description="Creado por"
    )
    updated_by: Optional[str] = Field(
        default=None, alias="updatedBy", description="Actualizado por"
    )


class FolioRule(BaseModel):
    """Modelo de Folio Rule embebido en MasterFolioRule"""

    id: int = Field(..., description="ID de la regla")
    name: str = Field(..., description="Nombre de la regla")
    code: str = Field(..., description="Código de la regla")
    is_active: bool = Field(..., alias="isActive", description="Está activa")
    type: Literal["percent", "breakdown"] = Field(..., description="Tipo de regla")
    percent_amount: Optional[float] = Field(
        default=None, alias="percentAmount", description="Cantidad porcentual"
    )
    breakdown_rent_mode: Optional[Literal["percent", "nights"]] = Field(
        default=None, alias="breakdownRentMode", description="Modo de renta"
    )
    breakdown_rent_include_tax: Optional[bool] = Field(
        default=None,
        alias="breakdownRentIncludeTax",
        description="Renta incluye impuestos",
    )
    breakdown_rent_percent: Optional[float] = Field(
        default=None, alias="breakdownRentPercent", description="Porcentaje de renta"
    )
    breakdown_rent_nights: Optional[int] = Field(
        default=None, alias="breakdownRentNights", description="Noches de renta"
    )
    breakdown_fee_mode: Optional[Literal["percent", "required"]] = Field(
        default=None, alias="breakdownFeeMode", description="Modo de tarifa"
    )
    breakdown_fee_include_tax: Optional[bool] = Field(
        default=None,
        alias="breakdownFeeIncludeTax",
        description="Tarifa incluye impuestos",
    )
    breakdown_fee_percent: Optional[float] = Field(
        default=None, alias="breakdownFeePercent", description="Porcentaje de tarifa"
    )
    breakdown_charges_mode: Optional[Literal["percent", "required"]] = Field(
        default=None, alias="breakdownChargesMode", description="Modo de cargos"
    )
    breakdown_charges_include_tax: Optional[bool] = Field(
        default=None,
        alias="breakdownChargesIncludeTax",
        description="Cargos incluyen impuestos",
    )
    created_at: Optional[str] = Field(
        default=None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        default=None, alias="updatedAt", description="Fecha de actualización"
    )
    created_by: Optional[str] = Field(
        default=None, alias="createdBy", description="Creado por"
    )
    updated_by: Optional[str] = Field(
        default=None, alias="updatedBy", description="Actualizado por"
    )


class MasterFolioRule(BaseModel):
    """Modelo de Master Folio Rule embebido en folio"""

    id: int = Field(..., description="ID del mapeo de regla")
    rule_id: int = Field(..., alias="ruleId", description="ID de la regla")
    start_date: Optional[str] = Field(
        default=None, alias="startDate", description="Fecha de inicio"
    )
    end_date: Optional[str] = Field(
        default=None, alias="endDate", description="Fecha de fin"
    )
    min_nights: Optional[int] = Field(
        default=None, alias="minNights", description="Noches mínimas"
    )
    max_nights: Optional[int] = Field(
        default=None, alias="maxNights", description="Noches máximas"
    )
    max_spend: Optional[float] = Field(
        default=None, alias="maxSpend", description="Gasto máximo"
    )
    created_at: Optional[str] = Field(
        default=None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        default=None, alias="updatedAt", description="Fecha de actualización"
    )
    created_by: Optional[str] = Field(
        default=None, alias="createdBy", description="Creado por"
    )
    updated_by: Optional[str] = Field(
        default=None, alias="updatedBy", description="Actualizado por"
    )
    rule: Optional[FolioRule] = Field(default=None, description="Regla embebida")


class FolioLinks(BaseModel):
    """Modelo de _links en folio"""

    self: Optional[Dict[str, str]] = Field(default=None, description="Link a sí mismo")
    logs: Optional[Dict[str, str]] = Field(default=None, description="Link a logs")


class FolioEmbedded(BaseModel):
    """Modelo de _embedded en folio"""

    contact: Optional[Contact] = Field(default=None, description="Contacto embebido")
    travel_agent: Optional[Company] = Field(
        default=None, alias="travelAgent", description="Agente de viajes embebido"
    )
    company: Optional[Company] = Field(default=None, description="Compañía embebida")
    master_folio_rule: Optional[MasterFolioRule] = Field(
        default=None, alias="masterFolioRule", description="Regla de folio maestro"
    )
    master_folio: Optional[Dict[str, Any]] = Field(
        default=None, alias="masterFolio", description="Folio maestro"
    )


class Folio(BaseModel):
    """Modelo principal de Folio"""

    model_config = {"populate_by_name": True}

    # Campos requeridos
    id: int = Field(..., description="ID único del folio")
    status: Literal["open", "closed"] = Field(..., description="Estado del folio")

    # Campos opcionales básicos
    type: Optional[Literal["guest", "master"]] = Field(
        default=None, description="Tipo de folio"
    )
    current_balance: Optional[float] = Field(
        default=None, alias="currentBalance", description="Balance actual"
    )
    realized_balance: Optional[float] = Field(
        default=None, alias="realizedBalance", description="Balance realizado"
    )
    start_date: Optional[str] = Field(
        default=None, alias="startDate", description="Fecha de inicio"
    )
    end_date: Optional[str] = Field(
        default=None, alias="endDate", description="Fecha de fin"
    )
    closed_date: Optional[str] = Field(
        default=None, alias="closedDate", description="Fecha de cierre"
    )
    contact_id: Optional[int] = Field(
        default=None, alias="contactId", description="ID del contacto"
    )
    company_id: Optional[int] = Field(
        default=None, alias="companyId", description="ID de la compañía"
    )
    reservation_id: Optional[int] = Field(
        default=None, alias="reservationId", description="ID de la reserva"
    )
    travel_agent_id: Optional[int] = Field(
        default=None, alias="travelAgentId", description="ID del agente de viajes"
    )
    name: Optional[str] = Field(default=None, description="Nombre del folio")
    tax_empty: Optional[bool] = Field(
        default=None, alias="taxEmpty", description="Exento de impuestos"
    )

    # Campos de excepción
    has_exception: Optional[bool] = Field(
        default=None, alias="hasException", description="Tiene excepción"
    )
    exception_message: Optional[str] = Field(
        default=None, alias="exceptionMessage", description="Mensaje de excepción"
    )

    # Campos financieros (visibles para ciertos tipos de folio)
    agent_commission: Optional[float] = Field(
        default=None, alias="agentCommission", description="Comisión del agente"
    )
    owner_commission: Optional[float] = Field(
        default=None, alias="ownerCommission", description="Comisión del propietario"
    )
    owner_revenue: Optional[float] = Field(
        default=None, alias="ownerRevenue", description="Ingresos del propietario"
    )
    check_in_date: Optional[str] = Field(
        default=None, alias="checkInDate", description="Fecha de check-in"
    )
    check_out_date: Optional[str] = Field(
        default=None, alias="checkOutDate", description="Fecha de check-out"
    )

    # Campos de folio maestro
    master_folio_rule_id: Optional[int] = Field(
        default=None,
        alias="masterFolioRuleId",
        description="ID de regla de folio maestro",
    )
    master_folio_id: Optional[int] = Field(
        default=None, alias="masterFolioId", description="ID de folio maestro"
    )

    # Metadatos
    created_at: Optional[str] = Field(
        default=None, alias="createdAt", description="Fecha de creación"
    )
    updated_at: Optional[str] = Field(
        default=None, alias="updatedAt", description="Fecha de actualización"
    )
    created_by: Optional[str] = Field(
        default=None, alias="createdBy", description="Creado por"
    )
    updated_by: Optional[str] = Field(
        default=None, alias="updatedBy", description="Actualizado por"
    )

    # Objetos embebidos
    embedded: Optional[FolioEmbedded] = Field(
        default=None, alias="_embedded", description="Objetos embebidos"
    )
    links: Optional[FolioLinks] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class GetFolioParams(BaseModel):
    """Parámetros para obtener un folio"""

    folio_id: int = Field(..., description="ID del folio a obtener")
