#!/usr/bin/env python3
"""
Script para ejecutar tests de search_units con diferentes configuraciones
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any


class TestRunner:
    """Runner para tests de search_units"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_dir = self.project_root / "tests"

    def run_tests(
        self,
        test_type: str = "all",
        verbose: bool = False,
        coverage: bool = False,
        parallel: bool = False,
        slow_tests: bool = False,
    ) -> int:
        """Ejecutar tests con configuración específica"""

        # Configurar variables de entorno
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root / "src")

        # Construir comando pytest
        cmd = ["python", "-m", "pytest"]

        # Agregar opciones de verbosidad
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        # Agregar cobertura si se solicita
        if coverage:
            cmd.extend(
                ["--cov=src/trackhs_mcp", "--cov-report=html", "--cov-report=term"]
            )

        # Agregar paralelización si se solicita
        if parallel:
            cmd.extend(["-n", "auto"])

        # Seleccionar tests basado en tipo
        if test_type == "unit":
            cmd.append("tests/test_search_units_unit.py")
        elif test_type == "integration":
            cmd.append("tests/test_search_units_integration.py")
        elif test_type == "api":
            cmd.append("tests/test_search_units_api_real.py")
        elif test_type == "e2e":
            cmd.append("tests/test_search_units_e2e.py")
        elif test_type == "all":
            cmd.extend(
                [
                    "tests/test_search_units_unit.py",
                    "tests/test_search_units_integration.py",
                ]
            )
            if slow_tests:
                cmd.extend(
                    [
                        "tests/test_search_units_api_real.py",
                        "tests/test_search_units_e2e.py",
                    ]
                )
        else:
            print(f"❌ Tipo de test inválido: {test_type}")
            return 1

        # Agregar marcadores
        if not slow_tests:
            cmd.extend(["-m", "not slow"])

        # Agregar configuración adicional
        cmd.extend(["--tb=short", "--strict-markers", "--disable-warnings"])

        print(f"🚀 Ejecutando tests: {' '.join(cmd)}")
        print(f"📁 Directorio de trabajo: {self.project_root}")

        # Ejecutar tests
        try:
            result = subprocess.run(cmd, cwd=self.project_root, env=env, check=True)
            print("✅ Tests completados exitosamente")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests fallaron con código: {e.returncode}")
            return e.returncode
        except Exception as e:
            print(f"❌ Error ejecutando tests: {e}")
            return 1

    def run_performance_tests(self) -> int:
        """Ejecutar tests de rendimiento"""
        print("🚀 Ejecutando tests de rendimiento...")

        cmd = [
            "python",
            "-m",
            "pytest",
            "tests/test_search_units_e2e.py::TestSearchUnitsE2E::test_e2e_performance_stress_test",
            "-v",
            "--tb=short",
        ]

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Tests de rendimiento completados")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests de rendimiento fallaron: {e.returncode}")
            return e.returncode

    def run_coverage_report(self) -> int:
        """Generar reporte de cobertura"""
        print("📊 Generando reporte de cobertura...")

        cmd = [
            "python",
            "-m",
            "pytest",
            "tests/test_search_units_unit.py",
            "tests/test_search_units_integration.py",
            "--cov=src/trackhs_mcp",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml",
        ]

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Reporte de cobertura generado")
            print("📁 Reporte HTML disponible en: htmlcov/index.html")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generando reporte de cobertura: {e.returncode}")
            return e.returncode

    def run_linting(self) -> int:
        """Ejecutar linting en el código"""
        print("🔍 Ejecutando linting...")

        # Verificar si flake8 está instalado
        try:
            subprocess.run(["flake8", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  flake8 no está instalado, saltando linting")
            return 0

        cmd = [
            "flake8",
            "src/trackhs_mcp/",
            "tests/",
            "--max-line-length=100",
            "--ignore=E203,W503",
        ]

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Linting completado sin errores")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Linting falló: {e.returncode}")
            return e.returncode

    def run_type_checking(self) -> int:
        """Ejecutar verificación de tipos"""
        print("🔍 Ejecutando verificación de tipos...")

        # Verificar si mypy está instalado
        try:
            subprocess.run(["mypy", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  mypy no está instalado, saltando verificación de tipos")
            return 0

        cmd = [
            "mypy",
            "src/trackhs_mcp/",
            "--ignore-missing-imports",
            "--no-strict-optional",
        ]

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Verificación de tipos completada")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Verificación de tipos falló: {e.returncode}")
            return e.returncode

    def run_all_checks(self) -> int:
        """Ejecutar todas las verificaciones"""
        print("🔍 Ejecutando todas las verificaciones...")

        checks = [
            ("Linting", self.run_linting),
            ("Verificación de tipos", self.run_type_checking),
            ("Tests unitarios", lambda: self.run_tests("unit", verbose=True)),
            (
                "Tests de integración",
                lambda: self.run_tests("integration", verbose=True),
            ),
            ("Cobertura", self.run_coverage_report),
        ]

        results = []
        for name, check_func in checks:
            print(f"\n🔍 Ejecutando: {name}")
            result = check_func()
            results.append((name, result))

            if result != 0:
                print(f"❌ {name} falló")
            else:
                print(f"✅ {name} completado")

        # Resumen
        print("\n📊 Resumen de verificaciones:")
        for name, result in results:
            status = "✅" if result == 0 else "❌"
            print(f"  {status} {name}")

        # Retornar código de error si alguna verificación falló
        failed_checks = [name for name, result in results if result != 0]
        if failed_checks:
            print(f"\n❌ Verificaciones fallidas: {', '.join(failed_checks)}")
            return 1
        else:
            print("\n✅ Todas las verificaciones completadas exitosamente")
            return 0


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Runner para tests de search_units")
    parser.add_argument(
        "test_type",
        choices=[
            "unit",
            "integration",
            "api",
            "e2e",
            "all",
            "performance",
            "coverage",
            "lint",
            "types",
            "all-checks",
        ],
        help="Tipo de test a ejecutar",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ejecutar en modo verbose"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Incluir reporte de cobertura"
    )
    parser.add_argument(
        "--parallel", action="store_true", help="Ejecutar tests en paralelo"
    )
    parser.add_argument("--slow", action="store_true", help="Incluir tests lentos")

    args = parser.parse_args()

    runner = TestRunner()

    if args.test_type == "performance":
        return runner.run_performance_tests()
    elif args.test_type == "coverage":
        return runner.run_coverage_report()
    elif args.test_type == "lint":
        return runner.run_linting()
    elif args.test_type == "types":
        return runner.run_type_checking()
    elif args.test_type == "all-checks":
        return runner.run_all_checks()
    else:
        return runner.run_tests(
            test_type=args.test_type,
            verbose=args.verbose,
            coverage=args.coverage,
            parallel=args.parallel,
            slow_tests=args.slow,
        )


if __name__ == "__main__":
    sys.exit(main())
