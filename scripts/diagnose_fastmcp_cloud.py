#!/usr/bin/env python3
"""
Script de diagnóstico para FastMCP Cloud - TrackHS API
Prueba diferentes configuraciones de URL y credenciales para identificar el problema
"""

import os
import sys
import httpx
import json
from typing import Dict, Any, List, Tuple

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_url_configuration(base_url: str, username: str, password: str, endpoint: str = "pms/units") -> Dict[str, Any]:
    """Probar una configuración específica de URL"""
    print(f"\n🔍 Probando configuración:")
    print(f"   Base URL: {base_url}")
    print(f"   Endpoint: {endpoint}")
    print(f"   Username: {username[:3]}***" if username else "None")
    print(f"   Password: {'***' if password else 'None'}")
    
    full_url = f"{base_url}/{endpoint}"
    print(f"   URL completa: {full_url}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=10.0) as client:
            response = client.get(full_url, params={"page": 1, "size": 1})
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content-Length: {len(response.text)}")
            
            # Verificar si la respuesta es HTML
            if "text/html" in response.headers.get("content-type", ""):
                print("   ⚠️  Respuesta HTML detectada - posible endpoint incorrecto")
                print(f"   Preview: {response.text[:200]}...")
                return {
                    "success": False,
                    "error": "HTML response received",
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type"),
                    "preview": response.text[:200]
                }
            
            # Verificar si la respuesta es JSON válido
            try:
                json_data = response.json()
                print("   ✅ Respuesta JSON válida recibida")
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type"),
                    "data_keys": list(json_data.keys()) if isinstance(json_data, dict) else "Not a dict",
                    "total_items": json_data.get("total_items", "N/A") if isinstance(json_data, dict) else "N/A"
                }
            except json.JSONDecodeError:
                print("   ❌ Respuesta no es JSON válido")
                print(f"   Preview: {response.text[:200]}...")
                return {
                    "success": False,
                    "error": "Invalid JSON response",
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type"),
                    "preview": response.text[:200]
                }
                
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error {e.response.status_code}: {e.response.text[:200]}")
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}",
            "status_code": e.response.status_code,
            "content_type": e.response.headers.get("content-type"),
            "preview": e.response.text[:200]
        }
    except httpx.RequestError as e:
        print(f"   ❌ Request Error: {str(e)}")
        return {
            "success": False,
            "error": f"Request error: {str(e)}",
            "status_code": None,
            "content_type": None,
            "preview": str(e)
        }
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "status_code": None,
            "content_type": None,
            "preview": str(e)
        }

def main():
    """Función principal de diagnóstico"""
    print("🚀 Diagnóstico de FastMCP Cloud - TrackHS API")
    print("=" * 60)
    
    # Obtener credenciales de variables de entorno
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: TRACKHS_USERNAME y TRACKHS_PASSWORD no están configurados")
        print("   Configure las variables de entorno antes de ejecutar este script")
        return
    
    print(f"✅ Credenciales encontradas:")
    print(f"   Username: {username[:3]}***")
    print(f"   Password: {'***' if password else 'None'}")
    
    # Diferentes configuraciones de URL para probar
    url_configurations = [
        # Configuración actual
        ("https://ihmvacations.trackhs.com/api", "pms/units"),
        
        # Posibles variaciones
        ("https://ihmvacations.trackhs.com", "api/pms/units"),
        ("https://api.trackhs.com", "pms/units"),
        ("https://api.trackhs.com/api", "pms/units"),
        ("https://ihmvacations.trackhs.com/api", "units"),
        ("https://ihmvacations.trackhs.com/api", "pms/units/"),
        
        # Otras posibles URLs
        ("https://trackhs.com/api", "pms/units"),
        ("https://api.trackhs.com/api", "pms/units"),
    ]
    
    results = []
    
    for base_url, endpoint in url_configurations:
        result = test_url_configuration(base_url, username, password, endpoint)
        result["base_url"] = base_url
        result["endpoint"] = endpoint
        results.append(result)
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    successful_configs = [r for r in results if r["success"]]
    failed_configs = [r for r in results if not r["success"]]
    
    print(f"✅ Configuraciones exitosas: {len(successful_configs)}")
    print(f"❌ Configuraciones fallidas: {len(failed_configs)}")
    
    if successful_configs:
        print("\n🎉 CONFIGURACIONES EXITOSAS:")
        for i, result in enumerate(successful_configs, 1):
            print(f"   {i}. {result['base_url']}/{result['endpoint']}")
            print(f"      Status: {result['status_code']}")
            print(f"      Content-Type: {result['content_type']}")
            if 'total_items' in result:
                print(f"      Total Items: {result['total_items']}")
    
    if failed_configs:
        print("\n❌ CONFIGURACIONES FALLIDAS:")
        for i, result in enumerate(failed_configs, 1):
            print(f"   {i}. {result['base_url']}/{result['endpoint']}")
            print(f"      Error: {result['error']}")
            if result['status_code']:
                print(f"      Status: {result['status_code']}")
            if result['content_type']:
                print(f"      Content-Type: {result['content_type']}")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    if successful_configs:
        best_config = successful_configs[0]
        print(f"   ✅ Usar: {best_config['base_url']}")
        print(f"   ✅ Endpoint: {best_config['endpoint']}")
        print(f"   ✅ Esta configuración funciona correctamente")
    else:
        print("   ❌ Ninguna configuración funcionó")
        print("   🔍 Posibles problemas:")
        print("      - Credenciales incorrectas")
        print("      - URL base incorrecta")
        print("      - Endpoint no disponible")
        print("      - Problemas de red o firewall")
    
    # Guardar resultados en archivo
    results_file = "fastmcp_cloud_diagnosis.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": os.popen("date").read().strip(),
            "username_configured": bool(username),
            "password_configured": bool(password),
            "total_tests": len(results),
            "successful_tests": len(successful_configs),
            "failed_tests": len(failed_configs),
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Resultados guardados en: {results_file}")

if __name__ == "__main__":
    main()
