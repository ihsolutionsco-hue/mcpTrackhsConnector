#!/usr/bin/env python3
"""
Script maestro para ejecutar todos los diagnósticos de FastMCP Cloud
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def run_script(script_name: str, description: str):
    """Ejecutar un script de diagnóstico"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, script_name], capture_output=True, text=True, timeout=60
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Script timeout (60s)")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando script: {str(e)}")
        return False


def main():
    """Función principal"""
    print("🚀 DIAGNÓSTICO COMPLETO DE FASTMCP CLOUD - TRACKHS API")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("scripts"):
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        return

    # Scripts a ejecutar
    scripts = [
        ("scripts/test_current_config.py", "Configuración Actual"),
        ("scripts/test_url_variations_simple.py", "Variaciones de URL"),
        ("scripts/test_auth_methods.py", "Métodos de Autenticación"),
        ("scripts/test_endpoints.py", "Endpoints Disponibles"),
    ]

    results = {}

    for script_path, description in scripts:
        if os.path.exists(script_path):
            success = run_script(script_path, description)
            results[description] = success
        else:
            print(f"❌ Script no encontrado: {script_path}")
            results[description] = False

    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL")
    print("=" * 80)

    successful_tests = sum(1 for success in results.values() if success)
    total_tests = len(results)

    print(f"Tests exitosos: {successful_tests}/{total_tests}")

    for test_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {test_name}")

    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")

    if successful_tests == 0:
        print("   ❌ Ningún test fue exitoso")
        print("   🔍 Verificar:")
        print("      - Variables de entorno TRACKHS_USERNAME y TRACKHS_PASSWORD")
        print("      - Conectividad de red")
        print("      - URL base correcta")
        print("      - Credenciales válidas")
    elif successful_tests < total_tests:
        print("   ⚠️  Algunos tests fallaron")
        print("   🔍 Revisar los logs de los tests fallidos")
        print("   💡 Usar la configuración que funcionó")
    else:
        print("   ✅ Todos los tests fueron exitosos")
        print("   🎉 La configuración actual debería funcionar")

    # Guardar resultados
    results_file = "full_diagnosis_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "results": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n📄 Resultados guardados en: {results_file}")


if __name__ == "__main__":
    main()
