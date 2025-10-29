"""
Schemas base para TrackHS MCP Server
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Schema base con configuración común"""

    model_config = {
        "extra": "allow",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""

    error: str = Field(description="Mensaje de error")
    error_code: Optional[str] = Field(default=None, description="Código de error")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Detalles adicionales del error"
    )


class SuccessResponse(BaseModel):
    """Respuesta de éxito estándar"""

    success: bool = Field(
        default=True, description="Indica si la operación fue exitosa"
    )
    message: Optional[str] = Field(default=None, description="Mensaje de éxito")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Datos de respuesta"
    )


class PaginationParams(BaseModel):
    """Parámetros de paginación comunes"""

    page: int = Field(default=1, ge=1, description="Número de página (1-based)")
    size: int = Field(default=10, ge=1, le=100, description="Tamaño de página (1-100)")


class PaginationResponse(BaseModel):
    """Respuesta con paginación"""

    total_items: int = Field(description="Total de elementos")
    total_pages: int = Field(description="Total de páginas")
    current_page: int = Field(description="Página actual")
    page_size: int = Field(description="Tamaño de página")
    has_next: bool = Field(description="Indica si hay página siguiente")
    has_prev: bool = Field(description="Indica si hay página anterior")
