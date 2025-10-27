#!/usr/bin/env python3
"""
Script para probar la corrección del filtro de fechas.
Prueba el workaround implementado para compensar el bug de la API TrackHS.
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trackhs_mcp.api_client import TrackHSClient
from trackhs_mcp.repositories.reservation_repository import ReservationRepository
from trackhs_mcp.services.reservation_service import ReservationService


def test_date_filter_fix():
    """Probar la corrección del filtro de fechas"""

    print("🧪 PROBANDO CORRECCIÓN DEL FILTRO DE FECHAS")
    print("=" * 50)

    # Configurar cliente
    base_url = "https://ihmvacations.trackhs.com"
    username = "aba99777416466b6bdc1a25223192ccb"
    password = "your_password_here"  # Reemplazar con password real

    try:
        # Inicializar cliente y servicios
        api_client = TrackHSClient(base_url, username, password)
        reservation_repo = ReservationRepository(api_client)
        reservation_service = ReservationService(reservation_repo)

        print("✅ Cliente inicializado correctamente")

        # Fecha de hoy para la prueba
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"📅 Buscando reservas para hoy: {today}")

        # Prueba 1: Búsqueda sin filtros (debe funcionar normalmente)
        print("\n🔍 PRUEBA 1: Búsqueda sin filtros de fecha")
        result_no_filter = reservation_service.search_reservations(page=1, size=5)
        print(f"   Reservas encontradas: {result_no_filter.get('total_items', 0)}")
        print(f"   Páginas totales: {result_no_filter.get('page_count', 0)}")

        # Mostrar fechas de las primeras reservas
        reservations = result_no_filter.get("_embedded", {}).get("reservations", [])
        print("   Fechas de llegada de las primeras 3 reservas:")
        for i, res in enumerate(reservations[:3]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"     {i+1}. {arrival_date}")

        # Prueba 2: Búsqueda con filtro de fecha (debe aplicar workaround)
        print(f"\n🔍 PRUEBA 2: Búsqueda con filtro de fecha (hoy: {today})")
        result_with_filter = reservation_service.search_reservations(
            page=1, size=20, arrival_start=today, arrival_end=today
        )
        print(f"   Reservas encontradas: {result_with_filter.get('total_items', 0)}")
        print(f"   Páginas totales: {result_with_filter.get('page_count', 0)}")

        # Mostrar fechas de las reservas filtradas
        filtered_reservations = result_with_filter.get("_embedded", {}).get(
            "reservations", []
        )
        print("   Fechas de llegada de las reservas filtradas:")
        for i, res in enumerate(filtered_reservations[:5]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"     {i+1}. {arrival_date}")

        # Prueba 3: Búsqueda con rango de fechas
        print(f"\n🔍 PRUEBA 3: Búsqueda con rango de fechas (últimos 7 días)")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        result_range = reservation_service.search_reservations(
            page=1, size=20, arrival_start=week_ago, arrival_end=today
        )
        print(f"   Reservas encontradas: {result_range.get('total_items', 0)}")
        print(f"   Rango: {week_ago} a {today}")

        # Mostrar fechas de las reservas en el rango
        range_reservations = result_range.get("_embedded", {}).get("reservations", [])
        print("   Fechas de llegada de las reservas en el rango:")
        for i, res in enumerate(range_reservations[:5]):
            arrival_date = res.get("arrivalDate", "N/A")
            print(f"     {i+1}. {arrival_date}")

        print("\n✅ PRUEBAS COMPLETADAS")

        # Resumen
        print("\n📊 RESUMEN:")
        print(f"   Sin filtros: {result_no_filter.get('total_items', 0)} reservas")
        print(
            f"   Con filtro (hoy): {result_with_filter.get('total_items', 0)} reservas"
        )
        print(f"   Con rango (7 días): {result_range.get('total_items', 0)} reservas")

        if result_with_filter.get("total_items", 0) < result_no_filter.get(
            "total_items", 0
        ):
            print("   ✅ El filtro de fechas está funcionando correctamente")
        else:
            print("   ⚠️  El filtro de fechas podría no estar funcionando como esperado")

    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    success = test_date_filter_fix()
    sys.exit(0 if success else 1)
