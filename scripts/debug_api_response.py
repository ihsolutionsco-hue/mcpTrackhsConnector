#!/usr/bin/env python3
"""
Script de depuración para analizar respuestas detalladas de la API
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


def debug_api_call(endpoint, params=None):
    """Hacer una llamada a la API con información detallada de depuración"""
    print(f"\n🔍 Llamada a: {endpoint}")
    if params:
        print(f"   Parámetros: {params}")

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}{endpoint}", params=params)

            print(f"   Status Code: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            print(f"   URL: {response.url}")

            # Mostrar contenido de la respuesta
            content = response.text
            print(f"   Content Length: {len(content)}")
            print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ JSON válido - Claves: {list(data.keys())}")
                    return data
                except json.JSONDecodeError:
                    print(f"   ⚠️  Respuesta no es JSON válido")
                    print(f"   Content: {content[:500]}...")
                    return None
            else:
                print(f"   ❌ Error {response.status_code}")
                print(f"   Content: {content[:1000]}...")
                return None

    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return None


def test_basic_endpoints():
    """Probar endpoints básicos"""
    print("🧪 Probando endpoints básicos")
    print("=" * 50)

    endpoints = [
        ("/", "Endpoint raíz"),
        ("/pms/units", "Unidades sin parámetros"),
        ("/pms/units?page=1&size=1", "Unidades con paginación mínima"),
        ("/pms/units/amenities", "Amenidades"),
        ("/pms/reservations", "Reservas"),
    ]

    for endpoint, description in endpoints:
        print(f"\n📋 {description}")
        debug_api_call(endpoint)


def test_authentication_methods():
    """Probar diferentes métodos de autenticación"""
    print("\n🔐 Probando métodos de autenticación")
    print("=" * 50)

    # Método 1: Basic Auth (actual)
    print("\n🔑 Método 1: Basic Auth")
    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=10.0) as client:
            response = client.get(f"{API_BASE_URL}/pms/units?page=1&size=1")
            print(f"   Status: {response.status_code}")
            print(f"   Content: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Método 2: Headers de autorización
    print("\n🔑 Método 2: Headers de autorización")
    try:
        with httpx.Client(timeout=10.0) as client:
            headers = {
                "Authorization": f"Bearer {API_PASSWORD}",
                "X-API-Key": API_PASSWORD,
                "X-API-Username": API_USERNAME,
                "X-API-Password": API_PASSWORD,
            }
            response = client.get(
                f"{API_BASE_URL}/pms/units?page=1&size=1", headers=headers
            )
            print(f"   Status: {response.status_code}")
            print(f"   Content: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Método 3: Query parameters
    print("\n🔑 Método 3: Query parameters")
    try:
        with httpx.Client(timeout=10.0) as client:
            params = {
                "page": 1,
                "size": 1,
                "username": API_USERNAME,
                "password": API_PASSWORD,
                "api_key": API_PASSWORD,
            }
            response = client.get(f"{API_BASE_URL}/pms/units", params=params)
            print(f"   Status: {response.status_code}")
            print(f"   Content: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")


def test_different_parameters():
    """Probar diferentes combinaciones de parámetros"""
    print("\n📊 Probando diferentes parámetros")
    print("=" * 50)

    test_cases = [
        ({"page": 1, "size": 1}, "Paginación mínima"),
        ({"page": 0, "size": 1}, "Página 0 (inválida)"),
        ({"page": 1, "size": 0}, "Tamaño 0 (inválido)"),
        ({"page": 1, "size": 1, "is_active": 1}, "Con filtro is_active"),
        ({"page": 1, "size": 1, "is_bookable": 1}, "Con filtro is_bookable"),
        ({"page": 1, "size": 1, "bedrooms": 1}, "Con filtro bedrooms"),
        ({"page": 1, "size": 1, "search": "test"}, "Con búsqueda"),
    ]

    for params, description in test_cases:
        print(f"\n📋 {description}")
        debug_api_call("/pms/units", params)


def test_alternative_endpoints():
    """Probar endpoints alternativos"""
    print("\n🔄 Probando endpoints alternativos")
    print("=" * 50)

    endpoints = [
        "/pms/units/amenities?page=1&size=1",
        "/pms/reservations?page=1&size=1",
        "/pms/units/types",
        "/pms/nodes",
        "/pms/units/1",  # Unidad específica
        "/pms/reservations/1",  # Reserva específica
        "/health",
        "/status",
        "/api/health",
        "/api/status",
    ]

    for endpoint in endpoints:
        print(f"\n📋 {endpoint}")
        debug_api_call(endpoint)


def main():
    """Función principal"""
    print("🔧 Depuración detallada de API TrackHS")
    print("=" * 60)

    # Verificar credenciales
    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas en .env")
        return 1

    print(f"Base URL: {API_BASE_URL}")
    print(f"Username: {API_USERNAME}")
    print(f"Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    # Ejecutar pruebas
    test_basic_endpoints()
    test_authentication_methods()
    test_different_parameters()
    test_alternative_endpoints()

    print("\n" + "=" * 60)
    print("🏁 Depuración completada")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
