"""
Reference resources para Error Codes
Códigos de error comunes de la API
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_error_codes(mcp, api_client: "ApiClientPort"):
    """Registra los códigos de error comunes"""

    @mcp.resource(
        "trackhs://reference/error-codes",
        name="Error Codes Reference",
        description="Common error codes for TrackHS API",
        mime_type="application/json",
    )
    async def error_codes() -> Dict[str, Any]:
        """Códigos de error comunes de la API"""
        return {
            "common_errors": [
                {
                    "code": 400,
                    "title": "Bad Request",
                    "description": "Solicitud malformada o parámetros inválidos",
                    "common_causes": [
                        "Parámetros de fecha en formato incorrecto",
                        "Valores de status inválidos",
                        "IDs no numéricos",
                        "Parámetros requeridos faltantes",
                    ],
                },
                {
                    "code": 401,
                    "title": "Unauthorized",
                    "description": "Credenciales inválidas o expiradas",
                    "common_causes": [
                        "Token de autenticación inválido",
                        "Credenciales expiradas",
                        "Falta de autorización",
                    ],
                },
                {
                    "code": 403,
                    "title": "Forbidden",
                    "description": "Permisos insuficientes para acceder al recurso",
                    "common_causes": [
                        "Usuario sin permisos para la operación",
                        "Acceso restringido por rol",
                        "Recurso protegido",
                    ],
                },
                {
                    "code": 404,
                    "title": "Not Found",
                    "description": "Recurso no encontrado",
                    "common_causes": [
                        "ID de reserva inexistente",
                        "ID de folio inexistente",
                        "Endpoint incorrecto",
                    ],
                },
                {
                    "code": 422,
                    "title": "Unprocessable Entity",
                    "description": "Entidad no procesable",
                    "common_causes": [
                        "Validación de datos fallida",
                        "Reglas de negocio violadas",
                        "Datos inconsistentes",
                    ],
                },
                {
                    "code": 429,
                    "title": "Too Many Requests",
                    "description": "Límite de velocidad excedido",
                    "common_causes": [
                        "Demasiadas solicitudes por minuto",
                        "Rate limiting activado",
                        "Cuota de API excedida",
                    ],
                },
                {
                    "code": 500,
                    "title": "Internal Server Error",
                    "description": "Error interno del servidor",
                    "common_causes": [
                        "Error en base de datos",
                        "Servicio temporalmente no disponible",
                        "Error de configuración",
                    ],
                },
            ],
            "error_response_format": {
                "type": "object",
                "properties": {
                    "code": "string - Código de error específico",
                    "type": "string - URI del tipo de problema",
                    "title": "string - Título del error",
                    "status": "integer - Código HTTP",
                    "detail": "string - Descripción detallada",
                    "validation_messages": "array - Mensajes de validación",
                },
            },
            "troubleshooting": {
                "authentication_errors": "Verificar credenciales y tokens",
                "permission_errors": "Revisar roles y permisos del usuario",
                "validation_errors": "Validar formato de parámetros",
                "rate_limit_errors": "Implementar backoff exponencial",
                "server_errors": "Reintentar con delay apropiado",
            },
        }
