#!/usr/bin/env python3
"""
Script para probar diferentes métodos de autenticación en local
con la API real de TrackHS
"""

import os
import sys
import httpx
import json

def test_basic_auth_local(base_url: str, endpoint: str, username: str, password: str):
    """Probar autenticación básica en local"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔐 Probando autenticación básica:")
    print(f"   URL: {full_url}")
    print(f"   Username: {username[:3]}***")
    print(f"   Password: {'***' if password else 'None'}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=30.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Autenticación básica exitosa")
                    print(f"   Claves: {list(data.keys())}")
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

def test_bearer_auth_local(base_url: str, endpoint: str, username: str, password: str):
    """Probar autenticación Bearer en local"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔐 Probando autenticación Bearer:")
    print(f"   URL: {full_url}")
    print(f"   Token: {username[:3]}***")
    
    try:
        headers = {"Authorization": f"Bearer {username}"}
        with httpx.Client(headers=headers, timeout=30.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Autenticación Bearer exitosa")
                    print(f"   Claves: {list(data.keys())}")
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

def test_custom_headers_local(base_url: str, endpoint: str, username: str, password: str):
    """Probar headers personalizados en local"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔐 Probando headers personalizados:")
    print(f"   URL: {full_url}")
    print(f"   API Key: {username[:3]}***")
    print(f"   API Secret: {'***' if password else 'None'}")
    
    try:
        headers = {
            "X-API-Key": username,
            "X-API-Secret": password,
            "Content-Type": "application/json"
        }
        with httpx.Client(headers=headers, timeout=30.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Headers personalizados exitosos")
                    print(f"   Claves: {list(data.keys())}")
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

def test_api_key_auth_local(base_url: str, endpoint: str, username: str, password: str):
    """Probar autenticación con API Key en local"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔐 Probando autenticación con API Key:")
    print(f"   URL: {full_url}")
    print(f"   API Key: {username[:3]}***")
    
    try:
        headers = {"X-API-Key": username}
        with httpx.Client(headers=headers, timeout=30.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("   ✅ Autenticación con API Key exitosa")
                    print(f"   Claves: {list(data.keys())}")
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
    print("🔐 PRUEBA DE MÉTODOS DE AUTENTICACIÓN EN LOCAL")
    print("=" * 80)
    print("Este script prueba diferentes métodos de autenticación")
    print("con la API real de TrackHS para encontrar el método correcto")
    print("=" * 80)
    
    # Obtener credenciales
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("\n💡 Configure las variables de entorno:")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")
        return
    
    # URL base a probar
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
    endpoint = "pms/units"
    
    print(f"Base URL: {base_url}")
    print(f"Endpoint: {endpoint}")
    print(f"Username: {username[:3]}***")
    print(f"Password: {'***' if password else 'None'}")
    
    # Probar diferentes métodos de autenticación
    auth_methods = [
        ("Basic Auth", test_basic_auth_local),
        ("Bearer Token", test_bearer_auth_local),
        ("Custom Headers", test_custom_headers_local),
        ("API Key", test_api_key_auth_local),
    ]
    
    successful_methods = []
    
    for method_name, test_func in auth_methods:
        print(f"\n{'='*20} {method_name} {'='*20}")
        if test_func(base_url, endpoint, username, password):
            successful_methods.append(method_name)
    
    # Resumen de resultados
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    if successful_methods:
        print(f"✅ Métodos exitosos: {', '.join(successful_methods)}")
        print(f"\n💡 RECOMENDACIÓN: Usar {successful_methods[0]}")
        
        print(f"\n🔧 CONFIGURACIÓN PARA FASTMCP CLOUD:")
        print(f"   TRACKHS_API_URL={base_url}")
        print(f"   TRACKHS_USERNAME={username}")
        print(f"   TRACKHS_PASSWORD={password}")
        
        if successful_methods[0] == "Basic Auth":
            print(f"\n📝 NOTA:")
            print(f"   El método Basic Auth funciona correctamente")
            print(f"   Esto debería resolver el problema en FastMCP Cloud")
        elif successful_methods[0] == "Bearer Token":
            print(f"\n📝 NOTA:")
            print(f"   El método Bearer Token funciona correctamente")
            print(f"   Podrías necesitar modificar el código para usar Bearer Token")
        elif successful_methods[0] == "Custom Headers":
            print(f"\n📝 NOTA:")
            print(f"   El método Custom Headers funciona correctamente")
            print(f"   Podrías necesitar modificar el código para usar headers personalizados")
        elif successful_methods[0] == "API Key":
            print(f"\n📝 NOTA:")
            print(f"   El método API Key funciona correctamente")
            print(f"   Podrías necesitar modificar el código para usar API Key")
        
    else:
        print("❌ Ningún método de autenticación funcionó")
        print("\n💡 Posibles problemas:")
        print("   - Credenciales incorrectas")
        print("   - URL base incorrecta")
        print("   - Endpoint no disponible")
        print("   - Método de autenticación no soportado")
        
        print(f"\n🔍 PRÓXIMOS PASOS:")
        print("   1. Verificar credenciales con TrackHS")
        print("   2. Probar diferentes URLs:")
        print("      - python scripts/test_local_api_real.py")
        print("   3. Contactar soporte técnico de TrackHS")
    
    # Guardar resultados
    results_file = "auth_methods_test_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": os.popen("date").read().strip(),
            "base_url": base_url,
            "endpoint": endpoint,
            "username_configured": bool(username),
            "password_configured": bool(password),
            "successful_methods": successful_methods,
            "total_methods": len(auth_methods),
            "success_rate": (len(successful_methods) / len(auth_methods)) * 100
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Resultados guardados en: {results_file}")

if __name__ == "__main__":
    main()
