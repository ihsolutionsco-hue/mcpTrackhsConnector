#!/usr/bin/env python3
"""
Test End-to-End (E2E) completo para verificar que la funcionalidad de amenities funciona correctamente
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


class E2EAmenitiesTester:
    """Tester E2E para la funcionalidad de amenities"""

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

    async def test_mcp_server_startup(self):
        """Test que el servidor MCP se inicia correctamente"""
        logger.info("🧪 Testing inicio del servidor MCP...")

        try:
            # Verificar que el servidor MCP está configurado
            if mcp is None:
                self.log_test(
                    "MCP Server startup", False, "Servidor MCP no inicializado"
                )
                return False

            # Verificar que tiene herramientas registradas
            tools = getattr(mcp, "tools", [])
            if not tools:
                self.log_test(
                    "MCP Server startup", False, "No hay herramientas registradas"
                )
                return False

            # Buscar la herramienta search_amenities
            amenities_tool = None
            for tool in tools:
                if hasattr(tool, "name") and tool.name == "search_amenities":
                    amenities_tool = tool
                    break

            if not amenities_tool:
                self.log_test(
                    "MCP Server startup",
                    False,
                    "Herramienta search_amenities no encontrada",
                )
                return False

            self.log_test(
                "MCP Server startup",
                True,
                f"Servidor MCP iniciado con {len(tools)} herramientas",
            )
            return True

        except Exception as e:
            self.log_test("MCP Server startup", False, f"Error: {str(e)}")
            return False

    async def test_amenities_tool_availability(self):
        """Test que la herramienta amenities está disponible"""
        logger.info("🧪 Testing disponibilidad de herramienta amenities...")

        try:
            # Verificar que la herramienta está registrada
            tools = getattr(mcp, "tools", [])
            amenities_tool = None

            for tool in tools:
                if hasattr(tool, "name") and tool.name == "search_amenities":
                    amenities_tool = tool
                    break

            if not amenities_tool:
                self.log_test(
                    "Amenities tool availability", False, "Herramienta no encontrada"
                )
                return False

            # Verificar que tiene los parámetros correctos
            if hasattr(amenities_tool, "parameters"):
                params = amenities_tool.parameters
                expected_params = [
                    "page",
                    "size",
                    "search",
                    "sort_column",
                    "sort_direction",
                    "group_id",
                    "is_public",
                    "public_searchable",
                    "is_filterable",
                    "homeaway_type",
                    "airbnb_type",
                    "tripadvisor_type",
                    "marriott_type",
                ]

                param_names = [
                    param.get("name", "")
                    for param in params.get("properties", {}).keys()
                ]
                missing_params = [p for p in expected_params if p not in param_names]

                if missing_params:
                    self.log_test(
                        "Amenities tool availability",
                        False,
                        f"Parámetros faltantes: {missing_params}",
                    )
                    return False

            self.log_test(
                "Amenities tool availability",
                True,
                "Herramienta disponible con todos los parámetros",
            )
            return True

        except Exception as e:
            self.log_test("Amenities tool availability", False, f"Error: {str(e)}")
            return False

    async def test_api_connectivity(self):
        """Test conectividad con la API de TrackHS"""
        logger.info("🧪 Testing conectividad con API TrackHS...")

        try:
            # Importar el cliente para verificar conectividad
            from trackhs_mcp.client import TrackHSClient
            from trackhs_mcp.config import get_settings

            settings = get_settings()
            if not settings.trackhs_username or not settings.trackhs_password:
                self.log_test("API connectivity", False, "Credenciales no configuradas")
                return False

            client = TrackHSClient(
                base_url=settings.trackhs_api_url,
                username=settings.trackhs_username,
                password=settings.trackhs_password,
            )

            # Test de conectividad básica
            result = client.get("api/pms/units/amenities", {"page": 1, "size": 1})

            if "_embedded" in result and "amenities" in result["_embedded"]:
                self.log_test(
                    "API connectivity", True, "API TrackHS conectada y respondiendo"
                )
                client.close()
                return True
            else:
                self.log_test("API connectivity", False, "Respuesta de API inválida")
                client.close()
                return False

        except Exception as e:
            self.log_test("API connectivity", False, f"Error de conectividad: {str(e)}")
            return False

    async def test_amenities_functionality(self):
        """Test funcionalidad completa de amenities"""
        logger.info("🧪 Testing funcionalidad completa de amenities...")

        try:
            # Test usando el cliente HTTP directamente (ya que la función MCP es un FunctionTool)
            from trackhs_mcp.client import TrackHSClient
            from trackhs_mcp.config import get_settings

            settings = get_settings()
            client = TrackHSClient(
                base_url=settings.trackhs_api_url,
                username=settings.trackhs_username,
                password=settings.trackhs_password,
            )

            # Test 1: Llamada básica
            result1 = client.get("api/pms/units/amenities", {"page": 1, "size": 5})
            self.results["api_responses"].append(("basic_call", result1))

            basic_success = (
                "_embedded" in result1
                and "amenities" in result1["_embedded"]
                and len(result1["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Basic functionality",
                basic_success,
                f"Llamada básica {'funciona' if basic_success else 'falla'}",
            )

            # Test 2: Búsqueda
            result2 = client.get(
                "api/pms/units/amenities", {"search": "wifi", "size": 3}
            )
            self.results["api_responses"].append(("search_test", result2))

            search_success = (
                "_embedded" in result2
                and "amenities" in result2["_embedded"]
                and len(result2["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Search functionality",
                search_success,
                f"Búsqueda {'funciona' if search_success else 'falla'}",
            )

            # Test 3: Filtros avanzados
            result3 = client.get(
                "api/pms/units/amenities",
                {
                    "isPublic": 1,
                    "isFilterable": 1,
                    "sortColumn": "name",
                    "sortDirection": "asc",
                    "size": 3,
                },
            )
            self.results["api_responses"].append(("advanced_filters", result3))

            advanced_success = (
                "_embedded" in result3
                and "amenities" in result3["_embedded"]
                and len(result3["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "Advanced filters",
                advanced_success,
                f"Filtros avanzados {'funcionan' if advanced_success else 'fallan'}",
            )

            # Test 4: Tipos OTA
            result4 = client.get(
                "api/pms/units/amenities",
                {"airbnbType": "ac", "marriottType": "AIR_CONDITION", "size": 3},
            )
            self.results["api_responses"].append(("ota_types", result4))

            ota_success = (
                "_embedded" in result4
                and "amenities" in result4["_embedded"]
                and len(result4["_embedded"]["amenities"]) > 0
            )

            self.log_test(
                "OTA types",
                ota_success,
                f"Tipos OTA {'funcionan' if ota_success else 'fallan'}",
            )

            client.close()
            return basic_success and search_success and advanced_success and ota_success

        except Exception as e:
            self.log_test("Amenities functionality", False, f"Error: {str(e)}")
            return False

    async def test_error_handling(self):
        """Test manejo de errores"""
        logger.info("🧪 Testing manejo de errores...")

        try:
            from trackhs_mcp.client import TrackHSClient
            from trackhs_mcp.config import get_settings

            settings = get_settings()
            client = TrackHSClient(
                base_url=settings.trackhs_api_url,
                username=settings.trackhs_username,
                password=settings.trackhs_password,
            )

            # Test parámetros inválidos
            try:
                client.get("api/pms/units/amenities", {"page": 0})
                self.log_test("Error handling: Page 0", False, "Debería haber fallado")
            except Exception:
                self.log_test(
                    "Error handling: Page 0", True, "Error manejado correctamente"
                )

            try:
                client.get("api/pms/units/amenities", {"page": -1})
                self.log_test(
                    "Error handling: Negative page", False, "Debería haber fallado"
                )
            except Exception:
                self.log_test(
                    "Error handling: Negative page",
                    True,
                    "Error manejado correctamente",
                )

            client.close()
            return True

        except Exception as e:
            self.log_test("Error handling", False, f"Error: {str(e)}")
            return False

    async def run_all_tests(self):
        """Ejecutar todos los tests E2E"""
        logger.info("🚀 Iniciando tests End-to-End (E2E)...")

        # Test 1: Inicio del servidor
        server_ok = await self.test_mcp_server_startup()
        if not server_ok:
            logger.error("❌ Servidor MCP no inició correctamente. Abortando tests.")
            return self.results

        # Test 2: Disponibilidad de herramienta
        tool_ok = await self.test_amenities_tool_availability()
        if not tool_ok:
            logger.error("❌ Herramienta amenities no disponible. Abortando tests.")
            return self.results

        # Test 3: Conectividad API
        api_ok = await self.test_api_connectivity()
        if not api_ok:
            logger.error("❌ API TrackHS no disponible. Abortando tests.")
            return self.results

        # Test 4: Funcionalidad completa
        await self.test_amenities_functionality()

        # Test 5: Manejo de errores
        await self.test_error_handling()

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
        with open("e2e_test_responses.json", "w") as f:
            json.dump(self.results["api_responses"], f, indent=2, default=str)
        logger.info(f"\n💾 Respuestas de API guardadas en e2e_test_responses.json")

        return self.results


async def main():
    """Función principal"""
    tester = E2EAmenitiesTester()
    results = await tester.run_all_tests()

    # Retornar código de salida basado en resultados
    if results["tests_failed"] > 0:
        logger.error(f"\n❌ {results['tests_failed']} tests fallaron")
        return 1
    else:
        logger.info(f"\n✅ Todos los tests E2E pasaron")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
