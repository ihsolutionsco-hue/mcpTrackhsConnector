#!/usr/bin/env python3
"""
Script para ejecutar todos los tests disponibles
Ejecuta todos los tests en secuencia para un diagnóstico completo
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def run_script(script_name: str, description: str):
    """Ejecutar un script específico"""
    print(f"\n{'='*120}")
    print(f"🔍 {description}")
    print(f"{'='*120}")

    if not os.path.exists(script_name):
        print(f"❌ Script no encontrado: {script_name}")
        return {"success": False, "error": "Script not found"}

    try:
        result = subprocess.run(
            [sys.executable, script_name], capture_output=True, text=True, timeout=300
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
        print("❌ Script timeout (300s)")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"❌ Error ejecutando script: {str(e)}")
        return {"success": False, "error": str(e)}


def check_environment():
    """Verificar entorno y credenciales"""
    print("🔍 Verificando entorno y credenciales...")

    # Verificar Python
    print(f"Python version: {sys.version}")

    # Verificar credenciales
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    api_url = os.getenv("TRACKHS_API_URL")

    print(f"TRACKHS_USERNAME: {'✅' if username else '❌'}")
    print(f"TRACKHS_PASSWORD: {'✅' if password else '❌'}")
    print(f"TRACKHS_API_URL: {'✅' if api_url else '⚠️  (usando default)'}")

    if not username or not password:
        print("\n❌ Error: Credenciales no configuradas")
        print("Configure las variables de entorno antes de continuar")
        return False

    return True


def main():
    """Función principal"""
    print("🚀 EJECUTAR TODOS LOS TESTS - TRACKHS API")
    print("=" * 140)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 140)
    print("Este script ejecuta todos los tests disponibles para")
    print("diagnosticar completamente el problema con el servidor MCP de TrackHS")
    print("=" * 140)

    # Verificar entorno
    if not check_environment():
        return

    # Scripts de test en orden de prioridad
    test_scripts = [
        ("scripts/run_quick_test.py", "1. Prueba Rápida"),
        (
            "scripts/verify_server_config.py",
            "2. Verificación de Configuración del Servidor",
        ),
        (
            "scripts/check_fastmcp_cloud_ready.py",
            "3. Verificación de Preparación para FastMCP Cloud",
        ),
        ("scripts/test_basic_connectivity.py", "4. Test de Conectividad Básica"),
        ("scripts/test_current_config_local.py", "5. Test de Configuración Actual"),
        ("scripts/test_local_api_real.py", "6. Test de Múltiples Configuraciones"),
        ("scripts/test_auth_methods_local.py", "7. Test de Métodos de Autenticación"),
        ("scripts/test_specific_issue.py", "8. Test del Problema Específico"),
        ("scripts/complete_diagnosis.py", "9. Diagnóstico Completo"),
        ("scripts/run_final_diagnosis.py", "10. Diagnóstico Final Completo"),
    ]

    results = {}
    successful_scripts = 0

    print("🎯 Ejecutando todos los tests en secuencia...")

    for script_path, description in test_scripts:
        print(f"\n⏳ Ejecutando: {description}")
        result = run_script(script_path, description)
        results[description] = result

        if result["success"]:
            successful_scripts += 1
            print(f"✅ {description} - EXITOSO")
        else:
            print(f"❌ {description} - FALLÓ")
            if "error" in result:
                print(f"   Error: {result['error']}")

    # Resumen final
    print("\n" + "=" * 140)
    print("📊 RESUMEN FINAL DE TODOS LOS TESTS")
    print("=" * 140)

    total_scripts = len(test_scripts)
    print(f"Scripts ejecutados: {total_scripts}")
    print(f"Scripts exitosos: {successful_scripts}")
    print(f"Scripts fallidos: {total_scripts - successful_scripts}")
    print(f"Tasa de éxito: {(successful_scripts / total_scripts) * 100:.1f}%")

    print(f"\n📋 DETALLE DE RESULTADOS:")
    for description, result in results.items():
        status = "✅" if result["success"] else "❌"
        print(f"   {status} {description}")
        if not result["success"] and "error" in result:
            print(f"      Error: {result['error']}")

    # Análisis y recomendaciones
    print(f"\n💡 ANÁLISIS Y RECOMENDACIONES:")
    print("=" * 140)

    if successful_scripts == 0:
        print("❌ NINGÚN TEST FUE EXITOSO")
        print("\n🔍 Posibles causas:")
        print("   - Credenciales incorrectas")
        print("   - URL base incorrecta")
        print("   - API no disponible")
        print("   - Problemas de conectividad")
        print("   - Método de autenticación incorrecto")
        print("   - Configuración del servidor incorrecta")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Verificar credenciales con TrackHS")
        print("   2. Verificar URL base correcta")
        print("   3. Contactar soporte técnico de TrackHS")
        print("   4. Verificar conectividad de red")
        print("   5. Verificar configuración del servidor")

    elif successful_scripts < total_scripts:
        print(f"⚠️  {successful_scripts}/{total_scripts} TESTS EXITOSOS")
        print("\n🔍 Algunos tests fallaron, pero otros funcionaron")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. Usar la configuración que funcionó")
        print("   2. Revisar los logs de los tests fallidos")
        print("   3. Implementar la solución exitosa en FastMCP Cloud")
        print("   4. Corregir los problemas identificados")

    else:
        print("🎉 TODOS LOS TESTS FUERON EXITOSOS")
        print("\n✅ La configuración funciona correctamente")
        print("\n🛠️  Acciones recomendadas:")
        print("   1. La configuración está lista para FastMCP Cloud")
        print("   2. Desplegar en FastMCP Cloud con la misma configuración")
        print("   3. Monitorear el funcionamiento")
        print("   4. Probar la herramienta search_units")

    # Configuración recomendada para FastMCP Cloud
    if successful_scripts > 0:
        print(f"\n🔧 CONFIGURACIÓN RECOMENDADA PARA FASTMCP CLOUD:")
        print("=" * 140)

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

        print(f"\n🚀 PRÓXIMOS PASOS:")
        print(f"   1. Configurar variables de entorno en FastMCP Cloud")
        print(f"   2. Desplegar el servidor")
        print(f"   3. Probar la herramienta search_units")
        print(f"   4. Monitorear el funcionamiento")

    # Guardar reporte completo
    report_file = f"all_tests_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_scripts": total_scripts,
        "successful_scripts": successful_scripts,
        "failed_scripts": total_scripts - successful_scripts,
        "success_rate": (successful_scripts / total_scripts) * 100,
        "results": results,
        "environment": {
            "python_version": sys.version,
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
            },
            "next_steps": [
                "Configurar variables de entorno en FastMCP Cloud",
                "Desplegar el servidor",
                "Probar la herramienta search_units",
                "Monitorear el funcionamiento",
            ],
        },
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Reporte completo guardado en: {report_file}")

    # Instrucciones finales
    print(f"\n🎯 INSTRUCCIONES FINALES:")
    print("=" * 140)

    if successful_scripts > 0:
        print("✅ Al menos un test fue exitoso")
        print("   - Usa la configuración que funcionó")
        print("   - Configura las variables de entorno en FastMCP Cloud")
        print("   - Despliega el servidor")
        print("   - Prueba la herramienta search_units")
    else:
        print("❌ Ningún test fue exitoso")
        print("   - Revisa las credenciales")
        print("   - Verifica la URL base")
        print("   - Contacta soporte técnico de TrackHS")

    print(f"\n📞 Para soporte adicional:")
    print("   - Incluye el archivo de reporte: {report_file}")
    print("   - Incluye los logs del servidor")
    print("   - Incluye la configuración de variables (sin credenciales)")


if __name__ == "__main__":
    main()
