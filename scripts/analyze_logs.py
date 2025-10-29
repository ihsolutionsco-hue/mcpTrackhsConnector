#!/usr/bin/env python3
"""
Script para analizar logs de TrackHS MCP Connector
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List


def load_logs(log_file: str) -> List[Dict[str, Any]]:
    """Carga logs desde un archivo JSON"""
    logs = []

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        print(f"❌ Archivo de log no encontrado: {log_file}")
        return []

    return logs


def analyze_api_calls(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analiza llamadas a API"""
    api_calls = [log for log in logs if log.get("api_call")]

    if not api_calls:
        return {"total": 0, "message": "No se encontraron llamadas a API"}

    # Agrupar por endpoint
    endpoints = Counter()
    methods = Counter()
    status_codes = Counter()
    response_times = []

    for call in api_calls:
        endpoints[call.get("endpoint", "unknown")] += 1
        methods[call.get("method", "unknown")] += 1
        status_codes[call.get("status_code", "unknown")] += 1

        if "response_time_ms" in call:
            response_times.append(call["response_time_ms"])

    return {
        "total": len(api_calls),
        "endpoints": dict(endpoints.most_common()),
        "methods": dict(methods.most_common()),
        "status_codes": dict(status_codes.most_common()),
        "avg_response_time_ms": (
            sum(response_times) / len(response_times) if response_times else 0
        ),
        "min_response_time_ms": min(response_times) if response_times else 0,
        "max_response_time_ms": max(response_times) if response_times else 0,
    }


def analyze_search_operations(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analiza operaciones de búsqueda"""
    search_ops = [log for log in logs if log.get("search_operation")]

    if not search_ops:
        return {"total": 0, "message": "No se encontraron operaciones de búsqueda"}

    # Agrupar por tipo de operación
    operations = Counter()
    filter_counts = []
    units_counts = []

    for op in search_ops:
        operations[op.get("operation", "unknown")] += 1

        if "filter_count" in op:
            filter_counts.append(op["filter_count"])

        if "units_count" in op:
            units_counts.append(op["units_count"])

    return {
        "total": len(search_ops),
        "operations": dict(operations.most_common()),
        "avg_filters_per_search": (
            sum(filter_counts) / len(filter_counts) if filter_counts else 0
        ),
        "avg_units_found": sum(units_counts) / len(units_counts) if units_counts else 0,
        "searches_with_zero_results": sum(1 for count in units_counts if count == 0),
    }


def analyze_errors(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analiza errores en los logs"""
    error_logs = [log for log in logs if log.get("level") == "ERROR"]

    if not error_logs:
        return {"total": 0, "message": "No se encontraron errores"}

    # Agrupar por tipo de error
    error_types = Counter()
    error_messages = Counter()

    for error in error_logs:
        error_types[error.get("error_type", "unknown")] += 1
        error_messages[error.get("message", "unknown")] += 1

    return {
        "total": len(error_logs),
        "error_types": dict(error_types.most_common()),
        "common_errors": dict(error_messages.most_common(5)),
    }


def analyze_debugging_metrics(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analiza métricas de debugging"""
    debug_logs = [log for log in logs if log.get("debugging_metrics")]

    if not debug_logs:
        return {"total": 0, "message": "No se encontraron métricas de debugging"}

    # Agregar métricas
    all_metrics = defaultdict(list)

    for log in debug_logs:
        metrics = log.get("metrics", {})
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                all_metrics[key].append(value)

    # Calcular estadísticas
    stats = {}
    for key, values in all_metrics.items():
        if values:
            stats[key] = {
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            }

    return {"total": len(debug_logs), "metrics": stats}


def generate_report(logs: List[Dict[str, Any]]) -> str:
    """Genera un reporte completo de análisis"""
    report = []
    report.append("📊 REPORTE DE ANÁLISIS DE LOGS - TrackHS MCP Connector")
    report.append("=" * 70)

    # Resumen general
    total_logs = len(logs)
    report.append(f"\n📈 RESUMEN GENERAL:")
    report.append(f"   Total de logs: {total_logs}")
    report.append(
        f"   Logs de API: {len([log for log in logs if log.get('api_call')])}"
    )
    report.append(
        f"   Logs de búsqueda: {len([log for log in logs if log.get('search_operation')])}"
    )
    report.append(
        f"   Logs de error: {len([log for log in logs if log.get('level') == 'ERROR'])}"
    )

    # Análisis de API
    api_analysis = analyze_api_calls(logs)
    report.append(f"\n🔌 ANÁLISIS DE LLAMADAS A API:")
    if api_analysis.get("total", 0) > 0:
        report.append(f"   Total de llamadas: {api_analysis['total']}")
        report.append(f"   Endpoints más usados: {api_analysis['endpoints']}")
        report.append(f"   Métodos HTTP: {api_analysis['methods']}")
        report.append(f"   Códigos de estado: {api_analysis['status_codes']}")
        report.append(
            f"   Tiempo promedio de respuesta: {api_analysis['avg_response_time_ms']:.2f}ms"
        )
    else:
        report.append(f"   {api_analysis.get('message', 'Sin datos')}")

    # Análisis de búsquedas
    search_analysis = analyze_search_operations(logs)
    report.append(f"\n🔍 ANÁLISIS DE BÚSQUEDAS:")
    if search_analysis.get("total", 0) > 0:
        report.append(f"   Total de búsquedas: {search_analysis['total']}")
        report.append(f"   Tipos de operación: {search_analysis['operations']}")
        report.append(
            f"   Filtros promedio por búsqueda: {search_analysis['avg_filters_per_search']:.2f}"
        )
        report.append(
            f"   Unidades encontradas promedio: {search_analysis['avg_units_found']:.2f}"
        )
        report.append(
            f"   Búsquedas sin resultados: {search_analysis['searches_with_zero_results']}"
        )
    else:
        report.append(f"   {search_analysis.get('message', 'Sin datos')}")

    # Análisis de errores
    error_analysis = analyze_errors(logs)
    report.append(f"\n❌ ANÁLISIS DE ERRORES:")
    if error_analysis.get("total", 0) > 0:
        report.append(f"   Total de errores: {error_analysis['total']}")
        report.append(f"   Tipos de error: {error_analysis['error_types']}")
        report.append(f"   Errores más comunes: {error_analysis['common_errors']}")
    else:
        report.append(f"   {error_analysis.get('message', 'Sin errores')}")

    # Análisis de métricas de debugging
    debug_analysis = analyze_debugging_metrics(logs)
    report.append(f"\n🔧 MÉTRICAS DE DEBUGGING:")
    if debug_analysis.get("total", 0) > 0:
        report.append(f"   Total de métricas: {debug_analysis['total']}")
        for metric, stats in debug_analysis["metrics"].items():
            report.append(
                f"   {metric}: avg={stats['avg']:.2f}, min={stats['min']}, max={stats['max']}"
            )
    else:
        report.append(f"   {debug_analysis.get('message', 'Sin métricas')}")

    return "\n".join(report)


def main():
    """Función principal"""
    if len(sys.argv) != 2:
        print("Uso: python analyze_logs.py <archivo_de_log>")
        print("Ejemplo: python analyze_logs.py logs/trackhs_mcp.log")
        sys.exit(1)

    log_file = sys.argv[1]

    print("🔍 Analizando logs de TrackHS MCP Connector...")

    # Cargar logs
    logs = load_logs(log_file)

    if not logs:
        print("❌ No se pudieron cargar logs del archivo especificado")
        sys.exit(1)

    # Generar reporte
    report = generate_report(logs)
    print(report)

    # Guardar reporte
    report_file = Path(log_file).parent / f"analysis_report_{Path(log_file).stem}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n💾 Reporte guardado en: {report_file}")


if __name__ == "__main__":
    main()
