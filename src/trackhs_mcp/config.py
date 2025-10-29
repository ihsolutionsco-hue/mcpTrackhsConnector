"""
Configuración centralizada para TrackHS MCP Server
Usando Pydantic Settings para validación y type safety
"""

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings

# Cargar variables de entorno del archivo .env
load_dotenv()


class TrackHSSettings(BaseSettings):
    """Configuración centralizada del servidor TrackHS MCP"""

    # Credenciales TrackHS (requeridas)
    trackhs_username: str = Field(
        ..., description="Usuario de TrackHS API", alias="TRACKHS_USERNAME"
    )
    trackhs_password: str = Field(
        ..., description="Contraseña de TrackHS API", alias="TRACKHS_PASSWORD"
    )

    # URL de API (opcional, con default)
    trackhs_api_url: str = Field(
        default="https://ihmvacations.trackhs.com",
        description="URL base de la API TrackHS",
        alias="TRACKHS_API_URL",
    )

    # Configuración de logging
    log_level: str = Field(
        default="INFO", description="Nivel de logging", alias="LOG_LEVEL"
    )
    log_format: str = Field(default="json", description="Formato de logs")

    # Configuración de autenticación
    auth_cache_ttl: int = Field(
        default=300, description="TTL del cache de autenticación en segundos"
    )

    # Configuración de validación
    strict_validation: bool = Field(
        default=False,
        description="Habilitar validación estricta de respuestas",
        alias="STRICT_VALIDATION",
    )

    # Configuración crítica para FastMCP
    force_input_coercion: bool = Field(
        default=True,
        description="Forzar coerción de tipos de entrada (CRÍTICO para parámetros numéricos)",
        alias="FORCE_INPUT_COERCION",
    )

    # Configuración de reintentos
    max_retries: int = Field(default=3, description="Máximo número de reintentos")
    retry_delay: float = Field(
        default=1.0, description="Delay inicial entre reintentos"
    )

    # Configuración de timeouts
    request_timeout: float = Field(
        default=30.0, description="Timeout de requests en segundos"
    )
    trackhs_timeout: int = Field(
        default=30,
        description="Timeout específico de TrackHS en segundos",
        alias="TRACKHS_TIMEOUT",
    )

    # Configuración de respuestas
    trackhs_compact_responses: bool = Field(
        default=True,
        description="Usar respuestas compactas de TrackHS",
        alias="TRACKHS_COMPACT_RESPONSES",
    )
    trackhs_max_response_items: int = Field(
        default=100,
        description="Máximo número de elementos en respuestas",
        alias="TRACKHS_MAX_RESPONSE_ITEMS",
    )

    # Configuración de CORS
    cors_origins: List[str] = Field(
        default=[
            "https://elevenlabs.io",
            "https://api.elevenlabs.io",
            "https://app.elevenlabs.io",
            "https://claude.ai",
            "https://app.claude.ai",
        ],
        description="Orígenes permitidos para CORS",
    )
    cors_credentials: bool = Field(
        default=True, description="Permitir credenciales en CORS"
    )

    # Configuración de health check
    health_check_enabled: bool = Field(
        default=True, description="Habilitar health check"
    )
    health_check_timeout: int = Field(
        default=30, description="Timeout del health check"
    )

    # Configuración de métricas
    metrics_enabled: bool = Field(default=True, description="Habilitar métricas")
    metrics_port: int = Field(
        default=9090, description="Puerto para métricas Prometheus"
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Permitir campos extra para variables de entorno
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validar nivel de logging"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level debe ser uno de: {valid_levels}")
        return v.upper()

    @field_validator("auth_cache_ttl")
    @classmethod
    def validate_auth_cache_ttl(cls, v):
        """Validar TTL del cache de autenticación"""
        if v < 60:  # Mínimo 1 minuto
            raise ValueError("auth_cache_ttl debe ser al menos 60 segundos")
        if v > 3600:  # Máximo 1 hora
            raise ValueError("auth_cache_ttl no debe exceder 3600 segundos")
        return v

    @field_validator("max_retries")
    @classmethod
    def validate_max_retries(cls, v):
        """Validar número máximo de reintentos"""
        if v < 0 or v > 10:
            raise ValueError("max_retries debe estar entre 0 y 10")
        return v

    @field_validator("request_timeout")
    @classmethod
    def validate_request_timeout(cls, v):
        """Validar timeout de requests"""
        if v < 5.0 or v > 300.0:
            raise ValueError("request_timeout debe estar entre 5 y 300 segundos")
        return v

    @field_validator("trackhs_timeout")
    @classmethod
    def validate_trackhs_timeout(cls, v):
        """Validar timeout específico de TrackHS"""
        if v < 5 or v > 300:
            raise ValueError("trackhs_timeout debe estar entre 5 y 300 segundos")
        return v

    @field_validator("trackhs_max_response_items")
    @classmethod
    def validate_trackhs_max_response_items(cls, v):
        """Validar máximo número de elementos en respuestas"""
        if v < 1 or v > 1000:
            raise ValueError("trackhs_max_response_items debe estar entre 1 y 1000")
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
