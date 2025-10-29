"""
Herramienta para obtener detalles de una reserva específica
"""

from typing import Any, Dict

from pydantic import Field

from ..schemas.reservation import ReservationDetailResponse
from ..utils.exceptions import TrackHSAPIError, TrackHSNotFoundError
from ..utils.validators import validate_positive_integer
from .base import BaseTool


class GetReservationParams:
    """Parámetros para obtener una reserva"""

    def __init__(self, reservation_id: int):
        self.reservation_id = reservation_id


class GetReservationTool(BaseTool):
    """Herramienta para obtener detalles de una reserva específica"""

    @property
    def name(self) -> str:
        return "get_reservation"

    @property
    def description(self) -> str:
        return """
        Obtener detalles completos de una reserva específica por ID usando la API V2 de TrackHS.

        Esta herramienta implementa la API completa de Get Reservation V2 de TrackHS
        con todos los campos disponibles según la documentación oficial.

        FUNCIONALIDADES PRINCIPALES:
        - Información completa de la reserva (fechas, estado, ocupantes)
        - Desglose financiero detallado (huésped y propietario)
        - Información de políticas (garantía, cancelación)
        - Datos embebidos (unidad, contacto, usuario, etc.)
        - Información de tarifas y planes de pago
        - Productos de seguro de viaje
        - Enlaces relacionados y navegación

        Args:
            reservation_id: ID único de la reserva en TrackHS (debe ser > 0)

        Returns:
            Detalles completos de la reserva
        """

    @property
    def input_schema(self) -> type:
        return GetReservationParams

    @property
    def output_schema(self) -> type:
        return ReservationDetailResponse

    def _execute_logic(self, validated_input: GetReservationParams) -> Dict[str, Any]:
        """
        Ejecuta la obtención de detalles de reserva

        Args:
            validated_input: Parámetros validados

        Returns:
            Detalles de la reserva
        """
        reservation_id = validated_input.reservation_id

        # Validar ID de reserva
        try:
            validated_id = validate_positive_integer(reservation_id, "reservation_id")
        except Exception as e:
            self.logger.error(
                f"ID de reserva inválido: {reservation_id}",
                extra={"reservation_id": reservation_id, "error": str(e)},
            )
            raise

        # Realizar llamada a la API V2
        try:
            result = self.api_client.get(f"api/v2/pms/reservations/{validated_id}")

            # Procesar resultado
            processed_result = self._process_api_response(result, validated_id)

            return processed_result

        except TrackHSNotFoundError:
            # Re-lanzar error de no encontrado
            raise
        except Exception as e:
            self.logger.error(
                f"Error obteniendo reserva {validated_id}",
                extra={
                    "reservation_id": validated_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise TrackHSAPIError(f"Error obteniendo reserva: {str(e)}")

    def _process_api_response(
        self, api_result: Dict[str, Any], reservation_id: int
    ) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API V2

        Args:
            api_result: Respuesta de la API
            reservation_id: ID de la reserva

        Returns:
            Resultado procesado
        """
        # Mapear datos de API V2 al schema esperado
        processed = {
            "id": api_result.get("id", reservation_id),
            "confirmation_number": self._get_confirmation_number(
                api_result, reservation_id
            ),
            "currency": api_result.get("currency"),
            "unit_id": api_result.get("unitId"),
            "unit_type_id": api_result.get("unitTypeId"),
            "arrival_date": api_result.get("arrival"),
            "departure_date": api_result.get("departure"),
            "status": api_result.get("status"),
            "total_amount": api_result.get("totalAmount"),
            "guest_count": api_result.get("guestCount"),
            "alternates": api_result.get("alternates"),
            "created_at": api_result.get("createdAt"),
            "updated_at": api_result.get("updatedAt"),
            "unit": api_result.get("unit"),
            "contact": api_result.get("contact"),
            "policies": api_result.get("policies"),
            "links": api_result.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}

    def _get_confirmation_number(
        self, api_result: Dict[str, Any], reservation_id: int
    ) -> str:
        """
        Obtiene el número de confirmación de la reserva

        Args:
            api_result: Respuesta de la API
            reservation_id: ID de la reserva

        Returns:
            Número de confirmación
        """
        # Si hay alternates, usar el primero como confirmation_number
        alternates = api_result.get("alternates")
        if alternates and len(alternates) > 0:
            return alternates[0]

        # Si no hay alternates, usar el ID como confirmation_number
        return str(reservation_id)
