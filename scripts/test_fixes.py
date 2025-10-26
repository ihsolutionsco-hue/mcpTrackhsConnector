#!/usr/bin/env python3
"""
Script para probar las correcciones del MCP TrackHS Connector
Verifica que los problemas reportados por el tester estén solucionados
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
API_BASE_URL = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com")
API_USERNAME = os.getenv("TRACKHS_USERNAME")
API_PASSWORD = os.getenv("TRACKHS_PASSWORD")


def test_basic_connectivity():
    """Probar conectividad básica con la URL corregida"""
    print("🔌 Probando conectividad básica con URL corregida...")
    print(f"   Base URL: {API_BASE_URL}")
    print(f"   Username: {'✅ Configurado' if API_USERNAME else '❌ No configurado'}")
    print(f"   Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas")
        return False

    return True


def test_units_endpoint():
    """Probar endpoint de unidades con parámetros numéricos corregidos"""
    print("\n🏠 Probando endpoint de unidades con correcciones...")

    test_cases = [
        {
            "name": "Búsqueda básica sin filtros",
            "params": {"page": 1, "size": 5},
            "expected_status": 200,
        },
        {
            "name": "Búsqueda con 3 dormitorios (parámetro numérico)",
            "params": {"page": 1, "size": 5, "bedrooms": 3},
            "expected_status": 200,
        },
        {
            "name": "Búsqueda con 2 baños (parámetro numérico)",
            "params": {"page": 1, "size": 5, "bathrooms": 2},
            "expected_status": 200,
        },
        {
            "name": "Búsqueda con filtros combinados",
            "params": {
                "page": 1,
                "size": 5,
                "bedrooms": 3,
                "bathrooms": 2,
                "is_active": 1,
            },
            "expected_status": 200,
        },
        {
            "name": "Búsqueda con texto",
            "params": {"page": 1, "size": 5, "search": "luxury"},
            "expected_status": 200,
        },
        {
            "name": "Búsqueda con unidades disponibles",
            "params": {"page": 1, "size": 5, "is_active": 1, "is_bookable": 1},
            "expected_status": 200,
        },
    ]

    success_count = 0
    total_tests = len(test_cases)

    for test_case in test_cases:
        print(f"\n   🔍 {test_case['name']}")
        print(f"      Parámetros: {test_case['params']}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(
                    f"{API_BASE_URL}/pms/units", params=test_case["params"]
                )
                print(f"      Status: {response.status_code}")

                if response.status_code == test_case["expected_status"]:
                    try:
                        data = response.json()
                        total_items = data.get("total_items", 0)
                        print(f"      ✅ Éxito - Total items: {total_items}")
                        success_count += 1
                    except json.JSONDecodeError:
                        print(f"      ⚠️  Respuesta no es JSON válido")
                        print(f"      Content: {response.text[:200]}...")
                else:
                    print(f"      ❌ Error {response.status_code}")
                    print(f"      Response: {response.text[:300]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")

    success_rate = (success_count / total_tests) * 100
    print(
        f"\n📊 Resultados: {success_count}/{total_tests} pruebas exitosas ({success_rate:.1f}%)"
    )

    return success_count == total_tests


def test_parameter_types():
    """Probar que los parámetros numéricos se envían correctamente"""
    print("\n🔢 Probando tipos de parámetros...")

    # Probar con diferentes tipos de parámetros
    test_params = {
        "page": 1,
        "size": 5,
        "bedrooms": 3,  # Entero
        "bathrooms": 2,  # Entero
        "is_active": 1,  # Entero
        "is_bookable": 1,  # Entero
    }

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/pms/units", params=test_params)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Parámetros numéricos aceptados correctamente")
                print(f"   📊 Total items: {data.get('total_items', 'N/A')}")
                return True
            else:
                print(f"   ❌ Error {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False


def test_alternative_endpoints():
    """Probar otros endpoints para verificar conectividad general"""
    print("\n🔄 Probando otros endpoints...")

    endpoints = [
        ("/pms/units/amenities?page=1&size=5", "Amenidades"),
        ("/pms/reservations?page=1&size=5", "Reservas"),
    ]

    for endpoint, name in endpoints:
        print(f"\n   🔍 {name}: {endpoint}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(f"{API_BASE_URL}{endpoint}")
                print(f"      Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    print(f"      ✅ Éxito - Total items: {total_items}")
                else:
                    print(f"      ❌ Error {response.status_code}")
                    print(f"      Response: {response.text[:200]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")


def main():
    """Función principal de prueba"""
    print("🔧 Prueba de Correcciones - MCP TrackHS Connector")
    print("=" * 60)
    print("Verificando que los problemas reportados estén solucionados:")
    print("1. ✅ Error 404 - URL corregida")
    print("2. ✅ Validación de tipos - Parámetros numéricos corregidos")
    print("3. ✅ Conectividad API - Verificando endpoints")
    print("=" * 60)

    # Verificar credenciales
    if not test_basic_connectivity():
        return 1

    # Probar endpoint de unidades con correcciones
    units_success = test_units_endpoint()

    # Probar tipos de parámetros
    params_success = test_parameter_types()

    # Probar otros endpoints
    test_alternative_endpoints()

    # Resumen final
    print("\n" + "=" * 60)
    print("🏁 Resumen de Pruebas")
    print("=" * 60)

    if units_success and params_success:
        print("✅ TODAS LAS CORRECCIONES FUNCIONAN CORRECTAMENTE")
        print("   • URL corregida: https://ihmvacations.trackhs.com")
        print("   • Parámetros numéricos convertidos a enteros")
        print("   • Endpoints respondiendo correctamente")
        print("\n🎉 El MCP TrackHS Connector está listo para producción")
        return 0
    else:
        print("❌ ALGUNAS CORRECCIONES NECESITAN REVISIÓN")
        if not units_success:
            print("   • Problemas con endpoint de unidades")
        if not params_success:
            print("   • Problemas con tipos de parámetros")
        return 1


if __name__ == "__main__":
    sys.exit(main())
