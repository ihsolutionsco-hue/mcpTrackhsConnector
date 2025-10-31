"""
Schemas para unidades de alojamiento
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .base import BaseSchema, PaginationParams, PaginationResponse


class UnitStatus(str, Enum):
    """Estados válidos para unidades"""

    CLEAN = "clean"
    DIRTY = "dirty"
    OCCUPIED = "occupied"
    INSPECTION = "inspection"
    INPROGRESS = "inprogress"


class SortColumn(str, Enum):
    """Columnas válidas para ordenamiento"""

    ID = "id"
    NAME = "name"
    NODE_NAME = "nodeName"
    UNIT_TYPE_NAME = "unitTypeName"


class SortDirection(str, Enum):
    """Direcciones válidas para ordenamiento"""

    ASC = "asc"
    DESC = "desc"


class UnitSearchParams(PaginationParams):
    """Parámetros de búsqueda de unidades - Implementación completa de la API TrackHS"""

    # Parámetros de búsqueda de texto
    search: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Búsqueda de texto en nombre o descripciones",
    )
    term: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Búsqueda de texto en término específico",
    )
    unit_code: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Búsqueda en código de unidad (exacta o con % para wildcard)",
    )
    short_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Búsqueda en nombre corto (exacta o con % para wildcard)",
    )

    # Parámetros de características físicas
    # Usar str para que schema MCP acepte strings, field_validator convierte a int
    bedrooms: Optional[str] = Field(
        default=None, description="Número exacto de dormitorios"
    )
    min_bedrooms: Optional[str] = Field(
        default=None, description="Número mínimo de dormitorios"
    )
    max_bedrooms: Optional[str] = Field(
        default=None, description="Número máximo de dormitorios"
    )
    bathrooms: Optional[str] = Field(default=None, description="Número exacto de baños")
    min_bathrooms: Optional[str] = Field(
        default=None, description="Número mínimo de baños"
    )
    max_bathrooms: Optional[str] = Field(
        default=None, description="Número máximo de baños"
    )
    occupancy: Optional[str] = Field(default=None, description="Capacidad exacta")
    min_occupancy: Optional[str] = Field(default=None, description="Capacidad mínima")
    max_occupancy: Optional[str] = Field(default=None, description="Capacidad máxima")

    # Parámetros de estado
    # Usar str para que schema MCP acepte strings, field_validator convierte a bool
    is_active: Optional[str] = Field(
        default=None, description="Solo unidades activas (1) o inactivas (0)"
    )
    is_bookable: Optional[str] = Field(
        default=None, description="Solo unidades reservables (1) o no (0)"
    )
    pets_friendly: Optional[str] = Field(
        default=None, description="Solo unidades pet-friendly (1) o no (0)"
    )
    unit_status: Optional[UnitStatus] = Field(
        default=None, description="Estado de la unidad"
    )
    allow_unit_rates: Optional[str] = Field(
        default=None,
        description="Solo unidades que permiten tarifas por unidad (1) o no (0)",
    )

    # Parámetros de disponibilidad
    arrival: Optional[str] = Field(
        default=None,
        description="Fecha de llegada (YYYY-MM-DD) para verificar disponibilidad",
    )
    departure: Optional[str] = Field(
        default=None,
        description="Fecha de salida (YYYY-MM-DD) para verificar disponibilidad",
    )

    # Parámetros de contenido
    computed: Optional[str] = Field(
        default=None, description="Incluir valores computados adicionales (1) o no (0)"
    )
    inherited: Optional[str] = Field(
        default=None, description="Incluir atributos heredados (1) o no (0)"
    )
    limited: Optional[str] = Field(
        default=None, description="Retornar atributos limitados (1) o completos (0)"
    )
    include_descriptions: Optional[str] = Field(
        default=None, description="Incluir descripciones de unidades (1) o no (0)"
    )
    content_updated_since: Optional[str] = Field(
        default=None,
        description="Fecha ISO 8601 - unidades con cambios desde esta fecha",
    )

    # Parámetros de IDs
    # Usar str para que schema MCP acepte strings, field_validator convierte a List[int]
    amenity_id: Optional[str] = Field(
        default=None,
        description="IDs de amenidades - unidades que tienen estas amenidades",
    )
    node_id: Optional[str] = Field(
        default=None, description="IDs de nodo - unidades descendientes"
    )
    unit_type_id: Optional[str] = Field(
        default=None, description="IDs de tipo de unidad"
    )
    owner_id: Optional[str] = Field(default=None, description="IDs del propietario")
    company_id: Optional[str] = Field(default=None, description="IDs de la empresa")
    channel_id: Optional[str] = Field(default=None, description="IDs del canal activo")
    lodging_type_id: Optional[str] = Field(
        default=None, description="IDs del tipo de alojamiento"
    )
    bed_type_id: Optional[str] = Field(default=None, description="IDs del tipo de cama")
    amenity_all: Optional[str] = Field(
        default=None, description="Filtrar unidades que tengan TODAS estas amenidades"
    )
    unit_ids: Optional[str] = Field(
        default=None, description="Filtrar por IDs específicos de unidades"
    )
    calendar_id: Optional[str] = Field(
        default=None, description="ID del grupo de calendario"
    )
    role_id: Optional[str] = Field(default=None, description="ID del rol específico")

    # Parámetros de ordenamiento
    sort_column: Optional[SortColumn] = Field(
        default=SortColumn.NAME, description="Columna para ordenar resultados"
    )
    sort_direction: Optional[SortDirection] = Field(
        default=SortDirection.ASC, description="Dirección de ordenamiento"
    )

    # Sin validadores: aceptar strings, convertir en build_units_query cuando sea necesario


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

    # Campos opcionales que pueden venir de la API
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos embebidos de la API"
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos adicionales de la API"
    )

    model_config = ConfigDict(extra="allow")  # Permitir campos adicionales de la API
