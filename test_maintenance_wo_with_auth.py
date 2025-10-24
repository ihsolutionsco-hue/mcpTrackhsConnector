#!/usr/bin/env python3
"""
Script de prueba con autenticación para la API de TrackHS
Usa las mismas credenciales que el MCP
"""

import asyncio
import json
import httpx
import base64
import os
from datetime import datetime

# Configuración de la API
BASE_URL = "https://api-integration-example.tracksandbox.io"
ENDPOINT = "/api/pms/maintenance/work-orders"

# Cargar credenciales del archivo .env si existe
def load_env_credentials():
    """Cargar credenciales del archivo .env"""
    credentials = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key] = value
    except FileNotFoundError:
        print("⚠️ Archivo .env no encontrado")
    
    return credentials

# Cargar credenciales
env_vars = load_env_credentials()
username = env_vars.get('TRACKHS_USERNAME', 'demo_user')
password = env_vars.get('TRACKHS_PASSWORD', 'demo_password')

print(f"🔐 Usando credenciales: {username}")

# Crear headers con autenticación básica
auth_string = f"{username}:{password}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth_b64}"
}

# Payload de prueba
TEST_PAYLOAD = {
    "dateReceived": "2025-01-24",
    "priority": 5,
    "status": "open",
    "summary": "Test work order - Aire acondicionado no funciona",
    "estimatedCost": 150.0,
    "estimatedTime": 120
}

async def test_with_authentication():
    """Probar con autenticación"""
    print("🔐 PROBANDO CON AUTENTICACIÓN")
    print("=" * 50)
    
    print(f"📡 URL: {BASE_URL}{ENDPOINT}")
    print(f"🔑 Auth: Basic {auth_b64[:20]}...")
    print(f"📦 Payload: {json.dumps(TEST_PAYLOAD, indent=2)}")
    print()
    
    async with httpx.AsyncClient() as client:
        try:
            print("🚀 Enviando petición POST con autenticación...")
            response = await client.post(
                f"{BASE_URL}{ENDPOINT}",
                json=TEST_PAYLOAD,
                headers=HEADERS,
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(response.headers)}")
            print()
            
            if response.is_success:
                print("✅ ÉXITO - Work Order creado")
                result = response.json()
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ ERROR - Falló la creación")
                print(f"📄 Response Body: {response.text}")
                
                # Intentar parsear como JSON para ver detalles
                try:
                    error_json = response.json()
                    print(f"📄 Error JSON: {json.dumps(error_json, indent=2)}")
                    
                    # Mostrar mensajes de validación si existen
                    if 'validation_messages' in error_json:
                        print(f"🔍 Validation Messages: {error_json['validation_messages']}")
                    if 'detail' in error_json:
                        print(f"🔍 Detail: {error_json['detail']}")
                        
                except Exception as e:
                    print(f"⚠️ No se pudo parsear como JSON: {e}")
                    
                return False
                    
        except httpx.RequestError as e:
            print(f"🌐 Error de red: {e}")
            return False
        except Exception as e:
            print(f"💥 Error inesperado: {e}")
            return False

async def test_different_endpoints():
    """Probar diferentes endpoints para ver cuál funciona"""
    print("\n" + "=" * 50)
    print("🔄 PROBANDO DIFERENTES ENDPOINTS")
    print("=" * 50)
    
    endpoints = [
        "/api/pms/maintenance/work-orders",
        "/pms/maintenance/work-orders", 
        "/api/maintenance/work-orders",
        "/maintenance/work-orders"
    ]
    
    async with httpx.AsyncClient() as client:
        for endpoint in endpoints:
            print(f"\n🧪 Probando endpoint: {endpoint}")
            
            try:
                response = await client.post(
                    f"{BASE_URL}{endpoint}",
                    json=TEST_PAYLOAD,
                    headers=HEADERS,
                    timeout=30.0
                )
                
                print(f"📊 Status: {response.status_code}")
                
                if response.is_success:
                    print("✅ ÉXITO - Endpoint funciona")
                    result = response.json()
                    print(f"📄 Work Order ID: {result.get('id', 'N/A')}")
                    return endpoint
                else:
                    print(f"❌ Error: {response.status_code}")
                    if response.status_code == 404:
                        print("🔍 Endpoint no encontrado")
                    elif response.status_code == 403:
                        print("🔍 Problema de autenticación")
                    elif response.status_code == 422:
                        print("🔍 Problema de validación de datos")
                        print(f"📄 Response: {response.text}")
                        
            except Exception as e:
                print(f"💥 Error: {e}")
    
    return None

if __name__ == "__main__":
    print("🔧 TRACKHS API - CREATE MAINTENANCE WORK ORDER TEST (WITH AUTH)")
    print("=" * 70)
    
    # Ejecutar pruebas
    success = asyncio.run(test_with_authentication())
    
    if not success:
        print("\n🔄 Probando diferentes endpoints...")
        working_endpoint = asyncio.run(test_different_endpoints())
        
        if working_endpoint:
            print(f"\n✅ Endpoint que funciona: {working_endpoint}")
        else:
            print("\n❌ Ningún endpoint funcionó")
    
    print("\n" + "=" * 70)
    print("🏁 PRUEBAS COMPLETADAS")
