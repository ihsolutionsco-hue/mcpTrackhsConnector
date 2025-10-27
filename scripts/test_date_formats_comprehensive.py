#!/usr/bin/env python3
"""
Script exhaustivo para probar diferentes formatos de fecha con la API TrackHS.
Prueba todos los formatos posibles según la documentación oficial.
"""

import json
import os
import sys
from datetime import datetime, timedelta

import requests

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_date_formats():
    """Probar diferentes formatos de fecha con la API TrackHS"""

    print("🧪 TESTING EXHAUSTIVO DE FORMATOS DE FECHA")
    print("=" * 60)

    # Configuración de la API
    base_url = "https://ihmvacations.trackhs.com"
    username = "aba99777416466b6bdc1a25223192ccb"
    password = "your_password_here"  # Reemplazar con password real

    # Headers de autenticación
    auth = (username, password)

    # Fecha base para las pruebas
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    print(f"📅 Fecha base para pruebas: {today.strftime('%Y-%m-%d')}")

    # Diferentes formatos de fecha a probar
    date_formats = {
        "YYYY-MM-DD": today.strftime("%Y-%m-%d"),
        "YYYY-MM-DDTHH:MM:SS": today.strftime("%Y-%m-%dT%H:%M:%S"),
        "YYYY-MM-DDTHH:MM:SSZ": today.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "YYYY-MM-DDTHH:MM:SS+00:00": today.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "YYYY-MM-DDTHH:MM:SS.000Z": today.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "YYYY-MM-DDTHH:MM:SS.000000Z": today.strftime("%Y-%m-%dT%H:%M:%S.000000Z"),
    }

    # Diferentes nombres de parámetros a probar
    param_names = [
        ("arrivalStart", "arrivalEnd"),  # Documentación oficial
        ("arrival_start", "arrival_end"),  # Nombres que estábamos usando
        ("arrivalDate", "departureDate"),  # Nombres alternativos
        ("checkin", "checkout"),  # Nombres simplificados
    ]

    results = {}

    for format_name, date_str in date_formats.items():
        print(f"\n🔍 PROBANDO FORMATO: {format_name}")
        print(f"   Fecha: {date_str}")

        results[format_name] = {}

        for start_param, end_param in param_names:
            print(f"\n   📋 Parámetros: {start_param}, {end_param}")

            # Construir URL con parámetros
            params = {"page": 1, "size": 5, start_param: date_str, end_param: date_str}

            url = f"{base_url}/api/pms/reservations"

            try:
                response = requests.get(url, params=params, auth=auth, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    total_items = data.get("total_items", 0)
                    reservations = data.get("_embedded", {}).get("reservations", [])

                    print(f"      ✅ Status: {response.status_code}")
                    print(f"      📊 Total items: {total_items}")
                    print(f"      📄 Reservas devueltas: {len(reservations)}")

                    # Mostrar fechas de llegada de las primeras reservas
                    if reservations:
                        print(f"      📅 Fechas de llegada (primeras 3):")
                        for i, res in enumerate(reservations[:3]):
                            arrival_date = res.get("arrivalDate", "N/A")
                            print(f"         {i+1}. {arrival_date}")

                    # Verificar si el filtro funcionó
                    filtered_count = 0
                    for res in reservations:
                        res_date = res.get("arrivalDate", "")
                        if res_date == today.strftime("%Y-%m-%d"):
                            filtered_count += 1

                    print(f"      🎯 Reservas con fecha de hoy: {filtered_count}")

                    results[format_name][f"{start_param}_{end_param}"] = {
                        "status": response.status_code,
                        "total_items": total_items,
                        "returned_count": len(reservations),
                        "filtered_count": filtered_count,
                        "success": filtered_count > 0 or total_items == 0,
                    }

                else:
                    print(f"      ❌ Status: {response.status_code}")
                    print(f"      📝 Error: {response.text[:200]}")

                    results[format_name][f"{start_param}_{end_param}"] = {
                        "status": response.status_code,
                        "error": response.text[:200],
                        "success": False,
                    }

            except Exception as e:
                print(f"      💥 Excepción: {str(e)}")
                results[format_name][f"{start_param}_{end_param}"] = {
                    "error": str(e),
                    "success": False,
                }

    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)

    successful_combinations = []

    for format_name, format_results in results.items():
        print(f"\n🔍 FORMATO: {format_name}")
        for param_combo, result in format_results.items():
            if result.get("success", False):
                print(
                    f"   ✅ {param_combo}: {result.get('filtered_count', 0)} reservas filtradas"
                )
                successful_combinations.append((format_name, param_combo))
            else:
                print(f"   ❌ {param_combo}: {result.get('error', 'Fallo')}")

    print(f"\n🎯 COMBINACIONES EXITOSAS: {len(successful_combinations)}")
    for format_name, param_combo in successful_combinations:
        print(f"   ✅ {format_name} + {param_combo}")

    # Guardar resultados en archivo
    with open("date_format_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Resultados guardados en: date_format_test_results.json")

    return len(successful_combinations) > 0


if __name__ == "__main__":
    success = test_date_formats()
    print(
        f"\n{'✅ ÉXITO' if success else '❌ FALLO'}: {'Se encontraron combinaciones exitosas' if success else 'No se encontraron combinaciones exitosas'}"
    )
    sys.exit(0 if success else 1)
