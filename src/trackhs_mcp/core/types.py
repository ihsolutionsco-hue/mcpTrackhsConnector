"""
Tipos compartidos para el servidor MCP de Track HS
"""

from typing import Dict, Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class TrackHSConfig(BaseModel):
    """Configuración para el cliente de Track HS API"""
    base_url: str = Field(..., description="URL base de la API de Track HS")
    username: str = Field(..., description="Nombre de usuario para autenticación")
    password: str = Field(..., description="Contraseña para autenticación")
    timeout: Optional[int] = Field(default=30, description="Timeout en segundos para las peticiones")

class RequestOptions(BaseModel):
    """Opciones para peticiones HTTP"""
    method: str = Field(default="GET", description="Método HTTP")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Headers adicionales")
    body: Optional[str] = Field(default=None, description="Cuerpo de la petición")

class ApiError(Exception):
    """Excepción personalizada para errores de la API"""
    def __init__(self, message: str, status: Optional[int] = None, status_text: Optional[str] = None):
        self.message = message
        self.status = status
        self.status_text = status_text
        super().__init__(self.message)

class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    page: Optional[int] = Field(default=1, ge=1, description="Número de página")
    size: Optional[int] = Field(default=10, ge=1, le=100, description="Tamaño de página")
    sort_column: Optional[str] = Field(default="id", description="Columna para ordenar")
    sort_direction: Optional[str] = Field(default="asc", pattern="^(asc|desc)$", description="Dirección de ordenamiento")

class SearchParams(BaseModel):
    """Parámetros de búsqueda"""
    search: Optional[str] = Field(default=None, description="Término de búsqueda")
    updated_since: Optional[str] = Field(default=None, description="Filtro por fecha de actualización (ISO 8601)")

class TrackHSResponse(BaseModel, Generic[T]):
    """Respuesta genérica de Track HS API"""
    data: T = Field(..., description="Datos de la respuesta")
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: Optional[str] = Field(default=None, description="Mensaje adicional")
