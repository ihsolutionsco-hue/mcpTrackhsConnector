#!/usr/bin/env python3
"""
Script para ejecutar tests de protocolo MCP
Enfoque: Ejecutar todos los tests de protocolo MCP con reportes detallados
"""

import os
import subprocess
import sys
from pathlib import Path


def run_mcp_protocol_tests():
    """Ejecuta todos los tests de protocolo MCP"""
    print("🧪 Ejecutando Tests de Protocolo MCP...")
    print("=" * 50)

    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)

    # Comando para ejecutar tests de protocolo MCP
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/mcp_protocol/",
        "-v",  # Verbose
        "--tb=short",  # Traceback corto
        "--color=yes",  # Colores
        "--durations=10",  # Mostrar los 10 tests más lentos
        "--cov=src/trackhs_mcp",  # Cobertura
        "--cov-report=term-missing",  # Reporte de cobertura
        "--cov-report=html:htmlcov_mcp_protocol",  # Reporte HTML
    ]

    try:
        # Ejecutar tests
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        print("✅ Tests de Protocolo MCP ejecutados exitosamente!")
        print("\n📊 Resumen de Resultados:")
        print(result.stdout)

        return True

    except subprocess.CalledProcessError as e:
        print("❌ Error ejecutando tests de protocolo MCP:")
        print(f"Código de salida: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def run_specific_test_files():
    """Ejecuta tests específicos de protocolo MCP"""
    test_files = [
        "tests/mcp_protocol/test_tools_registration.py",
        "tests/mcp_protocol/test_resources_registration.py",
        "tests/mcp_protocol/test_prompts_registration.py",
        "tests/mcp_protocol/test_schema_validation.py",
        "tests/mcp_protocol/test_complete_integration.py",
    ]

    print("🔍 Ejecutando tests específicos de protocolo MCP...")
    print("=" * 50)

    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📁 Ejecutando: {test_file}")
            cmd = ["python", "-m", "pytest", test_file, "-v", "--tb=short"]

            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"✅ {test_file} - PASÓ")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"❌ {test_file} - FALLÓ")
                print(f"Error: {e.stderr}")
        else:
            print(f"⚠️  {test_file} - NO ENCONTRADO")


def run_with_coverage():
    """Ejecuta tests con reporte de cobertura detallado"""
    print("📊 Ejecutando tests con cobertura detallada...")
    print("=" * 50)

    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/mcp_protocol/",
        "-v",
        "--cov=src/trackhs_mcp",
        "--cov-report=html:htmlcov_mcp_protocol",
        "--cov-report=xml:coverage_mcp_protocol.xml",
        "--cov-report=term-missing",
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Tests con cobertura ejecutados exitosamente!")
        print("\n📊 Reporte de Cobertura:")
        print(result.stdout)

        # Verificar si se generó el reporte HTML
        html_report = Path("htmlcov_mcp_protocol/index.html")
        if html_report.exists():
            print(f"\n🌐 Reporte HTML generado: {html_report.absolute()}")

        return True

    except subprocess.CalledProcessError as e:
        print("❌ Error ejecutando tests con cobertura:")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Función principal"""
    print("🚀 TrackHS MCP Protocol Tests Runner")
    print("=" * 50)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "all":
            success = run_mcp_protocol_tests()
        elif command == "specific":
            run_specific_test_files()
        elif command == "coverage":
            success = run_with_coverage()
        else:
            print(f"❌ Comando desconocido: {command}")
            print("Comandos disponibles: all, specific, coverage")
            sys.exit(1)
    else:
        # Por defecto, ejecutar todos los tests
        success = run_mcp_protocol_tests()

    if success:
        print("\n🎉 Tests de Protocolo MCP completados exitosamente!")
        sys.exit(0)
    else:
        print("\n💥 Tests de Protocolo MCP fallaron!")
        sys.exit(1)


if __name__ == "__main__":
    main()
