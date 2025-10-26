#!/usr/bin/env python3
"""
Script de prueba rápida
Ejecuta un test rápido para verificar que la configuración básica funciona
"""

import json
import os
import sys

import httpx


def quick_test():
    """Ejecutar test rápido de la configuración"""
    print("🔍 PRUEBA RÁPIDA - TRACKHS API")
    print("=" * 60)
    print("Este script ejecuta un test rápido para verificar")
    print("que la configuración básica funciona correctamente")
    print("=" * 60)

    # Verificar credenciales
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")

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
        with httpx.Client(auth=(username, password), timeout=15.0) as client:
            print("🔄 Enviando petición...")
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
                print(response.text[:300])
                print("-" * 50)
                print("\n💡 DIAGNÓSTICO:")
                print("   - El problema se reproduce en local")
                print("   - La URL base o endpoint es incorrecto")
                print("   - Las credenciales podrían ser incorrectas")
                print("\n🔧 SOLUCIÓN:")
                print("   - Ejecutar: python scripts/run_final_diagnosis.py")
                print("   - Probar diferentes configuraciones")
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
                print("\n🚀 PRÓXIMOS PASOS:")
                print("   1. Configurar las mismas variables en FastMCP Cloud")
                print("   2. Desplegar el servidor")
                print("   3. Probar la herramienta search_units")

                return True

            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
                print("Preview de la respuesta:")
                print("-" * 50)
                print(response.text[:300])
                print("-" * 50)
                print("\n🔧 SOLUCIÓN:")
                print("   - Ejecutar: python scripts/run_final_diagnosis.py")
                return False

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error {e.response.status_code}")
        print("Respuesta:")
        print("-" * 50)
        print(e.response.text[:300])
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

        print("\n🔧 SOLUCIÓN:")
        print("   - Ejecutar: python scripts/run_final_diagnosis.py")
        return False

    except httpx.RequestError as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("\n💡 DIAGNÓSTICO: Problema de conectividad")
        print("   - Verificar conexión a internet")
        print("   - Verificar que la URL sea accesible")
        print("\n🔧 SOLUCIÓN:")
        print("   - Ejecutar: python scripts/run_final_diagnosis.py")
        return False

    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        print("\n🔧 SOLUCIÓN:")
        print("   - Ejecutar: python scripts/run_final_diagnosis.py")
        return False


def main():
    """Función principal"""
    success = quick_test()

    if success:
        print("\n🎉 ¡La configuración actual funciona correctamente!")
        print(
            "El problema en FastMCP Cloud podría ser de configuración de variables de entorno"
        )
        print("\n🚀 PRÓXIMOS PASOS:")
        print("   1. Configurar las mismas variables en FastMCP Cloud")
        print("   2. Desplegar el servidor")
        print("   3. Probar la herramienta search_units")
    else:
        print("\n❌ La configuración actual no funciona")
        print(
            "Necesitas encontrar la configuración correcta antes de desplegar en FastMCP Cloud"
        )
        print("\n🔧 SOLUCIÓN:")
        print("   - Ejecutar: python scripts/run_final_diagnosis.py")
        print("   - Probar diferentes configuraciones")
        print("   - Contactar soporte técnico de TrackHS si es necesario")


if __name__ == "__main__":
    main()
