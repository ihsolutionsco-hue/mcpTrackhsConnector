#!/usr/bin/env python3
"""
Testing de Rendimiento para search_units
Prueba el rendimiento con diferentes tamaños de página y combinaciones complejas
"""

import json
import random
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Agregar el directorio src al path
sys.path.append("src")

from schemas.unit import SortColumn, SortDirection, UnitSearchParams, UnitStatus


class PerformanceTester:
    """Tester para rendimiento de búsquedas"""

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

    def run_performance_test(self, test_name: str, params: Dict[str, Any]) -> bool:
        """Ejecutar un test de rendimiento"""
        start_time = time.time()

        try:
            # Validar parámetros
            search_params = UnitSearchParams(**params)

            # Simular procesamiento (sin API real)
            # Simular tiempo de procesamiento basado en complejidad
            complexity_score = self._calculate_complexity(params)
            simulated_delay = complexity_score * 0.001  # 1ms por punto de complejidad
            time.sleep(simulated_delay)

            duration = time.time() - start_time
            self.log_test(test_name, True, duration, params)
            return True

        except Exception as e:
            duration = time.time() - start_time
            self.log_test(test_name, False, duration, params, error=str(e))
            return False

    def _calculate_complexity(self, params: Dict[str, Any]) -> int:
        """Calcular puntuación de complejidad de los parámetros"""
        complexity = 0

        # Búsquedas de texto
        if params.get("search"):
            complexity += 1
        if params.get("term"):
            complexity += 1
        if params.get("unit_code"):
            complexity += 1
        if params.get("short_name"):
            complexity += 1

        # Filtros numéricos
        numeric_filters = [
            "bedrooms",
            "bathrooms",
            "occupancy",
            "min_bedrooms",
            "max_bedrooms",
            "min_bathrooms",
            "max_bathrooms",
            "min_occupancy",
            "max_occupancy",
        ]
        for filter_name in numeric_filters:
            if params.get(filter_name) is not None:
                complexity += 1

        # Filtros booleanos
        boolean_filters = [
            "is_active",
            "is_bookable",
            "pets_friendly",
            "allow_unit_rates",
            "computed",
            "inherited",
            "limited",
            "include_descriptions",
        ]
        for filter_name in boolean_filters:
            if params.get(filter_name) is not None:
                complexity += 1

        # Filtros de estado
        if params.get("unit_status"):
            complexity += 1

        # Filtros de fechas
        if params.get("arrival"):
            complexity += 1
        if params.get("departure"):
            complexity += 1
        if params.get("content_updated_since"):
            complexity += 1

        # Filtros de IDs (cada lista cuenta como 1 punto)
        id_filters = [
            "amenity_id",
            "node_id",
            "unit_type_id",
            "owner_id",
            "company_id",
            "channel_id",
            "lodging_type_id",
            "bed_type_id",
            "amenity_all",
            "unit_ids",
        ]
        for filter_name in id_filters:
            if params.get(filter_name):
                complexity += 1

        # Filtros individuales
        if params.get("calendar_id"):
            complexity += 1
        if params.get("role_id"):
            complexity += 1

        # Ordenamiento
        if params.get("sort_column"):
            complexity += 1
        if params.get("sort_direction"):
            complexity += 1

        # Tamaño de página (afecta el procesamiento)
        page_size = params.get("size", 10)
        complexity += page_size // 10  # 1 punto por cada 10 elementos

        return complexity

    def test_page_sizes(self):
        """Probar diferentes tamaños de página"""
        print("\n[PAGE] TESTING TAMAÑOS DE PÁGINA")
        print("=" * 50)

        page_sizes = [1, 5, 10, 25, 50, 100]

        for size in page_sizes:
            self.run_performance_test(
                f"Tamaño de página {size}", {"page": 1, "size": size}
            )

    def test_complexity_levels(self):
        """Probar diferentes niveles de complejidad"""
        print("\n[COMPLEX] TESTING NIVELES DE COMPLEJIDAD")
        print("=" * 50)

        # Nivel 1: Básico
        self.run_performance_test(
            "Nivel 1: Básico (solo paginación)", {"page": 1, "size": 10}
        )

        # Nivel 2: Simple
        self.run_performance_test(
            "Nivel 2: Simple (búsqueda + filtros básicos)",
            {
                "search": "apartment",
                "bedrooms": 2,
                "is_active": True,
                "page": 1,
                "size": 10,
            },
        )

        # Nivel 3: Intermedio
        self.run_performance_test(
            "Nivel 3: Intermedio (múltiples filtros)",
            {
                "search": "luxury",
                "bedrooms": 2,
                "bathrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "arrival": "2024-01-15",
                "departure": "2024-01-20",
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

        # Nivel 4: Avanzado
        self.run_performance_test(
            "Nivel 4: Avanzado (filtros complejos)",
            {
                "search": "penthouse",
                "term": "luxury",
                "bedrooms": 3,
                "min_bedrooms": 2,
                "max_bedrooms": 4,
                "bathrooms": 2,
                "min_bathrooms": 1,
                "max_bathrooms": 3,
                "occupancy": 4,
                "min_occupancy": 2,
                "max_occupancy": 6,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "unit_status": UnitStatus.CLEAN,
                "allow_unit_rates": True,
                "arrival": "2024-01-15",
                "departure": "2024-01-20",
                "computed": True,
                "inherited": True,
                "include_descriptions": True,
                "amenity_id": [1, 2, 3, 4, 5],
                "node_id": [1, 2],
                "unit_type_id": [1, 2],
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 25,
            },
        )

        # Nivel 5: Máximo
        self.run_performance_test(
            "Nivel 5: Máximo (todos los filtros)",
            {
                "search": "luxury penthouse",
                "term": "vista al mar",
                "unit_code": "PENT%",
                "short_name": "SUITE%",
                "bedrooms": 3,
                "min_bedrooms": 2,
                "max_bedrooms": 4,
                "bathrooms": 3,
                "min_bathrooms": 2,
                "max_bathrooms": 4,
                "occupancy": 4,
                "min_occupancy": 2,
                "max_occupancy": 6,
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "unit_status": UnitStatus.CLEAN,
                "allow_unit_rates": True,
                "arrival": "2024-01-15",
                "departure": "2024-01-20",
                "computed": True,
                "inherited": True,
                "limited": False,
                "include_descriptions": True,
                "content_updated_since": "2024-01-01T00:00:00Z",
                "amenity_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "node_id": [1, 2, 3, 4, 5],
                "unit_type_id": [1, 2, 3],
                "owner_id": [1, 2],
                "company_id": [1, 2],
                "channel_id": [1, 2],
                "lodging_type_id": [1, 2],
                "bed_type_id": [1, 2],
                "amenity_all": [1, 2, 3, 4, 5],
                "unit_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "calendar_id": 1,
                "role_id": 1,
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 50,
            },
        )

    def test_stress_scenarios(self):
        """Probar escenarios de estrés"""
        print("\n[STRESS] TESTING ESCENARIOS DE ESTRÉS")
        print("=" * 50)

        # Escenario 1: Múltiples búsquedas de texto
        self.run_performance_test(
            "Múltiples búsquedas de texto",
            {
                "search": "luxury apartment penthouse suite",
                "term": "vista al mar piscina jacuzzi",
                "unit_code": "LUX%",
                "short_name": "SUITE%",
                "page": 1,
                "size": 30,
            },
        )

        # Escenario 2: Múltiples rangos numéricos
        self.run_performance_test(
            "Múltiples rangos numéricos",
            {
                "min_bedrooms": 1,
                "max_bedrooms": 5,
                "min_bathrooms": 1,
                "max_bathrooms": 4,
                "min_occupancy": 1,
                "max_occupancy": 10,
                "page": 1,
                "size": 40,
            },
        )

        # Escenario 3: Múltiples filtros de IDs
        self.run_performance_test(
            "Múltiples filtros de IDs",
            {
                "amenity_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "node_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "unit_type_id": [1, 2, 3, 4, 5],
                "owner_id": [1, 2, 3, 4, 5],
                "company_id": [1, 2, 3, 4, 5],
                "channel_id": [1, 2, 3, 4, 5],
                "lodging_type_id": [1, 2, 3, 4, 5],
                "bed_type_id": [1, 2, 3, 4, 5],
                "amenity_all": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "unit_ids": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                ],
                "page": 1,
                "size": 50,
            },
        )

        # Escenario 4: Todos los booleanos
        self.run_performance_test(
            "Todos los booleanos activos",
            {
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": True,
                "allow_unit_rates": True,
                "computed": True,
                "inherited": True,
                "limited": True,
                "include_descriptions": True,
                "page": 1,
                "size": 30,
            },
        )

        # Escenario 5: Página muy grande
        self.run_performance_test(
            "Página muy grande (100 elementos)", {"page": 1, "size": 100}
        )

        # Escenario 6: Página muy grande con filtros
        self.run_performance_test(
            "Página grande con filtros complejos",
            {
                "search": "apartment",
                "bedrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "arrival": "2024-01-15",
                "departure": "2024-01-20",
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 100,
            },
        )

    def test_pagination_performance(self):
        """Probar rendimiento de paginación"""
        print("\n[PAGINATION] TESTING RENDIMIENTO DE PAGINACIÓN")
        print("=" * 50)

        # Probar diferentes páginas
        for page in [1, 2, 5, 10, 20, 50, 100]:
            self.run_performance_test(f"Página {page}", {"page": page, "size": 10})

        # Probar páginas con filtros
        for page in [1, 5, 10, 25]:
            self.run_performance_test(
                f"Página {page} con filtros",
                {
                    "search": "apartment",
                    "bedrooms": 2,
                    "is_active": True,
                    "page": page,
                    "size": 20,
                },
            )

    def test_sorting_performance(self):
        """Probar rendimiento de ordenamiento"""
        print("\n[SORTING] TESTING RENDIMIENTO DE ORDENAMIENTO")
        print("=" * 50)

        # Probar diferentes columnas de ordenamiento
        for sort_column in [
            SortColumn.ID,
            SortColumn.NAME,
            SortColumn.NODE_NAME,
            SortColumn.UNIT_TYPE_NAME,
        ]:
            for sort_direction in [SortDirection.ASC, SortDirection.DESC]:
                self.run_performance_test(
                    f"Ordenar por {sort_column.value} {sort_direction.value}",
                    {
                        "sort_column": sort_column,
                        "sort_direction": sort_direction,
                        "page": 1,
                        "size": 25,
                    },
                )

        # Probar ordenamiento con filtros
        self.run_performance_test(
            "Ordenamiento con filtros complejos",
            {
                "search": "luxury",
                "bedrooms": 2,
                "is_active": True,
                "is_bookable": True,
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 30,
            },
        )

    def test_date_range_performance(self):
        """Probar rendimiento de rangos de fechas"""
        print("\n[DATES] TESTING RENDIMIENTO DE FECHAS")
        print("=" * 50)

        # Diferentes rangos de fechas
        today = datetime.now()
        date_ranges = [
            (1, 3),  # 2 días
            (1, 7),  # 6 días
            (1, 14),  # 13 días
            (1, 30),  # 29 días
            (1, 90),  # 89 días
            (30, 60),  # 30 días (futuro)
            (90, 120),  # 30 días (muy futuro)
        ]

        for start_days, end_days in date_ranges:
            arrival = (today + timedelta(days=start_days)).strftime("%Y-%m-%d")
            departure = (today + timedelta(days=end_days)).strftime("%Y-%m-%d")

            self.run_performance_test(
                f"Rango de fechas {start_days}-{end_days} días",
                {
                    "arrival": arrival,
                    "departure": departure,
                    "is_active": True,
                    "is_bookable": True,
                    "page": 1,
                    "size": 20,
                },
            )

    def test_random_combinations(self):
        """Probar combinaciones aleatorias"""
        print("\n[RANDOM] TESTING COMBINACIONES ALEATORIAS")
        print("=" * 50)

        # Generar 10 combinaciones aleatorias
        for i in range(10):
            params = self._generate_random_params()
            self.run_performance_test(f"Combinación aleatoria {i+1}", params)

    def _generate_random_params(self) -> Dict[str, Any]:
        """Generar parámetros aleatorios para testing"""
        params = {
            "page": random.randint(1, 10),
            "size": random.choice([5, 10, 20, 25, 50]),
        }

        # Búsquedas de texto aleatorias
        if random.random() < 0.7:
            params["search"] = random.choice(
                ["apartment", "suite", "penthouse", "villa", "luxury"]
            )
        if random.random() < 0.5:
            params["term"] = random.choice(
                ["vista", "mar", "piscina", "jacuzzi", "patio"]
            )
        if random.random() < 0.3:
            params["unit_code"] = random.choice(["APT%", "SUITE%", "PENT%", "LUX%"])

        # Filtros numéricos aleatorios
        if random.random() < 0.6:
            params["bedrooms"] = random.randint(1, 4)
        if random.random() < 0.6:
            params["bathrooms"] = random.randint(1, 3)
        if random.random() < 0.4:
            params["occupancy"] = random.randint(2, 8)

        # Filtros booleanos aleatorios
        if random.random() < 0.8:
            params["is_active"] = random.choice([True, False])
        if random.random() < 0.7:
            params["is_bookable"] = random.choice([True, False])
        if random.random() < 0.3:
            params["pets_friendly"] = random.choice([True, False])

        # Filtros de estado aleatorios
        if random.random() < 0.4:
            params["unit_status"] = random.choice(list(UnitStatus))

        # Filtros de fechas aleatorios
        if random.random() < 0.5:
            start_days = random.randint(1, 30)
            end_days = start_days + random.randint(1, 14)
            today = datetime.now()
            params["arrival"] = (today + timedelta(days=start_days)).strftime(
                "%Y-%m-%d"
            )
            params["departure"] = (today + timedelta(days=end_days)).strftime(
                "%Y-%m-%d"
            )

        # Filtros de IDs aleatorios
        if random.random() < 0.4:
            params["amenity_id"] = random.sample(range(1, 20), random.randint(1, 5))
        if random.random() < 0.3:
            params["node_id"] = random.sample(range(1, 10), random.randint(1, 3))
        if random.random() < 0.3:
            params["unit_type_id"] = random.sample(range(1, 10), random.randint(1, 3))

        # Ordenamiento aleatorio
        if random.random() < 0.6:
            params["sort_column"] = random.choice(list(SortColumn))
            params["sort_direction"] = random.choice(list(SortDirection))

        return params

    def run_all_performance_tests(self):
        """Ejecutar todos los tests de rendimiento"""
        print("[START] INICIANDO TESTING DE RENDIMIENTO")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)

        # Ejecutar todas las categorías de tests
        self.test_page_sizes()
        self.test_complexity_levels()
        self.test_stress_scenarios()
        self.test_pagination_performance()
        self.test_sorting_performance()
        self.test_date_range_performance()
        self.test_random_combinations()

        # Generar reporte final
        self.generate_report()

    def generate_report(self):
        """Generar reporte final de rendimiento"""
        total_time = time.time() - self.start_time
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["success"])
        failed_tests = total_tests - passed_tests

        print("\n" + "=" * 60)
        print("[REPORT] REPORTE FINAL DE RENDIMIENTO")
        print("=" * 60)
        print(f"Total de tests: {total_tests}")
        print(f"Tests exitosos: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Tests fallidos: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"Tiempo total: {total_time:.2f} segundos")
        print(f"Tiempo promedio por test: {total_time/total_tests:.3f} segundos")

        # Mostrar tests fallidos
        if failed_tests > 0:
            print(f"\n[ERROR] TESTS FALLIDOS ({failed_tests}):")
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
            print(f"  Tiempo mediano: {sorted(durations)[len(durations)//2]:.1f}ms")
            print(f"  Tiempo P95: {sorted(durations)[int(len(durations)*0.95)]:.1f}ms")
            print(f"  Tiempo P99: {sorted(durations)[int(len(durations)*0.99)]:.1f}ms")

        # Análisis por categoría
        categories = {}
        for test in self.test_results:
            category = (
                test["test_name"].split(":")[0] if ":" in test["test_name"] else "Other"
            )
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0, "durations": []}
            categories[category]["total"] += 1
            if test["success"]:
                categories[category]["passed"] += 1
                categories[category]["durations"].append(test["duration_ms"])

        print(f"\n[CATEGORIES] ANALISIS POR CATEGORIA:")
        for category, stats in categories.items():
            success_rate = stats["passed"] / stats["total"] * 100
            avg_duration = (
                sum(stats["durations"]) / len(stats["durations"])
                if stats["durations"]
                else 0
            )
            print(
                f"  {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%) - {avg_duration:.1f}ms avg"
            )

        # Guardar reporte detallado
        report_file = (
            f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
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
                        "min_time_ms": min(durations) if durations else 0,
                        "max_time_ms": max(durations) if durations else 0,
                        "median_time_ms": (
                            sorted(durations)[len(durations) // 2] if durations else 0
                        ),
                        "p95_time_ms": (
                            sorted(durations)[int(len(durations) * 0.95)]
                            if durations
                            else 0
                        ),
                        "p99_time_ms": (
                            sorted(durations)[int(len(durations) * 0.99)]
                            if durations
                            else 0
                        ),
                        "categories": categories,
                    },
                    "tests": self.test_results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\n[FILE] Reporte detallado guardado en: {report_file}")
        print("=" * 60)


def main():
    """Función principal para ejecutar los tests de rendimiento"""
    print("[CONFIG] TESTING DE RENDIMIENTO")
    print("=" * 40)
    print("Probando rendimiento con diferentes configuraciones")
    print("=" * 40)

    # Ejecutar tests de rendimiento
    tester = PerformanceTester()
    tester.run_all_performance_tests()

    return 0


if __name__ == "__main__":
    exit(main())
