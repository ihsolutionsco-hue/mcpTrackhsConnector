"""
Configuración para TrackHS MCP Server
"""

import os
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Credenciales de TrackHS
    trackhs_username: Optional[str] = Field(default=None, env="TRACKHS_USERNAME")
    trackhs_password: Optional[str] = Field(default=None, env="TRACKHS_PASSWORD")
    trackhs_api_url: str = Field(
        default="https://ihmvacations.trackhs.com", env="TRACKHS_API_URL"
    )

    # Configuración del servidor
    server_host: str = Field(default="0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(default=8000, env="SERVER_PORT")

    # Configuración de logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Configuración de API
    api_timeout: int = Field(default=30, env="API_TIMEOUT")

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación"""
    return Settings()
