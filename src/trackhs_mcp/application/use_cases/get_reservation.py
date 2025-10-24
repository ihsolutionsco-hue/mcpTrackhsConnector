"""
Use Case para obtener una reserva específica por ID desde TrackHS API V2
Implementa la lógica de negocio para el endpoint GET /v2/pms/reservations/{reservationId}
"""

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ...application.ports.api_client_port import ApiClientPort

from ...domain.entities.reservations import GetReservationParams, Reservation
from ...domain.exceptions.api_exceptions import ValidationError
from ...infrastructure.utils.error_handling import error_handler


class GetReservationUseCase:
    """Use Case para obtener una reserva específica por ID"""

    def __init__(self, api_client: "ApiClientPort"):
        self.api_client = api_client

    @error_handler("get_reservation")
    async def execute(self, params: GetReservationParams) -> Reservation:
        """
        Ejecuta la obtención de una reserva específica por ID.

        Args:
            params: Parámetros que incluyen el reservation_id

        Returns:
            Objeto Reservation completo con datos embebidos

        Raises:
            ValidationError: Si el ID de reserva es inválido
            ApiError: Si la API retorna error
            AuthenticationError: Si hay problemas de autenticación
        """
        # Validar parámetros de entrada
        if not params.reservation_id:
            raise ValidationError(
                "reservation_id es requerido",
                "reservation_id",
            )

        # Validar que el ID sea positivo
        if params.reservation_id <= 0:
            raise ValidationError(
                "reservation_id debe ser un número entero positivo válido",
                "reservation_id",
            )

        try:
            # Construir endpoint
            endpoint = f"/api/v2/pms/reservations/{params.reservation_id}"

            # Realizar petición GET a la API
            response_data = await self.api_client.get(endpoint)

            # Validar que la respuesta contiene datos
            if not response_data:
                raise ValidationError(
                    f"No se encontraron datos para la reserva ID {params.reservation_id}",
                    "reservation_id",
                )

            # Manejar caso donde la respuesta llegue como string JSON
            if isinstance(response_data, str):
                import json

                try:
                    response_data: Dict[str, Any] = json.loads(response_data)
                except json.JSONDecodeError as e:
                    raise ValidationError(
                        f"Error al parsear respuesta JSON: {str(e)}",
                        "api",
                    )

            # Crear objeto Reservation desde la respuesta
            reservation = Reservation.model_validate(response_data)

            return reservation

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
                        "Prohibido: Permisos insuficientes para esta operación. "
                        "Por favor verifica que tu cuenta tenga acceso a "
                        "los endpoints de PMS/Reservations.",
                        "permissions",
                    )
                elif e.status_code == 404:
                    raise ValidationError(
                        f"Reserva no encontrada: No existe una reserva con ID {params.reservation_id}. "
                        "Por favor verifica que el ID sea correcto.",
                        "reservation_id",
                    )
                elif e.status_code == 500:
                    raise ValidationError(
                        "Error interno del servidor: La API está temporalmente no disponible. "
                        "Por favor intenta nuevamente más tarde o contacta soporte.",
                        "api",
                    )

            # Re-lanzar otros errores
            raise ValidationError(f"Error en la petición a la API: {str(e)}", "api")
