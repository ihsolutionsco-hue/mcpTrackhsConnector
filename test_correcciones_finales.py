#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones implementadas
"""

import sys

sys.path.append("src")

from trackhs_mcp.server import (
    create_maintenance_work_order,
    get_folio,
    search_amenities,
    search_units,
)


def test_correcciones():
    print("=== PROBANDO CORRECCIONES IMPLEMENTADAS ===")
    print()

    # Test 1: search_units con parámetros correctos
    print("1. Probando search_units con parámetros correctos...")
    try:
        result = search_units(page=1, size=2, is_active=1, is_bookable=1)
        print("✅ search_units: FUNCIONA")
        print(f'   - Total items: {result.get("total_items", "N/A")}')
        print(f'   - Page: {result.get("page", "N/A")}')
        if "_embedded" in result and "units" in result["_embedded"]:
            units = result["_embedded"]["units"]
            print(f"   - Unidades encontradas: {len(units)}")
            if units:
                unit = units[0]
                print(
                    f'   - Primera unidad: {unit.get("name", "N/A")} (ID: {unit.get("id", "N/A")})'
                )
    except Exception as e:
        print(f"❌ search_units: ERROR - {e}")

    print()

    # Test 2: search_amenities
    print("2. Probando search_amenities...")
    try:
        result = search_amenities(page=1, size=3)
        print("✅ search_amenities: FUNCIONA")
        print(f'   - Total items: {result.get("total_items", "N/A")}')
        if "_embedded" in result and "amenities" in result["_embedded"]:
            amenities = result["_embedded"]["amenities"]
            print(f"   - Amenidades encontradas: {len(amenities)}")
            if amenities:
                amenity = amenities[0]
                print(
                    f'   - Primera amenidad: {amenity.get("name", "N/A")} (ID: {amenity.get("id", "N/A")})'
                )
                if "group" in amenity:
                    print(f'   - Grupo: {amenity["group"]}')
    except Exception as e:
        print(f"❌ search_amenities: ERROR - {e}")

    print()

    # Test 3: create_maintenance_work_order
    print("3. Probando create_maintenance_work_order...")
    try:
        result = create_maintenance_work_order(
            unit_id=75,
            summary="Prueba de corrección",
            description="Prueba de la corrección de tipos de datos",
            priority=3,
            estimated_cost=100.0,
            estimated_time=60,
        )
        print("✅ create_maintenance_work_order: FUNCIONA")
        print(f'   - ID: {result.get("id", "N/A")}')
        print(f'   - Status: {result.get("status", "N/A")}')
    except Exception as e:
        print(f"❌ create_maintenance_work_order: ERROR - {e}")

    print()

    # Test 4: get_folio (reserva cancelada)
    print("4. Probando get_folio con reserva cancelada...")
    try:
        result = get_folio(reservation_id=1)
        print("✅ get_folio: FUNCIONA")
        if "error" in result:
            print(f'   - Error manejado: {result.get("message", "N/A")}')
        else:
            print(f'   - Folio encontrado: {result.get("reservation_id", "N/A")}')
    except Exception as e:
        print(f"❌ get_folio: ERROR - {e}")

    print()
    print("=== RESUMEN DE PRUEBAS COMPLETADO ===")


if __name__ == "__main__":
    test_correcciones()
