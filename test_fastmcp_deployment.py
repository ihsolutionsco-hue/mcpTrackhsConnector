#!/usr/bin/env python3
"""
Test de despliegue para FastMCP Cloud
Simula exactamente lo que hace FastMCP Cloud durante el build
"""

import os
import subprocess
import sys
from pathlib import Path

# Configurar variables de entorno
os.environ["TRACKHS_USERNAME"] = "test_user"
os.environ["TRACKHS_PASSWORD"] = "test_password"
os.environ["TRACKHS_BASE_URL"] = "https://api-test.trackhs.com/api"


def test_fastmcp_inspect():
    """Test que simula el comando fastmcp inspect de FastMCP Cloud"""
    try:
        print("🔍 Ejecutando fastmcp inspect...")

        # Simular el comando que ejecuta FastMCP Cloud
        cmd = [
            "fastmcp",
            "inspect",
            "-f",
            "fastmcp",
            "-o",
            "/tmp/server-info.json",
            "src/trackhs_mcp/__main__.py",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

        if result.returncode == 0:
            print("✅ fastmcp inspect exitoso")
            print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ fastmcp inspect falló: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error ejecutando fastmcp inspect: {str(e)}")
        return False


def test_server_import():
    """Test de importación del servidor"""
    try:
        print("🔍 Probando importación del servidor...")

        # Agregar src al path
        src_dir = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_dir))

        # Importar el servidor
        from trackhs_mcp.server import mcp

        print(f"✅ Servidor importado: {mcp.name}")

        return True

    except Exception as e:
        print(f"❌ Error importando servidor: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_entry_point():
    """Test del punto de entrada"""
    try:
        print("🔍 Probando punto de entrada...")

        # Ejecutar el punto de entrada
        entry_point = Path(__file__).parent / "src" / "trackhs_mcp" / "__main__.py"

        # Simular ejecución del entry point
        import importlib.util

        spec = importlib.util.spec_from_file_location("__main__", entry_point)
        module = importlib.util.module_from_spec(spec)

        # Agregar src al path antes de ejecutar
        src_dir = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_dir))

        spec.loader.exec_module(module)

        print("✅ Punto de entrada ejecutado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error en punto de entrada: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Función principal de test"""
    print("🧪 Test de despliegue para FastMCP Cloud...")

    tests = [
        ("Importación del Servidor", test_server_import),
        ("Punto de Entrada", test_entry_point),
        ("FastMCP Inspect", test_fastmcp_inspect),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        if test_func():
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
    success = main()
    sys.exit(0 if success else 1)
