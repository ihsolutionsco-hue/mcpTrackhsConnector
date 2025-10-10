"""
Módulo de autenticación para Track HS API
"""

import base64
from typing import Optional
from .types import TrackHSConfig

class TrackHSAuth:
    """Manejador de autenticación para Track HS API"""
    
    def __init__(self, config: TrackHSConfig):
        self.config = config
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Valida que las credenciales estén configuradas correctamente"""
        if not self.config.username or not self.config.password:
            raise ValueError("Username y password son requeridos para la autenticación")
        
        if not self.config.base_url:
            raise ValueError("Base URL es requerida")
    
    def get_auth_header(self) -> str:
        """Genera el header de autenticación Basic Auth"""
        credentials = f"{self.config.username}:{self.config.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return f"Basic {encoded_credentials}"
    
    def get_headers(self) -> dict[str, str]:
        """Retorna los headers de autenticación completos"""
        return {
            "Authorization": self.get_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def validate_credentials(self) -> bool:
        """Valida que las credenciales estén configuradas correctamente"""
        try:
            self._validate_credentials()
            return True
        except ValueError:
            return False
