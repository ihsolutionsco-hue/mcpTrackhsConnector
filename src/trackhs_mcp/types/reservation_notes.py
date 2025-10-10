"""
Modelos Pydantic para Reservation Notes de Track HS API
"""

from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field
from .base import PaginationParams, SearchParams

class ReservationNote(BaseModel):
    """Modelo de ReservationNote"""
    id: int = Field(..., description="ID único de la nota")
    reservation_id: int = Field(..., description="ID de la reserva")
    content: str = Field(..., description="Contenido de la nota")
    author: str = Field(..., description="Autor de la nota")
    created_at: str = Field(..., description="Fecha de creación")
    updated_at: str = Field(..., description="Fecha de actualización")
    is_internal: bool = Field(..., description="Si es interna")
    note_type: Optional[str] = Field(default=None, description="Tipo de nota")
    priority: Optional[Literal["low", "medium", "high"]] = Field(default=None, description="Prioridad")
    tags: Optional[List[str]] = Field(default=None, description="Tags")

class ReservationNotesResponse(BaseModel):
    """Respuesta de notas de reserva"""
    _embedded: Dict[str, List[ReservationNote]] = Field(..., description="Datos embebidos")
    page: Optional[int] = Field(default=None, description="Página actual")
    page_count: Optional[int] = Field(default=None, description="Total de páginas")
    page_size: Optional[int] = Field(default=None, description="Tamaño de página")
    total_items: Optional[int] = Field(default=None, description="Total de elementos")
    _links: Dict[str, Union[str, Dict[str, str]]] = Field(..., description="Enlaces")

class GetReservationNotesParams(PaginationParams, SearchParams):
    """Parámetros para obtener notas de reserva"""
    is_internal: Optional[bool] = Field(default=None, description="Si es interna")
    note_type: Optional[str] = Field(default=None, description="Tipo de nota")
    priority: Optional[Literal["low", "medium", "high"]] = Field(default=None, description="Prioridad")
    author: Optional[str] = Field(default=None, description="Autor")
    sort_by: Optional[Literal["createdAt", "updatedAt", "author", "priority"]] = Field(default="createdAt", description="Campo para ordenar")
    sort_direction: Optional[Literal["asc", "desc"]] = Field(default="desc", description="Dirección de ordenamiento")
    date_from: Optional[str] = Field(default=None, description="Fecha desde")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta")

class CreateReservationNoteRequest(BaseModel):
    """Solicitud para crear nota de reserva"""
    content: str = Field(..., description="Contenido de la nota")
    is_internal: Optional[bool] = Field(default=False, description="Si es interna")
    note_type: Optional[str] = Field(default=None, description="Tipo de nota")
    priority: Optional[Literal["low", "medium", "high"]] = Field(default="medium", description="Prioridad")
    tags: Optional[List[str]] = Field(default=None, description="Tags")

class UpdateReservationNoteRequest(BaseModel):
    """Solicitud para actualizar nota de reserva"""
    content: Optional[str] = Field(default=None, description="Contenido de la nota")
    is_internal: Optional[bool] = Field(default=None, description="Si es interna")
    note_type: Optional[str] = Field(default=None, description="Tipo de nota")
    priority: Optional[Literal["low", "medium", "high"]] = Field(default=None, description="Prioridad")
    tags: Optional[List[str]] = Field(default=None, description="Tags")

class ReservationNoteResponse(BaseModel):
    """Respuesta de nota de reserva"""
    data: ReservationNote = Field(..., description="Datos de la nota")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")
