"""
Schema resources para Search Reservations V1
Información esencial del esquema de datos para API V1
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_reservations_v1_schema(mcp, api_client: "ApiClientPort"):
    """Registra el schema de Search Reservations V1"""

    @mcp.resource(
        "trackhs://schema/reservations-v1",
        name="Reservations V1 Schema",
        description="Schema for Search Reservations API V1",
        mime_type="application/json",
    )
    async def reservations_v1_schema() -> Dict[str, Any]:
        """Schema esencial para Search Reservations V1"""
        return {
            "endpoint": "/pms/reservations",
            "method": "GET",
            "version": "1.0",
            "description": "Search reservations with API V1",
            "fields": {
                "id": "integer - ID único de la reserva",
                "name": "string - Nombre de la reserva",
                "status": "string - Hold|Confirmed|Checked In|Checked Out|Cancelled",
                "unit_id": "integer - ID de la unidad",
                "contact_id": "integer - ID del contacto",
                "arrival_date": "string - Fecha de llegada (ISO 8601)",
                "departure_date": "string - Fecha de salida (ISO 8601)",
                "nights": "number - Número de noches",
                "created_at": "string - Fecha de creación (ISO 8601)",
                "updated_at": "string - Fecha de actualización (ISO 8601)",
                "booked_at": "string - Fecha de reserva (ISO 8601)",
            },
            "pagination": {
                "page": "integer - Número de página (0-based, max 10k total)",
                "size": "integer - Tamaño de página (max 1000)",
            },
            "filtering": {
                "search": "string - Búsqueda por texto",
                "status": "string - Estado de reserva",
                "arrivalStart": "string - Fecha inicio llegada",
                "arrivalEnd": "string - Fecha fin llegada",
                "departureStart": "string - Fecha inicio salida",
                "departureEnd": "string - Fecha fin salida",
                "nodeId": "integer - ID del nodo",
                "unitId": "integer - ID de la unidad",
                "contactId": "integer - ID del contacto",
            },
            "sorting": {
                "sortColumn": "string - name|status|checkin|checkout|nights",
                "sortDirection": "string - asc|desc",
            },
            "limits": {
                "max_total_results": 10000,
                "max_page_size": 1000,
                "scroll_timeout": "1 minute",
            },
        }
