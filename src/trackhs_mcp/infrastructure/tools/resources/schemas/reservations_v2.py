"""
Schema resources para Search Reservations V2
Información esencial del esquema de datos para API V2
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_reservations_v2_schema(mcp, api_client: "ApiClientPort"):
    """Registra el schema de Search Reservations V2"""

    @mcp.resource(
        "trackhs://schema/reservations-v2",
        name="Reservations V2 Schema",
        description="Schema for Search Reservations API V2",
        mime_type="application/json",
    )
    async def reservations_v2_schema() -> Dict[str, Any]:
        """Schema esencial para Search Reservations V2"""
        return {
            "endpoint": "/api/v2/pms/reservations",
            "method": "GET",
            "version": "2.0",
            "description": "Search reservations with API V2 (recommended)",
            "fields": {
                "id": "integer - ID único de la reserva",
                "alternates": "array - IDs de confirmación alternativos",
                "currency": "string - Moneda de la reserva",
                "unitId": "integer - ID de la unidad",
                "arrivalDate": "string - Fecha de llegada (ISO 8601)",
                "departureDate": "string - Fecha de salida (ISO 8601)",
                "nights": "number - Número de noches",
                "status": "string - Hold|Confirmed|Checked In|Checked Out|Cancelled",
                "contactId": "integer - ID del contacto",
                "channelId": "integer - ID del canal",
                "userId": "integer - ID del usuario",
                "travelAgentId": "integer - ID del agente de viajes",
                "campaignId": "integer - ID de la campaña",
                "unitTypeId": "integer - ID del tipo de unidad",
                "rateTypeId": "integer - ID del tipo de tarifa",
                "reservationTypeId": "integer - ID del tipo de reserva",
                "createdAt": "string - Fecha de creación (ISO 8601)",
                "updatedAt": "string - Fecha de actualización (ISO 8601)",
                "bookedAt": "string - Fecha de reserva (ISO 8601)",
            },
            "pagination": {
                "page": "integer - Número de página (0-based, max 10k total)",
                "size": "integer - Tamaño de página (max 1000)",
            },
            "filtering": {
                "search": "string - Búsqueda por texto",
                "status": "string|array - Estado(s) de reserva",
                "arrivalStart": "string - Fecha inicio llegada",
                "arrivalEnd": "string - Fecha fin llegada",
                "departureStart": "string - Fecha inicio salida",
                "departureEnd": "string - Fecha fin salida",
                "bookedStart": "string - Fecha inicio reserva",
                "bookedEnd": "string - Fecha fin reserva",
                "updatedSince": "string - Actualizadas desde fecha",
                "nodeId": "integer|array - ID(s) del nodo",
                "unitId": "integer|array - ID(s) de la unidad",
                "contactId": "integer|array - ID(s) del contacto",
                "travelAgentId": "integer|array - ID(s) del agente",
                "campaignId": "integer|array - ID(s) de la campaña",
                "userId": "integer|array - ID(s) del usuario",
                "unitTypeId": "integer|array - ID(s) del tipo de unidad",
                "rateTypeId": "integer|array - ID(s) del tipo de tarifa",
                "reservationTypeId": "integer|array - ID(s) del tipo de reserva",
                "groupId": "integer - ID del grupo",
                "checkinOfficeId": "integer - ID de la oficina de check-in",
                "inHouseToday": "integer - 0|1 - Huéspedes en casa hoy",
                "scroll": "integer|string - Scroll de Elasticsearch",
            },
            "sorting": {
                "sortColumn": "string - name|status|checkin|checkout|nights",
                "sortDirection": "string - asc|desc",
            },
            "improvements_v2": {
                "more_parameters": "25+ parámetros vs 20 en V1",
                "better_performance": "Consultas optimizadas",
                "enriched_data": "Información financiera completa",
                "flexibility": "Múltiples valores para algunos parámetros",
            },
            "limits": {
                "max_total_results": 10000,
                "max_page_size": 1000,
                "scroll_timeout": "1 minute",
            },
        }
