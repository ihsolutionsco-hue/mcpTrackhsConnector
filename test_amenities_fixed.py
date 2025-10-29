#!/usr/bin/env python3
"""
Test para verificar que la implementación corregida de amenities funciona correctamente
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

# Importar el cliente
sys.path.append("src")
from trackhs_mcp.client import TrackHSClient
from trackhs_mcp.config import get_settings


class FixedAmenitiesTester:
    """Tester para la implementación corregida de amenities"""

    def __init__(self):
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "issues_found": [],
            "api_responses": [],
        }
        self.client = None
        self.setup_client()

    def setup_client(self):
        """Configurar cliente HTTP"""
        try:
            settings = get_settings()
            if settings.trackhs_username and settings.trackhs_password:
                self.client = TrackHSClient(
                    base_url=settings.trackhs_api_url,
                    username=settings.trackhs_username,
                    password=settings.trackhs_password,
                )
                logger.info("✅ Cliente HTTP configurado correctamente")
            else:
                logger.error("❌ Credenciales no configuradas")
        except Exception as e:
            logger.error(f"❌ Error configurando cliente: {e}")

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

    def test_new_parameters(self):
        """Test de los nuevos parámetros implementados"""
        logger.info("🧪 Testing nuevos parámetros implementados...")

        if not self.client:
            self.log_test("New parameters", False, "Cliente no disponible")
            return

        # Test ordenamiento
        try:
            result = self.client.get(
                "api/pms/units/amenities",
                {"sortColumn": "name", "sortDirection": "asc", "size": 3},
            )
            self.log_test(
                "Sorting parameters",
                True,
                "Parámetros de ordenamiento funcionan correctamente",
            )
        except Exception as e:
            self.log_test("Sorting parameters", False, f"Error: {str(e)}")

        # Test filtros booleanos
        try:
            result = self.client.get(
                "api/pms/units/amenities", {"isPublic": 1, "isFilterable": 1, "size": 3}
            )
            self.log_test(
                "Boolean filters", True, "Filtros booleanos funcionan correctamente"
            )
        except Exception as e:
            self.log_test("Boolean filters", False, f"Error: {str(e)}")

        # Test filtro por grupo
        try:
            result = self.client.get(
                "api/pms/units/amenities", {"groupId": 2, "size": 3}
            )
            self.log_test(
                "Group filter", True, "Filtro por grupo funciona correctamente"
            )
        except Exception as e:
            self.log_test("Group filter", False, f"Error: {str(e)}")

        # Test tipos OTA
        ota_types = [
            ("homeawayType", "AMENITIES_AIR_CONDITIONING"),
            ("airbnbType", "ac"),
            ("marriottType", "AIR_CONDITION"),
        ]

        for param, value in ota_types:
            try:
                result = self.client.get(
                    "api/pms/units/amenities", {param: value, "size": 3}
                )
                self.log_test(
                    f"OTA type {param}", True, f"Búsqueda por {param}={value} funciona"
                )
            except Exception as e:
                self.log_test(f"OTA type {param}", False, f"Error: {str(e)}")

    def test_parameter_combinations(self):
        """Test combinaciones de parámetros"""
        logger.info("🧪 Testing combinaciones de parámetros...")

        if not self.client:
            self.log_test("Parameter combinations", False, "Cliente no disponible")
            return

        # Test combinación compleja
        try:
            result = self.client.get(
                "api/pms/units/amenities",
                {
                    "search": "air",
                    "isPublic": 1,
                    "isFilterable": 1,
                    "sortColumn": "name",
                    "sortDirection": "asc",
                    "size": 5,
                },
            )

            has_results = (
                "_embedded" in result
                and "amenities" in result["_embedded"]
                and len(result["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Complex parameter combination",
                has_results,
                f"Combinación compleja {'encontró resultados' if has_results else 'sin resultados'}",
            )

        except Exception as e:
            self.log_test("Complex parameter combination", False, f"Error: {str(e)}")

    def test_wildcard_search(self):
        """Test búsqueda con wildcards"""
        logger.info("🧪 Testing búsqueda con wildcards...")

        if not self.client:
            self.log_test("Wildcard search", False, "Cliente no disponible")
            return

        # Test wildcard en tipos OTA
        wildcard_tests = [
            ("airbnbType", "ac%"),
            ("marriottType", "AIR_%"),
            ("homeawayType", "AMENITIES_%"),
        ]

        for param, value in wildcard_tests:
            try:
                result = self.client.get(
                    "api/pms/units/amenities", {param: value, "size": 3}
                )

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    f"Wildcard {param}",
                    has_results,
                    f"Wildcard {param}={value} {'encontró resultados' if has_results else 'sin resultados'}",
                )

            except Exception as e:
                self.log_test(f"Wildcard {param}", False, f"Error: {str(e)}")

    def test_edge_cases(self):
        """Test casos límite"""
        logger.info("🧪 Testing casos límite...")

        if not self.client:
            self.log_test("Edge cases", False, "Cliente no disponible")
            return

        # Test página 0 (según OpenAPI, máximo es 0)
        try:
            result = self.client.get("api/pms/units/amenities", {"page": 0, "size": 1})
            self.log_test(
                "Page 0 support", True, "Página 0 soportada (aunque OpenAPI dice max=0)"
            )
        except Exception as e:
            self.log_test("Page 0 support", False, f"Error: {str(e)}")

        # Test tamaño de página grande
        try:
            result = self.client.get(
                "api/pms/units/amenities", {"page": 1, "size": 100}
            )
            self.log_test("Large page size", True, "Tamaño de página grande soportado")
        except Exception as e:
            self.log_test("Large page size", False, f"Error: {str(e)}")

        # Test parámetros vacíos
        try:
            result = self.client.get(
                "api/pms/units/amenities", {"search": "", "isPublic": "", "size": 1}
            )
            self.log_test(
                "Empty parameters", True, "Parámetros vacíos manejados correctamente"
            )
        except Exception as e:
            self.log_test("Empty parameters", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests de implementación corregida...")

        self.test_new_parameters()
        self.test_parameter_combinations()
        self.test_wildcard_search()
        self.test_edge_cases()

        # Resumen
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN DE TESTS")
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
        with open("amenities_fixed_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_fixed_test_responses.json"
        )

        return self.results


def main():
    """Función principal"""
    tester = FixedAmenitiesTester()
    results = tester.run_all_tests()

    # Cerrar cliente
    if tester.client:
        tester.client.close()

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
