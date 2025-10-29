#!/usr/bin/env python3
"""
Test final para verificar que la implementación corregida de amenities funciona correctamente
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


class FinalAmenitiesTester:
    """Tester final para verificar la implementación corregida"""

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

    def test_implementation_completeness(self):
        """Test completitud de la implementación"""
        logger.info("🧪 Testing completitud de la implementación...")

        if not self.client:
            self.log_test("Implementation completeness", False, "Cliente no disponible")
            return

        # Test todos los parámetros que ahora están implementados
        test_cases = [
            {
                "name": "Basic call",
                "params": {"page": 1, "size": 5},
                "expected_fields": ["_embedded", "page", "page_size", "total_items"],
            },
            {
                "name": "Search functionality",
                "params": {"search": "wifi", "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "Sorting parameters",
                "params": {"sortColumn": "name", "sortDirection": "asc", "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "Boolean filters",
                "params": {"isPublic": 1, "isFilterable": 1, "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "Group filter",
                "params": {"groupId": 2, "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "OTA types - Airbnb",
                "params": {"airbnbType": "ac", "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "OTA types - HomeAway",
                "params": {"homeawayType": "AMENITIES_AIR_CONDITIONING", "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "OTA types - Marriott",
                "params": {"marriottType": "AIR_CONDITION", "size": 3},
                "expected_fields": ["_embedded"],
            },
            {
                "name": "Complex combination",
                "params": {
                    "search": "air",
                    "isPublic": 1,
                    "isFilterable": 1,
                    "sortColumn": "name",
                    "sortDirection": "asc",
                    "size": 5,
                },
                "expected_fields": ["_embedded"],
            },
        ]

        for test_case in test_cases:
            try:
                result = self.client.get("api/pms/units/amenities", test_case["params"])
                self.results["api_responses"].append((test_case["name"], result))

                # Verificar campos esperados
                has_expected_fields = all(
                    field in result for field in test_case["expected_fields"]
                )

                # Verificar que hay resultados si se esperan
                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    test_case["name"],
                    has_expected_fields and has_results,
                    f"Campos: {has_expected_fields}, Resultados: {has_results}",
                )

            except Exception as e:
                self.log_test(test_case["name"], False, f"Error: {str(e)}")

    def test_parameter_validation(self):
        """Test validación de parámetros"""
        logger.info("🧪 Testing validación de parámetros...")

        if not self.client:
            self.log_test("Parameter validation", False, "Cliente no disponible")
            return

        # Test parámetros que deberían fallar
        invalid_tests = [
            ({"page": 0}, "Página 0 (debería fallar)"),
            ({"page": -1}, "Página negativa (debería fallar)"),
            ({"size": 0}, "Tamaño 0 (debería fallar)"),
            ({"size": 101}, "Tamaño > 100 (debería fallar)"),
        ]

        for params, description in invalid_tests:
            try:
                result = self.client.get("api/pms/units/amenities", params)
                # Si no falla, es un problema
                self.log_test(
                    f"Parameter validation: {description}",
                    False,
                    "Debería haber fallado con parámetros inválidos",
                )
            except Exception as e:
                # Si falla, es correcto
                self.log_test(
                    f"Parameter validation: {description}",
                    True,
                    f"Validación funcionó: {str(e)}",
                )

    def test_wildcard_functionality(self):
        """Test funcionalidad de wildcards"""
        logger.info("🧪 Testing funcionalidad de wildcards...")

        if not self.client:
            self.log_test("Wildcard functionality", False, "Cliente no disponible")
            return

        # Test wildcards en tipos OTA
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

    def test_response_structure(self):
        """Test estructura de respuesta"""
        logger.info("🧪 Testing estructura de respuesta...")

        if not self.client:
            self.log_test("Response structure", False, "Cliente no disponible")
            return

        try:
            result = self.client.get("api/pms/units/amenities", {"size": 1})

            if "_embedded" in result and "amenities" in result["_embedded"]:
                amenities = result["_embedded"]["amenities"]
                if amenities:
                    amenity = amenities[0]

                    # Verificar campos principales
                    main_fields = [
                        "id",
                        "name",
                        "groupId",
                        "group",
                        "isPublic",
                        "isFilterable",
                    ]
                    missing_fields = [
                        field for field in main_fields if field not in amenity
                    ]

                    self.log_test(
                        "Response structure completeness",
                        len(missing_fields) == 0,
                        f"Campos faltantes: {missing_fields}",
                    )

                    # Verificar tipos de datos
                    type_checks = [
                        ("id", isinstance(amenity.get("id"), int)),
                        ("name", isinstance(amenity.get("name"), str)),
                        ("isPublic", isinstance(amenity.get("isPublic"), bool)),
                        ("isFilterable", isinstance(amenity.get("isFilterable"), bool)),
                    ]

                    all_types_correct = all(check[1] for check in type_checks)
                    self.log_test(
                        "Data types", all_types_correct, f"Type checks: {type_checks}"
                    )

                else:
                    self.log_test(
                        "Response structure", False, "No amenities in response"
                    )
            else:
                self.log_test(
                    "Response structure", False, "Missing _embedded.amenities"
                )

        except Exception as e:
            self.log_test("Response structure", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests finales de verificación...")

        self.test_implementation_completeness()
        self.test_parameter_validation()
        self.test_wildcard_functionality()
        self.test_response_structure()

        # Resumen
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN DE TESTS FINALES")
        logger.info("=" * 60)
        logger.info(f"Tests ejecutados: {self.results['tests_run']}")
        logger.info(f"Tests pasados: {self.results['tests_passed']}")
        logger.info(f"Tests fallidos: {self.results['tests_failed']}")

        success_rate = (
            (self.results["tests_passed"] / self.results["tests_run"]) * 100
            if self.results["tests_run"] > 0
            else 0
        )
        logger.info(f"Tasa de éxito: {success_rate:.1f}%")

        if self.results["issues_found"]:
            logger.info("\n🔍 PROBLEMAS ENCONTRADOS:")
            for issue in self.results["issues_found"]:
                logger.info(f"  - {issue}")
        else:
            logger.info(
                "\n✅ ¡Todos los tests pasaron! La implementación está funcionando perfectamente."
            )

        # Guardar respuestas de API para análisis
        with open("amenities_final_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_final_test_responses.json"
        )

        return self.results


def main():
    """Función principal"""
    tester = FinalAmenitiesTester()
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
