"""
Herramienta MCP para obtener una reserva específica por ID en TrackHS API V2
Versión mejorada con tipos específicos siguiendo mejores prácticas MCP
"""

from typing import TYPE_CHECKING, Any, Dict

from pydantic import Field

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...application.use_cases.get_reservation import GetReservationUseCase
from ...domain.entities.reservations import GetReservationParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler
from ..utils.user_friendly_messages import format_required_error, format_type_error


def register_get_reservation_v2(mcp, api_client: "ApiClientPort"):
    """Registra la herramienta get_reservation_v2 mejorada"""

    @mcp.tool(name="get_reservation")
    @error_handler("get_reservation")
    async def get_reservation_v2(
        reservation_id: str = Field(
            description=(
                "Unique reservation ID (positive integer as string). "
                "Example: '12345' or '37152796'"
            ),
            pattern=r"^\d+$",
            min_length=1,
            max_length=20,
        )
    ) -> Dict[str, Any]:
        """
        Get complete reservation details by ID from TrackHS API V2.

        Retrieves all information for a specific reservation including financial data,
        embedded objects (unit, contact, policies), occupants, and metadata.

        Returns:
            Complete reservation object with guest information, unit details, pricing,
            policies, payment breakdowns, and all embedded data.

        Raises:
            ValidationError: If reservation_id is invalid or reservation not found
            APIError: If API request fails (401, 403, 404, 500)
        """
        # Validar parámetros de entrada
        if not reservation_id or not reservation_id.strip():
            raise ValidationError(
                format_required_error("reservation_id"),
                "reservation_id",
            )

        # Validar que sea un número entero positivo válido
        try:
            reservation_id_int = int(reservation_id.strip())
            if reservation_id_int <= 0:
                raise ValueError("ID debe ser positivo")
        except (ValueError, TypeError):
            raise ValidationError(
                format_type_error(
                    "reservation_id", "número entero positivo", reservation_id
                ),
                "reservation_id",
            )

        try:
            # Crear caso de uso
            use_case = GetReservationUseCase(api_client)

            # Crear parámetros con el ID convertido a entero
            params = GetReservationParams(reservation_id=reservation_id_int)

            # Ejecutar caso de uso
            reservation = await use_case.execute(params)

            # Convertir a diccionario para respuesta MCP
            result: Dict[str, Any] = reservation.model_dump(
                by_alias=True, exclude_none=True
            )
            return result

        except Exception as e:
            # Manejar errores específicos de la API
            if hasattr(e, "status_code"):
                if e.status_code == 401:
                    raise ValidationError(
                        "No autorizado: Credenciales de autenticación inválidas. "
                        "Por favor verifica que TRACKHS_USERNAME y TRACKHS_PASSWORD "
                        "sean correctos y no hayan expirado.",
                        "auth",
                    )
                elif e.status_code == 403:
                    raise ValidationError(
                        "Prohibido: Permisos insuficientes para acceder a esta reserva. "
                        "Por favor verifica que tu cuenta tenga acceso a "
                        "los endpoints de PMS/Reservations.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Reserva no encontrada: No existe una reserva con ID {reservation_id}. "
                        "Por favor verifica que el ID sea correcto y que la reserva exista.",
                        "reservation_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API de TrackHS está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte técnico.",
                        "api",
                    )

            # Re-lanzar otros errores con contexto
            raise ValidationError(f"Error al obtener la reserva: {str(e)}", "api")
