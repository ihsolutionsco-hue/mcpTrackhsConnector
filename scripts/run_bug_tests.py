#!/usr/bin/env python3
"""
Script para ejecutar tests de bugs y generar reportes
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class BugTestRunner:
    """Ejecutor de tests de bugs con generación de reportes"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        # Configurar timestamp para reportes
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_tests(self, test_type: str = "all") -> Dict[str, Any]:
        """
        Ejecuta los tests especificados

        Args:
            test_type: Tipo de tests a ejecutar (all, bug, integration, unit)

        Returns:
            Resultado de la ejecución
        """
        print(f"Ejecutando tests de tipo: {test_type}")
        print("=" * 50)

        # Construir comando pytest
        cmd = ["python", "-m", "pytest"]

        if test_type == "all":
            test_path = "tests/integration/test_bug_report.py"
        elif test_type == "bug":
            test_path = "tests/integration/test_bug_report.py"
            cmd.extend(["-m", "bug"])
        elif test_type == "integration":
            test_path = "tests/integration/"
        elif test_type == "unit":
            test_path = "tests/unit/"
        else:
            test_path = "tests/integration/test_bug_report.py"

        cmd.extend(
            [
                test_path,
                "-v",  # Verbose
                "--tb=short",  # Short traceback
                "--json-report",  # JSON report
                f"--json-report-file=reports/test_results_{self.timestamp}.json",
                "--html=reports/test_report.html",  # HTML report
                "--self-contained-html",  # Self-contained HTML
            ]
        )

        # Ejecutar tests
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos timeout
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd),
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Test execution timed out after 5 minutes",
                "command": " ".join(cmd),
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "command": " ".join(cmd),
            }

    def analyze_results(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza los resultados de los tests

        Args:
            result: Resultado de la ejecución de tests

        Returns:
            Análisis de resultados
        """
        analysis = {
            "timestamp": self.timestamp,
            "success": result["success"],
            "returncode": result["returncode"],
            "bugs_detected": [],
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "warnings": [],
            "summary": "",
        }

        # Analizar stdout para extraer información
        stdout_lines = result["stdout"].split("\n")

        for line in stdout_lines:
            if "PASSED" in line:
                analysis["tests_passed"] += 1
            elif "FAILED" in line:
                analysis["tests_failed"] += 1
                # Detectar bugs específicos
                if "BUG #1" in line or "is_active" in line:
                    analysis["bugs_detected"].append(
                        "BUG #1: Filtro is_active no funciona"
                    )
                elif "BUG #2" in line or "bedrooms" in line:
                    analysis["bugs_detected"].append(
                        "BUG #2: Filtros de rango ignorados"
                    )
                elif "BUG #3" in line or "unit_ids" in line:
                    analysis["bugs_detected"].append(
                        "BUG #3: Formato de array rechazado"
                    )
            elif "SKIPPED" in line:
                analysis["tests_skipped"] += 1
            elif "WARNING" in line or "WARN" in line:
                analysis["warnings"].append(line.strip())

        # Generar resumen
        total_tests = (
            analysis["tests_passed"]
            + analysis["tests_failed"]
            + analysis["tests_skipped"]
        )
        if total_tests > 0:
            pass_rate = (analysis["tests_passed"] / total_tests) * 100
            analysis["summary"] = (
                f"Ejecutados {total_tests} tests: {analysis['tests_passed']} pasaron, {analysis['tests_failed']} fallaron, {analysis['tests_skipped']} omitidos ({pass_rate:.1f}% éxito)"
            )
        else:
            analysis["summary"] = "No se ejecutaron tests"

        return analysis

    def generate_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """
        Genera un reporte en formato Markdown

        Args:
            analysis: Análisis de resultados

        Returns:
            Reporte en formato Markdown
        """
        report = f"""# 🧪 Reporte de Tests de Bugs - TrackHS API

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Timestamp:** {analysis['timestamp']}
**Estado:** {'✅ ÉXITO' if analysis['success'] else '❌ FALLÓ'}

## 📊 Resumen de Ejecución

{analysis['summary']}

### Estadísticas
- **Tests Pasados:** {analysis['tests_passed']}
- **Tests Fallidos:** {analysis['tests_failed']}
- **Tests Omitidos:** {analysis['tests_skipped']}
- **Código de Retorno:** {analysis['returncode']}

## 🐛 Bugs Detectados

"""

        if analysis["bugs_detected"]:
            for i, bug in enumerate(analysis["bugs_detected"], 1):
                report += f"{i}. {bug}\n"
        else:
            report += "✅ No se detectaron bugs nuevos\n"

        if analysis["warnings"]:
            report += "\n## ⚠️ Warnings\n\n"
            for warning in analysis["warnings"]:
                report += f"- {warning}\n"

        report += f"""
## 📁 Archivos Generados

- **Reporte HTML:** `reports/test_report.html`
- **Reporte JSON:** `reports/test_results_{analysis['timestamp']}.json`
- **Logs:** Ver salida de consola

## 🚀 Próximos Pasos

1. **Revisar bugs detectados** - Analizar cada bug encontrado
2. **Verificar logs** - Revisar salida detallada para debugging
3. **Implementar fixes** - Corregir bugs identificados
4. **Re-ejecutar tests** - Verificar que fixes funcionen

---
*Generado automáticamente por run_bug_tests.py*
"""

        return report

    def save_report(self, analysis: Dict[str, Any], markdown_report: str):
        """
        Guarda el reporte en archivos

        Args:
            analysis: Análisis de resultados
            markdown_report: Reporte en Markdown
        """
        # Guardar reporte JSON
        json_file = self.reports_dir / f"bug_analysis_{self.timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        # Guardar reporte Markdown
        md_file = self.reports_dir / f"bug_report_{self.timestamp}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_report)

        print(f"Reportes guardados:")
        print(f"   - JSON: {json_file}")
        print(f"   - Markdown: {md_file}")

    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        Ejecuta análisis comprehensivo de todos los bugs

        Returns:
            Resultado del análisis comprehensivo
        """
        print("Ejecutando análisis comprehensivo de bugs...")

        # Ejecutar test comprehensivo específico
        cmd = [
            "python",
            "-m",
            "pytest",
            "tests/integration/test_bug_report.py::test_comprehensive_bug_analysis",
            "-v",
            "-s",  # Verbose y sin capturar output
            "--tb=short",
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minutos timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "analysis_output": result.stdout,  # El test comprehensivo imprime análisis
            }

        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "analysis_output": "",
            }

    def main(self, args: List[str]):
        """
        Función principal del script

        Args:
            args: Argumentos de línea de comandos
        """
        print("TrackHS Bug Test Runner")
        print("=" * 40)

        # Parsear argumentos
        test_type = "all"
        comprehensive = False

        if len(args) > 1:
            if args[1] == "bug":
                test_type = "bug"
            elif args[1] == "integration":
                test_type = "integration"
            elif args[1] == "unit":
                test_type = "unit"
            elif args[1] == "comprehensive":
                comprehensive = True
            elif args[1] == "help":
                self.print_help()
                return

        if comprehensive:
            # Ejecutar análisis comprehensivo
            print("Ejecutando análisis comprehensivo...")
            result = self.run_comprehensive_analysis()

            print("\nRESULTADO DEL ANÁLISIS:")
            print("=" * 50)
            print(result["analysis_output"])

            if not result["success"]:
                print("\nERRORES:")
                print(result["stderr"])
        else:
            # Ejecutar tests normales
            print(f"Ejecutando tests de tipo: {test_type}")
            result = self.run_tests(test_type)

            # Analizar resultados
            analysis = self.analyze_results(result)

            # Generar reporte
            markdown_report = self.generate_markdown_report(analysis)

            # Mostrar resumen
            print("\nRESUMEN DE RESULTADOS:")
            print("=" * 50)
            print(analysis["summary"])

            if analysis["bugs_detected"]:
                print("\nBUGS DETECTADOS:")
                for i, bug in enumerate(analysis["bugs_detected"], 1):
                    print(f"   {i}. {bug}")

            if analysis["warnings"]:
                print("\nWARNINGS:")
                for warning in analysis["warnings"][:5]:  # Solo primeros 5
                    print(f"   - {warning}")

            # Guardar reportes
            self.save_report(analysis, markdown_report)

            # Mostrar salida completa si hay errores
            if not result["success"]:
                print("\nSALIDA COMPLETA:")
                print("=" * 50)
                print("STDOUT:")
                print(result["stdout"])
                print("\nSTDERR:")
                print(result["stderr"])

    def print_help(self):
        """Imprime ayuda del script"""
        help_text = """
TrackHS Bug Test Runner

USO:
    python scripts/run_bug_tests.py [TIPO]

TIPOS DE TESTS:
    all          - Todos los tests (default)
    bug          - Solo tests de bugs
    integration  - Tests de integración
    unit         - Tests unitarios
    comprehensive - Análisis comprehensivo de bugs
    help         - Mostrar esta ayuda

EJEMPLOS:
    python scripts/run_bug_tests.py
    python scripts/run_bug_tests.py bug
    python scripts/run_bug_tests.py comprehensive

ARCHIVOS GENERADOS:
    reports/test_report.html          - Reporte HTML
    reports/test_results_*.json       - Resultados JSON
    reports/bug_analysis_*.json       - Análisis de bugs
    reports/bug_report_*.md           - Reporte Markdown

VARIABLES DE ENTORNO:
    TRACKHS_USERNAME - Usuario para API real
    TRACKHS_PASSWORD - Password para API real
    TRACKHS_API_URL  - URL de la API (default: https://ihmvacations.trackhs.com)
"""
        print(help_text)


if __name__ == "__main__":
    runner = BugTestRunner()
    runner.main(sys.argv)
