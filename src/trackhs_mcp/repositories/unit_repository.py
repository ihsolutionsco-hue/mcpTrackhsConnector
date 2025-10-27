"""
Repository para unidades de TrackHS
Maneja todas las operaciones relacionadas con unidades
"""

import logging
from typing import Any, Dict, List, Optional

from ..exceptions import APIError, NotFoundError
from .base import BaseRepository

logger = logging.getLogger(__name__)


class UnitRepository(BaseRepository):
    """Repository para operaciones de unidades"""

    def __init__(self, api_client, cache_ttl: int = 300):
        super().__init__(api_client, cache_ttl)
        self.base_endpoint = "api/pms/units"
        self.amenities_endpoint = "api/pms/units/amenities"

    def get_by_id(self, unit_id: int) -> Dict[str, Any]:
        """
        Obtener unidad por ID.

        Args:
            unit_id: ID de la unidad

        Returns:
            Datos de la unidad

        Raises:
            NotFoundError: Si la unidad no existe
            APIError: Si hay error de API
        """
        cache_key = f"unit_{unit_id}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Fetching unit {unit_id} from API")
            result = self.api_client.get(f"{self.base_endpoint}/{unit_id}")

            # Guardar en cache
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"get_unit_{unit_id}")

    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buscar unidades con filtros.

        Args:
            filters: Filtros de búsqueda (page, size, search, bedrooms, bathrooms, etc.)

        Returns:
            Resultados de búsqueda con metadatos de paginación
        """
        # Crear clave de cache basada en filtros
        cache_key = f"units_search_{hash(frozenset(filters.items()))}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Searching units with filters: {filters}")
            result = self.api_client.get(self.base_endpoint, params=filters)

            # Guardar en cache
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"search_units_{filters}")

    def search_amenities(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buscar amenidades disponibles.

        Args:
            filters: Filtros de búsqueda (page, size, search)

        Returns:
            Resultados de búsqueda de amenidades
        """
        cache_key = f"amenities_search_{hash(frozenset(filters.items()))}"

        # Intentar obtener del cache
        cached_result = self._get_cached(cache_key)
        if cached_result:
            return cached_result

        try:
            logger.info(f"Searching amenities with filters: {filters}")
            result = self.api_client.get(self.amenities_endpoint, params=filters)

            # Guardar en cache (TTL más largo para amenidades)
            self._set_cached(cache_key, result)

            return result

        except Exception as e:
            self._handle_api_error(e, f"search_amenities_{filters}")

    def search_by_capacity(
        self, bedrooms: Optional[int] = None, bathrooms: Optional[int] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Buscar unidades por capacidad.

        Args:
            bedrooms: Número de dormitorios
            bathrooms: Número de baños
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {}
        if bedrooms is not None:
            filters["bedrooms"] = bedrooms
        if bathrooms is not None:
            filters["bathrooms"] = bathrooms
        filters.update(kwargs)

        return self.search(filters)

    def search_by_availability(
        self, is_active: bool = True, is_bookable: bool = True, **kwargs
    ) -> Dict[str, Any]:
        """
        Buscar unidades por disponibilidad.

        Args:
            is_active: Si la unidad está activa
            is_bookable: Si la unidad está disponible para reservar
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {
            "is_active": 1 if is_active else 0,
            "is_bookable": 1 if is_bookable else 0,
            **kwargs,
        }
        return self.search(filters)

    def search_by_text(self, search_term: str, **kwargs) -> Dict[str, Any]:
        """
        Buscar unidades por término de texto.

        Args:
            search_term: Término de búsqueda (nombre, descripción, código)
            **kwargs: Otros filtros opcionales

        Returns:
            Resultados de búsqueda
        """
        filters = {"search": search_term, **kwargs}
        return self.search(filters)

    def get_unit_amenities(self, unit_id: int) -> List[Dict[str, Any]]:
        """
        Obtener amenidades de una unidad específica.

        Args:
            unit_id: ID de la unidad

        Returns:
            Lista de amenidades de la unidad
        """
        unit = self.get_by_id(unit_id)
        return unit.get("amenities", [])

    def get_available_amenities(self) -> List[Dict[str, Any]]:
        """
        Obtener todas las amenidades disponibles en el sistema.

        Returns:
            Lista de amenidades disponibles
        """
        result = self.search_amenities({"page": 1, "size": 1000})  # Obtener todas
        return result.get("_embedded", {}).get("amenities", [])

    def _test_connection(self) -> None:
        """Probar conexión con la API de unidades"""
        try:
            # Hacer una búsqueda simple para probar conectividad
            self.api_client.get(self.base_endpoint, {"page": 1, "size": 1})
        except Exception as e:
            raise APIError(f"Error conectando con API de unidades: {str(e)}")

    def get_unit_summary(self, unit_id: int) -> Dict[str, Any]:
        """
        Obtener resumen de una unidad (datos básicos).

        Args:
            unit_id: ID de la unidad

        Returns:
            Resumen de la unidad
        """
        unit = self.get_by_id(unit_id)

        # Extraer solo datos básicos para el resumen
        summary = {
            "id": unit.get("id"),
            "name": unit.get("name"),
            "code": unit.get("code"),
            "bedrooms": unit.get("bedrooms"),
            "bathrooms": unit.get("bathrooms"),
            "max_occupancy": unit.get("max_occupancy"),
            "area": unit.get("area"),
            "address": unit.get("address"),
            "is_active": unit.get("is_active"),
            "is_bookable": unit.get("is_bookable"),
            "amenities_count": len(unit.get("amenities", [])),
        }

        return summary
