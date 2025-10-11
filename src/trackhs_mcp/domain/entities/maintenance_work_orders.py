"""
Modelos Pydantic para Maintenance Work Orders de Track HS API
"""

from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .base import PaginationParams, SearchParams


class Problem(BaseModel):
    """Modelo de Problem"""

    id: int = Field(..., description="ID del problema")
    name: str = Field(..., description="Nombre del problema")


class Assignee(BaseModel):
    """Modelo de Assignee"""

    id: int = Field(..., description="ID del asignado")
    name: str = Field(..., description="Nombre del asignado")
    email: Optional[str] = Field(default=None, description="Email del asignado")


class WorkOrderEmbedded(BaseModel):
    """Modelo de WorkOrderEmbedded"""

    unit: Optional[Dict[str, Union[int, str]]] = Field(
        default=None, description="Unidad"
    )
    vendor: Optional[Dict[str, Union[int, str]]] = Field(
        default=None, description="Vendor"
    )
    owner: Optional[Dict[str, Union[int, str]]] = Field(
        default=None, description="Propietario"
    )


class WorkOrderLinks(BaseModel):
    """Modelo de WorkOrderLinks"""

    self: Dict[str, str] = Field(..., description="Enlace propio")
    contacts: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace de contactos"
    )
    licences: Optional[Dict[str, str]] = Field(
        default=None, description="Enlace de licencias"
    )


class MaintenanceWorkOrder(BaseModel):
    """Modelo de MaintenanceWorkOrder"""

    id: int = Field(..., description="ID de la orden de trabajo")
    date_received: str = Field(..., description="Fecha de recepción")
    priority: Literal[5, 3, 1] = Field(
        ..., description="Prioridad (High=5, Medium=3, Low=1)"
    )
    status: Literal[
        "open",
        "not-started",
        "in-progress",
        "completed",
        "processed",
        "vendor-not-start",
        "vendor-assigned",
        "vendor-declined",
        "vendor-completed",
        "user-completed",
        "cancelled",
    ] = Field(..., description="Estado")
    assignees: Optional[List[Assignee]] = Field(default=None, description="Asignados")
    summary: str = Field(..., description="Resumen")
    problems: Optional[List[Problem]] = Field(default=None, description="Problemas")
    estimated_cost: Optional[int] = Field(default=None, description="Costo estimado")
    estimated_time: Optional[int] = Field(default=None, description="Tiempo estimado")
    actual_time: Optional[int] = Field(default=None, description="Tiempo actual")
    date_completed: Optional[str] = Field(
        default=None, description="Fecha de completado"
    )
    completed_by_id: Optional[int] = Field(
        default=None, description="ID de quien completó"
    )
    date_processed: Optional[str] = Field(
        default=None, description="Fecha de procesado"
    )
    processed_by_id: Optional[int] = Field(
        default=None, description="ID de quien procesó"
    )
    user_id: Optional[int] = Field(default=None, description="ID del usuario")
    vendor_id: Optional[int] = Field(default=None, description="ID del vendor")
    unit_id: Optional[int] = Field(default=None, description="ID de la unidad")
    owner_id: Optional[int] = Field(default=None, description="ID del propietario")
    reservation_id: Optional[int] = Field(default=None, description="ID de la reserva")
    reference_number: Optional[str] = Field(
        default=None, description="Número de referencia"
    )
    description: Optional[str] = Field(default=None, description="Descripción")
    work_performed: Optional[str] = Field(default=None, description="Trabajo realizado")
    source: Optional[str] = Field(default=None, description="Fuente")
    source_name: Optional[str] = Field(default=None, description="Nombre de la fuente")
    source_phone: Optional[str] = Field(
        default=None, description="Teléfono de la fuente"
    )
    block_checkin: Optional[bool] = Field(
        default=None, description="Si bloquea check-in"
    )
    created_at: str = Field(..., description="Fecha de creación")
    created_by: str = Field(..., description="Creado por")
    updated_at: str = Field(..., description="Fecha de actualización")
    updated_by: str = Field(..., description="Actualizado por")
    embedded: Optional[WorkOrderEmbedded] = Field(
        default=None, alias="_embedded", description="Datos embebidos"
    )
    links: Optional[WorkOrderLinks] = Field(
        default=None, alias="_links", description="Enlaces"
    )


class GetMaintenanceWorkOrdersParams(PaginationParams, SearchParams):
    """Parámetros para obtener órdenes de trabajo de mantenimiento"""

    sort_column: Optional[
        Literal[
            "id",
            "scheduledAt",
            "status",
            "priority",
            "dateReceived",
            "unitId",
            "vendorId",
            "userId",
            "summary",
        ]
    ] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="Dirección de ordenamiento"
    )
    is_scheduled: Optional[Literal[0, 1]] = Field(
        default=None, description="Si está programado"
    )
    unit_id: Optional[str] = Field(default=None, description="ID de la unidad")
    user_id: Optional[List[int]] = Field(default=None, description="IDs de usuarios")
    node_id: Optional[int] = Field(default=None, description="ID del nodo")
    role_id: Optional[int] = Field(default=None, description="ID del rol")
    owner_id: Optional[int] = Field(default=None, description="ID del propietario")
    priority: Optional[List[int]] = Field(default=None, description="Prioridades")
    reservation_id: Optional[int] = Field(default=None, description="ID de la reserva")
    vendor_id: Optional[int] = Field(default=None, description="ID del vendor")
    status: Optional[
        List[
            Literal[
                "open",
                "not-started",
                "in-progress",
                "completed",
                "processed",
                "vendor-not-start",
                "vendor-assigned",
                "vendor-declined",
                "vendor-completed",
                "user-completed",
                "cancelled",
            ]
        ]
    ] = Field(default=None, description="Estados")
    date_scheduled: Optional[str] = Field(default=None, description="Fecha programada")
    start_date: Optional[str] = Field(default=None, description="Fecha de inicio")
    end_date: Optional[str] = Field(default=None, description="Fecha de fin")
    problems: Optional[List[int]] = Field(default=None, description="IDs de problemas")


class MaintenanceWorkOrdersResponse(BaseModel):
    """Respuesta de órdenes de trabajo de mantenimiento"""

    model_config = {"populate_by_name": True}

    embedded: Dict[str, List[MaintenanceWorkOrder]] = Field(
        ..., alias="_embedded", description="Datos embebidos"
    )
    page: int = Field(..., description="Página actual")
    page_count: int = Field(..., description="Total de páginas")
    page_size: int = Field(..., description="Tamaño de página")
    total_items: int = Field(..., description="Total de elementos")
    links: Dict[str, Union[str, Dict[str, str]]] = Field(
        ..., alias="_links", description="Enlaces"
    )
