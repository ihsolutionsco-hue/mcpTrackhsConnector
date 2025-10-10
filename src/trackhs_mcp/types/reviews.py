"""
Modelos Pydantic para Reviews de Track HS API
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from .base import PaginationParams, SearchParams

class Review(BaseModel):
    """Modelo de Review de Track HS"""
    id: int = Field(..., description="ID único de la reseña")
    review_id: str = Field(..., description="ID público de la reseña")
    public_review: str = Field(..., description="Contenido público de la reseña")
    private_review: Optional[str] = Field(default=None, description="Contenido privado de la reseña")
    rating: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    guest_name: str = Field(..., description="Nombre del huésped")
    guest_email: str = Field(..., description="Email del huésped")
    property_id: str = Field(..., description="ID de la propiedad")
    property_name: str = Field(..., description="Nombre de la propiedad")
    channel: str = Field(..., description="Canal de origen de la reseña")
    created_at: str = Field(..., description="Fecha de creación (ISO 8601)")
    updated_at: str = Field(..., description="Fecha de última actualización (ISO 8601)")
    status: Literal["published", "pending", "rejected"] = Field(..., description="Estado de la reseña")
    response: Optional[str] = Field(default=None, description="Respuesta del host")
    response_date: Optional[str] = Field(default=None, description="Fecha de respuesta (ISO 8601)")

class GetReviewsParams(PaginationParams, SearchParams):
    """Parámetros para obtener reseñas"""
    sort_column: Literal["id"] = Field(default="id", description="Columna para ordenar")
    sort_direction: Literal["asc", "desc"] = Field(default="asc", description="Dirección de ordenamiento")

class ReviewsResponse(BaseModel):
    """Respuesta de la API de reseñas"""
    data: list[Review] = Field(..., description="Lista de reseñas")
    pagination: dict[str, int | bool] = Field(..., description="Información de paginación")
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")

class ReviewFilters(BaseModel):
    """Filtros para reseñas"""
    status: Optional[Literal["published", "pending", "rejected"]] = Field(default=None, description="Estado de la reseña")
    channel: Optional[str] = Field(default=None, description="Canal de origen")
    property_id: Optional[str] = Field(default=None, description="ID de la propiedad")
    rating: Optional[int] = Field(default=None, ge=1, le=5, description="Calificación mínima")
    date_from: Optional[str] = Field(default=None, description="Fecha desde (ISO 8601)")
    date_to: Optional[str] = Field(default=None, description="Fecha hasta (ISO 8601)")
