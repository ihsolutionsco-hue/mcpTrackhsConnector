"""
Modelos Pydantic para Amenities de Track HS Channel API
Basado en la especificación completa de la API Get Unit Amenities Collection
"""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class AmenityGroup(BaseModel):
    """Modelo para grupo de amenidades"""

    id: int = Field(..., description="ID del grupo")
    name: str = Field(..., description="Nombre del grupo")


class UnitAmenity(BaseModel):
    """Modelo para amenidad individual"""

    id: int = Field(..., description="ID de la amenidad")
    name: str = Field(..., description="Nombre de la amenidad")
    group_id: int = Field(..., alias="groupId", description="ID del grupo")
    group_name: str = Field(..., alias="groupName", description="Nombre del grupo")
    homeaway_type: Optional[str] = Field(
        default=None, alias="homeawayType", description="Tipo para HomeAway"
    )
    airbnb_type: Optional[str] = Field(
        default=None, alias="airbnbType", description="Tipo para Airbnb"
    )
    tripadvisor_type: Optional[str] = Field(
        default=None, alias="tripadvisorType", description="Tipo para TripAdvisor"
    )
    updated_at: str = Field(
        ..., alias="updatedAt", description="Fecha de actualización"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class SearchAmenitiesParams(PaginationParams, SearchParams):
    """Parámetros para buscar amenidades - Basado en la especificación completa"""

    sort_column: Optional[
        Literal[
            "id", "order", "isPublic", "publicSearchable", "isFilterable", "createdAt"
        ]
    ] = Field(default="order", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    search: Optional[str] = Field(default=None, description="Búsqueda en id y/o name")
    group_id: Optional[int] = Field(default=None, description="Filtro por ID de grupo")
    is_public: Optional[int] = Field(
        default=None, description="Filtro por amenidades públicas (0/1)"
    )
    public_searchable: Optional[int] = Field(
        default=None, description="Filtro por amenidades buscables públicamente (0/1)"
    )
    is_filterable: Optional[int] = Field(
        default=None, description="Filtro por amenidades filtrables (0/1)"
    )


class SearchAmenitiesResponse(BaseModel):
    """Respuesta de búsqueda de amenidades"""

    model_config = {"populate_by_name": True}

    embedded: Dict[str, List[UnitAmenity]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., alias="page_count", description="Total de páginas")
    page_size: int = Field(..., alias="page_size", description="Tamaño de página")
    total_items: int = Field(..., alias="total_items", description="Total de elementos")
    links: Dict[str, Dict[str, str]] = Field(..., alias="_links", description="Enlaces")


class GetAmenityParams(BaseModel):
    """Parámetros para obtener una amenidad específica"""

    amenity_id: int = Field(..., description="ID de la amenidad")


class AmenityResponse(BaseModel):
    """Respuesta de una amenidad específica"""

    data: UnitAmenity = Field(..., description="Datos de la amenidad")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")


class AmenityFilters(BaseModel):
    """Filtros para amenidades"""

    group_id: Optional[int] = Field(default=None, description="ID del grupo")
    is_public: Optional[int] = Field(default=None, description="Es pública (0/1)")
    public_searchable: Optional[int] = Field(
        default=None, description="Es buscable públicamente (0/1)"
    )
    is_filterable: Optional[int] = Field(default=None, description="Es filtrable (0/1)")
    search: Optional[str] = Field(default=None, description="Búsqueda por nombre")
