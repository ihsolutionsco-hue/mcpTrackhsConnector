#!/usr/bin/env python3
"""
Script de diagnóstico para la API de TrackHS
Verifica conectividad, autenticación y endpoints
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
API_BASE_URL = os.getenv("TRACKHS_BASE_URL", "https://api.trackhs.com/api")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


def test_basic_connectivity():
    """Probar conectividad básica"""
    print("🔌 Probando conectividad básica...")
    print(f"   Base URL: {API_BASE_URL}")
    print(f"   Username: {'✅ Configurado' if API_USERNAME else '❌ No configurado'}")
    print(f"   Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas")
        return False

    return True


def test_root_endpoint():
    """Probar endpoint raíz"""
    print("\n🌐 Probando endpoint raíz...")

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            # Probar endpoint raíz
            response = client.get(API_BASE_URL)
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")

            if response.status_code == 200:
                print("✅ Endpoint raíz accesible")
                return True
            else:
                print(f"❌ Endpoint raíz retornó {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"❌ Error conectando al endpoint raíz: {e}")
        return False


def test_units_endpoint():
    """Probar endpoint de unidades con diferentes parámetros"""
    print("\n🏠 Probando endpoint de unidades...")

    endpoints_to_test = [
        ("/pms/units", "Sin parámetros"),
        ("/pms/units?page=1&size=1", "Con paginación mínima"),
        ("/pms/units?page=1&size=5", "Con paginación pequeña"),
    ]

    for endpoint, description in endpoints_to_test:
        print(f"\n   🔍 {description}: {endpoint}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(f"{API_BASE_URL}{endpoint}")
                print(f"      Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    print(
                        f"      ✅ Éxito - Total items: {data.get('total_items', 'N/A')}"
                    )
                    return True
                else:
                    print(f"      ❌ Error {response.status_code}")
                    print(f"      Response: {response.text[:300]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")

    return False


def test_alternative_endpoints():
    """Probar endpoints alternativos"""
    print("\n🔄 Probando endpoints alternativos...")

    alternative_endpoints = [
        "/pms/units/amenities",
        "/pms/reservations",
        "/health",
        "/status",
        "/",
    ]

    for endpoint in alternative_endpoints:
        print(f"\n   🔍 Probando: {endpoint}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(f"{API_BASE_URL}{endpoint}")
                print(f"      Status: {response.status_code}")

                if response.status_code == 200:
                    print(f"      ✅ Endpoint accesible")
                    try:
                        data = response.json()
                        print(f"      📊 Datos: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        print(f"      📄 Texto: {response.text[:200]}...")
                else:
                    print(
                        f"      ❌ Error {response.status_code}: {response.text[:100]}..."
                    )

        except Exception as e:
            print(f"      ❌ Excepción: {e}")


def test_authentication():
    """Probar diferentes métodos de autenticación"""
    print("\n🔐 Probando métodos de autenticación...")

    auth_methods = [
        ("Basic Auth", (API_USERNAME, API_PASSWORD)),
        ("Headers", {"Authorization": f"Bearer {API_PASSWORD}"}),
        ("API Key", {"X-API-Key": API_PASSWORD}),
    ]

    for method_name, auth in auth_methods:
        print(f"\n   🔑 {method_name}")

        try:
            if isinstance(auth, tuple):
                # Basic Auth
                with httpx.Client(auth=auth, timeout=30.0) as client:
                    response = client.get(f"{API_BASE_URL}/pms/units?page=1&size=1")
            else:
                # Headers
                with httpx.Client(timeout=30.0) as client:
                    response = client.get(
                        f"{API_BASE_URL}/pms/units?page=1&size=1", headers=auth
                    )

            print(f"      Status: {response.status_code}")

            if response.status_code == 200:
                print(f"      ✅ {method_name} funciona")
                return True
            else:
                print(f"      ❌ {method_name} falló: {response.text[:100]}...")

        except Exception as e:
            print(f"      ❌ {method_name} excepción: {e}")

    return False


def test_network_connectivity():
    """Probar conectividad de red"""
    print("\n🌐 Probando conectividad de red...")

    import socket

    # Extraer hostname de la URL
    from urllib.parse import urlparse

    parsed_url = urlparse(API_BASE_URL)
    hostname = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)

    print(f"   Hostname: {hostname}")
    print(f"   Port: {port}")

    try:
        # Test de conectividad TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        sock.close()

        if result == 0:
            print("   ✅ Conectividad TCP exitosa")
        else:
            print(f"   ❌ Conectividad TCP falló: {result}")
            return False

    except Exception as e:
        print(f"   ❌ Error de conectividad: {e}")
        return False

    return True


def main():
    """Función principal de diagnóstico"""
    print("🔧 Diagnóstico de API TrackHS")
    print("=" * 60)

    # Verificar credenciales
    if not test_basic_connectivity():
        return 1

    # Probar conectividad de red
    if not test_network_connectivity():
        print("\n❌ Problemas de conectividad de red")
        return 1

    # Probar endpoint raíz
    test_root_endpoint()

    # Probar endpoint de unidades
    test_units_endpoint()

    # Probar endpoints alternativos
    test_alternative_endpoints()

    # Probar autenticación
    test_authentication()

    print("\n" + "=" * 60)
    print("🏁 Diagnóstico completado")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
