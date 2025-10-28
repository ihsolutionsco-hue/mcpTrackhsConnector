"""
Excepciones personalizadas para TrackHS MCP Server
"""


class TrackHSError(Exception):
    """Error base para TrackHS MCP Server"""

    pass


class AuthenticationError(TrackHSError):
    """Error de autenticación con TrackHS API"""

    pass


class APIError(TrackHSError):
    """Error de API TrackHS"""

    pass


class ValidationError(TrackHSError):
    """Error de validación de datos"""

    pass


class ConnectionError(TrackHSError):
    """Error de conexión con TrackHS API"""

    pass


class RateLimitError(TrackHSError):
    """Error de límite de velocidad de API"""

    pass


class NotFoundError(TrackHSError):
    """Error cuando no se encuentra un recurso"""

    pass
