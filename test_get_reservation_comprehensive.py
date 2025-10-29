#!/usr/bin/env python3
"""
Script de pruebas comprehensivas para el tool get_reservation actualizado con API V2
Incluye pruebas unitarias, de integración y end-to-end
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict

import pytest

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def run_tests():
    """Ejecutar todas las pruebas de get_reservation"""

    print("=" * 80)
    print("PRUEBAS COMPREHENSIVAS - GET RESERVATION API V2")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print()

    # Lista de archivos de prueba
    test_files = [
        "tests/test_get_reservation_unit.py",
        "tests/test_get_reservation_integration.py",
        "tests/test_get_reservation_e2e.py",
    ]

    # Configuración de pytest
    pytest_args = [
        "-v",  # Verbose
        "--tb=short",  # Traceback corto
        "--strict-markers",  # Marcadores estrictos
        "--disable-warnings",  # Deshabilitar warnings
        "--color=yes",  # Colores
        "--durations=10",  # Mostrar 10 tests más lentos
    ]

    # Agregar archivos de prueba
    pytest_args.extend(test_files)

    print("ARCHIVOS DE PRUEBA:")
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"   [OK] {test_file}")
        else:
            print(f"   [ERROR] {test_file} - NO ENCONTRADO")
    print()

    # Ejecutar pruebas
    print("EJECUTANDO PRUEBAS...")
    print("-" * 80)

    start_time = time.time()

    try:
        # Ejecutar pytest
        exit_code = pytest.main(pytest_args)

        end_time = time.time()
        execution_time = end_time - start_time

        print()
        print("-" * 80)
        print("📊 RESUMEN DE PRUEBAS")
        print("-" * 80)
        print(f"⏱️  Tiempo total: {execution_time:.2f} segundos")

        if exit_code == 0:
            print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
            print(
                "🎉 El tool get_reservation está funcionando correctamente con la API V2"
            )
        else:
            print("❌ ALGUNAS PRUEBAS FALLARON")
            print("🔍 Revisa los detalles arriba para más información")

        return exit_code == 0

    except Exception as e:
        print(f"❌ ERROR EJECUTANDO PRUEBAS: {str(e)}")
        return False


def run_individual_test_suites():
    """Ejecutar suites de prueba individuales"""

    print("=" * 80)
    print("🧪 PRUEBAS INDIVIDUALES - GET RESERVATION API V2")
    print("=" * 80)

    test_suites = [
        {
            "name": "Pruebas Unitarias",
            "file": "tests/test_get_reservation_unit.py",
            "description": "Pruebas de componentes individuales y mocks",
        },
        {
            "name": "Pruebas de Integración",
            "file": "tests/test_get_reservation_integration.py",
            "description": "Pruebas de comunicación con API V2",
        },
        {
            "name": "Pruebas End-to-End",
            "file": "tests/test_get_reservation_e2e.py",
            "description": "Pruebas de flujo completo",
        },
    ]

    results = {}

    for suite in test_suites:
        print(f"\n🔬 {suite['name']}")
        print(f"📝 {suite['description']}")
        print("-" * 60)

        if not os.path.exists(suite["file"]):
            print(f"❌ Archivo no encontrado: {suite['file']}")
            results[suite["name"]] = False
            continue

        start_time = time.time()

        try:
            exit_code = pytest.main(
                ["-v", "--tb=short", "--disable-warnings", "--color=yes", suite["file"]]
            )

            end_time = time.time()
            execution_time = end_time - start_time

            success = exit_code == 0
            results[suite["name"]] = success

            if success:
                print(f"✅ {suite['name']} - PASÓ ({execution_time:.2f}s)")
            else:
                print(f"❌ {suite['name']} - FALLÓ ({execution_time:.2f}s)")

        except Exception as e:
            print(f"❌ ERROR en {suite['name']}: {str(e)}")
            results[suite["name"]] = False

    # Resumen de resultados
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE SUITES DE PRUEBA")
    print("=" * 80)

    for name, success in results.items():
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{name:<25} {status}")

    all_passed = all(results.values())
    print(
        f"\n{'🎉 TODAS LAS SUITES PASARON' if all_passed else '⚠️  ALGUNAS SUITES FALLARON'}"
    )

    return all_passed


def generate_test_report():
    """Generar reporte detallado de pruebas"""

    print("\n" + "=" * 80)
    print("📋 GENERANDO REPORTE DE PRUEBAS")
    print("=" * 80)

    report = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "test_files": [
            "tests/test_get_reservation_unit.py",
            "tests/test_get_reservation_integration.py",
            "tests/test_get_reservation_e2e.py",
        ],
        "api_version": "V2",
        "endpoint": "/api/v2/pms/reservations/{reservationId}",
        "schema_fields": 57,
        "features_tested": [
            "Validación de esquema Pydantic",
            "Comunicación con API V2",
            "Manejo de errores",
            "Datos embebidos completos",
            "Desglose financiero detallado",
            "Enlaces relacionados",
            "Rendimiento",
            "Compatibilidad de tipos",
        ],
    }

    # Guardar reporte
    report_file = (
        f"get_reservation_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    try:
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📄 Reporte guardado en: {report_file}")
        print(f"📊 Campos del schema: {report['schema_fields']}")
        print(f"🔗 Endpoint: {report['endpoint']}")
        print(f"✨ Características probadas: {len(report['features_tested'])}")

    except Exception as e:
        print(f"❌ Error guardando reporte: {str(e)}")


def main():
    """Función principal"""

    print("INICIANDO PRUEBAS COMPREHENSIVAS DE GET RESERVATION")
    print("=" * 80)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src/trackhs_mcp"):
        print("ERROR: No se encontró el directorio src/trackhs_mcp")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        return False

    # Ejecutar pruebas individuales
    individual_success = run_individual_test_suites()

    # Ejecutar todas las pruebas juntas
    print("\n" + "=" * 80)
    print("🔄 EJECUTANDO TODAS LAS PRUEBAS JUNTAS")
    print("=" * 80)

    comprehensive_success = run_tests()

    # Generar reporte
    generate_test_report()

    # Resultado final
    print("\n" + "=" * 80)
    print("🏁 RESULTADO FINAL")
    print("=" * 80)

    if individual_success and comprehensive_success:
        print("🎉 ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("✅ El tool get_reservation está listo para producción con API V2")
        print("🚀 Características validadas:")
        print("   • 57 campos del schema actualizado")
        print("   • Endpoint V2 funcional")
        print("   • Datos embebidos completos")
        print("   • Desglose financiero detallado")
        print("   • Manejo robusto de errores")
        print("   • Rendimiento optimizado")
        return True
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON")
        print("🔍 Revisa los logs arriba para identificar problemas")
        print("🛠️  Corrige los errores antes de continuar")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
