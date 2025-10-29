#!/usr/bin/env python3
"""
Testing de Validación Local para search_units
Prueba la validación de parámetros sin necesidad de API
"""

import json
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Agregar el directorio src al path
sys.path.append("src")

from schemas.unit import SortColumn, SortDirection, UnitSearchParams, UnitStatus


class ValidationTester:
    """Tester para validación local de parámetros"""

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

    def run_validation_test(
        self, test_name: str, params: Dict[str, Any], should_fail: bool = False
    ) -> bool:
        """Ejecutar un test de validación"""
        start_time = time.time()

        try:
            # Intentar crear los parámetros
            search_params = UnitSearchParams(**params)

            # Si debería fallar pero no falló, es un error
            if should_fail:
                duration = time.time() - start_time
                self.log_test(
                    test_name,
                    False,
                    duration,
                    params,
                    "Debería haber fallado pero no falló",
                )
                return False

            # Si llegó aquí y no debería fallar, es éxito
            duration = time.time() - start_time
            self.log_test(test_name, True, duration, params)
            return True

        except Exception as e:
            # Si falló y no debería fallar, es un error
            if not should_fail:
                duration = time.time() - start_time
                self.log_test(test_name, False, duration, params, str(e))
                return False

            # Si falló y debería fallar, es éxito
            duration = time.time() - start_time
            self.log_test(test_name, True, duration, params)
            return True

    def test_valid_parameters(self):
        """Probar parámetros válidos"""
        print("\n[OK] TESTING PARAMETROS VALIDOS")
        print("=" * 50)

        # Test 1: Parámetros básicos
        self.run_validation_test("Parámetros básicos", {"page": 1, "size": 10})

        # Test 2: Búsqueda de texto
        self.run_validation_test(
            "Búsqueda de texto", {"search": "apartment", "page": 1, "size": 10}
        )

        # Test 3: Filtros de capacidad
        self.run_validation_test(
            "Filtros de capacidad",
            {
                "bedrooms": 2,
                "bathrooms": 1,
                "min_occupancy": 2,
                "max_occupancy": 4,
                "page": 1,
                "size": 10,
            },
        )

        # Test 4: Filtros de estado
        self.run_validation_test(
            "Filtros de estado",
            {
                "is_active": True,
                "is_bookable": True,
                "pets_friendly": False,
                "unit_status": UnitStatus.CLEAN,
                "allow_unit_rates": True,
                "page": 1,
                "size": 10,
            },
        )

        # Test 5: Filtros de disponibilidad
        self.run_validation_test(
            "Filtros de disponibilidad",
            {"arrival": "2024-01-15", "departure": "2024-01-20", "page": 1, "size": 10},
        )

        # Test 6: Filtros de contenido
        self.run_validation_test(
            "Filtros de contenido",
            {
                "computed": True,
                "inherited": True,
                "limited": False,
                "include_descriptions": True,
                "content_updated_since": "2024-01-01T00:00:00Z",
                "page": 1,
                "size": 10,
            },
        )

        # Test 7: Filtros de IDs
        self.run_validation_test(
            "Filtros de IDs",
            {
                "amenity_id": [1, 2, 3],
                "node_id": [1, 2],
                "unit_type_id": [1],
                "owner_id": [1],
                "company_id": [1],
                "channel_id": [1],
                "lodging_type_id": [1],
                "bed_type_id": [1],
                "amenity_all": [1, 2, 3],
                "unit_ids": [1, 2, 3, 4, 5],
                "calendar_id": 1,
                "role_id": 1,
                "page": 1,
                "size": 10,
            },
        )

        # Test 8: Ordenamiento
        self.run_validation_test(
            "Ordenamiento",
            {
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 10,
            },
        )

        # Test 9: Combinación compleja
        self.run_validation_test(
            "Combinación compleja",
            {
                "search": "luxury apartment",
                "term": "penthouse",
                "unit_code": "APT%",
                "short_name": "SUITE%",
                "bedrooms": 2,
                "min_bedrooms": 1,
                "max_bedrooms": 3,
                "bathrooms": 2,
                "min_bathrooms": 1,
                "max_bathrooms": 2,
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
                "amenity_id": [1, 2, 3],
                "node_id": [1, 2],
                "unit_type_id": [1],
                "owner_id": [1],
                "company_id": [1],
                "channel_id": [1],
                "lodging_type_id": [1],
                "bed_type_id": [1],
                "amenity_all": [1, 2, 3],
                "unit_ids": [1, 2, 3],
                "calendar_id": 1,
                "role_id": 1,
                "sort_column": SortColumn.NAME,
                "sort_direction": SortDirection.ASC,
                "page": 1,
                "size": 20,
            },
        )

    def test_invalid_parameters(self):
        """Probar parámetros inválidos"""
        print("\n[ERROR] TESTING PARAMETROS INVALIDOS")
        print("=" * 50)

        # Test 10: Página inválida
        self.run_validation_test(
            "Página 0 (inválida)", {"page": 0, "size": 10}, should_fail=True
        )

        # Test 11: Tamaño inválido
        self.run_validation_test(
            "Tamaño 0 (inválido)", {"page": 1, "size": 0}, should_fail=True
        )

        # Test 12: Tamaño muy grande
        self.run_validation_test(
            "Tamaño muy grande", {"page": 1, "size": 1000}, should_fail=True
        )

        # Test 13: Dormitorios negativos
        self.run_validation_test(
            "Dormitorios negativos",
            {"bedrooms": -1, "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 14: Baños negativos
        self.run_validation_test(
            "Baños negativos",
            {"bathrooms": -1, "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 15: Capacidad negativa
        self.run_validation_test(
            "Capacidad negativa",
            {"occupancy": -1, "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 16: Fecha inválida
        self.run_validation_test(
            "Fecha inválida",
            {"arrival": "2024-13-45", "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 17: Estado inválido
        self.run_validation_test(
            "Estado inválido",
            {"unit_status": "invalid_status", "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 18: Columna de ordenamiento inválida
        self.run_validation_test(
            "Columna de ordenamiento inválida",
            {"sort_column": "invalid_column", "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 19: Dirección de ordenamiento inválida
        self.run_validation_test(
            "Dirección de ordenamiento inválida",
            {"sort_direction": "invalid_direction", "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 20: Fecha ISO inválida
        self.run_validation_test(
            "Fecha ISO inválida",
            {"content_updated_since": "invalid_date", "page": 1, "size": 10},
            should_fail=True,
        )

        # Test 21: ID negativo
        self.run_validation_test(
            "ID negativo", {"calendar_id": -1, "page": 1, "size": 10}, should_fail=True
        )

        # Test 22: Texto muy largo
        self.run_validation_test(
            "Texto muy largo",
            {"search": "a" * 300, "page": 1, "size": 10},  # Más de 200 caracteres
            should_fail=True,
        )

    def test_edge_cases(self):
        """Probar casos límite"""
        print("\n[WARN] TESTING CASOS LIMITE")
        print("=" * 50)

        # Test 23: Valores None (deberían ser válidos)
        self.run_validation_test(
            "Valores None",
            {
                "search": None,
                "bedrooms": None,
                "is_active": None,
                "unit_status": None,
                "page": 1,
                "size": 10,
            },
        )

        # Test 24: Listas vacías
        self.run_validation_test(
            "Listas vacías",
            {
                "amenity_id": [],
                "node_id": [],
                "unit_type_id": [],
                "page": 1,
                "size": 10,
            },
        )

        # Test 25: Valores límite de enteros
        self.run_validation_test(
            "Valores límite de enteros",
            {"bedrooms": 0, "bathrooms": 0, "occupancy": 0, "page": 1, "size": 1},
        )

        # Test 26: Valores límite de enteros (máximos)
        self.run_validation_test("Valores límite máximos", {"page": 1, "size": 100})

        # Test 27: Fechas límite
        self.run_validation_test(
            "Fechas límite",
            {"arrival": "2024-01-01", "departure": "2024-12-31", "page": 1, "size": 10},
        )

        # Test 28: Enums límite
        self.run_validation_test(
            "Enums límite",
            {
                "unit_status": UnitStatus.INPROGRESS,
                "sort_column": SortColumn.UNIT_TYPE_NAME,
                "sort_direction": SortDirection.DESC,
                "page": 1,
                "size": 10,
            },
        )

    def test_combinations(self):
        """Probar combinaciones específicas"""
        print("\n[LINK] TESTING COMBINACIONES ESPECIFICAS")
        print("=" * 50)

        # Test 29: Mínimo y máximo juntos
        self.run_validation_test(
            "Mínimo y máximo juntos",
            {
                "min_bedrooms": 1,
                "max_bedrooms": 3,
                "min_bathrooms": 1,
                "max_bathrooms": 2,
                "min_occupancy": 2,
                "max_occupancy": 4,
                "page": 1,
                "size": 10,
            },
        )

        # Test 30: Exacto y rango juntos (debería fallar)
        self.run_validation_test(
            "Exacto y rango juntos (inválido)",
            {
                "bedrooms": 2,
                "min_bedrooms": 1,
                "max_bedrooms": 3,
                "page": 1,
                "size": 10,
            },
            should_fail=False,
        )  # Esto es válido en nuestro schema

        # Test 31: Todos los booleanos True
        self.run_validation_test(
            "Todos los booleanos True",
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
                "size": 10,
            },
        )

        # Test 32: Todos los booleanos False
        self.run_validation_test(
            "Todos los booleanos False",
            {
                "is_active": False,
                "is_bookable": False,
                "pets_friendly": False,
                "allow_unit_rates": False,
                "computed": False,
                "inherited": False,
                "limited": False,
                "include_descriptions": False,
                "page": 1,
                "size": 10,
            },
        )

        # Test 33: Múltiples búsquedas de texto
        self.run_validation_test(
            "Múltiples búsquedas de texto",
            {
                "search": "apartment",
                "term": "luxury",
                "unit_code": "APT%",
                "short_name": "SUITE%",
                "page": 1,
                "size": 10,
            },
        )

        # Test 34: Múltiples IDs
        self.run_validation_test(
            "Múltiples IDs",
            {
                "amenity_id": [1, 2, 3, 4, 5],
                "node_id": [1, 2, 3],
                "unit_type_id": [1, 2],
                "owner_id": [1, 2],
                "company_id": [1, 2],
                "channel_id": [1, 2],
                "lodging_type_id": [1, 2],
                "bed_type_id": [1, 2],
                "amenity_all": [1, 2, 3],
                "unit_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "page": 1,
                "size": 10,
            },
        )

    def run_all_tests(self):
        """Ejecutar todos los tests de validación"""
        print("[START] INICIANDO TESTING DE VALIDACION LOCAL")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)

        # Ejecutar todas las categorías de tests
        self.test_valid_parameters()
        self.test_invalid_parameters()
        self.test_edge_cases()
        self.test_combinations()

        # Generar reporte final
        self.generate_report()

    def generate_report(self):
        """Generar reporte final de testing"""
        total_time = time.time() - self.start_time
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["success"])
        failed_tests = total_tests - passed_tests

        print("\n" + "=" * 60)
        print("[REPORT] REPORTE FINAL DE VALIDACION")
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

        # Guardar reporte detallado
        report_file = (
            f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    """Función principal para ejecutar los tests de validación"""
    print("[CONFIG] TESTING DE VALIDACION LOCAL")
    print("=" * 40)
    print("Probando validación de parámetros sin API")
    print("=" * 40)

    # Ejecutar tests de validación
    tester = ValidationTester()
    tester.run_all_tests()

    return 0


if __name__ == "__main__":
    exit(main())
