"""
Repository base para TrackHS MCP Server
Define la interfaz común para todos los repositories
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..cache import IntelligentCache, get_cache, cache_key
from ..exceptions import APIError, AuthenticationError, ConnectionError, NotFoundError

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    """
    Repository base que define la interfaz común para todos los repositories.
    
    Proporciona funcionalidad común como:
    - Manejo de errores HTTP
    - Logging estructurado
    - Validación de respuestas
    - Cache básico
    """
    
    def __init__(self, api_client, cache_ttl: int = 300):
        """
        Inicializar repository base.
        
        Args:
            api_client: Cliente HTTP para TrackHS API
            cache_ttl: TTL del cache en segundos
        """
        self.api_client = api_client
        self.cache_ttl = cache_ttl
        self.cache = get_cache()  # Usar cache inteligente global
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Obtener valor del cache si no ha expirado"""
        return self.cache.get(key)
    
    def _set_cached(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Guardar valor en cache"""
        effective_ttl = ttl if ttl is not None else self.cache_ttl
        self.cache.set(key, value, ttl=effective_ttl)
        logger.debug(f"Cache set for key: {key} (TTL: {effective_ttl}s)")
    
    def _clear_cache(self, key: Optional[str] = None) -> None:
        """Limpiar cache"""
        if key:
            self.cache.delete(key)
            logger.debug(f"Cache cleared for key: {key}")
        else:
            self.cache.clear()
            logger.debug("All cache cleared")
    
    def _invalidate_pattern(self, pattern: str) -> int:
        """Invalidar entradas del cache por patrón"""
        count = self.cache.invalidate_pattern(pattern)
        logger.debug(f"Cache invalidated {count} entries matching pattern: {pattern}")
        return count
    
    def _handle_api_error(self, error: Exception, operation: str) -> None:
        """
        Manejar errores de API de manera consistente.
        
        Args:
            error: Excepción capturada
            operation: Nombre de la operación que falló
        """
        logger.error(f"Error in {operation}: {type(error).__name__}: {str(error)}")
        
        if isinstance(error, (APIError, AuthenticationError, ConnectionError, NotFoundError)):
            # Re-lanzar excepciones específicas de TrackHS
            raise
        else:
            # Convertir excepciones genéricas a APIError
            raise APIError(f"Error en {operation}: {str(error)}")
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Dict[str, Any]:
        """
        Obtener entidad por ID.
        
        Args:
            entity_id: ID de la entidad
            
        Returns:
            Datos de la entidad
            
        Raises:
            NotFoundError: Si la entidad no existe
            APIError: Si hay error de API
        """
        pass
    
    @abstractmethod
    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Buscar entidades con filtros.
        
        Args:
            filters: Filtros de búsqueda
            
        Returns:
            Resultados de búsqueda con metadatos de paginación
        """
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verificar salud del repository.
        
        Returns:
            Estado de salud del repository
        """
        try:
            # Intentar una operación simple para verificar conectividad
            self._test_connection()
            cache_metrics = self.cache.get_metrics()
            return {
                "status": "healthy",
                "cache_metrics": cache_metrics,
                "cache_ttl": self.cache_ttl
            }
        except Exception as e:
            cache_metrics = self.cache.get_metrics()
            return {
                "status": "unhealthy",
                "error": str(e),
                "cache_metrics": cache_metrics,
                "cache_ttl": self.cache_ttl
            }
    
    @abstractmethod
    def _test_connection(self) -> None:
        """
        Probar conexión con la API.
        
        Raises:
            APIError: Si no se puede conectar
        """
        pass
