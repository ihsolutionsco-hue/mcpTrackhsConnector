#!/usr/bin/env python3
"""
Test directo para la funcionalidad de amenities usando el cliente HTTP
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


class DirectAmenitiesTester:
    """Tester directo para amenities usando cliente HTTP"""

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

    def test_basic_api_call(self):
        """Test llamada básica a la API"""
        logger.info("🧪 Testing llamada básica a la API...")

        if not self.client:
            self.log_test("Basic API call", False, "Cliente no disponible")
            return

        try:
            result = self.client.get("api/pms/units/amenities", {"page": 1, "size": 5})
            self.results["api_responses"].append(("basic_call", result))

            # Verificar estructura básica
            has_embedded = "_embedded" in result
            has_amenities = "_embedded" in result and "amenities" in result["_embedded"]
            has_pagination = all(
                key in result for key in ["page", "page_size", "total_items"]
            )

            self.log_test(
                "Basic API call structure",
                has_embedded and has_amenities and has_pagination,
                f"Embedded: {has_embedded}, Amenities: {has_amenities}, Pagination: {has_pagination}",
            )

            if has_amenities:
                amenities_count = len(result["_embedded"]["amenities"])
                self.log_test(
                    "Amenities count",
                    amenities_count > 0,
                    f"Encontradas {amenities_count} amenidades",
                )

        except Exception as e:
            self.log_test("Basic API call", False, f"Exception: {str(e)}")

    def test_missing_parameters(self):
        """Test parámetros faltantes según OpenAPI"""
        logger.info("🧪 Testing parámetros faltantes...")

        if not self.client:
            self.log_test("Missing parameters", False, "Cliente no disponible")
            return

        # Parámetros que deberían existir según OpenAPI
        missing_params = [
            "sortColumn",
            "sortDirection",
            "groupId",
            "isPublic",
            "publicSearchable",
            "isFilterable",
            "homeawayType",
            "airbnbType",
            "tripadvisorType",
            "marriottType",
        ]

        for param in missing_params:
            try:
                # Intentar llamar con parámetro faltante
                result = self.client.get("api/pms/units/amenities", {param: "test"})
                # Si no falla, el parámetro está soportado por la API
                self.log_test(
                    f"API parameter {param}",
                    True,
                    f"Parámetro {param} soportado por la API",
                )
            except Exception as e:
                # Si falla, verificar si es por parámetro no soportado o error de conexión
                if "400" in str(e) or "422" in str(e):
                    self.log_test(
                        f"API parameter {param}",
                        False,
                        f"Parámetro {param} no soportado por la API (error 400/422): {str(e)}",
                    )
                else:
                    self.log_test(
                        f"API parameter {param}", False, f"Error inesperado: {str(e)}"
                    )

    def test_response_structure(self):
        """Test estructura de respuesta vs OpenAPI"""
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

                    # Campos requeridos según OpenAPI
                    required_fields = [
                        "id",
                        "name",
                        "groupId",
                        "group",
                        "homeawayType",
                        "airbnbType",
                        "tripadvisorType",
                        "marriottType",
                        "isFilterable",
                        "isPublic",
                        "publicSearchable",
                        "createdBy",
                        "createdAt",
                        "updatedBy",
                        "updatedAt",
                        "_links",
                    ]

                    missing_fields = []
                    present_fields = []
                    for field in required_fields:
                        if field in amenity:
                            present_fields.append(field)
                        else:
                            missing_fields.append(field)

                    self.log_test(
                        "Response structure completeness",
                        len(missing_fields) == 0,
                        f"Campos presentes: {len(present_fields)}, faltantes: {len(missing_fields)} - {missing_fields}",
                    )

                    # Verificar tipos de datos específicos
                    type_checks = []
                    if "id" in amenity:
                        type_checks.append(("id", isinstance(amenity["id"], int)))
                    if "name" in amenity:
                        type_checks.append(("name", isinstance(amenity["name"], str)))
                    if "isPublic" in amenity:
                        type_checks.append(
                            ("isPublic", isinstance(amenity["isPublic"], bool))
                        )
                    if "isFilterable" in amenity:
                        type_checks.append(
                            ("isFilterable", isinstance(amenity["isFilterable"], bool))
                        )

                    all_types_correct = all(check[1] for check in type_checks)
                    self.log_test(
                        "Data types", all_types_correct, f"Type checks: {type_checks}"
                    )

                    # Mostrar estructura real de la amenidad
                    logger.info(
                        f"📋 Estructura real de amenidad: {json.dumps(amenity, indent=2, default=str)}"
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

    def test_search_functionality(self):
        """Test funcionalidad de búsqueda"""
        logger.info("🧪 Testing funcionalidad de búsqueda...")

        if not self.client:
            self.log_test("Search functionality", False, "Cliente no disponible")
            return

        search_terms = ["wifi", "pool", "parking", "air conditioning", "kitchen"]

        for term in search_terms:
            try:
                result = self.client.get(
                    "api/pms/units/amenities", {"search": term, "size": 5}
                )

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                result_count = (
                    len(result["_embedded"]["amenities"])
                    if "_embedded" in result and "amenities" in result["_embedded"]
                    else 0
                )

                self.log_test(
                    f"Search term '{term}'",
                    has_results,
                    f"Término '{term}' encontró {result_count} resultados",
                )

            except Exception as e:
                self.log_test(f"Search term '{term}'", False, f"Error: {str(e)}")

    def test_pagination(self):
        """Test paginación"""
        logger.info("🧪 Testing paginación...")

        if not self.client:
            self.log_test("Pagination", False, "Cliente no disponible")
            return

        # Test diferentes tamaños de página
        page_sizes = [1, 5, 10, 50]

        for size in page_sizes:
            try:
                result = self.client.get(
                    "api/pms/units/amenities", {"page": 1, "size": size}
                )

                actual_size = (
                    len(result["_embedded"]["amenities"])
                    if "_embedded" in result and "amenities" in result["_embedded"]
                    else 0
                )
                expected_size = min(size, result.get("total_items", 0))

                self.log_test(
                    f"Page size {size}",
                    actual_size <= size,
                    f"Tamaño solicitado: {size}, obtenido: {actual_size}, total: {result.get('total_items', 0)}",
                )

            except Exception as e:
                self.log_test(f"Page size {size}", False, f"Error: {str(e)}")

    def test_sorting(self):
        """Test ordenamiento"""
        logger.info("🧪 Testing ordenamiento...")

        if not self.client:
            self.log_test("Sorting", False, "Cliente no disponible")
            return

        # Test diferentes columnas de ordenamiento
        sort_columns = ["id", "name", "isPublic", "isFilterable"]

        for column in sort_columns:
            try:
                result = self.client.get(
                    "api/pms/units/amenities",
                    {"sortColumn": column, "sortDirection": "asc", "size": 3},
                )

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    f"Sort by {column}",
                    has_results,
                    f"Ordenamiento por {column} {'funciona' if has_results else 'falla'}",
                )

            except Exception as e:
                self.log_test(f"Sort by {column}", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests directos de amenities...")

        self.test_basic_api_call()
        self.test_missing_parameters()
        self.test_response_structure()
        self.test_search_functionality()
        self.test_pagination()
        self.test_sorting()

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

        # Guardar respuestas de API para análisis
        with open("amenities_direct_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_direct_test_responses.json"
        )

        return self.results


def main():
    """Función principal"""
    tester = DirectAmenitiesTester()
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
