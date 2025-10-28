#!/usr/bin/env python3
"""
Test Simple de Validación MCP - TrackHS MCP Server
Verifica que las correcciones de validación funcionen correctamente
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configurar variables de entorno para testing
os.environ.setdefault("TRACKHS_USERNAME", "test_user")
os.environ.setdefault("TRACKHS_PASSWORD", "test_password")
os.environ.setdefault("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")


def test_validation_corrections():
    """Test de correcciones de validación"""
    print("🧪 TESTING CORRECCIONES DE VALIDACIÓN - TRACKHS MCP")
    print("=" * 60)

    # Importar las funciones directamente del servidor
    from trackhs_mcp.server import (
        create_housekeeping_work_order,
        create_maintenance_work_order,
        get_folio,
        search_amenities,
        search_units,
    )

    results = []

    # Test 1: Verificar que search_units maneja strings correctamente
    print("\n1. Testing search_units con parámetros string...")
    try:
        # Esto debería funcionar con la conversión de tipos implementada
        result = search_units(
            bedrooms="2",  # String que debería convertirse a int
            bathrooms="1",  # String que debería convertirse a int
            size=3,
        )

        if result and "_embedded" in result:
            print("✅ search_units con parámetros string: FUNCIONA")
            print(
                f"   - Unidades encontradas: {len(result['_embedded'].get('units', []))}"
            )
            results.append(
                {"test": "search_units_string", "status": "success", "data": result}
            )
        else:
            print("❌ search_units con parámetros string: FALLA - Sin datos")
            results.append(
                {
                    "test": "search_units_string",
                    "status": "failed",
                    "error": "Sin datos",
                }
            )
    except Exception as e:
        print(f"❌ search_units con parámetros string: ERROR - {e}")
        results.append(
            {"test": "search_units_string", "status": "error", "error": str(e)}
        )

    # Test 2: Verificar que search_units maneja integers correctamente
    print("\n2. Testing search_units con parámetros integer...")
    try:
        result = search_units(
            bedrooms=2, bathrooms=1, size=3  # Integer directo  # Integer directo
        )

        if result and "_embedded" in result:
            print("✅ search_units con parámetros integer: FUNCIONA")
            print(
                f"   - Unidades encontradas: {len(result['_embedded'].get('units', []))}"
            )
            results.append(
                {"test": "search_units_int", "status": "success", "data": result}
            )
        else:
            print("❌ search_units con parámetros integer: FALLA - Sin datos")
            results.append(
                {"test": "search_units_int", "status": "failed", "error": "Sin datos"}
            )
    except Exception as e:
        print(f"❌ search_units con parámetros integer: ERROR - {e}")
        results.append({"test": "search_units_int", "status": "error", "error": str(e)})

    # Test 3: Verificar search_amenities
    print("\n3. Testing search_amenities...")
    try:
        result = search_amenities(size=5)

        if result and "_embedded" in result:
            print("✅ search_amenities: FUNCIONA")
            amenities = result["_embedded"].get("amenities", [])
            print(f"   - Amenidades encontradas: {len(amenities)}")
            if amenities:
                amenity = amenities[0]
                print(f"   - Primera amenidad: {amenity.get('name', 'N/A')}")
            results.append(
                {"test": "search_amenities", "status": "success", "data": result}
            )
        else:
            print("❌ search_amenities: FALLA - Sin datos")
            results.append(
                {"test": "search_amenities", "status": "failed", "error": "Sin datos"}
            )
    except Exception as e:
        print(f"❌ search_amenities: ERROR - {e}")
        results.append({"test": "search_amenities", "status": "error", "error": str(e)})

    # Test 4: Verificar get_folio con manejo de errores
    print("\n4. Testing get_folio con reserva existente...")
    try:
        result = get_folio(reservation_id=27360905)

        if result and "reservation_id" in result:
            print("✅ get_folio: FUNCIONA")
            print(f"   - Reserva ID: {result.get('reservation_id')}")
            results.append({"test": "get_folio", "status": "success", "data": result})
        elif result and "error" in result:
            print("⚠️ get_folio: MANEJADO - Folio no encontrado (esperado)")
            print(f"   - Mensaje: {result.get('message', 'N/A')}")
            results.append({"test": "get_folio", "status": "handled", "data": result})
        else:
            print("❌ get_folio: FALLA - Respuesta inesperada")
            results.append(
                {
                    "test": "get_folio",
                    "status": "failed",
                    "error": "Respuesta inesperada",
                }
            )
    except Exception as e:
        print(f"❌ get_folio: ERROR - {e}")
        results.append({"test": "get_folio", "status": "error", "error": str(e)})

    # Test 5: Verificar create_maintenance_work_order
    print("\n5. Testing create_maintenance_work_order...")
    try:
        result = create_maintenance_work_order(
            unit_id=75,
            summary="Test de corrección MCP",
            description="Verificar que la creación de órdenes de mantenimiento funcione correctamente",
            priority=3,
            estimated_cost=150.0,
            estimated_time=120,
        )

        if result and "id" in result:
            print("✅ create_maintenance_work_order: FUNCIONA")
            print(f"   - ID de orden: {result.get('id')}")
            print(f"   - Estado: {result.get('status', 'N/A')}")
            results.append(
                {
                    "test": "create_maintenance_work_order",
                    "status": "success",
                    "data": result,
                }
            )
        else:
            print("❌ create_maintenance_work_order: FALLA - Sin ID")
            results.append(
                {
                    "test": "create_maintenance_work_order",
                    "status": "failed",
                    "error": "Sin ID",
                }
            )
    except Exception as e:
        print(f"❌ create_maintenance_work_order: ERROR - {e}")
        results.append(
            {
                "test": "create_maintenance_work_order",
                "status": "error",
                "error": str(e),
            }
        )

    # Test 6: Verificar create_housekeeping_work_order
    print("\n6. Testing create_housekeeping_work_order...")
    try:
        result = create_housekeeping_work_order(
            unit_id=75,
            scheduled_at="2024-01-15",
            is_inspection=False,
            clean_type_id=1,
            cost=80.0,
        )

        if result and "id" in result:
            print("✅ create_housekeeping_work_order: FUNCIONA")
            print(f"   - ID de orden: {result.get('id')}")
            print(f"   - Estado: {result.get('status', 'N/A')}")
            results.append(
                {
                    "test": "create_housekeeping_work_order",
                    "status": "success",
                    "data": result,
                }
            )
        else:
            print("❌ create_housekeeping_work_order: FALLA - Sin ID")
            results.append(
                {
                    "test": "create_housekeeping_work_order",
                    "status": "failed",
                    "error": "Sin ID",
                }
            )
    except Exception as e:
        print(f"❌ create_housekeeping_work_order: ERROR - {e}")
        results.append(
            {
                "test": "create_housekeeping_work_order",
                "status": "error",
                "error": str(e),
            }
        )

    return results


def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TEST SIMPLE DE VALIDACIÓN MCP")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    # Ejecutar tests
    results = test_validation_corrections()

    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)

    success_count = sum(1 for r in results if r["status"] == "success")
    handled_count = sum(1 for r in results if r["status"] == "handled")
    failed_count = sum(1 for r in results if r["status"] == "failed")
    error_count = sum(1 for r in results if r["status"] == "error")

    print(f"✅ Exitosos: {success_count}")
    print(f"⚠️ Manejados: {handled_count}")
    print(f"❌ Fallidos: {failed_count}")
    print(f"🔥 Errores: {error_count}")
    print(f"📊 Total: {len(results)}")

    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": len(results),
            "successful": success_count,
            "handled": handled_count,
            "failed": failed_count,
            "errors": error_count,
            "success_rate": (
                (success_count + handled_count) / len(results) * 100 if results else 0
            ),
        },
        "results": results,
    }

    filename = f"test_simple_mcp_validation_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Reporte guardado en: {filename}")
    print("=" * 70)
    print("✅ TESTING COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
