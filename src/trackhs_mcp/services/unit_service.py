"""
Servicio de Unidades para TrackHS.
Contiene la lógica de negocio para unidades de alojamiento.
"""

import logging
from typing import Any, Dict, Optional

from ..exceptions import TrackHSError, ValidationError
from ..repositories import UnitRepository

logger = logging.getLogger(__name__)


class UnitService:
    """
    Servicio para gestión de unidades de alojamiento.

    Separa la lógica de negocio de las herramientas MCP,
    permitiendo testing y reutilización.
    """

    def __init__(self, unit_repo: UnitRepository):
        self.unit_repo = unit_repo

    def search_units(
        self,
        page: int = 1,
        size: int = 10,
        search: Optional[str] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        is_active: Optional[int] = None,
        is_bookable: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Buscar unidades de alojamiento.

        Args:
            page: Número de página (1-based)
            size: Tamaño de página (1-25)
            search: Búsqueda de texto
            bedrooms: Número de dormitorios
            bathrooms: Número de baños
            is_active: Filtrar por activas (1) o inactivas (0)
            is_bookable: Filtrar por disponibles (1) o no (0)

        Returns:
            Resultado de la búsqueda

        Raises:
            ValidationError: Si los parámetros no son válidos
            TrackHSError: Si hay error en la API
        """
        # Validaciones de negocio
        if page < 1:
            raise ValidationError("El número de página debe ser mayor a 0")

        if size < 1 or size > 25:
            raise ValidationError("El tamaño de página debe estar entre 1 y 25")

        if bedrooms is not None and bedrooms < 0:
            raise ValidationError("El número de dormitorios no puede ser negativo")

        if bathrooms is not None and bathrooms < 0:
            raise ValidationError("El número de baños no puede ser negativo")

        if is_active is not None and is_active not in [0, 1]:
            raise ValidationError("is_active debe ser 0 o 1")

        if is_bookable is not None and is_bookable not in [0, 1]:
            raise ValidationError("is_bookable debe ser 0 o 1")

        logger.info(f"Buscando unidades: página {page}, tamaño {size}")

        try:
            # Construir parámetros
            params = {"page": page, "size": size}
            if search:
                params["search"] = search
            if bedrooms is not None:
                params["bedrooms"] = bedrooms
            if bathrooms is not None:
                params["bathrooms"] = bathrooms
            if is_active is not None:
                params["is_active"] = is_active
            if is_bookable is not None:
                params["is_bookable"] = is_bookable

            result = self.unit_repo.search(params)

            logger.info(
                f"Búsqueda de unidades completada. Encontradas: {result.get('total_items', 0)}"
            )
            return result

        except Exception as e:
            logger.error(f"Error buscando unidades: {str(e)}")
            raise TrackHSError(f"Error buscando unidades: {str(e)}")

    def get_unit_by_id(self, unit_id: int) -> Dict[str, Any]:
        """
        Obtener una unidad por ID.

        Args:
            unit_id: ID de la unidad

        Returns:
            Datos de la unidad

        Raises:
            ValidationError: Si el ID no es válido
            TrackHSError: Si hay error en la API
        """
        if unit_id <= 0:
            raise ValidationError("El ID de unidad debe ser mayor a 0")

        logger.info(f"Obteniendo unidad {unit_id}")

        try:
            result = self.unit_repo.get_by_id(unit_id)
            logger.info(f"Unidad {unit_id} obtenida exitosamente")
            return result

        except Exception as e:
            logger.error(f"Error obteniendo unidad {unit_id}: {str(e)}")
            raise TrackHSError(f"Error obteniendo unidad {unit_id}: {str(e)}")

    def search_amenities(
        self, page: int = 1, size: int = 10, search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Buscar amenidades disponibles.

        Args:
            page: Número de página
            size: Tamaño de página
            search: Búsqueda de texto

        Returns:
            Resultado de la búsqueda de amenidades
        """
        # Validaciones de negocio
        if page < 1:
            raise ValidationError("El número de página debe ser mayor a 0")

        if size < 1 or size > 100:
            raise ValidationError("El tamaño de página debe estar entre 1 y 100")

        logger.info(f"Buscando amenidades: página {page}, tamaño {size}")

        try:
            params = {"page": page, "size": size}
            if search:
                params["search"] = search

            result = self.unit_repo.search_amenities(params)

            logger.info(
                f"Búsqueda de amenidades completada. Encontradas: {result.get('total_items', 0)}"
            )
            return result

        except Exception as e:
            logger.error(f"Error buscando amenidades: {str(e)}")
            raise TrackHSError(f"Error buscando amenidades: {str(e)}")
