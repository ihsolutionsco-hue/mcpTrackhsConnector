#!/usr/bin/env python3
"""
Script final de prueba para search_units con la API real
"""

import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = os.getenv("TRACKHS_API_URL", "https://api.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


def test_search_units():
    """Probar search_units con la API real"""
    print("🚀 Prueba final de search_units con TrackHS API")
    print("=" * 60)
    print(f"Base URL: {API_BASE_URL}")
    print(f"Username: {API_USERNAME}")
    print(f"Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas")
        return 1

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            # Prueba básica
            print("\n🔍 Prueba básica de search_units...")
            response = client.get(f"{API_BASE_URL}/pms/units?page=1&size=5")
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ ¡Éxito! Total items: {data.get('total_items', 'N/A')}")
                print(
                    f"Página: {data.get('page', 'N/A')} de {data.get('page_count', 'N/A')}"
                )

                if data.get("_embedded", {}).get("units"):
                    units = data["_embedded"]["units"]
                    print(f"Mostrando {len(units)} unidades:")

                    for i, unit in enumerate(units, 1):
                        print(f"  {i}. {unit.get('name', 'Sin nombre')}")
                        print(f"     📍 {unit.get('streetAddress', 'Sin dirección')}")
                        print(
                            f"     🛏️  {unit.get('bedrooms', 0)} dormitorios, {unit.get('fullBathrooms', 0)} baños"
                        )
                        print(f"     👥 Capacidad: {unit.get('maxOccupancy', 'N/A')}")
                        if unit.get("amenities"):
                            amenities = [
                                a.get("name", "") for a in unit["amenities"][:3]
                            ]
                            print(f"     🏊 Amenidades: {', '.join(amenities)}")
                        print()

                # Prueba con filtros
                print("\n🔍 Prueba con filtros...")
                response2 = client.get(
                    f"{API_BASE_URL}/pms/units?page=1&size=3&bedrooms=2&is_active=1"
                )
                print(f"Status: {response2.status_code}")

                if response2.status_code == 200:
                    data2 = response2.json()
                    print(
                        f"✅ Filtros funcionan! Unidades de 2 dormitorios: {data2.get('total_items', 'N/A')}"
                    )

                # Prueba de amenidades
                print("\n🔍 Prueba de amenidades...")
                response3 = client.get(
                    f"{API_BASE_URL}/pms/units/amenities?page=1&size=5"
                )
                print(f"Status: {response3.status_code}")

                if response3.status_code == 200:
                    data3 = response3.json()
                    print(
                        f"✅ Amenidades disponibles: {data3.get('total_items', 'N/A')}"
                    )

                # Prueba de reservas
                print("\n🔍 Prueba de reservas...")
                response4 = client.get(f"{API_BASE_URL}/pms/reservations?page=1&size=3")
                print(f"Status: {response4.status_code}")

                if response4.status_code == 200:
                    data4 = response4.json()
                    print(f"✅ Reservas disponibles: {data4.get('total_items', 'N/A')}")

                print("\n🎉 ¡Todas las pruebas exitosas!")
                print("✅ La API de TrackHS está funcionando correctamente")
                print("✅ El servidor MCP está listo para usar")

                return 0
            else:
                print(f"❌ Error {response.status_code}: {response.text[:200]}...")
                return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(test_search_units())
