"""
Esquema de datos para Units API
Proporciona información detallada sobre la estructura de datos de unidades
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


def register_units_schema(mcp, api_client):
    """Registra el schema de units como resource MCP"""

    @mcp.resource("trackhs://schema/units")
    def units_schema():
        """
        Esquema completo de datos para Units API de Track HS Channel API.

        Este resource proporciona información detallada sobre la estructura
        de datos de unidades, incluyendo todos los campos disponibles,
        tipos de datos, validaciones y ejemplos de uso.

        **Información del Endpoint:**
        - URL: /pms/units
        - Método: GET
        - API: Channel API
        - Autenticación: Basic Auth o HMAC

        **Características Principales:**
        - ✅ 50+ campos de datos por unidad
        - ✅ Información completa de ubicación y contacto
        - ✅ Características físicas (habitaciones, baños, amenidades)
        - ✅ Políticas y reglas (mascotas, eventos, edad mínima)
        - ✅ Horarios de check-in/check-out
        - ✅ Datos embebidos (tipos, amenidades, habitaciones)
        - ✅ Paginación y navegación
        - ✅ Filtros avanzados (29+ parámetros)

        **Estructura de Datos:**
        - Información básica: id, name, shortName, unitCode
        - Ubicación: streetAddress, locality, region, country, coordinates
        - Características: bedrooms, bathrooms, maxOccupancy, area
        - Políticas: petsFriendly, eventsAllowed, smokingAllowed, childrenAllowed
        - Horarios: checkinTime, checkoutTime, timezone
        - Amenidades: amenities array con grupos y categorías
        - Habitaciones: rooms array con tipos y capacidades
        - Tipos de cama: bedTypes array con mapeos para OTAs
        - Datos personalizados: custom fields por cliente
        - Metadatos: updatedAt, links, embedded data

        **Filtros Disponibles:**
        - Paginación: page, size (limitado a 10k resultados)
        - Ordenamiento: sortColumn, sortDirection
        - Búsqueda: search, term, unitCode, shortName
        - Ubicación: nodeId, amenityId, unitTypeId
        - Características: bedrooms, bathrooms (rangos y exactos)
        - Políticas: petsFriendly, eventsAllowed, smokingAllowed
        - Estado: isActive, isBookable, unitStatus
        - Disponibilidad: arrival, departure
        - Actualización: contentUpdatedSince, updatedSince

        **Valores Booleanos:**
        La API espera valores 0/1 para parámetros booleanos:
        - petsFriendly: 0 (no) / 1 (sí)
        - eventsAllowed: 0 (no) / 1 (sí)
        - smokingAllowed: 0 (no) / 1 (sí)
        - childrenAllowed: 0 (no) / 1 (sí)
        - isActive: 0 (inactivo) / 1 (activo)
        - isBookable: 0 (no reservable) / 1 (reservable)

        **Campos Deprecados:**
        - unitType: Usar link a unit types API
        - coverImage: Usar images API
        - regulations: Campo deprecated
        - updatedSince: Usar contentUpdatedSince

        **Limitaciones:**
        - Máximo 10,000 resultados totales (page * size)
        - Máximo 1,000 unidades por página
        - Campos unitType y customData son inestables

        **Ejemplos de Uso:**

        # Búsqueda básica
        GET /pms/units?page=0&size=25

        # Filtro por características
        GET /pms/units?bedrooms=2&bathrooms=2&petsFriendly=1

        # Búsqueda por disponibilidad
        GET /pms/units?arrival=2024-01-01&departure=2024-01-07&isBookable=1

        # Filtro por amenidades
        GET /pms/units?amenityId=1,2,3&petsFriendly=1

        **Respuesta Típica:**
        ```json
        {
          "_embedded": {
            "units": [
              {
                "id": 7,
                "name": "Townhome 444",
                "shortName": "TH444",
                "unitCode": "TH444",
                "nodeId": 81,
                "bedrooms": 3,
                "fullBathrooms": 3,
                "maxOccupancy": 12,
                "petsFriendly": true,
                "eventsAllowed": false,
                "smokingAllowed": false,
                "childrenAllowed": true,
                "minimumAgeLimit": 25,
                "isAccessible": false,
                "updatedAt": "2020-05-21T22:30:18-06:00"
              }
            ]
          },
          "page": 0,
          "page_count": 13,
          "page_size": 25,
          "total_items": 304,
          "_links": {
            "self": {"href": "https://api.example.com/api/pms/units/?page=0"},
            "first": {"href": "https://api.example.com/api/pms/units/"},
            "last": {"href": "https://api.example.com/api/pms/units/?page=12"},
            "next": {"href": "https://api.example.com/api/pms/units/?page=1"}
          }
        }
        ```

        **Mejores Prácticas:**
        - Usar filtros específicos para reducir resultados
        - Implementar paginación para grandes conjuntos de datos
        - Validar formatos de fecha ISO 8601
        - Manejar errores de autenticación apropiadamente
        - Usar valores booleanos 0/1 en lugar de true/false
        - Evitar campos deprecated
        - Implementar caché para consultas frecuentes
        """
        return {
            "schema": "units",
            "version": "1.0",
            "api": "Channel API",
            "endpoint": "/pms/units",
            "method": "GET",
            "authentication": ["Basic Auth", "HMAC"],
            "description": "Esquema completo de datos para Units API de Track HS",
            "features": [
                "50+ campos de datos por unidad",
                "Información completa de ubicación y contacto",
                "Características físicas (habitaciones, baños, amenidades)",
                "Políticas y reglas (mascotas, eventos, edad mínima)",
                "Horarios de check-in/check-out",
                "Datos embebidos (tipos, amenidades, habitaciones)",
                "Paginación y navegación",
                "Filtros avanzados (29+ parámetros)",
            ],
            "data_structure": {
                "basic_info": ["id", "name", "shortName", "unitCode", "headline"],
                "location": [
                    "streetAddress",
                    "locality",
                    "region",
                    "country",
                    "latitude",
                    "longitude",
                ],
                "characteristics": [
                    "bedrooms",
                    "bathrooms",
                    "maxOccupancy",
                    "area",
                    "floors",
                ],
                "policies": [
                    "petsFriendly",
                    "eventsAllowed",
                    "smokingAllowed",
                    "childrenAllowed",
                ],
                "schedules": [
                    "checkinTime",
                    "checkoutTime",
                    "timezone",
                    "hasEarlyCheckin",
                    "hasLateCheckout",
                ],
                "amenities": ["amenities", "amenityDescription"],
                "rooms": ["rooms", "bedTypes"],
                "custom": ["custom", "localOffice"],
                "metadata": ["updatedAt", "links", "embedded"],
            },
            "filters": {
                "pagination": ["page", "size"],
                "sorting": ["sortColumn", "sortDirection"],
                "search": ["search", "term", "unitCode", "shortName"],
                "location": ["nodeId", "amenityId", "unitTypeId"],
                "characteristics": [
                    "bedrooms",
                    "bathrooms",
                    "minBedrooms",
                    "maxBedrooms",
                ],
                "policies": ["petsFriendly", "eventsAllowed", "smokingAllowed"],
                "status": ["isActive", "isBookable", "unitStatus"],
                "availability": ["arrival", "departure"],
                "updates": ["contentUpdatedSince", "updatedSince"],
            },
            "boolean_values": {
                "petsFriendly": "0 (no) / 1 (sí)",
                "eventsAllowed": "0 (no) / 1 (sí)",
                "smokingAllowed": "0 (no) / 1 (sí)",
                "childrenAllowed": "0 (no) / 1 (sí)",
                "isActive": "0 (inactivo) / 1 (activo)",
                "isBookable": "0 (no reservable) / 1 (reservable)",
            },
            "deprecated_fields": [
                "unitType (usar link a unit types API)",
                "coverImage (usar images API)",
                "regulations (campo deprecated)",
                "updatedSince (usar contentUpdatedSince)",
            ],
            "limitations": {
                "max_total_results": 10000,
                "max_page_size": 1000,
                "unstable_fields": ["unitType", "customData"],
            },
            "examples": {
                "basic_search": "GET /pms/units?page=0&size=25",
                "filter_by_features": "GET /pms/units?bedrooms=2&bathrooms=2&petsFriendly=1",
                "availability_search": "GET /pms/units?arrival=2024-01-01&departure=2024-01-07&isBookable=1",
                "amenity_filter": "GET /pms/units?amenityId=1,2,3&petsFriendly=1",
            },
            "best_practices": [
                "Usar filtros específicos para reducir resultados",
                "Implementar paginación para grandes conjuntos de datos",
                "Validar formatos de fecha ISO 8601",
                "Manejar errores de autenticación apropiadamente",
                "Usar valores booleanos 0/1 en lugar de true/false",
                "Evitar campos deprecated",
                "Implementar caché para consultas frecuentes",
            ],
        }


class UnitSchema(BaseModel):
    """Esquema completo de datos para una unidad"""

    # Información básica
    id: int = Field(..., description="ID único de la unidad")
    name: str = Field(..., description="Nombre de la unidad")
    short_name: Optional[str] = Field(default=None, description="Nombre corto")
    unit_code: Optional[str] = Field(default=None, description="Código de la unidad")
    headline: Optional[str] = Field(default=None, description="Título")
    short_description: Optional[str] = Field(
        default=None, description="Descripción corta"
    )
    long_description: Optional[str] = Field(
        default=None, description="Descripción larga"
    )
    house_rules: Optional[str] = Field(default=None, description="Reglas de la casa")

    # Ubicación y nodo
    node_id: int = Field(..., description="ID del nodo")
    directions: Optional[str] = Field(default=None, description="Direcciones")
    checkin_details: Optional[str] = Field(
        default=None, description="Detalles de check-in"
    )
    timezone: str = Field(..., description="Zona horaria")

    # Horarios
    checkin_time: str = Field(..., description="Hora de check-in")
    has_early_checkin: bool = Field(..., description="Permite check-in temprano")
    early_checkin_time: Optional[str] = Field(
        default=None, description="Hora de check-in temprano"
    )
    checkout_time: str = Field(..., description="Hora de check-out")
    has_late_checkout: bool = Field(..., description="Permite check-out tardío")
    late_checkout_time: Optional[str] = Field(
        default=None, description="Hora de check-out tardío"
    )

    # Ventanas de reserva
    min_booking_window: Optional[int] = Field(
        default=None, description="Ventana mínima de reserva"
    )
    max_booking_window: Optional[int] = Field(
        default=None, description="Ventana máxima de reserva"
    )

    # Contacto
    website: Optional[str] = Field(default=None, description="Sitio web")
    phone: Optional[str] = Field(default=None, description="Teléfono")

    # Dirección
    street_address: str = Field(..., description="Dirección")
    extended_address: Optional[str] = Field(
        default=None, description="Dirección extendida"
    )
    locality: str = Field(..., description="Localidad")
    region: str = Field(..., description="Región")
    postal: str = Field(..., description="Código postal")
    country: str = Field(..., description="País")
    latitude: Optional[float] = Field(default=None, description="Latitud")
    longitude: Optional[float] = Field(default=None, description="Longitud")

    # Políticas
    pets_friendly: bool = Field(..., description="Permite mascotas")
    max_pets: Optional[int] = Field(default=None, description="Máximo de mascotas")
    events_allowed: bool = Field(..., description="Permite eventos")
    smoking_allowed: bool = Field(..., description="Permite fumar")
    children_allowed: bool = Field(..., description="Permite niños")
    minimum_age_limit: Optional[int] = Field(default=None, description="Edad mínima")
    is_accessible: bool = Field(..., description="Es accesible")

    # Características físicas
    area: Optional[int] = Field(default=None, description="Área")
    floors: Optional[int] = Field(default=None, description="Pisos")
    max_occupancy: int = Field(..., description="Ocupación máxima")
    security_deposit: Optional[str] = Field(
        default=None, description="Depósito de seguridad"
    )

    # Habitaciones y baños
    bedrooms: int = Field(..., description="Habitaciones")
    full_bathrooms: int = Field(..., description="Baños completos")
    three_quarter_bathrooms: Optional[int] = Field(
        default=None, description="Baños de 3/4"
    )
    half_bathrooms: int = Field(..., description="Medios baños")

    # Tipos y amenidades
    unit_type: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de unidad (deprecated)"
    )
    lodging_type: Optional[Dict[str, Any]] = Field(
        default=None, description="Tipo de alojamiento"
    )
    bed_types: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Tipos de cama"
    )
    rooms: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Habitaciones"
    )
    amenities: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Amenidades"
    )
    amenity_description: Optional[str] = Field(
        default=None, description="Descripción de amenidades"
    )

    # Campos personalizados y adicionales
    custom: Optional[Dict[str, Any]] = Field(
        default=None, description="Campos personalizados"
    )
    cover_image: Optional[str] = Field(
        default=None, description="Imagen de portada (deprecated)"
    )
    tax_id: Optional[str] = Field(default=None, description="ID de impuesto")
    local_office: Optional[Dict[str, Any]] = Field(
        default=None, description="Oficina local"
    )
    regulations: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Regulaciones (deprecated)"
    )

    # Metadatos
    updated_at: str = Field(..., description="Fecha de actualización")
    embedded: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos embebidos"
    )
    links: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, description="Enlaces"
    )


class SearchUnitsParamsSchema(BaseModel):
    """Esquema de parámetros para búsqueda de unidades"""

    # Paginación
    page: int = Field(default=0, description="Número de página (0-based)")
    size: int = Field(default=25, description="Tamaño de página (máximo 1000)")

    # Ordenamiento
    sort_column: Literal["id", "name", "nodeName", "unitTypeName"] = Field(
        default="name", description="Columna para ordenar"
    )
    sort_direction: Literal["asc", "desc"] = Field(
        default="asc", description="Dirección de ordenamiento"
    )

    # Búsqueda
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

    # Filtros por ID
    node_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del nodo"
    )
    amenity_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) de amenidad"
    )
    unit_type_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID(s) del tipo de unidad"
    )
    id: Optional[List[int]] = Field(
        default=None, description="IDs específicos de unidades"
    )
    calendar_id: Optional[int] = Field(default=None, description="ID del calendario")
    role_id: Optional[int] = Field(default=None, description="ID del rol")

    # Filtros de habitaciones y baños
    bedrooms: Optional[int] = Field(
        default=None, description="Número exacto de habitaciones"
    )
    min_bedrooms: Optional[int] = Field(
        default=None, description="Mínimo de habitaciones"
    )
    max_bedrooms: Optional[int] = Field(
        default=None, description="Máximo de habitaciones"
    )
    bathrooms: Optional[int] = Field(default=None, description="Número exacto de baños")
    min_bathrooms: Optional[int] = Field(default=None, description="Mínimo de baños")
    max_bathrooms: Optional[int] = Field(default=None, description="Máximo de baños")

    # Filtros booleanos
    pets_friendly: Optional[Literal[0, 1]] = Field(
        default=None, description="Permite mascotas (0/1)"
    )
    allow_unit_rates: Optional[Literal[0, 1]] = Field(
        default=None, description="Permite tarifas de unidad (0/1)"
    )
    computed: Optional[Literal[0, 1]] = Field(
        default=None, description="Valores computados (0/1)"
    )
    inherited: Optional[Literal[0, 1]] = Field(
        default=None, description="Atributos heredados (0/1)"
    )
    limited: Optional[Literal[0, 1]] = Field(
        default=None, description="Atributos limitados (0/1)"
    )
    is_bookable: Optional[Literal[0, 1]] = Field(
        default=None, description="Es reservable (0/1)"
    )
    include_descriptions: Optional[Literal[0, 1]] = Field(
        default=None, description="Incluir descripciones (0/1)"
    )
    is_active: Optional[Literal[0, 1]] = Field(
        default=None, description="Está activo (0/1)"
    )

    # Filtros de fechas
    arrival: Optional[str] = Field(
        default=None, description="Fecha de llegada (ISO 8601)"
    )
    departure: Optional[str] = Field(
        default=None, description="Fecha de salida (ISO 8601)"
    )
    content_updated_since: Optional[str] = Field(
        default=None, description="Actualización de contenido desde (ISO 8601)"
    )
    updated_since: Optional[str] = Field(
        default=None, description="Actualización desde (ISO 8601) - deprecated"
    )

    # Estado
    unit_status: Optional[
        Literal["clean", "dirty", "occupied", "inspection", "inprogress"]
    ] = Field(default=None, description="Estado de la unidad")


class SearchUnitsResponseSchema(BaseModel):
    """Esquema de respuesta para búsqueda de unidades"""

    embedded: Dict[str, List[UnitSchema]] = Field(
        ..., description="Datos embebidos con array de unidades"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    links: Dict[str, Dict[str, str]] = Field(..., description="Enlaces de navegación")


class UnitFiltersSchema(BaseModel):
    """Esquema de filtros para unidades"""

    status: Optional[
        Literal["clean", "dirty", "occupied", "inspection", "inprogress"]
    ] = Field(default=None, description="Estado de la unidad")
    property_id: Optional[str] = Field(default=None, description="ID de la propiedad")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")
    unit_code: Optional[str] = Field(default=None, description="Código de unidad")
    node_id: Optional[int] = Field(default=None, description="ID del nodo")


# Esquemas de referencia para documentación
class UnitTypeReference(BaseModel):
    """Referencia de tipo de unidad"""

    id: int = Field(..., description="ID del tipo")
    name: str = Field(..., description="Nombre del tipo")


class LodgingTypeReference(BaseModel):
    """Referencia de tipo de alojamiento"""

    id: int = Field(..., description="ID del tipo")
    name: str = Field(..., description="Nombre del tipo")


class AmenityReference(BaseModel):
    """Referencia de amenidad"""

    id: int = Field(..., description="ID de la amenidad")
    name: str = Field(..., description="Nombre de la amenidad")
    group: Dict[str, Any] = Field(..., description="Grupo de la amenidad")


class RoomReference(BaseModel):
    """Referencia de habitación"""

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
    beds: List[Dict[str, Any]] = Field(..., description="Camas en la habitación")


class BedTypeReference(BaseModel):
    """Referencia de tipo de cama"""

    id: int = Field(..., description="ID del tipo de cama")
    name: str = Field(..., description="Nombre del tipo de cama")
    count: int = Field(..., description="Cantidad de camas")
    airbnb_type: Optional[str] = Field(default=None, description="Tipo para Airbnb")
    homeaway_type: Optional[str] = Field(default=None, description="Tipo para HomeAway")
    marriott_type: Optional[str] = Field(default=None, description="Tipo para Marriott")
