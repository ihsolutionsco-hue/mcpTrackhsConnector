#!/usr/bin/env python3
"""
Script maestro para ejecutar todos los tests locales
Prueba la API real de TrackHS en local antes de desplegar en FastMCP Cloud
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def run_local_test(script_name: str, description: str):
    """Ejecutar un test local específico"""
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


def check_credentials():
    """Verificar que las credenciales estén configuradas"""
    print("🔍 Verificando credenciales...")

    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("\n💡 Configure las variables de entorno:")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")
        print("\n   O cree un archivo .env con:")
        print("   TRACKHS_USERNAME=tu_usuario")
        print("   TRACKHS_PASSWORD=tu_password")
        return False

    print(f"✅ Credenciales encontradas:")
    print(f"   Username: {username[:3]}***")
    print(f"   Password: {'***' if password else 'None'}")
    return True


def main():
    """Función principal"""
    print("🚀 TESTS LOCALES - API REAL DE TRACKHS")
    print("=" * 100)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 100)
    print("Este script ejecuta todos los tests locales para verificar")
    print("que la API real de TrackHS funcione correctamente antes")
    print("de desplegar en FastMCP Cloud")
    print("=" * 100)

    # Verificar credenciales
    if not check_credentials():
        return

    # Scripts de test local en orden de prioridad
    local_tests = [
        ("scripts/test_basic_connectivity.py", "Test de Conectividad Básica"),
        ("scripts/test_current_config_local.py", "Test de Configuración Actual"),
        ("scripts/test_local_api_real.py", "Test de Múltiples Configuraciones"),
        ("scripts/test_auth_methods_local.py", "Test de Métodos de Autenticación"),
    ]

    results = {}
    successful_tests = 0

    print("🎯 Ejecutando tests locales en secuencia...")

    for script_path, description in local_tests:
        print(f"\n⏳ Ejecutando: {description}")
        result = run_local_test(script_path, description)
        results[description] = result

        if result["success"]:
            successful_tests += 1
            print(f"✅ {description} - EXITOSO")
        else:
            print(f"❌ {description} - FALLÓ")
            if "error" in result:
                print(f"   Error: {result['error']}")

    # Resumen final
    print("\n" + "=" * 100)
    print("📊 RESUMEN FINAL DE TESTS LOCALES")
    print("=" * 100)

    total_tests = len(local_tests)
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {successful_tests}")
    print(f"Tests fallidos: {total_tests - successful_tests}")

    print(f"\n📋 DETALLE DE RESULTADOS:")
    for description, result in results.items():
        status = "✅" if result["success"] else "❌"
        print(f"   {status} {description}")
        if not result["success"] and "error" in result:
            print(f"      Error: {result['error']}")

    # Análisis y recomendaciones
    print(f"\n💡 ANÁLISIS Y RECOMENDACIONES:")
    print("=" * 100)

    if successful_tests == 0:
        print("❌ NINGÚN TEST LOCAL FUE EXITOSO")
        print("\n🔍 Posibles causas:")
        print("   - Credenciales incorrectas")
        print("   - URL base incorrecta")
        print("   - API no disponible")
        print("   - Problemas de conectividad")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Verificar credenciales con TrackHS")
        print("   2. Contactar soporte técnico de TrackHS")
        print("   3. Verificar conectividad de red")

    elif successful_tests < total_tests:
        print(f"⚠️  {successful_tests}/{total_tests} TESTS LOCALES EXITOSOS")
        print("\n🔍 Algunos tests fallaron, pero otros funcionaron")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Usar la configuración que funcionó")
        print("   2. Revisar los logs de los tests fallidos")
        print("   3. Implementar la solución exitosa en FastMCP Cloud")

    else:
        print("🎉 TODOS LOS TESTS LOCALES FUERON EXITOSOS")
        print("\n✅ La configuración funciona correctamente con la API real")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. La configuración está lista para FastMCP Cloud")
        print("   2. Desplegar en FastMCP Cloud con la misma configuración")
        print("   3. Monitorear el funcionamiento")

    # Configuración recomendada para FastMCP Cloud
    if successful_tests > 0:
        print(f"\n🔧 CONFIGURACIÓN RECOMENDADA PARA FASTMCP CLOUD:")
        print("=" * 100)

        base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
        username = os.getenv("TRACKHS_USERNAME")
        password = os.getenv("TRACKHS_PASSWORD")

        print(f"Variables de entorno:")
        print(f"   TRACKHS_API_URL={base_url}")
        print(f"   TRACKHS_USERNAME={username}")
        print(f"   TRACKHS_PASSWORD={password}")

        print(f"\n📝 NOTAS:")
        print(f"   - Esta configuración funciona en local")
        print(f"   - Debería funcionar en FastMCP Cloud")
        print(f"   - Si hay problemas en FastMCP Cloud, revisar variables de entorno")

    # Guardar reporte completo
    report_file = f"local_tests_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "failed_tests": total_tests - successful_tests,
        "success_rate": (successful_tests / total_tests) * 100,
        "results": results,
        "environment": {
            "TRACKHS_USERNAME_configured": bool(os.getenv("TRACKHS_USERNAME")),
            "TRACKHS_PASSWORD_configured": bool(os.getenv("TRACKHS_PASSWORD")),
            "TRACKHS_API_URL_configured": bool(os.getenv("TRACKHS_API_URL")),
            "TRACKHS_API_URL_value": os.getenv("TRACKHS_API_URL", "default"),
        },
        "recommendations": {
            "fastmcp_cloud_config": {
                "TRACKHS_API_URL": os.getenv(
                    "TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api"
                ),
                "TRACKHS_USERNAME": os.getenv("TRACKHS_USERNAME"),
                "TRACKHS_PASSWORD": "***",
            }
        },
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Reporte completo guardado en: {report_file}")

    # Instrucciones finales
    print(f"\n🎯 INSTRUCCIONES FINALES:")
    print("=" * 100)

    if successful_tests > 0:
        print("✅ Al menos un test local fue exitoso")
        print("   - Usa la configuración que funcionó")
        print("   - Configura las variables de entorno en FastMCP Cloud")
        print("   - Despliega el servidor")
        print("   - Prueba la herramienta search_units")
    else:
        print("❌ Ningún test local fue exitoso")
        print("   - Revisa las credenciales")
        print("   - Verifica la URL base")
        print("   - Contacta soporte técnico de TrackHS")

    print(f"\n📞 Para soporte adicional:")
    print("   - Incluye el archivo de reporte: {report_file}")
    print("   - Incluye los logs del servidor")
    print("   - Incluye la configuración de variables (sin credenciales)")


if __name__ == "__main__":
    main()
