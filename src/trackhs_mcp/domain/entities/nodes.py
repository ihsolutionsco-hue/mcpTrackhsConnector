"""
Modelos Pydantic para Nodes de Track HS API
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class NodeType(BaseModel):
    """Modelo de NodeType"""

    id: int = Field(..., description="ID del tipo de nodo")
    name: str = Field(..., description="Nombre del tipo")
    description: Optional[str] = Field(default=None, description="Descripción")
    is_report: Optional[bool] = Field(default=None, description="Si es reporte")
    is_reservations: Optional[bool] = Field(
        default=None, description="Si es reservaciones"
    )
    is_housekeeping: Optional[bool] = Field(default=None, description="Si es limpieza")
    is_maintenance: Optional[bool] = Field(
        default=None, description="Si es mantenimiento"
    )
    is_online: Optional[bool] = Field(default=None, description="Si está en línea")
    is_owners: Optional[bool] = Field(default=None, description="Si es propietarios")
    is_active: Optional[bool] = Field(default=None, description="Si está activo")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class TaxDistrict(BaseModel):
    """Modelo de TaxDistrict"""

    id: int = Field(..., description="ID del distrito fiscal")
    is_active: Optional[bool] = Field(default=None, description="Si está activo")
    name: Optional[str] = Field(default=None, description="Nombre")
    short_term_policy_id: Optional[int] = Field(
        default=None, description="ID de política de corto plazo"
    )
    long_term_policy_id: Optional[int] = Field(
        default=None, description="ID de política de largo plazo"
    )
    has_breakpoint: Optional[bool] = Field(
        default=None, description="Si tiene punto de quiebre"
    )
    breakpoint: Optional[int] = Field(default=None, description="Punto de quiebre")
    sales_tax_policy_id: Optional[int] = Field(
        default=None, description="ID de política de impuesto de ventas"
    )
    sales_tax_policy: Optional[Any] = Field(
        default=None, description="Política de impuesto de ventas"
    )
    tax_markup: Optional[int] = Field(default=None, description="Markup de impuesto")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class CancellationBreakpoint(BaseModel):
    """Modelo de CancellationBreakpoint"""

    id: int = Field(..., description="ID del punto de quiebre")
    range_start: int = Field(..., description="Inicio del rango")
    range_end: int = Field(..., description="Fin del rango")
    non_refundable: bool = Field(..., description="No reembolsable")
    non_cancelable: bool = Field(..., description="No cancelable")
    penalty_nights: int = Field(..., description="Noches de penalización")
    penalty_percent: int = Field(..., description="Porcentaje de penalización")
    penalty_flat: int = Field(..., description="Penalización fija")
    description: str = Field(..., description="Descripción")


class CancellationPolicy(BaseModel):
    """Modelo de CancellationPolicy"""

    id: int = Field(..., description="ID de la política")
    is_default: Optional[bool] = Field(default=None, description="Si es por defecto")
    is_active: Optional[bool] = Field(default=None, description="Si está activa")
    name: Optional[str] = Field(default=None, description="Nombre")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    code: Optional[str] = Field(default=None, description="Código")
    charge_as: Optional[str] = Field(default=None, description="Cobrar como")
    can_exceed_balance: Optional[bool] = Field(
        default=None, description="Si puede exceder balance"
    )
    cancel_time: Optional[str] = Field(
        default=None, description="Tiempo de cancelación"
    )
    cancel_timezone: Optional[str] = Field(
        default=None, description="Zona horaria de cancelación"
    )
    post_date: Optional[str] = Field(default=None, description="Fecha de publicación")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo de Airbnb")
    tripadvisor_type: Optional[str] = Field(
        default=None, description="Tipo de TripAdvisor"
    )
    homeaway_type: Optional[str] = Field(default=None, description="Tipo de HomeAway")
    breakpoints: Optional[List[CancellationBreakpoint]] = Field(
        default=None, description="Puntos de quiebre"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class HousekeepingZone(BaseModel):
    """Modelo de HousekeepingZone"""

    id: int = Field(..., description="ID de la zona de limpieza")
    is_active: Optional[bool] = Field(default=None, description="Si está activa")
    name: Optional[str] = Field(default=None, description="Nombre")
    type: Optional[str] = Field(default=None, description="Tipo")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class MaintenanceZone(BaseModel):
    """Modelo de MaintenanceZone"""

    id: int = Field(..., description="ID de la zona de mantenimiento")
    is_active: Optional[bool] = Field(default=None, description="Si está activa")
    name: Optional[str] = Field(default=None, description="Nombre")
    type: Optional[str] = Field(default=None, description="Tipo")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class Node(BaseModel):
    """Modelo de Node"""

    id: int = Field(..., description="ID del nodo")
    name: str = Field(..., description="Nombre del nodo")
    max_pets: Optional[int] = Field(default=None, description="Máximo de mascotas")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    website_url: Optional[str] = Field(default=None, description="URL del sitio web")
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
    max_discount: Optional[int] = Field(default=None, description="Descuento máximo")
    timezone: Optional[str] = Field(default=None, description="Zona horaria")
    longitude: Optional[float] = Field(default=None, description="Longitud")
    latitude: Optional[float] = Field(default=None, description="Latitud")
    housekeeping_notes: Optional[str] = Field(
        default=None, description="Notas de limpieza"
    )
    pet_friendly: Optional[bool] = Field(default=None, description="Si acepta mascotas")
    smoking_allowed: Optional[bool] = Field(
        default=None, description="Si se permite fumar"
    )
    children_allowed: Optional[bool] = Field(
        default=None, description="Si se permiten niños"
    )
    events_allowed: Optional[bool] = Field(
        default=None, description="Si se permiten eventos"
    )
    is_accessible: Optional[bool] = Field(default=None, description="Si es accesible")
    has_early_checkin: Optional[bool] = Field(
        default=None, description="Si tiene check-in temprano"
    )
    has_late_checkout: Optional[bool] = Field(
        default=None, description="Si tiene check-out tardío"
    )
    quick_checkin: Optional[bool] = Field(
        default=None, description="Si tiene check-in rápido"
    )
    quick_checkout: Optional[bool] = Field(
        default=None, description="Si tiene check-out rápido"
    )
    checkin_time: Optional[str] = Field(default=None, description="Hora de check-in")
    checkout_time: Optional[str] = Field(default=None, description="Hora de check-out")
    early_checkin_time: Optional[str] = Field(
        default=None, description="Hora de check-in temprano"
    )
    late_checkout_time: Optional[str] = Field(
        default=None, description="Hora de check-out tardío"
    )
    description: Optional[str] = Field(default=None, description="Descripción")
    short_description: Optional[str] = Field(
        default=None, description="Descripción corta"
    )
    long_description: Optional[str] = Field(
        default=None, description="Descripción larga"
    )
    directions: Optional[str] = Field(default=None, description="Direcciones")
    checkin_details: Optional[str] = Field(
        default=None, description="Detalles de check-in"
    )
    house_rules: Optional[str] = Field(default=None, description="Reglas de la casa")
    parent_id: Optional[int] = Field(default=None, description="ID del nodo padre")
    parent: Optional[Any] = Field(default=None, description="Nodo padre")
    type_id: Optional[int] = Field(default=None, description="ID del tipo")
    type: Optional[NodeType] = Field(default=None, description="Tipo de nodo")
    tax_district_id: Optional[int] = Field(
        default=None, description="ID del distrito fiscal"
    )
    tax_district: Optional[TaxDistrict] = Field(
        default=None, description="Distrito fiscal"
    )
    checkin_office_id: Optional[int] = Field(
        default=None, description="ID de la oficina de check-in"
    )
    checkin_office: Optional[Any] = Field(
        default=None, description="Oficina de check-in"
    )
    cancellation_policy_id: Optional[int] = Field(
        default=None, description="ID de la política de cancelación"
    )
    cancellation_policy: Optional[CancellationPolicy] = Field(
        default=None, description="Política de cancelación"
    )
    housekeeping_zone_id: Optional[int] = Field(
        default=None, description="ID de la zona de limpieza"
    )
    housekeeping_zone: Optional[HousekeepingZone] = Field(
        default=None, description="Zona de limpieza"
    )
    maintenance_zone_id: Optional[int] = Field(
        default=None, description="ID de la zona de mantenimiento"
    )
    maintenance_zone: Optional[MaintenanceZone] = Field(
        default=None, description="Zona de mantenimiento"
    )
    is_reservations: Optional[bool] = Field(
        default=None, description="Si es reservaciones"
    )
    is_housekeeping: Optional[bool] = Field(default=None, description="Si es limpieza")
    is_maintenance: Optional[bool] = Field(
        default=None, description="Si es mantenimiento"
    )
    is_online: Optional[bool] = Field(default=None, description="Si está en línea")
    is_owners: Optional[bool] = Field(default=None, description="Si es propietarios")
    is_active: Optional[bool] = Field(default=None, description="Si está activo")
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    created_by: Optional[str] = Field(default=None, description="Creado por")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )
    updated_by: Optional[str] = Field(default=None, description="Actualizado por")
    roles: Optional[List[Dict[str, int]]] = Field(default=None, description="Roles")
    custom: Optional[Any] = Field(default=None, description="Datos personalizados")
    guarantee_policies_ids: Optional[List[int]] = Field(
        default=None, description="IDs de políticas de garantía"
    )
    amenities_ids: Optional[List[int]] = Field(
        default=None, description="IDs de amenidades"
    )
    documents_ids: Optional[List[int]] = Field(
        default=None, description="IDs de documentos"
    )
    gateways_ids: Optional[List[int]] = Field(
        default=None, description="IDs de gateways"
    )
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Optional[Dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class GetNodesParams(PaginationParams, SearchParams):
    """Parámetros para obtener nodos"""

    sort_column: Optional[Literal["id", "name"]] = Field(
        default="id", description="Columna para ordenar"
    )
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    term: Optional[str] = Field(default=None, description="Término de búsqueda")
    parent_id: Optional[int] = Field(default=None, description="ID del nodo padre")
    type_id: Optional[int] = Field(default=None, description="ID del tipo")
    computed: Optional[Literal[0, 1]] = Field(
        default=None, description="Si es computado"
    )
    inherited: Optional[Literal[0, 1]] = Field(
        default=None, description="Si es heredado"
    )
    include_descriptions: Optional[Literal[0, 1]] = Field(
        default=None, description="Si incluir descripciones"
    )


class GetNodesResponse(BaseModel):
    """Respuesta de obtener nodos"""

    model_config = {"populate_by_name": True}

    embedded: Dict[str, List[Node]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    links: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., alias="_links", description="Enlaces"
    )


class GetNodeParams(BaseModel):
    """Parámetros para obtener un nodo específico"""

    node_id: int = Field(..., description="ID del nodo")


class GetNodeResponse(Node):
    """Respuesta de un nodo específico"""

    pass


class NodeFilters(BaseModel):
    """Filtros para nodos"""

    parent_id: Optional[int] = Field(default=None, description="ID del nodo padre")
    type_id: Optional[int] = Field(default=None, description="ID del tipo")
    is_active: Optional[bool] = Field(default=None, description="Si está activo")
    is_reservations: Optional[bool] = Field(
        default=None, description="Si es reservaciones"
    )
    is_housekeeping: Optional[bool] = Field(default=None, description="Si es limpieza")
    is_maintenance: Optional[bool] = Field(
        default=None, description="Si es mantenimiento"
    )
    is_online: Optional[bool] = Field(default=None, description="Si está en línea")
    is_owners: Optional[bool] = Field(default=None, description="Si es propietarios")
    pet_friendly: Optional[bool] = Field(default=None, description="Si acepta mascotas")
    smoking_allowed: Optional[bool] = Field(
        default=None, description="Si se permite fumar"
    )
    children_allowed: Optional[bool] = Field(
        default=None, description="Si se permiten niños"
    )
    events_allowed: Optional[bool] = Field(
        default=None, description="Si se permiten eventos"
    )
    is_accessible: Optional[bool] = Field(default=None, description="Si es accesible")
