#!/usr/bin/env python3
"""
Script para verificar que el servidor esté listo para FastMCP Cloud
Verifica que todos los componentes estén configurados correctamente
"""

import json
import os
import sys
from typing import Any, Dict, List


def check_fastmcp_json() -> bool:
    """Verificar configuración de fastmcp.json"""
    print("\n🔍 Verificando fastmcp.json...")

    if not os.path.exists("fastmcp.json"):
        print("❌ fastmcp.json no encontrado")
        return False

    try:
        with open("fastmcp.json", "r") as f:
            config = json.load(f)

        # Verificar campos requeridos
        required_fields = ["source", "environment", "server"]
        missing_fields = [field for field in required_fields if field not in config]

        if missing_fields:
            print(f"❌ fastmcp.json faltan campos: {', '.join(missing_fields)}")
            return False

        # Verificar source
        source = config.get("source", {})
        if "path" not in source:
            print("❌ fastmcp.json: source.path no encontrado")
            return False

        expected_path = "src/trackhs_mcp/__main__.py:mcp"
        if source["path"] != expected_path:
            print(
                f"❌ fastmcp.json: source.path incorrecto. Esperado: {expected_path}, Actual: {source['path']}"
            )
            return False

        # Verificar environment
        environment = config.get("environment", {})
        if "python" not in environment:
            print("❌ fastmcp.json: environment.python no encontrado")
            return False

        if "requirements" not in environment:
            print("❌ fastmcp.json: environment.requirements no encontrado")
            return False

        # Verificar server
        server = config.get("server", {})
        if "name" not in server:
            print("❌ fastmcp.json: server.name no encontrado")
            return False

        print("✅ fastmcp.json configurado correctamente")
        return True

    except json.JSONDecodeError:
        print("❌ fastmcp.json no es JSON válido")
        return False
    except Exception as e:
        print(f"❌ Error leyendo fastmcp.json: {str(e)}")
        return False


def check_main_file() -> bool:
    """Verificar archivo __main__.py"""
    print("\n🔍 Verificando __main__.py...")

    main_file = "src/trackhs_mcp/__main__.py"
    if not os.path.exists(main_file):
        print(f"❌ {main_file} no encontrado")
        return False

    try:
        with open(main_file, "r") as f:
            content = f.read()

        # Verificar importación del servidor
        if "from .server import mcp" not in content:
            print("❌ __main__.py: importación del servidor no encontrada")
            return False

        # Verificar que mcp esté disponible
        if "mcp" not in content:
            print("❌ __main__.py: mcp no encontrado")
            return False

        print("✅ __main__.py configurado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error leyendo __main__.py: {str(e)}")
        return False


def check_server_file() -> bool:
    """Verificar archivo server.py"""
    print("\n🔍 Verificando server.py...")

    server_file = "src/trackhs_mcp/server.py"
    if not os.path.exists(server_file):
        print(f"❌ {server_file} no encontrado")
        return False

    try:
        with open(server_file, "r") as f:
            content = f.read()

        # Verificar componentes requeridos
        required_components = [
            "FastMCP",
            "search_units",
            "search_reservations",
            "get_reservation",
            "search_amenities",
            "get_folio",
            "create_maintenance_work_order",
            "create_housekeeping_work_order",
        ]

        missing_components = [
            comp for comp in required_components if comp not in content
        ]

        if missing_components:
            print(f"❌ server.py faltan componentes: {', '.join(missing_components)}")
            return False

        print("✅ server.py configurado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error leyendo server.py: {str(e)}")
        return False


def check_requirements() -> bool:
    """Verificar requirements.txt"""
    print("\n🔍 Verificando requirements.txt...")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt no encontrado")
        return False

    try:
        with open("requirements.txt", "r") as f:
            content = f.read()

        # Verificar dependencias requeridas
        required_deps = ["fastmcp", "httpx", "pydantic", "python-dotenv"]

        missing_deps = [dep for dep in required_deps if dep not in content]

        if missing_deps:
            print(f"❌ requirements.txt faltan dependencias: {', '.join(missing_deps)}")
            return False

        print("✅ requirements.txt configurado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {str(e)}")
        return False


def check_environment_variables() -> bool:
    """Verificar variables de entorno"""
    print("\n🔍 Verificando variables de entorno...")

    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username:
        print("❌ TRACKHS_USERNAME no configurada")
        return False

    if not password:
        print("❌ TRACKHS_PASSWORD no configurada")
        return False

    print("✅ Variables de entorno configuradas")
    return True


def check_directory_structure() -> bool:
    """Verificar estructura de directorios"""
    print("\n🔍 Verificando estructura de directorios...")

    required_dirs = ["src", "src/trackhs_mcp", "docs", "scripts"]

    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]

    if missing_dirs:
        print(f"❌ Directorios faltantes: {', '.join(missing_dirs)}")
        return False

    print("✅ Estructura de directorios correcta")
    return True


def check_python_files() -> bool:
    """Verificar archivos Python"""
    print("\n🔍 Verificando archivos Python...")

    required_files = [
        "src/trackhs_mcp/__init__.py",
        "src/trackhs_mcp/__main__.py",
        "src/trackhs_mcp/server.py",
        "src/trackhs_mcp/schemas.py",
        "src/trackhs_mcp/exceptions.py",
        "src/trackhs_mcp/middleware.py",
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"❌ Archivos Python faltantes: {', '.join(missing_files)}")
        return False

    print("✅ Archivos Python presentes")
    return True


def generate_fastmcp_cloud_instructions() -> None:
    """Generar instrucciones para FastMCP Cloud"""
    print("\n" + "=" * 80)
    print("🚀 INSTRUCCIONES PARA FASTMCP CLOUD")
    print("=" * 80)

    print("1. 🔧 Configurar Variables de Entorno:")
    print("   - TRACKHS_USERNAME=tu_usuario")
    print("   - TRACKHS_PASSWORD=tu_password")
    print("   - TRACKHS_API_URL=https://ihmvacations.trackhs.com/api (opcional)")

    print("\n2. 📁 Subir Archivos:")
    print("   - Subir todo el directorio del proyecto")
    print("   - Asegurar que fastmcp.json esté en la raíz")
    print("   - Asegurar que src/trackhs_mcp/__main__.py exista")

    print("\n3. 🚀 Desplegar:")
    print("   - Usar la configuración de fastmcp.json")
    print("   - Desplegar el servidor")
    print("   - Verificar que esté funcionando")

    print("\n4. 🔍 Probar:")
    print("   - Probar la herramienta search_units")
    print("   - Verificar que funcione correctamente")
    print("   - Monitorear el funcionamiento")

    print("\n5. 📞 Soporte:")
    print("   - Si hay problemas, ejecutar diagnósticos")
    print("   - Contactar soporte técnico si es necesario")


def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE PREPARACIÓN PARA FASTMCP CLOUD")
    print("=" * 80)
    print("Este script verifica que el servidor esté listo")
    print("para desplegar en FastMCP Cloud")
    print("=" * 80)

    # Ejecutar verificaciones
    checks = [
        ("fastmcp.json", check_fastmcp_json),
        ("__main__.py", check_main_file),
        ("server.py", check_server_file),
        ("requirements.txt", check_requirements),
        ("Variables de entorno", check_environment_variables),
        ("Estructura de directorios", check_directory_structure),
        ("Archivos Python", check_python_files),
    ]

    results = {}
    passed_checks = 0

    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results[check_name] = result
            if result:
                passed_checks += 1
        except Exception as e:
            print(f"❌ Error en {check_name}: {str(e)}")
            results[check_name] = False

    # Resumen de resultados
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 80)

    total_checks = len(checks)
    print(f"Verificaciones totales: {total_checks}")
    print(f"Verificaciones exitosas: {passed_checks}")
    print(f"Verificaciones fallidas: {total_checks - passed_checks}")
    print(f"Tasa de éxito: {(passed_checks / total_checks) * 100:.1f}%")

    print(f"\n📋 DETALLE DE RESULTADOS:")
    for check_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")

    # Generar instrucciones
    if passed_checks == total_checks:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        print("El servidor está listo para FastMCP Cloud")
        generate_fastmcp_cloud_instructions()
    else:
        print(f"\n⚠️  {total_checks - passed_checks} verificaciones fallaron")
        print("Corrija los problemas antes de desplegar en FastMCP Cloud")

        print(f"\n🔧 PROBLEMAS A CORREGIR:")
        for check_name, result in results.items():
            if not result:
                print(f"   - {check_name}")

    # Guardar resultados
    results_file = "fastmcp_cloud_readiness.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": os.popen("date").read().strip(),
                "total_checks": total_checks,
                "passed_checks": passed_checks,
                "failed_checks": total_checks - passed_checks,
                "success_rate": (passed_checks / total_checks) * 100,
                "results": results,
                "ready_for_fastmcp_cloud": passed_checks == total_checks,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n📄 Resultados guardados en: {results_file}")


if __name__ == "__main__":
    main()
