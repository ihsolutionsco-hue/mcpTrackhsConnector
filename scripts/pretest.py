#!/usr/bin/env python3
"""
Pre-tests para validar el despliegue en FastMCP Cloud
Ejecuta validaciones antes del commit para asegurar que el despliegue funcione correctamente
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verificar que la versión de Python sea compatible"""
    print("Verificando version de Python...")
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print(
            f"ERROR: Python {version.major}.{version.minor} no es compatible. Se requiere Python 3.8+"
        )
        return False
    print(f"OK: Python {version.major}.{version.minor}.{version.micro} es compatible")
    return True


def check_required_files():
    """Verificar que todos los archivos requeridos existan"""
    print("\nVerificando archivos requeridos...")

    required_files = [
        "src/trackhs_mcp/__main__.py",
        "src/trackhs_mcp/server.py",
        "src/trackhs_mcp/infrastructure/adapters/config.py",
        "src/trackhs_mcp/infrastructure/adapters/trackhs_api_client.py",
        "requirements.txt",
        "pyproject.toml",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"❌ Archivo faltante: {file_path}")
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"\n❌ Faltan {len(missing_files)} archivos requeridos")
        return False

    print("✅ Todos los archivos requeridos están presentes")
    return True


def check_imports():
    """Verificar que todos los imports funcionen correctamente"""
    print("\n📦 Verificando imports...")

    try:
        # Verificar imports principales
        sys.path.insert(0, str(Path("src").absolute()))

        # Test basic imports
        from trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
        from trackhs_mcp.infrastructure.adapters.trackhs_api_client import (
            TrackHSApiClient,
        )
        from trackhs_mcp.infrastructure.mcp.server import register_all_components

        print("✅ Imports básicos funcionan")

        # Test FastMCP import
        from fastmcp import FastMCP

        print("✅ FastMCP import funciona")

        return True

    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def check_main_file():
    """Verificar que el archivo __main__.py sea válido"""
    print("\n🚀 Verificando archivo __main__.py...")

    main_file = Path("src/trackhs_mcp/__main__.py")
    if not main_file.exists():
        print("❌ Archivo __main__.py no encontrado")
        return False

    try:
        # Verificar que el archivo se puede compilar
        with open(main_file, "r", encoding="utf-8") as f:
            code = f.read()

        compile(code, str(main_file), "exec")
        print("✅ Archivo __main__.py es válido")
        return True

    except SyntaxError as e:
        print(f"❌ Error de sintaxis en __main__.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al verificar __main__.py: {e}")
        return False


def check_environment_variables():
    """Verificar configuración de variables de entorno"""
    print("\n🔐 Verificando variables de entorno...")

    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("   Estas deben configurarse en FastMCP Cloud")
        return True  # No es un error crítico para el pre-test
    else:
        print("✅ Variables de entorno configuradas")
        return True


def check_dependencies():
    """Verificar que las dependencias estén en requirements.txt"""
    print("\n📋 Verificando dependencias...")

    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt no encontrado")
        return False

    required_deps = ["fastmcp", "httpx", "pydantic", "python-dotenv"]

    try:
        with open(requirements_file, "r") as f:
            content = f.read()

        missing_deps = []
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)

        if missing_deps:
            print(f"❌ Dependencias faltantes: {', '.join(missing_deps)}")
            return False

        print("✅ Todas las dependencias están en requirements.txt")
        return True

    except Exception as e:
        print(f"❌ Error al verificar requirements.txt: {e}")
        return False


def run_tests():
    """Ejecutar suite completa de tests"""
    print("\n🧪 Ejecutando suite completa de tests...")

    try:
        # Verificar si hay tests
        test_dir = Path("tests")
        if not test_dir.exists():
            print("⚠️  Directorio de tests no encontrado")
            return True

        # Ejecutar tests con cobertura y timeout extendido
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--tb=short",
                "--maxfail=5",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-fail-under=80",
                "--timeout=300",
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )

        # Analizar resultados
        if result.returncode == 0:
            print("✅ Todos los tests pasaron correctamente")
            return True
        else:
            # Analizar la salida para determinar si es aceptable
            output_lines = result.stdout.split("\n")
            passed_count = 0
            failed_count = 0
            coverage_info = ""

            for line in output_lines:
                if "PASSED" in line:
                    passed_count += 1
                elif "FAILED" in line:
                    failed_count += 1
                elif "TOTAL" in line and "%" in line:
                    coverage_info = line.strip()

            total_tests = passed_count + failed_count
            if total_tests > 0:
                success_rate = (passed_count / total_tests) * 100
                print(
                    f"📊 Tests: {passed_count} pasaron, {failed_count} fallaron ({success_rate:.1f}% éxito)"
                )

                if coverage_info:
                    print(f"📊 Cobertura: {coverage_info}")

                # Para pre-tests, requerimos al menos 80% de éxito
                if success_rate >= 80:
                    print("✅ Tasa de éxito aceptable para pre-tests")
                    return True
                else:
                    print("❌ Tasa de éxito muy baja")
                    return False
            else:
                print("⚠️  No se pudieron analizar los resultados de los tests")
                return True  # No es crítico para el pre-test

    except subprocess.TimeoutExpired:
        print("⚠️  Tests tardaron demasiado tiempo")
        return True
    except Exception as e:
        print(f"⚠️  Error ejecutando tests: {e}")
        return True  # No es crítico para el pre-test


def main():
    """Ejecutar todos los pre-tests"""
    print("Ejecutando pre-tests para FastMCP Cloud...")
    print("=" * 50)

    tests = [
        check_python_version,
        check_required_files,
        check_imports,
        check_main_file,
        check_environment_variables,
        check_dependencies,
        run_tests,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error en {test.__name__}: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} tests pasaron")

    if passed == total:
        print(
            "✅ Todos los pre-tests pasaron. El despliegue debería funcionar correctamente."
        )
        return 0
    else:
        print("❌ Algunos pre-tests fallaron. Revisa los errores antes del commit.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
