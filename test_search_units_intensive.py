#!/usr/bin/env python3
"""
Testing Intensivo de Búsquedas Combinadas para search_units
Simula escenarios reales de usuario con diferentes combinaciones de filtros
"""

import json
import random
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

# Agregar el directorio src al path
sys.path.append("src")

from schemas.unit import SortColumn, SortDirection, UnitSearchParams, UnitStatus
from utils.api_client import TrackHSAPIClient
from utils.exceptions import TrackHSAPIError


class SearchUnitsTester:
    """Tester intensivo para búsquedas de unidades"""

    def __init__(self, base_url: str, username: str, password: str):
        """Inicializar el tester con credenciales de API"""
        self.api_client = TrackHSAPIClient(base_url, username, password)
        self.test_results = []
        self.start_time = time.time()

    def log_test(
        self,
        test_name: str,
        success: bool,
        duration: float,
        params: Dict[str, Any],
        result: Dict[str, Any] = None,
        error: str = None,
    ):
        """Registrar resultado de test"""
        test_result = {
            "test_name": test_name,
            "success": success,
            "duration_ms": round(duration * 1000, 2),
            "params": params,
            "result": result,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(test_result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} ({duration*1000:.1f}ms)")
        if error:
            print(f"    Error: {error}")
        if result and "total_items" in result:
            print(f"    Resultados: {result['total_items']} unidades")

    def run_test(self, test_name: str, params: Dict[str, Any]) -> bool:
        """Ejecutar un test individual"""
        start_time = time.time()

        try:
            # Validar parámetros
            search_params = UnitSearchParams(**params)

            # Realizar búsqueda
            result = self.api_client.search_units(search_params.model_dump())

            duration = time.time() - start_time
            self.log_test(test_name, True, duration, params, result)
            return True

        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, False, duration, params, error=str(e))
            return False

    def test_basic_searches(self):
        """Probar búsquedas básicas"""
        print("\n🔍 TESTING BÚSQUEDAS BÁSICAS")
        print("=" * 50)

        # Test 1: Búsqueda sin filtros
        self.run_test("Búsqueda básica sin filtros", {"page": 1, "size": 10})

        # Test 2: Búsqueda por texto
        self.run_test(
            "Búsqueda por texto 'apartment'",
            {"search": "apartment", "page": 1, "size": 5},
        )

        # Test 3: Búsqueda por código de unidad
        self.run_test(
            "Búsqueda por código de unidad",
            {"unit_code": "APT%", "page": 1, "size": 10},
        )

        # Test 4: Búsqueda por término específico
        self.run_test(
            "Búsqueda por término 'luxury'", {"term": "luxury", "page": 1, "size": 5}
        )

        # Test 5: Búsqueda por nombre corto
        self.run_test(
            "Búsqueda por nombre corto", {"short_name": "SUITE%", "page": 1, "size": 10}
        )

    def test_capacity_filters(self):
        """Probar filtros de capacidad"""
        print("\n🏠 TESTING FILTROS DE CAPACIDAD")
        print("=" * 50)

        # Test 6: Filtro exacto de dormitorios
        self.run_test(
            "Exactamente 2 dormitorios", {"bedrooms": 2, "page": 1, "size": 10}
        )

        # Test 7: Rango de dormitorios
        self.run_test(
            "Entre 1 y 3 dormitorios",
            {"min_bedrooms": 1, "max_bedrooms": 3, "page": 1, "size": 10},
        )

        # Test 8: Mínimo de dormitorios
        self.run_test(
            "Mínimo 2 dormitorios", {"min_bedrooms": 2, "page": 1, "size": 10}
        )

        # Test 9: Filtro exacto de baños
        self.run_test("Exactamente 2 baños", {"bathrooms": 2, "page": 1, "size": 10})

        # Test 10: Rango de baños
        self.run_test(
            "Entre 1 y 2 baños",
            {"min_bathrooms": 1, "max_bathrooms": 2, "page": 1, "size": 10},
        )

        # Test 11: Capacidad exacta
        self.run_test(
            "Capacidad exacta de 4 personas", {"occupancy": 4, "page": 1, "size": 10}
        )

        # Test 12: Rango de capacidad
        self.run_test(
            "Capacidad entre 2 y 6 personas",
            {"min_occupancy": 2, "max_occupancy": 6, "page": 1, "size": 10},
        )

    def test_status_filters(self):
        """Probar filtros de estado"""
        print("\n📊 TESTING FILTROS DE ESTADO")
        print("=" * 50)

        # Test 13: Solo unidades activas
        self.run_test(
            "Solo unidades activas", {"is_active": True, "page": 1, "size": 10}
        )

        # Test 14: Solo unidades reservables
        self.run_test(
            "Solo unidades reservables", {"is_bookable": True, "page": 1, "size": 10}
        )

        # Test 15: Solo unidades pet-friendly
        self.run_test(
            "Solo unidades pet-friendly", {"pets_friendly": True, "page": 1, "size": 10}
        )

        # Test 16: Estado específico
        self.run_test(
            "Unidades limpias", {"unit_status": UnitStatus.CLEAN, "page": 1, "size": 10}
        )

        # Test 17: Unidades ocupadas
        self.run_test(
            "Unidades ocupadas",
            {"unit_status": UnitStatus.OCCUPIED, "page": 1, "size": 10},
        )

        # Test 18: Unidades en inspección
        self.run_test(
            "Unidades en inspección",
            {"unit_status": UnitStatus.INSPECTION, "page": 1, "size": 10},
        )

        # Test 19: Unidades que permiten tarifas por unidad
        self.run_test(
            "Unidades con tarifas por unidad",
            {"allow_unit_rates": True, "page": 1, "size": 10},
        )

    def test_availability_filters(self):
        """Probar filtros de disponibilidad"""
        print("\n📅 TESTING FILTROS DE DISPONIBILIDAD")
        print("=" * 50)

        # Fechas de prueba
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        next_month = today + timedelta(days=30)

        # Test 20: Disponibilidad para mañana
        self.run_test(
            "Disponibles para mañana",
            {"arrival": tomorrow.strftime("%Y-%m-%d"), "page": 1, "size": 10},
        )

        # Test 21: Disponibilidad para próxima semana
        self.run_test(
            "Disponibles para próxima semana",
            {
                "arrival": next_week.strftime("%Y-%m-%d"),
                "departure": (next_week + timedelta(days=3)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 10,
            },
        )

        # Test 22: Disponibilidad para próximo mes
        self.run_test(
            "Disponibles para próximo mes",
            {
                "arrival": next_month.strftime("%Y-%m-%d"),
                "departure": (next_month + timedelta(days=7)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 10,
            },
        )

    def test_content_filters(self):
        """Probar filtros de contenido"""
        print("\n📋 TESTING FILTROS DE CONTENIDO")
        print("=" * 50)

        # Test 23: Con valores computados
        self.run_test(
            "Con valores computados", {"computed": True, "page": 1, "size": 5}
        )

        # Test 24: Con atributos heredados
        self.run_test(
            "Con atributos heredados", {"inherited": True, "page": 1, "size": 5}
        )

        # Test 25: Atributos limitados
        self.run_test("Atributos limitados", {"limited": True, "page": 1, "size": 10})

        # Test 26: Con descripciones
        self.run_test(
            "Con descripciones", {"include_descriptions": True, "page": 1, "size": 5}
        )

        # Test 27: Actualizadas desde hace una semana
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        self.run_test(
            "Actualizadas desde hace una semana",
            {"content_updated_since": week_ago, "page": 1, "size": 10},
        )

    def test_combined_filters(self):
        """Probar combinaciones complejas de filtros"""
        print("\n🔗 TESTING COMBINACIONES COMPLEJAS")
        print("=" * 50)

        # Test 28: Apartamento de lujo
        self.run_test(
            "Apartamento de lujo (2D/2B, activo, pet-friendly)",
            {
                "search": "luxury",
                "bedrooms": 2,
                "bathrooms": 2,
                "is_active": True,
                "pets_friendly": True,
                "page": 1,
                "size": 5,
            },
        )

        # Test 29: Suite ejecutiva disponible
        self.run_test(
            "Suite ejecutiva disponible (3+D, activa, reservable)",
            {
                "search": "suite",
                "min_bedrooms": 3,
                "is_active": True,
                "is_bookable": True,
                "unit_status": UnitStatus.CLEAN,
                "page": 1,
                "size": 5,
            },
        )

        # Test 30: Penthouse con amenidades
        self.run_test(
            "Penthouse con amenidades específicas",
            {
                "search": "penthouse",
                "min_bedrooms": 3,
                "min_bathrooms": 2,
                "min_occupancy": 4,
                "is_active": True,
                "amenity_id": [1, 2, 3],  # IDs de amenidades
                "page": 1,
                "size": 3,
            },
        )

        # Test 31: Unidades familiares disponibles
        self.run_test(
            "Unidades familiares disponibles (4+ personas, pet-friendly)",
            {
                "min_occupancy": 4,
                "pets_friendly": True,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 10,
            },
        )

        # Test 32: Apartamentos económicos
        self.run_test(
            "Apartamentos económicos (1-2D, activos)",
            {
                "search": "apartment",
                "max_bedrooms": 2,
                "max_bathrooms": 1,
                "is_active": True,
                "allow_unit_rates": False,
                "page": 1,
                "size": 10,
            },
        )

        # Test 33: Unidades de lujo con todas las amenidades
        self.run_test(
            "Unidades de lujo con todas las amenidades",
            {
                "search": "luxury",
                "min_bedrooms": 2,
                "is_active": True,
                "amenity_all": [1, 2, 3, 4],  # Debe tener TODAS estas amenidades
                "computed": True,
                "include_descriptions": True,
                "page": 1,
                "size": 5,
            },
        )

    def test_sorting_and_pagination(self):
        """Probar ordenamiento y paginación"""
        print("\n📊 TESTING ORDENAMIENTO Y PAGINACIÓN")
        print("=" * 50)

        # Test 34: Ordenar por ID ascendente
        self.run_test(
            "Ordenar por ID ascendente",
            {
                "sort_column": SortColumn.ID,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Test 35: Ordenar por nombre descendente
        self.run_test(
            "Ordenar por nombre descendente",
            {
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.DESC,
                "page": 1,
                "size": 10,
            },
        )

        # Test 36: Ordenar por nodo ascendente
        self.run_test(
            "Ordenar por nodo ascendente",
            {
                "sort_column": SortColumn.NODE_NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Test 37: Ordenar por tipo de unidad descendente
        self.run_test(
            "Ordenar por tipo de unidad descendente",
            {
                "sort_column": SortColumn.UNIT_TYPE_NAME,
                "sort_direction": SortDirection.DESC,
                "page": 1,
                "size": 10,
            },
        )

        # Test 38: Paginación - página 2
        self.run_test("Paginación - página 2", {"page": 2, "size": 5})

        # Test 39: Paginación - página grande
        self.run_test("Paginación - página 10", {"page": 10, "size": 10})

        # Test 40: Tamaño de página grande
        self.run_test("Tamaño de página grande (50)", {"page": 1, "size": 50})

    def test_edge_cases(self):
        """Probar casos límite y validaciones"""
        print("\n⚠️ TESTING CASOS LÍMITE")
        print("=" * 50)

        # Test 41: Página 0 (debería fallar)
        self.run_test("Página 0 (inválida)", {"page": 0, "size": 10})

        # Test 42: Tamaño 0 (debería fallar)
        self.run_test("Tamaño 0 (inválido)", {"page": 1, "size": 0})

        # Test 43: Tamaño muy grande
        self.run_test("Tamaño muy grande (1000)", {"page": 1, "size": 1000})

        # Test 44: Dormitorios negativos (debería fallar)
        self.run_test(
            "Dormitorios negativos (inválido)", {"bedrooms": -1, "page": 1, "size": 10}
        )

        # Test 45: Fecha inválida (debería fallar)
        self.run_test(
            "Fecha inválida (debería fallar)",
            {"arrival": "2024-13-45", "page": 1, "size": 10},
        )

        # Test 46: Estado inválido (debería fallar)
        self.run_test(
            "Estado inválido (debería fallar)",
            {"unit_status": "invalid_status", "page": 1, "size": 10},
        )

        # Test 47: Columna de ordenamiento inválida (debería fallar)
        self.run_test(
            "Columna de ordenamiento inválida (debería fallar)",
            {"sort_column": "invalid_column", "page": 1, "size": 10},
        )

        # Test 48: Dirección de ordenamiento inválida (debería fallar)
        self.run_test(
            "Dirección de ordenamiento inválida (debería fallar)",
            {"sort_direction": "invalid_direction", "page": 1, "size": 10},
        )

    def test_performance_scenarios(self):
        """Probar escenarios de rendimiento"""
        print("\n⚡ TESTING RENDIMIENTO")
        print("=" * 50)

        # Test 49: Búsqueda con muchos filtros
        self.run_test(
            "Búsqueda con muchos filtros",
            {
                "search": "apartment",
                "bedrooms": 2,
                "bathrooms": 1,
                "min_occupancy": 2,
                "max_occupancy": 4,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": False,
                "unit_status": UnitStatus.CLEAN,
                "computed": True,
                "inherited": True,
                "include_descriptions": True,
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

        # Test 50: Búsqueda con múltiples IDs
        self.run_test(
            "Búsqueda con múltiples IDs",
            {
                "amenity_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "node_id": [1, 2, 3],
                "unit_type_id": [1, 2],
                "page": 1,
                "size": 25,
            },
        )

    def test_real_world_scenarios(self):
        """Probar escenarios del mundo real"""
        print("\n🌍 TESTING ESCENARIOS REALES")
        print("=" * 50)

        # Test 51: Búsqueda de vacaciones familiares
        self.run_test(
            "Vacaciones familiares (4+ personas, pet-friendly, disponible)",
            {
                "min_occupancy": 4,
                "pets_friendly": True,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 15,
            },
        )

        # Test 52: Búsqueda de luna de miel
        self.run_test(
            "Luna de miel (suite, lujo, disponible)",
            {
                "search": "suite",
                "min_bedrooms": 1,
                "min_bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "unit_status": UnitStatus.CLEAN,
                "amenity_id": [1, 2, 3],  # Amenidades de lujo
                "arrival": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 10,
            },
        )

        # Test 53: Búsqueda de viaje de negocios
        self.run_test(
            "Viaje de negocios (apartamento, activo, disponible)",
            {
                "search": "apartment",
                "bedrooms": 1,
                "bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

        # Test 54: Búsqueda de grupo grande
        self.run_test(
            "Grupo grande (6+ personas, múltiples dormitorios)",
            {
                "min_occupancy": 6,
                "min_bedrooms": 3,
                "min_bathrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=67)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 10,
            },
        )

        # Test 55: Búsqueda de última hora
        self.run_test(
            "Última hora (disponible mañana, cualquier tipo)",
            {
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 30,
            },
        )

    def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🚀 INICIANDO TESTING INTENSIVO DE SEARCH_UNITS")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)

        # Ejecutar todas las categorías de tests
        self.test_basic_searches()
        self.test_capacity_filters()
        self.test_status_filters()
        self.test_availability_filters()
        self.test_content_filters()
        self.test_combined_filters()
        self.test_sorting_and_pagination()
        self.test_edge_cases()
        self.test_performance_scenarios()
        self.test_real_world_scenarios()

        # Generar reporte final
        self.generate_report()

    def generate_report(self):
        """Generar reporte final de testing"""
        total_time = time.time() - self.start_time
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["success"])
        failed_tests = total_tests - passed_tests

        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE TESTING")
        print("=" * 60)
        print(f"Total de tests: {total_tests}")
        print(f"Tests exitosos: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Tests fallidos: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"Tiempo total: {total_time:.2f} segundos")
        print(f"Tiempo promedio por test: {total_time/total_tests:.3f} segundos")

        # Mostrar tests fallidos
        if failed_tests > 0:
            print(f"\n❌ TESTS FALLIDOS ({failed_tests}):")
            for test in self.test_results:
                if not test["success"]:
                    print(f"  - {test['test_name']}: {test['error']}")

        # Estadísticas de rendimiento
        durations = [
            test["duration_ms"] for test in self.test_results if test["success"]
        ]
        if durations:
            print(f"\n⚡ ESTADÍSTICAS DE RENDIMIENTO:")
            print(f"  Tiempo mínimo: {min(durations):.1f}ms")
            print(f"  Tiempo máximo: {max(durations):.1f}ms")
            print(f"  Tiempo promedio: {sum(durations)/len(durations):.1f}ms")

        # Guardar reporte detallado
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": {
                        "total_tests": total_tests,
                        "passed_tests": passed_tests,
                        "failed_tests": failed_tests,
                        "success_rate": passed_tests / total_tests * 100,
                        "total_time_seconds": total_time,
                        "average_time_ms": (
                            sum(durations) / len(durations) if durations else 0
                        ),
                    },
                    "tests": self.test_results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\n📄 Reporte detallado guardado en: {report_file}")
        print("=" * 60)


def main():
    """Función principal para ejecutar los tests"""
    # Configuración de la API (cambiar por credenciales reales)
    BASE_URL = "https://api-integration-example.tracksandbox.io"
    USERNAME = "your_username"
    PASSWORD = "your_password"

    print("🔧 CONFIGURACIÓN DE TESTING")
    print("=" * 40)
    print(f"Base URL: {BASE_URL}")
    print(f"Username: {USERNAME}")
    print("=" * 40)

    # Verificar si se proporcionaron credenciales
    if USERNAME == "your_username" or PASSWORD == "your_password":
        print("⚠️  ADVERTENCIA: Usando credenciales de ejemplo")
        print("   Para testing real, actualiza las credenciales en el script")
        print("   Continuando con tests de validación local...")

        # Solo ejecutar tests de validación local
        tester = SearchUnitsTester("", "", "")
        tester.test_validation_only()
    else:
        # Ejecutar tests completos con API
        try:
            tester = SearchUnitsTester(BASE_URL, USERNAME, PASSWORD)
            tester.run_all_tests()
        except Exception as e:
            print(f"❌ Error inicializando tester: {e}")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
