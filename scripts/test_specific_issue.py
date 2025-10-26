#!/usr/bin/env python3
"""
Script específico para diagnosticar el problema de FastMCP Cloud
Basado en el error: "Recurso no encontrado: <!DOCTYPE html>..."
"""

import json
import os
import sys

import httpx


def test_specific_issue():
    """Probar específicamente el problema reportado"""
    print("🔍 Diagnóstico específico del problema de FastMCP Cloud")
    print("=" * 60)
    print("Error reportado: 'Recurso no encontrado: <!DOCTYPE html>...'")
    print("=" * 60)

    # Obtener configuración
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")

    print(f"Base URL: {base_url}")
    print(f"Username: {username[:3]}***" if username else "None")
    print(f"Password: {'***' if password else 'None'}")

    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("💡 Configure TRACKHS_USERNAME y TRACKHS_PASSWORD en FastMCP Cloud")
        return False

    # Probar el endpoint específico que está fallando
    endpoint = "pms/units"
    full_url = f"{base_url}/{endpoint}"

    print(f"\n🎯 Probando endpoint específico: {full_url}")
    print("Este es el endpoint que está causando el error en FastMCP Cloud")

    try:
        with httpx.Client(auth=(username, password), timeout=15.0) as client:
            # Probar con parámetros mínimos
            params = {"page": 1, "size": 1}
            print(f"Parámetros: {params}")

            response = client.get(full_url, params=params)

            print(f"\n📊 RESULTADO:")
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"Content-Length: {len(response.text)}")
            print(f"Response Headers: {dict(response.headers)}")

            # Verificar si es HTML (el problema reportado)
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                print("\n❌ PROBLEMA CONFIRMADO: Respuesta HTML recibida")
                print("Esto confirma el error reportado en FastMCP Cloud")
                print("\n🔍 Análisis de la respuesta HTML:")

                # Buscar indicadores en el HTML
                html_content = response.text
                if "Page not found" in html_content:
                    print("   - Contiene 'Page not found'")
                if "Track Software" in html_content:
                    print("   - Contiene 'Track Software' (página de error de TrackHS)")
                if "Contact Support" in html_content:
                    print("   - Contiene enlace de soporte")

                print(f"\n📄 Preview de la respuesta HTML:")
                print("-" * 50)
                print(html_content[:500])
                print("-" * 50)

                print("\n💡 DIAGNÓSTICO:")
                print("   - El endpoint no existe en esta URL")
                print("   - La URL base podría ser incorrecta")
                print("   - Las credenciales podrían ser incorrectas")
                print("   - El endpoint podría requerir un path diferente")

                return False

            # Verificar si es JSON válido
            try:
                data = response.json()
                print("\n✅ ÉXITO: Respuesta JSON válida recibida")
                print(f"Claves en la respuesta: {list(data.keys())}")

                if "total_items" in data:
                    print(f"Total de elementos: {data['total_items']}")
                if "_embedded" in data:
                    print(f"Elementos embebidos: {list(data['_embedded'].keys())}")

                print("\n🎉 PROBLEMA RESUELTO:")
                print("   - El endpoint funciona correctamente")
                print("   - La configuración es válida")
                print("   - El problema podría estar en FastMCP Cloud")

                return True

            except json.JSONDecodeError:
                print("\n❌ ERROR: Respuesta no es JSON válido")
                print("Preview de la respuesta:")
                print("-" * 50)
                print(response.text[:500])
                print("-" * 50)
                return False

    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error {e.response.status_code}")
        print(f"Respuesta: {e.response.text[:200]}")

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
        print(f"\n❌ Error de conexión: {str(e)}")
        print("\n💡 DIAGNÓSTICO: Problema de conectividad")
        print("   - Verificar conexión a internet")
        print("   - Verificar que la URL sea accesible")
        return False

    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return False


def suggest_solutions():
    """Sugerir soluciones basadas en el diagnóstico"""
    print("\n" + "=" * 60)
    print("💡 SOLUCIONES RECOMENDADAS")
    print("=" * 60)

    print("1. 🔧 Verificar Variables de Entorno en FastMCP Cloud:")
    print("   - TRACKHS_USERNAME debe estar configurado")
    print("   - TRACKHS_PASSWORD debe estar configurado")
    print(
        "   - TRACKHS_API_URL es opcional (default: https://ihmvacations.trackhs.com/api)"
    )

    print("\n2. 🌐 Probar Diferentes URLs Base:")
    print("   - https://ihmvacations.trackhs.com/api")
    print("   - https://ihmvacations.trackhs.com")
    print("   - https://api.trackhs.com/api")
    print("   - https://api.trackhs.com")

    print("\n3. 🔍 Probar Diferentes Endpoints:")
    print("   - pms/units")
    print("   - units")
    print("   - api/pms/units")

    print("\n4. 🔐 Verificar Método de Autenticación:")
    print("   - Basic Auth (usuario/contraseña)")
    print("   - Bearer Token")
    print("   - Headers personalizados")

    print("\n5. 📋 Ejecutar Diagnósticos Completos:")
    print("   python scripts/run_full_diagnosis.py")
    print("   python scripts/test_url_variations_simple.py")
    print("   python scripts/test_auth_methods.py")


def main():
    """Función principal"""
    success = test_specific_issue()
    suggest_solutions()

    if success:
        print("\n🎉 ¡El problema está resuelto!")
        print("La configuración actual funciona correctamente.")
    else:
        print("\n❌ El problema persiste")
        print(
            "Ejecuta los scripts de diagnóstico para encontrar la configuración correcta."
        )


if __name__ == "__main__":
    main()
