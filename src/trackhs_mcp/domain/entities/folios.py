"""
Modelos Pydantic para Folios de Track HS API
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class FolioContact(BaseModel):
    """Modelo de FolioContact"""

    id: int = Field(..., description="ID del contacto")
    first_name: str = Field(..., description="Nombre")
    last_name: str = Field(..., description="Apellido")
    primary_email: str = Field(..., description="Email principal")
    secondary_email: Optional[str] = Field(default=None, description="Email secundario")
    home_phone: Optional[str] = Field(default=None, description="Teléfono de casa")
    cell_phone: Optional[str] = Field(default=None, description="Teléfono celular")
    work_phone: Optional[str] = Field(default=None, description="Teléfono de trabajo")
    other_phone: Optional[str] = Field(default=None, description="Otro teléfono")
    fax: Optional[str] = Field(default=None, description="Fax")
    street_address: Optional[str] = Field(
        default=None, description="Dirección de la calle"
    )
    country: Optional[str] = Field(default=None, description="País")
    postal_code: Optional[str] = Field(default=None, description="Código postal")
    region: Optional[str] = Field(default=None, description="Región")
    locality: Optional[str] = Field(default=None, description="Localidad")
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    notes: Optional[str] = Field(default=None, description="Notas")
    anniversary: Optional[str] = Field(default=None, description="Aniversario")
    birthdate: Optional[str] = Field(default=None, description="Fecha de nacimiento")
    is_vip: Optional[bool] = Field(default=None, description="Si es VIP")
    is_blacklist: Optional[bool] = Field(
        default=None, description="Si está en lista negra"
    )
    tax_id: Optional[str] = Field(default=None, description="ID de impuesto")
    payment_type: Optional[Literal["print", "direct"]] = Field(
        default=None, description="Tipo de pago"
    )
    ach_account_number: Optional[str] = Field(
        default=None, description="Número de cuenta ACH"
    )
    ach_routing_number: Optional[str] = Field(
        default=None, description="Número de ruteo ACH"
    )
    ach_account_type: Optional[
        Literal[
            "business-checking",
            "business-savings",
            "personal-checking",
            "personal-savings",
        ]
    ] = Field(default=None, description="Tipo de cuenta ACH")
    references: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Referencias"
    )
    tags: Optional[List[Dict[str, Union[int, str]]]] = Field(
        default=None, description="Tags"
    )
    custom_values: Optional[Dict[str, Any]] = Field(
        default=None, description="Valores personalizados"
    )
    no_identity: Optional[bool] = Field(default=None, description="Sin identidad")
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")
    updated_at: str = Field(..., description="Fecha de actualización")
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")


class FolioCompany(BaseModel):
    """Modelo de FolioCompany"""

    id: int = Field(..., description="ID de la empresa")
    type: Literal["company", "agent", "vendor", "owner"] = Field(
        ..., description="Tipo de empresa"
    )
    is_active: bool = Field(..., description="Si está activa")
    name: str = Field(..., description="Nombre")
    street_address: Optional[str] = Field(
        default=None, description="Dirección de la calle"
    )
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")
    tax_type: Optional[
        Literal["rents", "other", "none", "non_employee_compensation"]
    ] = Field(default=None, description="Tipo de impuesto")
    tax_name: Optional[str] = Field(default=None, description="Nombre del impuesto")
    tax_id: Optional[str] = Field(default=None, description="ID del impuesto")
    ach_account_number: Optional[str] = Field(
        default=None, description="Número de cuenta ACH"
    )
    ach_routing_number: Optional[str] = Field(
        default=None, description="Número de ruteo ACH"
    )
    ach_account_type: Optional[
        Literal[
            "business-checking",
            "business-savings",
            "personal-checking",
            "personal-savings",
        ]
    ] = Field(default=None, description="Tipo de cuenta ACH")
    ach_verified_at: Optional[str] = Field(
        default=None, description="Fecha de verificación ACH"
    )
    payment_type: Optional[Literal["print", "direct"]] = Field(
        default=None, description="Tipo de pago"
    )
    gl_expiration_date: Optional[str] = Field(
        default=None, description="Fecha de expiración GL"
    )
    gl_insurance_policy: Optional[str] = Field(
        default=None, description="Póliza de seguro GL"
    )
    wc_expiration_date: Optional[str] = Field(
        default=None, description="Fecha de expiración WC"
    )
    wc_insurance_policy: Optional[str] = Field(
        default=None, description="Póliza de seguro WC"
    )
    travel_agent_deduct_commission: Optional[bool] = Field(
        default=None, description="Si el agente de viajes deduce comisión"
    )
    travel_agent_commission: Optional[int] = Field(
        default=None, description="Comisión del agente de viajes"
    )
    travel_agent_iata_number: Optional[str] = Field(
        default=None, description="Número IATA del agente de viajes"
    )
    enable_work_order_approval: Optional[bool] = Field(
        default=None, description="Si habilitar aprobación de órdenes de trabajo"
    )
    notes: Optional[str] = Field(default=None, description="Notas")
    website: Optional[str] = Field(default=None, description="Sitio web")
    email: Optional[str] = Field(default=None, description="Email")
    fax: Optional[str] = Field(default=None, description="Fax")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    tags: Optional[List[Dict[str, Union[int, str]]]] = Field(
        default=None, description="Tags"
    )
    links: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., alias="_links", description="Enlaces"
    )
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")
    updated_by: str = Field(..., description="Actualizado por")
    updated_at: str = Field(..., description="Fecha de actualización")


class FolioRule(BaseModel):
    """Modelo de FolioRule"""

    id: int = Field(..., description="ID de la regla")
    name: str = Field(..., description="Nombre de la regla")
    code: str = Field(..., description="Código de la regla")
    is_active: bool = Field(..., description="Si está activa")
    type: Literal["percent", "breakdown"] = Field(..., description="Tipo de regla")
    percent_amount: Optional[int] = Field(default=None, description="Monto porcentual")
    breakdown_rent_mode: Optional[Literal["percent", "nights"]] = Field(
        default=None, description="Modo de desglose de renta"
    )
    breakdown_rent_include_tax: Optional[bool] = Field(
        default=None, description="Si incluir impuestos en desglose de renta"
    )
    breakdown_rent_percent: Optional[int] = Field(
        default=None, description="Porcentaje de desglose de renta"
    )
    breakdown_rent_nights: Optional[int] = Field(
        default=None, description="Noches de desglose de renta"
    )
    breakdown_fee_mode: Optional[Literal["percent", "required"]] = Field(
        default=None, description="Modo de desglose de tarifas"
    )
    breakdown_fee_include_tax: Optional[bool] = Field(
        default=None, description="Si incluir impuestos en desglose de tarifas"
    )
    breakdown_fee_percent: Optional[int] = Field(
        default=None, description="Porcentaje de desglose de tarifas"
    )
    breakdown_charges_mode: Optional[Literal["percent", "required"]] = Field(
        default=None, description="Modo de desglose de cargos"
    )
    breakdown_charges_include_tax: Optional[bool] = Field(
        default=None, description="Si incluir impuestos en desglose de cargos"
    )
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")
    updated_by: str = Field(..., description="Actualizado por")
    updated_at: str = Field(..., description="Fecha de actualización")


class MasterFolioRule(BaseModel):
    """Modelo de MasterFolioRule"""

    id: int = Field(..., description="ID de la regla maestra")
    rule_id: int = Field(..., description="ID de la regla")
    start_date: Optional[str] = Field(default=None, description="Fecha de inicio")
    end_date: Optional[str] = Field(default=None, description="Fecha de fin")
    min_nights: Optional[int] = Field(default=None, description="Mínimo de noches")
    max_nights: Optional[int] = Field(default=None, description="Máximo de noches")
    max_spend: Optional[int] = Field(default=None, description="Gasto máximo")
    created_by: str = Field(..., description="Creado por")
    created_at: str = Field(..., description="Fecha de creación")
    updated_by: str = Field(..., description="Actualizado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    embedded: Optional[Dict[str, FolioRule]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")


class Folio(BaseModel):
    """Modelo de Folio"""

    id: int = Field(..., description="ID del folio")
    status: Literal["open", "closed"] = Field(..., description="Estado del folio")
    type: Literal["guest", "master"] = Field(..., description="Tipo de folio")
    current_balance: int = Field(..., description="Balance actual")
    realized_balance: int = Field(..., description="Balance realizado")
    closed_date: Optional[str] = Field(default=None, description="Fecha de cierre")
    end_date: Optional[str] = Field(default=None, description="Fecha de fin")
    start_date: Optional[str] = Field(default=None, description="Fecha de inicio")
    tax_empty: bool = Field(..., description="Si está vacío de impuestos")
    company_id: Optional[int] = Field(default=None, description="ID de la empresa")
    contact_id: int = Field(..., description="ID del contacto")
    master_folio_rule_id: Optional[int] = Field(
        default=None, description="ID de la regla maestra del folio"
    )
    master_folio_id: Optional[int] = Field(
        default=None, description="ID del folio maestro"
    )
    agent_commission: Optional[int] = Field(
        default=None, description="Comisión del agente"
    )
    owner_commission: Optional[int] = Field(
        default=None, description="Comisión del propietario"
    )
    owner_revenue: Optional[int] = Field(
        default=None, description="Ingresos del propietario"
    )
    check_out_date: Optional[str] = Field(
        default=None, description="Fecha de check-out"
    )
    check_in_date: Optional[str] = Field(default=None, description="Fecha de check-in")
    exception_message: Optional[str] = Field(
        default=None, description="Mensaje de excepción"
    )
    has_exception: Optional[bool] = Field(
        default=None, description="Si tiene excepción"
    )
    travel_agent_id: Optional[int] = Field(
        default=None, description="ID del agente de viajes"
    )
    reservation_id: Optional[int] = Field(default=None, description="ID de la reserva")
    name: Optional[str] = Field(default=None, description="Nombre")
    links: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., alias="_links", description="Enlaces"
    )
    updated_at: str = Field(..., description="Fecha de actualización")
    updated_by: str = Field(..., description="Actualizado por")
    created_at: str = Field(..., description="Fecha de creación")
    created_by: str = Field(..., description="Creado por")
    embedded: Optional[
        Dict[str, Union[FolioContact, FolioCompany, MasterFolioRule, "Folio"]]
    ] = Field(default=None, alias="_embedded", description="Datos embebidos")


class GetFoliosCollectionParams(PaginationParams, SearchParams):
    """Parámetros para obtener colección de folios"""

    sort_column: Optional[
        Literal[
            "id",
            "name",
            "status",
            "type",
            "startDate",
            "endDate",
            "contactName",
            "companyName",
            "reservationId",
            "currentBalance",
            "realizedBalance",
            "masterFolioRule",
        ]
    ] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    type: Optional[
        Literal["guest", "master", "guest-sub-folio", "master-sub-folio"]
    ] = Field(default=None, description="Tipo de folio")
    status: Optional[Literal["open", "closed"]] = Field(
        default=None, description="Estado del folio"
    )
    master_folio_id: Optional[int] = Field(
        default=None, description="ID del folio maestro"
    )
    contact_id: Optional[int] = Field(default=None, description="ID del contacto")
    company_id: Optional[int] = Field(default=None, description="ID de la empresa")


class GetFoliosCollectionResponse(BaseModel):
    """Respuesta de obtener colección de folios"""

    embedded: Dict[str, List[Folio]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    links: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., alias="_links", description="Enlaces"
    )
