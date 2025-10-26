#!/usr/bin/env python3
"""
Script para verificar la configuración del servidor MCP
Verifica que todos los archivos y configuraciones estén correctos
"""

import json
import os
import sys
from typing import Any, Dict, List


def check_file_exists(file_path: str, description: str) -> bool:
    """Verificar que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (no encontrado)")
        return False


def check_file_content(
    file_path: str, required_content: List[str], description: str
) -> bool:
    """Verificar que un archivo contiene contenido requerido"""
    if not os.path.exists(file_path):
        print(f"❌ {description}: {file_path} (no encontrado)")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        missing_content = []
        for required in required_content:
            if required not in content:
                missing_content.append(required)

        if missing_content:
            print(
                f"❌ {description}: {file_path} (falta contenido: {', '.join(missing_content)})"
            )
            return False
        else:
            print(f"✅ {description}: {file_path}")
            return True

    except Exception as e:
        print(f"❌ {description}: {file_path} (error leyendo: {str(e)})")
        return False


def check_json_file(file_path: str, description: str) -> bool:
    """Verificar que un archivo JSON es válido"""
    if not os.path.exists(file_path):
        print(f"❌ {description}: {file_path} (no encontrado)")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"✅ {description}: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {description}: {file_path} (JSON inválido: {str(e)})")
        return False
    except Exception as e:
        print(f"❌ {description}: {file_path} (error: {str(e)})")
        return False


def check_environment_variables() -> Dict[str, bool]:
    """Verificar variables de entorno"""
    print("\n🔍 Verificando variables de entorno...")

    variables = {
        "TRACKHS_USERNAME": os.getenv("TRACKHS_USERNAME"),
        "TRACKHS_PASSWORD": os.getenv("TRACKHS_PASSWORD"),
        "TRACKHS_API_URL": os.getenv("TRACKHS_API_URL"),
    }

    results = {}
    for var, value in variables.items():
        if value:
            print(
                f"✅ {var}: {value[:3]}***" if len(value) > 3 else f"✅ {var}: {value}"
            )
            results[var] = True
        else:
            print(f"❌ {var}: No configurada")
            results[var] = False

    return results


def check_server_structure() -> Dict[str, bool]:
    """Verificar estructura del servidor"""
    print("\n🔍 Verificando estructura del servidor...")

    required_files = [
        ("src/trackhs_mcp/__init__.py", "Archivo __init__.py del paquete"),
        ("src/trackhs_mcp/__main__.py", "Archivo __main__.py del servidor"),
        ("src/trackhs_mcp/server.py", "Archivo server.py principal"),
        ("src/trackhs_mcp/schemas.py", "Archivo schemas.py"),
        ("src/trackhs_mcp/exceptions.py", "Archivo exceptions.py"),
        ("src/trackhs_mcp/middleware.py", "Archivo middleware.py"),
        ("fastmcp.json", "Archivo de configuración FastMCP"),
        ("requirements.txt", "Archivo de dependencias"),
        ("pyproject.toml", "Archivo de configuración del proyecto"),
    ]

    results = {}
    for file_path, description in required_files:
        results[file_path] = check_file_exists(file_path, description)

    return results


def check_server_content() -> Dict[str, bool]:
    """Verificar contenido del servidor"""
    print("\n🔍 Verificando contenido del servidor...")

    content_checks = [
        (
            "src/trackhs_mcp/__main__.py",
            ["from .server import mcp"],
            "Importación del servidor",
        ),
        (
            "src/trackhs_mcp/server.py",
            ["FastMCP", "search_units"],
            "Configuración del servidor",
        ),
        ("fastmcp.json", ["source", "environment"], "Configuración FastMCP"),
        (
            "requirements.txt",
            ["fastmcp", "httpx", "pydantic"],
            "Dependencias requeridas",
        ),
    ]

    results = {}
    for file_path, required_content, description in content_checks:
        results[file_path] = check_file_content(
            file_path, required_content, description
        )

    return results


def check_json_configs() -> Dict[str, bool]:
    """Verificar configuraciones JSON"""
    print("\n🔍 Verificando configuraciones JSON...")

    json_files = [
        ("fastmcp.json", "Configuración FastMCP"),
        ("pyproject.toml", "Configuración del proyecto"),
    ]

    results = {}
    for file_path, description in json_files:
        results[file_path] = check_json_file(file_path, description)

    return results


def check_dependencies() -> Dict[str, bool]:
    """Verificar dependencias"""
    print("\n🔍 Verificando dependencias...")

    dependencies = [
        ("httpx", "Cliente HTTP"),
        ("fastmcp", "Framework FastMCP"),
        ("pydantic", "Validación de datos"),
        ("python-dotenv", "Variables de entorno"),
    ]

    results = {}
    for dep, description in dependencies:
        try:
            __import__(dep)
            print(f"✅ {description}: {dep}")
            results[dep] = True
        except ImportError:
            print(f"❌ {description}: {dep} (no instalado)")
            results[dep] = False

    return results


def generate_recommendations(
    env_results: Dict[str, bool],
    structure_results: Dict[str, bool],
    content_results: Dict[str, bool],
    json_results: Dict[str, bool],
    dep_results: Dict[str, bool],
) -> None:
    """Generar recomendaciones basadas en los resultados"""
    print("\n" + "=" * 80)
    print("💡 RECOMENDACIONES")
    print("=" * 80)

    # Verificar variables de entorno
    if not env_results.get("TRACKHS_USERNAME") or not env_results.get(
        "TRACKHS_PASSWORD"
    ):
        print("❌ Variables de entorno no configuradas")
        print("   Configure TRACKHS_USERNAME y TRACKHS_PASSWORD")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")

    # Verificar estructura del servidor
    missing_files = [file for file, exists in structure_results.items() if not exists]
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        print("   Verifique que todos los archivos estén presentes")

    # Verificar contenido del servidor
    content_issues = [file for file, valid in content_results.items() if not valid]
    if content_issues:
        print(f"❌ Problemas de contenido: {', '.join(content_issues)}")
        print("   Verifique que los archivos tengan el contenido correcto")

    # Verificar configuraciones JSON
    json_issues = [file for file, valid in json_results.items() if not valid]
    if json_issues:
        print(f"❌ Problemas de JSON: {', '.join(json_issues)}")
        print("   Verifique que los archivos JSON sean válidos")

    # Verificar dependencias
    missing_deps = [dep for dep, installed in dep_results.items() if not installed]
    if missing_deps:
        print(f"❌ Dependencias faltantes: {', '.join(missing_deps)}")
        print("   Instale las dependencias: pip install -r requirements.txt")

    # Recomendaciones generales
    if (
        all(env_results.values())
        and all(structure_results.values())
        and all(content_results.values())
        and all(json_results.values())
        and all(dep_results.values())
    ):
        print("✅ ¡Todas las verificaciones pasaron!")
        print("   La configuración del servidor está lista")
        print("   Puede proceder con el despliegue en FastMCP Cloud")
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("   Corrija los problemas antes de desplegar")
        print("   Ejecute los diagnósticos para verificar la configuración")


def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DEL SERVIDOR MCP")
    print("=" * 80)
    print("Este script verifica que la configuración del servidor MCP")
    print("esté correcta antes de desplegar en FastMCP Cloud")
    print("=" * 80)

    # Ejecutar verificaciones
    env_results = check_environment_variables()
    structure_results = check_server_structure()
    content_results = check_server_content()
    json_results = check_json_configs()
    dep_results = check_dependencies()

    # Resumen de resultados
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 80)

    total_checks = (
        len(env_results)
        + len(structure_results)
        + len(content_results)
        + len(json_results)
        + len(dep_results)
    )
    passed_checks = (
        sum(env_results.values())
        + sum(structure_results.values())
        + sum(content_results.values())
        + sum(json_results.values())
        + sum(dep_results.values())
    )

    print(f"Verificaciones totales: {total_checks}")
    print(f"Verificaciones exitosas: {passed_checks}")
    print(f"Verificaciones fallidas: {total_checks - passed_checks}")
    print(f"Tasa de éxito: {(passed_checks / total_checks) * 100:.1f}%")

    # Generar recomendaciones
    generate_recommendations(
        env_results, structure_results, content_results, json_results, dep_results
    )

    # Guardar resultados
    results_file = "server_config_verification.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": os.popen("date").read().strip(),
                "total_checks": total_checks,
                "passed_checks": passed_checks,
                "failed_checks": total_checks - passed_checks,
                "success_rate": (passed_checks / total_checks) * 100,
                "environment": env_results,
                "structure": structure_results,
                "content": content_results,
                "json": json_results,
                "dependencies": dep_results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n📄 Resultados guardados en: {results_file}")


if __name__ == "__main__":
    main()
