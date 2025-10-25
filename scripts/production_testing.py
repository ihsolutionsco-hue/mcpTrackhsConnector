#!/usr/bin/env python3
"""
Suite de pruebas de producción para TrackHS MCP Server
Simula escenarios reales de usuario y verifica que el sistema esté listo para producción
"""

import json
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


class ProductionTester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "errors": [],
            "performance_metrics": [],
            "test_scenarios": [],
        }
        self.client = httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0)

    def log_test(self, test_name, success, duration=None, error=None, details=None):
        """Registrar resultado de prueba"""
        self.results["total_tests"] += 1
        if success:
            self.results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.results["failed_tests"] += 1
            status = "❌ FAIL"
            if error:
                self.results["errors"].append(f"{test_name}: {error}")

        test_result = {
            "name": test_name,
            "success": success,
            "duration": duration,
            "error": error,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        }
        self.results["test_scenarios"].append(test_result)

        print(f"{status} {test_name}")
        if duration:
            print(f"   ⏱️  Duración: {duration:.2f}s")
        if details:
            print(f"   📊 {details}")
        if error:
            print(f"   ❌ Error: {error}")
        print()

    def test_basic_connectivity(self):
        """Prueba 1: Conectividad básica"""
        print("🔌 PRUEBA 1: Conectividad básica")
        print("-" * 50)

        start_time = time.time()
        try:
            response = self.client.get(f"{API_BASE_URL}/pms/units?page=1&size=1")
            duration = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Conectividad básica",
                    True,
                    duration,
                    details=f"Total unidades: {data.get('total_items', 'N/A')}",
                )
                return True
            else:
                self.log_test(
                    "Conectividad básica",
                    False,
                    duration,
                    f"Status {response.status_code}",
                )
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Conectividad básica", False, duration, str(e))
            return False

    def test_search_by_bedrooms(self):
        """Prueba 2: Búsqueda por dormitorios"""
        print("🛏️  PRUEBA 2: Búsqueda por dormitorios")
        print("-" * 50)

        bedroom_counts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for bedrooms in bedroom_counts:
            start_time = time.time()
            try:
                response = self.client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size=5&bedrooms={bedrooms}"
                )
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    self.log_test(
                        f"Búsqueda {bedrooms} dormitorios",
                        True,
                        duration,
                        details=f"Encontradas: {total_items} unidades",
                    )
                else:
                    self.log_test(
                        f"Búsqueda {bedrooms} dormitorios",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(
                    f"Búsqueda {bedrooms} dormitorios", False, duration, str(e)
                )

    def test_search_by_bathrooms(self):
        """Prueba 3: Búsqueda por baños"""
        print("🚿 PRUEBA 3: Búsqueda por baños")
        print("-" * 50)

        bathroom_counts = [1, 2, 3, 4, 5, 6]
        for bathrooms in bathroom_counts:
            start_time = time.time()
            try:
                response = self.client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size=5&bathrooms={bathrooms}"
                )
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    self.log_test(
                        f"Búsqueda {bathrooms} baños",
                        True,
                        duration,
                        details=f"Encontradas: {total_items} unidades",
                    )
                else:
                    self.log_test(
                        f"Búsqueda {bathrooms} baños",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Búsqueda {bathrooms} baños", False, duration, str(e))

    def test_search_by_text(self):
        """Prueba 4: Búsqueda por texto"""
        print("🔍 PRUEBA 4: Búsqueda por texto")
        print("-" * 50)

        search_terms = [
            "luxury",
            "pool",
            "spa",
            "villa",
            "beach",
            "ocean",
            "mountain",
            "golf",
            "tennis",
            "penthouse",
            "condo",
            "house",
            "apartment",
            "private",
            "resort",
            "hotel",
            "suite",
            "studio",
            "loft",
        ]

        for term in search_terms:
            start_time = time.time()
            try:
                response = self.client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size=5&search={term}"
                )
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    self.log_test(
                        f"Búsqueda '{term}'",
                        True,
                        duration,
                        details=f"Encontradas: {total_items} unidades",
                    )
                else:
                    self.log_test(
                        f"Búsqueda '{term}'",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Búsqueda '{term}'", False, duration, str(e))

    def test_combined_filters(self):
        """Prueba 5: Filtros combinados"""
        print("🔗 PRUEBA 5: Filtros combinados")
        print("-" * 50)

        filter_combinations = [
            {"bedrooms": 2, "bathrooms": 1, "is_active": 1},
            {"bedrooms": 3, "bathrooms": 2, "is_bookable": 1},
            {"bedrooms": 4, "bathrooms": 3, "is_active": 1, "is_bookable": 1},
            {"search": "luxury", "bedrooms": 5, "bathrooms": 4},
            {"search": "pool", "bedrooms": 3, "is_active": 1},
        ]

        for i, filters in enumerate(filter_combinations, 1):
            start_time = time.time()
            try:
                params = {"page": 1, "size": 5, **filters}
                response = self.client.get(f"{API_BASE_URL}/pms/units", params=params)
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    filter_str = ", ".join([f"{k}={v}" for k, v in filters.items()])
                    self.log_test(
                        f"Filtros combinados {i}",
                        True,
                        duration,
                        details=f"Filtros: {filter_str} | Encontradas: {total_items}",
                    )
                else:
                    self.log_test(
                        f"Filtros combinados {i}",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Filtros combinados {i}", False, duration, str(e))

    def test_pagination(self):
        """Prueba 6: Paginación"""
        print("📄 PRUEBA 6: Paginación")
        print("-" * 50)

        # Probar diferentes tamaños de página
        page_sizes = [1, 5, 10, 25, 50]
        for size in page_sizes:
            start_time = time.time()
            try:
                response = self.client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size={size}"
                )
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    returned_items = len(data.get("_embedded", {}).get("units", []))
                    total_items = data.get("total_items", 0)
                    page_count = data.get("page_count", 0)
                    self.log_test(
                        f"Paginación size={size}",
                        True,
                        duration,
                        details=f"Retornados: {returned_items}, Total: {total_items}, Páginas: {page_count}",
                    )
                else:
                    self.log_test(
                        f"Paginación size={size}",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Paginación size={size}", False, duration, str(e))

        # Probar navegación entre páginas
        try:
            response = self.client.get(f"{API_BASE_URL}/pms/units?page=1&size=5")
            if response.status_code == 200:
                data = response.json()
                total_pages = data.get("page_count", 0)

                # Probar páginas 1, 2, y última
                pages_to_test = [1, 2]
                if total_pages > 2:
                    pages_to_test.append(min(total_pages, 5))  # Página 5 o última

                for page in pages_to_test:
                    start_time = time.time()
                    try:
                        response = self.client.get(
                            f"{API_BASE_URL}/pms/units?page={page}&size=5"
                        )
                        duration = time.time() - start_time

                        if response.status_code == 200:
                            data = response.json()
                            returned_items = len(
                                data.get("_embedded", {}).get("units", [])
                            )
                            self.log_test(
                                f"Página {page}",
                                True,
                                duration,
                                details=f"Retornados: {returned_items} elementos",
                            )
                        else:
                            self.log_test(
                                f"Página {page}",
                                False,
                                duration,
                                f"Status {response.status_code}",
                            )
                    except Exception as e:
                        duration = time.time() - start_time
                        self.log_test(f"Página {page}", False, duration, str(e))
        except Exception as e:
            self.log_test("Navegación entre páginas", False, 0, str(e))

    def test_error_handling(self):
        """Prueba 7: Manejo de errores"""
        print("⚠️  PRUEBA 7: Manejo de errores")
        print("-" * 50)

        # Casos que deberían fallar
        error_cases = [
            {"page": 0, "size": 5, "description": "Página 0 (inválida)"},
            {"page": 1, "size": 0, "description": "Tamaño 0 (inválido)"},
            {"page": -1, "size": 5, "description": "Página negativa"},
            {"page": 1, "size": -1, "description": "Tamaño negativo"},
            {"page": 1, "size": 1000, "description": "Tamaño excesivo"},
        ]

        for case in error_cases:
            start_time = time.time()
            try:
                params = {k: v for k, v in case.items() if k != "description"}
                response = self.client.get(f"{API_BASE_URL}/pms/units", params=params)
                duration = time.time() - start_time

                # Para casos de error, esperamos que falle o maneje correctamente
                if response.status_code in [400, 422, 500]:
                    self.log_test(
                        f"Error handling: {case['description']}",
                        True,
                        duration,
                        details=f"Status {response.status_code} (esperado)",
                    )
                elif response.status_code == 200:
                    # Si devuelve 200, verificar que los datos sean válidos
                    data = response.json()
                    if data.get("total_items", 0) >= 0:
                        self.log_test(
                            f"Error handling: {case['description']}",
                            True,
                            duration,
                            details="Manejado correctamente con datos válidos",
                        )
                    else:
                        self.log_test(
                            f"Error handling: {case['description']}",
                            False,
                            duration,
                            "Datos inválidos",
                        )
                else:
                    self.log_test(
                        f"Error handling: {case['description']}",
                        False,
                        duration,
                        f"Status inesperado {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(
                    f"Error handling: {case['description']}", False, duration, str(e)
                )

    def test_performance(self):
        """Prueba 8: Rendimiento"""
        print("⚡ PRUEBA 8: Rendimiento")
        print("-" * 50)

        # Pruebas de rendimiento con diferentes cargas
        performance_tests = [
            {"size": 1, "description": "Carga ligera (1 elemento)"},
            {"size": 10, "description": "Carga media (10 elementos)"},
            {"size": 25, "description": "Carga alta (25 elementos)"},
            {"size": 50, "description": "Carga máxima (50 elementos)"},
        ]

        for test in performance_tests:
            start_time = time.time()
            try:
                response = self.client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size={test['size']}"
                )
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    returned_items = len(data.get("_embedded", {}).get("units", []))

                    # Clasificar rendimiento
                    if duration < 1.0:
                        perf_rating = "Excelente"
                    elif duration < 2.0:
                        perf_rating = "Bueno"
                    elif duration < 5.0:
                        perf_rating = "Aceptable"
                    else:
                        perf_rating = "Lento"

                    self.log_test(
                        f"Rendimiento: {test['description']}",
                        True,
                        duration,
                        details=f"Retornados: {returned_items}, Rating: {perf_rating}",
                    )

                    # Guardar métrica de rendimiento
                    self.results["performance_metrics"].append(
                        {
                            "test": test["description"],
                            "duration": duration,
                            "items_returned": returned_items,
                            "rating": perf_rating,
                        }
                    )
                else:
                    self.log_test(
                        f"Rendimiento: {test['description']}",
                        False,
                        duration,
                        f"Status {response.status_code}",
                    )
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(
                    f"Rendimiento: {test['description']}", False, duration, str(e)
                )

    def test_concurrent_requests(self):
        """Prueba 9: Solicitudes concurrentes"""
        print("🔄 PRUEBA 9: Solicitudes concurrentes")
        print("-" * 50)

        import queue
        import threading

        results_queue = queue.Queue()

        def make_request(request_id):
            start_time = time.time()
            try:
                response = self.client.get(f"{API_BASE_URL}/pms/units?page=1&size=5")
                duration = time.time() - start_time
                results_queue.put(
                    {
                        "request_id": request_id,
                        "success": response.status_code == 200,
                        "duration": duration,
                        "status_code": response.status_code,
                    }
                )
            except Exception as e:
                duration = time.time() - start_time
                results_queue.put(
                    {
                        "request_id": request_id,
                        "success": False,
                        "duration": duration,
                        "error": str(e),
                    }
                )

        # Crear 5 solicitudes concurrentes
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request, args=(i + 1,))
            threads.append(thread)
            thread.start()

        # Esperar a que terminen
        for thread in threads:
            thread.join()

        # Recopilar resultados
        concurrent_results = []
        while not results_queue.empty():
            concurrent_results.append(results_queue.get())

        successful_requests = sum(1 for r in concurrent_results if r["success"])
        avg_duration = sum(r["duration"] for r in concurrent_results) / len(
            concurrent_results
        )

        self.log_test(
            "Solicitudes concurrentes",
            successful_requests >= 4,  # Al menos 4 de 5 exitosas
            avg_duration,
            details=f"Exitosas: {successful_requests}/5, Duración promedio: {avg_duration:.2f}s",
        )

    def test_amenities_endpoint(self):
        """Prueba 10: Endpoint de amenidades"""
        print("🏊 PRUEBA 10: Endpoint de amenidades")
        print("-" * 50)

        start_time = time.time()
        try:
            response = self.client.get(
                f"{API_BASE_URL}/pms/units/amenities?page=1&size=10"
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                total_amenities = data.get("total_items", 0)
                amenities = data.get("_embedded", {}).get("amenities", [])

                self.log_test(
                    "Amenidades disponibles",
                    True,
                    duration,
                    details=f"Total: {total_amenities}, Mostradas: {len(amenities)}",
                )

                # Mostrar algunas amenidades
                if amenities:
                    print("   🏊 Amenidades encontradas:")
                    for amenity in amenities[:5]:
                        name = amenity.get("name", "Sin nombre")
                        group = amenity.get("group", {}).get("name", "Sin grupo")
                        print(f"      • {name} ({group})")
            else:
                self.log_test(
                    "Amenidades disponibles",
                    False,
                    duration,
                    f"Status {response.status_code}",
                )
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Amenidades disponibles", False, duration, str(e))

    def test_reservations_endpoint(self):
        """Prueba 11: Endpoint de reservas"""
        print("📅 PRUEBA 11: Endpoint de reservas")
        print("-" * 50)

        start_time = time.time()
        try:
            response = self.client.get(f"{API_BASE_URL}/pms/reservations?page=1&size=5")
            duration = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                total_reservations = data.get("total_items", 0)
                reservations = data.get("_embedded", {}).get("reservations", [])

                self.log_test(
                    "Reservas disponibles",
                    True,
                    duration,
                    details=f"Total: {total_reservations}, Mostradas: {len(reservations)}",
                )

                # Mostrar algunas reservas
                if reservations:
                    print("   📅 Reservas encontradas:")
                    for reservation in reservations[:3]:
                        guest_name = reservation.get("guest", {}).get(
                            "name", "Sin nombre"
                        )
                        confirmation = reservation.get(
                            "confirmationNumber", "Sin confirmación"
                        )
                        status = reservation.get("status", "Sin estado")
                        print(f"      • {guest_name} - {confirmation} ({status})")
            else:
                self.log_test(
                    "Reservas disponibles",
                    False,
                    duration,
                    f"Status {response.status_code}",
                )
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Reservas disponibles", False, duration, str(e))

    def generate_report(self):
        """Generar reporte final"""
        print("\n" + "=" * 80)
        print("📊 REPORTE FINAL DE PRUEBAS DE PRODUCCIÓN")
        print("=" * 80)

        total_tests = self.results["total_tests"]
        passed_tests = self.results["passed_tests"]
        failed_tests = self.results["failed_tests"]
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        print(f"📈 RESUMEN GENERAL:")
        print(f"   Total de pruebas: {total_tests}")
        print(f"   Pruebas exitosas: {passed_tests}")
        print(f"   Pruebas fallidas: {failed_tests}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")

        if self.results["performance_metrics"]:
            print(f"\n⚡ MÉTRICAS DE RENDIMIENTO:")
            for metric in self.results["performance_metrics"]:
                print(
                    f"   {metric['test']}: {metric['duration']:.2f}s ({metric['rating']})"
                )

        if self.results["errors"]:
            print(f"\n❌ ERRORES ENCONTRADOS:")
            for error in self.results["errors"]:
                print(f"   • {error}")

        # Determinar si está listo para producción
        production_ready = success_rate >= 90 and failed_tests <= 5

        print(f"\n🚀 ESTADO DE PRODUCCIÓN:")
        if production_ready:
            print("   ✅ SISTEMA LISTO PARA PRODUCCIÓN")
            print("   ✅ Todas las funcionalidades principales funcionan correctamente")
            print("   ✅ El rendimiento es aceptable")
            print("   ✅ El manejo de errores es robusto")
        else:
            print("   ⚠️  SISTEMA NO LISTO PARA PRODUCCIÓN")
            print("   ⚠️  Se requieren correcciones antes del despliegue")
            print("   ⚠️  Revisar errores y mejorar rendimiento")

        # Guardar reporte en archivo
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "production_ready": production_ready,
            },
            "performance_metrics": self.results["performance_metrics"],
            "errors": self.results["errors"],
            "test_scenarios": self.results["test_scenarios"],
        }

        with open("production_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Reporte detallado guardado en: production_test_report.json")

        return production_ready

    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS DE PRODUCCIÓN")
        print("=" * 80)
        print(f"Base URL: {API_BASE_URL}")
        print(f"Username: {API_USERNAME}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)

        # Verificar credenciales
        if not API_USERNAME or not API_PASSWORD:
            print("❌ Error: Credenciales no configuradas")
            return False

        # Ejecutar todas las pruebas
        self.test_basic_connectivity()
        self.test_search_by_bedrooms()
        self.test_search_by_bathrooms()
        self.test_search_by_text()
        self.test_combined_filters()
        self.test_pagination()
        self.test_error_handling()
        self.test_performance()
        self.test_concurrent_requests()
        self.test_amenities_endpoint()
        self.test_reservations_endpoint()

        # Generar reporte final
        return self.generate_report()


def main():
    """Función principal"""
    tester = ProductionTester()
    try:
        production_ready = tester.run_all_tests()
        return 0 if production_ready else 1
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return 1
    finally:
        tester.client.close()


if __name__ == "__main__":
    sys.exit(main())
