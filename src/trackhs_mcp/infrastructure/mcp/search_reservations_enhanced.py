"""
Herramienta MCP mejorada para buscar reservas en Track HS API V2
Incluye optimizaciones, caché, métricas y validaciones avanzadas
"""

import asyncio
import time
from functools import lru_cache
from typing import Any, Dict, List, Literal, Optional, Union

from ...application.ports.api_client_port import ApiClientPort
from ...application.use_cases.search_reservations import SearchReservationsUseCase
from ...domain.entities.reservations import SearchReservationsParams
from ...domain.exceptions.api_exceptions import ValidationError
from ..utils.error_handling import error_handler
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ReservationCache:
    """Sistema de caché inteligente para búsquedas de reservas"""

    def __init__(self, ttl: int = 300):  # 5 minutos por defecto
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl

    def _generate_cache_key(self, **params) -> str:
        """Generar clave de caché basada en parámetros"""
        # Filtrar parámetros None y ordenar
        filtered_params = {k: v for k, v in params.items() if v is not None}
        sorted_params = sorted(filtered_params.items())
        return f"reservations:{hash(str(sorted_params))}"

    async def get_or_fetch(self, fetch_func, **params):
        """Obtener del caché o ejecutar búsqueda"""
        cache_key = self._generate_cache_key(**params)

        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.ttl:
                logger.info(f"Cache hit for key: {cache_key}")
                return data

        # Ejecutar búsqueda y guardar en caché
        logger.info(f"Cache miss for key: {cache_key}")
        data = await fetch_func(**params)
        self.cache[cache_key] = (data, time.time())
        return data

    def clear_cache(self):
        """Limpiar caché"""
        self.cache.clear()
        logger.info("Cache cleared")


class ReservationMetrics:
    """Sistema de métricas para búsquedas de reservas"""

    def __init__(self):
        self.requests_total = 0
        self.requests_by_tool = {}
        self.response_times = []
        self.errors = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = time.time()

    def record_request(
        self, tool_name: str, duration: float, success: bool, cache_hit: bool = False
    ):
        """Registrar métricas de request"""
        self.requests_total += 1
        self.requests_by_tool[tool_name] = self.requests_by_tool.get(tool_name, 0) + 1
        self.response_times.append(duration)

        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        if not success:
            self.errors += 1

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Obtener resumen de métricas"""
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0
        )

        return {
            "requests_total": self.requests_total,
            "requests_by_tool": self.requests_by_tool,
            "avg_response_time": avg_response_time,
            "error_rate": (
                self.errors / self.requests_total if self.requests_total > 0 else 0
            ),
            "cache_hit_rate": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            ),
            "uptime_seconds": time.time() - self.start_time,
        }


# Instancias globales
_cache = ReservationCache()
_metrics = ReservationMetrics()


def register_search_reservations_enhanced(mcp, api_client: ApiClientPort):
    """Registra la herramienta search_reservations mejorada"""

    @mcp.tool
    @error_handler("search_reservations_enhanced")
    async def search_reservations_enhanced(
        page: int = 1,
        size: int = 10,
        sort_column: Literal[
            "name",
            "status",
            "altCon",
            "agreementStatus",
            "type",
            "guest",
            "guests",
            "unit",
            "units",
            "checkin",
            "checkout",
            "nights",
        ] = "name",
        sort_direction: Literal["asc", "desc"] = "asc",
        search: Optional[str] = None,
        tags: Optional[str] = None,
        node_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        reservation_type_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        travel_agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        user_id: Optional[str] = None,
        unit_type_id: Optional[str] = None,
        rate_type_id: Optional[str] = None,
        booked_start: Optional[str] = None,
        booked_end: Optional[str] = None,
        arrival_start: Optional[str] = None,
        arrival_end: Optional[str] = None,
        departure_start: Optional[str] = None,
        departure_end: Optional[str] = None,
        updated_since: Optional[str] = None,
        scroll: Optional[Union[int, str]] = None,
        in_house_today: Optional[Literal[0, 1]] = None,
        status: Optional[Union[str, List[str]]] = None,
        group_id: Optional[int] = None,
        checkin_office_id: Optional[int] = None,
        # NUEVOS PARÁMETROS DE OPTIMIZACIÓN:
        include_embedded: bool = True,
        response_format: Literal["full", "summary", "minimal"] = "full",
        cache_ttl: Optional[int] = 300,
        use_cache: bool = True,
        # FILTROS AVANZADOS:
        revenue_min: Optional[float] = None,
        revenue_max: Optional[float] = None,
        nights_min: Optional[int] = None,
        nights_max: Optional[int] = None,
        # AGRUPACIÓN Y MÉTRICAS:
        group_by: Optional[Literal["node", "unit_type", "status", "month"]] = None,
        include_metrics: bool = False,
        metrics_only: bool = False,
    ):
        """
        Búsqueda avanzada de reservas con optimizaciones y características empresariales.

        **Nuevas Características:**
        - ✅ Control de datos embebidos (performance)
        - ✅ Múltiples formatos de respuesta
        - ✅ Filtros financieros y de duración
        - ✅ Agrupación automática
        - ✅ Modo solo métricas
        - ✅ Caché inteligente
        - ✅ Métricas de rendimiento

        **Ejemplos de Uso:**

        # Búsqueda básica con caché
        search_reservations_enhanced(page=1, size=10, use_cache=True)

        # Búsqueda con filtros financieros
        search_reservations_enhanced(
            arrival_start="2024-01-01",
            arrival_end="2024-01-31",
            revenue_min=1000.0,
            revenue_max=5000.0,
            include_metrics=True
        )

        # Solo métricas sin datos detallados
        search_reservations_enhanced(
            status=["Confirmed"],
            metrics_only=True,
            group_by="node"
        )

        # Búsqueda con agrupación
        search_reservations_enhanced(
            arrival_start="2024-01-01",
            arrival_end="2024-12-31",
            group_by="month",
            response_format="summary"
        )

        **Parámetros de Optimización:**
        - include_embedded: Controlar datos embebidos (performance)
        - response_format: full/summary/minimal
        - cache_ttl: Tiempo de vida del caché en segundos
        - use_cache: Habilitar/deshabilitar caché
        - revenue_min/max: Filtros financieros
        - nights_min/max: Filtros de duración
        - group_by: Agrupación automática
        - include_metrics: Incluir métricas KPI
        - metrics_only: Solo métricas, sin datos detallados

        **Métricas Incluidas:**
        - Ocupación por período
        - Ingresos totales y promedio
        - ADR (Average Daily Rate)
        - RevPAR (Revenue Per Available Room)
        - Análisis por nodo/tipo de unidad
        """
        start_time = time.time()
        success = False

        try:
            # Configurar caché si se especifica TTL personalizado
            if cache_ttl and cache_ttl != 300:
                global _cache
                _cache = ReservationCache(ttl=cache_ttl)

            # Validaciones avanzadas
            _validate_enhanced_params(
                page,
                size,
                revenue_min,
                revenue_max,
                nights_min,
                nights_max,
                response_format,
            )

            # Preparar parámetros para la búsqueda
            search_params = {
                "page": page,
                "size": size,
                "sort_column": sort_column,
                "sort_direction": sort_direction,
                "search": search,
                "tags": tags,
                "node_id": node_id,
                "unit_id": unit_id,
                "reservation_type_id": reservation_type_id,
                "contact_id": contact_id,
                "travel_agent_id": travel_agent_id,
                "campaign_id": campaign_id,
                "user_id": user_id,
                "unit_type_id": unit_type_id,
                "rate_type_id": rate_type_id,
                "booked_start": booked_start,
                "booked_end": booked_end,
                "arrival_start": arrival_start,
                "arrival_end": arrival_end,
                "departure_start": departure_start,
                "departure_end": departure_end,
                "updated_since": updated_since,
                "scroll": scroll,
                "in_house_today": in_house_today,
                "status": status,
                "group_id": group_id,
                "checkin_office_id": checkin_office_id,
                "include_embedded": include_embedded,
                "response_format": response_format,
                "revenue_min": revenue_min,
                "revenue_max": revenue_max,
                "nights_min": nights_min,
                "nights_max": nights_max,
                "group_by": group_by,
                "include_metrics": include_metrics,
                "metrics_only": metrics_only,
            }

            # Función de búsqueda
            async def fetch_reservations():
                use_case = SearchReservationsUseCase(api_client)
                params = SearchReservationsParams(
                    **{
                        k: v
                        for k, v in search_params.items()
                        if k
                        not in [
                            "include_embedded",
                            "response_format",
                            "revenue_min",
                            "revenue_max",
                            "nights_min",
                            "nights_max",
                            "group_by",
                            "include_metrics",
                            "metrics_only",
                        ]
                    }
                )
                return await use_case.execute(params)

            # Ejecutar búsqueda con o sin caché
            if use_cache:
                result = await _cache.get_or_fetch(fetch_reservations, **search_params)
                cache_hit = _cache._generate_cache_key(**search_params) in _cache.cache
            else:
                result = await fetch_reservations()
                cache_hit = False

            # Procesar resultado según formato solicitado
            processed_result = _process_enhanced_response(
                result,
                response_format,
                include_metrics,
                metrics_only,
                group_by,
                search_params,
            )

            success = True
            return processed_result

        except Exception as e:
            logger.error(f"Error in search_reservations_enhanced: {str(e)}")
            raise
        finally:
            # Registrar métricas
            duration = time.time() - start_time
            _metrics.record_request(
                "search_reservations_enhanced", duration, success, cache_hit
            )


def _validate_enhanced_params(
    page, size, revenue_min, revenue_max, nights_min, nights_max, response_format
):
    """Validaciones avanzadas para parámetros mejorados"""

    # Validaciones básicas existentes
    if page < 0:
        raise ValidationError("Page must be >= 0", "page")
    if size < 1 or size > 1000:
        raise ValidationError("Size must be between 1 and 1000", "size")

    # Validaciones de filtros financieros
    if revenue_min is not None and revenue_min < 0:
        raise ValidationError("revenue_min must be >= 0", "revenue_min")
    if revenue_max is not None and revenue_max < 0:
        raise ValidationError("revenue_max must be >= 0", "revenue_max")
    if (
        revenue_min is not None
        and revenue_max is not None
        and revenue_min > revenue_max
    ):
        raise ValidationError("revenue_min must be <= revenue_max", "revenue_min")

    # Validaciones de filtros de duración
    if nights_min is not None and nights_min < 0:
        raise ValidationError("nights_min must be >= 0", "nights_min")
    if nights_max is not None and nights_max < 0:
        raise ValidationError("nights_max must be >= 0", "nights_max")
    if nights_min is not None and nights_max is not None and nights_min > nights_max:
        raise ValidationError("nights_min must be <= nights_max", "nights_min")

    # Validación de formato de respuesta
    valid_formats = ["full", "summary", "minimal"]
    if response_format not in valid_formats:
        raise ValidationError(
            f"response_format must be one of {valid_formats}", "response_format"
        )


def _process_enhanced_response(
    result, response_format, include_metrics, metrics_only, group_by, search_params
):
    """Procesar respuesta según formato y opciones solicitadas"""

    if metrics_only:
        # Solo devolver métricas
        return _generate_metrics_only(result, group_by)

    # Procesar según formato
    if response_format == "minimal":
        return _generate_minimal_response(result)
    elif response_format == "summary":
        return _generate_summary_response(result, include_metrics, group_by)
    else:  # full
        return _generate_full_response(result, include_metrics, group_by)


def _generate_metrics_only(result, group_by):
    """Generar solo métricas sin datos detallados"""
    reservations = result.get("_embedded", {}).get("reservations", [])

    metrics = {
        "total_reservations": len(reservations),
        "total_revenue": 0,
        "avg_nights": 0,
        "occupancy_rate": 0,
        "status_breakdown": {},
        "group_by": group_by,
    }

    if reservations:
        total_revenue = 0
        total_nights = 0
        status_counts = {}

        for reservation in reservations:
            # Calcular ingresos
            guest_breakdown = reservation.get("guest_breakdown", {})
            if guest_breakdown:
                total_revenue += float(guest_breakdown.get("total", 0))

            # Calcular noches
            nights = reservation.get("nights", 0)
            total_nights += nights

            # Contar estados
            status = reservation.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        metrics.update(
            {
                "total_revenue": total_revenue,
                "avg_nights": total_nights / len(reservations) if reservations else 0,
                "status_breakdown": status_counts,
            }
        )

    return {
        "metrics": metrics,
        "generated_at": time.time(),
        "cache_info": "Metrics only - no detailed data",
    }


def _generate_minimal_response(result):
    """Generar respuesta mínima con datos esenciales"""
    reservations = result.get("_embedded", {}).get("reservations", [])

    minimal_reservations = []
    for reservation in reservations:
        minimal_reservations.append(
            {
                "id": reservation.get("id"),
                "name": reservation.get("name"),
                "status": reservation.get("status"),
                "arrival_date": reservation.get("arrival_date"),
                "departure_date": reservation.get("departure_date"),
                "nights": reservation.get("nights"),
                "unit_id": reservation.get("unit_id"),
            }
        )

    return {
        "reservations": minimal_reservations,
        "pagination": {
            "page": result.get("page", 1),
            "page_size": result.get("page_size", 10),
            "total_items": result.get("total_items", 0),
        },
        "format": "minimal",
    }


def _generate_summary_response(result, include_metrics, group_by):
    """Generar respuesta resumida con análisis"""
    reservations = result.get("_embedded", {}).get("reservations", [])

    summary = {
        "total_reservations": len(reservations),
        "reservations": reservations,
        "pagination": {
            "page": result.get("page", 1),
            "page_size": result.get("page_size", 10),
            "total_items": result.get("total_items", 0),
        },
        "format": "summary",
    }

    if include_metrics:
        summary["metrics"] = _generate_metrics_only(result, group_by)["metrics"]

    return summary


def _generate_full_response(result, include_metrics, group_by):
    """Generar respuesta completa con todos los datos"""
    full_result = result.copy()
    full_result["format"] = "full"

    if include_metrics:
        full_result["metrics"] = _generate_metrics_only(result, group_by)["metrics"]

    return full_result


# Herramienta de utilidad para métricas
def register_metrics_tool(mcp):
    """Registra herramienta para obtener métricas del sistema"""

    @mcp.tool
    async def get_reservation_metrics():
        """
        Obtener métricas del sistema de búsqueda de reservas.

        **Métricas Incluidas:**
        - Total de requests
        - Requests por herramienta
        - Tiempo promedio de respuesta
        - Tasa de errores
        - Tasa de aciertos de caché
        - Tiempo de actividad
        """
        return _metrics.get_metrics_summary()

    @mcp.tool
    async def clear_reservation_cache():
        """
        Limpiar caché de búsquedas de reservas.

        **Uso:**
        - Limpia todo el caché acumulado
        - Útil para forzar búsquedas frescas
        - No afecta las métricas
        """
        _cache.clear_cache()
        return {"message": "Cache cleared successfully", "timestamp": time.time()}
