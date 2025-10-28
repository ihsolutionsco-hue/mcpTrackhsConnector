#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones implementadas en search_units.
Prueba los casos problemáticos identificados en el user testing.
"""

import json
import sys
import time
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, "src")

from trackhs_mcp.config import get_settings
from trackhs_mcp.server import mcp


def test_search_units_corrections():
    """Probar las correcciones implementadas en search_units"""

    print("=" * 60)
    print("🧪 PRUEBA DE CORRECCIONES - SEARCH UNITS")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()

    # Configurar logging
    import logging

    logging.basicConfig(level=logging.INFO)

    # Obtener configuración
    settings = get_settings()
    print(f"🔧 Configuración:")
    print(f"   - API URL: {settings.trackhs_api_url}")
    print(
        f"   - Username: {'✅ Configurado' if settings.trackhs_username else '❌ No configurado'}"
    )
    print(
        f"   - Password: {'✅ Configurado' if settings.trackhs_password else '❌ No configurado'}"
    )
    print(f"   - Strict Validation: {settings.strict_validation}")
    print()

    # Casos de prueba que fallaban anteriormente
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

            # Llamar a la herramienta search_units
            result = mcp.call_tool("search_units", test_case["params"])

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
                    print(f"      - Dormitorios: {first_unit.get('bedrooms', 'N/A')}")
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

                results.append(
                    {
                        "test": test_case["name"],
                        "status": "SUCCESS",
                        "duration_ms": duration,
                        "units_found": len(units),
                        "total_items": total_items,
                        "data_types_ok": True,
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
        print()

    if failed_tests:
        print("❌ Pruebas fallidas:")
        for test in failed_tests:
            print(f"   - {test['test']}: {test.get('error', 'Error desconocido')}")
        print()

    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_correcciones_results_{timestamp}.json"

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(results),
        "successful_tests": len(successful_tests),
        "failed_tests": len(failed_tests),
        "success_rate": len(successful_tests) / len(results) * 100,
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


if __name__ == "__main__":
    success = test_search_units_corrections()
    sys.exit(0 if success else 1)
