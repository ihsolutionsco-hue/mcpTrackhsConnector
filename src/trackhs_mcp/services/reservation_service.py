"""
Servicio de Reservas para TrackHS.
Contiene la lógica de negocio para reservas.
"""

import logging
from typing import Any, Dict, Optional

from ..exceptions import NotFoundError, TrackHSError, ValidationError
from ..repositories import ReservationRepository

logger = logging.getLogger(__name__)


class ReservationService:
    """
    Servicio para gestión de reservas.

    Separa la lógica de negocio de las herramientas MCP,
    permitiendo testing y reutilización.
    """

    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def search_reservations(
        self,
        page: int = 0,
        size: int = 10,
        search: Optional[str] = None,
        arrival_start: Optional[str] = None,
        arrival_end: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Buscar reservas con filtros avanzados.

        Args:
            page: Número de página (0-based)
            size: Tamaño de página (1-100)
            search: Búsqueda de texto completo
            arrival_start: Fecha de llegada inicio (YYYY-MM-DD)
            arrival_end: Fecha de llegada fin (YYYY-MM-DD)
            status: Estado de reserva

        Returns:
            Resultado de la búsqueda

        Raises:
            ValidationError: Si los parámetros no son válidos
            TrackHSError: Si hay error en la API
        """
        # Validaciones de negocio
        if page < 0:
            raise ValidationError("El número de página debe ser mayor o igual a 0")

        if size < 1 or size > 100:
            raise ValidationError("El tamaño de página debe estar entre 1 y 100")

        if page * size > 10000:
            raise ValidationError("Límite de búsqueda excedido: page * size <= 10000")

        # Validar fechas si se proporcionan
        if arrival_start:
            self._validate_date_format(arrival_start, "arrival_start")

        if arrival_end:
            self._validate_date_format(arrival_end, "arrival_end")

        if arrival_start and arrival_end:
            from datetime import datetime

            start_date = datetime.strptime(arrival_start, "%Y-%m-%d")
            end_date = datetime.strptime(arrival_end, "%Y-%m-%d")
            if start_date > end_date:
                raise ValidationError(
                    "arrival_start no puede ser posterior a arrival_end"
                )

        logger.info(f"Buscando reservas: página {page}, tamaño {size}")

        try:
            # Construir parámetros usando nombres correctos según documentación API
            params = {"page": page, "size": size}
            if search:
                params["search"] = search
            if arrival_start:
                # Convertir formato YYYY-MM-DD a ISO 8601 para API
                params["arrivalStart"] = self._convert_to_iso8601(arrival_start)
            if arrival_end:
                # Convertir formato YYYY-MM-DD a ISO 8601 para API
                params["arrivalEnd"] = self._convert_to_iso8601(arrival_end)
            if status:
                params["status"] = status

            result = self.reservation_repo.search(params)

            # WORKAROUND: Filtro del lado del cliente para compensar bug de API TrackHS
            # La API no respeta los filtros de fecha, así que filtramos localmente
            if arrival_start or arrival_end:
                result = self._apply_client_side_date_filter(
                    result, arrival_start, arrival_end
                )

            logger.info(
                f"Búsqueda de reservas completada. Encontradas: {result.get('total_items', 0)}"
            )
            return result

        except Exception as e:
            logger.error(f"Error buscando reservas: {str(e)}")
            raise TrackHSError(f"Error buscando reservas: {str(e)}")

    def get_reservation_by_id(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtener una reserva por ID.

        Args:
            reservation_id: ID de la reserva

        Returns:
            Datos de la reserva

        Raises:
            ValidationError: Si el ID no es válido
            NotFoundError: Si la reserva no existe
            TrackHSError: Si hay error en la API
        """
        if reservation_id <= 0:
            raise ValidationError("El ID de reserva debe ser mayor a 0")

        logger.info(f"Obteniendo reserva {reservation_id}")

        try:
            result = self.reservation_repo.get_by_id(reservation_id)
            logger.info(f"Reserva {reservation_id} obtenida exitosamente")
            return result

        except NotFoundError:
            logger.warning(f"Reserva {reservation_id} no encontrada")
            raise
        except Exception as e:
            logger.error(f"Error obteniendo reserva {reservation_id}: {str(e)}")
            raise TrackHSError(f"Error obteniendo reserva {reservation_id}: {str(e)}")

    def get_folio(self, reservation_id: int) -> Dict[str, Any]:
        """
        Obtener el folio financiero de una reserva.

        Args:
            reservation_id: ID de la reserva

        Returns:
            Folio financiero

        Raises:
            ValidationError: Si el ID no es válido
            NotFoundError: Si la reserva no existe
            TrackHSError: Si hay error en la API
        """
        if reservation_id <= 0:
            raise ValidationError("El ID de reserva debe ser mayor a 0")

        logger.info(f"Obteniendo folio de reserva {reservation_id}")

        try:
            result = self.reservation_repo.get_folio(reservation_id)
            logger.info(f"Folio de reserva {reservation_id} obtenido exitosamente")
            return result

        except NotFoundError:
            logger.warning(f"Folio de reserva {reservation_id} no encontrado")
            raise
        except Exception as e:
            logger.error(
                f"Error obteniendo folio de reserva {reservation_id}: {str(e)}"
            )
            raise TrackHSError(
                f"Error obteniendo folio de reserva {reservation_id}: {str(e)}"
            )

    def _validate_date_format(self, date_str: str, field_name: str) -> None:
        """
        Validar formato de fecha YYYY-MM-DD.

        Args:
            date_str: String de fecha
            field_name: Nombre del campo para el error

        Raises:
            ValidationError: Si el formato no es válido
        """
        try:
            from datetime import datetime

            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(f"{field_name} debe tener formato YYYY-MM-DD")

    def _convert_to_iso8601(self, date_str: str) -> str:
        """
        Convertir fecha YYYY-MM-DD a formato ISO 8601 para la API.

        Args:
            date_str: Fecha en formato YYYY-MM-DD

        Returns:
            Fecha en formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
        """
        from datetime import datetime

        try:
            # Parsear fecha YYYY-MM-DD
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # Convertir a ISO 8601 con timezone UTC
            return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            # Si ya está en formato ISO 8601, devolverlo tal como está
            return date_str

    def _apply_client_side_date_filter(
        self,
        result: Dict[str, Any],
        arrival_start: Optional[str],
        arrival_end: Optional[str],
    ) -> Dict[str, Any]:
        """
        Aplicar filtro de fechas del lado del cliente para compensar bug de API TrackHS.

        Args:
            result: Resultado de la búsqueda de la API
            arrival_start: Fecha de inicio (YYYY-MM-DD)
            arrival_end: Fecha de fin (YYYY-MM-DD)

        Returns:
            Resultado filtrado
        """
        from datetime import datetime

        reservations = result.get("_embedded", {}).get("reservations", [])
        filtered_reservations = []

        for reservation in reservations:
            arrival_date = reservation.get("arrivalDate")
            if not arrival_date:
                continue

            # Convertir fecha de llegada a objeto datetime para comparación
            try:
                res_date = datetime.strptime(arrival_date, "%Y-%m-%d")

                # Aplicar filtros de fecha
                if arrival_start:
                    start_date = datetime.strptime(arrival_start, "%Y-%m-%d")
                    if res_date < start_date:
                        continue

                if arrival_end:
                    end_date = datetime.strptime(arrival_end, "%Y-%m-%d")
                    if res_date > end_date:
                        continue

                filtered_reservations.append(reservation)

            except ValueError:
                # Si no se puede parsear la fecha, omitir esta reserva
                logger.warning(f"No se pudo parsear fecha de llegada: {arrival_date}")
                continue

        # Actualizar el resultado con las reservas filtradas
        result["_embedded"]["reservations"] = filtered_reservations
        result["total_items"] = len(filtered_reservations)
        result["page_size"] = len(filtered_reservations)

        # Recalcular metadatos de paginación
        if filtered_reservations:
            result["page_count"] = (
                1  # Con filtro del cliente, solo mostramos una página
            )
            result["page"] = 1
        else:
            result["page_count"] = 0
            result["page"] = 1

        logger.info(
            f"Filtro del cliente aplicado: {len(filtered_reservations)} reservas encontradas"
        )

        return result
