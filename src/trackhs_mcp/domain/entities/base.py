"""
Modelos base para TrackHS MCP Connector
"""

from typing import Optional

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Parámetros de paginación"""

    page: Optional[int] = Field(default=1, ge=0, description="Número de página")
    size: Optional[int] = Field(
        default=10, ge=1, le=1000, description="Tamaño de página"
    )
    sort_column: Optional[str] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[str] = Field(
        default="asc", pattern="^(asc|desc)$", description="Dirección de ordenamiento"
    )


class SearchParams(BaseModel):
    """Parámetros de búsqueda"""

    search: Optional[str] = Field(default=None, description="Término de búsqueda")
    updated_since: Optional[str] = Field(
        default=None, description="Filtro por fecha de actualización (ISO 8601)"
    )


class TrackHSResponse(BaseModel):
    """Respuesta base de Track HS API"""

    success: bool = Field(..., description="Indica si la operación fue exitosa")
    data: Optional[dict] = Field(default=None, description="Datos de la respuesta")
    message: Optional[str] = Field(default=None, description="Mensaje de la respuesta")
    error: Optional[str] = Field(default=None, description="Mensaje de error si aplica")
