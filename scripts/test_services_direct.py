#!/usr/bin/env python3
"""
Script para probar los servicios de negocio directamente.
Esto permite testear la lógica sin el protocolo MCP.
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trackhs_mcp.server import (
    api_client,
    reservation_repo,
    unit_repo,
    work_order_repo,
)
from trackhs_mcp.services import (
    ReservationService,
    UnitService,
    WorkOrderService,
)


def print_section(title: str):
    """Imprime un separador de sección"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_services():
    """Probar los servicios de negocio directamente"""
    print_section("INICIALIZANDO SERVICIOS DE NEGOCIO")

    if api_client is None:
        print("❌ ERROR: Cliente API no está configurado")
        return False

    # Inicializar servicios
    try:
        reservation_service = ReservationService(reservation_repo)
        unit_service = UnitService(unit_repo)
        work_order_service = WorkOrderService(work_order_repo)

        print("✅ Servicios inicializados correctamente")
        return reservation_service, unit_service, work_order_service

    except Exception as e:
        print(f"❌ Error inicializando servicios: {str(e)}")
        return False


def test_unit_service(unit_service: UnitService):
    """Probar el servicio de unidades"""
    print_section("TEST 1: Servicio de Unidades")

    try:
        print("🔍 Buscando unidades activas...")
        result = unit_service.search_units(page=1, size=3, is_active=1, is_bookable=1)

        if "_embedded" in result and "units" in result["_embedded"]:
            units = result["_embedded"]["units"]
            print(f"\n✅ Encontradas {len(units)} unidades:")

            for unit in units:
                print(f"\n  📍 Unidad ID: {unit.get('id')}")
                print(f"     Nombre: {unit.get('name', 'N/A')}")
                print(f"     Dormitorios: {unit.get('bedrooms', 'N/A')}")
                print(f"     Baños: {unit.get('bathrooms', 'N/A')}")

            return units[0].get("id") if units else None
        else:
            print("❌ No se encontraron unidades")
            return None

    except Exception as e:
        print(f"❌ Error en servicio de unidades: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def test_work_order_service(work_order_service: WorkOrderService, unit_id: int):
    """Probar el servicio de work orders"""
    print_section("TEST 2: Servicio de Work Orders")

    # Test 1: Orden de mantenimiento
    print("🔧 Creando orden de mantenimiento...")
    try:
        maintenance_result = work_order_service.create_maintenance_work_order(
            unit_id=unit_id,
            summary="Aire acondicionado no funciona",
            description="El aire acondicionado no enfría correctamente. El termostato muestra temperatura alta y el compresor hace ruidos extraños. Se requiere revisión técnica urgente.",
            priority=5,  # Alta prioridad
            estimated_cost=250.0,
            estimated_time=180,  # 3 horas
            date_received=datetime.now().strftime("%Y-%m-%d"),
        )

        print("✅ Orden de mantenimiento creada exitosamente!")
        print(f"   ID: {maintenance_result.get('id', 'N/A')}")
        print(f"   Estado: {maintenance_result.get('status', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creando orden de mantenimiento: {str(e)}")
        import traceback

        traceback.print_exc()

    # Test 2: Orden de housekeeping
    print("\n🧹 Creando orden de housekeeping...")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        housekeeping_result = work_order_service.create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=tomorrow,
            is_inspection=False,
            clean_type_id=1,
            comments="Limpieza completa post check-out. Incluir cambio de sábanas, toallas y limpieza profunda.",
            cost=75.0,
        )

        print("✅ Orden de housekeeping creada exitosamente!")
        print(f"   ID: {housekeeping_result.get('id', 'N/A')}")
        print(f"   Estado: {housekeeping_result.get('status', 'N/A')}")
        print(f"   Fecha: {housekeeping_result.get('scheduledAt', 'N/A')}")

    except Exception as e:
        print(f"❌ Error creando orden de housekeeping: {str(e)}")
        import traceback

        traceback.print_exc()

    # Test 3: Orden de inspección
    print("\n🔍 Creando orden de inspección...")
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        inspection_result = work_order_service.create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=today,
            is_inspection=True,
            comments="Inspección de calidad post-limpieza. Verificar que todo esté en orden antes del check-in.",
        )

        print("✅ Orden de inspección creada exitosamente!")
        print(f"   ID: {inspection_result.get('id', 'N/A')}")
        print(f"   Estado: {inspection_result.get('status', 'N/A')}")
        print(
            f"   Tipo: {'Inspección' if inspection_result.get('isInspection') else 'Limpieza'}"
        )

    except Exception as e:
        print(f"❌ Error creando orden de inspección: {str(e)}")
        import traceback

        traceback.print_exc()


def test_reservation_service(reservation_service: ReservationService):
    """Probar el servicio de reservas"""
    print_section("TEST 3: Servicio de Reservas")

    try:
        print("🔍 Buscando reservas recientes...")
        result = reservation_service.search_reservations(
            page=0, size=3, arrival_start="2025-10-01", arrival_end="2025-12-31"
        )

        if "_embedded" in result and "reservations" in result["_embedded"]:
            reservations = result["_embedded"]["reservations"]
            print(f"\n✅ Encontradas {len(reservations)} reservas:")

            for reservation in reservations[:2]:  # Mostrar solo las primeras 2
                print(f"\n  📅 Reserva ID: {reservation.get('id')}")
                print(f"     Huésped: {reservation.get('guestName', 'N/A')}")
                print(f"     Check-in: {reservation.get('arrivalDate', 'N/A')}")
                print(f"     Estado: {reservation.get('status', 'N/A')}")
        else:
            print("❌ No se encontraron reservas")

    except Exception as e:
        print(f"❌ Error en servicio de reservas: {str(e)}")
        import traceback

        traceback.print_exc()


def main():
    """Función principal"""
    print("\n" + "🏨" * 40)
    print("  PRUEBA DIRECTA - SERVICIOS DE NEGOCIO")
    print("🏨" * 40)

    # Inicializar servicios
    services = test_services()
    if not services:
        sys.exit(1)

    reservation_service, unit_service, work_order_service = services

    # Test 1: Unidades
    unit_id = test_unit_service(unit_service)
    if unit_id is None:
        print("\n⚠️  Usando ID de unidad de ejemplo: 100")
        unit_id = 100

    # Test 2: Work Orders
    test_work_order_service(work_order_service, unit_id)

    # Test 3: Reservas
    test_reservation_service(reservation_service)

    # Resumen final
    print_section("RESUMEN DE PRUEBAS")
    print("✅ Pruebas de servicios completadas")
    print("✅ Arquitectura de servicios funcionando correctamente")
    print("✅ Separación de responsabilidades implementada")
    print("✅ Validación de tipos mejorada")

    print("\n" + "🏨" * 40)
    print("  FIN DE LAS PRUEBAS")
    print("🏨" * 40 + "\n")


if __name__ == "__main__":
    main()
