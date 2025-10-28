"""
Esquemas Pydantic para TrackHS MCP Server
Define enums, modelos y esquemas de salida para validación robusta

MEJORES PRÁCTICAS IMPLEMENTADAS:
- Un solo modelo Pydantic por entidad (DRY)
- Schemas JSON generados automáticamente desde modelos
- Validación estricta con mensajes claros
- Documentación completa para LLMs
- Tipos consistentes en toda la aplicación
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

# =============================================================================
# ENUMS Y CONSTANTES
# =============================================================================


class WorkOrderPriority(int, Enum):
    """Prioridades para órdenes de trabajo"""

    LOW = 1
    MEDIUM = 3
    HIGH = 5


class MaintenanceWorkOrderStatus(str, Enum):
    """Estados para órdenes de mantenimiento"""

    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class HousekeepingWorkOrderStatus(str, Enum):
    """Estados para órdenes de housekeeping"""

    PENDING = "pending"
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    PROCESSED = "processed"
    CANCELLED = "cancelled"
    EXCEPTION = "exception"


# =============================================================================
# MODELOS PRINCIPALES - UNA SOLA FUENTE DE VERDAD
# =============================================================================


class ReservationResponse(BaseModel):
    """Modelo completo para respuesta de reserva individual - UNA SOLA FUENTE DE VERDAD"""

    id: int = Field(description="ID único de la reserva")
    confirmation_number: Optional[str] = Field(
        None, description="Número de confirmación de la reserva"
    )
    status: Optional[str] = Field(None, description="Estado actual de la reserva")
    arrival_date: Optional[str] = Field(
        None, description="Fecha de llegada (YYYY-MM-DD)"
    )
    departure_date: Optional[str] = Field(
        None, description="Fecha de salida (YYYY-MM-DD)"
    )

    # Información del huésped
    guest: Optional[Dict[str, Any]] = Field(None, description="Información del huésped")

    # Información de la unidad
    unit: Optional[Dict[str, Any]] = Field(
        None, description="Información de la unidad reservada"
    )

    # Información financiera
    financial: Optional[Dict[str, Any]] = Field(
        None, description="Información financiera"
    )

    # Enlaces HATEOAS
    links: Optional[Dict[str, Any]] = Field(
        None, alias="_links", description="Enlaces a recursos relacionados"
    )

    model_config = {
        "extra": "allow",  # Permitir campos adicionales de la API
        "populate_by_name": True,  # Permitir alias
        "validate_assignment": True,  # Validar asignaciones
    }

    @field_validator("confirmation_number")
    @classmethod
    def validate_confirmation_number(cls, v):
        """Asegurar que confirmation_number sea string o None"""
        if v is not None and not isinstance(v, str):
            return str(v)
        return v

    @field_validator("arrival_date", "departure_date")
    @classmethod
    def validate_dates(cls, v):
        """Validar formato de fechas"""
        if v is not None and not isinstance(v, str):
            return str(v)
        return v


class UnitResponse(BaseModel):
    """Modelo completo para respuesta de unidad - UNA SOLA FUENTE DE VERDAD"""

    id: int = Field(description="ID único de la unidad")
    name: Optional[str] = Field(None, description="Nombre de la unidad")
    code: Optional[str] = Field(None, description="Código de la unidad")
    bedrooms: Optional[int] = Field(
        None, ge=0, le=20, description="Número de dormitorios"
    )
    bathrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de baños")
    max_occupancy: Optional[int] = Field(
        None, ge=1, description="Capacidad máxima de huéspedes"
    )
    area: Optional[Union[float, int, None]] = Field(
        None, description="Área en metros cuadrados"
    )
    address: Optional[str] = Field(None, description="Dirección completa de la unidad")
    is_active: Optional[bool] = Field(None, description="Si la unidad está activa")
    is_bookable: Optional[bool] = Field(
        None, description="Si la unidad está disponible para reservar"
    )
    amenities: Optional[List[str]] = Field(
        None, description="Lista de amenidades disponibles"
    )

    # Enlaces HATEOAS
    links: Optional[Dict[str, Any]] = Field(
        None, alias="_links", description="Enlaces a recursos relacionados"
    )

    model_config = {
        "extra": "allow",
        "populate_by_name": True,
        "validate_assignment": True,
    }

    @field_validator("bedrooms", "bathrooms", "max_occupancy")
    @classmethod
    def validate_positive_integers(cls, v):
        """Asegurar que los números sean enteros positivos o None"""
        if v is not None and not isinstance(v, int):
            try:
                return int(v)
            except (ValueError, TypeError):
                return None
        return v

    @field_validator("area")
    @classmethod
    def validate_area(cls, v):
        """Asegurar que el área sea un número o None"""
        if v is not None:
            try:
                # Convertir string a float si es necesario
                if isinstance(v, str):
                    # Limpiar string de caracteres no numéricos
                    cleaned = "".join(c for c in v if c.isdigit() or c in ".-")
                    if cleaned:
                        return float(cleaned)
                    return None
                return float(v)
            except (ValueError, TypeError):
                return None
        return v


class FolioResponse(BaseModel):
    """Modelo completo para respuesta de folio - UNA SOLA FUENTE DE VERDAD"""

    reservation_id: int = Field(description="ID de la reserva asociada")
    balance: Optional[float] = Field(None, description="Balance total pendiente")
    charges: Optional[List[Dict[str, Any]]] = Field(
        None, description="Lista de cargos aplicados"
    )
    payments: Optional[List[Dict[str, Any]]] = Field(
        None, description="Lista de pagos recibidos"
    )
    summary: Optional[Dict[str, Any]] = Field(None, description="Resumen financiero")

    # Enlaces HATEOAS
    links: Optional[Dict[str, Any]] = Field(
        None, alias="_links", description="Enlaces a recursos relacionados"
    )

    model_config = {
        "extra": "allow",
        "populate_by_name": True,
        "validate_assignment": True,
    }

    @field_validator("balance")
    @classmethod
    def validate_balance(cls, v):
        """Asegurar que balance sea float o None"""
        if v is not None and not isinstance(v, (int, float)):
            try:
                return float(v)
            except (ValueError, TypeError):
                return None
        return v


class WorkOrderResponse(BaseModel):
    """Modelo completo para respuesta de work order - UNA SOLA FUENTE DE VERDAD"""

    id: int = Field(description="ID único de la orden de trabajo")
    status: Optional[str] = Field(None, description="Estado actual de la orden")
    unit_id: Optional[int] = Field(None, description="ID de la unidad asociada")
    priority: Optional[int] = Field(
        None, ge=1, le=5, description="Prioridad (1=Baja, 3=Media, 5=Alta)"
    )
    summary: Optional[str] = Field(None, description="Resumen del trabajo")
    description: Optional[str] = Field(None, description="Descripción detallada")
    estimated_cost: Optional[float] = Field(None, ge=0, description="Costo estimado")
    estimated_time: Optional[int] = Field(
        None, ge=0, description="Tiempo estimado en minutos"
    )
    date_received: Optional[str] = Field(None, description="Fecha de recepción")
    date_completed: Optional[str] = Field(None, description="Fecha de finalización")
    assigned_to: Optional[str] = Field(None, description="Usuario asignado")
    vendor: Optional[str] = Field(None, description="Proveedor asignado")

    # Enlaces HATEOAS
    links: Optional[Dict[str, Any]] = Field(
        None, alias="_links", description="Enlaces a recursos relacionados"
    )

    model_config = {
        "extra": "allow",
        "populate_by_name": True,
        "validate_assignment": True,
    }

    @field_validator("unit_id")
    @classmethod
    def validate_unit_id(cls, v):
        """Asegurar que unit_id sea entero positivo o None"""
        if v is not None and not isinstance(v, int):
            try:
                return int(v)
            except (ValueError, TypeError):
                return None
        return v


# =============================================================================
# GENERACIÓN AUTOMÁTICA DE SCHEMAS JSON DESDE MODELOS PYDANTIC
# =============================================================================


def generate_json_schema(model_class: type) -> Dict[str, Any]:
    """
    Genera schema JSON automáticamente desde un modelo Pydantic.

    MEJOR PRÁCTICA: Un solo modelo Pydantic, schema JSON generado automáticamente.
    Evita duplicación y mantiene consistencia.
    """
    return model_class.model_json_schema()


def generate_collection_schema(item_model: type) -> Dict[str, Any]:
    """
    Genera schema para colecciones paginadas.

    Args:
        item_model: Modelo Pydantic para los elementos de la colección

    Returns:
        Schema JSON para colección paginada
    """
    return {
        "type": "object",
        "properties": {
            "page": {"type": "integer", "description": "Página actual"},
            "page_count": {"type": "integer", "description": "Total de páginas"},
            "page_size": {"type": "integer", "description": "Tamaño de página"},
            "total_items": {"type": "integer", "description": "Total de elementos"},
            "_embedded": {
                "type": "object",
                "description": "Datos embebidos de la respuesta",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": generate_json_schema(item_model),
                        "description": f"Lista de {item_model.__name__.lower().replace('response', 's')}",
                    }
                },
            },
            "_links": {
                "type": "object",
                "description": "Enlaces de navegación HATEOAS",
            },
        },
        "required": [
            "page",
            "page_count",
            "page_size",
            "total_items",
            "_embedded",
            "_links",
        ],
    }


# =============================================================================
# SCHEMAS GENERADOS AUTOMÁTICAMENTE - UNA SOLA FUENTE DE VERDAD
# =============================================================================

# Schemas de respuestas individuales
RESERVATION_DETAIL_OUTPUT_SCHEMA = generate_json_schema(ReservationResponse)
UNIT_DETAIL_OUTPUT_SCHEMA = generate_json_schema(UnitResponse)
FOLIO_DETAIL_OUTPUT_SCHEMA = generate_json_schema(FolioResponse)
WORK_ORDER_DETAIL_OUTPUT_SCHEMA = generate_json_schema(WorkOrderResponse)

# Schemas de colecciones
RESERVATION_SEARCH_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer", "description": "Página actual"},
        "page_count": {"type": "integer", "description": "Total de páginas"},
        "page_size": {"type": "integer", "description": "Tamaño de página"},
        "total_items": {"type": "integer", "description": "Total de elementos"},
        "_embedded": {
            "type": "object",
            "description": "Datos embebidos de la respuesta",
            "properties": {
                "reservations": {
                    "type": "array",
                    "items": generate_json_schema(ReservationResponse),
                    "description": "Lista de reservas",
                }
            },
        },
        "_links": {"type": "object", "description": "Enlaces de navegación HATEOAS"},
    },
    "required": [
        "page",
        "page_count",
        "page_size",
        "total_items",
        "_embedded",
        "_links",
    ],
}

UNIT_SEARCH_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer", "description": "Página actual"},
        "page_count": {"type": "integer", "description": "Total de páginas"},
        "page_size": {"type": "integer", "description": "Tamaño de página"},
        "total_items": {"type": "integer", "description": "Total de elementos"},
        "_embedded": {
            "type": "object",
            "description": "Datos embebidos de la respuesta",
            "properties": {
                "units": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "ID único de la unidad",
                            },
                            "name": {
                                "type": "string",
                                "description": "Nombre de la unidad",
                            },
                            "code": {
                                "type": "string",
                                "description": "Código de la unidad",
                            },
                            "bedrooms": {
                                "type": "integer",
                                "description": "Número de dormitorios",
                            },
                            "bathrooms": {
                                "type": "integer",
                                "description": "Número de baños",
                            },
                            "max_occupancy": {
                                "type": "integer",
                                "description": "Capacidad máxima",
                            },
                            "area": {
                                "type": ["number", "null"],
                                "description": "Área en metros cuadrados",
                            },
                            "address": {
                                "type": "string",
                                "description": "Dirección completa",
                            },
                            "is_active": {
                                "type": ["boolean", "null"],
                                "description": "Si está activa",
                            },
                            "is_bookable": {
                                "type": ["boolean", "null"],
                                "description": "Si está disponible para reservar",
                            },
                            "amenities": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Lista de amenidades",
                            },
                            "_links": {
                                "type": "object",
                                "description": "Enlaces relacionados",
                            },
                        },
                        "required": ["id"],
                        "additionalProperties": True,
                    },
                    "description": "Lista de unidades",
                }
            },
        },
        "_links": {"type": "object", "description": "Enlaces de navegación HATEOAS"},
    },
    "required": [
        "page",
        "page_count",
        "page_size",
        "total_items",
        "_embedded",
        "_links",
    ],
}

# Schema para amenidades (caso especial - mantener estructura específica)
AMENITIES_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer", "description": "Página actual"},
        "page_count": {"type": "integer", "description": "Total de páginas"},
        "page_size": {"type": "integer", "description": "Tamaño de página"},
        "total_items": {
            "type": "integer",
            "description": "Total de amenidades encontradas",
        },
        "_embedded": {
            "type": "object",
            "description": "Datos embebidos de la respuesta",
            "properties": {
                "amenities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "ID único de la amenidad",
                            },
                            "name": {
                                "type": "string",
                                "description": "Nombre de la amenidad",
                            },
                            "group": {
                                "type": "object",
                                "description": "Grupo de la amenidad",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Nombre del grupo",
                                    }
                                },
                            },
                            "is_public": {
                                "type": "boolean",
                                "description": "Si es pública",
                            },
                            "is_filterable": {
                                "type": "boolean",
                                "description": "Si es filtrable",
                            },
                            "description": {
                                "type": "string",
                                "description": "Descripción de la amenidad",
                            },
                        },
                    },
                }
            },
        },
        "_links": {"type": "object", "description": "Enlaces de navegación HATEOAS"},
    },
}

# =============================================================================
# ALIASES PARA COMPATIBILIDAD - MANTENER EXISTING CODE
# =============================================================================

# Alias para mantener compatibilidad con código existente
WORK_ORDER_OUTPUT_SCHEMA = WORK_ORDER_DETAIL_OUTPUT_SCHEMA


class CollectionResponse(BaseModel):
    """Respuesta de colección paginada genérica."""

    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    embedded: Dict[str, Any] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    links: Dict[str, Any] = Field(
        ..., alias="_links", description="Enlaces de navegación"
    )
