#!/usr/bin/env python3
"""
Test Local de Correcciones - TrackHS MCP Server
Verifica que todas las correcciones implementadas funcionen correctamente
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trackhs_mcp.server import mcp

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")


class TestResults:
    """Clase para manejar resultados de testing"""

    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def add_result(self, test_name: str, success: bool, message: str, data: Any = None):
        """Agregar resultado de test"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self.results.append(result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")

    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE TESTING LOCAL")
        print("=" * 60)
        print(f"Total de tests: {self.total_tests}")
        print(f"Tests exitosos: {self.passed_tests}")
        print(f"Tests fallidos: {self.failed_tests}")
        print(f"Tasa de éxito: {(self.passed_tests/self.total_tests)*100:.1f}%")

        if self.failed_tests > 0:
            print("\n❌ TESTS FALLIDOS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['message']}")

        print("=" * 60)


async def test_search_reservations(test_results: TestResults):
    """Test de búsqueda de reservas"""
    try:
        # Usar la función directamente en lugar de call_tool
        from trackhs_mcp.server import search_reservations

        result = search_reservations(size=3)

        if result and "_embedded" in result and "reservations" in result["_embedded"]:
            test_results.add_result(
                "search_reservations",
                True,
                f"Encontradas {result['total_items']} reservas",
                {
                    "total_items": result["total_items"],
                    "page_size": result["page_size"],
                },
            )
        else:
            test_results.add_result(
                "search_reservations", False, "Respuesta inválida o sin datos", result
            )
    except Exception as e:
        test_results.add_result("search_reservations", False, f"Error: {str(e)}")


async def test_get_reservation(test_results: TestResults):
    """Test de obtención de detalles de reserva"""
    try:
        from trackhs_mcp.server import get_reservation

        result = get_reservation(reservation_id=1)

        if result and "id" in result:
            test_results.add_result(
                "get_reservation",
                True,
                f"Reserva {result['id']} obtenida correctamente",
                {"reservation_id": result["id"], "status": result.get("status", "N/A")},
            )
        else:
            test_results.add_result(
                "get_reservation", False, "Respuesta inválida o sin datos", result
            )
    except Exception as e:
        test_results.add_result("get_reservation", False, f"Error: {str(e)}")


async def test_search_units_with_strings(test_results: TestResults):
    """Test de búsqueda de unidades con parámetros string (problema corregido)"""
    try:
        from trackhs_mcp.server import search_units

        result = search_units(
            bedrooms="2",  # String en lugar de int
            bathrooms="1",  # String en lugar de int
            is_active="1",  # String en lugar de bool
            is_bookable="1",  # String en lugar de bool
            size=5,
        )

        if result and "_embedded" in result and "units" in result["_embedded"]:
            test_results.add_result(
                "search_units_string_params",
                True,
                f"Encontradas {result['total_items']} unidades con parámetros string",
                {
                    "total_items": result["total_items"],
                    "page_size": result["page_size"],
                },
            )
        else:
            test_results.add_result(
                "search_units_string_params",
                False,
                "Respuesta inválida o sin datos",
                result,
            )
    except Exception as e:
        test_results.add_result("search_units_string_params", False, f"Error: {str(e)}")


async def test_search_units_with_ints(test_results: TestResults):
    """Test de búsqueda de unidades con parámetros int (caso normal)"""
    try:
        from trackhs_mcp.server import search_units

        result = search_units(
            bedrooms=2,  # Int normal
            bathrooms=1,  # Int normal
            is_active=True,  # Bool normal
            is_bookable=True,  # Bool normal
            size=5,
        )

        if result and "_embedded" in result and "units" in result["_embedded"]:
            test_results.add_result(
                "search_units_int_params",
                True,
                f"Encontradas {result['total_items']} unidades con parámetros int",
                {
                    "total_items": result["total_items"],
                    "page_size": result["page_size"],
                },
            )
        else:
            test_results.add_result(
                "search_units_int_params",
                False,
                "Respuesta inválida o sin datos",
                result,
            )
    except Exception as e:
        test_results.add_result("search_units_int_params", False, f"Error: {str(e)}")


async def test_search_amenities(test_results: TestResults):
    """Test de búsqueda de amenidades (problema de esquema corregido)"""
    try:
        from trackhs_mcp.server import search_amenities

        result = search_amenities(size=5)

        if result and "_embedded" in result and "amenities" in result["_embedded"]:
            test_results.add_result(
                "search_amenities",
                True,
                f"Encontradas {result['total_items']} amenidades",
                {
                    "total_items": result["total_items"],
                    "page_size": result["page_size"],
                },
            )
        else:
            test_results.add_result(
                "search_amenities", False, "Respuesta inválida o sin datos", result
            )
    except Exception as e:
        test_results.add_result("search_amenities", False, f"Error: {str(e)}")


async def test_get_folio(test_results: TestResults):
    """Test de obtención de folio (problema de endpoint corregido)"""
    try:
        from trackhs_mcp.server import get_folio

        result = get_folio(reservation_id=1)

        if result and "reservation_id" in result:
            test_results.add_result(
                "get_folio",
                True,
                f"Folio para reserva {result['reservation_id']} obtenido correctamente",
                {
                    "reservation_id": result["reservation_id"],
                    "balance": result.get("balance", "N/A"),
                },
            )
        else:
            test_results.add_result(
                "get_folio", False, "Respuesta inválida o sin datos", result
            )
    except Exception as e:
        test_results.add_result("get_folio", False, f"Error: {str(e)}")


async def test_create_maintenance_work_order_strings(test_results: TestResults):
    """Test de creación de orden de mantenimiento con parámetros string (problema corregido)"""
    try:
        from trackhs_mcp.server import create_maintenance_work_order

        result = create_maintenance_work_order(
            unit_id=75,
            summary="Test de aire acondicionado",
            description="Problema reportado por huésped - AC no enfría",
            priority=3,
            estimated_cost="150.50",  # String en lugar de float
            estimated_time="120",  # String en lugar de int
        )

        if result and "id" in result:
            test_results.add_result(
                "create_maintenance_work_order_strings",
                True,
                f"Orden de mantenimiento {result['id']} creada con parámetros string",
                {"order_id": result["id"], "status": result.get("status", "N/A")},
            )
        else:
            test_results.add_result(
                "create_maintenance_work_order_strings",
                False,
                "Respuesta inválida o sin datos",
                result,
            )
    except Exception as e:
        test_results.add_result(
            "create_maintenance_work_order_strings", False, f"Error: {str(e)}"
        )


async def test_create_housekeeping_work_order_strings(test_results: TestResults):
    """Test de creación de orden de housekeeping con parámetros string (problema corregido)"""
    try:
        from trackhs_mcp.server import create_housekeeping_work_order

        result = create_housekeeping_work_order(
            unit_id=75,
            scheduled_at="2024-01-15",
            is_inspection=False,
            clean_type_id="1",  # String en lugar de int
            comments="Limpieza post-checkout urgente",
            cost="80.00",  # String en lugar de float
        )

        if result and "id" in result:
            test_results.add_result(
                "create_housekeeping_work_order_strings",
                True,
                f"Orden de housekeeping {result['id']} creada con parámetros string",
                {"order_id": result["id"], "status": result.get("status", "N/A")},
            )
        else:
            test_results.add_result(
                "create_housekeeping_work_order_strings",
                False,
                "Respuesta inválida o sin datos",
                result,
            )
    except Exception as e:
        test_results.add_result(
            "create_housekeeping_work_order_strings", False, f"Error: {str(e)}"
        )


async def run_all_tests():
    """Ejecutar todos los tests"""
    print("🚀 INICIANDO TESTING LOCAL DE CORRECCIONES")
    print("=" * 60)

    test_results = TestResults()

    # Tests de funcionalidades que ya funcionaban
    await test_search_reservations(test_results)
    await test_get_reservation(test_results)

    # Tests de correcciones implementadas
    await test_search_units_with_strings(test_results)
    await test_search_units_with_ints(test_results)
    await test_search_amenities(test_results)
    await test_get_folio(test_results)
    await test_create_maintenance_work_order_strings(test_results)
    await test_create_housekeeping_work_order_strings(test_results)

    # Imprimir resumen
    test_results.print_summary()

    # Guardar resultados en archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_correcciones_results_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "total_tests": test_results.total_tests,
                    "passed_tests": test_results.passed_tests,
                    "failed_tests": test_results.failed_tests,
                    "success_rate": (
                        (test_results.passed_tests / test_results.total_tests) * 100
                        if test_results.total_tests > 0
                        else 0
                    ),
                },
                "results": test_results.results,
                "timestamp": datetime.now().isoformat(),
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n📄 Resultados guardados en: {filename}")

    return test_results


if __name__ == "__main__":
    asyncio.run(run_all_tests())
