#!/usr/bin/env python3
"""
Script simple para probar la configuración actual en local
Prueba la API real de TrackHS con la configuración actual
"""

import json
import os
import sys

import httpx


def test_current_config_local():
    """Probar la configuración actual en local"""
    print("🔍 Probando configuración actual en local con API real")
    print("=" * 60)

    # Obtener configuración actual
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    print(f"Base URL: {base_url}")
    print(f"Username: {username[:3]}***" if username else "None")
    print(f"Password: {'***' if password else 'None'}")

    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("\n💡 Configure las variables de entorno:")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")
        return False

    # Probar endpoint de unidades
    endpoint = "pms/units"
    full_url = f"{base_url}/{endpoint}"
    print(f"\nURL completa: {full_url}")

    try:
        with httpx.Client(auth=(username, password), timeout=30.0) as client:
            print("🔄 Enviando petición a la API real...")
            response = client.get(full_url, params={"page": 1, "size": 1})

            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"Content-Length: {len(response.text)}")

            # Verificar si es HTML (el problema reportado)
            if "text/html" in response.headers.get("content-type", ""):
                print(
                    "❌ Respuesta HTML recibida - mismo problema que en FastMCP Cloud"
                )
                print("Preview de respuesta:")
                print("-" * 50)
                print(response.text[:500])
                print("-" * 50)
                print("\n💡 DIAGNÓSTICO:")
                print("   - El problema se reproduce en local")
                print("   - La URL base o endpoint es incorrecto")
                print("   - Las credenciales podrían ser incorrectas")
                return False

            # Intentar parsear JSON
            try:
                data = response.json()
                print("✅ Respuesta JSON válida recibida")
                print(f"Claves en la respuesta: {list(data.keys())}")

                if "total_items" in data:
                    print(f"Total de elementos: {data['total_items']}")

                if "_embedded" in data and "units" in data["_embedded"]:
                    units = data["_embedded"]["units"]
                    print(f"Unidades en esta página: {len(units)}")
                    if units:
                        unit = units[0]
                        print(
                            f"Primera unidad: {unit.get('name', 'N/A')} (ID: {unit.get('id', 'N/A')})"
                        )

                print("\n🎉 ¡CONFIGURACIÓN ACTUAL FUNCIONA!")
                print("   - La API responde correctamente")
                print("   - Las credenciales son válidas")
                print("   - La URL base y endpoint son correctos")
                print("\n💡 Esto significa que el problema en FastMCP Cloud")
                print("   podría ser de configuración de variables de entorno")

                return True

            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
                print("Preview de la respuesta:")
                print("-" * 50)
                print(response.text[:500])
                print("-" * 50)
                return False

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error {e.response.status_code}")
        print("Respuesta:")
        print("-" * 50)
        print(e.response.text[:500])
        print("-" * 50)

        if e.response.status_code == 401:
            print("\n💡 DIAGNÓSTICO: Credenciales inválidas")
            print("   - Verificar TRACKHS_USERNAME")
            print("   - Verificar TRACKHS_PASSWORD")
        elif e.response.status_code == 403:
            print("\n💡 DIAGNÓSTICO: Acceso denegado")
            print("   - Las credenciales son correctas pero no tienen permisos")
        elif e.response.status_code == 404:
            print("\n💡 DIAGNÓSTICO: Endpoint no encontrado")
            print("   - La URL base podría ser incorrecta")
            print("   - El endpoint podría no existir")

        return False

    except httpx.RequestError as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("\n💡 DIAGNÓSTICO: Problema de conectividad")
        print("   - Verificar conexión a internet")
        print("   - Verificar que la URL sea accesible")
        return False

    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False


def suggest_next_steps(success: bool):
    """Sugerir próximos pasos basados en el resultado"""
    print("\n" + "=" * 60)
    print("💡 PRÓXIMOS PASOS")
    print("=" * 60)

    if success:
        print("✅ La configuración actual funciona en local")
        print("\n🔧 Para FastMCP Cloud:")
        print("   1. Verificar que las variables de entorno estén configuradas:")
        print("      - TRACKHS_USERNAME")
        print("      - TRACKHS_PASSWORD")
        print("      - TRACKHS_API_URL (opcional)")
        print("   2. Reiniciar el servidor en FastMCP Cloud")
        print("   3. Probar la herramienta search_units")

        print("\n🔍 Si el problema persiste en FastMCP Cloud:")
        print("   - Ejecutar: python scripts/test_specific_issue.py")
        print("   - Ejecutar: python scripts/complete_diagnosis.py")

    else:
        print("❌ La configuración actual no funciona en local")
        print("\n🔧 Acciones recomendadas:")
        print("   1. Verificar credenciales con TrackHS")
        print("   2. Probar diferentes URLs:")
        print("      - python scripts/test_local_api_real.py")
        print("   3. Contactar soporte técnico de TrackHS")

        print("\n🔍 Scripts de diagnóstico disponibles:")
        print("   - python scripts/test_local_api_real.py")
        print("   - python scripts/complete_diagnosis.py")


def main():
    """Función principal"""
    print("🚀 PRUEBA LOCAL - CONFIGURACIÓN ACTUAL")
    print("=" * 80)
    print("Este script prueba la configuración actual con la API real de TrackHS")
    print("para verificar si las URLs y credenciales funcionan correctamente")
    print("=" * 80)

    success = test_current_config_local()
    suggest_next_steps(success)

    if success:
        print("\n🎉 ¡La configuración actual funciona correctamente!")
        print(
            "El problema en FastMCP Cloud podría ser de configuración de variables de entorno"
        )
    else:
        print("\n❌ La configuración actual no funciona")
        print(
            "Necesitas encontrar la configuración correcta antes de desplegar en FastMCP Cloud"
        )


if __name__ == "__main__":
    main()
