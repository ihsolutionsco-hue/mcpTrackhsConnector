#!/usr/bin/env python3
"""
Script simple para probar diferentes variaciones de URL base
"""

import os
import sys
import httpx
import json

def test_url_variation(base_url: str, endpoint: str, username: str, password: str):
    """Probar una variación específica de URL"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔍 Probando: {full_url}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=10.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if "text/html" in response.headers.get("content-type", ""):
                print("   ❌ Respuesta HTML - endpoint incorrecto")
                return False
            
            try:
                data = response.json()
                print("   ✅ Respuesta JSON válida")
                print(f"   Claves: {list(data.keys())}")
                return True
            except json.JSONDecodeError:
                print("   ❌ No es JSON válido")
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP {e.response.status_code}: {e.response.text[:100]}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔍 Probando variaciones de URL para FastMCP Cloud")
    print("=" * 60)
    
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        return
    
    # Variaciones a probar
    variations = [
        # Configuración actual
        ("https://ihmvacations.trackhs.com/api", "pms/units"),
        
        # Sin /api al final
        ("https://ihmvacations.trackhs.com", "api/pms/units"),
        
        # Diferentes dominios
        ("https://api.trackhs.com", "pms/units"),
        ("https://api.trackhs.com/api", "pms/units"),
        
        # Sin /pms
        ("https://ihmvacations.trackhs.com/api", "units"),
        
        # Con trailing slash
        ("https://ihmvacations.trackhs.com/api/", "pms/units"),
        ("https://ihmvacations.trackhs.com/api", "pms/units/"),
    ]
    
    successful = []
    
    for base_url, endpoint in variations:
        if test_url_variation(base_url, endpoint, username, password):
            successful.append((base_url, endpoint))
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)
    
    if successful:
        print(f"✅ {len(successful)} configuración(es) exitosa(s):")
        for i, (base_url, endpoint) in enumerate(successful, 1):
            print(f"   {i}. {base_url}/{endpoint}")
        
        print(f"\n💡 RECOMENDACIÓN:")
        best = successful[0]
        print(f"   Usar: {best[0]}")
        print(f"   Endpoint: {best[1]}")
    else:
        print("❌ Ninguna configuración funcionó")
        print("💡 Posibles problemas:")
        print("   - Credenciales incorrectas")
        print("   - URL base incorrecta")
        print("   - Endpoint no disponible")

if __name__ == "__main__":
    main()
