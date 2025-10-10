"""
Modelos base para TrackHS MCP Connector
"""

from typing import Optional
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    page: Optional[int] = Field(default=1, ge=1, description="Número de página")
    size: Optional[int] = Field(default=10, ge=1, le=100, description="Tamaño de página")
    sort_column: Optional[str] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[str] = Field(default="asc", regex="^(asc|desc)$", description="Dirección de ordenamiento")

class SearchParams(BaseModel):
    """Parámetros de búsqueda"""
    search: Optional[str] = Field(default=None, description="Término de búsqueda")
    updated_since: Optional[str] = Field(default=None, description="Filtro por fecha de actualización (ISO 8601)")
