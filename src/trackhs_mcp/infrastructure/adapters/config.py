"""
Configuración centralizada para TrackHS MCP Connector
"""

import os
from typing import ClassVar

from ...domain.value_objects.config import TrackHSConfig as BaseTrackHSConfig


class TrackHSConfig(BaseTrackHSConfig):
    """Configuración centralizada para TrackHS API"""

    # URL base oficial - IHVM Vacations
    DEFAULT_URL: ClassVar[str] = "https://ihmvacations.trackhs.com/api"

    # Configuración por defecto
    base_url: str
    username: str
    password: str
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "TrackHSConfig":
        """Crear configuración desde variables de entorno"""
        base_url = os.getenv("TRACKHS_API_URL", cls.DEFAULT_URL)
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")
        timeout = int(os.getenv("TRACKHS_TIMEOUT", "30"))

        # Validar que las credenciales estén configuradas
        if not username or not password:
            raise ValueError(
                "Credenciales de TrackHS no configuradas. "
                "Configura TRACKHS_USERNAME y TRACKHS_PASSWORD en variables de entorno."
            )

        # Intentar decodificar credenciales si están encriptadas
        try:
            # Verificar si las credenciales parecen estar encriptadas (hex)
            if len(username) == 32 and all(
                c in "0123456789ABCDEF" for c in username.upper()
            ):
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Credenciales parecen estar encriptadas. Usando valores tal como están."
                )
                # Si están encriptadas, podrías implementar decodificación aquí
                # Por ahora, usamos los valores tal como están
        except Exception:
            # Si hay error en la verificación, continuar con los valores originales
            pass

        return cls(
            base_url=base_url, username=username, password=password, timeout=timeout
        )

    def validate_url(self) -> bool:
        """Validar que la URL base sea válida"""
        # Verificar que la URL contenga el dominio correcto
        return "ihmvacations.trackhs.com" in self.base_url

    def get_endpoint_url(self, endpoint: str) -> str:
        """Obtener URL completa del endpoint"""
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url.rstrip('/')}{endpoint}"
