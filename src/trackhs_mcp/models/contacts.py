"""
Modelos Pydantic para Contacts de Track HS API
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class ContactReference(BaseModel):
    """Modelo de ContactReference"""

    reference: str = Field(..., description="Referencia")
    sales_link_id: int = Field(..., description="ID del enlace de ventas")
    channel_id: int = Field(..., description="ID del canal")


class ContactTag(BaseModel):
    """Modelo de ContactTag"""

    id: int = Field(..., description="ID del tag")
    name: str = Field(..., description="Nombre del tag")


class ContactLinks(BaseModel):
    """Modelo de ContactLinks"""

    self: Dict[str, str] = Field(..., description="Enlace propio")


class Contact(BaseModel):
    """Modelo de Contact"""

    id: int = Field(..., description="ID único del contacto")
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
    is_vip: bool = Field(..., description="Si es VIP")
    is_blacklist: bool = Field(..., description="Si está en lista negra")
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
    references: Optional[List[ContactReference]] = Field(
        default=None, description="Referencias"
    )
    tags: Optional[List[ContactTag]] = Field(default=None, description="Tags")
    custom_values: Optional[Dict[str, Union[str, List[str]]]] = Field(
        default=None, description="Valores personalizados"
    )
    links: Optional[ContactLinks] = Field(
        default=None, alias="_links", description="Enlaces"
    )
    updated_at: str = Field(..., description="Fecha de actualización")
    updated_by: str = Field(..., description="Actualizado por")
    created_at: str = Field(..., description="Fecha de creación")
    created_by: str = Field(..., description="Creado por")
    no_identity: bool = Field(..., description="Sin identidad")


class GetContactsParams(PaginationParams, SearchParams):
    """Parámetros para obtener contactos"""

    sort_column: Optional[
        Literal["id", "name", "email", "cellPhone", "homePhone", "otherPhone", "vip"]
    ] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    term: Optional[str] = Field(default=None, description="Término de búsqueda")
    email: Optional[str] = Field(default=None, description="Email")


class ContactsResponse(BaseModel):
    """Respuesta de contactos"""

    embedded: Dict[str, List[Contact]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )


class ContactFilters(BaseModel):
    """Filtros para contactos"""

    is_vip: Optional[bool] = Field(default=None, description="Si es VIP")
    is_blacklist: Optional[bool] = Field(
        default=None, description="Si está en lista negra"
    )
    country: Optional[str] = Field(default=None, description="País")
    region: Optional[str] = Field(default=None, description="Región")
    tags: Optional[List[str]] = Field(default=None, description="Tags")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
