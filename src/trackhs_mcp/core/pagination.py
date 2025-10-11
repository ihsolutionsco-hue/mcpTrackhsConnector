"""
Utilidad de paginación robusta para Track HS MCP Connector
Maneja grandes conjuntos de datos con paginación eficiente y scroll de Elasticsearch
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

logger = logging.getLogger(__name__)


class PaginationMode(Enum):
    """Modos de paginación disponibles"""

    STANDARD = "standard"  # Paginación estándar con page/size
    SCROLL = "scroll"  # Scroll de Elasticsearch para grandes conjuntos
    CURSOR = "cursor"  # Paginación basada en cursor


@dataclass
class PaginationConfig:
    """Configuración de paginación"""

    mode: PaginationMode = PaginationMode.STANDARD
    max_page_size: int = 1000
    max_total_results: int = 10000
    scroll_timeout: str = "1m"
    enable_auto_scroll: bool = True
    preserve_order: bool = True


@dataclass
class PageInfo:
    """Información de una página"""

    page: int
    size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    scroll_id: Optional[str] = None


@dataclass
class PaginationResult:
    """Resultado de paginación"""

    data: List[Any]
    page_info: PageInfo
    links: Dict[str, str]
    metadata: Dict[str, Any]


class PaginationUtility:
    """Utilidad de paginación robusta"""

    def __init__(self, config: PaginationConfig = None):
        self.config = config or PaginationConfig()
        self._scroll_cache: Dict[str, Any] = {}

    def validate_pagination_params(self, page: int, size: int) -> Dict[str, Any]:
        """Valida parámetros de paginación"""
        if page < 1:
            page = 1

        if size < 1:
            size = 10
        elif size > self.config.max_page_size:
            size = self.config.max_page_size

        # Validar límite total de resultados
        total_requested = page * size
        if total_requested > self.config.max_total_results:
            raise ValueError(
                f"Total de resultados solicitados ({total_requested}) excede el límite máximo ({self.config.max_total_results})"
            )

        return {"page": page, "size": size, "offset": (page - 1) * size}

    def calculate_page_info(self, page: int, size: int, total_items: int) -> PageInfo:
        """Calcula información de la página"""
        total_pages = (total_items + size - 1) // size if total_items > 0 else 0

        return PageInfo(
            page=page,
            size=size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
            next_page=page + 1 if page < total_pages else None,
            previous_page=page - 1 if page > 1 else None,
        )

    def generate_links(
        self, base_url: str, page_info: PageInfo, query_params: Dict[str, Any]
    ) -> Dict[str, str]:
        """Genera enlaces de paginación"""
        links = {}

        def build_url(page_num: Optional[int]) -> str:
            if page_num is None:
                return ""
            params = query_params.copy()
            params["page"] = page_num
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            return f"{base_url}?{param_str}" if param_str else base_url

        links["sel"] = build_url(page_info.page)
        links["first"] = build_url(1)
        links["last"] = build_url(page_info.total_pages)

        if page_info.has_next:
            links["next"] = build_url(page_info.next_page)

        if page_info.has_previous:
            links["prev"] = build_url(page_info.previous_page)

        return links

    def process_scroll_response(self, response: Dict[str, Any]) -> PaginationResult:
        """Procesa respuesta de scroll de Elasticsearch"""
        data = response.get("_embedded", {}).get("reservations", [])
        page_info = PageInfo(
            page=1,  # Scroll no usa páginas tradicionales
            size=len(data),
            total_items=response.get("total_items", 0),
            total_pages=1,
            has_next="_links" in response and "next" in response["_links"],
            has_previous=False,
            scroll_id=response.get("_scroll_id"),
        )

        links = response.get("_links", {})

        return PaginationResult(
            data=data,
            page_info=page_info,
            links=links,
            metadata={"scroll_mode": True, "scroll_id": page_info.scroll_id},
        )

    def process_standard_response(
        self, response: Dict[str, Any], page: int, size: int
    ) -> PaginationResult:
        """Procesa respuesta de paginación estándar"""
        data = response.get("_embedded", {}).get("reservations", [])
        total_items = response.get("total_items", 0)

        page_info = self.calculate_page_info(page, size, total_items)
        links = response.get("_links", {})

        return PaginationResult(
            data=data,
            page_info=page_info,
            links=links,
            metadata={"scroll_mode": False, "standard_pagination": True},
        )

    async def paginate_async(
        self,
        api_client,
        endpoint: str,
        params: Dict[str, Any],
        mode: PaginationMode = None,
    ) -> AsyncIterator[PaginationResult]:
        """Iterador asíncrono para paginación"""
        mode = mode or self.config.mode

        if mode == PaginationMode.SCROLL:
            async for result in self._scroll_paginate(api_client, endpoint, params):
                yield result
        else:
            async for result in self._standard_paginate(api_client, endpoint, params):
                yield result

    async def _scroll_paginate(
        self, api_client, endpoint: str, params: Dict[str, Any]
    ) -> AsyncIterator[PaginationResult]:
        """Paginación con scroll de Elasticsearch"""
        scroll_params = params.copy()
        scroll_params["scroll"] = 1
        scroll_params["size"] = min(params.get("size", 100), self.config.max_page_size)

        try:
            # Primera página
            response = await api_client.get(endpoint, params=scroll_params)
            result = self.process_scroll_response(response)
            yield result

            # Páginas siguientes usando scroll
            scroll_id = result.metadata.get("scroll_id")
            while scroll_id and result.page_info.has_next:
                scroll_params["scroll"] = scroll_id
                response = await api_client.get(endpoint, params=scroll_params)
                result = self.process_scroll_response(response)
                scroll_id = result.metadata.get("scroll_id")

                if result.data:  # Solo yield si hay datos
                    yield result
                else:
                    break

        except Exception as e:
            logger.error(f"Error en scroll pagination: {str(e)}")
            raise

    async def _standard_paginate(
        self, api_client, endpoint: str, params: Dict[str, Any]
    ) -> AsyncIterator[PaginationResult]:
        """Paginación estándar"""
        page = params.get("page", 1)
        size = params.get("size", 10)

        # Validar parámetros
        validated = self.validate_pagination_params(page, size)
        params.update(validated)

        try:
            # Primera página
            response = await api_client.get(endpoint, params=params)
            result = self.process_standard_response(response, page, size)
            yield result

            # Páginas siguientes
            current_page = page
            while (
                result.page_info.has_next
                and current_page < self.config.max_total_results // size
            ):
                current_page += 1
                params["page"] = current_page

                response = await api_client.get(endpoint, params=params)
                result = self.process_standard_response(response, current_page, size)

                if result.data:  # Solo yield si hay datos
                    yield result
                else:
                    break

        except Exception as e:
            logger.error(f"Error en standard pagination: {str(e)}")
            raise

    def get_all_pages(self, results: List[PaginationResult]) -> List[Any]:
        """Obtiene todos los datos de múltiples páginas"""
        all_data = []
        for result in results:
            all_data.extend(result.data)
        return all_data

    def get_summary(self, results: List[PaginationResult]) -> Dict[str, Any]:
        """Obtiene resumen de los resultados paginados"""
        total_items = sum(len(result.data) for result in results)
        total_pages = len(results)

        return {
            "total_items": total_items,
            "total_pages": total_pages,
            "pages_processed": total_pages,
            "average_items_per_page": (
                total_items / total_pages if total_pages > 0 else 0
            ),
            "pagination_mode": results[0].metadata.get("scroll_mode", False)
            and "scroll"
            or "standard",
        }


# Funciones de conveniencia
async def paginate_reservations(
    api_client, params: Dict[str, Any], config: PaginationConfig = None
) -> List[Any]:
    """Función de conveniencia para paginar reservaciones"""
    pagination = PaginationUtility(config)
    results = []

    async for result in pagination.paginate_async(
        api_client, "/v2/pms/reservations", params
    ):
        results.append(result)

    return pagination.get_all_pages(results)


async def get_paginated_summary(
    api_client, params: Dict[str, Any], config: PaginationConfig = None
) -> Dict[str, Any]:
    """Obtiene resumen de resultados paginados"""
    pagination = PaginationUtility(config)
    results = []

    async for result in pagination.paginate_async(
        api_client, "/v2/pms/reservations", params
    ):
        results.append(result)

    return pagination.get_summary(results)
