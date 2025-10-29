#!/usr/bin/env python3
"""
Test simple para verificar que la función search_amenities funciona correctamente
"""

import json
import logging
import sys
from typing import Any, Dict

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Importar la función directamente
sys.path.append("src")
from trackhs_mcp.server import search_amenities


class SimpleAmenitiesTester:
    """Tester simple para la función search_amenities"""

    def __init__(self):
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "issues_found": [],
            "api_responses": [],
        }

    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Registrar resultado de test"""
        self.results["tests_run"] += 1
        if passed:
            self.results["tests_passed"] += 1
            logger.info(f"✅ {test_name}: PASSED {details}")
        else:
            self.results["tests_failed"] += 1
            self.results["issues_found"].append(f"{test_name}: {details}")
            logger.error(f"❌ {test_name}: FAILED - {details}")

    def test_basic_functionality(self):
        """Test funcionalidad básica"""
        logger.info("🧪 Testing funcionalidad básica...")

        try:
            # Test llamada básica
            result = search_amenities()
            self.results["api_responses"].append(("basic_call", result))

            has_embedded = "_embedded" in result
            has_amenities = "_embedded" in result and "amenities" in result["_embedded"]
            has_pagination = all(
                key in result for key in ["page", "page_size", "total_items"]
            )

            self.log_test(
                "Basic call structure",
                has_embedded and has_amenities and has_pagination,
                f"Embedded: {has_embedded}, Amenities: {has_amenities}, Pagination: {has_pagination}",
            )

        except Exception as e:
            self.log_test("Basic functionality", False, f"Exception: {str(e)}")

    def test_new_parameters(self):
        """Test nuevos parámetros implementados"""
        logger.info("🧪 Testing nuevos parámetros...")

        # Test con parámetros de ordenamiento
        try:
            result = search_amenities(
                page=1, size=3, sort_column="name", sort_direction="asc"
            )
            self.results["api_responses"].append(("sorting_test", result))

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Sorting parameters",
                has_results,
                f"Ordenamiento {'funciona' if has_results else 'falla'}",
            )

        except Exception as e:
            self.log_test("Sorting parameters", False, f"Error: {str(e)}")

        # Test con filtros booleanos
        try:
            result = search_amenities(page=1, size=3, is_public=1, is_filterable=1)
            self.results["api_responses"].append(("boolean_filters", result))

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Boolean filters",
                has_results,
                f"Filtros booleanos {'funcionan' if has_results else 'fallan'}",
            )

        except Exception as e:
            self.log_test("Boolean filters", False, f"Error: {str(e)}")

        # Test con filtro por grupo
        try:
            result = search_amenities(page=1, size=3, group_id=2)
            self.results["api_responses"].append(("group_filter", result))

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Group filter",
                has_results,
                f"Filtro por grupo {'funciona' if has_results else 'falla'}",
            )

        except Exception as e:
            self.log_test("Group filter", False, f"Error: {str(e)}")

        # Test con tipos OTA
        try:
            result = search_amenities(
                page=1, size=3, airbnb_type="ac", marriott_type="AIR_CONDITION"
            )
            self.results["api_responses"].append(("ota_types", result))

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "OTA types",
                has_results,
                f"Tipos OTA {'funcionan' if has_results else 'fallan'}",
            )

        except Exception as e:
            self.log_test("OTA types", False, f"Error: {str(e)}")

    def test_parameter_combinations(self):
        """Test combinaciones de parámetros"""
        logger.info("🧪 Testing combinaciones de parámetros...")

        try:
            result = search_amenities(
                page=1,
                size=5,
                search="wifi",
                is_public=1,
                is_filterable=1,
                sort_column="name",
                sort_direction="asc",
            )
            self.results["api_responses"].append(("complex_combination", result))

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Complex parameter combination",
                has_results,
                f"Combinación compleja {'funciona' if has_results else 'falla'}",
            )

        except Exception as e:
            self.log_test("Complex parameter combination", False, f"Error: {str(e)}")

    def test_error_handling(self):
        """Test manejo de errores"""
        logger.info("🧪 Testing manejo de errores...")

        # Test parámetros inválidos
        invalid_tests = [
            ({"page": 0}, "Página 0"),
            ({"page": -1}, "Página negativa"),
            ({"size": 0}, "Tamaño 0"),
            ({"size": 101}, "Tamaño > 100"),
        ]

        for params, description in invalid_tests:
            try:
                result = search_amenities(**params)
                # Si no falla, es un problema
                self.log_test(
                    f"Error handling: {description}",
                    False,
                    "Debería haber fallado con parámetros inválidos",
                )
            except Exception as e:
                # Si falla, es correcto
                self.log_test(
                    f"Error handling: {description}",
                    True,
                    f"Validación funcionó: {str(e)}",
                )

    def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests simples de verificación...")

        self.test_basic_functionality()
        self.test_new_parameters()
        self.test_parameter_combinations()
        self.test_error_handling()

        # Resumen
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN DE TESTS SIMPLES")
        logger.info("=" * 60)
        logger.info(f"Tests ejecutados: {self.results['tests_run']}")
        logger.info(f"Tests pasados: {self.results['tests_passed']}")
        logger.info(f"Tests fallidos: {self.results['tests_failed']}")

        if self.results["issues_found"]:
            logger.info("\n🔍 PROBLEMAS ENCONTRADOS:")
            for issue in self.results["issues_found"]:
                logger.info(f"  - {issue}")
        else:
            logger.info(
                "\n✅ ¡Todos los tests pasaron! La implementación está funcionando correctamente."
            )

        # Guardar respuestas de API para análisis
        with open("amenities_simple_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_simple_test_responses.json"
        )

        return self.results


def main():
    """Función principal"""
    tester = SimpleAmenitiesTester()
    results = tester.run_all_tests()

    # Retornar código de salida basado en resultados
    if results["tests_failed"] > 0:
        logger.error(f"\n❌ {results['tests_failed']} tests fallaron")
        return 1
    else:
        logger.info(f"\n✅ Todos los tests pasaron")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
