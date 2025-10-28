#!/usr/bin/env python3
"""
Script de prueba directo para verificar las correcciones implementadas.
Usa las herramientas MCP directamente sin el servidor.
"""

import json
import sys
import time
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, "src")

from trackhs_mcp.repositories.unit_repository import UnitRepository
from trackhs_mcp.server import API_BASE_URL, API_PASSWORD, API_USERNAME, TrackHSClient
from trackhs_mcp.services.unit_service import UnitService


def test_search_units_direct():
    """Probar las correcciones directamente usando los servicios"""

    print("=" * 60)
    print("🧪 PRUEBA DIRECTA DE CORRECCIONES - SEARCH UNITS")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()

    # Verificar configuración
    if not API_USERNAME or not API_PASSWORD:
        print("❌ ERROR: Credenciales no configuradas")
        return False

    print(f"🔧 Configuración:")
    print(f"   - API URL: {API_BASE_URL}")
    print(f"   - Username: {'✅ Configurado' if API_USERNAME else '❌ No configurado'}")
    print(f"   - Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")
    print()

    try:
        # Inicializar cliente y servicios
        print("🔌 Inicializando cliente API...")
        api_client = TrackHSClient(API_BASE_URL, API_USERNAME, API_PASSWORD)

        print("📦 Inicializando repositorio...")
        unit_repo = UnitRepository(api_client)

        print("⚙️  Inicializando servicio...")
        unit_service = UnitService(unit_repo)

        print("✅ Servicios inicializados correctamente")
        print()

        # Casos de prueba
        test_cases = [
            {
                "name": "Búsqueda básica (5 unidades)",
                "params": {"size": 5},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con filtros numéricos",
                "params": {"bedrooms": 2, "bathrooms": 1, "size": 3},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con filtros booleanos (enteros)",
                "params": {"is_active": 1, "is_bookable": 1, "size": 3},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con filtros booleanos (strings)",
                "params": {"is_active": "1", "is_bookable": "1", "size": 3},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con filtros booleanos (booleanos)",
                "params": {"is_active": True, "is_bookable": True, "size": 3},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con texto",
                "params": {"search": "penthouse", "size": 3},
                "expected_success": True,
            },
            {
                "name": "Búsqueda con paginación",
                "params": {"page": 2, "size": 2},
                "expected_success": True,
            },
        ]

        results = []

        for i, test_case in enumerate(test_cases, 1):
            print(f"🔍 Prueba {i}: {test_case['name']}")
            print(f"   Parámetros: {test_case['params']}")

            try:
                start_time = time.time()

                # Llamar directamente al servicio
                result = unit_service.search_units(**test_case["params"])

                end_time = time.time()
                duration = round((end_time - start_time) * 1000, 2)

                # Verificar que la respuesta sea válida
                if isinstance(result, dict) and "_embedded" in result:
                    units = result.get("_embedded", {}).get("units", [])
                    total_items = result.get("total_items", 0)

                    print(
                        f"   ✅ ÉXITO - {len(units)} unidades encontradas (total: {total_items})"
                    )
                    print(f"   ⏱️  Tiempo: {duration}ms")

                    # Verificar que los datos estén limpios
                    if units:
                        first_unit = units[0]
                        print(f"   📊 Datos de la primera unidad:")
                        print(f"      - ID: {first_unit.get('id')}")
                        print(f"      - Nombre: {first_unit.get('name', 'N/A')}")
                        print(
                            f"      - Dormitorios: {first_unit.get('bedrooms', 'N/A')}"
                        )
                        print(f"      - Baños: {first_unit.get('bathrooms', 'N/A')}")
                        print(
                            f"      - Área: {first_unit.get('area', 'N/A')} (tipo: {type(first_unit.get('area')).__name__})"
                        )
                        print(
                            f"      - Activa: {first_unit.get('is_active', 'N/A')} (tipo: {type(first_unit.get('is_active')).__name__})"
                        )
                        print(
                            f"      - Reservable: {first_unit.get('is_bookable', 'N/A')} (tipo: {type(first_unit.get('is_bookable')).__name__})"
                        )

                    # Verificar tipos de datos
                    data_types_ok = True
                    if units:
                        first_unit = units[0]
                        # Verificar que area sea number o None
                        area = first_unit.get("area")
                        if area is not None and not isinstance(area, (int, float)):
                            print(
                                f"   ⚠️  ADVERTENCIA: Campo 'area' no es numérico: {type(area)}"
                            )
                            data_types_ok = False

                        # Verificar que is_active e is_bookable sean boolean o None
                        for field in ["is_active", "is_bookable"]:
                            value = first_unit.get(field)
                            if value is not None and not isinstance(value, bool):
                                print(
                                    f"   ⚠️  ADVERTENCIA: Campo '{field}' no es booleano: {type(value)}"
                                )
                                data_types_ok = False

                    results.append(
                        {
                            "test": test_case["name"],
                            "status": "SUCCESS",
                            "duration_ms": duration,
                            "units_found": len(units),
                            "total_items": total_items,
                            "data_types_ok": data_types_ok,
                        }
                    )

                else:
                    print(f"   ❌ FALLO - Respuesta inválida: {type(result)}")
                    results.append(
                        {
                            "test": test_case["name"],
                            "status": "FAILED",
                            "duration_ms": duration,
                            "error": "Respuesta inválida",
                            "data_types_ok": False,
                        }
                    )

            except Exception as e:
                end_time = time.time()
                duration = round((end_time - start_time) * 1000, 2)

                print(f"   ❌ ERROR - {str(e)}")
                print(f"   ⏱️  Tiempo: {duration}ms")

                results.append(
                    {
                        "test": test_case["name"],
                        "status": "ERROR",
                        "duration_ms": duration,
                        "error": str(e),
                        "data_types_ok": False,
                    }
                )

            print()

        # Resumen de resultados
        print("=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)

        successful_tests = [r for r in results if r["status"] == "SUCCESS"]
        failed_tests = [r for r in results if r["status"] in ["FAILED", "ERROR"]]

        print(f"✅ Pruebas exitosas: {len(successful_tests)}/{len(results)}")
        print(f"❌ Pruebas fallidas: {len(failed_tests)}/{len(results)}")
        print()

        if successful_tests:
            avg_duration = sum(r["duration_ms"] for r in successful_tests) / len(
                successful_tests
            )
            print(f"⏱️  Tiempo promedio: {avg_duration:.2f}ms")

            # Verificar tipos de datos
            data_types_ok_count = sum(
                1 for r in successful_tests if r.get("data_types_ok", False)
            )
            print(
                f"📊 Tipos de datos correctos: {data_types_ok_count}/{len(successful_tests)}"
            )
            print()

        if failed_tests:
            print("❌ Pruebas fallidas:")
            for test in failed_tests:
                print(f"   - {test['test']}: {test.get('error', 'Error desconocido')}")
            print()

        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_mcp_tools_direct_{timestamp}.json"

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "successful_tests": len(successful_tests),
            "failed_tests": len(failed_tests),
            "success_rate": len(successful_tests) / len(results) * 100,
            "data_types_correct": data_types_ok_count if successful_tests else 0,
            "results": results,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 Reporte guardado en: {filename}")

        # Determinar si las correcciones fueron exitosas
        if len(successful_tests) == len(results):
            print("🎉 ¡TODAS LAS CORRECCIONES FUNCIONAN CORRECTAMENTE!")
            return True
        else:
            print("⚠️  Algunas correcciones necesitan ajustes adicionales.")
            return False

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_search_units_direct()
    sys.exit(0 if success else 1)
