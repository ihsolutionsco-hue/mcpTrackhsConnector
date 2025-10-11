"""
Modelos Pydantic para Ledger Accounts de Track HS API
"""

from typing import Optional, Literal, List, Dict, Any, Union
from pydantic import BaseModel, Field
from .base import PaginationParams, SearchParams

class StakeholderTag(BaseModel):
    """Modelo de StakeholderTag"""
    id: int = Field(..., description="ID del tag")
    name: str = Field(..., description="Nombre del tag")

class StakeholderLinks(BaseModel):
    """Modelo de StakeholderLinks"""
    self: Dict[str, str] = Field(..., description="Enlace propio")
    contacts: Optional[Dict[str, str]] = Field(default=None, description="Enlace de contactos")
    licences: Optional[Dict[str, str]] = Field(default=None, description="Enlace de licencias")

class Stakeholder(BaseModel):
    """Modelo de Stakeholder"""
    id: int = Field(..., description="ID del stakeholder")
    type: Literal["company", "agent", "vendor", "owner"] = Field(..., description="Tipo de stakeholder")
    is_active: bool = Field(..., description="Si está activo")
    name: str = Field(..., description="Nombre")
    street_address: Optional[str] = Field(default=None, description="Dirección de la calle")
    extended_address: Optional[str] = Field(default=None, description="Dirección extendida")
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    tax_type: Optional[Literal["rents", "other", "none", "non_employee_compensation"]] = Field(default=None, description="Tipo de impuesto")
    tax_name: Optional[str] = Field(default=None, description="Nombre del impuesto")
    tax_id: Optional[str] = Field(default=None, description="ID del impuesto")
    ach_account_number: Optional[str] = Field(default=None, description="Número de cuenta ACH")
    ach_routing_number: Optional[str] = Field(default=None, description="Número de ruteo ACH")
    ach_account_type: Optional[Literal["business-checking", "business-savings", "personal-checking", "personal-savings"]] = Field(default=None, description="Tipo de cuenta ACH")
    ach_verified_at: Optional[str] = Field(default=None, description="Fecha de verificación ACH")
    payment_type: Optional[Literal["print", "direct"]] = Field(default=None, description="Tipo de pago")
    gl_expiration_date: Optional[str] = Field(default=None, description="Fecha de expiración GL")
    gl_insurance_policy: Optional[str] = Field(default=None, description="Póliza de seguro GL")
    wc_expiration_date: Optional[str] = Field(default=None, description="Fecha de expiración WC")
    wc_insurance_policy: Optional[str] = Field(default=None, description="Póliza de seguro WC")
    travel_agent_deduct_commission: Optional[bool] = Field(default=None, description="Si el agente de viajes deduce comisión")
    travel_agent_commission: Optional[int] = Field(default=None, description="Comisión del agente de viajes")
    travel_agent_iata_number: Optional[str] = Field(default=None, description="Número IATA del agente de viajes")
    enable_work_order_approval: Optional[bool] = Field(default=None, description="Si habilitar aprobación de órdenes de trabajo")
    notes: Optional[str] = Field(default=None, description="Notas")
    website: Optional[str] = Field(default=None, description="Sitio web")
    email: Optional[str] = Field(default=None, description="Email")
    fax: Optional[str] = Field(default=None, description="Fax")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")
    updated_by: str = Field(..., description="Actualizado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    tags: Optional[List[StakeholderTag]] = Field(default=None, description="Tags")
    links: Optional[StakeholderLinks] = Field(default=None, alias="_links", description="Enlaces")

class LedgerAccountLinks(BaseModel):
    """Modelo de LedgerAccountLinks"""
    self: Dict[str, str] = Field(..., description="Enlace propio")

class LedgerAccount(BaseModel):
    """Modelo de LedgerAccount"""
    id: int = Field(..., description="ID de la cuenta contable")
    code: str = Field(..., description="Código de la cuenta")
    name: str = Field(..., description="Nombre de la cuenta")
    description: Optional[str] = Field(default=None, description="Descripción")
    category: Literal["revenue", "asset", "equity", "expense", "liability"] = Field(..., description="Categoría")
    account_type: Literal["bank", "current", "fixed", "other-asset", "receivable"] = Field(..., description="Tipo de cuenta")
    parent_id: Optional[int] = Field(default=None, description="ID de la cuenta padre")
    is_active: bool = Field(..., description="Si está activa")
    external_id: Optional[int] = Field(default=None, description="ID externo")
    external_name: Optional[str] = Field(default=None, description="Nombre externo")
    bank_name: Optional[str] = Field(default=None, description="Nombre del banco")
    ach_enabled: bool = Field(..., description="Si ACH está habilitado")
    allow_owner_payments: bool = Field(..., description="Si permite pagos de propietarios")
    ach_orgin_id: Optional[int] = Field(default=None, description="ID de origen ACH")
    routing_number: Optional[int] = Field(default=None, description="Número de ruteo")
    account_number: Optional[int] = Field(default=None, description="Número de cuenta")
    currency: Optional[str] = Field(default=None, description="Moneda")
    current_balance: Optional[int] = Field(default=None, description="Balance actual")
    recursive_balance: Optional[int] = Field(default=None, description="Balance recursivo")
    immediate_destination: Optional[int] = Field(default=None, description="Destino inmediato")
    immediate_destination_name: Optional[str] = Field(default=None, description="Nombre del destino inmediato")
    immediate_origin_name: Optional[str] = Field(default=None, description="Nombre del origen inmediato")
    company_name: Optional[str] = Field(default=None, description="Nombre de la empresa")
    company_identification: Optional[int] = Field(default=None, description="Identificación de la empresa")
    stakeholder_id: Optional[int] = Field(default=None, description="ID del stakeholder")
    enable_refunds: bool = Field(..., description="Si habilitar reembolsos")
    default_refund_account: Optional[int] = Field(default=None, description="Cuenta de reembolso por defecto")
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")
    updated_by: str = Field(..., description="Actualizado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    embedded: Optional[Dict[str, Union["LedgerAccount", Stakeholder]]] = Field(default=None, alias="_embedded", description="Datos embebidos")
    links: Optional[LedgerAccountLinks] = Field(default=None, alias="_links", description="Enlaces")

class GetLedgerAccountsParams(PaginationParams, SearchParams):
    """Parámetros para obtener cuentas contables"""
    sort_column: Optional[Literal["id", "name", "type", "relativeOrder", "isActive"]] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(default="asc", description="Dirección de ordenamiento")
    is_active: Optional[int] = Field(default=None, description="Si está activa")
    category: Optional[Literal["Revenue", "Asset", "Equity", "Liability", "Expense"]] = Field(default=None, description="Categoría")
    account_type: Optional[str] = Field(default=None, description="Tipo de cuenta")
    parent_id: Optional[int] = Field(default=None, description="ID de la cuenta padre")
    include_restricted: Optional[int] = Field(default=None, description="Si incluir restringidas")
    sort_by_category_value: Optional[int] = Field(default=None, description="Ordenar por valor de categoría")

class LedgerAccountsResponse(BaseModel):
    """Respuesta de cuentas contables"""
    embedded: Dict[str, List[LedgerAccount]] = Field(..., alias="_embedded", description="Datos embebidos")

class GetLedgerAccountParams(BaseModel):
    """Parámetros para obtener una cuenta contable específica"""
    account_id: int = Field(..., description="ID de la cuenta contable")

class LedgerAccountResponse(BaseModel):
    """Respuesta de una cuenta contable específica"""
    data: LedgerAccount = Field(..., description="Datos de la cuenta contable")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")

class LedgerAccountFilters(BaseModel):
    """Filtros para cuentas contables"""
    category: Optional[str] = Field(default=None, description="Categoría")
    account_type: Optional[str] = Field(default=None, description="Tipo de cuenta")
    is_active: Optional[bool] = Field(default=None, description="Si está activa")
    parent_id: Optional[int] = Field(default=None, description="ID de la cuenta padre")
    stakeholder_id: Optional[int] = Field(default=None, description="ID del stakeholder")
    currency: Optional[str] = Field(default=None, description="Moneda")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
