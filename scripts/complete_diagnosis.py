#!/usr/bin/env python3
"""
Script completo de diagnóstico para FastMCP Cloud - TrackHS API
Ejecuta todos los diagnósticos en secuencia y genera un reporte completo
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def run_diagnosis_script(script_name: str, description: str):
    """Ejecutar un script de diagnóstico específico"""
    print(f"\n{'='*80}")
    print(f"🔍 {description}")
    print(f"{'='*80}")

    if not os.path.exists(script_name):
        print(f"❌ Script no encontrado: {script_name}")
        return {"success": False, "error": "Script not found"}

    try:
        result = subprocess.run(
            [sys.executable, script_name], capture_output=True, text=True, timeout=120
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        print("❌ Script timeout (120s)")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"❌ Error ejecutando script: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Función principal de diagnóstico completo"""
    print("🚀 DIAGNÓSTICO COMPLETO DE FASTMCP CLOUD - TRACKHS API")
    print("=" * 100)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 100)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("scripts"):
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        return

    # Scripts de diagnóstico en orden de prioridad
    diagnosis_scripts = [
        (
            "scripts/check_fastmcp_cloud_config.py",
            "Verificación de Configuración FastMCP Cloud",
        ),
        ("scripts/test_specific_issue.py", "Diagnóstico del Problema Específico"),
        ("scripts/test_current_config.py", "Prueba de Configuración Actual"),
        ("scripts/test_url_variations_simple.py", "Prueba de Variaciones de URL"),
        ("scripts/test_auth_methods.py", "Prueba de Métodos de Autenticación"),
        ("scripts/test_endpoints.py", "Prueba de Endpoints Disponibles"),
        ("scripts/diagnose_fastmcp_cloud.py", "Diagnóstico Avanzado Completo"),
    ]

    results = {}
    successful_scripts = 0

    print("🎯 Ejecutando diagnósticos en secuencia...")

    for script_path, description in diagnosis_scripts:
        print(f"\n⏳ Ejecutando: {description}")
        result = run_diagnosis_script(script_path, description)
        results[description] = result

        if result["success"]:
            successful_scripts += 1
            print(f"✅ {description} - EXITOSO")
        else:
            print(f"❌ {description} - FALLÓ")
            if "error" in result:
                print(f"   Error: {result['error']}")

    # Resumen final
    print("\n" + "=" * 100)
    print("📊 RESUMEN FINAL DEL DIAGNÓSTICO")
    print("=" * 100)

    total_scripts = len(diagnosis_scripts)
    print(f"Scripts ejecutados: {total_scripts}")
    print(f"Scripts exitosos: {successful_scripts}")
    print(f"Scripts fallidos: {total_scripts - successful_scripts}")

    print(f"\n📋 DETALLE DE RESULTADOS:")
    for description, result in results.items():
        status = "✅" if result["success"] else "❌"
        print(f"   {status} {description}")
        if not result["success"] and "error" in result:
            print(f"      Error: {result['error']}")

    # Análisis y recomendaciones
    print(f"\n💡 ANÁLISIS Y RECOMENDACIONES:")
    print("=" * 100)

    if successful_scripts == 0:
        print("❌ NINGÚN DIAGNÓSTICO FUE EXITOSO")
        print("\n🔍 Posibles causas:")
        print("   - Variables de entorno no configuradas")
        print("   - Credenciales incorrectas")
        print("   - Problemas de conectividad")
        print("   - URL base incorrecta")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Verificar variables de entorno en FastMCP Cloud")
        print("   2. Contactar soporte técnico de TrackHS")
        print("   3. Verificar conectividad de red")

    elif successful_scripts < total_scripts:
        print(f"⚠️  {successful_scripts}/{total_scripts} DIAGNÓSTICOS EXITOSOS")
        print("\n🔍 Algunos diagnósticos fallaron, pero otros funcionaron")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Usar la configuración que funcionó")
        print("   2. Revisar los logs de los diagnósticos fallidos")
        print("   3. Implementar la solución exitosa")

    else:
        print("🎉 TODOS LOS DIAGNÓSTICOS FUERON EXITOSOS")
        print("\n✅ La configuración actual funciona correctamente")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. La configuración está lista para producción")
        print("   2. Desplegar en FastMCP Cloud")
        print("   3. Monitorear el funcionamiento")

    # Guardar reporte completo
    report_file = (
        f"complete_diagnosis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_scripts": total_scripts,
        "successful_scripts": successful_scripts,
        "failed_scripts": total_scripts - successful_scripts,
        "success_rate": (successful_scripts / total_scripts) * 100,
        "results": results,
        "environment": {
            "TRACKHS_USERNAME_configured": bool(os.getenv("TRACKHS_USERNAME")),
            "TRACKHS_PASSWORD_configured": bool(os.getenv("TRACKHS_PASSWORD")),
            "TRACKHS_API_URL_configured": bool(os.getenv("TRACKHS_API_URL")),
            "TRACKHS_API_URL_value": os.getenv("TRACKHS_API_URL", "default"),
        },
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Reporte completo guardado en: {report_file}")

    # Instrucciones finales
    print(f"\n🎯 INSTRUCCIONES FINALES:")
    print("=" * 100)

    if successful_scripts > 0:
        print("✅ Al menos un diagnóstico fue exitoso")
        print("   - Usa la configuración que funcionó")
        print("   - Actualiza las variables de entorno en FastMCP Cloud")
        print("   - Reinicia el servidor")
    else:
        print("❌ Ningún diagnóstico fue exitoso")
        print("   - Revisa las variables de entorno")
        print("   - Verifica las credenciales")
        print("   - Contacta soporte técnico")

    print(f"\n📞 Para soporte adicional:")
    print("   - Incluye el archivo de reporte: {report_file}")
    print("   - Incluye los logs del servidor")
    print("   - Incluye la configuración de variables (sin credenciales)")


if __name__ == "__main__":
    main()
