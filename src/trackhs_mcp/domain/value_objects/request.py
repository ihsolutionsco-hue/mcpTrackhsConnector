"""
Value Objects para peticiones HTTP
"""

from typing import Dict, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field

T = TypeVar("T")


class RequestOptions(BaseModel):
    """Opciones para peticiones HTTP"""

    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"] = Field(
        default="GET", description="Método HTTP"
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Headers adicionales"
    )
    body: Optional[str] = Field(default=None, description="Cuerpo de la petición")


class PaginationParams(BaseModel):
    """Parámetros de paginación"""

    page: Optional[int] = Field(default=1, ge=1, description="Número de página")
    size: Optional[int] = Field(
        default=10, ge=1, le=100, description="Tamaño de página"
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
    node_id: Optional[Union[int, List[int]]] = Field(
        default=None, description="ID del nodo"
    )
    tags: Optional[str] = Field(default=None, description="Tags para filtrar")


class TrackHSResponse(BaseModel, Generic[T]):
    """Respuesta genérica de Track HS API"""

    data: T = Field(..., description="Datos de la respuesta")
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")
