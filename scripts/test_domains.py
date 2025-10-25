#!/usr/bin/env python3
"""
Script para probar diferentes dominios de TrackHS
Basado en la documentación oficial que muestra {customerDomain}/api
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
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")

# Dominios posibles basados en la documentación
POSSIBLE_DOMAINS = [
    "https://api.trackhs.com",
    "https://api.trackhs.com/api",
    "https://app.trackhs.com/api",
    "https://trackhs.com/api",
    "https://api.trackhs.io",
    "https://api.trackhs.io/api",
    "https://app.trackhs.io/api",
    "https://trackhs.io/api",
    # Dominios de ejemplo de la documentación
    "https://api-integration-example.tracksandbox.io",
    "https://api-integration-example.tracksandbox.io/api",
    # Dominios genéricos
    "https://api.trackhs.net",
    "https://api.trackhs.net/api",
    "https://app.trackhs.net/api",
]


def test_domain(domain):
    """Probar un dominio específico"""
    print(f"\n🌐 Probando dominio: {domain}")

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=10.0) as client:
            # Probar endpoint raíz
            response = client.get(domain)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                print(f"   ✅ Endpoint raíz accesible")
                return True
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint raíz no encontrado, probando /api...")
                # Probar con /api
                api_url = f"{domain}/api" if not domain.endswith("/api") else domain
                response = client.get(api_url)
                print(f"   Status: {response.status_code}")

                if response.status_code == 200:
                    print(f"   ✅ Endpoint /api accesible")
                    return True
                else:
                    print(f"   ❌ Endpoint /api no accesible")
                    return False
            else:
                print(f"   ❌ Error {response.status_code}")
                return False

    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False


def test_units_endpoint(domain):
    """Probar endpoint de unidades en un dominio"""
    print(f"\n🏠 Probando endpoint de unidades en: {domain}")

    # Asegurar que el dominio termine en /api
    if not domain.endswith("/api"):
        domain = f"{domain}/api"

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=10.0) as client:
            # Probar endpoint de unidades
            response = client.get(f"{domain}/pms/units?page=1&size=1")
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Endpoint de unidades accesible")
                print(f"   📊 Total items: {data.get('total_items', 'N/A')}")
                return True
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}...")
                return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_alternative_endpoints(domain):
    """Probar endpoints alternativos"""
    print(f"\n🔄 Probando endpoints alternativos en: {domain}")

    # Asegurar que el dominio termine en /api
    if not domain.endswith("/api"):
        domain = f"{domain}/api"

    endpoints = [
        "/pms/units/amenities",
        "/pms/reservations",
        "/health",
        "/status",
        "/",
    ]

    for endpoint in endpoints:
        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=10.0
            ) as client:
                response = client.get(f"{domain}{endpoint}")
                print(f"   {endpoint}: {response.status_code}")

                if response.status_code == 200:
                    print(f"   ✅ {endpoint} accesible")
                    return True

        except Exception as e:
            print(f"   ❌ {endpoint} error: {e}")

    return False


def main():
    """Función principal"""
    print("🔍 Probando dominios de TrackHS")
    print("=" * 60)

    # Verificar credenciales
    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas en .env")
        return 1

    print(f"Username: {API_USERNAME}")
    print(f"Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    working_domains = []

    # Probar cada dominio
    for domain in POSSIBLE_DOMAINS:
        if test_domain(domain):
            working_domains.append(domain)

    if working_domains:
        print(f"\n✅ Dominios accesibles: {len(working_domains)}")
        for domain in working_domains:
            print(f"   • {domain}")

        # Probar endpoints en dominios accesibles
        for domain in working_domains[:3]:  # Probar solo los primeros 3
            if test_units_endpoint(domain):
                print(f"\n🎉 ¡Éxito! Dominio funcional encontrado: {domain}")
                print(f"   Puedes usar este dominio en tu archivo .env:")
                print(f"   TRACKHS_BASE_URL={domain}")
                return 0

            test_alternative_endpoints(domain)
    else:
        print("\n❌ No se encontraron dominios accesibles")
        print("   Posibles causas:")
        print("   • Credenciales incorrectas")
        print("   • Dominio específico del cliente no incluido")
        print("   • Problemas de conectividad")
        print("   • API no disponible")

    return 1


if __name__ == "__main__":
    sys.exit(main())
