"""
Esquemas Pydantic para TrackHS MCP Server
Define enums, modelos y esquemas de salida para validación robusta
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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


class CollectionMetadata(BaseModel):
    """Metadatos de paginación para colecciones"""

    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")


class CollectionLinks(BaseModel):
    """Enlaces HATEOAS para navegación"""

    self: Optional[str] = Field(None, description="Enlace a la página actual")
    first: Optional[str] = Field(None, description="Enlace a la primera página")
    last: Optional[str] = Field(None, description="Enlace a la última página")
    next: Optional[str] = Field(None, description="Enlace a la siguiente página")
    prev: Optional[str] = Field(None, description="Enlace a la página anterior")


class CollectionResponse(BaseModel):
    """Respuesta estándar para colecciones con metadatos"""

    page: int = Field(description="Página actual")
    page_count: int = Field(description="Total de páginas")
    page_size: int = Field(description="Tamaño de página")
    total_items: int = Field(description="Total de elementos")
    embedded: Dict[str, Any] = Field(alias="_embedded", description="Datos embebidos")
    links: Dict[str, Any] = Field(alias="_links", description="Enlaces de navegación")

    model_config = {"populate_by_name": True}


class ReservationResponse(BaseModel):
    """Modelo para validar respuesta de reserva individual"""

    id: int = Field(description="ID de la reserva")
    confirmation_number: Optional[str] = Field(
        None, description="Número de confirmación"
    )
    status: Optional[str] = Field(None, description="Estado de la reserva")
    arrival: Optional[str] = Field(None, description="Fecha de llegada (YYYY-MM-DD)")
    departure: Optional[str] = Field(None, description="Fecha de salida (YYYY-MM-DD)")

    model_config = {"extra": "allow"}  # Permitir campos adicionales


class UnitResponse(BaseModel):
    """Modelo para validar respuesta de unidad"""

    id: int = Field(description="ID de la unidad")
    name: Optional[str] = Field(None, description="Nombre de la unidad")
    code: Optional[str] = Field(None, description="Código de la unidad")
    bedrooms: Optional[int] = Field(None, description="Número de dormitorios")
    bathrooms: Optional[int] = Field(None, description="Número de baños")

    model_config = {"extra": "allow"}


class FolioResponse(BaseModel):
    """Modelo para validar respuesta de folio"""

    id: int = Field(description="ID del folio")
    reservation_id: Optional[int] = Field(None, description="ID de la reserva")
    balance: Optional[float] = Field(None, description="Balance pendiente")
    total: Optional[float] = Field(None, description="Total")

    model_config = {"extra": "allow"}


class WorkOrderResponse(BaseModel):
    """Modelo para validar respuesta de work order"""

    id: int = Field(description="ID de la orden de trabajo")
    status: Optional[str] = Field(None, description="Estado de la orden")
    unit_id: Optional[int] = Field(None, description="ID de la unidad")
    priority: Optional[int] = Field(None, description="Prioridad")

    model_config = {"extra": "allow"}


# Esquemas de salida para tools
RESERVATION_SEARCH_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer", "description": "Página actual"},
        "page_count": {"type": "integer", "description": "Total de páginas"},
        "page_size": {"type": "integer", "description": "Tamaño de página"},
        "total_items": {
            "type": "integer",
            "description": "Total de reservas encontradas",
        },
        "_embedded": {
            "type": "object",
            "properties": {
                "reservations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "ID único de la reserva",
                            },
                            "confirmationNumber": {
                                "type": "string",
                                "description": "Número de confirmación",
                            },
                            "guest": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Nombre del huésped",
                                    },
                                    "email": {
                                        "type": "string",
                                        "description": "Email del huésped",
                                    },
                                    "phone": {
                                        "type": "string",
                                        "description": "Teléfono del huésped",
                                    },
                                },
                            },
                            "arrivalDate": {
                                "type": "string",
                                "description": "Fecha de llegada (ISO 8601)",
                            },
                            "departureDate": {
                                "type": "string",
                                "description": "Fecha de salida (ISO 8601)",
                            },
                            "status": {
                                "type": "string",
                                "description": "Estado de la reserva",
                            },
                            "unit": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "integer",
                                        "description": "ID de la unidad",
                                    },
                                    "name": {
                                        "type": "string",
                                        "description": "Nombre de la unidad",
                                    },
                                    "code": {
                                        "type": "string",
                                        "description": "Código de la unidad",
                                    },
                                },
                            },
                            "financial": {
                                "type": "object",
                                "properties": {
                                    "totalAmount": {
                                        "type": "number",
                                        "description": "Monto total",
                                    },
                                    "balance": {
                                        "type": "number",
                                        "description": "Balance pendiente",
                                    },
                                    "deposit": {
                                        "type": "number",
                                        "description": "Depósito requerido",
                                    },
                                },
                            },
                            "_links": {
                                "type": "object",
                                "description": "Enlaces a recursos relacionados",
                            },
                        },
                    },
                }
            },
        },
        "_links": {"type": "object", "description": "Enlaces de navegación HATEOAS"},
    },
}

UNIT_SEARCH_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer", "description": "Página actual"},
        "page_count": {"type": "integer", "description": "Total de páginas"},
        "page_size": {"type": "integer", "description": "Tamaño de página"},
        "total_items": {
            "type": "integer",
            "description": "Total de unidades encontradas",
        },
        "_embedded": {
            "type": "object",
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
                                "type": "number",
                                "description": "Área en metros cuadrados",
                            },
                            "address": {
                                "type": "string",
                                "description": "Dirección de la unidad",
                            },
                            "amenities": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Amenidades disponibles",
                            },
                            "is_active": {
                                "type": "boolean",
                                "description": "Si la unidad está activa",
                            },
                            "is_bookable": {
                                "type": "boolean",
                                "description": "Si la unidad está disponible para reservar",
                            },
                        },
                    },
                }
            },
        },
        "_links": {"type": "object", "description": "Enlaces de navegación HATEOAS"},
    },
}

WORK_ORDER_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "description": "ID único de la orden de trabajo"},
        "status": {"type": "string", "description": "Estado actual de la orden"},
        "priority": {
            "type": "integer",
            "description": "Prioridad (1=Baja, 3=Media, 5=Alta)",
        },
        "summary": {"type": "string", "description": "Resumen del trabajo"},
        "description": {"type": "string", "description": "Descripción detallada"},
        "unit_id": {"type": "integer", "description": "ID de la unidad"},
        "estimated_cost": {"type": "number", "description": "Costo estimado"},
        "estimated_time": {
            "type": "integer",
            "description": "Tiempo estimado en minutos",
        },
        "date_received": {"type": "string", "description": "Fecha de recepción"},
        "date_completed": {"type": "string", "description": "Fecha de finalización"},
        "assigned_to": {"type": "string", "description": "Usuario asignado"},
        "vendor": {"type": "string", "description": "Proveedor asignado"},
        "_links": {"type": "object", "description": "Enlaces a recursos relacionados"},
    },
}

# Esquemas adicionales para herramientas sin output schema
RESERVATION_DETAIL_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "description": "ID único de la reserva"},
        "confirmation_number": {
            "type": "string",
            "description": "Número de confirmación",
        },
        "guest": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nombre del huésped"},
                "email": {"type": "string", "description": "Email del huésped"},
                "phone": {"type": "string", "description": "Teléfono del huésped"},
                "address": {"type": "string", "description": "Dirección del huésped"},
            },
        },
        "dates": {
            "type": "object",
            "properties": {
                "arrival": {"type": "string", "description": "Fecha de llegada"},
                "departure": {"type": "string", "description": "Fecha de salida"},
                "nights": {"type": "integer", "description": "Número de noches"},
            },
        },
        "unit": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID de la unidad"},
                "name": {"type": "string", "description": "Nombre de la unidad"},
                "code": {"type": "string", "description": "Código de la unidad"},
                "bedrooms": {"type": "integer", "description": "Número de dormitorios"},
                "bathrooms": {"type": "integer", "description": "Número de baños"},
            },
        },
        "status": {"type": "string", "description": "Estado de la reserva"},
        "financial": {
            "type": "object",
            "properties": {
                "total_amount": {"type": "number", "description": "Monto total"},
                "balance": {"type": "number", "description": "Balance pendiente"},
                "deposit": {"type": "number", "description": "Depósito requerido"},
            },
        },
        "_links": {"type": "object", "description": "Enlaces a recursos relacionados"},
    },
}

FOLIO_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "reservation_id": {"type": "integer", "description": "ID de la reserva"},
        "balance": {"type": "number", "description": "Balance total"},
        "charges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "ID del cargo"},
                    "description": {
                        "type": "string",
                        "description": "Descripción del cargo",
                    },
                    "amount": {"type": "number", "description": "Monto del cargo"},
                    "date": {"type": "string", "description": "Fecha del cargo"},
                    "type": {"type": "string", "description": "Tipo de cargo"},
                },
            },
        },
        "payments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "ID del pago"},
                    "amount": {"type": "number", "description": "Monto del pago"},
                    "date": {"type": "string", "description": "Fecha del pago"},
                    "method": {"type": "string", "description": "Método de pago"},
                    "status": {"type": "string", "description": "Estado del pago"},
                },
            },
        },
        "summary": {
            "type": "object",
            "properties": {
                "total_charges": {"type": "number", "description": "Total de cargos"},
                "total_payments": {"type": "number", "description": "Total de pagos"},
                "balance_due": {"type": "number", "description": "Balance pendiente"},
            },
        },
    },
}

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
                                "type": "string",
                                "description": "Grupo de la amenidad",
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
