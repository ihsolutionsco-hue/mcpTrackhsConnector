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
                "Example: '12345' or '37152796'. "
                "Must be a valid positive integer. Invalid formats like 'abc123', '-1', or empty strings will be rejected."
            ),
            pattern=r"^\d+$",
            min_length=1,
            max_length=20,
        )
    ) -> Dict[str, Any]:
        """
        Get complete reservation details by ID from TrackHS API V2.

        **CLIENT-FOCUSED FEATURES:**
        - Complete guest information (contact details, preferences)
        - Full stay details (dates, unit, occupancy, policies)
        - Comprehensive financial breakdown (payments, balances, fees)
        - Operational information (check-in/out times, special requests)
        - Embedded objects (unit details, contact info, policies)

        **RETURNS:**
        - Complete reservation object with guest information, unit details, pricing,
          policies, payment breakdowns, and all embedded data
        - Financial breakdowns (guest_breakdown, owner_breakdown, security_deposit)
        - Operational details (arrival/departure times, check-in/out procedures)
        - Contact information and special requirements
        - Policy information (cancellation, guarantee, payment terms)

        **VALIDATION:**
        - reservation_id must be a positive integer (rejects 'abc123', '-1', empty)
        - Returns 404 error for non-existent reservations
        - Provides clear error messages for invalid inputs

        **CLIENT USE CASES:**
        - Guest check-in preparation and verification
        - Financial reconciliation and payment tracking
        - Operational planning and special request handling
        - Customer service and guest communication
        - Reservation status monitoring and updates

        **TESTING INSIGHTS:**
        - Validates input format strictly (only positive integers)
        - Handles non-existent reservations gracefully
        - Provides comprehensive guest and financial information
        - Returns complete operational data for hotel staff
        - Supports real-world hotel management workflows

        Raises:
            ValidationError: If reservation_id is invalid or reservation not found
            APIError: If API request fails (401, 403, 404, 500)
        """
        # Validar parámetros de entrada con mensajes mejorados basados en testing
        if not reservation_id or not reservation_id.strip():
            raise ValidationError(
                "Input validation error: '' should be non-empty",
                "reservation_id",
            )

        # Validar que sea un número entero positivo válido con mensajes específicos
        try:
            reservation_id_int = int(reservation_id.strip())
            if reservation_id_int <= 0:
                raise ValueError("ID debe ser positivo")
        except (ValueError, TypeError):
            # Mensaje específico basado en el tipo de error encontrado en testing
            if reservation_id.startswith("-"):
                raise ValidationError(
                    f"Input validation error: '{reservation_id}' does not match '^\\d+$'",
                    "reservation_id",
                )
            elif any(c.isalpha() for c in reservation_id):
                raise ValidationError(
                    f"Input validation error: '{reservation_id}' does not match '^\\d+$'",
                    "reservation_id",
                )
            else:
                raise ValidationError(
                    f"Input validation error: '{reservation_id}' does not match '^\\d+$'",
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
            # Manejar errores específicos de la API con mensajes mejorados basados en testing
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
                        f"Error calling tool 'get_reservation': Error al obtener la reserva: "
                        f"Reserva no encontrada: No existe una reserva con ID {reservation_id}. "
                        "Por favor verifica que el ID sea correcto.",
                        "reservation_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API de TrackHS está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte técnico.",
                        "api",
                    )

            # Re-lanzar otros errores con contexto mejorado
            raise ValidationError(
                f"Error calling tool 'get_reservation': Error al obtener la reserva: {str(e)}",
                "api",
            )
