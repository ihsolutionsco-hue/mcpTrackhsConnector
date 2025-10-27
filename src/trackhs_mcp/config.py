"""
Configuración centralizada para TrackHS MCP Server
Usando Pydantic Settings para validación y type safety
"""

import os
from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class TrackHSSettings(BaseSettings):
    """Configuración centralizada del servidor TrackHS MCP"""

    # Credenciales TrackHS (requeridas)
    trackhs_username: str = Field(..., description="Usuario de TrackHS API")
    trackhs_password: str = Field(..., description="Contraseña de TrackHS API")

    # URL de API (opcional, con default)
    trackhs_api_url: str = Field(
        default="https://ihmvacations.trackhs.com/api",
        description="URL base de la API TrackHS"
    )

    # Configuración de logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_format: str = Field(default="json", description="Formato de logs")

    # Configuración de autenticación
    auth_cache_ttl: int = Field(
        default=300,
        description="TTL del cache de autenticación en segundos"
    )

    # Configuración de validación
    strict_validation: bool = Field(
        default=True,
        description="Habilitar validación estricta de respuestas"
    )

    # Configuración de reintentos
    max_retries: int = Field(default=3, description="Máximo número de reintentos")
    retry_delay: float = Field(default=1.0, description="Delay inicial entre reintentos")

    # Configuración de timeouts
    request_timeout: float = Field(default=30.0, description="Timeout de requests en segundos")

    # Configuración de CORS
    cors_origins: List[str] = Field(
        default=[
            "https://elevenlabs.io",
            "https://api.elevenlabs.io",
            "https://app.elevenlabs.io",
            "https://claude.ai",
            "https://app.claude.ai"
        ],
        description="Orígenes permitidos para CORS"
    )
    cors_credentials: bool = Field(default=True, description="Permitir credenciales en CORS")

    # Configuración de health check
    health_check_enabled: bool = Field(default=True, description="Habilitar health check")
    health_check_timeout: int = Field(default=30, description="Timeout del health check")

    # Configuración de métricas
    metrics_enabled: bool = Field(default=True, description="Habilitar métricas")
    metrics_port: int = Field(default=9090, description="Puerto para métricas Prometheus")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Mapear variables de entorno
        fields = {
            "trackhs_username": {"env": "TRACKHS_USERNAME"},
            "trackhs_password": {"env": "TRACKHS_PASSWORD"},
            "trackhs_api_url": {"env": "TRACKHS_API_URL"},
            "log_level": {"env": "LOG_LEVEL"},
            "strict_validation": {"env": "STRICT_VALIDATION"},
        }

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validar nivel de logging"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level debe ser uno de: {valid_levels}")
        return v.upper()

    @validator("auth_cache_ttl")
    def validate_auth_cache_ttl(cls, v):
        """Validar TTL del cache de autenticación"""
        if v < 60:  # Mínimo 1 minuto
            raise ValueError("auth_cache_ttl debe ser al menos 60 segundos")
        if v > 3600:  # Máximo 1 hora
            raise ValueError("auth_cache_ttl no debe exceder 3600 segundos")
        return v

    @validator("max_retries")
    def validate_max_retries(cls, v):
        """Validar número máximo de reintentos"""
        if v < 0 or v > 10:
            raise ValueError("max_retries debe estar entre 0 y 10")
        return v

    @validator("request_timeout")
    def validate_request_timeout(cls, v):
        """Validar timeout de requests"""
        if v < 5.0 or v > 300.0:
            raise ValueError("request_timeout debe estar entre 5 y 300 segundos")
        return v


# Instancia global de configuración
settings = TrackHSSettings()

# Función helper para obtener configuración
def get_settings() -> TrackHSSettings:
    """Obtener instancia de configuración"""
    return settings


# Función para validar configuración al inicio
def validate_configuration() -> bool:
    """Validar que la configuración sea correcta"""
    try:
        # Verificar credenciales requeridas
        if not settings.trackhs_username or not settings.trackhs_password:
            raise ValueError("TRACKHS_USERNAME y TRACKHS_PASSWORD son requeridos")

        # Verificar URL de API
        if not settings.trackhs_api_url.startswith(("http://", "https://")):
            raise ValueError("TRACKHS_API_URL debe ser una URL válida")

        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False
