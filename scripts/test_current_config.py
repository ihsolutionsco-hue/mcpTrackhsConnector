#!/usr/bin/env python3
"""
Script simple para probar la configuración actual de FastMCP Cloud
"""

import os
import sys
import httpx
import json

def test_current_config():
    """Probar la configuración actual"""
    print("🔍 Probando configuración actual de FastMCP Cloud")
    print("=" * 50)
    
    # Obtener configuración actual
    base_url = os.getenv("TRACKHS_API_URL", "https://ihmvacations.trackhs.com/api")
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    print(f"Base URL: {base_url}")
    print(f"Username: {username[:3]}***" if username else "None")
    print(f"Password: {'***' if password else 'None'}")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        return False
    
    # Probar endpoint de unidades
    endpoint = "pms/units"
    full_url = f"{base_url}/{endpoint}"
    print(f"\nURL completa: {full_url}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=10.0) as client:
            print("🔄 Enviando petición...")
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"Content-Length: {len(response.text)}")
            
            # Verificar si es HTML
            if "text/html" in response.headers.get("content-type", ""):
                print("❌ Respuesta HTML recibida - posible problema de endpoint")
                print("Preview de respuesta:")
                print("-" * 30)
                print(response.text[:500])
                print("-" * 30)
                return False
            
            # Intentar parsear JSON
            try:
                data = response.json()
                print("✅ Respuesta JSON válida")
                print(f"Claves en la respuesta: {list(data.keys())}")
                if "total_items" in data:
                    print(f"Total de elementos: {data['total_items']}")
                return True
            except json.JSONDecodeError:
                print("❌ Respuesta no es JSON válido")
                print("Preview de respuesta:")
                print("-" * 30)
                print(response.text[:500])
                print("-" * 30)
                return False
                
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error {e.response.status_code}")
        print("Respuesta:")
        print("-" * 30)
        print(e.response.text[:500])
        print("-" * 30)
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_current_config()
    if success:
        print("\n🎉 ¡Configuración actual funciona correctamente!")
    else:
        print("\n❌ La configuración actual no funciona")
        print("💡 Ejecuta 'python scripts/diagnose_fastmcp_cloud.py' para probar otras configuraciones")
