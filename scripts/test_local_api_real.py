#!/usr/bin/env python3
"""
Script para probar la API real de TrackHS en local
Verifica que las URLs y credenciales funcionen antes de desplegar en FastMCP Cloud
"""

import os
import sys
import httpx
import json
from typing import Dict, Any, List, Tuple

def test_api_connection(base_url: str, username: str, password: str, endpoint: str = "pms/units") -> Dict[str, Any]:
    """Probar conexión con la API real de TrackHS"""
    full_url = f"{base_url}/{endpoint}"
    print(f"\n🔍 Probando conexión real con TrackHS API:")
    print(f"   URL: {full_url}")
    print(f"   Username: {username[:3]}***")
    print(f"   Password: {'***' if password else 'None'}")
    
    try:
        with httpx.Client(auth=(username, password), timeout=30.0) as client:
            # Probar con parámetros mínimos
            params = {"page": 1, "size": 1}
            print(f"   Parámetros: {params}")
            
            response = client.get(full_url, params=params)
            
            print(f"\n📊 RESULTADO:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content-Length: {len(response.text)}")
            
            # Verificar si es HTML (problema reportado)
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                print("\n❌ PROBLEMA: Respuesta HTML recibida")
                print("   Esto confirma el error en FastMCP Cloud")
                print(f"   Preview: {response.text[:200]}...")
                return {
                    "success": False,
                    "error": "HTML response",
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "preview": response.text[:200]
                }
            
            # Verificar si es JSON válido
            try:
                data = response.json()
                print("\n✅ ÉXITO: Respuesta JSON válida")
                print(f"   Claves en respuesta: {list(data.keys())}")
                
                if "total_items" in data:
                    print(f"   Total de elementos: {data['total_items']}")
                if "_embedded" in data and "units" in data["_embedded"]:
                    units_count = len(data["_embedded"]["units"])
                    print(f"   Unidades en esta página: {units_count}")
                
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "data_keys": list(data.keys()),
                    "total_items": data.get("total_items", "N/A"),
                    "units_count": len(data.get("_embedded", {}).get("units", []))
                }
                
            except json.JSONDecodeError:
                print("\n❌ ERROR: Respuesta no es JSON válido")
                print(f"   Preview: {response.text[:200]}...")
                return {
                    "success": False,
                    "error": "Invalid JSON",
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "preview": response.text[:200]
                }
                
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error {e.response.status_code}")
        print(f"   Respuesta: {e.response.text[:200]}...")
        
        if e.response.status_code == 401:
            print("   💡 DIAGNÓSTICO: Credenciales inválidas")
        elif e.response.status_code == 403:
            print("   💡 DIAGNÓSTICO: Acceso denegado")
        elif e.response.status_code == 404:
            print("   💡 DIAGNÓSTICO: Endpoint no encontrado")
        
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}",
            "status_code": e.response.status_code,
            "content_type": e.response.headers.get("content-type"),
            "preview": e.response.text[:200]
        }
        
    except httpx.RequestError as e:
        print(f"\n❌ Error de conexión: {str(e)}")
        return {
            "success": False,
            "error": f"Connection error: {str(e)}",
            "status_code": None,
            "content_type": None,
            "preview": str(e)
        }
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "status_code": None,
            "content_type": None,
            "preview": str(e)
        }

def test_multiple_configurations():
    """Probar múltiples configuraciones de URL y endpoint"""
    print("🔍 Probando múltiples configuraciones de URL y endpoint")
    print("=" * 80)
    
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("   Configure TRACKHS_USERNAME y TRACKHS_PASSWORD")
        return []
    
    # Diferentes configuraciones a probar
    configurations = [
        # Configuración actual
        ("https://ihmvacations.trackhs.com/api", "pms/units"),
        
        # Variaciones de URL base
        ("https://ihmvacations.trackhs.com", "api/pms/units"),
        ("https://api.trackhs.com", "pms/units"),
        ("https://api.trackhs.com/api", "pms/units"),
        
        # Variaciones de endpoint
        ("https://ihmvacations.trackhs.com/api", "units"),
        ("https://ihmvacations.trackhs.com/api", "pms/units/"),
        ("https://ihmvacations.trackhs.com/api", "api/pms/units"),
        
        # Otras posibles URLs
        ("https://trackhs.com/api", "pms/units"),
        ("https://api.trackhs.com", "units"),
    ]
    
    results = []
    
    for base_url, endpoint in configurations:
        result = test_api_connection(base_url, username, password, endpoint)
        result["base_url"] = base_url
        result["endpoint"] = endpoint
        results.append(result)
    
    return results

def test_other_endpoints(base_url: str, username: str, password: str):
    """Probar otros endpoints disponibles"""
    print(f"\n🔍 Probando otros endpoints en {base_url}")
    print("=" * 60)
    
    endpoints_to_test = [
        "pms/reservations",
        "pms/units/amenities", 
        "health",
        "status",
        "ping",
        "docs",
        "swagger",
        "openapi",
    ]
    
    results = []
    
    for endpoint in endpoints_to_test:
        print(f"\n📡 Probando endpoint: {endpoint}")
        result = test_api_connection(base_url, username, password, endpoint)
        result["endpoint"] = endpoint
        results.append(result)
    
    return results

def main():
    """Función principal"""
    print("🚀 PRUEBA LOCAL DE API REAL - TRACKHS")
    print("=" * 80)
    print("Este script prueba la conexión real con la API de TrackHS")
    print("para verificar que las URLs y credenciales funcionen correctamente")
    print("=" * 80)
    
    # Verificar credenciales
    username = os.getenv("TRACKHS_USERNAME")
    password = os.getenv("TRACKHS_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Credenciales no configuradas")
        print("\n💡 Configure las variables de entorno:")
        print("   export TRACKHS_USERNAME='tu_usuario'")
        print("   export TRACKHS_PASSWORD='tu_password'")
        print("\n   O cree un archivo .env con:")
        print("   TRACKHS_USERNAME=tu_usuario")
        print("   TRACKHS_PASSWORD=tu_password")
        return
    
    print(f"✅ Credenciales encontradas:")
    print(f"   Username: {username[:3]}***")
    print(f"   Password: {'***' if password else 'None'}")
    
    # Probar múltiples configuraciones
    print(f"\n{'='*20} PROBANDO CONFIGURACIONES {'='*20}")
    config_results = test_multiple_configurations()
    
    # Analizar resultados
    successful_configs = [r for r in config_results if r["success"]]
    failed_configs = [r for r in config_results if not r["success"]]
    
    print(f"\n📊 RESUMEN DE CONFIGURACIONES:")
    print(f"   Configuraciones exitosas: {len(successful_configs)}")
    print(f"   Configuraciones fallidas: {len(failed_configs)}")
    
    if successful_configs:
        print(f"\n✅ CONFIGURACIONES EXITOSAS:")
        for i, result in enumerate(successful_configs, 1):
            print(f"   {i}. {result['base_url']}/{result['endpoint']}")
            print(f"      Status: {result['status_code']}")
            print(f"      Total Items: {result.get('total_items', 'N/A')}")
            print(f"      Units: {result.get('units_count', 'N/A')}")
        
        # Probar otros endpoints con la configuración exitosa
        best_config = successful_configs[0]
        print(f"\n🔍 Probando otros endpoints con la mejor configuración:")
        print(f"   Base URL: {best_config['base_url']}")
        
        other_results = test_other_endpoints(best_config['base_url'], username, password)
        
        successful_endpoints = [r for r in other_results if r["success"]]
        if successful_endpoints:
            print(f"\n✅ ENDPOINTS ADICIONALES EXITOSOS:")
            for result in successful_endpoints:
                print(f"   - {result['endpoint']} (Status: {result['status_code']})")
    
    if failed_configs:
        print(f"\n❌ CONFIGURACIONES FALLIDAS:")
        for i, result in enumerate(failed_configs, 1):
            print(f"   {i}. {result['base_url']}/{result['endpoint']}")
            print(f"      Error: {result['error']}")
            if result['status_code']:
                print(f"      Status: {result['status_code']}")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES:")
    if successful_configs:
        best = successful_configs[0]
        print(f"✅ USAR ESTA CONFIGURACIÓN:")
        print(f"   Base URL: {best['base_url']}")
        print(f"   Endpoint: {best['endpoint']}")
        print(f"   Esta configuración funciona correctamente con la API real")
        
        print(f"\n🔧 CONFIGURACIÓN PARA FASTMCP CLOUD:")
        print(f"   TRACKHS_API_URL={best['base_url']}")
        print(f"   TRACKHS_USERNAME={username}")
        print(f"   TRACKHS_PASSWORD={password}")
        
        print(f"\n📝 NOTA:")
        print(f"   El endpoint '{best['endpoint']}' funciona correctamente")
        print(f"   Esto debería resolver el problema en FastMCP Cloud")
        
    else:
        print(f"❌ NINGUNA CONFIGURACIÓN FUNCIONÓ")
        print(f"   Posibles problemas:")
        print(f"   - Credenciales incorrectas")
        print(f"   - URL base incorrecta")
        print(f"   - API no disponible")
        print(f"   - Problemas de red")
        
        print(f"\n🔍 PRÓXIMOS PASOS:")
        print(f"   1. Verificar credenciales con TrackHS")
        print(f"   2. Verificar URL base correcta")
        print(f"   3. Contactar soporte técnico de TrackHS")
    
    # Guardar resultados
    results_file = "local_api_test_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": os.popen("date").read().strip(),
            "username_configured": bool(username),
            "password_configured": bool(password),
            "successful_configs": len(successful_configs),
            "failed_configs": len(failed_configs),
            "config_results": config_results,
            "recommendations": {
                "best_config": successful_configs[0] if successful_configs else None,
                "fastmcp_cloud_config": {
                    "TRACKHS_API_URL": successful_configs[0]["base_url"] if successful_configs else None,
                    "TRACKHS_USERNAME": username,
                    "TRACKHS_PASSWORD": "***"
                }
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Resultados guardados en: {results_file}")

if __name__ == "__main__":
    main()
