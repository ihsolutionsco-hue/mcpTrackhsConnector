#!/usr/bin/env python3
"""
Script para probar diferentes variaciones de la URL de TrackHS
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
BASE_URL = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


def test_url_variation(url, description):
    """Probar una variación de URL"""
    print(f"\n🔍 {description}")
    print(f"   URL: {url}")

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=10.0) as client:
            response = client.get(f"{url}/pms/units?page=1&size=1")
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(
                        f"   ✅ ¡Éxito! - Total items: {data.get('total_items', 'N/A')}"
                    )
                    return True
                except json.JSONDecodeError:
                    print(f"   ⚠️  Respuesta no es JSON válido")
                    print(f"   Content: {response.text[:200]}...")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint no encontrado")
            elif response.status_code == 401:
                print(f"   ❌ No autorizado")
            elif response.status_code == 403:
                print(f"   ❌ Prohibido")
            else:
                print(f"   ❌ Error {response.status_code}")
                print(f"   Content: {response.text[:200]}...")

    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

    return False


def main():
    """Función principal"""
    print("🔍 Probando variaciones de URL de TrackHS")
    print("=" * 60)

    # Verificar credenciales
    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas en .env")
        return 1

    print(f"Base URL: {BASE_URL}")
    print(f"Username: {API_USERNAME}")
    print(f"Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    # Variaciones de URL a probar
    url_variations = [
        (f"{BASE_URL}", "URL base sin /api"),
        (f"{BASE_URL}/api", "URL base con /api"),
        (f"{BASE_URL}/api/v1", "URL base con /api/v1"),
        (f"{BASE_URL}/api/v2", "URL base con /api/v2"),
        (f"{BASE_URL}/v1", "URL base con /v1"),
        (f"{BASE_URL}/v2", "URL base con /v2"),
        (f"{BASE_URL}/pms", "URL base con /pms"),
        (f"{BASE_URL}/pms/api", "URL base con /pms/api"),
    ]

    working_urls = []

    # Probar cada variación
    for url, description in url_variations:
        if test_url_variation(url, description):
            working_urls.append((url, description))

    if working_urls:
        print(f"\n✅ URLs funcionales encontradas: {len(working_urls)}")
        for url, description in working_urls:
            print(f"   • {url} - {description}")

        print(f"\n🎉 ¡Éxito! Usa esta URL en tu archivo .env:")
        print(f"   TRACKHS_API_URL={working_urls[0][0]}")

        # Probar algunos endpoints adicionales con la URL que funciona
        working_url = working_urls[0][0]
        print(f"\n🧪 Probando endpoints adicionales con: {working_url}")

        additional_endpoints = [
            "/pms/units/amenities?page=1&size=1",
            "/pms/reservations?page=1&size=1",
            "/pms/units?page=1&size=5",
        ]

        for endpoint in additional_endpoints:
            try:
                with httpx.Client(
                    auth=(API_USERNAME, API_PASSWORD), timeout=10.0
                ) as client:
                    response = client.get(f"{working_url}{endpoint}")
                    print(f"   {endpoint}: {response.status_code}")

                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(
                                f"      ✅ Total items: {data.get('total_items', 'N/A')}"
                            )
                        except json.JSONDecodeError:
                            print(f"      ⚠️  No es JSON válido")
                    else:
                        print(f"      ❌ Error {response.status_code}")

            except Exception as e:
                print(f"      ❌ Error: {e}")

        return 0
    else:
        print("\n❌ No se encontraron URLs funcionales")
        print("   Posibles causas:")
        print("   • La API no está disponible en este dominio")
        print("   • Las credenciales son incorrectas")
        print("   • La API requiere un endpoint diferente")
        print("   • Necesitas contactar al soporte de TrackHS")

        return 1


if __name__ == "__main__":
    sys.exit(main())
