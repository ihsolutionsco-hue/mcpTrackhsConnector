"""
Tests para sistema de cache y métricas de TrackHS MCP Server
Prueba funcionalidad de cache inteligente y métricas Prometheus
"""

import pytest
import time
from unittest.mock import Mock, patch

from src.trackhs_mcp.cache import (
    IntelligentCache,
    CacheStrategy,
    get_cache,
    cache_key,
    cached
)
from src.trackhs_mcp.metrics import (
    PrometheusMetrics,
    get_metrics,
    record_request_metrics,
    record_trackhs_api_metrics,
    record_cache_metrics,
    record_mcp_tool_metrics
)


class TestIntelligentCache:
    """Tests para IntelligentCache"""
    
    @pytest.fixture
    def cache(self):
        """Instancia de cache para testing"""
        return IntelligentCache(max_size=10, default_ttl=60)
    
    def test_basic_set_get(self, cache):
        """Test operaciones básicas de set/get"""
        # Arrange
        key = "test_key"
        value = {"data": "test_value"}
        
        # Act
        cache.set(key, value)
        result = cache.get(key)
        
        # Assert
        assert result == value
    
    def test_get_nonexistent_key(self, cache):
        """Test obtener clave que no existe"""
        # Act
        result = cache.get("nonexistent")
        
        # Assert
        assert result is None
    
    def test_ttl_expiration(self, cache):
        """Test expiración por TTL"""
        # Arrange
        key = "ttl_key"
        value = "test_value"
        cache.set(key, value, ttl=0.1)  # TTL muy corto
        
        # Act - Obtener antes de expirar
        result1 = cache.get(key)
        
        # Wait for expiration
        time.sleep(0.2)
        
        # Act - Obtener después de expirar
        result2 = cache.get(key)
        
        # Assert
        assert result1 == value
        assert result2 is None
    
    def test_lru_eviction(self, cache):
        """Test eviction por LRU"""
        # Arrange - Llenar cache
        for i in range(10):
            cache.set(f"key_{i}", f"value_{i}")
        
        # Act - Acceder a key_0 para hacerla más reciente
        cache.get("key_0")
        
        # Act - Agregar nueva clave (debería evictar key_1)
        cache.set("new_key", "new_value")
        
        # Assert
        assert cache.get("key_0") == "value_0"  # Debería estar
        assert cache.get("key_1") is None  # Debería estar evictada
        assert cache.get("new_key") == "new_value"  # Debería estar
    
    def test_invalidate_pattern(self, cache):
        """Test invalidación por patrón"""
        # Arrange
        cache.set("user:123", "user_data")
        cache.set("user:456", "user_data")
        cache.set("order:789", "order_data")
        cache.set("product:abc", "product_data")
        
        # Act - Invalidar solo usuarios
        invalidated = cache.invalidate_pattern("user:*")
        
        # Assert
        assert invalidated == 2
        assert cache.get("user:123") is None
        assert cache.get("user:456") is None
        assert cache.get("order:789") == "order_data"
        assert cache.get("product:abc") == "product_data"
    
    def test_metrics(self, cache):
        """Test métricas del cache"""
        # Arrange
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.get("key1")  # Hit
        cache.get("key3")  # Miss
        
        # Act
        metrics = cache.get_metrics()
        
        # Assert
        assert metrics["current_size"] == 2
        assert metrics["hits"] == 1
        assert metrics["misses"] == 1
        assert metrics["hit_rate_percentage"] == 50.0
    
    def test_clear_cache(self, cache):
        """Test limpiar cache"""
        # Arrange
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Act
        cache.clear()
        
        # Assert
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert cache.get_metrics()["current_size"] == 0


class TestCacheDecorator:
    """Tests para decorator de cache"""
    
    def test_cached_decorator(self):
        """Test decorator @cached"""
        call_count = 0
        
        @cached(ttl=60)
        def expensive_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # Act - Primera llamada
        result1 = expensive_function(5, y=15)
        
        # Act - Segunda llamada (debería usar cache)
        result2 = expensive_function(5, y=15)
        
        # Assert
        assert result1 == 20
        assert result2 == 20
        assert call_count == 1  # Solo se ejecutó una vez
    
    def test_cached_with_different_args(self):
        """Test decorator con argumentos diferentes"""
        call_count = 0
        
        @cached(ttl=60)
        def expensive_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # Act - Llamadas con argumentos diferentes
        result1 = expensive_function(5, y=15)
        result2 = expensive_function(5, y=20)  # Argumentos diferentes
        
        # Assert
        assert result1 == 20
        assert result2 == 25
        assert call_count == 2  # Se ejecutó dos veces


class TestPrometheusMetrics:
    """Tests para PrometheusMetrics"""
    
    @pytest.fixture
    def metrics(self):
        """Instancia de métricas para testing"""
        return PrometheusMetrics()
    
    def test_increment_counter(self, metrics):
        """Test incrementar contador"""
        # Act
        metrics.increment_counter("test_counter", {"label": "value"})
        metrics.increment_counter("test_counter", {"label": "value"}, value=5)
        
        # Assert
        assert metrics.metrics["test_counter"]["value"] == 6
    
    def test_set_gauge(self, metrics):
        """Test establecer gauge"""
        # Act
        metrics.set_gauge("test_gauge", 42.5, {"label": "value"})
        
        # Assert
        assert metrics.metrics["test_gauge"]["value"] == 42.5
    
    def test_observe_histogram(self, metrics):
        """Test observar histograma"""
        # Act
        metrics.observe_histogram("test_histogram", 1.5)
        metrics.observe_histogram("test_histogram", 2.0)
        metrics.observe_histogram("test_histogram", 0.5)
        
        # Assert
        assert len(metrics.metrics["test_histogram"]["values"]) == 3
        assert 1.5 in metrics.metrics["test_histogram"]["values"]
    
    def test_record_request(self, metrics):
        """Test registrar request"""
        # Act
        metrics.record_request("GET", 1.5, 200)
        metrics.record_request("POST", 2.0, 404)
        
        # Assert
        assert metrics.metrics["requests_total"]["value"] == 2
        assert metrics.metrics["errors_total"]["value"] == 1
        assert len(metrics.metrics["request_duration_seconds"]["values"]) == 2
    
    def test_record_trackhs_api_call(self, metrics):
        """Test registrar llamada a TrackHS API"""
        # Act
        metrics.record_trackhs_api_call("pms/reservations", 1.2, True)
        metrics.record_trackhs_api_call("pms/units", 0.8, False)
        
        # Assert
        assert metrics.metrics["trackhs_api_requests_total"]["value"] == 2
        assert metrics.metrics["trackhs_api_errors_total"]["value"] == 1
        assert len(metrics.metrics["trackhs_api_duration_seconds"]["values"]) == 2
    
    def test_record_cache_operation(self, metrics):
        """Test registrar operación de cache"""
        # Act
        metrics.record_cache_operation(True, "key1")
        metrics.record_cache_operation(False, "key2")
        metrics.record_cache_operation(True, "key3")
        
        # Assert
        assert metrics.metrics["cache_hits_total"]["value"] == 2
        assert metrics.metrics["cache_misses_total"]["value"] == 1
    
    def test_record_mcp_tool_call(self, metrics):
        """Test registrar llamada a herramienta MCP"""
        # Act
        metrics.record_mcp_tool_call("search_reservations", 1.5, True)
        metrics.record_mcp_tool_call("get_reservation", 0.8, False)
        
        # Assert
        assert metrics.metrics["mcp_tools_called_total"]["value"] == 2
        assert metrics.metrics["errors_total"]["value"] == 1
        assert len(metrics.metrics["mcp_tool_duration_seconds"]["values"]) == 2
    
    def test_update_cache_metrics(self, metrics):
        """Test actualizar métricas de cache"""
        # Act
        metrics.update_cache_metrics(size=100, hit_rate=85.5)
        
        # Assert
        assert metrics.metrics["cache_size"]["value"] == 100
        assert metrics.metrics["cache_hit_rate"]["value"] == 85.5
    
    def test_get_metrics_summary(self, metrics):
        """Test obtener resumen de métricas"""
        # Arrange
        metrics.record_request("GET", 1.0, 200)
        metrics.observe_histogram("test_histogram", 1.5)
        metrics.observe_histogram("test_histogram", 2.0)
        
        # Act
        summary = metrics.get_metrics_summary()
        
        # Assert
        assert "uptime_seconds" in summary
        assert "metrics" in summary
        assert "histogram_stats" in summary
        assert "timestamp" in summary
        assert summary["histogram_stats"]["test_histogram"]["count"] == 2
    
    def test_export_prometheus_format(self, metrics):
        """Test exportar formato Prometheus"""
        # Arrange
        metrics.increment_counter("test_counter", {"label": "value"})
        metrics.set_gauge("test_gauge", 42.5)
        metrics.observe_histogram("test_histogram", 1.5)
        
        # Act
        prometheus_output = metrics.export_prometheus_format()
        
        # Assert
        assert "# HELP test_counter" in prometheus_output
        assert "# TYPE test_counter counter" in prometheus_output
        assert 'test_counter{label="value"} 1' in prometheus_output
        assert "# HELP test_gauge" in prometheus_output
        assert "# TYPE test_gauge gauge" in prometheus_output
        assert 'test_gauge{label="value"} 42.5' in prometheus_output


class TestMetricsIntegration:
    """Tests de integración para métricas"""
    
    def test_global_metrics_instance(self):
        """Test instancia global de métricas"""
        # Act
        metrics1 = get_metrics()
        metrics2 = get_metrics()
        
        # Assert
        assert metrics1 is metrics2  # Debería ser la misma instancia
    
    def test_record_functions(self):
        """Test funciones de registro de métricas"""
        # Act
        record_request_metrics("GET", 1.5, 200)
        record_trackhs_api_metrics("pms/reservations", 1.2, True)
        record_cache_metrics(True, "test_key")
        record_mcp_tool_metrics("search_reservations", 1.0, True)
        
        # Assert
        metrics = get_metrics()
        assert metrics.metrics["requests_total"]["value"] == 1
        assert metrics.metrics["trackhs_api_requests_total"]["value"] == 1
        assert metrics.metrics["cache_hits_total"]["value"] == 1
        assert metrics.metrics["mcp_tools_called_total"]["value"] == 1


class TestCacheKeyGeneration:
    """Tests para generación de claves de cache"""
    
    def test_cache_key_with_args(self):
        """Test generar clave con argumentos posicionales"""
        # Act
        key = cache_key("test", 123, True)
        
        # Assert
        assert key == "test:123:True"
    
    def test_cache_key_with_kwargs(self):
        """Test generar clave con argumentos con nombre"""
        # Act
        key = cache_key("test", page=1, size=10, status="active")
        
        # Assert
        assert "test" in key
        assert "page:1" in key
        assert "size:10" in key
        assert 'status:"active"' in key
    
    def test_cache_key_with_mixed_args(self):
        """Test generar clave con argumentos mixtos"""
        # Act
        key = cache_key("search", "reservations", page=1, filters={"status": "confirmed"})
        
        # Assert
        assert "search" in key
        assert "reservations" in key
        assert "page:1" in key
        assert "filters:" in key


class TestCacheAndMetricsIntegration:
    """Tests de integración entre cache y métricas"""
    
    def test_cache_metrics_integration(self):
        """Test integración de métricas con cache"""
        # Arrange
        cache = IntelligentCache(max_size=5, default_ttl=60)
        metrics = get_metrics()
        
        # Act - Operaciones de cache
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.get("key1")  # Hit
        cache.get("key3")  # Miss
        
        # Act - Actualizar métricas de cache
        cache_metrics = cache.get_metrics()
        metrics.update_cache_metrics(
            size=cache_metrics["current_size"],
            hit_rate=cache_metrics["hit_rate_percentage"]
        )
        
        # Assert
        assert metrics.metrics["cache_size"]["value"] == 2
        assert metrics.metrics["cache_hit_rate"]["value"] == 50.0
    
    def test_performance_metrics(self):
        """Test métricas de rendimiento"""
        # Arrange
        cache = IntelligentCache(max_size=100, default_ttl=60)
        metrics = get_metrics()
        
        # Act - Simular operaciones de alto volumen
        start_time = time.time()
        
        for i in range(100):
            cache.set(f"key_{i}", f"value_{i}")
            cache.get(f"key_{i}")
        
        duration = time.time() - start_time
        
        # Act - Registrar métricas de rendimiento
        metrics.record_request("GET", duration, 200)
        
        # Assert
        assert metrics.metrics["requests_total"]["value"] == 1
        assert metrics.metrics["request_duration_seconds"]["values"][0] == duration
        assert cache.get_metrics()["current_size"] == 100
