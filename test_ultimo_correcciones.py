#!/usr/bin/env python3
"""
Script de prueba final usando el método correcto de FastMCP
"""

import asyncio
import json
import sys

sys.path.append("src")

from trackhs_mcp.server import mcp


async def test_correcciones_ultimo():
    print("=== PROBANDO CORRECCIONES IMPLEMENTADAS (ÚLTIMO) ===")
    print()

    # Test 1: search_units con parámetros correctos
    print("1. Probando search_units con parámetros correctos...")
    try:
        # Usar el método correcto de FastMCP
        result = await mcp.run_stdio_async(
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "search_units",
                        "arguments": {
                            "page": 1,
                            "size": 2,
                            "is_active": 1,
                            "is_bookable": 1,
                        },
                    },
                }
            ]
        )

        if result and len(result) > 0:
            response = result[0]
            if "result" in response:
                data = response["result"]
                print("✅ search_units: FUNCIONA")
                print(f'   - Total items: {data.get("total_items", "N/A")}')
                print(f'   - Page: {data.get("page", "N/A")}')
                if "_embedded" in data and "units" in data["_embedded"]:
                    units = data["_embedded"]["units"]
                    print(f"   - Unidades encontradas: {len(units)}")
                    if units:
                        unit = units[0]
                        print(
                            f'   - Primera unidad: {unit.get("name", "N/A")} (ID: {unit.get("id", "N/A")})'
                        )
            else:
                print(
                    f'❌ search_units: ERROR - {response.get("error", "Unknown error")}'
                )
        else:
            print("❌ search_units: Sin respuesta")
    except Exception as e:
        print(f"❌ search_units: ERROR - {e}")

    print()

    # Test 2: search_amenities
    print("2. Probando search_amenities...")
    try:
        result = await mcp.run_stdio_async(
            [
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "search_amenities",
                        "arguments": {"page": 1, "size": 3},
                    },
                }
            ]
        )

        if result and len(result) > 0:
            response = result[0]
            if "result" in response:
                data = response["result"]
                print("✅ search_amenities: FUNCIONA")
                print(f'   - Total items: {data.get("total_items", "N/A")}')
                if "_embedded" in data and "amenities" in data["_embedded"]:
                    amenities = data["_embedded"]["amenities"]
                    print(f"   - Amenidades encontradas: {len(amenities)}")
                    if amenities:
                        amenity = amenities[0]
                        print(
                            f'   - Primera amenidad: {amenity.get("name", "N/A")} (ID: {amenity.get("id", "N/A")})'
                        )
                        if "group" in amenity:
                            print(f'   - Grupo: {amenity["group"]}')
            else:
                print(
                    f'❌ search_amenities: ERROR - {response.get("error", "Unknown error")}'
                )
        else:
            print("❌ search_amenities: Sin respuesta")
    except Exception as e:
        print(f"❌ search_amenities: ERROR - {e}")

    print()

    # Test 3: create_maintenance_work_order
    print("3. Probando create_maintenance_work_order...")
    try:
        result = await mcp.run_stdio_async(
            [
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "create_maintenance_work_order",
                        "arguments": {
                            "unit_id": 75,
                            "summary": "Prueba de corrección",
                            "description": "Prueba de la corrección de tipos de datos",
                            "priority": 3,
                            "estimated_cost": 100.0,
                            "estimated_time": 60,
                        },
                    },
                }
            ]
        )

        if result and len(result) > 0:
            response = result[0]
            if "result" in response:
                data = response["result"]
                print("✅ create_maintenance_work_order: FUNCIONA")
                print(f'   - ID: {data.get("id", "N/A")}')
                print(f'   - Status: {data.get("status", "N/A")}')
            else:
                print(
                    f'❌ create_maintenance_work_order: ERROR - {response.get("error", "Unknown error")}'
                )
        else:
            print("❌ create_maintenance_work_order: Sin respuesta")
    except Exception as e:
        print(f"❌ create_maintenance_work_order: ERROR - {e}")

    print()

    # Test 4: get_folio (reserva cancelada)
    print("4. Probando get_folio con reserva cancelada...")
    try:
        result = await mcp.run_stdio_async(
            [
                {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {"name": "get_folio", "arguments": {"reservation_id": 1}},
                }
            ]
        )

        if result and len(result) > 0:
            response = result[0]
            if "result" in response:
                data = response["result"]
                print("✅ get_folio: FUNCIONA")
                if "error" in data:
                    print(f'   - Error manejado: {data.get("message", "N/A")}')
                else:
                    print(f'   - Folio encontrado: {data.get("reservation_id", "N/A")}')
            else:
                print(f'❌ get_folio: ERROR - {response.get("error", "Unknown error")}')
        else:
            print("❌ get_folio: Sin respuesta")
    except Exception as e:
        print(f"❌ get_folio: ERROR - {e}")

    print()
    print("=== RESUMEN DE PRUEBAS COMPLETADO ===")


if __name__ == "__main__":
    asyncio.run(test_correcciones_ultimo())
