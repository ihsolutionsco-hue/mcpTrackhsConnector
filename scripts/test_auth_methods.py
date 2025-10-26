#!/usr/bin/env python3
"""
Script para probar diferentes métodos de autenticación
"""

import os
import sys
import httpx
import json
import base64

def test_basic_auth(base_url: str, endpoint: str, username: str, password: str):
    """Probar autenticación básica"""
    print(f"\n🔐 Probando autenticación básica: {base_url}/{endpoint}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=10.0) as client:
            response = client.get(f"{base_url}/{endpoint}", params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Autenticación básica exitosa")
                    return True
                except json.JSONDecodeError:
                    print("   ❌ Respuesta no es JSON")
                    return False
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                print(f"   Respuesta: {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_bearer_auth(base_url: str, endpoint: str, username: str, password: str):
    """Probar autenticación Bearer (si las credenciales son un token)"""
    print(f"\n🔐 Probando autenticación Bearer: {base_url}/{endpoint}")
    
    try:
        headers = {"Authorization": f"Bearer {username}"}
        with httpx.Client(headers=headers, timeout=10.0) as client:
            response = client.get(f"{base_url}/{endpoint}", params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Autenticación Bearer exitosa")
                    return True
                except json.JSONDecodeError:
                    print("   ❌ Respuesta no es JSON")
                    return False
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_custom_headers(base_url: str, endpoint: str, username: str, password: str):
    """Probar con headers personalizados"""
    print(f"\n🔐 Probando headers personalizados: {base_url}/{endpoint}")
    
    try:
        headers = {
            "X-API-Key": username,
            "X-API-Secret": password,
            "Content-Type": "application/json"
        }
        with httpx.Client(headers=headers, timeout=10.0) as client:
            response = client.get(f"{base_url}/{endpoint}", params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Headers personalizados exitosos")
                    return True
                except json.JSONDecodeError:
                    print("   ❌ Respuesta no es JSON")
                    return False
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔐 Probando diferentes métodos de autenticación")
    print("=" * 60)
    
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        return
    
    # URL base a probar
    base_url = "https://ihmvacations.trackhs.com/api"
    endpoint = "pms/units"
    
    print(f"Base URL: {base_url}")
    print(f"Endpoint: {endpoint}")
    print(f"Username: {username[:3]}***")
    print(f"Password: {'***' if password else 'None'}")
    
    # Probar diferentes métodos de autenticación
    methods = [
        ("Basic Auth", test_basic_auth),
        ("Bearer Token", test_bearer_auth),
        ("Custom Headers", test_custom_headers),
    ]
    
    successful_methods = []
    
    for method_name, test_func in methods:
        print(f"\n{'='*20} {method_name} {'='*20}")
        if test_func(base_url, endpoint, username, password):
            successful_methods.append(method_name)
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)
    
    if successful_methods:
        print(f"✅ Métodos exitosos: {', '.join(successful_methods)}")
        print(f"\n💡 RECOMENDACIÓN: Usar {successful_methods[0]}")
    else:
        print("❌ Ningún método de autenticación funcionó")
        print("💡 Posibles problemas:")
        print("   - Credenciales incorrectas")
        print("   - URL base incorrecta")
        print("   - Endpoint no disponible")
        print("   - Método de autenticación no soportado")

if __name__ == "__main__":
    main()
