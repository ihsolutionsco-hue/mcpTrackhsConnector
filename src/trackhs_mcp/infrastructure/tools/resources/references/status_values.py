"""
Reference resources para Status Values
Valores válidos para el parámetro status
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ....application.ports.api_client_port import ApiClientPort


def register_status_values(mcp, api_client: "ApiClientPort"):
    """Registra los valores válidos de status"""

    @mcp.resource(
        "trackhs://reference/status-values",
        name="Status Values Reference",
        description="Valid values for status parameter",
        mime_type="application/json",
    )
    async def status_values() -> Dict[str, Any]:
        """Valores válidos para el parámetro status"""
        return {
            "valid_statuses": [
                {
                    "value": "Hold",
                    "description": "Reserva en espera de confirmación",
                    "color": "#FFA500",
                    "is_active": True,
                },
                {
                    "value": "Confirmed",
                    "description": "Reserva confirmada",
                    "color": "#28A745",
                    "is_active": True,
                },
                {
                    "value": "Checked In",
                    "description": "Huésped registrado",
                    "color": "#007BFF",
                    "is_active": True,
                },
                {
                    "value": "Checked Out",
                    "description": "Huésped salido",
                    "color": "#6C757D",
                    "is_active": False,
                },
                {
                    "value": "Cancelled",
                    "description": "Reserva cancelada",
                    "color": "#DC3545",
                    "is_active": False,
                },
            ],
            "usage_examples": {
                "single_status": "status=Confirmed",
                "multiple_statuses": "status=Confirmed,Checked In",
                "array_format": 'status=["Confirmed", "Checked In"]',
            },
        }
