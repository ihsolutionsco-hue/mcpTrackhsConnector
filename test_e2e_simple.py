#!/usr/bin/env python3
"""
Test End-to-End (E2E) simple para verificar que la funcionalidad de amenities funciona correctamente
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


class SimpleE2ETester:
    """Tester E2E simple para la funcionalidad de amenities"""

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

    def test_system_startup(self):
        """Test que el sistema se inicia correctamente"""
        logger.info("🧪 Testing inicio del sistema...")

        try:
            # Verificar configuración
            settings = get_settings()
            if not settings.trackhs_username or not settings.trackhs_password:
                self.log_test("System startup", False, "Credenciales no configuradas")
                return False

            if not settings.trackhs_api_url:
                self.log_test("System startup", False, "URL de API no configurada")
                return False

            self.log_test("System startup", True, "Sistema iniciado correctamente")
            return True

        except Exception as e:
            self.log_test("System startup", False, f"Error: {str(e)}")
            return False

    def test_api_connectivity(self):
        """Test conectividad con la API"""
        logger.info("🧪 Testing conectividad con API...")

        if not self.client:
            self.log_test("API connectivity", False, "Cliente no disponible")
            return False

        try:
            # Test de conectividad básica
            result = self.client.get("api/pms/units/amenities", {"page": 1, "size": 1})

            if "_embedded" in result and "amenities" in result["_embedded"]:
                self.log_test("API connectivity", True, "API conectada y respondiendo")
                return True
            else:
                self.log_test("API connectivity", False, "Respuesta de API inválida")
                return False

        except Exception as e:
            self.log_test("API connectivity", False, f"Error: {str(e)}")
            return False

    def test_basic_functionality(self):
        """Test funcionalidad básica"""
        logger.info("🧪 Testing funcionalidad básica...")

        if not self.client:
            self.log_test("Basic functionality", False, "Cliente no disponible")
            return False

        try:
            # Test llamada básica
            result = self.client.get("api/pms/units/amenities", {"page": 1, "size": 5})
            self.results["api_responses"].append(("basic_call", result))

            has_embedded = "_embedded" in result
            has_amenities = "_embedded" in result and "amenities" in result["_embedded"]
            has_pagination = all(
                key in result for key in ["page", "page_size", "total_items"]
            )

            success = has_embedded and has_amenities and has_pagination

            self.log_test(
                "Basic functionality",
                success,
                f"Embedded: {has_embedded}, Amenities: {has_amenities}, Pagination: {has_pagination}",
            )

            return success

        except Exception as e:
            self.log_test("Basic functionality", False, f"Error: {str(e)}")
            return False

    def test_advanced_functionality(self):
        """Test funcionalidad avanzada"""
        logger.info("🧪 Testing funcionalidad avanzada...")

        if not self.client:
            self.log_test("Advanced functionality", False, "Cliente no disponible")
            return False

        test_cases = [
            {
                "name": "Search functionality",
                "params": {"search": "wifi", "size": 3},
                "description": "Búsqueda por texto",
            },
            {
                "name": "Sorting functionality",
                "params": {"sortColumn": "name", "sortDirection": "asc", "size": 3},
                "description": "Ordenamiento",
            },
            {
                "name": "Boolean filters",
                "params": {"isPublic": 1, "isFilterable": 1, "size": 3},
                "description": "Filtros booleanos",
            },
            {
                "name": "Group filter",
                "params": {"groupId": 2, "size": 3},
                "description": "Filtro por grupo",
            },
            {
                "name": "OTA types",
                "params": {
                    "airbnbType": "ac",
                    "marriottType": "AIR_CONDITION",
                    "size": 3,
                },
                "description": "Tipos OTA",
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
                "description": "Combinación compleja",
            },
        ]

        all_passed = True

        for test_case in test_cases:
            try:
                result = self.client.get("api/pms/units/amenities", test_case["params"])
                self.results["api_responses"].append((test_case["name"], result))

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    test_case["name"],
                    has_results,
                    f"{test_case['description']} {'funciona' if has_results else 'falla'}",
                )

                if not has_results:
                    all_passed = False

            except Exception as e:
                self.log_test(test_case["name"], False, f"Error: {str(e)}")
                all_passed = False

        return all_passed

    def test_error_handling(self):
        """Test manejo de errores"""
        logger.info("🧪 Testing manejo de errores...")

        if not self.client:
            self.log_test("Error handling", False, "Cliente no disponible")
            return False

        # Test parámetros inválidos
        invalid_tests = [
            ({"page": 0}, "Página 0 (debería fallar)"),
            ({"page": -1}, "Página negativa (debería fallar)"),
            ({"size": 0}, "Tamaño 0 (debería fallar)"),
        ]

        all_passed = True

        for params, description in invalid_tests:
            try:
                result = self.client.get("api/pms/units/amenities", params)
                # Si no falla, es un problema
                self.log_test(
                    f"Error handling: {description}",
                    False,
                    "Debería haber fallado con parámetros inválidos",
                )
                all_passed = False
            except Exception as e:
                # Si falla, es correcto
                self.log_test(
                    f"Error handling: {description}",
                    True,
                    f"Error manejado correctamente: {str(e)}",
                )

        return all_passed

    def test_response_structure(self):
        """Test estructura de respuesta"""
        logger.info("🧪 Testing estructura de respuesta...")

        if not self.client:
            self.log_test("Response structure", False, "Cliente no disponible")
            return False

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

                    # Verificar tipos de datos
                    type_checks = [
                        ("id", isinstance(amenity.get("id"), int)),
                        ("name", isinstance(amenity.get("name"), str)),
                        ("isPublic", isinstance(amenity.get("isPublic"), bool)),
                        ("isFilterable", isinstance(amenity.get("isFilterable"), bool)),
                    ]

                    all_types_correct = all(check[1] for check in type_checks)

                    success = len(missing_fields) == 0 and all_types_correct

                    self.log_test(
                        "Response structure",
                        success,
                        f"Campos faltantes: {len(missing_fields)}, Tipos correctos: {all_types_correct}",
                    )

                    return success
                else:
                    self.log_test(
                        "Response structure", False, "No amenities in response"
                    )
                    return False
            else:
                self.log_test(
                    "Response structure", False, "Missing _embedded.amenities"
                )
                return False

        except Exception as e:
            self.log_test("Response structure", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Ejecutar todos los tests E2E"""
        logger.info("🚀 Iniciando tests End-to-End (E2E) simples...")

        # Test 1: Inicio del sistema
        system_ok = self.test_system_startup()
        if not system_ok:
            logger.error("❌ Sistema no inició correctamente. Abortando tests.")
            return self.results

        # Test 2: Conectividad API
        api_ok = self.test_api_connectivity()
        if not api_ok:
            logger.error("❌ API no disponible. Abortando tests.")
            return self.results

        # Test 3: Funcionalidad básica
        basic_ok = self.test_basic_functionality()
        if not basic_ok:
            logger.error("❌ Funcionalidad básica falló. Continuando con tests...")

        # Test 4: Funcionalidad avanzada
        advanced_ok = self.test_advanced_functionality()
        if not advanced_ok:
            logger.error("❌ Funcionalidad avanzada falló. Continuando con tests...")

        # Test 5: Manejo de errores
        error_ok = self.test_error_handling()
        if not error_ok:
            logger.error("❌ Manejo de errores falló. Continuando con tests...")

        # Test 6: Estructura de respuesta
        structure_ok = self.test_response_structure()
        if not structure_ok:
            logger.error("❌ Estructura de respuesta falló. Continuando con tests...")

        # Resumen
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN DE TESTS E2E")
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
                "\n✅ ¡Todos los tests E2E pasaron! El sistema está funcionando correctamente."
            )

        # Guardar respuestas de API para análisis
        with open("e2e_simple_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en e2e_simple_test_responses.json"
        )

        return self.results


def main():
    """Función principal"""
    tester = SimpleE2ETester()
    results = tester.run_all_tests()

    # Cerrar cliente
    if tester.client:
        tester.client.close()

    # Retornar código de salida basado en resultados
    if results["tests_failed"] > 0:
        logger.error(f"\n❌ {results['tests_failed']} tests fallaron")
        return 1
    else:
        logger.info(f"\n✅ Todos los tests E2E pasaron")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
