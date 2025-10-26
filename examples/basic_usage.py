"""
Ejemplos básicos de uso del TrackHS MCP Server.

Este script demuestra cómo usar cada herramienta del servidor MCP.
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar el servidor MCP
from src.trackhs_mcp import server


def example_1_search_reservations():
    """Ejemplo 1: Buscar reservas que llegan hoy"""
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Buscar reservas que llegan hoy")
    print("=" * 60)

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        result = server.search_reservations(
            arrival_start=today, arrival_end=today, status="confirmed", page=0, size=10
        )

        print(f"\n✅ Reservas encontradas: {result['total_items']}")
        print(f"   Página: {result['page'] + 1} de {result['page_count']}")

        if result["total_items"] > 0:
            print("\n📋 Detalles de reservas:")
            for reservation in result["_embedded"]["reservations"]:
                print(
                    f"\n   • Confirmación: {reservation.get('confirmationNumber', 'N/A')}"
                )
                print(f"     Huésped: {reservation.get('guestName', 'N/A')}")
                print(f"     Estado: {reservation.get('status', 'N/A')}")
                print(f"     Llegada: {reservation.get('arrival', 'N/A')}")
                print(f"     Salida: {reservation.get('departure', 'N/A')}")
        else:
            print("\n   No hay llegadas para hoy")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_2_get_reservation():
    """Ejemplo 2: Obtener detalles de una reserva específica"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Obtener detalles de reserva")
    print("=" * 60)

    # Nota: Cambiar el ID por uno válido de tu sistema
    reservation_id = 12345

    try:
        result = server.get_reservation(reservation_id=reservation_id)

        print(f"\n✅ Reserva #{reservation_id} encontrada")
        print(f"\n📋 Detalles:")
        print(f"   • Confirmación: {result.get('confirmationNumber', 'N/A')}")
        print(f"   • Estado: {result.get('status', 'N/A')}")
        print(f"   • Llegada: {result.get('arrival', 'N/A')}")
        print(f"   • Salida: {result.get('departure', 'N/A')}")

        if "guest" in result:
            print(f"\n👤 Huésped:")
            print(f"   • Nombre: {result['guest'].get('name', 'N/A')}")
            print(f"   • Email: [REDACTED]")  # Protegido
            print(f"   • Teléfono: [REDACTED]")  # Protegido

        if "unit" in result:
            print(f"\n🏠 Unidad:")
            print(f"   • Nombre: {result['unit'].get('name', 'N/A')}")
            print(f"   • Código: {result['unit'].get('code', 'N/A')}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_3_search_units():
    """Ejemplo 3: Buscar unidades disponibles"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Buscar unidades de 2 habitaciones")
    print("=" * 60)

    try:
        result = server.search_units(
            bedrooms=2, bathrooms=2, is_active=1, is_bookable=1, page=1, size=5
        )

        print(f"\n✅ Unidades encontradas: {result['total_items']}")

        if result["total_items"] > 0:
            print("\n🏠 Listado de unidades:")
            for unit in result["_embedded"]["units"]:
                print(f"\n   • {unit.get('name', 'N/A')} ({unit.get('code', 'N/A')})")
                print(
                    f"     {unit.get('bedrooms', 0)} dormitorios, {unit.get('bathrooms', 0)} baños"
                )
                print(f"     Activa: {'Sí' if unit.get('isActive') else 'No'}")
                print(f"     Reservable: {'Sí' if unit.get('isBookable') else 'No'}")
        else:
            print("\n   No hay unidades disponibles con esos criterios")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_4_get_folio():
    """Ejemplo 4: Obtener folio financiero"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Obtener folio financiero")
    print("=" * 60)

    # Nota: Cambiar el ID por uno válido de tu sistema
    reservation_id = 12345

    try:
        result = server.get_folio(reservation_id=reservation_id)

        print(f"\n✅ Folio de reserva #{reservation_id}")
        print(f"\n💰 Estado Financiero:")
        print(f"   • Total: ${result.get('total', 0):.2f}")
        print(f"   • Balance pendiente: ${result.get('balance', 0):.2f}")
        print(f"   • Pagado: ${result.get('total', 0) - result.get('balance', 0):.2f}")

        if result.get("balance", 0) > 0:
            print(f"\n   ⚠️  Pago pendiente: ${result['balance']:.2f}")
        else:
            print(f"\n   ✅ Pagado completo")

        # Mostrar cargos si existen
        if "charges" in result and result["charges"]:
            print(f"\n📋 Cargos ({len(result['charges'])} total):")
            for charge in result["charges"][:5]:  # Primeros 5
                print(
                    f"   • {charge.get('description', 'N/A')}: ${charge.get('amount', 0):.2f}"
                )

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_5_create_maintenance_work_order():
    """Ejemplo 5: Crear orden de mantenimiento"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Crear orden de mantenimiento")
    print("=" * 60)

    # Nota: Cambiar el unit_id por uno válido de tu sistema
    unit_id = 101

    try:
        result = server.create_maintenance_work_order(
            unit_id=unit_id,
            summary="Revisar aire acondicionado",
            description="El aire acondicionado de la sala no enfría adecuadamente. Verificar termostato, filtros y nivel de refrigerante.",
            priority=3,  # Media
            estimated_cost=150.00,
            estimated_time=120,  # 2 horas
        )

        print(f"\n✅ Orden de mantenimiento creada")
        print(f"\n📋 Detalles:")
        print(f"   • ID: #{result.get('id', 'N/A')}")
        print(f"   • Estado: {result.get('status', 'N/A')}")
        print(f"   • Prioridad: {result.get('priority', 'N/A')}")
        print(f"   • Unidad: #{result.get('unitId', unit_id)}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_6_create_housekeeping_work_order():
    """Ejemplo 6: Crear orden de housekeeping"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Crear orden de housekeeping")
    print("=" * 60)

    # Nota: Cambiar el unit_id por uno válido de tu sistema
    unit_id = 101
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        result = server.create_housekeeping_work_order(
            unit_id=unit_id,
            scheduled_at=tomorrow,
            is_inspection=False,
            clean_type_id=1,  # Limpieza completa
            comments="Check-out a las 11am, check-in a las 3pm. Revisar inventario.",
            cost=50.00,
        )

        print(f"\n✅ Orden de housekeeping creada")
        print(f"\n📋 Detalles:")
        print(f"   • ID: #{result.get('id', 'N/A')}")
        print(f"   • Estado: {result.get('status', 'N/A')}")
        print(
            f"   • Tipo: {'Inspección' if result.get('isInspection') else 'Limpieza'}"
        )
        print(f"   • Fecha programada: {result.get('scheduledAt', tomorrow)}")
        print(f"   • Unidad: #{result.get('unitId', unit_id)}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def example_7_search_amenities():
    """Ejemplo 7: Buscar amenidades"""
    print("\n" + "=" * 60)
    print("EJEMPLO 7: Buscar amenidades disponibles")
    print("=" * 60)

    try:
        result = server.search_amenities(search="wifi", page=1, size=10)

        print(f"\n✅ Amenidades encontradas: {result['total_items']}")

        if result["total_items"] > 0:
            print("\n🎯 Listado de amenidades:")
            for amenity in result["_embedded"]["amenities"]:
                print(f"\n   • {amenity.get('name', 'N/A')}")
                print(f"     Grupo: {amenity.get('group', 'N/A')}")
                print(f"     Pública: {'Sí' if amenity.get('isPublic') else 'No'}")
                if amenity.get("description"):
                    print(f"     Descripción: {amenity['description'][:50]}...")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 60)
    print("🏨 EJEMPLOS DE USO - TRACKHS MCP SERVER")
    print("=" * 60)

    print("\n⚙️  Verificando credenciales...")
    if not os.getenv("TRACKHS_USERNAME") or not os.getenv("TRACKHS_PASSWORD"):
        print("\n❌ ERROR: Credenciales no configuradas")
        print("   Por favor configura TRACKHS_USERNAME y TRACKHS_PASSWORD en .env")
        return

    print("✅ Credenciales configuradas")

    # Ejecutar ejemplos
    try:
        example_1_search_reservations()
        example_2_get_reservation()
        example_3_search_units()
        example_4_get_folio()
        example_5_create_maintenance_work_order()
        example_6_create_housekeeping_work_order()
        example_7_search_amenities()

    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida por el usuario")

    print("\n" + "=" * 60)
    print("✅ Ejemplos completados")
    print("=" * 60)
    print("\n💡 Nota: Algunos ejemplos pueden fallar si los IDs no existen")
    print("   Cambia los IDs por valores válidos en tu sistema TrackHS\n")


if __name__ == "__main__":
    main()
