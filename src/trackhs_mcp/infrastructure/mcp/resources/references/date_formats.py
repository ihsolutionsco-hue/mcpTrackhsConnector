"""
Reference resources para Date Formats
Formatos de fecha soportados por la API
"""

from typing import Any, Dict

from ....application.ports.api_client_port import ApiClientPort


def register_date_formats(mcp, api_client: ApiClientPort):
    """Registra los formatos de fecha soportados"""

    @mcp.resource(
        "trackhs://reference/date-formats",
        name="Date Formats Reference",
        description="Supported date formats for API",
        mime_type="application/json",
    )
    async def date_formats() -> Dict[str, Any]:
        """Formatos de fecha soportados por la API"""
        return {
            "supported_formats": [
                {
                    "format": "YYYY-MM-DD",
                    "example": "2024-01-01",
                    "description": "Solo fecha",
                    "usage": "Para rangos de fechas básicos",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SS",
                    "example": "2024-01-01T00:00:00",
                    "description": "Fecha y hora sin timezone",
                    "usage": "Para fechas específicas",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SSZ",
                    "example": "2024-01-01T00:00:00Z",
                    "description": "Fecha y hora con timezone UTC",
                    "usage": "Para fechas con timezone explícito",
                },
                {
                    "format": "YYYY-MM-DDTHH:MM:SS+HH:MM",
                    "example": "2024-01-01T00:00:00+00:00",
                    "description": "Fecha y hora con offset",
                    "usage": "Para fechas con timezone específico",
                },
            ],
            "examples": {
                "arrival_start": "2024-01-01",
                "arrival_end": "2024-01-31T23:59:59Z",
                "booked_start": "2024-01-01T00:00:00",
                "updated_since": "2024-01-01T00:00:00Z",
            },
            "best_practices": [
                "Usar formato ISO 8601 completo para fechas específicas",
                "Usar solo fecha (YYYY-MM-DD) para rangos de días completos",
                "Especificar timezone cuando sea relevante",
                "Usar Z para UTC cuando no se especifique timezone",
            ],
        }
