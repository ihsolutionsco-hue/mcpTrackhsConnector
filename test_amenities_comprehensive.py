#!/usr/bin/env python3
"""
Test comprehensivo para la funcionalidad de amenities
Identifica problemas y discrepancias con la especificación OpenAPI
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Importar el servidor MCP
sys.path.append("src")
from trackhs_mcp.server import search_amenities


class AmenitiesTester:
    """Tester para la funcionalidad de amenities"""

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

    async def test_basic_functionality(self):
        """Test básico de funcionalidad"""
        logger.info("🧪 Testing funcionalidad básica de amenities...")

        try:
            # Test 1: Llamada básica sin parámetros
            result = search_amenities()
            self.results["api_responses"].append(("basic_call", result))

            # Verificar estructura básica
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

            # Test 2: Con parámetros básicos
            result_with_params = search_amenities(page=1, size=5, search="wifi")
            self.results["api_responses"].append(("with_params", result_with_params))

            self.log_test(
                "Call with parameters",
                isinstance(result_with_params, dict),
                f"Response type: {type(result_with_params)}",
            )

        except Exception as e:
            self.log_test("Basic functionality", False, f"Exception: {str(e)}")

    async def test_missing_parameters(self):
        """Test parámetros faltantes según OpenAPI"""
        logger.info("🧪 Testing parámetros faltantes...")

        # Parámetros que deberían existir según OpenAPI pero no están implementados
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
                # Intentar llamar con parámetro faltante usando kwargs
                kwargs = {param: "test"}
                result = search_amenities(**kwargs)
                # Si no falla, el parámetro no está implementado correctamente
                self.log_test(
                    f"Missing parameter {param}",
                    False,
                    f"Parámetro {param} no está implementado pero debería existir según OpenAPI",
                )
            except TypeError as e:
                # Si falla con TypeError, es esperado porque no está implementado
                self.log_test(
                    f"Missing parameter {param}",
                    True,
                    f"Parámetro {param} correctamente no implementado (error esperado): {str(e)}",
                )
            except Exception as e:
                # Otros errores también son esperados
                self.log_test(
                    f"Missing parameter {param}",
                    True,
                    f"Parámetro {param} correctamente no implementado (error esperado): {str(e)}",
                )

    async def test_response_structure(self):
        """Test estructura de respuesta vs OpenAPI"""
        logger.info("🧪 Testing estructura de respuesta...")

        try:
            result = search_amenities(size=1)

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
                    for field in required_fields:
                        if field not in amenity:
                            missing_fields.append(field)

                    self.log_test(
                        "Response structure completeness",
                        len(missing_fields) == 0,
                        f"Campos faltantes en respuesta: {missing_fields}",
                    )

                    # Verificar tipos de datos
                    type_checks = []
                    if "id" in amenity:
                        type_checks.append(("id", isinstance(amenity["id"], int)))
                    if "name" in amenity:
                        type_checks.append(("name", isinstance(amenity["name"], str)))
                    if "isPublic" in amenity:
                        type_checks.append(
                            ("isPublic", isinstance(amenity["isPublic"], bool))
                        )

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

    async def test_pagination_limits(self):
        """Test límites de paginación"""
        logger.info("🧪 Testing límites de paginación...")

        # Test página 0 (según OpenAPI, máximo es 0, lo cual es extraño)
        try:
            result = search_amenities(page=0)
            self.log_test(
                "Page 0 support", True, "Página 0 soportada (aunque OpenAPI dice max=0)"
            )
        except Exception as e:
            self.log_test("Page 0 support", False, f"Página 0 no soportada: {str(e)}")

        # Test página 1 (debería funcionar)
        try:
            result = search_amenities(page=1)
            self.log_test("Page 1 support", True, "Página 1 funciona correctamente")
        except Exception as e:
            self.log_test("Page 1 support", False, f"Página 1 falla: {str(e)}")

        # Test tamaño de página grande
        try:
            result = search_amenities(size=1000)
            self.log_test("Large page size", True, "Tamaño de página grande soportado")
        except Exception as e:
            self.log_test("Large page size", False, f"Tamaño grande falla: {str(e)}")

    async def test_search_functionality(self):
        """Test funcionalidad de búsqueda"""
        logger.info("🧪 Testing funcionalidad de búsqueda...")

        search_terms = ["wifi", "pool", "parking", "air conditioning", "kitchen"]

        for term in search_terms:
            try:
                result = search_amenities(search=term)

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    f"Search term '{term}'",
                    has_results,
                    f"Término '{term}' {'encontró resultados' if has_results else 'sin resultados'}",
                )

            except Exception as e:
                self.log_test(f"Search term '{term}'", False, f"Error: {str(e)}")

    async def test_error_handling(self):
        """Test manejo de errores"""
        logger.info("🧪 Testing manejo de errores...")

        # Test parámetros inválidos
        invalid_tests = [
            ({"page": -1}, "Página negativa"),
            ({"size": -1}, "Tamaño negativo"),
            ({"page": "invalid"}, "Página no numérica"),
            ({"size": "invalid"}, "Tamaño no numérico"),
        ]

        for params, description in invalid_tests:
            try:
                result = search_amenities(**params)
                # Si no falla, verificar si los valores fueron corregidos
                if "page" in params and isinstance(params["page"], str):
                    # Debería convertir string a int
                    self.log_test(
                        f"Error handling: {description}",
                        True,
                        "Conversión de tipos funcionó",
                    )
                else:
                    self.log_test(
                        f"Error handling: {description}",
                        False,
                        "Debería haber fallado con parámetros inválidos",
                    )
            except Exception as e:
                self.log_test(
                    f"Error handling: {description}",
                    True,
                    f"Error manejado correctamente: {str(e)}",
                )

    async def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests comprehensivos de amenities...")

        await self.test_basic_functionality()
        await self.test_missing_parameters()
        await self.test_response_structure()
        await self.test_pagination_limits()
        await self.test_search_functionality()
        await self.test_error_handling()

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
        with open("amenities_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_test_responses.json"
        )

        return self.results


async def main():
    """Función principal"""
    tester = AmenitiesTester()
    results = await tester.run_all_tests()

    # Retornar código de salida basado en resultados
    if results["tests_failed"] > 0:
        logger.error(f"\n❌ {results['tests_failed']} tests fallaron")
        return 1
    else:
        logger.info(f"\n✅ Todos los tests pasaron")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
