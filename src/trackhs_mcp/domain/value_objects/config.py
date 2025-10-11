"""
Value Objects para configuración
"""

from typing import Optional

from pydantic import BaseModel, Field


class TrackHSConfig(BaseModel):
    """Configuración para el cliente de Track HS API"""

    base_url: str = Field(..., description="URL base de la API de Track HS")
    username: str = Field(..., description="Nombre de usuario para autenticación")
    password: str = Field(..., description="Contraseña para autenticación")
    timeout: Optional[int] = Field(
        default=30, description="Timeout en segundos para las peticiones"
    )
