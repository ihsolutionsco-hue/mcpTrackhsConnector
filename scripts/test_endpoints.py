#!/usr/bin/env python3
"""
Script para probar diferentes endpoints de TrackHS
"""

import json
import os
import sys

import httpx


def test_endpoint(base_url: str, endpoint: str, username: str, password: str):
    """Probar un endpoint específico"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔍 Probando endpoint: {full_url}")

    try:
        with httpx.Client(auth=(username, password), timeout=10.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})

            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content-Length: {len(response.text)}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Endpoint funciona")
                    print(f"   Claves en respuesta: {list(data.keys())}")
                    if "total_items" in data:
                        print(f"   Total items: {data['total_items']}")
                    return True
                except json.JSONDecodeError:
                    print("   ❌ Respuesta no es JSON válido")
                    print(f"   Preview: {response.text[:200]}")
                    return False
            elif response.status_code == 401:
                print("   ❌ Error 401 - Credenciales inválidas")
                return False
            elif response.status_code == 403:
                print("   ❌ Error 403 - Acceso denegado")
                return False
            elif response.status_code == 404:
                print("   ❌ Error 404 - Endpoint no encontrado")
                return False
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                print(f"   Respuesta: {response.text[:200]}")
                return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def main():
    """Función principal"""
    print("🔍 Probando diferentes endpoints de TrackHS")
    print("=" * 60)

    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        return

    base_url = "https://ihmvacations.trackhs.com/api"

    # Diferentes endpoints a probar
    endpoints = [
        # Endpoints principales
        "pms/units",
        "pms/reservations",
        "pms/units/amenities",
        # Endpoints alternativos
        "units",
        "reservations",
        "amenities",
        # Endpoints con trailing slash
        "pms/units/",
        "pms/reservations/",
        # Endpoints de prueba
        "health",
        "status",
        "ping",
        # Endpoints de documentación
        "docs",
        "swagger",
        "openapi",
    ]

    print(f"Base URL: {base_url}")
    print(f"Username: {username[:3]}***")
    print(f"Password: {'***' if password else 'None'}")

    successful_endpoints = []

    for endpoint in endpoints:
        if test_endpoint(base_url, endpoint, username, password):
            successful_endpoints.append(endpoint)

    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)

    if successful_endpoints:
        print(f"✅ Endpoints exitosos ({len(successful_endpoints)}):")
        for endpoint in successful_endpoints:
            print(f"   - {endpoint}")

        print(f"\n💡 RECOMENDACIÓN:")
        print(f"   Usar endpoint: {successful_endpoints[0]}")
    else:
        print("❌ Ningún endpoint funcionó")
        print("💡 Posibles problemas:")
        print("   - URL base incorrecta")
        print("   - Credenciales incorrectas")
        print("   - API no disponible")
        print("   - Endpoints no existen")


if __name__ == "__main__":
    main()
