"""
Servicio de amenidades para TrackHS MCP.
Implementa la lógica de negocio separada de la función MCP.
"""

import logging
from typing import Any, Dict, Optional

from fastmcp.exceptions import ToolError

from .amenities_error_handler import AmenitiesErrorHandler
from .amenities_models import AmenitiesSearchParams

logger = logging.getLogger(__name__)


class AmenitiesService:
    """
    Servicio de amenidades que encapsula la lógica de negocio.

    Separa la lógica de búsqueda de amenidades de la función MCP,
    facilitando el testing y mantenimiento del código.
    """

    def __init__(self, api_client):
        """
        Inicializar servicio de amenidades.

        Args:
            api_client: Cliente API de TrackHS
        """
        self.api_client = api_client
        self.error_handler = AmenitiesErrorHandler("amenities_service")

    def search_amenities(
        self,
        page: int = 1,
        size: int = 10,
        sortColumn: Optional[str] = None,
        sortDirection: Optional[str] = None,
        search: Optional[str] = None,
        groupId: Optional[int] = None,
        isPublic: Optional[int] = None,
        publicSearchable: Optional[int] = None,
        isFilterable: Optional[int] = None,
        homeawayType: Optional[str] = None,
        airbnbType: Optional[str] = None,
        tripadvisorType: Optional[str] = None,
        marriottType: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Buscar amenidades en TrackHS.

        Args:
            page: Número de página (1-based)
            size: Tamaño de página
            sortColumn: Columna para ordenar
            sortDirection: Dirección de ordenamiento
            search: Término de búsqueda
            groupId: ID del grupo
            isPublic: Filtro público/privado
            publicSearchable: Filtro buscable públicamente
            isFilterable: Filtro filtrable
            homeawayType: Tipo de HomeAway
            airbnbType: Tipo de Airbnb
            tripadvisorType: Tipo de TripAdvisor
            marriottType: Tipo de Marriott

        Returns:
            Respuesta de la API con amenidades encontradas

        Raises:
            ToolError: Si hay error de validación, autenticación, autorización o conexión
        """
        if self.api_client is None:
            raise ToolError(
                "Cliente API no disponible. Verifique las credenciales de TrackHS."
            )

        # Validar parámetros usando Pydantic
        try:
            params = AmenitiesSearchParams(
                page=page,
                size=size,
                sortColumn=sortColumn,
                sortDirection=sortDirection,
                search=search,
                groupId=groupId,
                isPublic=isPublic,
                publicSearchable=publicSearchable,
                isFilterable=isFilterable,
                homeawayType=homeawayType,
                airbnbType=airbnbType,
                tripadvisorType=tripadvisorType,
                marriottType=marriottType,
            )
        except Exception as e:
            raise self.error_handler.handle_error(
                e, {"page": page, "size": size, "search": search, "groupId": groupId}
            )

        logger.info(f"Buscando amenidades: página {params.page}, tamaño {params.size}")

        try:
            # Construir parámetros para la API usando el modelo validado
            api_params = params.to_api_params()

            # Realizar llamada a la API
            result = self.api_client.get("api/pms/units/amenities", api_params)

            # Validar respuesta
            if not isinstance(result, dict):
                raise ValueError("Respuesta inesperada de la API de TrackHS")

            total_items = result.get("total_items", 0)
            logger.info(f"Encontradas {total_items} amenidades")

            return result

        except ToolError:
            # Re-lanzar ToolError tal como están
            raise
        except Exception as e:
            # Manejar otros errores con el manejador específico
            raise self.error_handler.handle_error(e, params.to_api_params())

    def get_amenities_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtener resumen de los resultados de búsqueda.

        Args:
            result: Resultado de la búsqueda de amenidades

        Returns:
            Resumen estructurado de los resultados
        """
        if not isinstance(result, dict):
            return {"error": "Resultado inválido"}

        total_items = result.get("total_items", 0)
        page = result.get("page", 0)
        page_size = result.get("page_size", 0)

        amenities = []
        if "_embedded" in result and "amenities" in result["_embedded"]:
            amenities = result["_embedded"]["amenities"]

        return {
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
            "amenities_count": len(amenities),
            "has_amenities": len(amenities) > 0,
            "amenities": amenities[:5] if amenities else [],  # Primeros 5 para preview
        }

    def validate_search_parameters(
        self, page: int = 1, size: int = 10, **kwargs
    ) -> AmenitiesSearchParams:
        """
        Validar parámetros de búsqueda sin ejecutar la búsqueda.

        Args:
            page: Número de página
            size: Tamaño de página
            **kwargs: Otros parámetros de búsqueda

        Returns:
            Parámetros validados

        Raises:
            ToolError: Si hay error de validación
        """
        try:
            return AmenitiesSearchParams(page=page, size=size, **kwargs)
        except Exception as e:
            raise self.error_handler.handle_error(
                e, {"page": page, "size": size, **kwargs}
            )

    def get_available_sort_columns(self) -> list:
        """
        Obtener columnas disponibles para ordenamiento.

        Returns:
            Lista de columnas válidas para ordenamiento
        """
        return [
            "id",
            "order",
            "isPublic",
            "publicSearchable",
            "isFilterable",
            "createdAt",
        ]

    def get_available_sort_directions(self) -> list:
        """
        Obtener direcciones disponibles para ordenamiento.

        Returns:
            Lista de direcciones válidas para ordenamiento
        """
        return ["asc", "desc"]

    def get_ota_platforms(self) -> list:
        """
        Obtener plataformas OTA soportadas.

        Returns:
            Lista de plataformas OTA soportadas
        """
        return ["homeawayType", "airbnbType", "tripadvisorType", "marriottType"]
