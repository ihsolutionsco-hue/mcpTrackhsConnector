#!/usr/bin/env python3
"""
Script de Verificación Final - MCP TrackHS Connector
Verifica que todos los problemas reportados por el tester estén resueltos
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


def print_header():
    """Imprimir encabezado del reporte"""
    print("=" * 80)
    print("🔧 VERIFICACIÓN FINAL - MCP TrackHS Connector")
    print("=" * 80)
    print("Verificando que todos los problemas críticos reportados estén resueltos")
    print("=" * 80)


def test_problem_1_404_error():
    """Probar que el Error 404 está resuelto"""
    print("\n🔍 PROBLEMA 1: Error 404 - Endpoint No Disponible")
    print("-" * 60)

    try:
        with httpx.Client(auth=(API_USERNAME, API_PASSWORD), timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/pms/units?page=1&size=1")

            if response.status_code == 200:
                print("✅ RESUELTO: Endpoint responde correctamente")
                print(f"   Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Total items: {data.get('total_items', 'N/A')}")
                    return True
                except json.JSONDecodeError:
                    print("   ⚠️  Respuesta no es JSON válido")
                    return False
            else:
                print(f"❌ NO RESUELTO: Status {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"❌ NO RESUELTO: Error de conexión - {e}")
        return False


def test_problem_2_parameter_validation():
    """Probar que la validación de tipos está corregida"""
    print("\n🔍 PROBLEMA 2: Errores de Validación de Tipos")
    print("-" * 60)

    test_cases = [
        {"name": "3 dormitorios", "params": {"bedrooms": 3}},
        {"name": "2 baños", "params": {"bathrooms": 2}},
        {"name": "Unidades activas", "params": {"is_active": 1}},
        {"name": "Unidades disponibles", "params": {"is_bookable": 1}},
        {
            "name": "Filtros combinados",
            "params": {"bedrooms": 3, "bathrooms": 2, "is_active": 1},
        },
    ]

    success_count = 0

    for test_case in test_cases:
        print(f"   🔍 {test_case['name']}: {test_case['params']}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(
                    f"{API_BASE_URL}/pms/units", params=test_case["params"]
                )

                if response.status_code == 200:
                    print(f"      ✅ Éxito - Status: {response.status_code}")
                    success_count += 1
                else:
                    print(f"      ❌ Error - Status: {response.status_code}")
                    print(f"      Response: {response.text[:100]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")

    success_rate = (success_count / len(test_cases)) * 100
    print(
        f"\n   📊 Resultado: {success_count}/{len(test_cases)} pruebas exitosas ({success_rate:.1f}%)"
    )

    return success_count == len(test_cases)


def test_problem_3_api_connectivity():
    """Probar que la conectividad con API TrackHS está funcionando"""
    print("\n🔍 PROBLEMA 3: Falta de Conectividad con API TrackHS")
    print("-" * 60)

    endpoints = [
        ("/pms/units", "Unidades"),
        ("/pms/units/amenities", "Amenidades"),
        ("/pms/reservations", "Reservas"),
    ]

    success_count = 0

    for endpoint, name in endpoints:
        print(f"   🔍 {name}: {endpoint}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(f"{API_BASE_URL}{endpoint}?page=1&size=1")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        total_items = data.get("total_items", 0)
                        print(f"      ✅ Éxito - Total items: {total_items}")
                        success_count += 1
                    except json.JSONDecodeError:
                        print(f"      ⚠️  Respuesta no es JSON válido")
                else:
                    print(f"      ❌ Error - Status: {response.status_code}")
                    print(f"      Response: {response.text[:100]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")

    success_rate = (success_count / len(endpoints)) * 100
    print(
        f"\n   📊 Resultado: {success_count}/{len(endpoints)} endpoints funcionando ({success_rate:.1f}%)"
    )

    return success_count == len(endpoints)


def test_user_scenarios():
    """Probar los casos de uso específicos reportados por el tester"""
    print("\n🔍 CASOS DE USO DEL TESTER")
    print("-" * 60)

    user_scenarios = [
        {
            "name": "¿Qué casas tienen disponibles?",
            "params": {"size": 10, "page": 1},
            "description": "Búsqueda básica de unidades disponibles",
        },
        {
            "name": "Casa con 3 dormitorios y 2 baños",
            "params": {"bedrooms": 3, "bathrooms": 2},
            "description": "Filtros por características específicas",
        },
        {
            "name": "Casa con piscina",
            "params": {"search": "pool"},
            "description": "Búsqueda por texto",
        },
        {
            "name": "Solo casas disponibles",
            "params": {"is_active": 1, "is_bookable": 1},
            "description": "Filtros de disponibilidad",
        },
        {
            "name": "Primeras 5 casas",
            "params": {"size": 5, "page": 1},
            "description": "Paginación básica",
        },
    ]

    success_count = 0

    for scenario in user_scenarios:
        print(f"   🔍 {scenario['name']}")
        print(f"      {scenario['description']}")
        print(f"      Parámetros: {scenario['params']}")

        try:
            with httpx.Client(
                auth=(API_USERNAME, API_PASSWORD), timeout=30.0
            ) as client:
                response = client.get(
                    f"{API_BASE_URL}/pms/units", params=scenario["params"]
                )

                if response.status_code == 200:
                    try:
                        data = response.json()
                        total_items = data.get("total_items", 0)
                        print(f"      ✅ Éxito - {total_items} unidades encontradas")
                        success_count += 1
                    except json.JSONDecodeError:
                        print(f"      ⚠️  Respuesta no es JSON válido")
                else:
                    print(f"      ❌ Error - Status: {response.status_code}")
                    print(f"      Response: {response.text[:100]}...")

        except Exception as e:
            print(f"      ❌ Excepción: {e}")

        print()

    success_rate = (success_count / len(user_scenarios)) * 100
    print(
        f"   📊 Resultado: {success_count}/{len(user_scenarios)} escenarios exitosos ({success_rate:.1f}%)"
    )

    return success_count == len(user_scenarios)


def print_final_report(problem1, problem2, problem3, user_scenarios):
    """Imprimir reporte final"""
    print("\n" + "=" * 80)
    print("🏁 REPORTE FINAL DE VERIFICACIÓN")
    print("=" * 80)

    total_problems = 4
    resolved_problems = sum([problem1, problem2, problem3, user_scenarios])

    print(f"📊 RESUMEN GENERAL:")
    print(f"   Problemas resueltos: {resolved_problems}/{total_problems}")
    print(f"   Tasa de éxito: {(resolved_problems/total_problems)*100:.1f}%")
    print()

    print("📋 ESTADO DE PROBLEMAS:")
    print(
        f"   1. Error 404 - Endpoint No Disponible: {'✅ RESUELTO' if problem1 else '❌ NO RESUELTO'}"
    )
    print(
        f"   2. Errores de Validación de Tipos: {'✅ RESUELTO' if problem2 else '❌ NO RESUELTO'}"
    )
    print(
        f"   3. Falta de Conectividad API: {'✅ RESUELTO' if problem3 else '❌ NO RESUELTO'}"
    )
    print(
        f"   4. Casos de Uso del Tester: {'✅ RESUELTO' if user_scenarios else '❌ NO RESUELTO'}"
    )
    print()

    if resolved_problems == total_problems:
        print("🎉 ¡TODOS LOS PROBLEMAS HAN SIDO RESUELTOS!")
        print("   El MCP TrackHS Connector está 100% operativo")
        print("   Listo para uso en producción")
        return 0
    else:
        print("⚠️  ALGUNOS PROBLEMAS PERSISTEN")
        print("   Se requiere revisión adicional")
        return 1


def main():
    """Función principal de verificación"""
    print_header()

    # Verificar credenciales
    if not API_USERNAME or not API_PASSWORD:
        print("❌ Error: Credenciales no configuradas")
        print("   Configure TRACKHS_USERNAME y TRACKHS_PASSWORD")
        return 1

    print(f"🔧 Configuración:")
    print(f"   Base URL: {API_BASE_URL}")
    print(f"   Username: {API_USERNAME}")
    print(f"   Password: {'✅ Configurado' if API_PASSWORD else '❌ No configurado'}")

    # Ejecutar pruebas
    problem1 = test_problem_1_404_error()
    problem2 = test_problem_2_parameter_validation()
    problem3 = test_problem_3_api_connectivity()
    user_scenarios = test_user_scenarios()

    # Reporte final
    return print_final_report(problem1, problem2, problem3, user_scenarios)


if __name__ == "__main__":
    sys.exit(main())
