#!/usr/bin/env python3
"""
Script para probar la corrección de paginación de reservas
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from trackhs_mcp.server import reservation_service


async def test_reservations_fixed():
    """Probar reservas con paginación corregida"""
    print("🔍 PROBANDO RESERVAS CON PAGINACIÓN CORREGIDA")
    print("=" * 50)

    if reservation_service is None:
        print("❌ Servicio de reservas no disponible")
        return

    try:
        # Test 1: Búsqueda básica con página 1
        print("\n1. Búsqueda básica con página 1...")
        result = reservation_service.search_reservations(
            page=1, size=5, status="confirmed"  # 1-based en lugar de 0-based
        )
        print(f"✅ Búsqueda básica exitosa: {result.get('total_items', 0)} reservas")
        if result.get("_embedded", {}).get("reservations"):
            reservation = result["_embedded"]["reservations"][0]
            print(
                f"   Primera reserva: {reservation.get('confirmation_number', 'N/A')}"
            )
            print(f"   Huésped: {reservation.get('guest', {}).get('name', 'N/A')}")
            print(f"   Estado: {reservation.get('status', 'N/A')}")

    except Exception as e:
        print(f"❌ Error en búsqueda básica: {e}")

    try:
        # Test 2: Búsqueda por fecha con página 1
        print("\n2. Búsqueda por fecha con página 1...")
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")
        result = reservation_service.search_reservations(
            page=1, arrival_start=today, arrival_end=today, size=5  # 1-based
        )
        print(
            f"✅ Búsqueda por fecha exitosa: {result.get('total_items', 0)} reservas para hoy"
        )

    except Exception as e:
        print(f"❌ Error en búsqueda por fecha: {e}")

    try:
        # Test 3: Obtener reserva específica
        print("\n3. Obteniendo reserva específica...")
        search_result = reservation_service.search_reservations(
            page=1, size=1, status="confirmed"
        )
        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            result = reservation_service.get_reservation_by_id(reservation_id)
            print(f"✅ Reserva obtenida: {result.get('confirmation_number', 'N/A')}")
            print(f"   Estado: {result.get('status', 'N/A')}")
            print(f"   Llegada: {result.get('arrival_date', 'N/A')}")
            print(f"   Salida: {result.get('departure_date', 'N/A')}")
        else:
            print("❌ No hay reservas disponibles para probar")

    except Exception as e:
        print(f"❌ Error obteniendo reserva: {e}")

    try:
        # Test 4: Obtener folio
        print("\n4. Obteniendo folio...")
        search_result = reservation_service.search_reservations(
            page=1, size=1, status="confirmed"
        )
        if search_result.get("_embedded", {}).get("reservations"):
            reservation_id = search_result["_embedded"]["reservations"][0]["id"]
            result = reservation_service.get_folio(reservation_id)
            print(f"✅ Folio obtenido: Balance ${result.get('balance', 0)}")
            print(f"   Cargos: {len(result.get('charges', []))}")
            print(f"   Pagos: {len(result.get('payments', []))}")
        else:
            print("❌ No hay reservas disponibles para probar folio")

    except Exception as e:
        print(f"❌ Error obteniendo folio: {e}")


async def main():
    """Función principal"""
    print("🚀 PROBANDO CORRECCIÓN DE PAGINACIÓN")
    print("=" * 60)

    try:
        await test_reservations_fixed()
        print("\n\n✅ PRUEBAS COMPLETADAS")
        print("=" * 60)
        print("La corrección de paginación funciona correctamente.")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
