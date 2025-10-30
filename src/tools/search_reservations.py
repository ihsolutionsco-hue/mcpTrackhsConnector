"""
Herramienta para buscar reservas
"""

from typing import Any, Dict

from schemas.reservation import ReservationSearchParams, ReservationSearchResponse
from utils.exceptions import TrackHSAPIError

from .base import BaseTool


class SearchReservationsTool(BaseTool):
    """Herramienta para buscar reservas en TrackHS"""

    @property
    def name(self) -> str:
        return "search_reservations"

    @property
    def description(self) -> str:
        return """
        Buscar reservas en TrackHS con filtros avanzados.

        Permite buscar reservas por:
        - Texto libre (nombre, email, etc.)
        - Rango de fechas de llegada
        - Estado de la reserva
        - Paginación

        Returns:
            Lista de reservas encontradas con información detallada
        """

    @property
    def input_schema(self) -> type:
        return ReservationSearchParams

    @property
    def output_schema(self) -> type:
        return ReservationSearchResponse

    def _execute_logic(
        self, validated_input: ReservationSearchParams
    ) -> Dict[str, Any]:
        """
        Ejecuta la búsqueda de reservas

        Args:
            validated_input: Parámetros de búsqueda validados

        Returns:
            Resultado de la búsqueda
        """
        # Preparar parámetros para la API
        params = self._prepare_api_params(validated_input)

        # Realizar llamada a la API
        try:
            result = self.api_client.get("api/pms/reservations", params)

            # Procesar resultado
            processed_result = self._process_api_response(result)

            return processed_result

        except Exception as e:
            self.logger.error(
                f"Error en búsqueda de reservas",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "search_params": params,
                },
            )
            raise TrackHSAPIError(f"Error buscando reservas: {str(e)}")

    def _prepare_api_params(
        self, validated_input: ReservationSearchParams
    ) -> Dict[str, Any]:
        """
        Prepara parámetros para la llamada a la API

        Args:
            validated_input: Parámetros validados

        Returns:
            Parámetros formateados para la API
        """
        params = {"page": validated_input.page, "size": validated_input.size}

        if validated_input.search:
            params["search"] = validated_input.search

        if validated_input.arrival_start:
            params["arrivalStart"] = validated_input.arrival_start.strftime("%Y-%m-%d")

        if validated_input.arrival_end:
            params["arrivalEnd"] = validated_input.arrival_end.strftime("%Y-%m-%d")

        if validated_input.status:
            params["status"] = validated_input.status

        return params

    def _process_api_response(self, api_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de la API

        Args:
            api_result: Respuesta de la API

        Returns:
            Resultado procesado
        """
        # Calcular información de paginación
        total_items = api_result.get("total_items", 0)
        current_page = api_result.get("page", 1)
        page_size = api_result.get("size", 10)
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        # Procesar reservas
        reservations = api_result.get("reservations", [])
        processed_reservations = []

        for reservation in reservations:
            processed_reservation = self._process_reservation(reservation)
            processed_reservations.append(processed_reservation)

        return {
            "reservations": processed_reservations,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "page_size": page_size,
            "has_next": current_page < total_pages,
            "has_prev": current_page > 1,
        }

    def _process_reservation(self, reservation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una reserva individual

        Args:
            reservation: Datos de la reserva

        Returns:
            Reserva procesada
        """
        # Mapear campos de la API al schema
        processed = {
            "id": reservation.get("id"),
            "confirmation_number": reservation.get("confirmation_number"),
            "currency": reservation.get("currency"),
            "unit_id": reservation.get("unitId"),
            "unit_type_id": reservation.get("unitTypeId"),
            "arrival_date": reservation.get("arrival"),
            "departure_date": reservation.get("departure"),
            "status": reservation.get("status"),
            "total_amount": reservation.get("totalAmount"),
            "guest_count": reservation.get("guestCount"),
            "alternates": reservation.get("alternates"),
            "created_at": reservation.get("createdAt"),
            "updated_at": reservation.get("updatedAt"),
            "unit": reservation.get("unit"),
            "contact": reservation.get("contact"),
            "policies": reservation.get("policies"),
            "links": reservation.get("links"),
        }

        # Limpiar valores None
        return {k: v for k, v in processed.items() if v is not None}
