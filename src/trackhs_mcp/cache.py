"""
Sistema de cache inteligente para TrackHS MCP Server
Implementa cache con TTL, invalidación y métricas
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Estrategias de cache disponibles"""
    LRU = "lru"  # Least Recently Used
    TTL = "ttl"  # Time To Live
    BOTH = "both"  # LRU + TTL


@dataclass
class CacheEntry:
    """Entrada de cache con metadatos"""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    ttl: Optional[float] = None
    access_count: int = 0
    
    def is_expired(self) -> bool:
        """Verificar si la entrada ha expirado"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def touch(self) -> None:
        """Actualizar timestamp de último acceso"""
        self.last_accessed = time.time()
        self.access_count += 1


class IntelligentCache:
    """
    Sistema de cache inteligente con múltiples estrategias.
    
    Características:
    - TTL (Time To Live) por entrada
    - LRU (Least Recently Used) eviction
    - Métricas de rendimiento
    - Invalidación por patrones
    - Serialización JSON para persistencia
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: Optional[float] = None,
        strategy: CacheStrategy = CacheStrategy.BOTH
    ):
        """
        Inicializar cache inteligente.
        
        Args:
            max_size: Tamaño máximo del cache
            default_ttl: TTL por defecto en segundos
            strategy: Estrategia de eviction
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.strategy = strategy
        
        # Storage
        self._cache: Dict[str, CacheEntry] = {}
        
        # Métricas
        self.metrics = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "invalidations": 0,
            "total_requests": 0,
        }
        
        # Configuración de limpieza
        self._last_cleanup = time.time()
        self._cleanup_interval = 60  # Limpiar cada 60 segundos
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtener valor del cache.
        
        Args:
            key: Clave del cache
            
        Returns:
            Valor si existe y no ha expirado, None en caso contrario
        """
        self.metrics["total_requests"] += 1
        
        if key not in self._cache:
            self.metrics["misses"] += 1
            return None
        
        entry = self._cache[key]
        
        # Verificar si ha expirado
        if entry.is_expired():
            self._remove_entry(key)
            self.metrics["misses"] += 1
            return None
        
        # Actualizar acceso
        entry.touch()
        self.metrics["hits"] += 1
        
        # Limpieza periódica
        self._periodic_cleanup()
        
        return entry.value
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[float] = None,
        tags: Optional[List[str]] = None
    ) -> None:
        """
        Guardar valor en cache.
        
        Args:
            key: Clave del cache
            value: Valor a guardar
            ttl: TTL específico para esta entrada
            tags: Tags para invalidación por patrones
        """
        # Usar TTL por defecto si no se especifica
        effective_ttl = ttl if ttl is not None else self.default_ttl
        
        # Crear entrada
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            last_accessed=time.time(),
            ttl=effective_ttl,
            access_count=1
        )
        
        # Verificar si necesitamos eviction
        if len(self._cache) >= self.max_size and key not in self._cache:
            self._evict_entry()
        
        # Guardar entrada
        self._cache[key] = entry
        
        # Agregar tags si se proporcionan
        if tags:
            for tag in tags:
                self._add_tag(key, tag)
    
    def delete(self, key: str) -> bool:
        """
        Eliminar entrada del cache.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        if key in self._cache:
            self._remove_entry(key)
            return True
        return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidar entradas que coincidan con un patrón.
        
        Args:
            pattern: Patrón de búsqueda (soporta * y ?)
            
        Returns:
            Número de entradas invalidadas
        """
        import fnmatch
        
        keys_to_remove = []
        for key in self._cache.keys():
            if fnmatch.fnmatch(key, pattern):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            self._remove_entry(key)
        
        self.metrics["invalidations"] += len(keys_to_remove)
        return len(keys_to_remove)
    
    def invalidate_tags(self, tags: List[str]) -> int:
        """
        Invalidar entradas por tags.
        
        Args:
            tags: Lista de tags a invalidar
            
        Returns:
            Número de entradas invalidadas
        """
        # Esta funcionalidad requeriría un sistema de tags más complejo
        # Por simplicidad, implementamos invalidación por patrón
        count = 0
        for tag in tags:
            count += self.invalidate_pattern(f"*{tag}*")
        return count
    
    def clear(self) -> None:
        """Limpiar todo el cache"""
        self._cache.clear()
        self.metrics["invalidations"] += len(self._cache)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtener métricas del cache.
        
        Returns:
            Diccionario con métricas
        """
        hit_rate = (
            self.metrics["hits"] / self.metrics["total_requests"] * 100
            if self.metrics["total_requests"] > 0 else 0
        )
        
        return {
            **self.metrics,
            "hit_rate_percentage": round(hit_rate, 2),
            "current_size": len(self._cache),
            "max_size": self.max_size,
            "utilization_percentage": round(len(self._cache) / self.max_size * 100, 2),
        }
    
    def _remove_entry(self, key: str) -> None:
        """Eliminar entrada del cache"""
        if key in self._cache:
            del self._cache[key]
    
    def _evict_entry(self) -> None:
        """Eliminar entrada según la estrategia configurada"""
        if not self._cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            # Encontrar entrada menos recientemente usada
            lru_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].last_accessed
            )
            self._remove_entry(lru_key)
        elif self.strategy == CacheStrategy.TTL:
            # Encontrar entrada más próxima a expirar
            ttl_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].created_at + (self._cache[k].ttl or float('inf'))
            )
            self._remove_entry(ttl_key)
        else:  # BOTH
            # Combinar LRU y TTL
            current_time = time.time()
            candidates = []
            
            for key, entry in self._cache.items():
                # Calcular score combinado
                age = current_time - entry.created_at
                last_access = current_time - entry.last_accessed
                
                # Score más alto = más candidato para eviction
                score = last_access + (age * 0.1)  # Ponderar edad ligeramente
                candidates.append((key, score))
            
            if candidates:
                evict_key = max(candidates, key=lambda x: x[1])[0]
                self._remove_entry(evict_key)
        
        self.metrics["evictions"] += 1
    
    def _periodic_cleanup(self) -> None:
        """Limpieza periódica de entradas expiradas"""
        current_time = time.time()
        
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        expired_keys = []
        for key, entry in self._cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_entry(key)
        
        self._last_cleanup = current_time
        
        if expired_keys:
            logger.debug(f"Cache cleanup: removed {len(expired_keys)} expired entries")
    
    def _add_tag(self, key: str, tag: str) -> None:
        """Agregar tag a una entrada (implementación simplificada)"""
        # En una implementación más compleja, mantendríamos un índice de tags
        # Por simplicidad, usamos la clave con prefijo de tag
        tag_key = f"tag:{tag}:{key}"
        self._cache[tag_key] = CacheEntry(
            key=tag_key,
            value=key,
            created_at=time.time(),
            last_accessed=time.time(),
            ttl=self.default_ttl
        )


# Instancia global de cache
_global_cache: Optional[IntelligentCache] = None


def get_cache() -> IntelligentCache:
    """Obtener instancia global de cache"""
    global _global_cache
    if _global_cache is None:
        _global_cache = IntelligentCache(
            max_size=1000,
            default_ttl=300,  # 5 minutos por defecto
            strategy=CacheStrategy.BOTH
        )
    return _global_cache


def cache_key(*args, **kwargs) -> str:
    """
    Generar clave de cache a partir de argumentos.
    
    Args:
        *args: Argumentos posicionales
        **kwargs: Argumentos con nombre
        
    Returns:
        Clave de cache generada
    """
    # Crear representación serializable
    key_parts = []
    
    for arg in args:
        if isinstance(arg, (str, int, float, bool)):
            key_parts.append(str(arg))
        else:
            key_parts.append(json.dumps(arg, sort_keys=True))
    
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (str, int, float, bool)):
            key_parts.append(f"{k}:{v}")
        else:
            key_parts.append(f"{k}:{json.dumps(v, sort_keys=True)}")
    
    return ":".join(key_parts)


def cached(ttl: Optional[float] = None, tags: Optional[List[str]] = None):
    """
    Decorator para cachear resultados de funciones.
    
    Args:
        ttl: TTL específico para esta función
        tags: Tags para invalidación
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generar clave de cache
            cache_key_str = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Intentar obtener del cache
            cache = get_cache()
            result = cache.get(cache_key_str)
            
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result
            
            # Ejecutar función y guardar resultado
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            cache.set(cache_key_str, result, ttl=ttl, tags=tags)
            
            return result
        
        return wrapper
    return decorator
