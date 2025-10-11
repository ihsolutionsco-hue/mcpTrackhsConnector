"""
Puerto (interfaz) para el cliente API
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ...domain.value_objects.request import PaginationParams, SearchParams


class ApiClientPort(ABC):
    """Puerto para el cliente API de Track HS"""

    @abstractmethod
    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición GET"""
        pass

    @abstractmethod
    async def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición POST"""
        pass

    @abstractmethod
    async def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición PUT"""
        pass

    @abstractmethod
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Realizar petición DELETE"""
        pass

    @abstractmethod
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Realizar petición HTTP genérica"""
        pass
