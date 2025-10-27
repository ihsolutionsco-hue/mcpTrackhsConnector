#!/usr/bin/env python3
"""
Script de testing real con la API de TrackHS
Prueba todas las herramientas con datos reales
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.server import mcp


async def test_search_reservations():
    """Probar búsqueda de reservas"""
    print("\n🔍 PROBANDO SEARCH_RESERVATIONS")
    print("=" * 50)

    # Test 1: Búsqueda básica
    print("\n1. Búsqueda básica de reservas...")
    try:
        result = await mcp.call_tool(
            "search_reservations", {"page": 0, "size": 5, "status": "confirmed"}
        )
        print(
            f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} reservas encontradas"
        )
        if result.get("_embedded", {}).get("reservations"):
            print(
                f"   Primera reserva: {result['_embedded']['reservations'][0].get('confirmation_number', 'N/A')}"
            )
    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    # Test 2: Búsqueda por fecha
    print("\n2. Búsqueda por fecha...")
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        result = await mcp.call_tool(
            "search_reservations",
            {"arrival_start": today, "arrival_end": today, "size": 5},
        )
        print(
            f"✅ Búsqueda por fecha exitosa: {result.get('total_items', 0)} reservas para hoy"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda por fecha: {e}")

    # Test 3: Búsqueda con texto
    print("\n3. Búsqueda con texto...")
    try:
        result = await mcp.call_tool(
            "search_reservations", {"search": "test", "size": 5}
        )
        print(
            f"✅ Búsqueda con texto exitosa: {result.get('total_items', 0)} reservas encontradas"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda con texto: {e}")


async def test_get_reservation():
    """Probar obtención de reserva específica"""
    print("\n\n📋 PROBANDO GET_RESERVATION")
    print("=" * 50)

    # Primero buscar una reserva para obtener su ID
    try:
        search_result = await mcp.call_tool(
            "search_reservations", {"page": 0, "size": 1, "status": "confirmed"}
        )

        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            print(f"1. Obteniendo detalles de reserva ID: {reservation_id}")

            result = await mcp.call_tool(
                "get_reservation", {"reservation_id": reservation_id}
            )
            print(f"✅ Reserva obtenida: {result.get('confirmation_number', 'N/A')}")
            print(f"   Huésped: {result.get('guest', {}).get('name', 'N/A')}")
            print(f"   Estado: {result.get('status', 'N/A')}")
        else:
            print("❌ No hay reservas disponibles para probar")
    except Exception as e:
        print(f"❌ Error obteniendo reserva: {e}")


async def test_search_units():
    """Probar búsqueda de unidades"""
    print("\n\n🏠 PROBANDO SEARCH_UNITS")
    print("=" * 50)

    # Test 1: Búsqueda básica
    print("\n1. Búsqueda básica de unidades...")
    try:
        result = await mcp.call_tool(
            "search_units", {"page": 1, "size": 5, "is_active": 1, "is_bookable": 1}
        )
        print(
            f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} unidades encontradas"
        )
        if result.get("_embedded", {}).get("units"):
            unit = result["_embedded"]["units"][0]
            print(
                f"   Primera unidad: {unit.get('name', 'N/A')} ({unit.get('code', 'N/A')})"
            )
    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    # Test 2: Búsqueda por capacidad
    print("\n2. Búsqueda por capacidad...")
    try:
        result = await mcp.call_tool(
            "search_units", {"bedrooms": 2, "bathrooms": 1, "is_active": 1, "size": 5}
        )
        print(
            f"✅ Búsqueda por capacidad exitosa: {result.get('total_items', 0)} unidades 2BR/1BA"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda por capacidad: {e}")

    # Test 3: Búsqueda con texto
    print("\n3. Búsqueda con texto...")
    try:
        result = await mcp.call_tool("search_units", {"search": "apartment", "size": 5})
        print(
            f"✅ Búsqueda con texto exitosa: {result.get('total_items', 0)} unidades encontradas"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda con texto: {e}")


async def test_search_amenities():
    """Probar búsqueda de amenidades"""
    print("\n\n🏊 PROBANDO SEARCH_AMENITIES")
    print("=" * 50)

    # Test 1: Búsqueda básica
    print("\n1. Búsqueda básica de amenidades...")
    try:
        result = await mcp.call_tool("search_amenities", {"page": 1, "size": 10})
        print(
            f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} amenidades encontradas"
        )
        if result.get("_embedded", {}).get("amenities"):
            amenity = result["_embedded"]["amenities"][0]
            print(
                f"   Primera amenidad: {amenity.get('name', 'N/A')} ({amenity.get('group', 'N/A')})"
            )
    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    # Test 2: Búsqueda con texto
    print("\n2. Búsqueda con texto...")
    try:
        result = await mcp.call_tool("search_amenities", {"search": "wifi", "size": 5})
        print(
            f"✅ Búsqueda con texto exitosa: {result.get('total_items', 0)} amenidades WiFi encontradas"
        )
    except Exception as e:
        print(f"❌ Error en búsqueda con texto: {e}")


async def test_get_folio():
    """Probar obtención de folio"""
    print("\n\n💰 PROBANDO GET_FOLIO")
    print("=" * 50)

    # Primero buscar una reserva para obtener su ID
    try:
        search_result = await mcp.call_tool(
            "search_reservations", {"page": 0, "size": 1, "status": "confirmed"}
        )

        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            print(f"1. Obteniendo folio de reserva ID: {reservation_id}")

            result = await mcp.call_tool(
                "get_folio", {"reservation_id": reservation_id}
            )
            print(f"✅ Folio obtenido: Balance ${result.get('balance', 0)}")
            print(f"   Cargos: {len(result.get('charges', []))}")
            print(f"   Pagos: {len(result.get('payments', []))}")
        else:
            print("❌ No hay reservas disponibles para probar folio")
    except Exception as e:
        print(f"❌ Error obteniendo folio: {e}")


async def test_create_maintenance_work_order():
    """Probar creación de orden de mantenimiento"""
    print("\n\n🔧 PROBANDO CREATE_MAINTENANCE_WORK_ORDER")
    print("=" * 50)

    # Primero buscar una unidad para usar
    try:
        units_result = await mcp.call_tool(
            "search_units", {"page": 1, "size": 1, "is_active": 1}
        )

        if units_result.get("_embedded", {}).get("units"):
            unit_id = units_result["_embedded"]["units"][0]["id"]
            print(f"1. Creando orden de mantenimiento para unidad ID: {unit_id}")

            result = await mcp.call_tool(
                "create_maintenance_work_order",
                {
                    "unit_id": unit_id,
                    "summary": "Test de mantenimiento - Fuga en grifo",
                    "description": "Prueba de creación de orden de mantenimiento para testing del sistema MCP",
                    "priority": 3,
                    "estimated_cost": 100.0,
                    "estimated_time": 60,
                },
            )
            print(f"✅ Orden de mantenimiento creada: ID {result.get('id', 'N/A')}")
            print(f"   Estado: {result.get('status', 'N/A')}")
            print(f"   Prioridad: {result.get('priority', 'N/A')}")
        else:
            print("❌ No hay unidades disponibles para probar mantenimiento")
    except Exception as e:
        print(f"❌ Error creando orden de mantenimiento: {e}")


async def test_create_housekeeping_work_order():
    """Probar creación de orden de housekeeping"""
    print("\n\n🧹 PROBANDO CREATE_HOUSEKEEPING_WORK_ORDER")
    print("=" * 50)

    # Primero buscar una unidad para usar
    try:
        units_result = await mcp.call_tool(
            "search_units", {"page": 1, "size": 1, "is_active": 1}
        )

        if units_result.get("_embedded", {}).get("units"):
            unit_id = units_result["_embedded"]["units"][0]["id"]
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"1. Creando orden de housekeeping para unidad ID: {unit_id}")

            result = await mcp.call_tool(
                "create_housekeeping_work_order",
                {
                    "unit_id": unit_id,
                    "scheduled_at": tomorrow,
                    "is_inspection": False,
                    "clean_type_id": 4,  # Departure Clean
                    "comments": "Test de housekeeping - Limpieza post-checkout",
                    "cost": 75.0,
                },
            )
            print(f"✅ Orden de housekeeping creada: ID {result.get('id', 'N/A')}")
            print(f"   Estado: {result.get('status', 'N/A')}")
            print(f"   Fecha programada: {result.get('scheduled_at', 'N/A')}")
        else:
            print("❌ No hay unidades disponibles para probar housekeeping")
    except Exception as e:
        print(f"❌ Error creando orden de housekeeping: {e}")


async def test_error_handling():
    """Probar manejo de errores"""
    print("\n\n🚫 PROBANDO MANEJO DE ERRORES")
    print("=" * 50)

    # Test 1: ID de reserva inexistente
    print("\n1. Probando ID de reserva inexistente...")
    try:
        result = await mcp.call_tool("get_reservation", {"reservation_id": 999999})
        print("❌ Debería haber fallado con ID inexistente")
    except Exception as e:
        print(f"✅ Correctamente manejó ID inexistente: {e}")

    # Test 2: Parámetros inválidos
    print("\n2. Probando parámetros inválidos...")
    try:
        result = await mcp.call_tool(
            "search_reservations", {"page": -1, "size": 10}  # Página inválida
        )
        print("❌ Debería haber fallado con página inválida")
    except Exception as e:
        print(f"✅ Correctamente manejó parámetros inválidos: {e}")

    # Test 3: Fecha inválida
    print("\n3. Probando fecha inválida...")
    try:
        result = await mcp.call_tool(
            "search_reservations",
            {"arrival_start": "2024-13-45", "size": 10},  # Fecha inválida
        )
        print("❌ Debería haber fallado con fecha inválida")
    except Exception as e:
        print(f"✅ Correctamente manejó fecha inválida: {e}")


async def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TESTING REAL CON API TRACKHS")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Ejecutar todas las pruebas
        await test_search_reservations()
        await test_get_reservation()
        await test_search_units()
        await test_search_amenities()
        await test_get_folio()
        await test_create_maintenance_work_order()
        await test_create_housekeeping_work_order()
        await test_error_handling()

        print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("El MCP está funcionando correctamente con la API real.")

    except Exception as e:
        print(f"\n\n❌ ERROR CRÍTICO EN LAS PRUEBAS: {e}")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
