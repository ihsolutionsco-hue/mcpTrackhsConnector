"""
Excepciones del dominio para la API
"""

from typing import Optional


class ApiError(Exception):
    """Excepción personalizada para errores de la API"""

    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        status_text: Optional[str] = None,
    ):
        self.message = message
        self.status = status
        self.status_text = status_text
        super().__init__(self.message)


class AuthenticationError(ApiError):
    """Error de autenticación"""

    pass


class ValidationError(ApiError):
    """Error de validación de datos"""

    pass


class NetworkError(ApiError):
    """Error de red"""

    pass


class TimeoutError(ApiError):
    """Error de timeout"""

    pass
