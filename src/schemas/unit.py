"""
Schemas para unidades de alojamiento
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseSchema, PaginationParams, PaginationResponse


class UnitSearchParams(PaginationParams):
    """Parámetros de búsqueda de unidades"""

    search: Optional[str] = Field(
        default=None, max_length=200, description="Búsqueda de texto"
    )
    bedrooms: Optional[int] = Field(
        default=None, ge=0, description="Número de dormitorios"
    )
    bathrooms: Optional[int] = Field(default=None, ge=0, description="Número de baños")
    min_occupancy: Optional[int] = Field(
        default=None, ge=0, description="Capacidad mínima"
    )
    max_occupancy: Optional[int] = Field(
        default=None, ge=0, description="Capacidad máxima"
    )
    is_active: Optional[bool] = Field(default=None, description="Solo unidades activas")
    is_bookable: Optional[bool] = Field(
        default=None, description="Solo unidades reservables"
    )
    pets_friendly: Optional[bool] = Field(
        default=None, description="Solo unidades pet-friendly"
    )
    unit_status: Optional[str] = Field(default=None, description="Estado de la unidad")
    arrival: Optional[str] = Field(
        default=None, description="Fecha de llegada para verificar disponibilidad"
    )
    departure: Optional[str] = Field(
        default=None, description="Fecha de salida para verificar disponibilidad"
    )
    amenity_id: Optional[List[int]] = Field(
        default=None, description="IDs de amenidades requeridas"
    )
    node_id: Optional[List[int]] = Field(default=None, description="IDs de nodos")
    unit_type_id: Optional[List[int]] = Field(
        default=None, description="IDs de tipos de unidad"
    )
    owner_id: Optional[List[int]] = Field(
        default=None, description="IDs de propietarios"
    )
    company_id: Optional[List[int]] = Field(default=None, description="IDs de empresas")
    channel_id: Optional[List[int]] = Field(default=None, description="IDs de canales")
    lodging_type_id: Optional[List[int]] = Field(
        default=None, description="IDs de tipos de alojamiento"
    )
    bed_type_id: Optional[List[int]] = Field(
        default=None, description="IDs de tipos de cama"
    )
    amenity_all: Optional[List[int]] = Field(
        default=None, description="Amenidades que debe tener TODAS"
    )
    unit_ids: Optional[List[int]] = Field(
        default=None, description="IDs específicos de unidades"
    )
    unit_code: Optional[str] = Field(
        default=None, max_length=100, description="Código de unidad"
    )
    short_name: Optional[str] = Field(
        default=None, max_length=100, description="Nombre corto"
    )
    term: Optional[str] = Field(
        default=None, max_length=200, description="Término de búsqueda"
    )
    sort_column: Optional[str] = Field(
        default="name", description="Columna para ordenar"
    )
    sort_direction: Optional[str] = Field(
        default="asc", description="Dirección de ordenamiento"
    )


class UnitDetailResponse(BaseModel):
    """Respuesta detallada de unidad"""

    id: int = Field(description="ID de la unidad")
    name: str = Field(description="Nombre de la unidad")
    unit_code: Optional[str] = Field(default=None, description="Código de la unidad")
    short_name: Optional[str] = Field(default=None, description="Nombre corto")
    description: Optional[str] = Field(default=None, description="Descripción")
    bedrooms: Optional[int] = Field(default=None, description="Número de dormitorios")
    bathrooms: Optional[int] = Field(default=None, description="Número de baños")
    occupancy: Optional[int] = Field(default=None, description="Capacidad")
    unit_type_id: Optional[int] = Field(
        default=None, description="ID del tipo de unidad"
    )
    unit_type_name: Optional[str] = Field(
        default=None, description="Nombre del tipo de unidad"
    )
    node_id: Optional[int] = Field(default=None, description="ID del nodo")
    node_name: Optional[str] = Field(default=None, description="Nombre del nodo")
    is_active: Optional[bool] = Field(default=None, description="Unidad activa")
    is_bookable: Optional[bool] = Field(default=None, description="Unidad reservable")
    pets_friendly: Optional[bool] = Field(default=None, description="Permite mascotas")
    unit_status: Optional[str] = Field(default=None, description="Estado de la unidad")

    # Amenidades
    amenities: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Amenidades disponibles"
    )

    # Precios
    base_price: Optional[float] = Field(default=None, description="Precio base")
    currency: Optional[str] = Field(default=None, description="Moneda")

    # Ubicación
    address: Optional[Dict[str, Any]] = Field(default=None, description="Dirección")
    coordinates: Optional[Dict[str, float]] = Field(
        default=None, description="Coordenadas"
    )

    # Metadatos
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )

    # Enlaces
    links: Optional[Dict[str, str]] = Field(
        default=None, description="Enlaces relacionados"
    )


class UnitSearchResponse(PaginationResponse):
    """Respuesta de búsqueda de unidades"""

    units: List[UnitDetailResponse] = Field(description="Lista de unidades encontradas")
