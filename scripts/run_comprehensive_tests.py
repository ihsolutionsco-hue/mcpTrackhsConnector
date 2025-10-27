#!/usr/bin/env python3
"""
Script de testing comprehensivo para TrackHS MCP Server
Ejecuta todos los tests y genera reportes detallados
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Comando: {command}")
    print("-" * 60)
    
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        duration = time.time() - start_time
        
        print(f"✅ Completado en {duration:.2f}s")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Error en {duration:.2f}s: {e}")
        return False, "", str(e)

def check_environment():
    """Verificar entorno de testing"""
    print("🔍 Verificando entorno de testing...")
    
    # Verificar Python
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 11):
        print("❌ Se requiere Python 3.11+")
        return False
    
    # Verificar dependencias
    try:
        import pytest
        import httpx
        import pydantic
        print("✅ Dependencias principales disponibles")
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        return False
    
    return True

def run_unit_tests():
    """Ejecutar tests unitarios"""
    print("\n🧪 Ejecutando tests unitarios...")
    
    commands = [
        ("python -m pytest tests/test_business_validators.py -v", "Validadores de negocio"),
        ("python -m pytest tests/test_response_validation.py -v", "Validación de respuestas"),
        ("python -m pytest tests/test_sanitization.py -v", "Sanitización de datos"),
        ("python -m pytest tests/test_retries.py -v", "Sistema de reintentos"),
    ]
    
    results = []
    for command, description in commands:
        success, stdout, stderr = run_command(command, description)
        results.append((description, success, stdout, stderr))
    
    return results

def run_integration_tests():
    """Ejecutar tests de integración"""
    print("\n🔗 Ejecutando tests de integración...")
    
    commands = [
        ("python -m pytest tests/test_repositories_integration.py -v", "Repositories"),
        ("python -m pytest tests/test_cache_and_metrics.py -v", "Cache y métricas"),
        ("python -m pytest tests/test_middleware.py -v", "Middleware"),
        ("python -m pytest tests/test_integration.py -v", "Integración general"),
    ]
    
    results = []
    for command, description in commands:
        success, stdout, stderr = run_command(command, description)
        results.append((description, success, stdout, stderr))
    
    return results

def run_mcp_tests():
    """Ejecutar tests de protocolo MCP"""
    print("\n📡 Ejecutando tests de protocolo MCP...")
    
    commands = [
        ("python -m pytest tests/test_mcp_protocol.py -v", "Protocolo MCP"),
        ("python -m pytest tests/test_mcp_server.py -v", "Servidor MCP"),
        ("python -m pytest tests/test_health.py -v", "Health check"),
    ]
    
    results = []
    for command, description in commands:
        success, stdout, stderr = run_command(command, description)
        results.append((description, success, stdout, stderr))
    
    return results

def run_tool_tests():
    """Ejecutar tests de herramientas MCP"""
    print("\n🛠️ Ejecutando tests de herramientas MCP...")
    
    commands = [
        ("python -m pytest tests/test_search_reservations.py -v", "Búsqueda de reservas"),
        ("python -m pytest tests/test_get_reservation.py -v", "Obtener reserva"),
        ("python -m pytest tests/test_search_units.py -v", "Búsqueda de unidades"),
        ("python -m pytest tests/test_get_folio.py -v", "Obtener folio"),
        ("python -m pytest tests/test_create_maintenance_work_order.py -v", "Órdenes de mantenimiento"),
    ]
    
    results = []
    for command, description in commands:
        success, stdout, stderr = run_command(command, description)
        results.append((description, success, stdout, stderr))
    
    return results

def run_coverage_tests():
    """Ejecutar tests con cobertura"""
    print("\n📊 Ejecutando tests con cobertura...")
    
    command = "python -m pytest --cov=src/trackhs_mcp --cov-report=html --cov-report=term-missing tests/ -v"
    success, stdout, stderr = run_command(command, "Cobertura de código")
    
    return success, stdout, stderr

def run_performance_tests():
    """Ejecutar tests de rendimiento"""
    print("\n⚡ Ejecutando tests de rendimiento...")
    
    # Test de carga básico
    command = "python -m pytest tests/test_integration.py::test_performance -v -s"
    success, stdout, stderr = run_command(command, "Test de rendimiento")
    
    return success, stdout, stderr

def generate_test_report(all_results):
    """Generar reporte de testing"""
    print("\n📋 Generando reporte de testing...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "success_rate": 0.0
        },
        "categories": {},
        "details": []
    }
    
    for category, results in all_results.items():
        category_passed = sum(1 for _, success, _, _ in results if success)
        category_total = len(results)
        
        report["categories"][category] = {
            "passed": category_passed,
            "total": category_total,
            "success_rate": (category_passed / category_total * 100) if category_total > 0 else 0
        }
        
        report["summary"]["total_tests"] += category_total
        report["summary"]["passed"] += category_passed
        
        for description, success, stdout, stderr in results:
            report["details"].append({
                "category": category,
                "test": description,
                "success": success,
                "stdout": stdout,
                "stderr": stderr
            })
    
    report["summary"]["failed"] = report["summary"]["total_tests"] - report["summary"]["passed"]
    if report["summary"]["total_tests"] > 0:
        report["summary"]["success_rate"] = (
            report["summary"]["passed"] / report["summary"]["total_tests"] * 100
        )
    
    # Guardar reporte
    report_file = Path(__file__).parent.parent / "test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Reporte guardado en: {report_file}")
    
    return report

def print_summary(report):
    """Imprimir resumen de testing"""
    print("\n" + "="*80)
    print("📊 RESUMEN DE TESTING COMPREHENSIVO")
    print("="*80)
    
    summary = report["summary"]
    print(f"Total de tests: {summary['total_tests']}")
    print(f"Exitosos: {summary['passed']}")
    print(f"Fallidos: {summary['failed']}")
    print(f"Tasa de éxito: {summary['success_rate']:.1f}%")
    
    print("\n📈 Por categoría:")
    for category, stats in report["categories"].items():
        status = "✅" if stats["success_rate"] == 100 else "⚠️" if stats["success_rate"] >= 80 else "❌"
        print(f"  {status} {category}: {stats['passed']}/{stats['total']} ({stats['success_rate']:.1f}%)")
    
    print("\n" + "="*80)

def main():
    """Función principal"""
    print("🚀 Iniciando testing comprehensivo de TrackHS MCP Server")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar entorno
    if not check_environment():
        print("❌ Entorno de testing no válido")
        return 1
    
    # Ejecutar tests por categoría
    all_results = {}
    
    # Tests unitarios
    all_results["Unitarios"] = run_unit_tests()
    
    # Tests de integración
    all_results["Integración"] = run_integration_tests()
    
    # Tests MCP
    all_results["MCP"] = run_mcp_tests()
    
    # Tests de herramientas
    all_results["Herramientas"] = run_tool_tests()
    
    # Tests de cobertura
    coverage_success, coverage_stdout, coverage_stderr = run_coverage_tests()
    all_results["Cobertura"] = [("Cobertura de código", coverage_success, coverage_stdout, coverage_stderr)]
    
    # Tests de rendimiento
    perf_success, perf_stdout, perf_stderr = run_performance_tests()
    all_results["Rendimiento"] = [("Test de rendimiento", perf_success, perf_stdout, perf_stderr)]
    
    # Generar reporte
    report = generate_test_report(all_results)
    
    # Mostrar resumen
    print_summary(report)
    
    # Determinar código de salida
    if report["summary"]["success_rate"] >= 90:
        print("\n🎉 ¡Testing completado exitosamente!")
        return 0
    elif report["summary"]["success_rate"] >= 70:
        print("\n⚠️ Testing completado con advertencias")
        return 1
    else:
        print("\n❌ Testing falló")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
