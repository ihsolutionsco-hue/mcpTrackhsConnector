"""
Repository para reservas de TrackHS
Maneja todas las operaciones relacionadas con reservas
"""

import logging
from typing import Any, Dict, List, Optional

from .base import BaseRepository
from ..exceptions import NotFoundError, APIError

logger = logging.getLogger(__name__)


class ReservationRepository(BaseRepository):
    """Repository para operaciones de reservas"""

    def __init__(self, api_client, cache_ttl: int = 300):
        super().__init__(api_client, cache_ttl)
        self.base_endpoint = "pms/reservations"

    def get_by_id(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtener reserva por ID.

        Args:
            reservation_id: ID de la reserva

        Returns:
            Datos de la reserva

        Raises:
            NotFoundError: Si la reserva no existe
            APIError: Si hay error de API
        """
        cache_key = f"reservation_{reservation_id}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Fetching reservation {reservation_id} from API")
            result = self.api_client.get(f"{self.base_endpoint}/{reservation_id}")

            # Guardar en cache
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"get_reservation_{reservation_id}")

    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buscar reservas con filtros.

        Args:
            filters: Filtros de búsqueda (page, size, search, arrival_start, etc.)

        Returns:
            Resultados de búsqueda con metadatos de paginación
        """
        # Crear clave de cache basada en filtros
        cache_key = f"reservations_search_{hash(frozenset(filters.items()))}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Searching reservations with filters: {filters}")
            result = self.api_client.get(self.base_endpoint, params=filters)

            # Guardar en cache (con TTL más corto para búsquedas)
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"search_reservations_{filters}")

    def get_folio(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtener folio financiero de una reserva.

        Args:
            reservation_id: ID de la reserva

        Returns:
            Datos del folio financiero

        Raises:
            NotFoundError: Si la reserva no existe
            APIError: Si hay error de API
        """
        cache_key = f"reservation_folio_{reservation_id}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Fetching folio for reservation {reservation_id}")
            result = self.api_client.get(f"{self.base_endpoint}/{reservation_id}/folio")

            # Guardar en cache
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"get_folio_{reservation_id}")

    def search_by_date_range(self, start_date: str, end_date: str, **kwargs) -> Dict[str, Any]:
        """
        Buscar reservas por rango de fechas.

        Args:
            start_date: Fecha de inicio (YYYY-MM-DD)
            end_date: Fecha de fin (YYYY-MM-DD)
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {
            "arrival_start": start_date,
            "arrival_end": end_date,
            **kwargs
        }
        return self.search(filters)

    def search_by_status(self, status: str, **kwargs) -> Dict[str, Any]:
        """
        Buscar reservas por estado.

        Args:
            status: Estado de la reserva (confirmed, cancelled, etc.)
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {
            "status": status,
            **kwargs
        }
        return self.search(filters)

    def search_by_guest(self, search_term: str, **kwargs) -> Dict[str, Any]:
        """
        Buscar reservas por término de búsqueda (nombre, email, confirmación).

        Args:
            search_term: Término de búsqueda
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {
            "search": search_term,
            **kwargs
        }
        return self.search(filters)

    def _test_connection(self) -> None:
        """Probar conexión con la API de reservas"""
        try:
            # Hacer una búsqueda simple para probar conectividad
            self.api_client.get(self.base_endpoint, {"page": 1, "size": 1})
        except Exception as e:
            raise APIError(f"Error conectando con API de reservas: {str(e)}")

    def get_reservation_summary(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtener resumen de una reserva (datos básicos sin folio).

        Args:
            reservation_id: ID de la reserva

        Returns:
            Resumen de la reserva
        """
        reservation = self.get_by_id(reservation_id)

        # Extraer solo datos básicos para el resumen
        summary = {
            "id": reservation.get("id"),
            "confirmation_number": reservation.get("confirmationNumber"),
            "guest_name": reservation.get("guest", {}).get("name"),
            "guest_email": reservation.get("guest", {}).get("email"),
            "arrival_date": reservation.get("arrivalDate"),
            "departure_date": reservation.get("departureDate"),
            "status": reservation.get("status"),
            "unit_id": reservation.get("unit", {}).get("id"),
            "unit_name": reservation.get("unit", {}).get("name"),
        }

        return summary
