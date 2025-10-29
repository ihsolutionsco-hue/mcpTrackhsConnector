"""
Schemas para amenidades
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseSchema, PaginationParams, PaginationResponse


class AmenitySearchParams(PaginationParams):
    """Parámetros de búsqueda de amenidades"""

    search: Optional[str] = Field(
        default=None, max_length=200, description="Búsqueda en nombre de amenidad"
    )
    group_id: Optional[int] = Field(
        default=None, gt=0, description="ID del grupo de amenidades"
    )
    is_public: Optional[bool] = Field(
        default=None, description="Solo amenidades públicas"
    )
    public_searchable: Optional[bool] = Field(
        default=None, description="Solo amenidades buscables públicamente"
    )
    is_filterable: Optional[bool] = Field(
        default=None, description="Solo amenidades filtrables"
    )
    homeaway_type: Optional[str] = Field(
        default=None, max_length=200, description="Tipo de HomeAway"
    )
    airbnb_type: Optional[str] = Field(
        default=None, max_length=200, description="Tipo de Airbnb"
    )
    tripadvisor_type: Optional[str] = Field(
        default=None, max_length=200, description="Tipo de TripAdvisor"
    )
    marriott_type: Optional[str] = Field(
        default=None, max_length=200, description="Tipo de Marriott"
    )
    sort_column: Optional[str] = Field(
        default="order", description="Columna para ordenar"
    )
    sort_direction: Optional[str] = Field(
        default="asc", description="Dirección de ordenamiento"
    )


class AmenityDetailResponse(BaseModel):
    """Respuesta detallada de amenidad"""

    id: int = Field(description="ID de la amenidad")
    name: str = Field(description="Nombre de la amenidad")
    description: Optional[str] = Field(default=None, description="Descripción")
    group_id: Optional[int] = Field(default=None, description="ID del grupo")
    group_name: Optional[str] = Field(default=None, description="Nombre del grupo")
    order: Optional[int] = Field(default=None, description="Orden de visualización")
    is_public: Optional[bool] = Field(default=None, description="Amenidad pública")
    public_searchable: Optional[bool] = Field(
        default=None, description="Buscable públicamente"
    )
    is_filterable: Optional[bool] = Field(default=None, description="Filtrable")

    # Tipos de plataformas OTA
    homeaway_type: Optional[str] = Field(default=None, description="Tipo de HomeAway")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo de Airbnb")
    tripadvisor_type: Optional[str] = Field(
        default=None, description="Tipo de TripAdvisor"
    )
    marriott_type: Optional[str] = Field(default=None, description="Tipo de Marriott")

    # Metadatos
    created_at: Optional[str] = Field(default=None, description="Fecha de creación")
    updated_at: Optional[str] = Field(
        default=None, description="Fecha de actualización"
    )

    # Enlaces
    links: Optional[Dict[str, str]] = Field(
        default=None, description="Enlaces relacionados"
    )


class AmenitySearchResponse(PaginationResponse):
    """Respuesta de búsqueda de amenidades"""

    amenities: List[AmenityDetailResponse] = Field(
        description="Lista de amenidades encontradas"
    )
