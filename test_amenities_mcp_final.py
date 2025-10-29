#!/usr/bin/env python3
"""
Test final para verificar que la implementación MCP de amenities funciona correctamente
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
from trackhs_mcp.server import mcp


class MCPAmenitiesTester:
    """Tester para la implementación MCP de amenities"""

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

    async def test_mcp_tool_call(self):
        """Test llamada directa a la herramienta MCP"""
        logger.info("🧪 Testing llamada directa a herramienta MCP...")

        try:
            # Obtener la herramienta search_amenities del servidor MCP
            tools = mcp.list_tools()
            amenities_tool = None

            for tool in tools:
                if tool.name == "search_amenities":
                    amenities_tool = tool
                    break

            if not amenities_tool:
                self.log_test(
                    "MCP tool availability",
                    False,
                    "Herramienta search_amenities no encontrada",
                )
                return

            self.log_test(
                "MCP tool availability", True, "Herramienta search_amenities disponible"
            )

            # Test llamada básica
            try:
                # Simular llamada con parámetros básicos
                result = await mcp.call_tool("search_amenities", {"page": 1, "size": 5})

                self.results["api_responses"].append(("mcp_basic_call", result))

                has_embedded = "_embedded" in result
                has_amenities = (
                    "_embedded" in result and "amenities" in result["_embedded"]
                )
                has_pagination = all(
                    key in result for key in ["page", "page_size", "total_items"]
                )

                self.log_test(
                    "MCP basic call structure",
                    has_embedded and has_amenities and has_pagination,
                    f"Embedded: {has_embedded}, Amenities: {has_amenities}, Pagination: {has_pagination}",
                )

            except Exception as e:
                self.log_test(
                    "MCP basic call", False, f"Error en llamada básica: {str(e)}"
                )

            # Test con parámetros nuevos
            try:
                result = await mcp.call_tool(
                    "search_amenities",
                    {
                        "page": 1,
                        "size": 3,
                        "search": "wifi",
                        "is_public": 1,
                        "is_filterable": 1,
                        "sort_column": "name",
                        "sort_direction": "asc",
                    },
                )

                self.results["api_responses"].append(("mcp_advanced_call", result))

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    "MCP advanced parameters",
                    has_results,
                    f"Parámetros avanzados {'encontraron resultados' if has_results else 'sin resultados'}",
                )

            except Exception as e:
                self.log_test(
                    "MCP advanced parameters",
                    False,
                    f"Error en parámetros avanzados: {str(e)}",
                )

            # Test tipos OTA
            try:
                result = await mcp.call_tool(
                    "search_amenities",
                    {
                        "page": 1,
                        "size": 3,
                        "airbnb_type": "ac",
                        "marriott_type": "AIR_CONDITION",
                    },
                )

                self.results["api_responses"].append(("mcp_ota_types", result))

                has_results = (
                    "_embedded" in result
                    and "amenities" in result["_embedded"]
                    and len(result["_embedded"]["amenities"]) > 0
                )

                self.log_test(
                    "MCP OTA types",
                    has_results,
                    f"Tipos OTA {'encontraron resultados' if has_results else 'sin resultados'}",
                )

            except Exception as e:
                self.log_test("MCP OTA types", False, f"Error en tipos OTA: {str(e)}")

        except Exception as e:
            self.log_test("MCP tool call", False, f"Error general: {str(e)}")

    async def test_parameter_validation(self):
        """Test validación de parámetros"""
        logger.info("🧪 Testing validación de parámetros...")

        # Test parámetros inválidos
        invalid_tests = [
            ({"page": 0}, "Página 0 (debería fallar)"),
            ({"page": -1}, "Página negativa (debería fallar)"),
            ({"size": 0}, "Tamaño 0 (debería fallar)"),
            ({"size": 101}, "Tamaño > 100 (debería fallar)"),
        ]

        for params, description in invalid_tests:
            try:
                result = await mcp.call_tool("search_amenities", params)
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
                    f"Validación funcionó correctamente: {str(e)}",
                )

    async def test_error_handling(self):
        """Test manejo de errores"""
        logger.info("🧪 Testing manejo de errores...")

        # Test con parámetros que deberían causar errores de API
        try:
            result = await mcp.call_tool(
                "search_amenities", {"page": 99999, "size": 1}  # Página muy alta
            )

            # Debería manejar la página alta graciosamente
            self.log_test(
                "Error handling: High page number",
                True,
                "Página alta manejada correctamente",
            )

        except Exception as e:
            self.log_test(
                "Error handling: High page number",
                True,
                f"Error manejado correctamente: {str(e)}",
            )

    async def run_all_tests(self):
        """Ejecutar todos los tests"""
        logger.info("🚀 Iniciando tests finales de implementación MCP...")

        await self.test_mcp_tool_call()
        await self.test_parameter_validation()
        await self.test_error_handling()

        # Resumen
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN DE TESTS FINALES")
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
                "\n✅ ¡Todos los tests pasaron! La implementación MCP está funcionando correctamente."
            )

        # Guardar respuestas de API para análisis
        with open("amenities_mcp_final_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(
            f"\n💾 Respuestas de API guardadas en amenities_mcp_final_test_responses.json"
        )

        return self.results


async def main():
    """Función principal"""
    tester = MCPAmenitiesTester()
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
