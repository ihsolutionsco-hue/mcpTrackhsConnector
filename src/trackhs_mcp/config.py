"""
Configuración centralizada para TrackHS MCP Connector
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class TrackHSConfig:
    """Configuración centralizada para TrackHS API"""
    
    # URL base oficial - IHVM Vacations
    DEFAULT_URL = "https://ihmvacations.trackhs.com/api"
    
    # Configuración por defecto
    base_url: str
    username: str
    password: str
    timeout: int = 30
    
    @classmethod
    def from_env(cls) -> 'TrackHSConfig':
        """Crear configuración desde variables de entorno"""
        base_url = os.getenv("TRACKHS_API_URL", cls.DEFAULT_URL)
        username = os.getenv("TRACKHS_USERNAME", "aba99777416466b6bdc1a25223192ccb")
        password = os.getenv("TRACKHS_PASSWORD", "18c87461011f355cc11000a24215cbda")
        timeout = int(os.getenv("TRACKHS_TIMEOUT", "30"))
        
        return cls(
            base_url=base_url,
            username=username,
            password=password,
            timeout=timeout
        )
    
    def validate_url(self) -> bool:
        """Validar que la URL base sea válida"""
        # Verificar que la URL contenga el dominio correcto
        return "ihmvacations.trackhs.com" in self.base_url
    
    def get_endpoint_url(self, endpoint: str) -> str:
        """Obtener URL completa del endpoint"""
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return f"{self.base_url.rstrip('/')}{endpoint}"
