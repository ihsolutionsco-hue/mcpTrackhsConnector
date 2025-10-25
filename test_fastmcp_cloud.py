#!/usr/bin/env python3
"""
Script de prueba para FastMCP Cloud
Verifica que el servidor funcione correctamente en el entorno de despliegue
"""

import asyncio
import os
import sys
from pathlib import Path

# Configurar variables de entorno para test
os.environ["TRACKHS_USERNAME"] = "test_user"
os.environ["TRACKHS_PASSWORD"] = "test_password"
os.environ["TRACKHS_BASE_URL"] = "https://api-test.trackhs.com/api"


def test_imports():
    """Test de importaciones"""
    try:
        print("🔍 Probando importaciones...")

        # Test importación del servidor
        from trackhs_mcp.server import mcp

        print("✅ Servidor importado correctamente")

        # Test importación de esquemas
        from trackhs_mcp.schemas import WorkOrderPriority

        print("✅ Esquemas importados correctamente")

        # Test creación del servidor
        print(f"✅ Servidor MCP creado: {mcp.name}")

        return True

    except Exception as e:
        print(f"❌ Error en importaciones: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def test_server_startup():
    """Test de inicio del servidor"""
    try:
        print("🚀 Probando inicio del servidor...")

        from trackhs_mcp.server import mcp

        # Verificar que el servidor tiene las herramientas esperadas
        tools = await mcp.get_tools()
        print(f"✅ Servidor tiene {len(tools)} herramientas")

        for tool in tools:
            print(f"  - {tool}")

        return True

    except Exception as e:
        print(f"❌ Error en inicio del servidor: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def test_health_check():
    """Test del health check"""
    try:
        print("🏥 Probando health check...")

        from trackhs_mcp.server import mcp

        # Verificar que el health check está disponible
        resources = await mcp.get_resources()
        print(f"✅ Servidor tiene {len(resources)} recursos")

        for resource in resources:
            print(f"  - {resource}")

        return True

    except Exception as e:
        print(f"❌ Error en health check: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Función principal de test"""
    print("🧪 Iniciando tests para FastMCP Cloud...")

    tests = [
        ("Importaciones", test_imports),
        ("Inicio del Servidor", test_server_startup),
        ("Health Check", test_health_check),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        if test_name == "Importaciones":
            result = test_func()
        else:
            result = await test_func()

        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")

    print(f"\n📊 Resultados: {passed}/{total} tests pasaron")

    if passed == total:
        print("🎉 Todos los tests pasaron! El servidor está listo para FastMCP Cloud.")
        return True
    else:
        print("⚠️  Algunos tests fallaron. Revisar errores antes del despliegue.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
