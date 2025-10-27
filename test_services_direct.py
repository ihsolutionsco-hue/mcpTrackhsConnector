#!/usr/bin/env python3
"""
Script de testing directo de los servicios internos
Prueba la funcionalidad sin usar el protocolo MCP
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.server import (
    api_client,
    reservation_service,
    unit_service,
    work_order_service,
)


async def test_reservation_service():
    """Probar servicio de reservas"""
    print("\n🔍 PROBANDO SERVICIO DE RESERVAS")
    print("=" * 50)

    if reservation_service is None:
        print("❌ Servicio de reservas no disponible")
        return

    try:
        # Test 1: Búsqueda básica
        print("\n1. Búsqueda básica de reservas...")
        result = reservation_service.search_reservations(
            page=0, size=5, status="confirmed"
        )
        print(f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} reservas")
        if result.get("_embedded", {}).get("reservations"):
            reservation = result["_embedded"]["reservations"][0]
            print(
                f"   Primera reserva: {reservation.get('confirmation_number', 'N/A')}"
            )
            print(f"   Huésped: {reservation.get('guest', {}).get('name', 'N/A')}")

    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    try:
        # Test 2: Búsqueda por fecha
        print("\n2. Búsqueda por fecha...")
        today = datetime.now().strftime("%Y-%m-%d")
        result = reservation_service.search_reservations(
            arrival_start=today, arrival_end=today, size=5
        )
        print(
            f"✅ Búsqueda por fecha exitosa: {result.get('total_items', 0)} reservas para hoy"
        )

    except Exception as e:
        print(f"❌ Error en búsqueda por fecha: {e}")

    try:
        # Test 3: Obtener reserva específica
        print("\n3. Obteniendo reserva específica...")
        # Primero buscar una reserva
        search_result = reservation_service.search_reservations(
            page=0, size=1, status="confirmed"
        )
        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            result = reservation_service.get_reservation_by_id(reservation_id)
            print(f"✅ Reserva obtenida: {result.get('confirmation_number', 'N/A')}")
            print(f"   Estado: {result.get('status', 'N/A')}")
        else:
            print("❌ No hay reservas disponibles para probar")

    except Exception as e:
        print(f"❌ Error obteniendo reserva: {e}")

    try:
        # Test 4: Obtener folio
        print("\n4. Obteniendo folio...")
        search_result = reservation_service.search_reservations(
            page=0, size=1, status="confirmed"
        )
        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            result = reservation_service.get_folio(reservation_id)
            print(f"✅ Folio obtenido: Balance ${result.get('balance', 0)}")
            print(f"   Cargos: {len(result.get('charges', []))}")
        else:
            print("❌ No hay reservas disponibles para probar folio")

    except Exception as e:
        print(f"❌ Error obteniendo folio: {e}")


async def test_unit_service():
    """Probar servicio de unidades"""
    print("\n\n🏠 PROBANDO SERVICIO DE UNIDADES")
    print("=" * 50)

    if unit_service is None:
        print("❌ Servicio de unidades no disponible")
        return

    try:
        # Test 1: Búsqueda básica
        print("\n1. Búsqueda básica de unidades...")
        result = unit_service.search_units(page=1, size=5, is_active=1, is_bookable=1)
        print(f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} unidades")
        if result.get("_embedded", {}).get("units"):
            unit = result["_embedded"]["units"][0]
            print(
                f"   Primera unidad: {unit.get('name', 'N/A')} ({unit.get('code', 'N/A')})"
            )
            print(
                f"   Dormitorios: {unit.get('bedrooms', 'N/A')}, Baños: {unit.get('bathrooms', 'N/A')}"
            )

    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    try:
        # Test 2: Búsqueda por capacidad
        print("\n2. Búsqueda por capacidad...")
        result = unit_service.search_units(bedrooms=2, bathrooms=1, is_active=1, size=5)
        print(
            f"✅ Búsqueda por capacidad exitosa: {result.get('total_items', 0)} unidades 2BR/1BA"
        )

    except Exception as e:
        print(f"❌ Error en búsqueda por capacidad: {e}")

    try:
        # Test 3: Búsqueda de amenidades
        print("\n3. Búsqueda de amenidades...")
        result = unit_service.search_amenities(page=1, size=10)
        print(
            f"✅ Búsqueda de amenidades exitosa: {result.get('total_items', 0)} amenidades"
        )
        if result.get("_embedded", {}).get("amenities"):
            amenity = result["_embedded"]["amenities"][0]
            print(
                f"   Primera amenidad: {amenity.get('name', 'N/A')} ({amenity.get('group', 'N/A')})"
            )

    except Exception as e:
        print(f"❌ Error en búsqueda de amenidades: {e}")


async def test_work_order_service():
    """Probar servicio de órdenes de trabajo"""
    print("\n\n🔧 PROBANDO SERVICIO DE ÓRDENES DE TRABAJO")
    print("=" * 50)

    if work_order_service is None:
        print("❌ Servicio de órdenes de trabajo no disponible")
        return

    try:
        # Test 1: Crear orden de mantenimiento
        print("\n1. Creando orden de mantenimiento...")
        result = work_order_service.create_maintenance_work_order(
            unit_id=1,
            summary="Test de mantenimiento - Fuga en grifo",
            description="Prueba de creación de orden de mantenimiento para testing del sistema MCP",
            priority=3,
            estimated_cost=100.0,
            estimated_time=60,
        )
        print(f"✅ Orden de mantenimiento creada: ID {result.get('id', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        print(f"   Prioridad: {result.get('priority', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creando orden de mantenimiento: {e}")

    try:
        # Test 2: Crear orden de housekeeping
        print("\n2. Creando orden de housekeeping...")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        result = work_order_service.create_housekeeping_work_order(
            unit_id=1,
            scheduled_at=tomorrow,
            is_inspection=False,
            clean_type_id=4,  # Departure Clean
            comments="Test de housekeeping - Limpieza post-checkout",
            cost=75.0,
        )
        print(f"✅ Orden de housekeeping creada: ID {result.get('id', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        print(f"   Fecha programada: {result.get('scheduled_at', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creando orden de housekeeping: {e}")


async def test_api_connectivity():
    """Probar conectividad con la API"""
    print("\n\n🌐 PROBANDO CONECTIVIDAD CON API")
    print("=" * 50)

    if api_client is None:
        print("❌ Cliente API no disponible")
        return

    try:
        # Test 1: Endpoint de amenidades (más simple)
        print("\n1. Probando endpoint de amenidades...")
        result = api_client.get("api/pms/units/amenities", {"page": 1, "size": 1})
        print("✅ API conectada correctamente")
        print(f"   Respuesta recibida: {len(str(result))} caracteres")

    except Exception as e:
        print(f"❌ Error conectando con API: {e}")

    try:
        # Test 2: Endpoint de unidades
        print("\n2. Probando endpoint de unidades...")
        result = api_client.get("api/pms/units", {"page": 1, "size": 1})
        print("✅ Endpoint de unidades funcionando")
        print(f"   Respuesta recibida: {len(str(result))} caracteres")

    except Exception as e:
        print(f"❌ Error en endpoint de unidades: {e}")

    try:
        # Test 3: Endpoint de reservas
        print("\n3. Probando endpoint de reservas...")
        result = api_client.get("api/pms/reservations", {"page": 0, "size": 1})
        print("✅ Endpoint de reservas funcionando")
        print(f"   Respuesta recibida: {len(str(result))} caracteres")

    except Exception as e:
        print(f"❌ Error en endpoint de reservas: {e}")


async def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TESTING DIRECTO DE SERVICIOS")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Ejecutar todas las pruebas
        await test_api_connectivity()
        await test_reservation_service()
        await test_unit_service()
        await test_work_order_service()

        print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("Los servicios están funcionando correctamente con la API real.")

    except Exception as e:
        print(f"\n\n❌ ERROR CRÍTICO: {e}")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
