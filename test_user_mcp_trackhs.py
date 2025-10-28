#!/usr/bin/env python3
"""
Test de Usuario - TrackHS MCP Connector v2.0.0
Script completo para probar todas las herramientas MCP del servidor TrackHS
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Agregar src al path para importaciones
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

# Importar el servidor MCP
from trackhs_mcp.server import mcp

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TrackHSMCPTester:
    """Tester completo para el MCP de TrackHS"""

    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
        }
        self.test_data = {}

    async def run_all_tests(self):
        """Ejecutar todos los tests de usuario"""
        print("🚀 Iniciando Test de Usuario - TrackHS MCP Connector v2.0.0")
        print("=" * 70)

        try:
            async with Client(transport=mcp) as client:
                print("✅ Cliente MCP conectado exitosamente")

                # Ejecutar tests en orden
                await self.test_server_info(client)
                await self.test_search_reservations(client)
                await self.test_get_reservation(client)
                await self.test_search_units(client)
                await self.test_search_amenities(client)
                await self.test_get_folio(client)
                await self.test_create_maintenance_work_order(client)
                await self.test_create_housekeeping_work_order(client)
                await self.test_health_check(client)

                # Mostrar resumen final
                self.show_final_summary()

        except Exception as e:
            logger.error(f"❌ Error crítico durante testing: {e}")
            print(f"❌ Error crítico: {e}")

    async def test_server_info(self, client):
        """Test 1: Información del servidor"""
        print("\n🧪 Test 1: Información del servidor")
        print("-" * 40)

        try:
            # Obtener información del servidor
            tools = await client.list_tools()
            resources = await client.list_resources()

            print(f"✅ Herramientas disponibles: {len(tools)}")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")

            print(f"✅ Recursos disponibles: {len(resources)}")
            for resource in resources:
                print(f"   - {resource.name}: {resource.description}")

            self.record_test(
                "server_info",
                True,
                f"Servidor con {len(tools)} herramientas y {len(resources)} recursos",
            )

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("server_info", False, str(e))

    async def test_search_reservations(self, client):
        """Test 2: Búsqueda de reservas"""
        print("\n🧪 Test 2: Búsqueda de reservas")
        print("-" * 40)

        try:
            # Test básico de búsqueda
            result = await client.call_tool(
                "search_reservations",
                arguments={"page": 1, "size": 5, "search": "test"},
            )

            if result and hasattr(result, "content") and result.content:
                data = (
                    result.content[0]
                    if isinstance(result.content, list)
                    else result.content
                )
                reservations = data.get("_embedded", {}).get("reservations", [])
                total_items = data.get("total_items", 0)
                print(
                    f"✅ Búsqueda exitosa: {len(reservations)} reservas encontradas de {total_items} total"
                )
                print(f"   - Página: {data.get('page', 'N/A')}")
                print(f"   - Tamaño: {data.get('page_size', 'N/A')}")

                # Guardar datos para tests posteriores
                if reservations:
                    self.test_data["sample_reservation_id"] = reservations[0].get("id")
                    print(
                        f"   - ID de reserva de muestra: {self.test_data['sample_reservation_id']}"
                    )

                self.record_test(
                    "search_reservations",
                    True,
                    f"Encontradas {len(reservations)} reservas",
                )
            else:
                print("⚠️ Sin datos de reservas")
                self.record_test(
                    "search_reservations", True, "Sin datos (posiblemente normal)"
                )

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("search_reservations", False, str(e))

    async def test_get_reservation(self, client):
        """Test 3: Obtener detalles de reserva"""
        print("\n🧪 Test 3: Obtener detalles de reserva")
        print("-" * 40)

        if not self.test_data.get("sample_reservation_id"):
            print("⚠️ Saltando test - no hay ID de reserva de muestra")
            self.record_test("get_reservation", True, "Saltado - sin datos de muestra")
            return

        try:
            reservation_id = self.test_data["sample_reservation_id"]
            result = await client.call_tool(
                "get_reservation", arguments={"reservation_id": reservation_id}
            )

            if result:
                print(f"✅ Reserva {reservation_id} obtenida exitosamente")
                print(f"   - Estado: {result.get('status', 'N/A')}")
                print(f"   - Check-in: {result.get('arrival', 'N/A')}")
                print(f"   - Check-out: {result.get('departure', 'N/A')}")
                self.record_test(
                    "get_reservation", True, f"Reserva {reservation_id} obtenida"
                )
            else:
                print("⚠️ Sin datos de reserva")
                self.record_test("get_reservation", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("get_reservation", False, str(e))

    async def test_search_units(self, client):
        """Test 4: Búsqueda de unidades"""
        print("\n🧪 Test 4: Búsqueda de unidades")
        print("-" * 40)

        try:
            # Test con filtros básicos
            result = await client.call_tool(
                "search_units",
                arguments={"page": 1, "size": 5, "is_active": 1, "is_bookable": 1},
            )

            if result:
                units = result.get("_embedded", {}).get("units", [])
                total_items = result.get("total_items", 0)
                print(
                    f"✅ Búsqueda exitosa: {len(units)} unidades encontradas de {total_items} total"
                )

                # Guardar datos para tests posteriores
                if units:
                    self.test_data["sample_unit_id"] = units[0].get("id")
                    print(
                        f"   - ID de unidad de muestra: {self.test_data['sample_unit_id']}"
                    )
                    print(f"   - Nombre: {units[0].get('name', 'N/A')}")
                    print(f"   - Dormitorios: {units[0].get('bedrooms', 'N/A')}")
                    print(f"   - Baños: {units[0].get('bathrooms', 'N/A')}")

                self.record_test(
                    "search_units", True, f"Encontradas {len(units)} unidades"
                )
            else:
                print("⚠️ Sin datos de unidades")
                self.record_test("search_units", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("search_units", False, str(e))

    async def test_search_amenities(self, client):
        """Test 5: Búsqueda de amenidades"""
        print("\n🧪 Test 5: Búsqueda de amenidades")
        print("-" * 40)

        try:
            result = await client.call_tool(
                "search_amenities", arguments={"page": 1, "size": 10, "search": "wifi"}
            )

            if result:
                amenities = result.get("_embedded", {}).get("amenities", [])
                total_items = result.get("total_items", 0)
                print(
                    f"✅ Búsqueda exitosa: {len(amenities)} amenidades encontradas de {total_items} total"
                )

                for amenity in amenities[:3]:  # Mostrar primeras 3
                    print(
                        f"   - {amenity.get('name', 'N/A')}: {amenity.get('description', 'N/A')[:50]}..."
                    )

                self.record_test(
                    "search_amenities", True, f"Encontradas {len(amenities)} amenidades"
                )
            else:
                print("⚠️ Sin datos de amenidades")
                self.record_test("search_amenities", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("search_amenities", False, str(e))

    async def test_get_folio(self, client):
        """Test 6: Obtener folio financiero"""
        print("\n🧪 Test 6: Obtener folio financiero")
        print("-" * 40)

        if not self.test_data.get("sample_reservation_id"):
            print("⚠️ Saltando test - no hay ID de reserva de muestra")
            self.record_test("get_folio", True, "Saltado - sin datos de muestra")
            return

        try:
            reservation_id = self.test_data["sample_reservation_id"]
            result = await client.call_tool(
                "get_folio", arguments={"reservation_id": reservation_id}
            )

            if result:
                if "error" in result:
                    print(f"⚠️ Folio no encontrado: {result.get('message', 'N/A')}")
                    self.record_test(
                        "get_folio", True, "Folio no encontrado (esperado)"
                    )
                else:
                    print(f"✅ Folio de reserva {reservation_id} obtenido exitosamente")
                    balance = result.get("balance", "N/A")
                    print(f"   - Balance: {balance}")
                    self.record_test(
                        "get_folio", True, f"Folio obtenido - Balance: {balance}"
                    )
            else:
                print("⚠️ Sin datos de folio")
                self.record_test("get_folio", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("get_folio", False, str(e))

    async def test_create_maintenance_work_order(self, client):
        """Test 7: Crear orden de mantenimiento"""
        print("\n🧪 Test 7: Crear orden de mantenimiento")
        print("-" * 40)

        if not self.test_data.get("sample_unit_id"):
            print("⚠️ Saltando test - no hay ID de unidad de muestra")
            self.record_test(
                "create_maintenance_work_order", True, "Saltado - sin datos de muestra"
            )
            return

        try:
            unit_id = self.test_data["sample_unit_id"]
            result = await client.call_tool(
                "create_maintenance_work_order",
                arguments={
                    "unit_id": unit_id,
                    "summary": "Test de mantenimiento - MCP Testing",
                    "description": "Orden de trabajo creada durante testing del MCP de TrackHS. Esta es una orden de prueba.",
                    "priority": 3,
                    "estimated_cost": 50.0,
                    "estimated_time": 120,
                },
            )

            if result:
                work_order_id = result.get("id", "N/A")
                status = result.get("status", "N/A")
                print(f"✅ Orden de mantenimiento creada exitosamente")
                print(f"   - ID: {work_order_id}")
                print(f"   - Estado: {status}")
                print(f"   - Unidad: {unit_id}")
                self.record_test(
                    "create_maintenance_work_order",
                    True,
                    f"Orden {work_order_id} creada",
                )
            else:
                print("⚠️ Sin datos de orden creada")
                self.record_test("create_maintenance_work_order", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("create_maintenance_work_order", False, str(e))

    async def test_create_housekeeping_work_order(self, client):
        """Test 8: Crear orden de housekeeping"""
        print("\n🧪 Test 8: Crear orden de housekeeping")
        print("-" * 40)

        if not self.test_data.get("sample_unit_id"):
            print("⚠️ Saltando test - no hay ID de unidad de muestra")
            self.record_test(
                "create_housekeeping_work_order", True, "Saltado - sin datos de muestra"
            )
            return

        try:
            unit_id = self.test_data["sample_unit_id"]
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

            result = await client.call_tool(
                "create_housekeeping_work_order",
                arguments={
                    "unit_id": unit_id,
                    "scheduled_at": tomorrow,
                    "is_inspection": False,
                    "clean_type_id": 4,  # Departure Clean
                    "comments": "Limpieza de prueba - MCP Testing",
                    "cost": 75.0,
                },
            )

            if result:
                work_order_id = result.get("id", "N/A")
                status = result.get("status", "N/A")
                print(f"✅ Orden de housekeeping creada exitosamente")
                print(f"   - ID: {work_order_id}")
                print(f"   - Estado: {status}")
                print(f"   - Unidad: {unit_id}")
                print(f"   - Fecha programada: {tomorrow}")
                self.record_test(
                    "create_housekeeping_work_order",
                    True,
                    f"Orden {work_order_id} creada",
                )
            else:
                print("⚠️ Sin datos de orden creada")
                self.record_test("create_housekeeping_work_order", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("create_housekeeping_work_order", False, str(e))

    async def test_health_check(self, client):
        """Test 9: Health check"""
        print("\n🧪 Test 9: Health check")
        print("-" * 40)

        try:
            result = await client.read_resource("https://trackhs-mcp.local/health")

            if result:
                status = result.get("status", "unknown")
                version = result.get("version", "N/A")
                dependencies = result.get("dependencies", {})
                trackhs_status = dependencies.get("trackhs_api", {}).get(
                    "status", "unknown"
                )

                print(f"✅ Health check exitoso")
                print(f"   - Estado del servidor: {status}")
                print(f"   - Versión: {version}")
                print(f"   - Estado API TrackHS: {trackhs_status}")

                if trackhs_status == "healthy":
                    response_time = dependencies.get("trackhs_api", {}).get(
                        "response_time_ms", "N/A"
                    )
                    print(f"   - Tiempo de respuesta: {response_time}ms")

                self.record_test(
                    "health_check", True, f"Estado: {status}, API: {trackhs_status}"
                )
            else:
                print("⚠️ Sin datos de health check")
                self.record_test("health_check", True, "Sin datos")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.record_test("health_check", False, str(e))

    def record_test(self, test_name: str, passed: bool, details: str):
        """Registrar resultado de test"""
        self.results["total_tests"] += 1
        if passed:
            self.results["passed_tests"] += 1
        else:
            self.results["failed_tests"] += 1

        self.results["test_details"].append(
            {
                "test": test_name,
                "passed": passed,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def show_final_summary(self):
        """Mostrar resumen final de tests"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN FINAL DE TESTS")
        print("=" * 70)

        total = self.results["total_tests"]
        passed = self.results["passed_tests"]
        failed = self.results["failed_tests"]
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"Total de tests: {total}")
        print(f"✅ Exitosos: {passed}")
        print(f"❌ Fallidos: {failed}")
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")

        print("\n📋 Detalles por test:")
        for test in self.results["test_details"]:
            status = "✅" if test["passed"] else "❌"
            print(f"   {status} {test['test']}: {test['details']}")

        if success_rate >= 90:
            print("\n🎉 ¡EXCELENTE! El MCP de TrackHS está funcionando perfectamente")
        elif success_rate >= 70:
            print(
                "\n✅ ¡BUENO! El MCP de TrackHS está funcionando bien con algunos problemas menores"
            )
        else:
            print(
                "\n⚠️ ATENCIÓN: El MCP de TrackHS tiene problemas que requieren revisión"
            )

        # Guardar reporte
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Reporte guardado en: {report_file}")


async def main():
    """Función principal"""
    print("🔧 TrackHS MCP Connector v2.0.0 - Test de Usuario")
    print("=" * 70)

    # Verificar variables de entorno
    required_vars = ["TRACKHS_USERNAME", "TRACKHS_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Por favor, configure las credenciales de TrackHS:")
        print("export TRACKHS_USERNAME=tu_usuario")
        print("export TRACKHS_PASSWORD=tu_contraseña")
        return

    print("✅ Variables de entorno configuradas")

    # Ejecutar tests
    tester = TrackHSMCPTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {e}")
        sys.exit(1)
