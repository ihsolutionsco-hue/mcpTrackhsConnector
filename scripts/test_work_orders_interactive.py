#!/usr/bin/env python3
"""
Script interactivo para probar las herramientas de Work Orders del MCP TrackHS.
Simula un usuario real usando las herramientas.
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trackhs_mcp.server import (
    api_client,
    create_housekeeping_work_order,
    create_maintenance_work_order,
    search_reservations,
    search_units,
)


def print_section(title: str):
    """Imprime un separador de sección"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_search_units():
    """Prueba 1: Buscar unidades disponibles"""
    print_section("TEST 1: Buscar unidades disponibles para trabajo")

    try:
        print("🔍 Buscando unidades activas...")
        result = search_units(page=1, size=5, is_active=1)

        if "_embedded" in result and "units" in result["_embedded"]:
            units = result["_embedded"]["units"]
            print(f"\n✅ Encontradas {len(units)} unidades:")

            for unit in units[:3]:  # Mostrar solo las primeras 3
                print(f"\n  📍 Unidad ID: {unit.get('id')}")
                print(f"     Nombre: {unit.get('name', 'N/A')}")
                print(f"     Dormitorios: {unit.get('bedrooms', 'N/A')}")
                print(f"     Baños: {unit.get('bathrooms', 'N/A')}")

            return units[0].get("id") if units else None
        else:
            print("❌ No se encontraron unidades")
            return None

    except Exception as e:
        print(f"❌ Error buscando unidades: {str(e)}")
        return None


def test_create_maintenance_order(unit_id: int):
    """Prueba 2: Crear orden de trabajo de mantenimiento"""
    print_section("TEST 2: Crear orden de trabajo de MANTENIMIENTO")

    print(f"🔧 Creando orden de mantenimiento para unidad {unit_id}...")
    print("\n📝 Datos de la orden:")
    print("   - Problema: Aire acondicionado no funciona")
    print("   - Prioridad: ALTA (5)")
    print("   - Costo estimado: $250.00")
    print("   - Tiempo estimado: 3 horas (180 minutos)")

    try:
        result = create_maintenance_work_order(
            unit_id=unit_id,
            summary="Aire acondicionado no funciona correctamente",
            description="El aire acondicionado no enfría. El termostato muestra temperatura alta constante y el compresor hace ruidos extraños. Se requiere revisión técnica urgente antes del próximo check-in programado.",
            priority=5,  # Alta prioridad
            estimated_cost=250.0,
            estimated_time=180,  # 3 horas
            date_received=datetime.now().strftime("%Y-%m-%d"),
        )

        print("\n✅ Orden de mantenimiento creada exitosamente!")
        print(f"\n📋 Detalles de la orden:")
        print(f"   ID: {result.get('id', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        print(f"   Fecha creación: {result.get('dateReceived', 'N/A')}")

        if "_links" in result:
            print(f"\n🔗 Enlaces disponibles:")
            for link_name, link_data in result["_links"].items():
                if isinstance(link_data, dict) and "href" in link_data:
                    print(f"   - {link_name}: {link_data['href']}")

        return result.get("id")

    except Exception as e:
        print(f"❌ Error creando orden de mantenimiento: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def test_create_housekeeping_order(unit_id: int):
    """Prueba 3: Crear orden de trabajo de housekeeping"""
    print_section("TEST 3: Crear orden de trabajo de HOUSEKEEPING")

    # Programar para mañana
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"🧹 Creando orden de housekeeping para unidad {unit_id}...")
    print(f"\n📝 Datos de la orden:")
    print(f"   - Fecha programada: {tomorrow}")
    print("   - Tipo: Limpieza completa (turnover)")
    print("   - Clean Type ID: 1")
    print("   - Costo: $75.00")

    try:
        result = create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=tomorrow,
            is_inspection=False,
            clean_type_id=1,
            comments="Limpieza completa post check-out. Incluir cambio de sábanas, toallas y limpieza profunda de baños y cocina.",
            cost=75.0,
        )

        print("\n✅ Orden de housekeeping creada exitosamente!")
        print(f"\n📋 Detalles de la orden:")
        print(f"   ID: {result.get('id', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        print(f"   Fecha programada: {result.get('scheduledAt', 'N/A')}")
        print(f"   Tipo: {'Inspección' if result.get('isInspection') else 'Limpieza'}")

        return result.get("id")

    except Exception as e:
        print(f"❌ Error creando orden de housekeeping: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def test_create_inspection_order(unit_id: int):
    """Prueba 4: Crear orden de inspección"""
    print_section("TEST 4: Crear orden de INSPECCIÓN")

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"🔍 Creando orden de inspección para unidad {unit_id}...")
    print(f"\n📝 Datos de la orden:")
    print(f"   - Fecha programada: {today}")
    print("   - Tipo: Inspección de calidad")

    try:
        result = create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=today,
            is_inspection=True,
            comments="Inspección de calidad post-limpieza. Verificar que todo esté en orden antes del check-in de las 3 PM.",
        )

        print("\n✅ Orden de inspección creada exitosamente!")
        print(f"\n📋 Detalles de la orden:")
        print(f"   ID: {result.get('id', 'N/A')}")
        print(f"   Estado: {result.get('status', 'N/A')}")
        print(f"   Fecha programada: {result.get('scheduledAt', 'N/A')}")

        return result.get("id")

    except Exception as e:
        print(f"❌ Error creando orden de inspección: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def main():
    """Función principal"""
    print("\n" + "🏨" * 40)
    print("  PRUEBA INTERACTIVA - WORK ORDERS TRACKHS MCP")
    print("🏨" * 40)

    # Verificar que el cliente API esté disponible
    if api_client is None:
        print("\n❌ ERROR: Cliente API no está configurado")
        print("   Configure las variables TRACKHS_USERNAME y TRACKHS_PASSWORD")
        sys.exit(1)

    print("\n✅ Cliente API configurado correctamente")
    print(f"   Base URL: {api_client.base_url}")

    # TEST 1: Buscar unidades
    unit_id = test_search_units()

    if unit_id is None:
        print("\n⚠️  No se pudo obtener un ID de unidad válido")
        print("   Usando ID de ejemplo: 100")
        unit_id = 100

    # TEST 2: Crear orden de mantenimiento
    maintenance_id = test_create_maintenance_order(unit_id)

    # TEST 3: Crear orden de housekeeping
    housekeeping_id = test_create_housekeeping_order(unit_id)

    # TEST 4: Crear orden de inspección
    inspection_id = test_create_inspection_order(unit_id)

    # Resumen final
    print_section("RESUMEN DE PRUEBAS")

    print("📊 Resultados:")
    print(f"   ✅ Unidad usada: {unit_id}")
    print(
        f"   {'✅' if maintenance_id else '❌'} Orden de mantenimiento: {maintenance_id or 'FALLÓ'}"
    )
    print(
        f"   {'✅' if housekeeping_id else '❌'} Orden de housekeeping: {housekeeping_id or 'FALLÓ'}"
    )
    print(
        f"   {'✅' if inspection_id else '❌'} Orden de inspección: {inspection_id or 'FALLÓ'}"
    )

    successful = sum(
        [
            maintenance_id is not None,
            housekeeping_id is not None,
            inspection_id is not None,
        ]
    )

    print(f"\n🎯 Tasa de éxito: {successful}/3 ({successful*100//3}%)")

    print("\n" + "🏨" * 40)
    print("  FIN DE LAS PRUEBAS")
    print("🏨" * 40 + "\n")


if __name__ == "__main__":
    main()
