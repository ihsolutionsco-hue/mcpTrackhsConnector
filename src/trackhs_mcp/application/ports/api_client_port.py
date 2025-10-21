"""
Puerto (interfaz) para el cliente API
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

# PaginationParams, SearchParams imports removed - not used


class ApiClientPort(ABC):
    """Puerto para el cliente API de Track HS"""

    @abstractmethod
    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición GET"""

    @abstractmethod
    async def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición POST"""

    @abstractmethod
    async def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Realizar petición PUT"""

    @abstractmethod
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Realizar petición DELETE"""

    @abstractmethod
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Realizar petición HTTP genérica"""
