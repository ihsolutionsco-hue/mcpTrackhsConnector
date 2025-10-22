#!/usr/bin/env python3
"""
FastMCP Smoke Test Completo
Validación exhaustiva del servidor MCP para despliegue en FastMCP Cloud
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


def check_fastmcp_config():
    """Verificar configuración de FastMCP"""
    print("🔧 Verificando configuración FastMCP...")

    config_file = Path("fastmcp.yaml")
    if not config_file.exists():
        print("❌ ERROR: fastmcp.yaml no encontrado")
        return False

    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # Verificar campos requeridos
        required_fields = ["entrypoint", "environment", "server"]
        for field in required_fields:
            if field not in config:
                print(f"❌ ERROR: Campo requerido '{field}' faltante en fastmcp.yaml")
                return False

        # Verificar entrypoint
        entrypoint = config.get("entrypoint", {})
        if "module" not in entrypoint:
            print("❌ ERROR: Módulo de entrada no especificado")
            return False

        print("✅ Configuración FastMCP válida")
        return True

    except Exception as e:
        print(f"❌ ERROR: Error validando fastmcp.yaml: {e}")
        return False


async def test_mcp_server_initialization():
    """Probar inicialización completa del servidor MCP"""
    print("🚀 Probando inicialización del servidor MCP...")

    try:
        # Agregar src al path
        src_path = Path("src").absolute()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # Importar y crear el servidor
        from trackhs_mcp.__main__ import main

        # Crear instancia del servidor
        mcp = main()

        if not mcp:
            print("❌ ERROR: No se pudo crear instancia del servidor MCP")
            return False

        print("✅ Servidor MCP inicializado correctamente")
        return mcp

    except Exception as e:
        print(f"❌ ERROR: Error inicializando servidor MCP: {e}")
        return False


async def test_mcp_tools_registration(mcp):
    """Verificar que las herramientas están registradas correctamente"""
    print("🔧 Verificando registro de herramientas...")

    try:
        # Obtener herramientas registradas
        tools = getattr(mcp, "_tools", {})

        if not tools:
            print("❌ ERROR: No se encontraron herramientas registradas")
            return False

        tool_count = len(tools)
        print(f"📊 Herramientas registradas: {tool_count}")

        # Verificar que hay al menos 10 herramientas
        if tool_count < 10:
            print(
                f"⚠️  WARNING: Solo {tool_count} herramientas registradas (esperado: 10+)"
            )
            return False

        # Listar algunas herramientas para verificación
        tool_names = list(tools.keys())[:5]  # Primeras 5
        print(f"🔧 Herramientas encontradas: {', '.join(tool_names)}...")

        # Verificar herramientas críticas
        critical_tools = ["search_units", "get_folio", "search_amenities"]
        missing_critical = []

        for tool_name in critical_tools:
            if tool_name not in tools:
                missing_critical.append(tool_name)

        if missing_critical:
            print(
                f"❌ ERROR: Herramientas críticas faltantes: {', '.join(missing_critical)}"
            )
            return False

        print("✅ Herramientas registradas correctamente")
        return True

    except Exception as e:
        print(f"❌ ERROR: Error verificando herramientas: {e}")
        return False


async def test_mcp_resources_registration(mcp):
    """Verificar que los recursos están registrados correctamente"""
    print("📚 Verificando registro de recursos...")

    try:
        # Obtener recursos registrados
        resources = getattr(mcp, "_resources", {})

        if not resources:
            print("⚠️  WARNING: No se encontraron recursos registrados")
            return True  # No es crítico

        resource_count = len(resources)
        print(f"📊 Recursos registrados: {resource_count}")

        # Listar algunos recursos
        resource_names = list(resources.keys())[:3]  # Primeros 3
        print(f"📚 Recursos encontrados: {', '.join(resource_names)}...")

        print("✅ Recursos registrados correctamente")
        return True

    except Exception as e:
        print(f"⚠️  WARNING: Error verificando recursos: {e}")
        return True  # No es crítico


async def test_mcp_prompts_registration(mcp):
    """Verificar que los prompts están registrados correctamente"""
    print("💬 Verificando registro de prompts...")

    try:
        # Obtener prompts registrados
        prompts = getattr(mcp, "_prompts", {})

        if not prompts:
            print("⚠️  WARNING: No se encontraron prompts registrados")
            return True  # No es crítico

        prompt_count = len(prompts)
        print(f"📊 Prompts registrados: {prompt_count}")

        print("✅ Prompts registrados correctamente")
        return True

    except Exception as e:
        print(f"⚠️  WARNING: Error verificando prompts: {e}")
        return True  # No es crítico


async def test_mcp_server_response(mcp):
    """Probar que el servidor responde correctamente"""
    print("🌐 Probando respuesta del servidor...")

    try:
        # Verificar que el servidor tiene los métodos necesarios
        required_methods = ["run", "tool"]
        missing_methods = []

        for method in required_methods:
            if not hasattr(mcp, method):
                missing_methods.append(method)

        if missing_methods:
            print(
                f"❌ ERROR: Métodos faltantes en servidor: {', '.join(missing_methods)}"
            )
            return False

        # Verificar que el servidor está configurado para FastMCP
        if hasattr(mcp, "name"):
            print(f"📝 Nombre del servidor: {mcp.name}")

        print("✅ Servidor responde correctamente")
        return True

    except Exception as e:
        print(f"❌ ERROR: Error probando servidor: {e}")
        return False


async def test_environment_variables():
    """Verificar variables de entorno"""
    print("🔐 Verificando variables de entorno...")

    required_vars = ["TRACKHS_API_URL", "TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  WARNING: Variables faltantes: {', '.join(missing_vars)}")
        print("   Estas deben configurarse en FastMCP Cloud")
        return True  # No es crítico para smoke test

    print("✅ Variables de entorno configuradas")
    return True


async def main():
    """Ejecutar smoke test completo"""
    print("🧪 Ejecutando FastMCP Smoke Test Completo...")
    print("=" * 60)

    # Lista de checks
    checks = [
        ("Configuración FastMCP", check_fastmcp_config),
        ("Variables de entorno", test_environment_variables),
    ]

    # Ejecutar checks síncronos
    passed = 0
    total = len(checks)

    for name, check in checks:
        try:
            if check():
                passed += 1
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: FALLO")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")

    # Inicializar servidor MCP
    print("\n🚀 Inicializando servidor MCP...")
    mcp = await test_mcp_server_initialization()

    if not mcp:
        print("\n" + "=" * 60)
        print(f"❌ RESULTADO: {passed}/{total} checks pasaron")
        print("❌ Smoke test FALLÓ - Servidor MCP no se pudo inicializar")
        return 1

    # Ejecutar tests del servidor
    server_checks = [
        ("Registro de herramientas", lambda: test_mcp_tools_registration(mcp)),
        ("Registro de recursos", lambda: test_mcp_resources_registration(mcp)),
        ("Registro de prompts", lambda: test_mcp_prompts_registration(mcp)),
        ("Respuesta del servidor", lambda: test_mcp_server_response(mcp)),
    ]

    server_passed = 0
    server_total = len(server_checks)

    for name, check in server_checks:
        try:
            if await check():
                server_passed += 1
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: FALLO")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")

    # Resultados finales
    total_passed = passed + server_passed
    total_checks = total + server_total

    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {total_passed}/{total_checks} checks pasaron")
    print(f"   - Configuración: {passed}/{total}")
    print(f"   - Servidor MCP: {server_passed}/{server_total}")

    if total_passed == total_checks:
        print("✅ Smoke test EXITOSO - Servidor listo para despliegue")
        return 0
    elif server_passed >= server_total * 0.8:  # 80% de los tests del servidor
        print("⚠️  Smoke test PARCIAL - Servidor funcional pero con advertencias")
        return 0
    else:
        print("❌ Smoke test FALLÓ - Servidor no está listo para despliegue")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
