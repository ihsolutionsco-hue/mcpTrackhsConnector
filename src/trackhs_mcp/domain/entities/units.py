"""
Modelos Pydantic para Units de Track HS Channel API
Basado en la especificación completa de la API Get Units Collection
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class UnitType(BaseModel):
    """Modelo para tipo de unidad (deprecated)"""

    id: int = Field(..., description="ID del tipo de unidad")
    name: str = Field(..., description="Nombre del tipo de unidad")


class LodgingType(BaseModel):
    """Modelo para tipo de alojamiento"""

    id: int = Field(..., description="ID del tipo de alojamiento")
    name: str = Field(..., description="Nombre del tipo de alojamiento")


class BedType(BaseModel):
    """Modelo para tipo de cama"""

    id: int = Field(..., description="ID del tipo de cama")
    name: str = Field(..., description="Nombre del tipo de cama")
    count: int = Field(..., description="Cantidad de camas de este tipo")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo para Airbnb")
    homeaway_type: Optional[str] = Field(default=None, description="Tipo para HomeAway")
    marriott_type: Optional[str] = Field(default=None, description="Tipo para Marriott")


class Bed(BaseModel):
    """Modelo para cama individual en una habitación"""

    id: int = Field(..., description="ID del tipo de cama")
    name: str = Field(..., description="Nombre del tipo de cama")
    count: str = Field(..., description="Cantidad como string")
    homeaway_type: Optional[str] = Field(default=None, description="Tipo para HomeAway")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo para Airbnb")
    marriott_type: Optional[str] = Field(default=None, description="Tipo para Marriott")


class Room(BaseModel):
    """Modelo para habitación individual"""

    name: str = Field(..., description="Nombre de la habitación")
    type: Literal[
        "bedroom",
        "half_bathroom",
        "three_quarter_bathroom",
        "full_bathroom",
        "kitchen",
        "common",
        "outside",
    ] = Field(..., description="Tipo de habitación")
    sleeps: int = Field(..., description="Capacidad de dormir")
    description: Optional[str] = Field(
        default=None, description="Descripción de la habitación"
    )
    has_attached_bathroom: bool = Field(
        ..., alias="hasAttachedBathroom", description="Tiene baño adjunto"
    )
    beds: List[Bed] = Field(..., description="Camas en la habitación")
    order: Optional[int] = Field(default=None, description="Orden de la habitación")
    homeaway_type: Optional[str] = Field(default=None, description="Tipo para HomeAway")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo para Airbnb")


class AmenityGroup(BaseModel):
    """Modelo para grupo de amenidades"""

    id: int = Field(..., description="ID del grupo")
    name: str = Field(..., description="Nombre del grupo")


class Amenity(BaseModel):
    """Modelo para amenidad"""

    id: int = Field(..., description="ID de la amenidad")
    name: str = Field(..., description="Nombre de la amenidad")
    group: AmenityGroup = Field(..., description="Grupo de la amenidad")


class LocalOffice(BaseModel):
    """Modelo para oficina local"""

    name: str = Field(..., description="Nombre de la oficina")
    directions: Optional[str] = Field(default=None, description="Direcciones")
    email: Optional[str] = Field(default=None, description="Email")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    latitude: Optional[str] = Field(default=None, description="Latitud")
    longitude: Optional[str] = Field(default=None, description="Longitud")
    street_address: Optional[str] = Field(default=None, description="Dirección")
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: Optional[str] = Field(default=None, description="Localidad")
    region: Optional[str] = Field(default=None, description="Región")
    postal_code: Optional[str] = Field(default=None, description="Código postal")
    country: Optional[str] = Field(default=None, description="País")


class Unit(BaseModel):
    """Modelo de Unit - Basado en la especificación completa de la API"""

    model_config = {"populate_by_name": True}

    id: int = Field(..., description="ID único de la unidad")
    name: str = Field(..., description="Nombre de la unidad")
    short_name: Optional[str] = Field(
        default=None, alias="shortName", description="Nombre corto"
    )
    unit_code: Optional[str] = Field(
        default=None, alias="unitCode", description="Código de la unidad"
    )
    headline: Optional[str] = Field(default=None, description="Título")
    short_description: Optional[str] = Field(
        default=None, alias="shortDescription", description="Descripción corta"
    )
    long_description: Optional[str] = Field(
        default=None, alias="longDescription", description="Descripción larga"
    )
    house_rules: Optional[str] = Field(
        default=None, alias="houseRules", description="Reglas de la casa"
    )
    node_id: int = Field(..., alias="nodeId", description="ID del nodo")
    unit_type: Optional[UnitType] = Field(
        default=None, alias="unitType", description="Tipo de unidad (deprecated)"
    )
    lodging_type: Optional[LodgingType] = Field(
        default=None, alias="lodgingType", description="Tipo de alojamiento"
    )
    directions: Optional[str] = Field(default=None, description="Direcciones")
    checkin_details: Optional[str] = Field(
        default=None, alias="checkinDetails", description="Detalles de check-in"
    )
    timezone: str = Field(..., description="Zona horaria")
    checkin_time: str = Field(..., alias="checkinTime", description="Hora de check-in")
    has_early_checkin: bool = Field(
        ..., alias="hasEarlyCheckin", description="Permite check-in temprano"
    )
    early_checkin_time: Optional[str] = Field(
        default=None, alias="earlyCheckinTime", description="Hora de check-in temprano"
    )
    checkout_time: str = Field(
        ..., alias="checkoutTime", description="Hora de check-out"
    )
    has_late_checkout: bool = Field(
        ..., alias="hasLateCheckout", description="Permite check-out tardío"
    )
    late_checkout_time: Optional[str] = Field(
        default=None, alias="lateCheckoutTime", description="Hora de check-out tardío"
    )
    min_booking_window: Optional[int] = Field(
        default=None, alias="minBookingWindow", description="Ventana mínima de reserva"
    )
    max_booking_window: Optional[int] = Field(
        default=None, alias="maxBookingWindow", description="Ventana máxima de reserva"
    )
    website: Optional[str] = Field(default=None, description="Sitio web")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    street_address: str = Field(..., alias="streetAddress", description="Dirección")
    extended_address: Optional[str] = Field(
        default=None, alias="extendedAddress", description="Dirección extendida"
    )
    locality: str = Field(..., description="Localidad")
    region: str = Field(..., description="Región")
    postal: str = Field(..., description="Código postal")
    country: str = Field(..., description="País")
    latitude: Optional[float] = Field(default=None, description="Latitud")
    longitude: Optional[float] = Field(default=None, description="Longitud")
    pets_friendly: bool = Field(
        ..., alias="petsFriendly", description="Permite mascotas"
    )
    max_pets: Optional[int] = Field(
        default=None, alias="maxPets", description="Máximo de mascotas"
    )
    events_allowed: bool = Field(
        ..., alias="eventsAllowed", description="Permite eventos"
    )
    smoking_allowed: bool = Field(
        ..., alias="smokingAllowed", description="Permite fumar"
    )
    children_allowed: bool = Field(
        ..., alias="childrenAllowed", description="Permite niños"
    )
    minimum_age_limit: Optional[int] = Field(
        default=None, alias="minimumAgeLimit", description="Edad mínima"
    )
    is_accessible: bool = Field(..., alias="isAccessible", description="Es accesible")
    area: Optional[int] = Field(default=None, description="Área")
    floors: Optional[int] = Field(default=None, description="Pisos")
    max_occupancy: int = Field(
        ..., alias="maxOccupancy", description="Ocupación máxima"
    )
    security_deposit: Optional[str] = Field(
        default=None, alias="securityDeposit", description="Depósito de seguridad"
    )
    bedrooms: int = Field(..., description="Habitaciones")
    full_bathrooms: int = Field(
        ..., alias="fullBathrooms", description="Baños completos"
    )
    three_quarter_bathrooms: Optional[int] = Field(
        default=None, alias="threeQuarterBathrooms", description="Baños de 3/4"
    )
    half_bathrooms: int = Field(..., alias="halfBathrooms", description="Medios baños")
    bed_types: Optional[List[BedType]] = Field(
        default=None, alias="bedTypes", description="Tipos de cama"
    )
    rooms: Optional[List[Room]] = Field(default=None, description="Habitaciones")
    amenities: Optional[List[Amenity]] = Field(default=None, description="Amenidades")
    amenity_description: Optional[str] = Field(
        default=None,
        alias="amenityDescription",
        description="Descripción de amenidades",
    )
    custom: Optional[Dict[str, Any]] = Field(
        default=None, description="Campos personalizados"
    )
    cover_image: Optional[str] = Field(
        default=None, alias="coverImage", description="Imagen de portada (deprecated)"
    )
    tax_id: Optional[str] = Field(
        default=None, alias="taxId", description="ID de impuesto"
    )
    local_office: Optional[LocalOffice] = Field(
        default=None, alias="localOffice", description="Oficina local"
    )
    regulations: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Regulaciones (deprecated)"
    )
    updated_at: str = Field(
        ..., alias="updatedAt", description="Fecha de actualización"
    )
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class SearchUnitsParams(PaginationParams, SearchParams):
    """Parámetros para buscar unidades - Basado en la especificación completa"""

    sort_column: Optional[Literal["id", "name", "nodeName", "unitTypeName"]] = Field(
        default=None, description="Columna para ordenar"
    )
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default=None, description="Dirección de ordenamiento"
    )
    node_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del nodo específico"
    )
    amenity_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) de amenidad específica"
    )
    unit_type_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del tipo de unidad específico"
    )
    content_updated_since: Optional[str] = Field(
        default=None, description="Fecha de actualización de contenido desde (ISO 8601)"
    )
    updated_since: Optional[str] = Field(
        default=None, description="Fecha de actualización desde (ISO 8601) - deprecated"
    )
    search: Optional[str] = Field(
        default=None, description="Búsqueda por nombre o descripción"
    )
    term: Optional[str] = Field(default=None, description="Búsqueda por término")
    unit_code: Optional[str] = Field(
        default=None, description="Búsqueda por código de unidad"
    )
    short_name: Optional[str] = Field(
        default=None, description="Búsqueda por nombre corto"
    )
    min_bedrooms: Optional[int] = Field(
        default=None, description="Mínimo de habitaciones"
    )
    max_bedrooms: Optional[int] = Field(
        default=None, description="Máximo de habitaciones"
    )
    bedrooms: Optional[int] = Field(
        default=None, description="Número exacto de habitaciones"
    )
    min_bathrooms: Optional[int] = Field(default=None, description="Mínimo de baños")
    max_bathrooms: Optional[int] = Field(default=None, description="Máximo de baños")
    bathrooms: Optional[int] = Field(default=None, description="Número exacto de baños")
    calendar_id: Optional[int] = Field(default=None, description="ID del calendario")
    pets_friendly: Optional[int] = Field(
        default=None, description="Permite mascotas (0/1)"
    )
    allow_unit_rates: Optional[int] = Field(
        default=None, description="Permite tarifas de unidad (0/1)"
    )
    computed: Optional[int] = Field(
        default=None, description="Valores computados (0/1)"
    )
    inherited: Optional[int] = Field(
        default=None, description="Atributos heredados (0/1)"
    )
    limited: Optional[int] = Field(
        default=None, description="Atributos limitados (0/1)"
    )
    is_bookable: Optional[int] = Field(default=None, description="Es reservable (0/1)")
    include_descriptions: Optional[int] = Field(
        default=None, description="Incluir descripciones (0/1)"
    )
    is_active: Optional[int] = Field(default=None, description="Está activo (0/1)")
    events_allowed: Optional[int] = Field(
        default=None, description="Permite eventos (0/1)"
    )
    smoking_allowed: Optional[int] = Field(
        default=None, description="Permite fumar (0/1)"
    )
    children_allowed: Optional[int] = Field(
        default=None, description="Permite niños (0/1)"
    )
    is_accessible: Optional[int] = Field(default=None, description="Es accesible (0/1)")
    arrival: Optional[str] = Field(
        default=None, description="Fecha de llegada (ISO 8601)"
    )
    departure: Optional[str] = Field(
        default=None, description="Fecha de salida (ISO 8601)"
    )
    role_id: Optional[int] = Field(default=None, description="ID del rol")
    id: Optional[List[int]] = Field(
        default=None, description="IDs específicos de unidades"
    )
    unit_status: Optional[
        Literal["clean", "dirty", "occupied", "inspection", "inprogress"]
    ] = Field(default=None, description="Estado de la unidad")


class SearchUnitsResponse(BaseModel):
    """Respuesta de búsqueda de unidades"""

    model_config = {"populate_by_name": True}

    embedded: Dict[str, List[Unit]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., alias="page_count", description="Total de páginas")
    page_size: int = Field(..., alias="page_size", description="Tamaño de página")
    total_items: int = Field(..., alias="total_items", description="Total de elementos")
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")


class GetUnitParams(BaseModel):
    """Parámetros para obtener una unidad específica"""

    unit_id: int = Field(..., description="ID de la unidad")


class UnitResponse(BaseModel):
    """Respuesta de una unidad específica"""

    data: Unit = Field(..., description="Datos de la unidad")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")


class UnitFilters(BaseModel):
    """Filtros para unidades"""

    status: Optional[
        Literal["clean", "dirty", "occupied", "inspection", "inprogress"]
    ] = Field(default=None, description="Estado")
    property_id: Optional[str] = Field(default=None, description="ID de la propiedad")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
    unit_code: Optional[str] = Field(default=None, description="Código de unidad")
    node_id: Optional[int] = Field(default=None, description="ID del nodo")
