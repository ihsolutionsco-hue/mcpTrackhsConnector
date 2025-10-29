#!/usr/bin/env python3
"""
Testing de Escenarios de Usuario para search_units
Simula búsquedas reales que harían los usuarios finales
"""

import json
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Agregar el directorio src al path
sys.path.append("src")

from schemas.unit import SortColumn, SortDirection, UnitSearchParams, UnitStatus


class UserScenarioTester:
    """Tester para escenarios reales de usuario"""

    def __init__(self):
        self.test_results = []
        self.start_time = time.time()

    def log_test(
        self,
        test_name: str,
        success: bool,
        duration: float,
        params: Dict[str, Any],
        error: str = None,
    ):
        """Registrar resultado de test"""
        test_result = {
            "test_name": test_name,
            "success": success,
            "duration_ms": round(duration * 1000, 2),
            "params": params,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(test_result)

        status = "PASS" if success else "FAIL"
        print(f"{status} {test_name} ({duration*1000:.1f}ms)")
        if error:
            print(f"    Error: {error}")

    def run_scenario_test(self, test_name: str, params: Dict[str, Any]) -> bool:
        """Ejecutar un test de escenario"""
        start_time = time.time()

        try:
            # Validar parámetros
            search_params = UnitSearchParams(**params)

            # Simular procesamiento (sin API real)
            duration = time.time() - start_time
            self.log_test(test_name, True, duration, params)
            return True

        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, False, duration, params, error=str(e))
            return False

    def test_family_vacation_scenarios(self):
        """Probar escenarios de vacaciones familiares"""
        print("\n[FAMILY] ESCENARIOS DE VACACIONES FAMILIARES")
        print("=" * 60)

        # Escenario 1: Familia con niños pequeños
        self.run_scenario_test(
            "Familia con niños pequeños (4 personas, pet-friendly)",
            {
                "min_occupancy": 4,
                "pets_friendly": True,
                "is_active": True,
                "is_bookable": True,
                "min_bedrooms": 2,
                "min_bathrooms": 1,
                "arrival": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 15,
            },
        )

        # Escenario 2: Familia numerosa
        self.run_scenario_test(
            "Familia numerosa (6+ personas, múltiples dormitorios)",
            {
                "min_occupancy": 6,
                "min_bedrooms": 3,
                "min_bathrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=67)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Escenario 3: Familia con mascotas
        self.run_scenario_test(
            "Familia con mascotas (pet-friendly, patio)",
            {
                "min_occupancy": 4,
                "pets_friendly": True,
                "is_active": True,
                "is_bookable": True,
                "search": "patio",
                "min_bedrooms": 2,
                "arrival": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=52)).strftime("%Y-%m-%d"),
                "page": 1,
                "size": 12,
            },
        )

        # Escenario 4: Familia en presupuesto
        self.run_scenario_test(
            "Familia en presupuesto (apartamento económico)",
            {
                "search": "apartment",
                "max_bedrooms": 2,
                "max_bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 3,
                "max_occupancy": 4,
                "arrival": (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=27)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

    def test_couple_scenarios(self):
        """Probar escenarios de parejas"""
        print("\n[COUPLE] ESCENARIOS DE PAREJAS")
        print("=" * 60)

        # Escenario 5: Luna de miel
        self.run_scenario_test(
            "Luna de miel (suite de lujo, romántico)",
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
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Escenario 6: Aniversario
        self.run_scenario_test(
            "Aniversario (penthouse, vista al mar)",
            {
                "search": "penthouse",
                "min_bedrooms": 1,
                "min_bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "term": "vista",
                "arrival": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=97)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 8,
            },
        )

        # Escenario 7: Escapada de fin de semana
        self.run_scenario_test(
            "Escapada de fin de semana (cerca del centro)",
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
                "size": 15,
            },
        )

        # Escenario 8: Viaje de negocios
        self.run_scenario_test(
            "Viaje de negocios (apartamento funcional)",
            {
                "search": "apartment",
                "bedrooms": 1,
                "bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

    def test_group_scenarios(self):
        """Probar escenarios de grupos"""
        print("\n[GROUP] ESCENARIOS DE GRUPOS")
        print("=" * 60)

        # Escenario 9: Grupo de amigos
        self.run_scenario_test(
            "Grupo de amigos (6-8 personas, fiesta)",
            {
                "min_occupancy": 6,
                "max_occupancy": 8,
                "min_bedrooms": 3,
                "min_bathrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=28)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Escenario 10: Grupo corporativo
        self.run_scenario_test(
            "Grupo corporativo (múltiples unidades)",
            {
                "min_occupancy": 2,
                "max_occupancy": 4,
                "min_bedrooms": 1,
                "min_bathrooms": 1,
                "is_active": True,
                "is_bookable": True,
                "unit_type_id": [1, 2],  # Tipos específicos
                "arrival": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=17)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.UNIT_TYPE_NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 25,
            },
        )

        # Escenario 11: Grupo deportivo
        self.run_scenario_test(
            "Grupo deportivo (cerca de instalaciones)",
            {
                "min_occupancy": 4,
                "max_occupancy": 6,
                "min_bedrooms": 2,
                "min_bathrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "search": "deportes",
                "arrival": (datetime.now() + timedelta(days=35)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=42)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 12,
            },
        )

    def test_luxury_scenarios(self):
        """Probar escenarios de lujo"""
        print("\n[LUXURY] ESCENARIOS DE LUJO")
        print("=" * 60)

        # Escenario 12: Penthouse de lujo
        self.run_scenario_test(
            "Penthouse de lujo (todas las amenidades)",
            {
                "search": "penthouse",
                "min_bedrooms": 3,
                "min_bathrooms": 3,
                "min_occupancy": 4,
                "is_active": True,
                "is_bookable": True,
                "amenity_all": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Todas las amenidades
                "computed": True,
                "include_descriptions": True,
                "arrival": (datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=127)).strftime(
                    "%Y-%m-%d"
                ),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 5,
            },
        )

        # Escenario 13: Suite presidencial
        self.run_scenario_test(
            "Suite presidencial (máximo confort)",
            {
                "search": "suite",
                "term": "presidencial",
                "min_bedrooms": 2,
                "min_bathrooms": 2,
                "min_occupancy": 2,
                "is_active": True,
                "is_bookable": True,
                "unit_status": UnitStatus.CLEAN,
                "amenity_id": [1, 2, 3, 4, 5],  # Amenidades premium
                "computed": True,
                "inherited": True,
                "include_descriptions": True,
                "arrival": (datetime.now() + timedelta(days=150)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=157)).strftime(
                    "%Y-%m-%d"
                ),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 3,
            },
        )

        # Escenario 14: Villa privada
        self.run_scenario_test(
            "Villa privada (privacidad total)",
            {
                "search": "villa",
                "min_bedrooms": 4,
                "min_bathrooms": 3,
                "min_occupancy": 8,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "amenity_all": [1, 2, 3, 4, 5, 6, 7, 8],  # Muchas amenidades
                "computed": True,
                "include_descriptions": True,
                "arrival": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=194)).strftime(
                    "%Y-%m-%d"
                ),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 2,
            },
        )

    def test_last_minute_scenarios(self):
        """Probar escenarios de última hora"""
        print("\n[URGENT] ESCENARIOS DE ÚLTIMA HORA")
        print("=" * 60)

        # Escenario 15: Disponible mañana
        self.run_scenario_test(
            "Disponible mañana (cualquier tipo)",
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

        # Escenario 16: Disponible esta semana
        self.run_scenario_test(
            "Disponible esta semana (apartamento)",
            {
                "search": "apartment",
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 25,
            },
        )

        # Escenario 17: Disponible este fin de semana
        self.run_scenario_test(
            "Disponible este fin de semana (cualquier tipo)",
            {
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

    def test_special_requirements_scenarios(self):
        """Probar escenarios con requisitos especiales"""
        print("\n[SPECIAL] ESCENARIOS CON REQUISITOS ESPECIALES")
        print("=" * 60)

        # Escenario 18: Accesibilidad
        self.run_scenario_test(
            "Accesibilidad (silla de ruedas)",
            {
                "search": "accesible",
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 2,
                "arrival": (datetime.now() + timedelta(days=25)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=32)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 15,
            },
        )

        # Escenario 19: Mascotas grandes
        self.run_scenario_test(
            "Mascotas grandes (patio, espacio)",
            {
                "pets_friendly": True,
                "is_active": True,
                "is_bookable": True,
                "search": "patio",
                "min_occupancy": 2,
                "arrival": (datetime.now() + timedelta(days=40)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=47)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 12,
            },
        )

        # Escenario 20: Larga estancia
        self.run_scenario_test(
            "Larga estancia (1+ mes, descuento)",
            {
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 2,
                "arrival": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

        # Escenario 21: Evento especial
        self.run_scenario_test(
            "Evento especial (boda, aniversario)",
            {
                "search": "evento",
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 4,
                "min_bedrooms": 2,
                "min_bathrooms": 2,
                "arrival": (datetime.now() + timedelta(days=100)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=107)).strftime(
                    "%Y-%m-%d"
                ),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 8,
            },
        )

    def test_complex_combinations(self):
        """Probar combinaciones complejas reales"""
        print("\n[COMPLEX] COMBINACIONES COMPLEJAS REALES")
        print("=" * 60)

        # Escenario 22: Búsqueda completa de lujo
        self.run_scenario_test(
            "Búsqueda completa de lujo (múltiples filtros)",
            {
                "search": "luxury",
                "term": "penthouse",
                "min_bedrooms": 3,
                "min_bathrooms": 2,
                "min_occupancy": 4,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "unit_status": UnitStatus.CLEAN,
                "amenity_id": [1, 2, 3, 4, 5],
                "amenity_all": [1, 2, 3],
                "computed": True,
                "include_descriptions": True,
                "arrival": (datetime.now() + timedelta(days=75)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=82)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Escenario 23: Búsqueda de emergencia
        self.run_scenario_test(
            "Búsqueda de emergencia (máxima flexibilidad)",
            {
                "is_active": True,
                "is_bookable": True,
                "arrival": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 50,
            },
        )

        # Escenario 24: Búsqueda corporativa
        self.run_scenario_test(
            "Búsqueda corporativa (múltiples unidades)",
            {
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 1,
                "max_occupancy": 2,
                "min_bedrooms": 1,
                "min_bathrooms": 1,
                "unit_type_id": [1, 2, 3],
                "node_id": [1, 2],
                "arrival": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                "departure": (datetime.now() + timedelta(days=22)).strftime("%Y-%m-%d"),
                "sort_column": SortColumn.UNIT_TYPE_NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 30,
            },
        )

        # Escenario 25: Búsqueda de temporada alta
        self.run_scenario_test(
            "Búsqueda de temporada alta (verano)",
            {
                "is_active": True,
                "is_bookable": True,
                "min_occupancy": 2,
                "arrival": "2024-07-01",
                "departure": "2024-07-08",
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 25,
            },
        )

    def run_all_scenarios(self):
        """Ejecutar todos los escenarios de usuario"""
        print("[START] INICIANDO TESTING DE ESCENARIOS DE USUARIO")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 70)

        # Ejecutar todas las categorías de escenarios
        self.test_family_vacation_scenarios()
        self.test_couple_scenarios()
        self.test_group_scenarios()
        self.test_luxury_scenarios()
        self.test_last_minute_scenarios()
        self.test_special_requirements_scenarios()
        self.test_complex_combinations()

        # Generar reporte final
        self.generate_report()

    def generate_report(self):
        """Generar reporte final de escenarios"""
        total_time = time.time() - self.start_time
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["success"])
        failed_tests = total_tests - passed_tests

        print("\n" + "=" * 70)
        print("[REPORT] REPORTE FINAL DE ESCENARIOS DE USUARIO")
        print("=" * 70)
        print(f"Total de escenarios: {total_tests}")
        print(
            f"Escenarios exitosos: {passed_tests} ({passed_tests/total_tests*100:.1f}%)"
        )
        print(
            f"Escenarios fallidos: {failed_tests} ({failed_tests/total_tests*100:.1f}%)"
        )
        print(f"Tiempo total: {total_time:.2f} segundos")
        print(f"Tiempo promedio por escenario: {total_time/total_tests:.3f} segundos")

        # Mostrar escenarios fallidos
        if failed_tests > 0:
            print(f"\n[ERROR] ESCENARIOS FALLIDOS ({failed_tests}):")
            for test in self.test_results:
                if not test["success"]:
                    print(f"  - {test['test_name']}: {test['error']}")

        # Estadísticas de rendimiento
        durations = [
            test["duration_ms"] for test in self.test_results if test["success"]
        ]
        if durations:
            print(f"\n[PERF] ESTADISTICAS DE RENDIMIENTO:")
            print(f"  Tiempo mínimo: {min(durations):.1f}ms")
            print(f"  Tiempo máximo: {max(durations):.1f}ms")
            print(f"  Tiempo promedio: {sum(durations)/len(durations):.1f}ms")

        # Análisis por categoría
        categories = {}
        for test in self.test_results:
            category = test["test_name"].split(" ")[0]
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            categories[category]["total"] += 1
            if test["success"]:
                categories[category]["passed"] += 1

        print(f"\n[CATEGORIES] ANALISIS POR CATEGORIA:")
        for category, stats in categories.items():
            success_rate = stats["passed"] / stats["total"] * 100
            print(
                f"  {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)"
            )

        # Guardar reporte detallado
        report_file = (
            f"user_scenarios_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": {
                        "total_scenarios": total_tests,
                        "passed_scenarios": passed_tests,
                        "failed_scenarios": failed_tests,
                        "success_rate": passed_tests / total_tests * 100,
                        "total_time_seconds": total_time,
                        "average_time_ms": (
                            sum(durations) / len(durations) if durations else 0
                        ),
                        "categories": categories,
                    },
                    "scenarios": self.test_results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\n[FILE] Reporte detallado guardado en: {report_file}")
        print("=" * 70)


def main():
    """Función principal para ejecutar los escenarios de usuario"""
    print("[CONFIG] TESTING DE ESCENARIOS DE USUARIO")
    print("=" * 50)
    print("Simulando búsquedas reales de usuarios finales")
    print("=" * 50)

    # Ejecutar escenarios de usuario
    tester = UserScenarioTester()
    tester.run_all_scenarios()

    return 0


if __name__ == "__main__":
    exit(main())
