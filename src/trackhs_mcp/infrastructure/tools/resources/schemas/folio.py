"""
Schema resources para Get Folio
Información esencial del esquema de datos para obtener folio
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_folio_schema(mcp, api_client: "ApiClientPort"):
    """Registra el schema de Get Folio"""

    @mcp.resource(
        "trackhs://schema/folio",
        name="Folio Schema",
        description="Schema for Get Folio API",
        mime_type="application/json",
    )
    async def folio_schema() -> Dict[str, Any]:
        """Schema esencial para Get Folio"""
        return {
            "endpoint": "/api/pms/folios/{folioId}",
            "method": "GET",
            "version": "1.0",
            "description": "Get individual folio with financial information",
            "fields": {
                "id": "integer - ID del folio",
                "type": "string - guest|master",
                "status": "string - open|closed",
                "currentBalance": "number - Balance actual",
                "realizedBalance": "number - Balance realizado",
                "startDate": "string - Fecha de inicio (ISO 8601)",
                "endDate": "string - Fecha de fin (ISO 8601)",
                "closedDate": "string - Fecha de cierre (ISO 8601)",
                "contactId": "integer - ID del contacto",
                "companyId": "integer - ID de la empresa",
                "reservationId": "integer - ID de la reserva",
                "travelAgentId": "integer - ID del agente de viajes",
                "name": "string - Nombre del folio",
                "taxEmpty": "boolean - Si está exento de impuestos",
            },
            "financial_info": {
                "agentCommission": "number - Comisión del agente",
                "ownerCommission": "number - Comisión del propietario",
                "ownerRevenue": "number - Ingresos del propietario",
                "checkInDate": "string - Fecha de check-in",
                "checkOutDate": "string - Fecha de check-out",
            },
            "embedded_objects": {
                "contact": "object - Información del contacto",
                "travelAgent": "object - Información del agente de viajes",
                "company": "object - Información de la empresa",
                "masterFolioRule": "object - Regla del folio maestro",
                "masterFolio": "object - Folio maestro",
            },
            "exception_handling": {
                "hasException": "boolean - Si tiene excepción",
                "exceptionMessage": "string - Mensaje de excepción",
            },
            "error_codes": {
                "401": "No autorizado - Credenciales inválidas",
                "403": "Prohibido - Permisos insuficientes",
                "404": "No encontrado - Folio no existe",
                "500": "Error interno del servidor",
            },
        }
