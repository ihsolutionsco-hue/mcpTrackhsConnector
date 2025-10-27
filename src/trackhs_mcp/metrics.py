"""
Sistema de métricas avanzadas para TrackHS MCP Server
Implementa métricas Prometheus y métricas personalizadas
"""

import logging
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Tipos de métricas disponibles"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class MetricData:
    """Datos de una métrica"""
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: float
    metric_type: MetricType


class PrometheusMetrics:
    """
    Sistema de métricas compatible con Prometheus.

    Implementa métricas estándar de Prometheus:
    - Counters: Valores que solo aumentan
    - Gauges: Valores que pueden subir y bajar
    - Histograms: Distribución de valores
    - Summaries: Estadísticas de valores
    """

    def __init__(self):
        """Inicializar sistema de métricas"""
        self.metrics: Dict[str, Any] = {}
        self.start_time = time.time()

        # Métricas del sistema
        self._init_system_metrics()

        # Métricas de la aplicación
        self._init_app_metrics()

    def _init_system_metrics(self):
        """Inicializar métricas del sistema"""
        # Contador de requests totales
        self.metrics["requests_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total number of requests"
        }

        # Contador de requests por método
        self.metrics["requests_by_method"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Requests by HTTP method"
        }

        # Contador de errores
        self.metrics["errors_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total number of errors"
        }

        # Gauge de requests activos
        self.metrics["active_requests"] = {
            "type": MetricType.GAUGE,
            "value": 0,
            "labels": {},
            "description": "Number of active requests"
        }

        # Histograma de duración de requests
        self.metrics["request_duration_seconds"] = {
            "type": MetricType.HISTOGRAM,
            "buckets": [0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
            "values": [],
            "labels": {},
            "description": "Request duration in seconds"
        }

    def _init_app_metrics(self):
        """Inicializar métricas de la aplicación"""
        # Métricas de TrackHS API
        self.metrics["trackhs_api_requests_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total TrackHS API requests"
        }

        self.metrics["trackhs_api_errors_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total TrackHS API errors"
        }

        self.metrics["trackhs_api_duration_seconds"] = {
            "type": MetricType.HISTOGRAM,
            "buckets": [0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
            "values": [],
            "labels": {},
            "description": "TrackHS API request duration"
        }

        # Métricas de cache
        self.metrics["cache_hits_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total cache hits"
        }

        self.metrics["cache_misses_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total cache misses"
        }

        self.metrics["cache_size"] = {
            "type": MetricType.GAUGE,
            "value": 0,
            "labels": {},
            "description": "Current cache size"
        }

        # Métricas de herramientas MCP
        self.metrics["mcp_tools_called_total"] = {
            "type": MetricType.COUNTER,
            "value": 0,
            "labels": {},
            "description": "Total MCP tool calls"
        }

        self.metrics["mcp_tool_duration_seconds"] = {
            "type": MetricType.HISTOGRAM,
            "buckets": [0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
            "values": [],
            "labels": {},
            "description": "MCP tool execution duration"
        }

    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None, value: float = 1.0):
        """Incrementar contador"""
        if name not in self.metrics:
            self.metrics[name] = {
                "type": MetricType.COUNTER,
                "value": 0,
                "labels": labels or {},
                "description": f"Counter metric: {name}"
            }

        self.metrics[name]["value"] += value
        if labels:
            self.metrics[name]["labels"].update(labels)

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Establecer valor de gauge"""
        if name not in self.metrics:
            self.metrics[name] = {
                "type": MetricType.GAUGE,
                "value": 0,
                "labels": labels or {},
                "description": f"Gauge metric: {name}"
            }

        self.metrics[name]["value"] = value
        if labels:
            self.metrics[name]["labels"].update(labels)

    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observar valor en histograma"""
        if name not in self.metrics:
            self.metrics[name] = {
                "type": MetricType.HISTOGRAM,
                "buckets": [0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
                "values": [],
                "labels": labels or {},
                "description": f"Histogram metric: {name}"
            }

        self.metrics[name]["values"].append(value)
        if labels:
            self.metrics[name]["labels"].update(labels)

    def record_request(self, method: str, duration: float, status_code: int = 200):
        """Registrar request HTTP"""
        self.increment_counter("requests_total")
        self.increment_counter("requests_by_method", {"method": method})

        if status_code >= 400:
            self.increment_counter("errors_total", {"status_code": str(status_code)})

        self.observe_histogram("request_duration_seconds", duration)

    def record_trackhs_api_call(self, endpoint: str, duration: float, success: bool = True):
        """Registrar llamada a TrackHS API"""
        self.increment_counter("trackhs_api_requests_total", {"endpoint": endpoint})

        if not success:
            self.increment_counter("trackhs_api_errors_total", {"endpoint": endpoint})

        self.observe_histogram("trackhs_api_duration_seconds", duration)

    def record_cache_operation(self, hit: bool, cache_key: str):
        """Registrar operación de cache"""
        if hit:
            self.increment_counter("cache_hits_total", {"key": cache_key})
        else:
            self.increment_counter("cache_misses_total", {"key": cache_key})

    def record_mcp_tool_call(self, tool_name: str, duration: float, success: bool = True):
        """Registrar llamada a herramienta MCP"""
        self.increment_counter("mcp_tools_called_total", {"tool": tool_name})

        if not success:
            self.increment_counter("errors_total", {"tool": tool_name})

        self.observe_histogram("mcp_tool_duration_seconds", duration)

    def update_cache_metrics(self, size: int, hit_rate: float):
        """Actualizar métricas de cache"""
        self.set_gauge("cache_size", size)
        self.set_gauge("cache_hit_rate", hit_rate)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Obtener resumen de métricas"""
        uptime = time.time() - self.start_time

        # Calcular estadísticas de histogramas
        histogram_stats = {}
        for name, metric in self.metrics.items():
            if metric["type"] == MetricType.HISTOGRAM and metric["values"]:
                values = metric["values"]
                histogram_stats[name] = {
                    "count": len(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }

        return {
            "uptime_seconds": uptime,
            "metrics": self.metrics,
            "histogram_stats": histogram_stats,
            "timestamp": time.time()
        }

    def export_prometheus_format(self) -> str:
        """Exportar métricas en formato Prometheus"""
        lines = []
        lines.append("# HELP TrackHS MCP Server Metrics")
        lines.append("# TYPE TrackHS MCP Server Metrics")
        lines.append("")

        for name, metric in self.metrics.items():
            # Agregar descripción
            lines.append(f"# HELP {name} {metric.get('description', '')}")
            lines.append(f"# TYPE {name} {metric['type'].value}")

            if metric["type"] == MetricType.COUNTER:
                value = metric["value"]
                labels_str = self._format_labels(metric["labels"])
                lines.append(f"{name}{labels_str} {value}")

            elif metric["type"] == MetricType.GAUGE:
                value = metric["value"]
                labels_str = self._format_labels(metric["labels"])
                lines.append(f"{name}{labels_str} {value}")

            elif metric["type"] == MetricType.HISTOGRAM:
                values = metric.get("values", [])
                if values:
                    # Calcular buckets
                    buckets = metric.get("buckets", [0.1, 0.5, 1.0, 2.5, 5.0, 10.0])
                    bucket_counts = {}

                    for bucket in buckets:
                        count = sum(1 for v in values if v <= bucket)
                        bucket_counts[bucket] = count

                    # Agregar buckets
                    for bucket, count in bucket_counts.items():
                        labels_str = self._format_labels({**metric["labels"], "le": str(bucket)})
                        lines.append(f"{name}_bucket{labels_str} {count}")

                    # Agregar suma y cuenta
                    labels_str = self._format_labels(metric["labels"])
                    lines.append(f"{name}_sum{labels_str} {sum(values)}")
                    lines.append(f"{name}_count{labels_str} {len(values)}")

            lines.append("")

        return "\n".join(lines)

    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Formatear etiquetas para Prometheus"""
        if not labels:
            return ""

        label_pairs = [f'{k}="{v}"' for k, v in labels.items()]
        return "{" + ",".join(label_pairs) + "}"


# Instancia global de métricas
_global_metrics: Optional[PrometheusMetrics] = None


def get_metrics() -> PrometheusMetrics:
    """Obtener instancia global de métricas"""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = PrometheusMetrics()
    return _global_metrics


def record_request_metrics(method: str, duration: float, status_code: int = 200):
    """Registrar métricas de request"""
    metrics = get_metrics()
    metrics.record_request(method, duration, status_code)


def record_trackhs_api_metrics(endpoint: str, duration: float, success: bool = True):
    """Registrar métricas de TrackHS API"""
    metrics = get_metrics()
    metrics.record_trackhs_api_call(endpoint, duration, success)


def record_cache_metrics(hit: bool, cache_key: str):
    """Registrar métricas de cache"""
    metrics = get_metrics()
    metrics.record_cache_operation(hit, cache_key)


def record_mcp_tool_metrics(tool_name: str, duration: float, success: bool = True):
    """Registrar métricas de herramienta MCP"""
    metrics = get_metrics()
    metrics.record_mcp_tool_call(tool_name, duration, success)
